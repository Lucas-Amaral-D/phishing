"""Experimentos reproduzíveis executados exclusivamente no desenvolvimento."""
import json
import platform
import warnings
from datetime import datetime, timezone
from time import perf_counter
from uuid import uuid4

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.base import clone
from sklearn.inspection import permutation_importance
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold
from threadpoolctl import threadpool_limits

from .config import ROOT, UCI_CSV_SHA256
from .data_loader import sha256
from .evaluation import metrics
from .feature_audit import scenario_features
from .feature_extraction import domain_group
from .models import SEARCH, SEED, models
from .preprocessing import pipeline_for
from .splitting import SPLITS, grouped_folds, load_rows

EXPERIMENTS = ROOT / "results" / "experiments"
MODELS = ROOT / "models"


def save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def pipeline(name, frame):
    return pipeline_for(frame, models()[name], scaled=name == "logistica")


def score_fold(estimator, x, y, train, valid):
    started = perf_counter()
    estimator.fit(x.iloc[train], y[train])
    fit = perf_counter() - started
    started = perf_counter()
    scores = estimator.predict_proba(x.iloc[valid])[:, 1]
    elapsed = perf_counter() - started
    return {"fit_s": fit, "inference_s": elapsed, **metrics(y[valid], scores)}, scores


def evaluate_cv(estimator, x, y, folds, destination, key):
    rows = []
    out = np.empty(len(y))
    for index, (train, valid) in enumerate(folds):
        result, out[valid] = score_fold(clone(estimator), x, y, train, valid)
        rows.append({"fold": index, "train_rows": len(train), "valid_rows": len(valid), **result})
    table = pd.DataFrame(rows)
    table.to_csv(destination / f"{key}.csv", index=False)
    return table.f1.mean(), table.f1.std(), out


def tune(name, x, y, train, valid, inner, destination):
    base = pipeline(name, x)
    params = {f"model__{key}": values for key, values in SEARCH[name].items()}
    search = RandomizedSearchCV(
        base, params, n_iter=2, cv=inner, scoring="f1", n_jobs=1, random_state=SEED,
        refit=False, error_score="raise",
    )
    started = perf_counter()
    search.fit(x.iloc[train], y[train])
    seconds = perf_counter() - started
    pd.DataFrame(search.cv_results_).to_csv(destination / f"busca_{name}.csv", index=False)
    estimator = clone(base).set_params(**search.best_params_)
    baseline, _ = score_fold(base, x, y, train, valid)
    optimized, _ = score_fold(estimator, x, y, train, valid)
    save_json(destination / f"busca_{name}.json", {
        "strategy": "RandomizedSearchCV", "space": params, "folds": len(inner),
        "combinations": 2, "metric": "f1", "seconds": seconds, "best": search.best_params_,
        "baseline_holdout": baseline, "optimized_holdout": optimized,
    })
    return estimator


def explain(estimator, x, y, train, valid, threshold, destination, key):
    subset = np.random.default_rng(SEED).choice(valid, min(4000, len(valid)), replace=False)
    explanation = permutation_importance(
        estimator, x.iloc[subset], y[subset], n_repeats=3, random_state=SEED, scoring="f1",
    )
    pd.DataFrame({
        "atributo": x.columns, "media_f1": explanation.importances_mean,
        "desvio": explanation.importances_std,
    }).sort_values("media_f1", ascending=False).to_csv(destination / f"importancia_{key}.csv",
                                                       index=False)
    scores = estimator.predict_proba(x.iloc[valid])[:, 1]
    predicted = scores >= threshold
    errors = x.iloc[valid].copy()
    errors.insert(0, "row_id", x.index[valid])
    errors["expected"] = y[valid]
    errors["score"] = scores
    errors["type"] = np.select(
        [(y[valid] == 0) & predicted, (y[valid] == 1) & ~predicted, y[valid] == 1],
        ["FP", "FN", "TP"], default="TN",
    )
    feature = "comprimento" if key == "C" else "URLLength"
    errors["length"] = pd.cut(errors[feature], [0, 35, 75, 150, np.inf], include_lowest=True)
    pd.crosstab(errors["length"], errors["type"]).to_csv(destination / f"erros_{key}.csv")
    errors["distancia"] = np.abs(scores - threshold)
    local = pd.concat([errors.groupby("type").head(3), errors.nsmallest(5, "distancia")]).drop_duplicates()
    selected = local[["row_id", "expected", "score", "type", feature, "distancia"]].copy()
    relevant = x.columns[np.argsort(explanation.importances_mean)[-3:]]
    source_rows = x.loc[selected.row_id]
    for column in relevant:
        changed = source_rows.copy()
        changed[column] = x.iloc[train][column].mode().iat[0]
        selected[f"delta_moda_{column}"] = (
            estimator.predict_proba(changed)[:, 1] - selected.score.to_numpy()
        )
    selected.to_csv(destination / f"casos_{key}.csv", index=False)


def run(quick=False):
    destination = EXPERIMENTS / (("rapido-" if quick else "completo-") + uuid4().hex)
    destination.mkdir(parents=True)
    print(f"Experimento: {destination.name}", flush=True)
    metadata = {
        "state": "started", "utc": datetime.now(timezone.utc).isoformat(), "quick": quick,
        "python": platform.python_version(), "platform": platform.platform(),
        "sklearn": sklearn.__version__, "seed": SEED, "dataset_sha256": UCI_CSV_SHA256,
        "dev_sha256": sha256(SPLITS / "dev.npy"),
    }
    save_json(destination / "metadata.json", metadata)
    try:
        with warnings.catch_warnings(record=True) as caught, threadpool_limits(limits=4):
            warnings.simplefilter("always")
            conduct(destination, quick)
        metadata["warnings"] = sorted({str(item.message) for item in caught})
        metadata["state"] = "complete"
    except Exception as error:
        metadata.update(state="failed", error=f"{type(error).__name__}: {error}")
        raise
    finally:
        save_json(destination / "metadata.json", metadata)
    return destination


def conduct(destination, quick):
    frame = load_rows("dev")
    if quick:
        frame = frame.sample(n=min(2500, len(frame)), random_state=SEED)
    y = 1 - frame.label.to_numpy()
    groups = frame.URL.map(domain_group).to_numpy()
    folds = grouped_folds(y, groups)
    train, valid = folds[0]
    inner = grouped_folds(y[train], groups[train])
    random = list(StratifiedKFold(5, shuffle=True, random_state=SEED).split(y, y))
    fold_audit = [
        {"fold": i, "train_rows": len(tr), "validation_rows": len(va),
         "train_phishing_fraction": y[tr].mean(), "validation_phishing_fraction": y[va].mean(),
         "group_overlap": len(set(groups[tr]) & set(groups[va]))}
        for i, (tr, va) in enumerate(folds)
    ]
    save_json(destination / "folds.json", fold_audit)
    np.savez_compressed(destination / "fold_indices.npz", **{
        f"validation_{i}": frame.index[va].to_numpy() for i, (_, va) in enumerate(folds)
    })
    variants = scenario_features(frame)
    config = {
        scenario: {name: {"features": list(x.columns), "pipeline": repr(pipeline(name, x)),
                          "parameters": models()[name].get_params()}
                   for name in models()}
        for scenario, x in variants.items()
    }
    save_json(destination / "config.json", config)
    print("Baselines agrupados", flush=True)
    records = []
    for scenario in ["B", "A", "C"]:
        x = variants[scenario]
        names = list(models()) if scenario != "A" else ["logistica", "boosting"]
        for name in names:
            mean, sd, _ = evaluate_cv(
                pipeline(name, x), x, y, folds, destination, f"{scenario}_{name}",
            )
            records.append({"scenario": scenario, "model": name, "mean_f1": mean, "sd_f1": sd})
            print(f"{scenario} {name}: F1 {mean:.4f}", flush=True)
    summary = pd.DataFrame(records)
    summary.to_csv(destination / "comparacao.csv", index=False)
    print("Busca de hiperparâmetros", flush=True)
    tuned = {name: tune(name, variants["B"], y, train, valid, inner, destination) for name in SEARCH}

    print("Comparações, limiares e explicabilidade", flush=True)
    for scenario in variants:
        x = variants[scenario]
        evaluate_cv(pipeline("boosting", x), x, y, random, destination, f"{scenario}_aleatorio")
    final = {}
    candidates_rows = []
    for scenario in ["B", "C"]:
        x = variants[scenario]
        candidates = {name: pipeline(name, x) for name in models() if name != "dummy"}
        if scenario == "B":
            candidates.update({f"{name}_otimizado": model for name, model in tuned.items()})
        evaluated = {}
        for name, estimator in candidates.items():
            result, scores = score_fold(estimator, x, y, train, valid)
            evaluated[name] = (result, scores)
            candidates_rows.append({"scenario": scenario, "model": name, **result})
        best = max(result["f1"] for result, _ in evaluated.values())
        close = [name for name, (result, _) in evaluated.items() if best - result["f1"] <= .002]
        # As médias basais fornecem uma referência de estabilidade por família.
        sd = summary[summary.scenario.eq(scenario)].set_index("model").sd_f1
        winner = max(close, key=lambda name: (
            evaluated[name][0]["recall"], -sd[name.removesuffix("_otimizado")],
            -evaluated[name][0]["inference_s"],
        ))
        selected = candidates[winner]
        estimator = clone(selected)
        # A validação interna compara candidatos e define o ponto de corte; seu F1 é descritivo.
        holdout_scores = evaluated[winner][1]
        thresholds = [{
            "threshold": float(level), **metrics(y[valid], holdout_scores, level)
        } for level in np.linspace(.1, .9, 33)]
        pd.DataFrame(thresholds).to_csv(destination / f"limiar_{scenario}.csv", index=False)
        chosen = max(thresholds, key=lambda row: (row["f1"], row["recall"]))
        threshold = chosen["threshold"]
        selected.fit(x.iloc[train], y[train])
        explain(selected, x, y, train, valid, threshold, destination, scenario)
        learning = []
        rng = np.random.default_rng(SEED)
        shuffled = rng.permutation(train)
        for fraction in [.25, .5, 1.]:
            subset = shuffled[:int(fraction * len(shuffled))]
            result, _ = score_fold(clone(estimator), x, y, subset, valid)
            learning.append({"fraction": fraction, "rows": len(subset), **result})
        pd.DataFrame(learning).to_csv(destination / f"aprendizado_{scenario}.csv", index=False)
        if not quick:
            MODELS.mkdir(exist_ok=True)
            start = perf_counter()
            estimator.fit(x, y)
            seconds = perf_counter() - start
            filename = f"{destination.name}-{scenario}.joblib"
            file = MODELS / filename
            joblib.dump(estimator, file, compress=3)
            final[scenario] = {
                "model": winner, "threshold": threshold, "file": filename,
                "sha256": sha256(file), "bytes": file.stat().st_size, "fit_s": seconds,
                "features": list(x.columns), "parameters": estimator.named_steps["model"].get_params(),
                "holdout": chosen, "baseline_family_sd": sd[winner.removesuffix("_otimizado")],
            }
        logistic = candidates["logistica"]
        logistic.fit(x.iloc[train], y[train])
        pd.Series(
            logistic.named_steps["model"].coef_[0],
            index=logistic.named_steps["preparation"].get_feature_names_out(),
        ).sort_values().to_csv(destination / f"coeficientes_{scenario}.csv")
    pd.DataFrame(candidates_rows).to_csv(destination / "validacao_interna.csv", index=False)
    if not quick:
        eligible = [key for key, row in final.items()
                    if max(v["holdout"]["f1"] for v in final.values()) - row["holdout"]["f1"] <= .002]
        primary = max(eligible, key=lambda key: (final[key]["holdout"]["recall"],
                      -final[key]["baseline_family_sd"], key == "C"))
        save_json(destination / "freeze.json", {
            "models": final, "primary": primary, "operational": "C",
            "test_sha256": json.loads((SPLITS / "manifest.json").read_text())["test"]["sha256"],
            "dataset_sha256": UCI_CSV_SHA256, "development_rows": len(frame),
            "protocol": "selecao.md", "experiment": destination.name,
        })
