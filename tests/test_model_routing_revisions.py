from karakana.models.router import MODEL_TIERS, route_model


def test_documentation_routes_to_codex_mini():
    route = route_model("documentation")

    assert route["provider"] == "openai_codex"
    assert route["model"] == "gpt-5.4-mini"
    assert route["role"] == "documentation_writer"
    assert route["token_budget"] == "small"


def test_issue_triage_routes_to_triage_summarizer():
    route = route_model("issue_triage")

    assert route["provider"] == "openai_codex"
    assert route["model"] == "gpt-5.4-mini"
    assert route["role"] == "triage_summarizer"


def test_planning_routes_to_codex_mini():
    route = route_model("planning")

    assert route["provider"] == "openai_codex"
    assert route["model"] == "gpt-5.4-mini"
    assert route["role"] == "planner"
    assert "requirements" in route["token_policy"]


def test_deep_planning_routes_to_codex_5_4():
    for task_type in ["implementation_planning", "architecture_review", "framework_design", "protocol_workflow_planning", "system_assessment", "skill_design"]:
        route = route_model(task_type)
        assert route["provider"] == "openai_codex"
        assert route["model"] == "gpt-5.4"
        assert route["role"] == "deep_planner"


def test_high_risk_planning_routes_to_codex_5_6():
    for task_type in ["high_risk_planning", "model_routing_planning", "safety_policy_planning", "cross_project_architecture"]:
        route = route_model(task_type)
        assert route["provider"] == "openai_codex"
        assert route["model"] == "gpt-5.6-sol"
        assert route["role"] == "principal_planner"


def test_assessment_review_is_cost_aware_by_default():
    route = route_model("assessment_review")

    assert route["provider"] == "openai_codex"
    assert route["model"] == "gpt-5.4-mini"
    assert route["role"] == "assessment_reviewer"


def test_routine_code_routes_to_codex_mini():
    route = route_model("routine_code_implementation")

    assert route["provider"] == "openai_codex"
    assert route["model"] == "gpt-5.4-mini"
    assert route["role"] == "routine_implementer"


def test_test_generation_routes_to_codex_mini():
    route = route_model("test_generation")

    assert route["provider"] == "openai_codex"
    assert route["model"] == "gpt-5.4-mini"
    assert route["role"] == "test_designer"


def test_codex_task_drafting_routes_to_task_author():
    route = route_model("codex_task_drafting")

    assert route["provider"] == "openai_codex"
    assert route["model"] == "gpt-5.4-mini"
    assert route["role"] == "task_author"


def test_ci_repair_and_refactoring_route_to_codex_5_4():
    assert route_model("ci_repair")["model"] == "gpt-5.4"
    assert route_model("ci_repair")["role"] == "ci_analyst"
    assert route_model("refactoring")["model"] == "gpt-5.4"
    assert route_model("refactoring")["role"] == "serious_implementer"


def test_pr_review_routes_to_code_reviewer():
    route = route_model("pr_review")

    assert route["provider"] == "openai_codex"
    assert route["model"] == "gpt-5.4"
    assert route["role"] == "code_reviewer"


def test_reflection_and_research_have_non_mutating_roles():
    assert route_model("reflection")["role"] == "reflection_reviewer"
    assert route_model("research")["role"] == "researcher"
    assert route_model("evidence_review")["role"] == "researcher"


def test_high_risk_routes_use_codex_5_6():
    for task_type in [
        "high_risk_code_review",
        "security_or_auth_change",
        "payment_or_billing_logic",
        "database_or_index_migration",
        "viewflow_process_state_change",
    ]:
        route = route_model(task_type)
        assert route["provider"] == "openai_codex"
        assert route["model"] == "gpt-5.6-sol"


def test_cost_tier_metadata():
    assert MODEL_TIERS["claude-haiku-4.5"]["cost_tier"] == "low"
    assert MODEL_TIERS["gpt-5.5"]["capability_tier"] == "principal_engineer"
    assert MODEL_TIERS["gpt-5.6-sol"]["capability_tier"] == "frontier_principal_engineer"
    assert MODEL_TIERS["gpt-5.6-terra"]["cost_tier"] == "frontier"
    assert MODEL_TIERS["gpt-5.6-luna"]["cost_tier"] == "frontier"
    assert MODEL_TIERS["gpt-5.6"]["variant"] == "alias"


def test_gpt_5_6_family_manual_overrides_have_frontier_metadata():
    for model in ["gpt-5.6", "gpt-5.6-sol", "gpt-5.6-terra", "gpt-5.6-luna"]:
        route = route_model("model_routing_planning", model=model)
        assert route["model"] == model
        assert route["cost_tier"] == "frontier"
        assert route["capability_tier"] == "frontier_principal_engineer"


def test_principal_routes_are_reserved_budget():
    route = route_model("security_or_auth_change")

    assert route["role"] == "principal_reviewer"
    assert route["token_budget"] == "reserved"
    assert "frontier route" in route["token_policy"]
