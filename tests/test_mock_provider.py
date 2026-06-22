from karakana.models.providers.mock_provider import MockProvider


def test_mock_provider_returns_deterministic_response():
    provider = MockProvider()
    request = provider.build_request("Hello", "mock-model")

    response = provider.complete(request)

    assert provider.is_configured()
    assert "[MOCK MODEL RESPONSE]" in response.content
    assert response.provider == "mock"
