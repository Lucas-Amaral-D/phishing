import joblib
import numpy as np
import pandas as pd
import pytest
from sklearn.linear_model import LogisticRegression

from phishield.data_validation import inspect_csv
from phishield.evaluation import metrics
from phishield.feature_audit import scenario_features
from phishield.feature_extraction import domain_group, extract_url
from phishield.preprocessing import pipeline_for
from phishield.splitting import check_partition, grouped_folds, target_array


@pytest.mark.parametrize("url", [
    "", None, "ftp://example.org", "http://", "http://host:65536",
    "http://x y.example/", "http://name@example.org", "https://example.org/" + "a" * 16384,
])
def test_invalid_urls(url):
    with pytest.raises((ValueError, UnicodeError)):
        extract_url(url)


def test_local_url_features_without_network(monkeypatch):
    def reject(*args, **kwargs):
        pytest.fail("O extrator tentou abrir uma conexão.")

    monkeypatch.setattr("socket.create_connection", reject)
    url = "https://a.b.example.co.uk:8443/a/b?x=1&y=2#secao"
    row = extract_url(url)
    assert [row[key] for key in (
        "https", "parametros", "subdominios", "profundidade", "porta", "fragmento",
    )] == [1, 2, 2, 2, 1, 1]
    assert domain_group(url) == "example.co.uk"
    assert extract_url("http://192.0.2.1/a")["ip"] == 1
    assert domain_group("https://exemploá.org") == domain_group("https://xn--exemplo-2wa.org") or (
        domain_group("https://exemploá.org") == "exemploá.org".encode("idna").decode()
    )


def test_csv_missing_and_duplicate_header(tmp_path):
    path = tmp_path / "missing.csv"
    with pytest.raises(FileNotFoundError):
        inspect_csv(path)
    path.write_text("x,x\n1,2\n")
    with pytest.raises(ValueError, match="duplicadas"):
        inspect_csv(path)


def test_target_array_uses_only_original_uci_labels():
    assert target_array(pd.DataFrame({"label": [1, 0]})).tolist() == [0, 1]
    with pytest.raises(ValueError, match="Rótulo"):
        target_array(pd.DataFrame({"label": [2]}))


def test_inspection_flags_nonfinite_numeric_content(tmp_path):
    path = tmp_path / "values.csv"
    path.write_text("URLLength,label\n30,1\ninf,0\n")
    assert inspect_csv(path)["types"]["URLLength"] == "texto"


def test_grouped_folds_reproducible_and_cover_validation():
    groups = np.repeat(np.arange(30), 2)
    y = np.tile([0, 1], 30)
    folds = grouped_folds(y, groups)
    repeated = grouped_folds(y, groups)
    assert all(np.array_equal(a[1], b[1]) for a, b in zip(folds, repeated, strict=True))
    assert sorted(np.concatenate([valid for _, valid in folds])) == list(range(60))


def test_group_overlap_rejected():
    with pytest.raises(ValueError, match="compartilhados"):
        check_partition(np.array([1, 0, 1, 0]), np.array([1, 2, 1, 3]),
                        np.array([0, 1]), np.array([2, 3]))


@pytest.mark.parametrize(("scores", "f1", "fp", "fn"), [
    ([0.1, 0.9], 1., 0, 0), ([0.9, 0.1], 0., 1, 1), ([0.1, 0.2], 0., 0, 1),
])
def test_metrics_phishing_positive(scores, f1, fp, fn):
    record = metrics(np.array([0, 1]), np.array(scores))
    assert (record["f1"], record["fp"], record["fn"]) == (f1, fp, fn)


def test_load_train_persist_infer(tmp_path):
    frame = pd.DataFrame({
        "length": [0., 1., 10., 11., np.nan],
        "suffix": ["org", "org", "net", "net", "org"],
    })
    estimator = pipeline_for(frame, LogisticRegression(), scaled=True)
    estimator.fit(frame, [0, 0, 1, 1, 1])
    unknown = pd.DataFrame({"length": [np.nan], "suffix": ["test"]})
    artifact = tmp_path / "model.joblib"
    joblib.dump(estimator, artifact)
    assert np.allclose(estimator.predict_proba(unknown),
                       joblib.load(artifact).predict_proba(unknown))
    with pytest.raises(FileNotFoundError):
        joblib.load(tmp_path / "missing.joblib")


def test_identifiers_and_suspect_columns_removed():
    from phishield.data_validation import COLUMNS

    frame = pd.DataFrame([{name: 0 for name in COLUMNS}])
    frame["URL"] = "https://example.org/"
    variants = scenario_features(frame)
    assert all("URL" not in x and "FILENAME" not in x and "label" not in x for x in variants.values())
    assert "TLDLegitimateProb" in variants["A"]
    assert "TLDLegitimateProb" not in variants["B"]
