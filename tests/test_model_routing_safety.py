from karakana.safety.model_routing import validate_model_route


def test_low_risk_docs_warn_for_frontier_model():
    warnings = validate_model_route("documentation", "openai_codex", "gpt-5.6-sol")

    assert warnings


def test_routine_code_warns_for_frontier_model():
    warnings = validate_model_route("routine_code_implementation", "openai_codex", "gpt-5.6-sol")

    assert any("Routine coding" in warning for warning in warnings)


def test_high_risk_warns_below_codex_5_4():
    warnings = validate_model_route("payment_or_billing_logic", "openai_codex", "gpt-5.4-mini")

    assert any("High-risk" in warning for warning in warnings)


def test_deep_planning_warns_below_codex_5_4():
    warnings = validate_model_route("implementation_planning", "github", "gpt-5-mini")

    assert any("Consequential planning" in warning for warning in warnings)


def test_high_risk_planning_warns_below_codex_5_6():
    warnings = validate_model_route("model_routing_planning", "openai_codex", "gpt-5.4")

    assert any("High-risk planning" in warning for warning in warnings)


def test_high_risk_planning_accepts_gpt_5_6_family_variants():
    for model in ["gpt-5.6", "gpt-5.6-sol", "gpt-5.6-terra", "gpt-5.6-luna"]:
        warnings = validate_model_route("model_routing_planning", "openai_codex", model, risk_level="high")
        assert not warnings
