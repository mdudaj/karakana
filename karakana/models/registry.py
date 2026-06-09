"""Registry for model providers."""

from __future__ import annotations

from karakana.models.base import ModelProvider
from karakana.models.errors import ModelProviderError
from karakana.models.providers.anthropic_provider import AnthropicProvider
from karakana.models.providers.github_models import GitHubModelsProvider
from karakana.models.providers.mock_provider import MockProvider
from karakana.models.providers.openai_provider import OpenAIProvider


class ModelProviderRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, ModelProvider] = {}

    def register(self, provider: ModelProvider) -> None:
        self._providers[provider.name] = provider

    def get(self, name: str) -> ModelProvider:
        if name not in self._providers:
            raise ModelProviderError(f"Unknown model provider: {name}")
        return self._providers[name]

    def list_providers(self) -> list[str]:
        return sorted(self._providers)

    def configured_providers(self) -> list[str]:
        return sorted(name for name, provider in self._providers.items() if provider.is_configured())


def default_registry() -> ModelProviderRegistry:
    registry = ModelProviderRegistry()
    registry.register(MockProvider())
    registry.register(GitHubModelsProvider())
    registry.register(OpenAIProvider())
    registry.register(AnthropicProvider())
    return registry
