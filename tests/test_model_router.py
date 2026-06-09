from karakana.models.router import route_model


def test_route_model_defaults_for_planning():
    route = route_model("planning")

    assert route == {"provider": "github", "model": "gpt-5-mini"}


def test_route_model_overrides():
    route = route_model("planning", provider="mock", model="mock-model")

    assert route == {"provider": "mock", "model": "mock-model"}
