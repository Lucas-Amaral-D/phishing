"""Inferência lexical com artefato local e esquema verificado."""
import json
from pathlib import Path

import joblib
import pandas as pd
from threadpoolctl import threadpool_limits

from .config import ROOT
from .data_loader import sha256
from .feature_extraction import FEATURES, extract_url

MODELS = ROOT / "models"


def load_operational(freeze_path):
    manifest = json.loads(freeze_path.read_text(encoding="utf-8"))
    if manifest["operational"] != "C":
        raise ValueError("O manifesto precisa identificar um modelo lexical.")
    spec = manifest["models"]["C"]
    filename = Path(spec["file"])
    if filename.name != spec["file"] or filename.suffix != ".joblib":
        raise ValueError("Nome de artefato inválido no manifesto.")
    artifact = MODELS / filename
    if spec["features"] != FEATURES or sha256(artifact) != spec["sha256"]:
        raise ValueError("Esquema ou integridade do artefato incompatível.")
    pipeline = joblib.load(artifact)
    if list(pipeline.feature_names_in_) != FEATURES or list(pipeline.classes_) != [0, 1]:
        raise ValueError("O pipeline usa atributos ou classes incompatíveis.")
    return pipeline, spec


def classify(url, estimator, threshold):
    row = extract_url(url)
    frame = pd.DataFrame([row], columns=FEATURES)
    with threadpool_limits(limits=4):
        score = float(estimator.predict_proba(frame)[0, 1])
    return {"phishing": score >= threshold, "score": score, "features": row}
