from karakana.actions.extractor import ActionExtractor
from karakana.actions.store import ActionStore
from karakana.codex.handoff import CodexHandoffBuilder
from tests.test_action_extractor import write_response


def test_codex_handoff_generation_from_action_bundle(tmp_path):
    response = write_response(tmp_path, "Codex task: Implement safe docs update.\n", {"status": "passed", "blocked": False})
    bundle = ActionExtractor(tmp_path).extract_from_response(response, project="karakana", skill="karakana-self-improvement")
    ActionStore(tmp_path).save(bundle)

    paths = CodexHandoffBuilder(tmp_path).build_from_action_bundle(bundle.action_run_id)

    assert len(paths) == 1
    assert paths[0].exists()
    text = paths[0].read_text(encoding="utf-8")
    assert "# Karakana Codex Handoff Task" in text
    assert "## Recommended Codex Model" in text
    assert "gpt-5.4-mini" in text


def test_codex_handoff_high_risk_payment_routes_to_gpt5_5(tmp_path):
    response = write_response(tmp_path, "Codex task: Implement payment migration review.\n", {"status": "passed", "blocked": False})
    bundle = ActionExtractor(tmp_path).extract_from_response(response)
    ActionStore(tmp_path).save(bundle)

    path = CodexHandoffBuilder(tmp_path).build_from_action_bundle(bundle.action_run_id)[0]

    assert "gpt-5.5" in path.read_text(encoding="utf-8")
