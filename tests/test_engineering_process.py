import pytest
from typer.testing import CliRunner

from karakana.cli import app
from karakana.protocols.checks import check_trace_protocol_artifacts
from karakana.traces.schemas import TraceArtifact
from karakana.traces.store import TraceStore


def make_trace(root, required):
    store = TraceStore(root)
    trace = store.create_run(
        command="test", project="example", protocol_id="python-code-change",
        work_category="implementation", risk_level="low", required_artifacts=required,
    )
    store.save(trace)
    return trace


@pytest.mark.parametrize("kind", ["missing", "empty", "directory"])
def test_unusable_file_is_not_artifact_evidence(tmp_path, kind):
    trace = make_trace(tmp_path, ["requirements_note"])
    evidence = tmp_path / "evidence"
    if kind == "empty":
        evidence.touch()
    elif kind == "directory":
        evidence.mkdir()
    trace.artifacts.append(TraceArtifact(path=str(evidence), kind="requirements_note"))
    result = check_trace_protocol_artifacts(tmp_path, trace)
    assert not result.ok
    assert result.missing_artifacts == ["requirements_note"]


@pytest.mark.parametrize("value", ["passed", "missing.md", "", None, {}, []])
def test_output_claim_is_not_file_evidence(tmp_path, value):
    trace = make_trace(tmp_path, ["verification_summary"])
    trace.outputs["verification_summary"] = value
    assert not check_trace_protocol_artifacts(tmp_path, trace).ok


def test_existing_legacy_output_file_remains_supported(tmp_path):
    trace = make_trace(tmp_path, ["verification_summary"])
    (tmp_path / "verified.md").write_text("Focused tests passed; reviewed against criteria.")
    trace.outputs["verification_summary"] = "verified.md"
    assert check_trace_protocol_artifacts(tmp_path, trace).ok


def test_preimplementation_defers_outputs_not_requirements(tmp_path):
    trace = make_trace(tmp_path, ["trace", "task_classification", "requirements_note",
                                  "verification_summary", "handoff"])
    assert not check_trace_protocol_artifacts(tmp_path, trace, stage="pre-implementation").ok
    evidence = tmp_path / "requirements.md"
    evidence.write_text("Bounded change and observable acceptance criteria.")
    trace.artifacts.append(TraceArtifact(path=str(evidence), kind="requirements_note"))
    ready = check_trace_protocol_artifacts(tmp_path, trace, stage="pre-implementation")
    assert ready.ok
    assert ready.metadata["stage"] == "pre-implementation"
    assert ready.metadata["evidence_scope"] == "artifact_presence_only"
    assert ready.metadata["deferred_artifacts"] == ["verification_summary", "handoff"]
    done = check_trace_protocol_artifacts(tmp_path, trace)
    assert not done.ok
    assert done.missing_artifacts == ["verification_summary", "handoff"]


def test_unknown_stage_fails_closed(tmp_path):
    trace = make_trace(tmp_path, ["trace"])
    with pytest.raises(ValueError, match="stage"):
        check_trace_protocol_artifacts(tmp_path, trace, stage="skip-everything")


def test_cli_stage_is_explicit_and_completion_still_default(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    trace = make_trace(tmp_path, ["trace", "handoff"])
    runner = CliRunner()
    pre = runner.invoke(app, ["protocol", "check", "--trace", trace.run_id,
                              "--stage", "pre-implementation", "--json"])
    assert pre.exit_code == 0, pre.output
    assert '"stage": "pre-implementation"' in pre.output
    complete = runner.invoke(app, ["protocol", "check", "--trace", trace.run_id])
    assert complete.exit_code == 1


def test_valid_file_does_not_claim_semantic_verification(tmp_path):
    trace = make_trace(tmp_path, ["verification_summary"])
    evidence = tmp_path / "result.md"
    evidence.write_text("Tests failed; needs correction.")
    trace.artifacts.append(TraceArtifact(path=str(evidence), kind="verification_summary"))
    result = check_trace_protocol_artifacts(tmp_path, trace)
    assert result.ok  # Presence is deliberately separate from outcome review.
    assert result.metadata["evidence_scope"] == "artifact_presence_only"


def test_shared_guidance_reaches_protocol_and_coding_handoff():
    from karakana.codex.handoff import render_codex_handoff_task
    from karakana.codex.schemas import CodexHandoffTask
    from karakana.protocols.classifier import ProtocolClassification
    from karakana.protocols.lifecycle import render_engineering_process
    from karakana.protocols.start import ProtocolStartArtifact, render_protocol_start

    classification = ProtocolClassification(
        task="Review current behavior", project="example", skillpack=None,
        protocol_id="assessment-review", work_category="assessment", risk_level="low",
    )
    start = ProtocolStartArtifact(start_id="test", task=classification.task, classification=classification)
    task = CodexHandoffTask(task_id="test", source_action_run_id=None, source_action_id=None,
                           title="Bounded change", description="Acceptance-backed change")
    for output in (render_protocol_start(start), render_codex_handoff_task(task)):
        assert render_engineering_process() in output
