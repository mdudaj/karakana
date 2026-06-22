"""Redaction and secret detection for handoff content."""

from __future__ import annotations

import re

from karakana.traces.schemas import redact_value


PRIVATE_KEY_RE = re.compile(r"-----BEGIN [^-]*PRIVATE KEY-----.*?-----END [^-]*PRIVATE KEY-----", re.DOTALL)
DATABASE_URL_RE = re.compile(r"\b([a-z][a-z0-9+.-]*://)([^\s:/]+):([^\s@]+)@", re.IGNORECASE)
ENV_ASSIGNMENT_RE = re.compile(r"(?m)^([A-Z][A-Z0-9_]{2,})=(?!\[REDACTED\])\S+\s*$")
KEY_PREFIX_RE = re.compile(r"\b(sk-[A-Za-z0-9_-]{12,}|gh[pousr]_[A-Za-z0-9]{12,})\b")
SECRET_ASSIGNMENT_RE = re.compile(
    r"\b(token|secret|password|api[_-]?key|authorization|private[_-]?key|client[_-]?secret|access[_-]?key|refresh[_-]?token)\s*[:=]\s*(?!\[REDACTED\])\S+",
    re.IGNORECASE,
)


def redact_handoff_text(text: str | None) -> str:
    if not text:
        return ""
    redacted = str(redact_value(text))
    redacted = PRIVATE_KEY_RE.sub("[REDACTED PRIVATE KEY]", redacted)
    redacted = DATABASE_URL_RE.sub(r"\1[REDACTED]@", redacted)
    redacted = ENV_ASSIGNMENT_RE.sub(r"\1=[REDACTED]", redacted)
    redacted = KEY_PREFIX_RE.sub("[REDACTED API KEY]", redacted)
    return redacted


def contains_unredacted_secret(text: str) -> bool:
    return bool(
        PRIVATE_KEY_RE.search(text)
        or DATABASE_URL_RE.search(text)
        or ENV_ASSIGNMENT_RE.search(text)
        or KEY_PREFIX_RE.search(text)
        or SECRET_ASSIGNMENT_RE.search(text)
    )
