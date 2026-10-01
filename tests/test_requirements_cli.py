from typer.testing import CliRunner

from karakana.cli import app


def test_requirements_cli_prd_stories_issues_ready_show_publish(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(app, ["requirements", "prd", "--from-note", "Add a safe requirements layer", "--project", "karakana", "--no-current-skillpack"])

    assert result.exit_code == 0
    assert "Requirement ID:" in result.output
    req_id = [line.split(":", 1)[1].strip() for line in result.output.splitlines() if line.startswith("Requirement ID:")][0]

    stories = CliRunner().invoke(app, ["requirements", "stories", "--from-prd", req_id])
    assert stories.exit_code == 0
    assert "Stories:" in stories.output

    issues = CliRunner().invoke(app, ["requirements", "issues", "--from-prd", req_id])
    assert issues.exit_code == 0
    assert "Issues:" in issues.output

    ready = CliRunner().invoke(app, ["requirements", "ready", req_id])
    assert ready.exit_code == 0
    assert "Status: not_ready" in ready.output
    assert "Ready: False" in ready.output

    show = CliRunner().invoke(app, ["requirements", "show", req_id])
    assert show.exit_code == 0
    assert "Requirement ID" in show.output

    publish = CliRunner().invoke(app, ["requirements", "publish", req_id])
    assert publish.exit_code == 0
    assert "Dry run" in publish.output


def test_requirements_cli_structured_source_is_ready(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    seed = """## Specification / PRD Seed
Problem: Project handoffs omit active development items.
Goal: Link active project backlog items from each handoff.
Functional requirements:
- Handoffs include only their own project's active backlog path.
Acceptance criteria:
- Completed-only backlogs are omitted from handoffs.
"""

    generated = CliRunner().invoke(app, ["requirements", "prd", "--from-note", seed, "--project", "karakana", "--no-current-skillpack"])
    assert generated.exit_code == 0
    req_id = [line.split(":", 1)[1].strip() for line in generated.output.splitlines() if line.startswith("Requirement ID:")][0]

    ready = CliRunner().invoke(app, ["requirements", "ready", req_id, "--json"])

    assert ready.exit_code == 0
    assert "Ready: True" in ready.output
    assert '"failed": []' in ready.output
