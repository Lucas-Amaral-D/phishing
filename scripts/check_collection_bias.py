"""Mede sensibilidade à representação dentro da validação de desenvolvimento."""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from sklearn.model_selection import StratifiedKFold
from threadpoolctl import threadpool_limits

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from audit_collection import representation  # noqa: E402
from phishield.config import EXPERIMENT  # noqa: E402
from phishield.evaluation import metrics  # noqa: E402
from phishield.feature_audit import scenario_features  # noqa: E402
from phishield.feature_extraction import domain_group  # noqa: E402
from phishield.splitting import grouped_folds, load_rows, target_array  # noqa: E402
from phishield.training import pipeline, save_json  # noqa: E402


def check(freeze_path):
    freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
    frame = load_rows("dev")
    y = target_array(frame)
    groups = frame.URL.map(domain_group).to_numpy()
    train, valid = grouped_folds(y, groups)[0]
    common_format = np.array([all(representation(url).values()) for url in frame.URL.iloc[valid]])
    rows = StratifiedKFold(
        EXPERIMENT["cv_folds"], shuffle=True, random_state=EXPERIMENT["random_state"],
    ).split(y, y)
    result = {"random_group_overlap_by_fold": [len(set(groups[t]) & set(groups[v])) for t, v in rows]}
    features = scenario_features(frame)
    with threadpool_limits(limits=4):
        for key, spec in freeze["models"].items():
            x = features[key]
            name = spec["model"].removesuffix("_otimizado")
            estimator = pipeline(name, x)
            estimator.named_steps["model"].set_params(**spec["parameters"])
            estimator.fit(x.iloc[train], y[train])
            scores = estimator.predict_proba(x.iloc[valid])[:, 1]
            result[key] = {
                "common_format_n": int(common_format.sum()),
                "common_format_phishing": int(y[valid][common_format].sum()),
                "common_format": metrics(y[valid][common_format], scores[common_format],
                                         spec["threshold"]),
                "whole_validation": metrics(y[valid], scores, spec["threshold"]),
            }
    save_json(freeze_path.parent / "sensibilidade_coleta.json", result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("freeze", type=Path)
    check(parser.parse_args().freeze)
