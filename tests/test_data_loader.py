from hashlib import sha256
from io import BytesIO

import pytest

from phishield.data_loader import _publish_stream


def test_preserves_original_and_rejects_replacement(tmp_path):
    target = tmp_path / "original.csv"
    original = b"label\n1\n"
    different = b"label\n0\n"
    original_hash = sha256(original).hexdigest()
    _publish_stream(BytesIO(original), target, original_hash)
    _publish_stream(BytesIO(original), target, original_hash)
    with pytest.raises(ValueError, match="SHA-256"):
        _publish_stream(BytesIO(different), target, sha256(different).hexdigest())
    assert target.read_bytes() == original
    assert list(tmp_path.iterdir()) == [target]


def test_hash_mismatch_leaves_no_partial_download(tmp_path):
    target = tmp_path / "original.csv"
    with pytest.raises(ValueError, match="SHA-256"):
        _publish_stream(BytesIO(b"resposta incorreta"), target, "0" * 64)
    assert list(tmp_path.iterdir()) == []
