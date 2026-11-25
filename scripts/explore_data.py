"""Gera a EDA do desenvolvimento."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from phishield.eda import run_eda  # noqa: E402

if __name__ == "__main__":
    run_eda()
