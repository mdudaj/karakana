from karakana.models.errors import ModelProviderError
from karakana.models.registry import default_registry


def test_default_registry_lists_providers():
    registry = default_registry()

    assert registry.list_providers() == ["anthropic", "github", "mock", "openai", "openai_codex"]
    assert "mock" in registry.configured_providers()


def test_openai_codex_registry_uses_codex_cli(monkeypatch):
    monkeypatch.setenv("CODEX_BIN", "/usr/local/bin/codex")

    registry = default_registry()
    provider = registry.get("openai_codex")

    assert provider.is_configured() is True
    assert provider.redact_config()["executable"] == "/usr/local/bin/codex"
    assert provider.redact_config()["frontier_default"] == "gpt-5.6-sol"
    assert "gpt-5.6-luna" in provider.redact_config()["available_frontier_models"]


def test_unknown_provider_errors():
    registry = default_registry()

    try:
        registry.get("missing")
    except ModelProviderError as exc:
        assert "Unknown model provider" in str(exc)
    else:
        raise AssertionError("Expected ModelProviderError")
