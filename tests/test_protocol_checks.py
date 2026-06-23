import json
from pathlib import Path

from typer.testing import CliRunner

from karakana.cli import app
from karakana.protocols.artifacts import missing_artifact_suggestions, render_template
from karakana.protocols.checks import check_trace_protocol_artifacts
from karakana.traces.schemas import TraceArtifact
from karakana.traces.store import TraceStore


def write_minimal_requirement(root):
    req = root / ".karakana" / "requirements" / "req-demo"
    req.mkdir(parents=True)
    (root / ".karakana" / "requirements" / "latest").write_text("req-demo\n", encoding="utf-8")
    (req / "prd.json").write_text(
        json.dumps(
            {
                "req_id": "req-demo",
                "title": "Improve dashboard UX",
                "project": "karakana",
                "skillpack": "karakana",
                "status": "draft",
                "source": {"source_type": "note"},
                "context": "Context",
                "problem": "Problem",
                "goal": "Improve dashboard UX.",
            }
        ),
        encoding="utf-8",
    )


def write_minimal_skillpack(root):
    protocols = root / "protocols"
    protocols.mkdir(parents=True, exist_ok=True)
    for protocol_id, category in [
        ("python-code-change", "implementation"),
        ("requirements-change", "requirements"),
        ("ux-change", "frontend"),
    ]:
        (protocols / f"{protocol_id}.yml").write_text(
            f"""protocol_id: {protocol_id}
name: {protocol_id}
version: 0.1.0
category: {category}
risk_floor: low
summary: Test protocol
roles: [planner]
steps:
  - step_id: classify
    action: classify
    instruction: classify
artifacts:
  - kind: trace
  - kind: requirements_note
verification: [verify]
""",
            encoding="utf-8",
        )
    skillpack = root / "skillpacks" / "karakana.yml"
    skillpack.parent.mkdir(parents=True)
    skillpack.write_text(
        """name: karakana
description: Test skillpack
version: 0.1.0
status: stable
project:
  id: karakana
  display_name: Karakana
skills:
  required: []
  optional: []
protocols:
  default: python-code-change
  categories:
    requirements: requirements-change
    frontend: ux-change
""",
        encoding="utf-8",
    )


def test_protocol_check_passes_when_required_artifacts_have_evidence(tmp_path):
    store = TraceStore(tmp_path)
    trace = store.create_run(
        command="demo",
        protocol_id="python-code-change",
        work_category="implementation",
        risk_level="low",
        required_artifacts=["trace", "verification_summary"],
    )
    evidence = tmp_path / "test-result.json"
    evidence.write_text("{}", encoding="utf-8")
    trace.artifacts.append(TraceArtifact(path=str(evidence), kind="test_result"))
    trace.finish("success")
    store.save(trace)

    result = check_trace_protocol_artifacts(tmp_path, trace)

    assert result.ok
    assert result.missing_artifacts == []


def test_protocol_check_fails_missing_artifacts(tmp_path):
    store = TraceStore(tmp_path)
    trace = store.create_run(
        command="demo",
        protocol_id="python-code-change",
        work_category="implementation",
        risk_level="low",
        required_artifacts=["trace", "requirements_note", "user_story"],
    )
    trace.finish("success")
    store.save(trace)

    result = check_trace_protocol_artifacts(tmp_path, trace)

    assert not result.ok
    assert result.status == "failed"
    assert result.missing_artifacts == ["requirements_note", "user_story"]


def test_protocol_check_cli_exits_nonzero_for_missing_artifacts(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    store = TraceStore(tmp_path)
    trace = store.create_run(
        command="demo",
        protocol_id="python-code-change",
        work_category="implementation",
        risk_level="low",
        required_artifacts=["trace", "requirements_note"],
    )
    trace.finish("success")
    store.save(trace)

    result = CliRunner().invoke(app, ["protocol", "check", "--trace", trace.run_id])

    assert result.exit_code == 1
    assert "requirements_note" in result.output


def test_handoff_refresh_warns_about_missing_protocol_artifacts(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_minimal_skillpack(tmp_path)
    store = TraceStore(tmp_path)
    trace = store.create_run(
        command="demo",
        project="karakana",
        protocol_id="python-code-change",
        work_category="implementation",
        risk_level="low",
        required_artifacts=["trace", "requirements_note"],
    )
    trace.finish("success")
    store.save(trace)

    result = CliRunner().invoke(app, ["handoff", "refresh", "--project", "karakana", "--skillpack", "karakana"])

    assert result.exit_code == 0
    handoff_paths = sorted((tmp_path / ".karakana" / "handoffs").glob("*/handoff.md"))
    assert handoff_paths
    handoff_text = handoff_paths[-1].read_text(encoding="utf-8")
    assert "Protocol check" in handoff_text
    assert "Missing protocol artifacts: requirements_note" in handoff_text


def test_handoff_refresh_can_require_protocol_pass(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_minimal_skillpack(tmp_path)
    store = TraceStore(tmp_path)
    trace = store.create_run(
        command="demo",
        project="karakana",
        protocol_id="python-code-change",
        work_category="implementation",
        risk_level="low",
        required_artifacts=["trace", "requirements_note"],
    )
    trace.finish("success")
    store.save(trace)

    result = CliRunner().invoke(
        app,
        ["handoff", "refresh", "--project", "karakana", "--skillpack", "karakana", "--require-protocol-pass"],
    )

    assert result.exit_code == 1
    assert "Protocol check failed" in result.output


def test_patch_gate_warns_on_linked_protocol_check(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    store = TraceStore(tmp_path)
    trace = store.create_run(
        command="demo",
        project="karakana",
        protocol_id="python-code-change",
        work_category="implementation",
        risk_level="low",
        required_artifacts=["trace", "requirements_note"],
    )
    trace.finish("success")
    store.save(trace)
    patch_root = tmp_path / ".karakana" / "patches" / "patch-1"
    patch_root.mkdir(parents=True)
    diff_path = patch_root / "changes.diff"
    diff_path.write_text("diff --git a/a.py b/a.py\n", encoding="utf-8")
    (patch_root / "patch.json").write_text(
        json.dumps(
            {
                "patch_run_id": "patch-1",
                "source_task_id": trace.run_id,
                "created_at": "",
                "git_branch": "feature",
                "git_status": "",
                "diff_path": str(diff_path),
                "summary_path": str(patch_root / "summary.md"),
                "tests_path": None,
                "files_changed": ["a.py"],
                "warnings": [],
                "errors": [],
                "project": "karakana",
                "skillpack": None,
                "repository_path": str(tmp_path),
            }
        ),
        encoding="utf-8",
    )

    result = CliRunner().invoke(app, ["patch", "gate", "--patch-run", "patch-1", "--json"])

    assert result.exit_code == 0
    gate_json = json.loads((sorted((tmp_path / ".karakana" / "patch-gates").glob("*/gate.json"))[-1]).read_text(encoding="utf-8"))
    assert gate_json["metadata"]["protocol_check_status"] == "failed"
    assert "requirements_note" in gate_json["metadata"]["protocol_check_missing_artifacts"]


def test_protocol_template_cli_lists_prints_and_writes(tmp_path, monkeypatch):
    monkeypatch.chdir(Path.cwd())
    runner = CliRunner()
    output = tmp_path / "requirements-note.md"

    list_result = runner.invoke(app, ["protocol", "template"])
    print_result = runner.invoke(app, ["protocol", "template", "requirements_note"])
    write_result = runner.invoke(app, ["protocol", "template", "requirements_note", "--output", str(output)])

    assert list_result.exit_code == 0
    assert "requirements_note" in list_result.output
    assert print_result.exit_code == 0
    assert "# Requirements Note" in print_result.output
    assert write_result.exit_code == 0
    assert output.exists()


def test_missing_suggestions_include_template_and_attach_commands(tmp_path):
    store = TraceStore(tmp_path)
    trace = store.create_run(
        command="demo",
        protocol_id="python-code-change",
        work_category="implementation",
        risk_level="low",
        required_artifacts=["trace", "requirements_note"],
    )
    trace.finish("success")
    store.save(trace)
    templates = tmp_path / "templates" / "protocols"
    templates.mkdir(parents=True)
    (templates / "requirements-note.md").write_text("# Requirements Note\n", encoding="utf-8")

    suggestions = missing_artifact_suggestions(tmp_path, trace.run_id)

    assert suggestions[0].artifact_kind == "requirements_note"
    assert "protocol template requirements_note" in suggestions[0].template_command
    assert f"protocol attach --trace {trace.run_id}" in suggestions[0].attach_command


def test_protocol_attach_cli_makes_check_pass(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    store = TraceStore(tmp_path)
    trace = store.create_run(
        command="demo",
        protocol_id="python-code-change",
        work_category="implementation",
        risk_level="low",
        required_artifacts=["trace", "requirements_note"],
    )
    trace.finish("success")
    store.save(trace)
    artifact = tmp_path / "requirements-note.md"
    artifact.write_text("# Requirements Note\n", encoding="utf-8")

    attach_result = CliRunner().invoke(
        app,
        ["protocol", "attach", "--trace", trace.run_id, "--kind", "requirements_note", "--path", str(artifact)],
    )
    check_result = CliRunner().invoke(app, ["protocol", "check", "--trace", trace.run_id])

    assert attach_result.exit_code == 0
    assert check_result.exit_code == 0
    assert "Protocol check: passed" in check_result.output


def test_all_declared_templates_render():
    for artifact_kind in [
        "acceptance_criteria",
        "adr",
        "definition_of_done",
        "migration_plan",
        "requirements_note",
        "rollback_plan",
        "safety_review",
        "schema_contract",
        "threat_or_abuse_case_note",
        "user_story",
        "ux_description",
        "verification_summary",
    ]:
        assert render_template(Path.cwd(), artifact_kind).startswith("#")


def test_protocol_start_cli_writes_start_artifacts(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_minimal_skillpack(tmp_path)

    result = CliRunner().invoke(
        app,
        ["protocol", "start", "--task", "Write requirements and user stories.", "--project", "karakana", "--write-plan"],
    )

    assert result.exit_code == 0
    assert "Protocol: requirements-change" in result.output
    start_paths = sorted((tmp_path / ".karakana" / "protocol-starts").glob("*/start.json"))
    assert start_paths
    data = json.loads(start_paths[-1].read_text(encoding="utf-8"))
    assert data["classification"]["protocol_id"] == "requirements-change"
    assert "requirements_note" in data["required_artifacts"]


def test_protocol_start_cli_uses_requirements_source(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_minimal_skillpack(tmp_path)
    write_minimal_requirement(tmp_path)

    result = CliRunner().invoke(
        app,
        ["protocol", "start", "--from-requirements", "req-demo", "--write-plan", "--json"],
    )

    assert result.exit_code == 0
    assert '"source_type": "requirements"' in result.output
    assert '"protocol_id": "ux-change"' in result.output


def test_protocol_start_rejects_multiple_sources(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["protocol", "start", "--task", "One", "--from-note", "Two"])

    assert result.exit_code == 1
    assert "Provide exactly one" in result.output
