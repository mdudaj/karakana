from karakana.actions.extractor import ActionExtractor
from karakana.actions.store import ActionStore, generate_action_run_id
from tests.test_action_extractor import write_response


def test_action_run_id_shape():
    assert "-actions-" in generate_action_run_id()


def test_action_store_writes_summary_and_artifacts(tmp_path):
    response = write_response(
        tmp_path,
        """## Next Actions
- Codex task: Implement test coverage.
- Create issue: Track follow-up.
- Update skill: Add verification note.
- Next action: Review checklist.
""",
        {"status": "passed", "blocked": False},
    )
    bundle = ActionExtractor().extract_from_response(response)
    path = ActionStore(tmp_path).save(bundle)

    assert path.exists()
    root = path.parent
    assert (root / "actions.md").exists()
    assert (root / "handoff.md").exists()
    assert list((root / "codex-tasks").glob("*.md"))
    assert list((root / "issue-drafts").glob("*.md"))
    assert list((root / "proposals").glob("*.md"))
    assert list((root / "checklists").glob("*.md"))
    assert ActionStore(tmp_path).latest().action_run_id == bundle.action_run_id
