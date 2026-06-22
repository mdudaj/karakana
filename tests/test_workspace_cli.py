from typer.testing import CliRunner

from karakana.cli import app


def test_workspace_cli_commands():
    runner = CliRunner()

    assert runner.invoke(app, ["workspace", "list"]).exit_code == 0
    assert runner.invoke(app, ["workspace", "show", "default"]).exit_code == 0
    assert runner.invoke(app, ["workspace", "validate", "default"]).exit_code == 0
    assert runner.invoke(app, ["workspace", "activate", "default"]).exit_code == 0
    assert runner.invoke(app, ["workspace", "current"]).exit_code == 0
    assert runner.invoke(app, ["workspace", "status", "--workspace", "default"]).exit_code == 0
    assert runner.invoke(app, ["workspace", "summary", "default"]).exit_code == 0


def test_workspace_plan_and_handoff_cli():
    runner = CliRunner()

    plan = runner.invoke(app, ["workspace", "plan", "--workspace", "default", "--project", "karakana", "--task", "Review workspace"])
    assert plan.exit_code == 0
    assert "Workspace plan written" in plan.output

    handoff = runner.invoke(app, ["workspace", "handoff", "--workspace", "default", "--project", "karakana"])
    assert handoff.exit_code == 0
    assert "Workspace handoff written" in handoff.output
