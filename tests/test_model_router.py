from karakana.models.router import infer_task_type, route_model


def test_route_model_defaults_for_planning():
    route = route_model("planning")

    assert route["provider"] == "openai_codex"
    assert route["model"] == "gpt-5.4-mini"
    assert route["cost_tier"] == "low_to_medium"
    assert route["capability_tier"] == "routine_coding"
    assert route["role"] == "planner"
    assert route["token_budget"] == "standard"
    assert "Codex mini" in route["token_policy"]


def test_route_model_deep_planning_uses_stronger_model():
    route = route_model("implementation_planning")

    assert route["provider"] == "openai_codex"
    assert route["model"] == "gpt-5.4"
    assert route["role"] == "deep_planner"
    assert route["token_budget"] == "large"


def test_route_model_high_risk_planning_uses_principal_model():
    route = route_model("model_routing_planning")

    assert route["provider"] == "openai_codex"
    assert route["model"] == "gpt-5.6-sol"
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


def test_infer_task_type_keeps_planning_off_coding_route():
    assert infer_task_type("Plan TACATDP prototype slice 1 implementation") == "planning"


def test_infer_task_type_routes_production_publish_as_high_risk_planning():
    assert infer_task_type("Publish TACATDP app to production") == "high_risk_planning"
