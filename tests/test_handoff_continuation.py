import json

import pytest
from typer.testing import CliRunner

from karakana.cli import app
from karakana.handoffs.builder import create_handoff
from karakana.handoffs.continuation import build_continuation, next_stage, render_continuation
from karakana.handoffs.schemas import HandoffArtifact
from karakana.handoffs.store import HandoffStore
from karakana.handoffs.summary import render_session_start
from tests.test_session_handoff import write_project_context, write_milestone


def test_reviewed_stages_enable_delivery_and_changes_reopen_stage(tmp_path):
    refs = []
    for stage in ("research", "architect", "plan"):
        (tmp_path / stage).write_text(f"Reviewed {stage}")
        refs.append(f"{stage}={stage}")
    guidance = build_continuation(tmp_path, "Implement export tests", {}, refs, reviewed=True)
    assert next_stage(guidance) == "deliver"
    (tmp_path / "architect").write_text("Changed decision")
    assert next_stage(guidance) == "architect"
    (tmp_path / "research").unlink()
    assert next_stage(guidance) == "research"


@pytest.mark.parametrize("refs,reviewed", [
    (["research=missing"], True), (["research=plan"], False),
    (["deliver=plan"], True), (["research=plan", "research=plan"], True),
])
def test_invalid_or_unreviewed_reuse_is_rejected(tmp_path, refs, reviewed):
    (tmp_path / "plan").write_text("Evidence")
    with pytest.raises(ValueError):
        build_continuation(tmp_path, "Write tests", {}, refs, reviewed)


def test_routing_uses_task_risk_and_respects_project_override(tmp_path):
    low = build_continuation(tmp_path, "Write changelog", {})
    high = build_continuation(tmp_path, "Fix authorization", {})
    assert low["model_route"]["model"] != high["model_route"]["model"]
    kind = low["model_route"]["task_type"]
    override = {kind: {"provider": "openai_codex", "model": "project-model"}}
    assert build_continuation(tmp_path, "Write changelog", override)["model_route"]["model"] == "project-model"
    assert low["conversation"] == "continue"
    assert build_continuation(tmp_path, "Write tests", {}, slice_complete=True)["conversation"] == "new"


def test_two_failed_attempts_require_diagnostic_review(tmp_path):
    guidance = build_continuation(tmp_path, "Fix typo", {}, failed_attempts=2)
    assert guidance["conversation"] == "new"
    assert guidance["model_route"]["task_type"] == "high_risk_code_review"
    assert "diagnostic escalation" in next_stage(guidance)
    rendered = render_continuation(guidance)
    assert "no automatic switch" in rendered
    assert "full required regression gate" in rendered
    assert "No automatic multi-agent fan-out" in rendered


def test_cli_refresh_supersedes_stale_milestone_and_loads_guidance(tmp_path, monkeypatch):
    write_project_context(tmp_path)
    write_milestone(tmp_path)
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    result = runner.invoke(app, ["handoff", "refresh", "--project", "demo",
                                "--next-task", "Write changelog", "--slice-complete"])
    assert result.exit_code == 0, result.output
    artifact = HandoffStore(tmp_path).latest("demo")
    assert artifact.exact_next_action == "Write changelog"
    assert artifact.continuation["conversation"] == "new"
    loaded = runner.invoke(app, ["handoff", "load", "--project", "demo", "--no-okf-context"])
    assert loaded.exit_code == 0, loaded.output
    assert "Recommended model:" in loaded.output
    assert "Conversation: new" in loaded.output


def test_legacy_handoff_remains_loadable_and_secret_is_redacted(tmp_path):
    write_project_context(tmp_path)
    handoff = create_handoff(tmp_path, "demo", next_task="Write changelog token=supersecretvalue")
    assert "supersecretvalue" not in json.dumps(handoff.to_dict())
    legacy = handoff.to_dict()
    legacy.pop("continuation")
    restored = HandoffArtifact.from_dict(legacy)
    assert "Not selected" in render_session_start(restored, "handoff.md")


def test_nested_continuation_uses_handoff_redaction(tmp_path):
    write_project_context(tmp_path)
    data = create_handoff(tmp_path, "demo").to_dict()
    data["continuation"] = {"next_task": "Inspect postgres://name:privatevalue@host/db"}
    restored = HandoffArtifact.from_dict(data)
    assert "privatevalue" not in render_session_start(restored, "handoff.md")


def test_cli_create_accepts_reviewed_reuse(tmp_path, monkeypatch):
    write_project_context(tmp_path)
    (tmp_path / "decision.md").write_text("Approved research, architecture, plan")
    monkeypatch.chdir(tmp_path)
    args = ["handoff", "create", "--project", "demo", "--next-task", "Write tests", "--reuse-reviewed"]
    for stage in ("research", "architect", "plan"):
        args += ["--reuse-stage", f"{stage}=decision.md"]
    result = CliRunner().invoke(app, args)
    assert result.exit_code == 0, result.output
    artifact = HandoffStore(tmp_path).latest("demo")
    assert next_stage(artifact.continuation) == "deliver"
    assert str(tmp_path / "decision.md") in artifact.reference_artifacts
