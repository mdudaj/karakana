from karakana.models.schemas import ModelMessage, ModelRequest, ModelResponse


def test_model_request_serializes_and_redacts_metadata():
    request = ModelRequest(
        provider="mock",
        model="mock-model",
        messages=[ModelMessage(role="user", content="Hello")],
        metadata={"api_key": "secret"},
    )

    data = request.to_dict()

    assert data["messages"][0]["content"] == "Hello"
    assert data["metadata"]["api_key"] == "[REDACTED]"


def test_model_response_serializes():
    response = ModelResponse(provider="mock", model="mock-model", content="content")

    assert response.to_dict()["content"] == "content"


def test_model_request_validation_flags_malformed_request():
    request = ModelRequest(
        provider="",
        model="",
        messages=[ModelMessage(role="invalid", content="")],
        temperature=3,
        max_output_tokens=0,
    )

    errors = request.validate()

    assert "Provider must not be empty." in errors
    assert "Model must not be empty." in errors
    assert any("unsupported role" in error for error in errors)
    assert any("content must not be empty" in error for error in errors)
    assert "Temperature must be between 0 and 2." in errors
    assert "max_output_tokens must be positive." in errors
