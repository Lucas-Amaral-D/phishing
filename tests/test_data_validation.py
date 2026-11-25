from pathlib import Path

import pytest

from phishield.config import EXPECTED_COUNTS
from phishield.data_validation import COLUMNS, TEXT_COLUMNS, encode_target, inspect_csv
from phishield.data_validation import validate_phiusiil


@pytest.mark.parametrize(("original", "internal"), [("0", 1), ("1", 0)])
def test_phishing_is_positive(original, internal):
    assert encode_target(original) == internal


@pytest.mark.parametrize("value", ["", "-1", "2", "0.0"])
def test_invalid_labels_are_rejected(value):
    with pytest.raises(ValueError, match="Rótulo"):
        encode_target(value)


def test_csv_summary_handles_quoted_fields(tmp_path: Path):
    path = tmp_path / "sample.csv"
    path.write_text('Title,score,Result\n"Título, teste",1.5,-1\n', encoding="utf-8")
    report = inspect_csv(path)
    assert report["rows"] == 1
    assert report["types"] == {"Title": "texto", "score": "real", "Result": "inteiro"}
    assert report["target_counts"] == {"-1": 1}


def test_rejects_irregular_row(tmp_path: Path):
    path = tmp_path / "sample.csv"
    path.write_text("a,label\n0,1,2\n", encoding="utf-8")
    with pytest.raises(ValueError, match="registro 1"):
        inspect_csv(path)


@pytest.fixture
def official_summary():
    return {
        "columns": list(COLUMNS),
        "rows": sum(EXPECTED_COUNTS.values()),
        "target": "label",
        "target_counts": EXPECTED_COUNTS.copy(),
        "types": {name: "texto" if name in TEXT_COLUMNS else "inteiro" for name in COLUMNS},
    }


def test_accepts_official_structure(official_summary):
    validate_phiusiil(official_summary)


@pytest.mark.parametrize(("field", "value", "message"), [
    ("columns", ["index", "Result"], "Cabeçalho"),
    ("rows", 11_055, "Quantidade"),
    ("target_counts", {"0": 134_850, "1": 100_945}, "distribuição"),
    ("target", "Result", "Alvo"),
])
def test_rejects_incompatible_structure(official_summary, field, value, message):
    official_summary[field] = value
    with pytest.raises(ValueError, match=message):
        validate_phiusiil(official_summary)


def test_rejects_non_numeric_predictor(official_summary):
    official_summary["types"]["URLLength"] = "texto"
    with pytest.raises(ValueError, match="URLLength"):
        validate_phiusiil(official_summary)
