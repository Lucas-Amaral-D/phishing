"""Executa e verifica os oito notebooks em ordem sem reavaliar o teste."""
import os
from pathlib import Path
from tempfile import TemporaryDirectory

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]


if __name__ == "__main__":
    with TemporaryDirectory() as temp:
        os.environ.setdefault("IPYTHONDIR", str(Path(temp) / "ipython"))
        os.environ.setdefault("JUPYTER_RUNTIME_DIR", str(Path(temp) / "runtime"))
        for path in sorted((ROOT / "notebooks").glob("*.ipynb")):
            notebook = nbformat.read(path, as_version=4)
            nbformat.validate(notebook)
            options = {"metadata": {"path": str(ROOT)}}
            executed = NotebookClient(notebook, timeout=120, resources=options).execute()
            path.write_text(nbformat.writes(executed) + "\n", encoding="utf-8", newline="\n")
            print(f"Executado: {path.name}", flush=True)
