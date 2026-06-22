from karakana.actions.extractor import ActionExtractor, extract_standards_spec_context
from karakana.actions.store import ActionStore
from tests.test_action_extractor import write_response


def test_extracts_standards_vs_spec_context(tmp_path):
    response = """## Standards Review

### Blocking Issues

- Missing tests for permission handling.

## Spec Review

### Missing Requirements

- Acceptance criteria did not cover migration rollback.

## Acceptance Criteria

- Tests pass.

## Next Actions

- Codex task: Implement missing permission tests.
"""

    context = extract_standards_spec_context(response)

    assert context is not None
    assert "Missing tests" in context.standards_risks[0]
    assert "migration rollback" in context.spec_gaps[0]
    assert context.acceptance_criteria == ["Tests pass."]


def test_standards_vs_spec_context_written_to_artifacts(tmp_path):
    response = write_response(
        tmp_path,
        """## Standards Review

### Blocking Issues

- Missing tests.

## Spec Review

### Missing Requirements

- Missing acceptance criterion.

## Next Actions

- Codex task: Implement missing tests.
""",
        {"status": "passed", "blocked": False},
    )
    bundle = ActionExtractor().extract_from_response(response)
    path = ActionStore(tmp_path).save(bundle)

    text = (path.parent / "actions.md").read_text(encoding="utf-8")
    codex = next((path.parent / "codex-tasks").glob("*.md")).read_text(encoding="utf-8")

    assert "Standards-vs-Spec Context" in text
    assert "Missing tests" in codex
