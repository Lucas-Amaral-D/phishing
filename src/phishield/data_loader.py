"""Aquisição dos dados públicos e registro da proveniência."""

import hashlib
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from zipfile import ZipFile

from .config import CATALOG, DOI, INTERNAL_CLASSES, KAGGLE_ID, MENDELEY
from .config import ORIGINAL_CLASSES, RAW, UCI_CSV, UCI_CSV_SHA256, UCI_ZIP, UCI_ZIP_SHA256
from .data_validation import inspect_csv, validate_phiusiil


def sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def _verify_hash(path: Path, expected: str) -> None:
    if sha256(path) != expected:
        raise ValueError(f"SHA-256 incompatível com a versão registrada: {path.name}.")


def _publish_stream(stream, destination: Path, expected: str) -> None:
    """Publica os bytes completos sem substituir um arquivo bruto existente."""
    with NamedTemporaryFile(dir=destination.parent, delete=False) as temp:
        temporary = Path(temp.name)
        try:
            with temp:
                shutil.copyfileobj(stream, temp)
            _verify_hash(temporary, expected)
            try:
                os.link(temporary, destination)
            except FileExistsError:
                _verify_hash(destination, expected)
        finally:
            temporary.unlink(missing_ok=True)


def audit_kaggle() -> dict:
    """Consulta a versão observada e compara os CSVs encontrados com a UCI."""
    os.environ.setdefault("KAGGLEHUB_CACHE", str(RAW / "kaggle-cache"))
    import kagglehub

    version = 2
    directory = Path(kagglehub.dataset_download(f"{KAGGLE_ID}/versions/{version}"))
    files = sorted(path for path in directory.rglob("*") if path.is_file())
    tables = []
    for path in files:
        if path.suffix.lower() != ".csv":
            continue
        summary = inspect_csv(path)
        try:
            validate_phiusiil(summary)
        except ValueError as error:
            identity = str(error)
        else:
            identity = "Esquema compatível com UCI 967"
        tables.append({
            "filename": str(path.relative_to(directory)),
            "sha256": sha256(path),
            "comparison": identity,
            **summary,
        })
    return {
        "source": f"https://www.kaggle.com/datasets/{KAGGLE_ID}",
        "version": version,
        "newest_file_mtime_utc": _mtime(max(files, key=lambda path: path.stat().st_mtime))
        if files else None,
        "files": [
            {"name": str(path.relative_to(directory)), "extension": path.suffix.lower(),
             "bytes": path.stat().st_size}
            for path in files
        ],
        "tables": tables,
    }


def acquire_uci() -> dict:
    """Preserva o ZIP oficial e o CSV original, registrando ambos os hashes."""
    RAW.mkdir(parents=True, exist_ok=True)
    archive = RAW / "uci-967.zip"
    csv_path = RAW / UCI_CSV
    if not archive.exists():
        with urlopen(UCI_ZIP, timeout=90) as response:
            _publish_stream(response, archive, UCI_ZIP_SHA256)
    _verify_hash(archive, UCI_ZIP_SHA256)
    if not csv_path.exists():
        with ZipFile(archive) as package, package.open(UCI_CSV) as member:
            _publish_stream(member, csv_path, UCI_CSV_SHA256)
    _verify_hash(csv_path, UCI_CSV_SHA256)
    summary = inspect_csv(csv_path)
    validate_phiusiil(summary)
    return {
        "catalog": CATALOG,
        "download_url": UCI_ZIP,
        "release": "UCI 967, publicação de 2024-03-03; revisão sem número no catálogo",
        "license": "CC BY 4.0",
        "references": [DOI, MENDELEY],
        "archive": archive.name,
        "archive_mtime_utc": _mtime(archive),
        "archive_sha256": sha256(archive),
        "csv": csv_path.name,
        "csv_sha256": sha256(csv_path),
        "original_classes": ORIGINAL_CLASSES,
        "internal_encoding": INTERNAL_CLASSES,
        "predictors": len(summary["columns"]) - 2,
        **summary,
    }


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _mtime(path: Path) -> str:
    """Registra o horário do arquivo local, mesmo quando reutilizado."""
    return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()
