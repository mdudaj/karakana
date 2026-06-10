from karakana.actions.extractor import ActionExtractor
from karakana.actions.store import ActionStore
from tests.test_action_extractor import write_response


def test_action_summary_includes_suggested_skills_and_handoff_reference(tmp_path):
    response = write_response(
        tmp_path,
        """Suggested skills: karakana-handoff

## Next Actions
- Handoff: Prepare current state for the next agent.
""",
        {"status": "passed", "blocked": False},
    )
    bundle = ActionExtractor().extract_from_response(response)
    path = ActionStore(tmp_path).save(bundle)

    text = (path.parent / "actions.md").read_text(encoding="utf-8")

    assert "## Suggested Skills" in text
    assert "karakana-handoff" in text
    assert "See `handoff.md`" in text
