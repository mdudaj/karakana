from karakana.actions.schemas import ActionBundle, ActionSource, ExtractedAction
from karakana.actions.store import ActionStore
from karakana.codex.handoff import CodexHandoffBuilder
from karakana.skillpacks.resolver import SkillpackResolver


def test_codex_handoff_includes_skillpack_tests(tmp_path):
    bundle = ActionBundle(
        action_run_id="actions",
        status="ready_for_review",
        created_at="now",
        source=ActionSource(source_type="test"),
        summary="Summary",
        actions=[ExtractedAction(action_id="a1", action_type="codex_task", title="Task", description="Implement")],
    )
    ActionStore(tmp_path).save(bundle)
    context = SkillpackResolver(__import__("pathlib").Path.cwd()).resolve_for_project("karakana")

    [path] = CodexHandoffBuilder(tmp_path).build_from_action_bundle("actions", skillpack_context=context)
    text = path.read_text(encoding="utf-8")

    assert "karakana eval run" in text
    assert "karakana-self-improvement" in text
