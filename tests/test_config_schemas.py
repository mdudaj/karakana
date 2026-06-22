from karakana.config.schemas import KarakanaConfig


def test_config_schema_defaults_and_redaction():
    config = KarakanaConfig()
    config.metadata["api_key"] = "secret-value"

    data = config.to_dict()

    assert data["default_workspace"] == "default"
    assert data["models"]["live_mode_default"] is False
    assert data["metadata"]["api_key"] == "[REDACTED]"

