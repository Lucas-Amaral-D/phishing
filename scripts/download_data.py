"""Audita o Kaggle e valida a fonte oficial, com resultados em JSON."""

import argparse
import json
import sys
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from phishield.data_loader import acquire_uci, audit_kaggle, timestamp  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only-uci", action="store_true", help="Valida apenas a fonte UCI.")
    args = parser.parse_args()
    report = {"checked_at_utc": timestamp()}
    failures = {}
    sources = {"uci": acquire_uci} if args.only_uci else {
        "kaggle": audit_kaggle,
        "uci": acquire_uci,
    }
    for source, operation in sources.items():
        try:
            report[source] = operation()
        except Exception as error:
            failures[source] = f"{type(error).__name__}: {error}"
    report["errors"] = failures
    destination = ROOT / "results" / "data_audit"
    destination.mkdir(parents=True, exist_ok=True)
    output = destination / f"{uuid4().hex}.json"
    with output.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(f"Registro de auditoria: {output.relative_to(ROOT)}")
    for source, error in failures.items():
        print(f"Falha em {source}: {error}", file=sys.stderr)
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
