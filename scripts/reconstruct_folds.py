"""Reconstrói os índices internos da execução histórica usando só o desenvolvimento."""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import sklearn
from sklearn.model_selection import StratifiedKFold

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from phishield.config import EXPERIMENT  # noqa: E402
from phishield.data_loader import sha256  # noqa: E402
from phishield.feature_extraction import domain_group  # noqa: E402
from phishield.splitting import SPLITS, grouped_folds, load_rows, target_array  # noqa: E402


def reconstruct(directory):
    metadata = json.loads((directory / "metadata.json").read_text(encoding="utf-8"))
    if metadata["quick"] or metadata["seed"] != EXPERIMENT["random_state"]:
        raise ValueError("A reconstrução requer a execução completa e a semente de origem.")
    if metadata["sklearn"] != sklearn.__version__:
        raise ValueError("Use a versão de scikit-learn da execução de origem.")
    if metadata["dev_sha256"] != sha256(SPLITS / "dev.npy"):
        raise ValueError("A partição de desenvolvimento diverge da execução de origem.")
    frame = load_rows("dev")
    target = target_array(frame)
    groups = frame.URL.map(domain_group).to_numpy()
    ids = frame.index.to_numpy()
    outer = grouped_folds(target, groups)
    historical = directory / "fold_indices.npz"
    with np.load(historical, allow_pickle=False) as recorded:
        for i, (_, valid) in enumerate(outer):
            if not np.array_equal(ids[valid], recorded[f"validation_{i}"]):
                raise ValueError(f"Fold externo {i} divergente do registro histórico.")
    train, holdout = outer[0]
    inner = grouped_folds(target[train], groups[train])
    random = list(StratifiedKFold(
        EXPERIMENT["cv_folds"], shuffle=True, random_state=EXPERIMENT["random_state"],
    ).split(target, target))
    indices = {
        **{f"tuning_{i}": ids[train[valid]] for i, (_, valid) in enumerate(inner)},
        **{f"random_{i}": ids[valid] for i, (_, valid) in enumerate(random)},
    }
    output = directory / "fold_indices_reconstruidos.npz"
    with output.open("xb") as stream:
        np.savez_compressed(stream, **indices)
    report = {
        "method": "Reconstrução determinística após a execução original",
        "reference_sha256": sha256(historical),
        "reconstructed_sha256": sha256(output),
        "holdout_rows": len(holdout),
        "tuning_validation_rows": [len(valid) for _, valid in inner],
        "tuning_overlapping_groups": [
            len(set(groups[train[a]]) & set(groups[train[b]])) for a, b in inner
        ],
        "random_overlapping_groups": [
            len(set(groups[a]) & set(groups[b])) for a, b in random
        ],
    }
    with (directory / "reconstrucao_folds.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("experiment", type=Path)
    reconstruct(parser.parse_args().experiment)
