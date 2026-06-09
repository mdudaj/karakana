"""Deterministic mock model provider."""

from __future__ import annotations

from karakana.models.base import ModelProvider
from karakana.models.schemas import ModelRequest, ModelResponse, TokenUsage


class MockProvider(ModelProvider):
    name = "mock"

    def is_configured(self) -> bool:
        return True

    def complete(self, request: ModelRequest) -> ModelResponse:
        self.validate_request(request)
        return ModelResponse(
            provider=self.name,
            model=request.model,
            content=(
                "[MOCK MODEL RESPONSE]\n\n"
                f"Provider: {self.name}\n"
                f"Model: {request.model}\n\n"
                "This is a deterministic mock response for testing."
            ),
            usage=TokenUsage(input_tokens=None, output_tokens=None, total_tokens=None),
            finish_reason="stop",
        )
