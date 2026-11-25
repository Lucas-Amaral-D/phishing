import json

import joblib
import pandas as pd
import pytest
from sklearn.dummy import DummyClassifier

from phishield import prediction
from phishield.data_loader import sha256
from phishield.feature_extraction import FEATURES, extract_url
from phishield.preprocessing import pipeline_for


@pytest.fixture
def model_manifest(tmp_path, monkeypatch):
    monkeypatch.setattr(prediction, "MODELS", tmp_path)
    x = pd.DataFrame([extract_url("https://example.org"), extract_url("http://example.net/a")])
    estimator = pipeline_for(x, DummyClassifier(strategy="prior")).fit(x, [0, 1])
    artifact = tmp_path / "model.joblib"
    joblib.dump(estimator, artifact)
    manifest = tmp_path / "freeze.json"
    manifest.write_text(json.dumps({
        "operational": "C", "models": {"C": {
            "file": artifact.name, "features": FEATURES, "sha256": sha256(artifact),
            "threshold": .5,
        }},
    }), encoding="utf-8")
    return manifest, artifact


def test_load_and_classify_consistently(model_manifest):
    manifest, _ = model_manifest
    estimator, spec = prediction.load_operational(manifest)
    first = prediction.classify("https://example.org", estimator, spec["threshold"])
    second = prediction.classify("https://example.org", estimator, spec["threshold"])
    assert first == second
    assert first["score"] == .5
    with pytest.raises(ValueError):
        prediction.classify("data:example", estimator, spec["threshold"])


def test_artifact_missing_or_corrupted(model_manifest):
    manifest, artifact = model_manifest
    artifact.write_bytes(b"arquivo divergente")
    with pytest.raises(ValueError, match="integridade"):
        prediction.load_operational(manifest)
    artifact.unlink()
    with pytest.raises(FileNotFoundError):
        prediction.load_operational(manifest)
