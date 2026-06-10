from karakana.models.router import route_model


def test_route_model_defaults_for_planning():
    route = route_model("planning")

    assert route["provider"] == "github"
    assert route["model"] == "gpt-5-mini"
    assert route["cost_tier"] == "low_to_medium"
    assert route["capability_tier"] == "planning_reasoning"


def test_route_model_overrides():
    route = route_model("planning", provider="mock", model="mock-model")

    assert route["provider"] == "mock"
    assert route["model"] == "mock-model"
    assert route["manual_override"] is True
