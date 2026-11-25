import json

import pytest

from phishield import final_evaluation


def test_evaluation_marker_blocks_access_before_loading_test(tmp_path, monkeypatch):
    monkeypatch.setattr(final_evaluation, "ROOT", tmp_path)
    monkeypatch.setattr(final_evaluation, "sha256", lambda _: "digest")

    def reject_read(*args):
        pytest.fail("A reserva já avaliada foi acessada.")

    monkeypatch.setattr(final_evaluation, "load_rows", reject_read)
    freeze = tmp_path / "freeze.json"
    freeze.write_text(json.dumps({
        "test_sha256": "digest", "dataset_sha256": "digest",
        "primary": "C", "operational": "C",
        "models": {"C": {"file": "model.joblib", "sha256": "digest"}},
    }), encoding="utf-8")
    state = tmp_path / "results" / "final" / "digest" / "execucao.json"
    state.parent.mkdir(parents=True)
    state.write_text('{"state":"complete"}', encoding="utf-8")
    with pytest.raises(FileExistsError):
        final_evaluation.evaluate(freeze)
    assert state.read_text() == '{"state":"complete"}'
