from karakana.models.escalation import recommend_escalation


def test_escalates_haiku_to_gpt5_mini():
    result = recommend_escalation("github", "claude-haiku-4.5", ["architecture_reasoning_needed"])

    assert result["should_escalate"] is True
    assert result["to_provider"] == "github"
    assert result["to_model"] == "gpt-5-mini"


def test_escalates_gpt5_mini_to_codex_mini():
    result = recommend_escalation("github", "gpt-5-mini", ["tests_need_writing"])

    assert result["should_escalate"] is True
    assert result["to_provider"] == "openai_codex"
    assert result["to_model"] == "gpt-5.4-mini"


def test_escalates_codex_mini_to_5_4():
    result = recommend_escalation("openai_codex", "gpt-5.4-mini", ["tests_fail_after_first_patch"])

    assert result["should_escalate"] is True
    assert result["to_model"] == "gpt-5.4"


def test_escalates_codex_5_4_to_5_5():
    result = recommend_escalation("openai_codex", "gpt-5.4", ["security_or_authentication_change"])

    assert result["should_escalate"] is True
    assert result["to_model"] == "gpt-5.5"


def test_no_escalation_without_matching_signal():
    result = recommend_escalation("github", "gpt-5-mini", ["unrelated"])

    assert result["should_escalate"] is False
