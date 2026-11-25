"""Executa os experimentos de desenvolvimento e congela os modelos."""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from phishield.training import run  # noqa: E402

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rapido", action="store_true", help="Teste técnico com até 2.500 registros.")
    run(parser.parse_args().rapido)
