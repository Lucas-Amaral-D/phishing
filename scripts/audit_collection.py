"""Quantifica diferenças de representação entre classes no desenvolvimento."""
import json
import sys
from pathlib import Path
from urllib.parse import urlsplit

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from phishield.config import ROOT  # noqa: E402
from phishield.splitting import load_rows  # noqa: E402


def representation(url):
    address = urlsplit(url)
    return {
        "https": address.scheme == "https",
        "www": bool(address.hostname and address.hostname.startswith("www.")),
        "raiz_sem_parametros": address.path in {"", "/"} and not address.query
        and not address.fragment,
    }


if __name__ == "__main__":
    frame = load_rows("dev")
    formats = pd.DataFrame.from_records(map(representation, frame.URL))
    formats["formato_combinado"] = formats.all(axis=1)
    formats["classe"] = frame.label.map({0: "phishing", 1: "legitimo"}).to_numpy()
    counts = formats.groupby("classe").sum().to_dict(orient="index")
    totals = formats.classe.value_counts()
    result = {key: {"total": int(totals[key]), **value} for key, value in counts.items()}
    (ROOT / "results/exploracao/formato_coleta.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8",
    )
    print(json.dumps(result, indent=2))
