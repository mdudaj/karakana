"""Research closeout must make decisions and blockers actionable."""

from pathlib import Path

import pytest
import yaml
from typer.testing import CliRunner

from karakana.cli import app
from karakana.protocols.classifier import ProtocolClassifier
from karakana.protocols.checks import check_trace_protocol_artifacts, render_protocol_check
from karakana.protocols.loader import ProtocolLoader
from karakana.protocols.research_resolution import validate_research_resolution
from karakana.protocols.validator import ProtocolValidator
from karakana.traces.schemas import TraceArtifact
from karakana.traces.store import TraceStore


def make_record(tmp_path: Path, *, status: str = "ready_for_implementation") -> tuple[Path, dict]:
    (tmp_path / "requirements.md").write_text("# Requirements\n\nObservable acceptance.\n")
    (tmp_path / "design.md").write_text("# Design\n\nChosen method and rationale.\n")
    data = {
        "status": status,
        "question": "How should the bounded notification rule behave?",
        "evidence": [{"source": "apps/rules.py", "finding": "The current service checks grants."}],
        "requirements": [{"decision": "Only granted managers may publish.",
                          "acceptance": "A revoked manager is denied.", "artifact": "requirements.md"}],
        "design": [{"choice": "Use the existing publication service pattern.",
                    "rationale": "It preserves grant checks and version history.", "artifact": "design.md"}],
        "artifact_choices": [
            {"kind": "requirements", "disposition": "updated", "path": "requirements.md",
             "rationale": "Records behavior and acceptance."},
            {"kind": "design", "disposition": "updated", "path": "design.md",
             "rationale": "Records the selected architecture."},
        ],
        "authority": {"state": "approved", "evidence": "Scoped user instruction in task trace."},
        "pending_decisions": [],
        "next_action": "Implement the rule service and test role revocation.",
    }
    record = tmp_path / "research-resolution.md"
    write_record(record, data)
    return record, data


def write_record(path: Path, data: dict) -> None:
    path.write_text("---\n" + yaml.safe_dump(data, sort_keys=False) +
                    "---\n\n# Research Resolution\n\nThe evidence supports the choice above.\n")


def test_research_has_dedicated_protocol_for_project_and_global_fallback():
    root = Path.cwd()
    protocol = ProtocolLoader(root).load("research-resolution")
    assert ProtocolValidator(root).validate("research-resolution").ok
    assert "research_resolution" in {item.kind for item in protocol.artifacts}
    for project in ("karakana", "ent-meal", "msc-platform", "unknown-project"):
        result = ProtocolClassifier(root).classify("Research notification requirements and design.", project=project)
        assert result.work_category == "research"
        assert result.protocol_id == "research-resolution"
        assert "research_resolution" in result.required_artifacts
        assert not result.ux_change  # `ui` inside `requirements` is not a UX request.


def test_research_start_and_template_cli_use_closeout(isolated_repo):
    runner = CliRunner()
    started = runner.invoke(app, ["protocol", "start", "--task",
                                  "Research notification requirements and design.",
                                  "--project", "karakana", "--write-plan"])
    assert started.exit_code == 0, started.output
    assert "Protocol: research-resolution" in started.output
    assert "research_resolution" in started.output
    template = runner.invoke(app, ["protocol", "template", "research_resolution",
                                   "--output", "research-resolution.md"])
    assert template.exit_code == 0, template.output
    assert (isolated_repo / "research-resolution.md").exists()


def test_ready_research_resolution_and_protocol_gate(tmp_path):
    record, _ = make_record(tmp_path)
    assert validate_research_resolution(tmp_path, record) == []
    store = TraceStore(tmp_path)
    trace = store.create_run(command="research", project="example",
                             protocol_id="research-resolution", work_category="research",
                             risk_level="low", required_artifacts=["trace", "research_resolution"])
    trace.artifacts.append(TraceArtifact(path=str(record), kind="research_resolution"))
    store.save(trace)
    result = check_trace_protocol_artifacts(tmp_path, trace)
    assert result.ok
    assert result.metadata["evidence_scope"] == "artifact_presence_plus_research_structure"
    assert result.metadata["research_outcome"] == "ready_for_implementation"
    assert result.metadata["implementation_ready"] is True
    assert "research structure and local references" in render_protocol_check(result)


@pytest.mark.parametrize("status", ["resolved_no_change", "decision_required", "evidence_blocked"])
def test_other_research_outcomes_are_explicit(tmp_path, status):
    record, data = make_record(tmp_path, status=status)
    if status == "resolved_no_change":
        data["authority"] = {"state": "not_required", "evidence": "No source change is proposed."}
        data["next_action"] = "Close the issue with the evidence summary."
    else:
        data["authority"] = {"state": "pending", "evidence": "The owner has not decided."}
        data["pending_decisions"] = [{"owner": "Product owner", "question": "Approve the proposed rule?",
                                       "next_action": "Review the linked rule specification and decide."}]
    write_record(record, data)
    assert validate_research_resolution(tmp_path, record) == []


@pytest.mark.parametrize("mutation", [
    lambda data: data["requirements"][0].update(decision="TBD"),
    lambda data: data["design"][0].update(rationale=""),
    lambda data: data["evidence"].clear(),
    lambda data: data["requirements"][0].update(artifact="missing.md"),
    lambda data: data["artifact_choices"][0].update(path="design.md"),
    lambda data: data["artifact_choices"].pop(),
    lambda data: data["authority"].update(state="pending"),
    lambda data: data["pending_decisions"].append({"owner": "Someone", "question": "Maybe?", "next_action": "Review later"}),
])
def test_ready_closeout_rejects_incomplete_or_conflicting_choices(tmp_path, mutation):
    record, data = make_record(tmp_path)
    mutation(data)
    write_record(record, data)
    assert validate_research_resolution(tmp_path, record)


def test_blocked_closeout_requires_named_action(tmp_path):
    record, data = make_record(tmp_path, status="decision_required")
    data["authority"] = {"state": "pending", "evidence": "Approval is missing."}
    data["pending_decisions"] = [{"owner": "", "question": "Approve?", "next_action": "Later"}]
    write_record(record, data)
    assert validate_research_resolution(tmp_path, record)


def test_approval_request_must_have_reviewable_artifacts(tmp_path):
    record, data = make_record(tmp_path, status="decision_required")
    data["authority"] = {"state": "pending", "evidence": "Product approval is missing."}
    data["pending_decisions"] = [{"owner": "Product owner", "question": "Approve the rule?",
                                   "next_action": "Review the proposed contract."}]
    data["design"][0]["artifact"] = "missing-design.md"
    data["artifact_choices"][1]["path"] = "missing-design.md"
    write_record(record, data)
    assert any("design[0].artifact" in error for error in validate_research_resolution(tmp_path, record))


def test_decision_required_is_complete_research_but_not_implementation_ready(tmp_path):
    record, data = make_record(tmp_path, status="decision_required")
    data["authority"] = {"state": "pending", "evidence": "Product approval is missing."}
    data["pending_decisions"] = [{"owner": "Product owner", "question": "Approve the rule?",
                                   "next_action": "Review the proposed contract."}]
    write_record(record, data)
    store = TraceStore(tmp_path)
    trace = store.create_run(command="research", project="example",
                             protocol_id="research-resolution", work_category="research",
                             risk_level="low", required_artifacts=["trace", "research_resolution"])
    trace.artifacts.append(TraceArtifact(path=str(record), kind="research_resolution"))
    store.save(trace)
    result = check_trace_protocol_artifacts(tmp_path, trace)
    assert result.ok
    assert result.metadata["research_outcome"] == "decision_required"
    assert result.metadata["implementation_ready"] is False
    assert "Implementation ready: false" in render_protocol_check(result)


@pytest.mark.parametrize("field,value", [
    ("status", ["ready_for_implementation"]),
    ("artifact_kind", ["requirements"]),
    ("disposition", ["updated"]),
    ("authority_state", ["approved"]),
    ("artifact_row", "invalid row"),
])
def test_malformed_yaml_types_fail_as_validation_errors(tmp_path, field, value):
    record, data = make_record(tmp_path)
    if field == "artifact_kind":
        data["artifact_choices"][0]["kind"] = value
    elif field == "disposition":
        data["artifact_choices"][0]["disposition"] = value
    elif field == "authority_state":
        data["authority"]["state"] = value
    elif field == "artifact_row":
        data["artifact_choices"][0] = value
    else:
        data[field] = value
    write_record(record, data)
    assert validate_research_resolution(tmp_path, record)


def test_protocol_gate_rejects_heading_only_research_note(tmp_path):
    record = tmp_path / "research-resolution.md"
    record.write_text("# Research Resolution\n\n## Requirements\n\n## Design\n")
    store = TraceStore(tmp_path)
    trace = store.create_run(command="research", project="example",
                             protocol_id="research-resolution", work_category="research",
                             risk_level="low", required_artifacts=["trace", "research_resolution"])
    trace.artifacts.append(TraceArtifact(path=str(record), kind="research_resolution"))
    store.save(trace)
    result = check_trace_protocol_artifacts(tmp_path, trace)
    assert not result.ok
    assert result.missing_artifacts == ["research_resolution"]
    assert "Research resolution" in result.checks[-1].message
