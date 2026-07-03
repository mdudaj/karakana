from karakana.models.router import infer_task_type, route_model


def test_route_model_defaults_for_planning():
    route = route_model("planning")

    assert route["provider"] == "github"
    assert route["model"] == "gpt-5-mini"
    assert route["cost_tier"] == "low_to_medium"
    assert route["capability_tier"] == "planning_reasoning"
    assert route["role"] == "planner"
    assert route["token_budget"] == "standard"
    assert "GitHub inference" in route["token_policy"]


def test_route_model_deep_planning_uses_stronger_model():
    route = route_model("implementation_planning")

    assert route["provider"] == "openai_codex"
    assert route["model"] == "gpt-5.4"
    assert route["role"] == "deep_planner"
    assert route["token_budget"] == "large"


def test_route_model_high_risk_planning_uses_principal_model():
    route = route_model("model_routing_planning")

    assert route["provider"] == "openai_codex"
    assert route["model"] == "gpt-5.5"
    assert route["role"] == "principal_planner"
    assert route["token_budget"] == "reserved"


def test_route_model_overrides():
    route = route_model("planning", provider="mock", model="mock-model")

    assert route["provider"] == "mock"
    assert route["model"] == "mock-model"
    assert route["manual_override"] is True
    assert route["role"] == "planner"


def test_route_model_unknown_uses_dry_run_role():
    route = route_model("unclassified_work")

    assert route["provider"] == "mock"
    assert route["role"] == "dry_run"
    assert route["token_budget"] == "none"


def test_infer_task_type_routes_high_risk_task_text():
    assert infer_task_type("Implement authentication and permission checks") == "security_or_auth_change"
    assert infer_task_type("Plan authentication rollout", intent="planning") == "high_risk_planning"


def test_infer_task_type_routes_routine_task_text():
    assert infer_task_type("Write regression tests for the parser") == "test_generation"
    assert infer_task_type("Update the README documentation") == "documentation"
