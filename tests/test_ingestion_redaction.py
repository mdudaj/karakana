import pytest

from karakana.ingestion.redaction import mostly_secret, redact_text
from karakana.ingestion.sources import load_note_source


def test_redacts_secret_like_content():
    redacted, applied, warnings = redact_text("api_key=abc123\nAuthorization: Bearer tokenvalue\ncat .env")

    assert applied
    assert "[REDACTED]" in redacted
    assert any(".env" in warning for warning in warnings)
    assert "abc123" not in redacted


def test_blocks_mostly_secret_note():
    assert mostly_secret("password=one\nclient_secret=two\nnormal")
    with pytest.raises(ValueError, match="mostly secret"):
        load_note_source("password=one\nclient_secret=two")
