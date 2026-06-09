import json

import pytest

from karakana.actions.extractor import ActionExtractor


def write_response(tmp_path, text: str, review: dict | None = None):
    path = tmp_path / ".karakana" / "runs" / "run" / "artifacts" / "model-response.md"
    path.parent.mkdir(parents=True)
    path.write_text(text, encoding="utf-8")
    if review is not None:
        (path.parent / "response-review.json").write_text(json.dumps(review), encoding="utf-8")
    return path


def test_extracts_next_actions_and_classifies_types(tmp_path):
    response = write_response(
        tmp_path,
        """## Next Actions
- Codex task: Implement the parser tests.
- Create issue: Track documentation gap.
- Add eval: Add regression case for workflow state.
""",
        {"status": "passed", "blocked": False},
    )

    bundle = ActionExtractor().extract_from_response(response, project="karakana", skill="viewflow-framework")

    assert [action.action_type for action in bundle.actions] == ["codex_task", "github_issue_draft", "eval_case"]
    assert bundle.source.run_id == "run"


def test_todo_lines_and_high_risk_detection(tmp_path):
    response = write_response(tmp_path, "TODO: Update skill for permission migration review.", {"status": "warning", "blocked": False})

    bundle = ActionExtractor().extract_from_response(response)

    assert bundle.actions[0].action_type == "skill_update"
    assert bundle.actions[0].risk_level == "high"


def test_fallback_manual_review_when_no_actions(tmp_path):
    response = write_response(tmp_path, "This response has no structured action markers.")

    bundle = ActionExtractor().extract_from_response(response)

    assert bundle.actions[0].action_type == "manual_review"
    assert bundle.warnings


def test_blocked_response_creates_blocked_bundle(tmp_path):
    response = write_response(tmp_path, "TODO: Implement unsafe change.", {"status": "blocked", "blocked": True})

    bundle = ActionExtractor().extract_from_response(response)

    assert bundle.status == "blocked"
    assert bundle.actions == []


def test_require_passed_review_enforced(tmp_path):
    response = write_response(tmp_path, "TODO: Implement safe change.")

    with pytest.raises(ValueError, match="passed or warning"):
        ActionExtractor().extract_from_response(response, require_passed_review=True)
