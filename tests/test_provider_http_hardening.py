import json
import urllib.error

import pytest

from karakana.models.errors import ModelProviderRequestError, ModelProviderResponseError
from karakana.models.providers.anthropic_provider import AnthropicProvider
from karakana.models.providers.github_models import GitHubModelsProvider
from karakana.models.providers.http import anthropic_payload, chat_payload, post_json
from karakana.models.providers.openai_provider import OpenAIProvider
from karakana.models.schemas import ModelMessage, ModelRequest


class FakeResponse:
    def __init__(self, payload: dict, status: int = 200):
        self.payload = payload
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self, *_args):
        return json.dumps(self.payload).encode("utf-8")

    def close(self):
        return None


def request(provider: str = "openai", model: str = "model") -> ModelRequest:
    return ModelRequest(provider=provider, model=model, messages=[ModelMessage(role="user", content="Hello")])


def test_post_json_rejects_non_https_endpoint():
    with pytest.raises(ModelProviderRequestError, match="HTTPS"):
        post_json("http://example.test/chat", {"model": "x"}, {})


def test_post_json_sanitizes_http_error(monkeypatch):
    def fail(_request, timeout):
        raise urllib.error.HTTPError(
            url="https://example.test",
            code=401,
            msg="Unauthorized",
            hdrs={},
            fp=FakeResponse({"error": "Bearer abc123 client_secret=hidden"}),
        )

    monkeypatch.setattr("urllib.request.urlopen", fail)

    with pytest.raises(ModelProviderRequestError) as exc:
        post_json("https://example.test/chat", {"model": "x"}, {})

    assert "Bearer [REDACTED]" in str(exc.value)
    assert "client_secret=[REDACTED]" in str(exc.value)
    assert "abc123" not in str(exc.value)
    assert "hidden" not in str(exc.value)


def test_openai_provider_parses_content_usage_and_finish_reason(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-token")

    def fake_urlopen(_request, timeout):
        return FakeResponse(
            {
                "choices": [{"message": {"content": "Done"}, "finish_reason": "stop"}],
                "usage": {"prompt_tokens": 2, "completion_tokens": 3, "total_tokens": 5},
            }
        )

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    response = OpenAIProvider().complete(request())

    assert response.content == "Done"
    assert response.finish_reason == "stop"
    assert response.usage.total_tokens == 5


def test_github_provider_rejects_malformed_response(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.setenv("GH_TOKEN", "test-token")

    def fake_urlopen(_request, timeout):
        return FakeResponse({"choices": []})

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    with pytest.raises(ModelProviderResponseError, match="choices"):
        GitHubModelsProvider().complete(request(provider="github", model="gpt-5-mini"))


def test_anthropic_provider_uses_messages_payload_and_parses_usage(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-token")
    seen_payloads = []

    def fake_urlopen(req, timeout):
        seen_payloads.append(json.loads(req.data.decode("utf-8")))
        return FakeResponse(
            {
                "content": [{"type": "text", "text": "Anthropic done"}],
                "usage": {"input_tokens": 4, "output_tokens": 6},
                "stop_reason": "end_turn",
            }
        )

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    model_request = ModelRequest(
        provider="anthropic",
        model="claude-haiku-4.5",
        messages=[ModelMessage(role="system", content="Be brief."), ModelMessage(role="user", content="Hello")],
    )
    response = AnthropicProvider().complete(model_request)

    assert seen_payloads[0]["system"] == "Be brief."
    assert seen_payloads[0]["messages"] == [{"role": "user", "content": "Hello"}]
    assert response.content == "Anthropic done"
    assert response.usage.total_tokens == 10
    assert response.finish_reason == "end_turn"


def test_payload_helpers_include_optional_generation_controls():
    model_request = ModelRequest(
        provider="openai",
        model="gpt",
        messages=[ModelMessage(role="user", content="Hello")],
        temperature=0.2,
        max_output_tokens=50,
    )

    assert chat_payload(model_request)["temperature"] == 0.2
    assert chat_payload(model_request)["max_tokens"] == 50
    assert anthropic_payload(model_request)["max_tokens"] == 50
