from karakana.actions.extractor import ActionExtractor
from karakana.actions.store import ActionStore
from tests.test_action_extractor import write_response


def test_handoff_artifact_is_always_created(tmp_path):
    response = write_response(tmp_path, "TODO: Update documentation for handoff behavior.", {"status": "passed", "blocked": False})
    bundle = ActionExtractor().extract_from_response(response)
    path = ActionStore(tmp_path).save(bundle)

    handoff = path.parent / "handoff.md"

    assert handoff.exists()
    text = handoff.read_text(encoding="utf-8")
    assert "# Handoff" in text
    assert "## Suggested Skills" in text
    assert "## Definition of Done" in text
