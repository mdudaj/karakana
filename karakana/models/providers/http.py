"""Small HTTP helpers for model providers.

The provider layer intentionally uses the standard library so normal
installation stays lightweight. Keep all credential handling and response
parsing here so provider adapters do not drift.
"""

from __future__ import annotations

from http import HTTPStatus
import json
import re
from typing import Any
import urllib.error
import urllib.parse
import urllib.request

from karakana.models.errors import ModelProviderRequestError, ModelProviderResponseError
from karakana.models.schemas import ModelRequest, TokenUsage

DEFAULT_TIMEOUT_SECONDS = 30
MAX_ERROR_BODY_CHARS = 500
MAX_RESPONSE_BYTES = 5_000_000
USER_AGENT = "karakana/0.1"


def validate_https_endpoint(endpoint: str) -> None:
    parsed = urllib.parse.urlparse(endpoint)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ModelProviderRequestError("Model provider endpoint must be an absolute HTTPS URL.")


def chat_payload(request: ModelRequest) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": request.model,
        "messages": [{"role": message.role, "content": message.content} for message in request.messages],
    }
    if request.temperature is not None:
        payload["temperature"] = request.temperature
    if request.max_output_tokens is not None:
        payload["max_tokens"] = request.max_output_tokens
    return payload


def anthropic_payload(request: ModelRequest) -> dict[str, Any]:
    system_messages = [message.content for message in request.messages if message.role == "system"]
    chat_messages = [
        {"role": message.role, "content": message.content}
        for message in request.messages
        if message.role in {"user", "assistant"}
    ]
    payload: dict[str, Any] = {
        "model": request.model,
        "messages": chat_messages,
        "max_tokens": request.max_output_tokens or 1024,
    }
    if system_messages:
        payload["system"] = "\n\n".join(system_messages)
    if request.temperature is not None:
        payload["temperature"] = request.temperature
    return payload


def post_json(url: str, payload: dict[str, Any], headers: dict[str, str], timeout: int = DEFAULT_TIMEOUT_SECONDS) -> dict[str, Any]:
    validate_https_endpoint(url)
    safe_headers = {"Accept": "application/json", "Content-Type": "application/json", "User-Agent": USER_AGENT}
    safe_headers.update(headers)
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers=safe_headers,
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = getattr(response, "status", HTTPStatus.OK)
            body = response.read(MAX_RESPONSE_BYTES + 1)
    except urllib.error.HTTPError as exc:
        detail = _read_error_detail(exc)
        raise ModelProviderRequestError(f"Model provider HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise ModelProviderRequestError(_sanitize_error(f"Model provider request failed: {exc.reason}")) from exc
    except TimeoutError as exc:
        raise ModelProviderRequestError("Model provider request timed out.") from exc

    if status >= 400:
        raise ModelProviderRequestError(f"Model provider HTTP {status}.")
    if len(body) > MAX_RESPONSE_BYTES:
        raise ModelProviderResponseError("Model provider response exceeded maximum size.")
    try:
        parsed = json.loads(body.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise ModelProviderResponseError("Model provider response was not valid JSON.") from exc
    if not isinstance(parsed, dict):
        raise ModelProviderResponseError("Model provider response JSON must be an object.")
    return parsed


def parse_openai_compatible_response(provider: str, model: str, raw: dict[str, Any]) -> tuple[str, TokenUsage | None, str | None]:
    choices = raw.get("choices")
    if not isinstance(choices, list) or not choices:
        raise ModelProviderResponseError("Model provider response did not include choices.")
    first = choices[0]
    if not isinstance(first, dict):
        raise ModelProviderResponseError("Model provider choice was not an object.")
    message = first.get("message")
    content = message.get("content") if isinstance(message, dict) else first.get("text")
    if not isinstance(content, str):
        raise ModelProviderResponseError(f"{provider} response did not include text content for {model}.")
    return content, _parse_usage(raw.get("usage")), first.get("finish_reason")


def parse_anthropic_response(model: str, raw: dict[str, Any]) -> tuple[str, TokenUsage | None, str | None]:
    content_blocks = raw.get("content")
    if not isinstance(content_blocks, list):
        raise ModelProviderResponseError("Anthropic response did not include content blocks.")
    chunks = [block.get("text", "") for block in content_blocks if isinstance(block, dict) and block.get("type") == "text"]
    content = "\n".join(chunk for chunk in chunks if chunk)
    if not content:
        raise ModelProviderResponseError(f"Anthropic response did not include text content for {model}.")
    return content, _parse_usage(raw.get("usage")), raw.get("stop_reason")


def _parse_usage(raw_usage: Any) -> TokenUsage | None:
    if not isinstance(raw_usage, dict):
        return None
    input_tokens = raw_usage.get("prompt_tokens", raw_usage.get("input_tokens"))
    output_tokens = raw_usage.get("completion_tokens", raw_usage.get("output_tokens"))
    total_tokens = raw_usage.get("total_tokens")
    if total_tokens is None and isinstance(input_tokens, int) and isinstance(output_tokens, int):
        total_tokens = input_tokens + output_tokens
    return TokenUsage(input_tokens=input_tokens, output_tokens=output_tokens, total_tokens=total_tokens)


def _read_error_detail(exc: urllib.error.HTTPError) -> str:
    try:
        body = exc.read(MAX_ERROR_BODY_CHARS).decode("utf-8", errors="replace")
    except Exception:
        body = ""
    return _sanitize_error(body or exc.reason or "request failed")


def _sanitize_error(message: object) -> str:
    text = str(message)
    text = re.sub(r"Bearer\s+[A-Za-z0-9._~+/=-]+", "Bearer [REDACTED]", text, flags=re.IGNORECASE)
    text = re.sub(
        r"(api[_-]?key|token|authorization|x-api-key|secret|password|private_key|client_secret|access_key|refresh_token)\s*[:=]\s*[^,\s}]+",
        r"\1=[REDACTED]",
        text,
        flags=re.IGNORECASE,
    )
    return text[:MAX_ERROR_BODY_CHARS]
