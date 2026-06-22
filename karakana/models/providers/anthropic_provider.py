"""Anthropic provider adapter."""

from __future__ import annotations

import os

from karakana.models.base import ModelProvider
from karakana.models.errors import ModelProviderNotConfigured
from karakana.models.providers.http import anthropic_payload, parse_anthropic_response, post_json
from karakana.models.schemas import ModelRequest, ModelResponse


class AnthropicProvider(ModelProvider):
    name = "anthropic"

    def __init__(self) -> None:
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        self.endpoint = os.environ.get("ANTHROPIC_ENDPOINT", "https://api.anthropic.com/v1/messages")

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def complete(self, request: ModelRequest) -> ModelResponse:
        self.validate_request(request)
        if not self.is_configured():
            raise ModelProviderNotConfigured("ANTHROPIC_API_KEY is required for Anthropic live calls")
        raw = post_json(
            self.endpoint,
            anthropic_payload(request),
            headers={"x-api-key": self.api_key, "anthropic-version": "2023-06-01"},
        )
        content, usage, finish_reason = parse_anthropic_response(request.model, raw)
        return ModelResponse(provider=self.name, model=request.model, content=content, usage=usage, raw=raw, finish_reason=finish_reason)

    def redact_config(self) -> dict:
        return {"provider": self.name, "configured": self.is_configured(), "endpoint": self.endpoint}
