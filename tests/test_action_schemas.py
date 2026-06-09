from karakana.actions.schemas import ActionBundle, ActionSource, ExtractedAction


def test_action_schema_serializes_and_redacts():
    bundle = ActionBundle(
        action_run_id="run",
        status="ready_for_review",
        created_at="now",
        source=ActionSource("model_response", path="response.md", review_status="passed"),
        summary="client_secret=abc",
        actions=[
            ExtractedAction(
                action_id="action-001",
                action_type="codex_task",
                title="Implement fix",
                description="Use token=abc carefully",
            )
        ],
    )

    data = bundle.to_dict()

    assert data["summary"] == "client_secret=[REDACTED]"
    assert data["actions"][0]["description"] == "Use token=[REDACTED] carefully"


def test_invalid_action_type_fails():
    try:
        ExtractedAction(action_id="a", action_type="bad", title="Bad", description="Bad")
    except ValueError as exc:
        assert "Invalid action type" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
