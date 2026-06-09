from karakana.models.errors import ModelProviderError
from karakana.models.registry import default_registry


def test_default_registry_lists_providers():
    registry = default_registry()

    assert registry.list_providers() == ["anthropic", "github", "mock", "openai"]
    assert "mock" in registry.configured_providers()


def test_unknown_provider_errors():
    registry = default_registry()

    try:
        registry.get("missing")
    except ModelProviderError as exc:
        assert "Unknown model provider" in str(exc)
    else:
        raise AssertionError("Expected ModelProviderError")
