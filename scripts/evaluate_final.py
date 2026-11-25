"""Executa a avaliação final uma vez para o hash da partição reservada."""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from phishield.final_evaluation import evaluate  # noqa: E402

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("freeze", type=Path)
    print(evaluate(parser.parse_args().freeze))
