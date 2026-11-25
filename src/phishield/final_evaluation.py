"""Avaliação única do manifesto congelado e gráficos baseados nas previsões."""
import json
from datetime import datetime, timezone
from time import perf_counter

import joblib
import matplotlib
import pandas as pd
from sklearn.metrics import precision_recall_curve, roc_curve
from threadpoolctl import threadpool_limits

from .config import RAW, ROOT, UCI_CSV
from .data_loader import sha256
from .evaluation import metrics
from .feature_audit import scenario_features
from .splitting import SPLITS, load_rows, target_array
from .training import MODELS, save_json

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def charts(table, record, output, key):
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8), layout="constrained")
    matrix = [[record["tn"], record["fp"]], [record["fn"], record["tp"]]]
    axes[0].imshow(matrix, cmap="Blues", alpha=.65)
    for row in range(2):
        for col in range(2):
            axes[0].text(col, row, str(matrix[row][col]), ha="center", va="center")
    axes[0].set(xticks=[0, 1], yticks=[0, 1], xticklabels=["Legítimo", "Phishing"],
                yticklabels=["Legítimo", "Phishing"], xlabel="Previsto", ylabel="Real",
                title="Matriz de confusão")
    fpr, tpr, _ = roc_curve(table.expected, table.score)
    axes[1].plot(fpr, tpr)
    axes[1].plot([0, 1], [0, 1], "--", color="gray")
    axes[1].set(title="Curva ROC", xlabel="Taxa de falsos positivos", ylabel="Recall")
    precision, recall, _ = precision_recall_curve(table.expected, table.score)
    axes[2].plot(recall, precision)
    axes[2].set(title="Curva precisão-recall", xlabel="Recall", ylabel="Precisão")
    fig.savefig(output / f"avaliacao_{key}.png", dpi=180)
    plt.close(fig)


def evaluate(freeze_path):
    freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
    if sha256(SPLITS / "test.npy") != freeze["test_sha256"]:
        raise ValueError("A partição de teste diverge do manifesto.")
    if sha256(RAW / UCI_CSV) != freeze["dataset_sha256"]:
        raise ValueError("O CSV original diverge do manifesto.")
    keys = list(dict.fromkeys([freeze["primary"], freeze["operational"]]))
    for key in keys:
        model = freeze["models"][key]
        if sha256(MODELS / model["file"]) != model["sha256"]:
            raise ValueError("Artefato de modelo divergente.")
    output = ROOT / "results" / "final" / freeze["test_sha256"]
    output.mkdir(parents=True, exist_ok=True)
    state_path = output / "execucao.json"
    record = {
        "utc": datetime.now(timezone.utc).isoformat(), "state": "started",
        "freeze_sha256": sha256(freeze_path), "freeze": freeze, "outputs": [],
    }
    with state_path.open("x", encoding="utf-8") as stream:
        json.dump(record, stream, ensure_ascii=False, indent=2)
    try:
        frame = load_rows("test")
        truth = target_array(frame)
        variants = scenario_features(frame)
        result = {}
        for key in keys:
            spec = freeze["models"][key]
            estimator = joblib.load(MODELS / spec["file"])
            features = variants[key]
            if list(features.columns) != spec["features"]:
                raise ValueError("Atributos do teste incompatíveis com o manifesto.")
            start = perf_counter()
            with threadpool_limits(limits=4):
                scores = estimator.predict_proba(features)[:, 1]
            seconds = perf_counter() - start
            table = pd.DataFrame({
                "row_id": frame.index, "expected": truth, "score": scores,
                "predicted": (scores >= spec["threshold"]).astype(int),
            })
            prediction = f"previsoes_{key}.csv"
            table.to_csv(output / prediction, index=False)
            record["outputs"].append(prediction)
            result[key] = {"threshold": spec["threshold"], "inference_s": seconds,
                           **metrics(truth, scores, spec["threshold"])}
            charts(table, result[key], output, key)
            record["outputs"].append(f"avaliacao_{key}.png")
        save_json(output / "metrics.json", result)
        record["outputs"].append("metrics.json")
        record["state"] = "complete"
    except Exception as error:
        record.update(state="failed", error=f"{type(error).__name__}: {error}")
        raise
    finally:
        save_json(state_path, record)
    return output
