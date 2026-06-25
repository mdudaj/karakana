from karakana.safety.model_routing import validate_model_route


def test_low_risk_docs_warn_for_gpt5_5():
    warnings = validate_model_route("documentation", "openai_codex", "gpt-5.5")

    assert warnings


def test_routine_code_warns_for_gpt5_5():
    warnings = validate_model_route("routine_code_implementation", "openai_codex", "gpt-5.5")

    assert any("Routine coding" in warning for warning in warnings)


def test_high_risk_warns_below_codex_5_4():
    warnings = validate_model_route("payment_or_billing_logic", "openai_codex", "gpt-5.4-mini")

    assert any("High-risk" in warning for warning in warnings)


def test_deep_planning_warns_below_codex_5_4():
    warnings = validate_model_route("implementation_planning", "github", "gpt-5-mini")

    assert any("Consequential planning" in warning for warning in warnings)


def test_high_risk_planning_warns_below_codex_5_5():
    warnings = validate_model_route("model_routing_planning", "openai_codex", "gpt-5.4")

    assert any("High-risk planning" in warning for warning in warnings)
