from karakana.models.router import MODEL_TIERS, route_model


def test_documentation_routes_to_haiku():
    route = route_model("documentation")

    assert route["provider"] == "github"
    assert route["model"] == "claude-haiku-4.5"
    assert route["role"] == "triage_summarizer"
    assert route["token_budget"] == "small"


def test_planning_routes_to_gpt5_mini():
    route = route_model("planning")

    assert route["provider"] == "github"
    assert route["model"] == "gpt-5-mini"
    assert route["role"] == "planner"
    assert "requirements" in route["token_policy"]


def test_routine_code_routes_to_codex_mini():
    route = route_model("routine_code_implementation")

    assert route["provider"] == "openai_codex"
    assert route["model"] == "gpt-5.4-mini"
    assert route["role"] == "routine_implementer"


def test_test_generation_routes_to_codex_mini():
    route = route_model("test_generation")

    assert route["provider"] == "openai_codex"
    assert route["model"] == "gpt-5.4-mini"
    assert route["role"] == "routine_implementer"


def test_ci_repair_and_refactoring_route_to_codex_5_4():
    assert route_model("ci_repair")["model"] == "gpt-5.4"
    assert route_model("refactoring")["model"] == "gpt-5.4"


def test_high_risk_routes_use_codex_5_5():
    for task_type in [
        "high_risk_code_review",
        "security_or_auth_change",
        "payment_or_billing_logic",
        "database_or_index_migration",
        "viewflow_process_state_change",
    ]:
        route = route_model(task_type)
        assert route["provider"] == "openai_codex"
        assert route["model"] == "gpt-5.5"


def test_cost_tier_metadata():
    assert MODEL_TIERS["claude-haiku-4.5"]["cost_tier"] == "low"
    assert MODEL_TIERS["gpt-5.5"]["capability_tier"] == "principal_engineer"


def test_principal_routes_are_reserved_budget():
    route = route_model("security_or_auth_change")

    assert route["role"] == "principal_reviewer"
    assert route["token_budget"] == "reserved"
    assert "highest-cost route" in route["token_policy"]
