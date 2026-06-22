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
    assert "Ready: True" in ready.output

    show = CliRunner().invoke(app, ["requirements", "show", req_id])
    assert show.exit_code == 0
    assert "Requirement ID" in show.output

    publish = CliRunner().invoke(app, ["requirements", "publish", req_id])
    assert publish.exit_code == 0
    assert "Dry run" in publish.output
