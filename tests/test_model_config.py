from karakana.models.config import redacted_model_config


def test_redacted_model_config_defaults(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.delenv("GH_TOKEN", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    config = redacted_model_config()

    assert config["default_provider"] == "mock"
    assert config["providers"]["mock"]["configured"] is True
    assert config["providers"]["github"]["configured"] is False
    assert "GITHUB_TOKEN" not in str(config)


def test_redacted_model_config_accepts_gh_token(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.setenv("GH_TOKEN", "token")

    config = redacted_model_config()

    assert config["providers"]["github"]["configured"] is True
    assert "token" not in str(config)
