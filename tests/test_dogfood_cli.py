from typer.testing import CliRunner

from karakana.cli import app


def test_dogfood_cli_lifecycle():
    runner = CliRunner()

    run = runner.invoke(app, ["dogfood", "run", "--project", "karakana", "--skillpack", "karakana"])
    assert run.exit_code == 0
    dogfood_id = [line.split(":", 1)[1].strip() for line in run.output.splitlines() if line.startswith("Dogfood ID:")][0]

    assert runner.invoke(app, ["dogfood", "analyze", dogfood_id]).exit_code == 0
    assert runner.invoke(app, ["dogfood", "backlog", dogfood_id]).exit_code == 0
    assert runner.invoke(app, ["dogfood", "report", dogfood_id]).exit_code == 0
    requirements = runner.invoke(app, ["dogfood", "requirements", dogfood_id])
    assert requirements.exit_code == 0
    assert "Dogfood requirements written" in requirements.output

    listed = runner.invoke(app, ["dogfood", "list"])
    assert listed.exit_code == 0
    assert dogfood_id in listed.output

    shown = runner.invoke(app, ["dogfood", "show", dogfood_id])
    assert shown.exit_code == 0
    assert "# Karakana Dogfood Report" in shown.output

    latest = runner.invoke(app, ["dogfood", "latest"])
    assert latest.exit_code == 0
    assert "# Karakana Dogfood Report" in latest.output


def test_dogfood_checklist_cli():
    result = CliRunner().invoke(app, ["dogfood", "checklist", "--project", "karakana", "--skillpack", "karakana"])

    assert result.exit_code == 0
    assert "Dogfood checklist written" in result.output
