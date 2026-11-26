"""Preparação da reserva e verificação de partições independentes."""
import json
from hashlib import sha256 as digest
from io import BytesIO

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit, StratifiedGroupKFold

from .config import EXPERIMENT, RAW, ROOT, UCI_CSV, UCI_CSV_SHA256
from .data_loader import _publish_stream, sha256
from .data_validation import TEXT_COLUMNS, encode_target
from .feature_extraction import domain_group

SPLITS = ROOT / "data" / "splits"


def target_array(frame):
    """Aplica ao alvo a codificação interna testada, com phishing positivo."""
    return np.fromiter((encode_target(str(value)) for value in frame.label),
                       dtype=np.int64, count=len(frame))


def check_partition(y, groups, train, valid):
    if not np.array_equal(np.sort(np.r_[train, valid]), np.arange(len(y))):
        raise ValueError("Partição incompleta ou com índices inválidos ou compartilhados.")
    if set(groups[train]) & set(groups[valid]):
        raise ValueError("Domínios compartilhados.")
    if len(np.unique(y[train])) != 2 or len(np.unique(y[valid])) != 2:
        raise ValueError("Partição sem ambas as classes.")


def partition_path(partition, manifest):
    if partition not in {"dev", "test"}:
        raise ValueError("Partição desconhecida.")
    path = SPLITS / f"{partition}.npy"
    if sha256(path) != manifest[partition]["sha256"]:
        raise ValueError(f"Hash da partição {partition} divergente.")
    return path


def load_rows(partition):
    manifest = json.loads((SPLITS / "manifest.json").read_text(encoding="utf-8"))
    raw = RAW / UCI_CSV
    if manifest["dataset_sha256"] != UCI_CSV_SHA256 or sha256(raw) != UCI_CSV_SHA256:
        raise ValueError("Arquivo UCI divergente.")
    indices = np.sort(np.load(partition_path(partition, manifest), allow_pickle=False))
    include = set(indices + 1)
    dtypes = {column: "string" for column in TEXT_COLUMNS}
    frame = pd.read_csv(
        raw, dtype=dtypes, skiprows=lambda row: row != 0 and row not in include,
        keep_default_na=False,
    )
    frame.index = indices
    return frame


def grouped_folds(y, groups, folds=EXPERIMENT["cv_folds"]):
    splitter = StratifiedGroupKFold(folds, shuffle=True, random_state=EXPERIMENT["random_state"])
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
    manifest = SPLITS / "manifest.json"
    if manifest.is_file():
        report = json.loads(manifest.read_text(encoding="utf-8"))
        if report["dataset_sha256"] != UCI_CSV_SHA256 or report["seed"] != EXPERIMENT["random_state"]:
            raise ValueError("Manifesto da reserva incompatível com a configuração.")
        for name in ("dev", "test"):
            partition_path(name, report)
        return report
    frame = pd.read_csv(path, dtype={column: "string" for column in TEXT_COLUMNS}, keep_default_na=False)
    exact = int(frame.drop(columns="FILENAME").duplicated().sum())
    frame["url_key"] = frame["URL"].str.rstrip("/")
    duplicate_urls = int(frame["url_key"].duplicated().sum())
    conflicts = frame.groupby("url_key")["label"].transform("nunique").gt(1)
    before = {str(label): count for label, count in frame["label"].value_counts().items()}
    accepted = frame.loc[~conflicts].drop_duplicates("url_key").copy()
    groups = {}
    for row, url in accepted["URL"].items():
        try:
            groups[row] = domain_group(url)
        except (ValueError, UnicodeError):
            continue
    invalid = len(accepted) - len(groups)
    accepted = accepted.loc[list(groups)]
    y = target_array(accepted)
    group_array = np.array(list(groups.values()))
    size = EXPERIMENT["test_size"]
    splits = GroupShuffleSplit(n_splits=24, test_size=size, random_state=EXPERIMENT["random_state"])
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
        "seed": EXPERIMENT["random_state"], "strategy": "GroupShuffleSplit e PSL local",
        "dataset_sha256": UCI_CSV_SHA256,
    }
    for name, part in [("dev", train), ("test", test)]:
        target = SPLITS / f"{name}.npy"
        stream = BytesIO()
        np.save(stream, accepted.index.to_numpy()[part], allow_pickle=False)
        checksum = digest(stream.getbuffer()).hexdigest()
        stream.seek(0)
        _publish_stream(stream, target, checksum)
        report[name] = {
            "rows": len(part), "groups": len(set(group_array[part])),
            "phishing": int(y[part].sum()), "sha256": checksum,
        }
    content = json.dumps(report, indent=2).encode("utf-8")
    _publish_stream(BytesIO(content), manifest, digest(content).hexdigest())
    return report
