"""Redaction helpers for ingestion artifacts."""

from __future__ import annotations

import re

SECRET_TERMS = (
    "token",
    "secret",
    "password",
    "api_key",
    "apikey",
    "authorization",
    "bearer",
    "private_key",
    "client_secret",
    "access_key",
    "refresh_token",
    "github_token",
    "openai_api_key",
    "anthropic_api_key",
)


def redact_text(text: str) -> tuple[str, bool, list[str]]:
    warnings: list[str] = []
    redacted = text
    redacted = re.sub(r"\b(" + "|".join(SECRET_TERMS) + r")\s*[:=]\s*\S+", r"\1=[REDACTED]", redacted, flags=re.IGNORECASE)
    redacted = re.sub(r"\bBearer\s+[A-Za-z0-9._~+/=-]+", "Bearer [REDACTED]", redacted, flags=re.IGNORECASE)
    redacted = re.sub(r"(?m)^.*\b(GITHUB_TOKEN|OPENAI_API_KEY|ANTHROPIC_API_KEY)\b.*$", "[REDACTED SECRET ENV]", redacted)
    applied = redacted != text
    if applied:
        warnings.append("Secret-like content was redacted.")
    if ".env" in text:
        warnings.append("Source referenced .env content or paths.")
    return redacted, applied, warnings


def mostly_secret(text: str) -> bool:
    if not text.strip():
        return False
    lines = [line for line in text.splitlines() if line.strip()]
    secret_lines = [line for line in lines if any(term in line.lower() for term in SECRET_TERMS)]
    return len(secret_lines) >= max(2, len(lines) // 2)


def contains_secret(text: str) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in SECRET_TERMS)
