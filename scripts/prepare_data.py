"""Reserva persistente do teste agrupado por domínio."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from phishield.splitting import reserve  # noqa: E402

if __name__ == "__main__":
    print(json.dumps(reserve(), indent=2, ensure_ascii=False))
