import json
from pathlib import Path

from typer.testing import CliRunner

from karakana.cli import app
from karakana.handoffs.builder import create_handoff
from karakana.handoffs.doctor import diagnose_handoff
from karakana.handoffs.schemas import HandoffArtifact
from karakana.handoffs.store import HandoffStore


def write_project_context(root: Path, project: str = "demo", skillpack: str | None = None) -> str:
    skillpack = skillpack or project
    (root / "KARAKANA.md").write_text("# Contract\n", encoding="utf-8")
    memory = root / "ubongo" / "projects" / project
    memory.mkdir(parents=True, exist_ok=True)
    (memory / "overview.md").write_text("# Overview\n\nCurrent bounded state.\n", encoding="utf-8")
    (root / "skillpacks").mkdir(exist_ok=True)
    (root / "skillpacks" / f"{skillpack}.yml").write_text(
        f"""name: {skillpack}
description: Test skillpack
version: 0.1.0
status: experimental
project:
  id: {project}
  memory: ubongo/projects/{project}
skills:
  required: [karakana-handoff, research-platform]
  optional: [django-debugging]
model_routes: {{}}
safety:
  high_risk_paths: []
  blocked_paths: []
  requires_approval_for: [remote_push]
tests:
  commands: [pytest]
  recommended_before_commit: []
conventions:
  notes: []
""",
        encoding="utf-8",
    )
    for name in ("karakana-handoff", "research-platform", "django-debugging"):
        skill_dir = root / "skills" / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(
            f"""---
name: {name}
description: Test skill
version: 0.1.0
risk_level: low
allowed_tools: [read_file]
requires_approval_for: []
---
# {name}

## Purpose

Test skill.
""",
            encoding="utf-8",
        )
    return skillpack


def write_milestone(root: Path, project: str = "demo", run_id: str = "20260618-010000-milestone-demo") -> Path:
    directory = root / ".karakana" / "milestones" / run_id
    directory.mkdir(parents=True)
    data = {
        "run_id": run_id,
        "project": project,
        "recommended_milestone": "Slice 1.1: Curriculum Intake Management UX",
        "current_state_summary": "Slice 1 exists but operator actions are absent.",
        "open_findings": ["No curriculum action button."],
        "generated_instructions": "LONG BODY MUST NOT BE DUPLICATED " * 200,
    }
    (directory / "next-milestone.json").write_text(json.dumps(data), encoding="utf-8")
    path = directory / "next-milestone.md"
    path.write_text("# Durable Milestone Artifact\n\nLONG BODY MUST NOT BE DUPLICATED\n", encoding="utf-8")
    return path


def test_handoff_create_writes_structured_compact_artifacts(tmp_path, monkeypatch):
    write_project_context(tmp_path)
    milestone_path = write_milestone(tmp_path)
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(
        app,
        [
            "handoff", "create", "--project", "demo", "--skillpack", "demo",
            "--purpose", "Continue the operator UX", "--from-note", "Current note.",
        ],
    )

    assert result.exit_code == 0, result.output
    handoff = HandoffStore(tmp_path).latest("demo", "demo")
    assert handoff is not None
    run_dir = HandoffStore(tmp_path).run_dir(handoff.handoff_id)
    markdown = (run_dir / "handoff.md").read_text(encoding="utf-8")
    data = json.loads((run_dir / "handoff.json").read_text(encoding="utf-8"))
    assert handoff.current_milestone == "Slice 1.1: Curriculum Intake Management UX"
    assert handoff.exact_next_action
    assert "karakana-handoff" in handoff.suggested_skills
    assert str(milestone_path) in handoff.reference_artifacts
    assert "LONG BODY MUST NOT BE DUPLICATED LONG BODY" not in markdown
    assert data["return_handoff_expected"] is True
    assert CliRunner().invoke(app, ["handoff", "show", "--project", "demo"]).exit_code == 0
    assert CliRunner().invoke(app, ["handoff", "list", "--project", "demo"]).exit_code == 0


def test_handoff_load_recovers_when_none_exists(tmp_path, monkeypatch):
    write_project_context(tmp_path)
    write_milestone(tmp_path)
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["handoff", "load", "--project", "demo", "--skillpack", "demo"])

    assert result.exit_code == 0, result.output
    assert "# Karakana Session Start" in result.output
    assert "Recovered: True" in result.output
    handoff = HandoffStore(tmp_path).latest("demo", "demo")
    assert handoff is not None and handoff.recovered is True
    assert any("Verify before acting" in note for note in handoff.staleness_notes)


def test_handoff_refresh_preserves_history(tmp_path, monkeypatch):
    write_project_context(tmp_path)
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    assert runner.invoke(app, ["handoff", "create", "--project", "demo", "--skillpack", "demo"]).exit_code == 0
    first = HandoffStore(tmp_path).latest("demo", "demo")

    result = runner.invoke(app, ["handoff", "refresh", "--project", "demo", "--skillpack", "demo", "--purpose", "Next session"])

    assert result.exit_code == 0, result.output
    handoffs = HandoffStore(tmp_path).list(project="demo")
    assert len(handoffs) == 2
    assert handoffs[0].previous_handoff_id == first.handoff_id
    assert HandoffStore(tmp_path).run_dir(first.handoff_id).exists()


def test_handoff_records_okf_concept_ids(tmp_path, monkeypatch):
    write_project_context(tmp_path)
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(
        app,
        [
            "handoff", "create", "--project", "demo", "--skillpack", "demo",
            "--okf-concept", "demo.project",
            "--changed-okf-concept", "demo.design.dashboard",
        ],
    )

    assert result.exit_code == 0, result.output
    handoff = HandoffStore(tmp_path).latest("demo", "demo")
    assert handoff.okf_concepts_loaded == ["demo.project"]
    assert handoff.okf_concepts_changed == ["demo.design.dashboard"]
    markdown = (HandoffStore(tmp_path).run_dir(handoff.handoff_id) / "handoff.md").read_text(encoding="utf-8")
    assert "## OKF Concepts Loaded" in markdown
    assert "demo.project" in markdown


def test_handoff_selection_is_project_aware(tmp_path):
    write_project_context(tmp_path, "alpha")
    write_project_context(tmp_path, "beta")
    store = HandoffStore(tmp_path)
    store.save(create_handoff(tmp_path, "alpha", "alpha", purpose="Alpha"))
    store.save(create_handoff(tmp_path, "beta", "beta", purpose="Beta"))

    assert store.latest("alpha").purpose == "Alpha"
    assert store.latest("beta").purpose == "Beta"


def test_handoff_redacts_required_secret_classes(tmp_path):
    write_project_context(tmp_path)
    note = """password=hunter2
OPENAI_API_KEY=sk-12345678901234567890
postgres://alice:secretpass@db.example/demo
-----BEGIN PRIVATE KEY-----
private material
-----END PRIVATE KEY-----
Bearer abcdefghijklmnop
"""

    handoff = create_handoff(tmp_path, "demo", "demo", from_note=note)
    path, _ = HandoffStore(tmp_path).save(handoff)
    text = path.read_text(encoding="utf-8")

    for secret in ("hunter2", "sk-12345678901234567890", "secretpass", "private material", "abcdefghijklmnop"):
        assert secret not in text
    assert "[REDACTED" in text


def test_handoff_doctor_detects_stale_missing_references_and_skills(tmp_path):
    write_project_context(tmp_path)
    handoff = HandoffArtifact(
        handoff_id="20200101-000000-handoff-old",
        created_at="2020-01-01T00:00:00+00:00",
        updated_at="2020-01-01T00:00:00+00:00",
        workspace=None,
        project="demo",
        skillpack="demo",
        current_milestone="Old milestone",
        purpose="Old purpose",
        reference_artifacts=[str(tmp_path / "missing.md")],
        suggested_skills=["missing-skill"],
        exact_next_action="Verify state.",
    )
    HandoffStore(tmp_path).save(handoff)

    report = diagnose_handoff(tmp_path, "demo", "demo", stale_after_days=1)

    assert report.status == "error"
    assert report.checks["not_stale"] is False
    assert report.checks["references_exist"] is False
    assert report.checks["suggested_skills_exist"] is False


def test_task_protocols_are_documented():
    agents = Path("AGENTS.md").read_text(encoding="utf-8")
    skills = Path("docs/skills/README.md").read_text(encoding="utf-8")
    workspaces = Path("docs/workspaces/README.md").read_text(encoding="utf-8")

    assert "## Start Every Task" in agents
    assert "## End Every Task" in agents
    assert ".venv/bin/karakana handoff load" in agents
    assert "handoff load" in skills
    assert ".venv/bin/karakana handoff load" in skills
    assert "handoff refresh" in workspaces
    assert ".venv/bin/karakana handoff load" in workspaces


def test_skillpack_plan_autoloads_recovered_handoff(tmp_path, monkeypatch):
    write_project_context(tmp_path)
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(
        app,
        ["plan", "--project", "demo", "--use-skillpack", "--task", "Review next work"],
    )

    assert result.exit_code == 0, result.output
    prompt = (tmp_path / ".karakana" / "planning-task.md").read_text(encoding="utf-8")
    assert "# Karakana Session Start" in prompt
    assert HandoffStore(tmp_path).latest("demo", "demo").recovered is True
