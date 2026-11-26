import pandas as pd
import pytest

from phishield import splitting
from phishield.data_loader import sha256


def test_reserve_can_resume_without_replacing_existing_indices(tmp_path, monkeypatch):
    raw = tmp_path / "raw"
    raw.mkdir()
    source = raw / "data.csv"
    pd.DataFrame([
        {
            "FILENAME": f"{i}-{label}",
            "URL": f"https://example{i}.org/sample-{label}",
            "Domain": f"example{i}.org",
            "TLD": "org",
            "Title": "Exemplo seguro",
            "label": label,
        }
        for i in range(20) for label in (0, 1)
    ]).to_csv(source, index=False)
    splits = tmp_path / "splits"
    monkeypatch.setattr(splitting, "RAW", raw)
    monkeypatch.setattr(splitting, "SPLITS", splits)
    monkeypatch.setattr(splitting, "UCI_CSV", source.name)
    monkeypatch.setattr(splitting, "UCI_CSV_SHA256", sha256(source))
    publish = splitting._publish_stream

    def interrupted(stream, path, expected):
        if path.name == "test.npy":
            raise OSError("Interrupção simulada.")
        publish(stream, path, expected)

    monkeypatch.setattr(splitting, "_publish_stream", interrupted)
    with pytest.raises(OSError, match="Interrupção"):
        splitting.reserve()
    before = (splits / "dev.npy").stat().st_mtime_ns
    assert not (splits / "manifest.json").exists()

    monkeypatch.setattr(splitting, "_publish_stream", publish)
    report = splitting.reserve()
    assert splitting.reserve() == report
    assert (splits / "dev.npy").stat().st_mtime_ns == before
    assert len(splitting.load_rows("dev")) == report["dev"]["rows"]
    (splits / "dev.npy").write_bytes(b"arquivo divergente")
    with pytest.raises(ValueError, match="Hash"):
        splitting.load_rows("dev")


def test_partition_validates_name_before_reading():
    with pytest.raises(ValueError, match="desconhecida"):
        splitting.partition_path("../config", {})
