from karakana.models.config import redacted_model_config


def test_redacted_model_config_defaults(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.delenv("GH_TOKEN", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("CODEX_BIN", raising=False)
    monkeypatch.setattr("karakana.models.config.shutil.which", lambda name: None)

    config = redacted_model_config()

    assert config["default_provider"] == "mock"
    assert config["providers"]["mock"]["configured"] is True
    assert config["providers"]["github"]["configured"] is False
    assert config["providers"]["openai"]["configured"] is False
    assert config["providers"]["openai_codex"]["configured"] is False
    assert "GITHUB_TOKEN" not in str(config)


def test_redacted_model_config_accepts_gh_token(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.setenv("GH_TOKEN", "token")

    config = redacted_model_config()

    assert config["providers"]["github"]["configured"] is True
    assert "token" not in str(config)


def test_openai_codex_config_uses_codex_cli_not_openai_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("CODEX_BIN", "/usr/local/bin/codex")

    config = redacted_model_config()

    assert config["providers"]["openai"]["configured"] is False
    assert config["providers"]["openai_codex"]["configured"] is True
    assert config["providers"]["openai_codex"]["executable"] == "/usr/local/bin/codex"
    assert config["providers"]["openai_codex"]["frontier_default"] == "gpt-5.6-sol"
    assert "gpt-5.6-terra" in config["providers"]["openai_codex"]["available_frontier_models"]
