"""Environment-driven model provider configuration."""

from __future__ import annotations

import os

DEFAULT_PROVIDER = "mock"
DEFAULT_MODEL = "mock-model"


def model_config() -> dict:
    provider = os.environ.get("KARAKANA_MODEL_PROVIDER", DEFAULT_PROVIDER)
    model = os.environ.get("KARAKANA_MODEL") or _default_model(provider)
    return {
        "default_provider": provider,
        "default_model": model,
        "live_mode": os.environ.get("KARAKANA_LIVE_MODE", "false").lower() == "true",
        "providers": {
            "github": {
                "configured": bool(os.environ.get("GITHUB_TOKEN")),
                "model": os.environ.get("KARAKANA_MODEL") or "gpt-5-mini",
                "endpoint": os.environ.get("GITHUB_MODELS_ENDPOINT", "https://models.inference.ai.azure.com"),
            },
            "openai": {
                "configured": bool(os.environ.get("OPENAI_API_KEY")),
                "model": os.environ.get("OPENAI_MODEL", "gpt-5.4"),
                "endpoint": os.environ.get("OPENAI_ENDPOINT", "https://api.openai.com/v1/chat/completions"),
            },
            "openai_codex": {
                "configured": bool(os.environ.get("OPENAI_API_KEY")),
                "model": os.environ.get("OPENAI_CODEX_MODEL", "gpt-5.4-mini"),
                "endpoint": os.environ.get("OPENAI_ENDPOINT", "https://api.openai.com/v1/chat/completions"),
            },
            "anthropic": {
                "configured": bool(os.environ.get("ANTHROPIC_API_KEY")),
                "model": os.environ.get("ANTHROPIC_MODEL", "claude-haiku-4.5"),
                "endpoint": os.environ.get("ANTHROPIC_ENDPOINT", "https://api.anthropic.com/v1/messages"),
            },
            "mock": {"configured": True, "model": DEFAULT_MODEL},
        },
    }


def redacted_model_config() -> dict:
    return model_config()


def _default_model(provider: str) -> str:
    return {
        "github": "gpt-5-mini",
        "openai": "gpt-5.4",
        "openai_codex": "gpt-5.4-mini",
        "anthropic": "claude-haiku-4.5",
        "mock": DEFAULT_MODEL,
    }.get(provider, DEFAULT_MODEL)
