from karakana.codex.schemas import CodexHandoffTask, PatchReview, PatchReviewFinding


def test_codex_handoff_task_serializes_and_redacts():
    task = CodexHandoffTask(
        task_id="task",
        source_action_run_id="actions",
        source_action_id="action-001",
        title="Implement",
        description="Use token=abc carefully",
    )

    assert task.to_dict()["description"] == "Use token=[REDACTED] carefully"


def test_patch_review_schema():
    review = PatchReview(
        patch_run_id="patch",
        status="warning",
        risk_level="medium",
        findings=[PatchReviewFinding("missing_tests", "medium", "No tests")],
    )

    assert review.to_dict()["findings"][0]["finding_type"] == "missing_tests"
