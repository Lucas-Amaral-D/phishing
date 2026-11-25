"""Preparação da reserva e verificação de partições independentes."""
import json

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit, StratifiedGroupKFold

from .config import RAW, ROOT, UCI_CSV, UCI_CSV_SHA256
from .data_loader import sha256
from .data_validation import TEXT_COLUMNS
from .feature_extraction import domain_group

SPLITS = ROOT / "data" / "splits"
CONFIG = json.loads((ROOT / "configs/experiment_config.json").read_text(encoding="utf-8"))


def check_partition(y, groups, train, valid):
    if len(np.unique(np.r_[train, valid])) != len(y):
        raise ValueError("Partição incompleta ou com sobreposição.")
    if np.intersect1d(train, valid).size or set(groups[train]) & set(groups[valid]):
        raise ValueError("Registros ou domínios compartilhados.")
    if len(np.unique(y[train])) != 2 or len(np.unique(y[valid])) != 2:
        raise ValueError("Partição sem ambas as classes.")


def load_rows(partition):
    indices = np.sort(np.load(SPLITS / f"{partition}.npy", allow_pickle=False))
    include = set(indices + 1)
    dtypes = {column: "string" for column in TEXT_COLUMNS}
    frame = pd.read_csv(
        RAW / UCI_CSV, dtype=dtypes, skiprows=lambda row: row != 0 and row not in include,
        keep_default_na=False,
    )
    frame.index = indices
    return frame


def grouped_folds(y, groups, folds=CONFIG["cv_folds"]):
    splitter = StratifiedGroupKFold(folds, shuffle=True, random_state=CONFIG["random_state"])
    result = list(splitter.split(y, y, groups))
    for train, valid in result:
        check_partition(y, groups, train, valid)
    if not np.array_equal(np.sort(np.concatenate([v for _, v in result])), np.arange(len(y))):
        raise ValueError("As validações não cobrem cada registro uma única vez.")
    return result


def reserve():
    path = RAW / UCI_CSV
    if sha256(path) != UCI_CSV_SHA256:
        raise ValueError("Arquivo UCI divergente.")
    frame = pd.read_csv(path, dtype={column: "string" for column in TEXT_COLUMNS}, keep_default_na=False)
    exact = int(frame.drop(columns="FILENAME").duplicated().sum())
    frame["url_key"] = frame["URL"].str.rstrip("/")
    duplicate_urls = int(frame["url_key"].duplicated().sum())
    conflicts = frame.groupby("url_key")["label"].transform("nunique").gt(1)
    before = frame["label"].value_counts().to_dict()
    accepted = frame.loc[~conflicts].drop_duplicates("url_key").copy()
    groups = {}
    for row, url in accepted["URL"].items():
        try:
            groups[row] = domain_group(url)
        except (ValueError, UnicodeError):
            continue
    invalid = len(accepted) - len(groups)
    accepted = accepted.loc[list(groups)]
    y = 1 - accepted["label"].to_numpy()
    group_array = np.array(list(groups.values()))
    size = CONFIG["test_size"]
    splits = GroupShuffleSplit(n_splits=24, test_size=size, random_state=CONFIG["random_state"])
    train, test = min(
        splits.split(y, y, group_array),
        key=lambda pair: abs(len(pair[1]) / len(y) - size) + abs(y[pair[1]].mean() - y.mean()),
    )
    check_partition(y, group_array, train, test)
    SPLITS.mkdir(parents=True, exist_ok=True)
    report = {
        "duplicates_ignoring_filename": exact, "repeated_urls": duplicate_urls,
        "conflicting_rows": int(conflicts.sum()), "invalid_urls": invalid,
        "original_labels": before, "retained_phishing": int(y.sum()),
        "registered_domains": len(set(group_array)),
        "rows_with_repeated_domain": int(pd.Series(group_array).duplicated(keep=False).sum()),
        "seed": CONFIG["random_state"], "strategy": "GroupShuffleSplit e PSL local",
        "dataset_sha256": UCI_CSV_SHA256,
    }
    for name, part in [("dev", train), ("test", test)]:
        target = SPLITS / f"{name}.npy"
        with target.open("xb") as stream:
            np.save(stream, accepted.index.to_numpy()[part], allow_pickle=False)
        report[name] = {
            "rows": len(part), "groups": len(set(group_array[part])),
            "phishing": int(y[part].sum()), "sha256": sha256(target),
        }
    (SPLITS / "manifest.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report
