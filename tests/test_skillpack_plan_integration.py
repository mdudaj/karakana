from typer.testing import CliRunner

from karakana.cli import app


def test_plan_uses_skillpack_context(tmp_path, monkeypatch):
    monkeypatch.chdir(__import__("pathlib").Path.cwd())
    result = CliRunner().invoke(app, ["plan", "--project", "nhrdm", "--use-skillpack", "--task", "Review custom field changes"])

    assert result.exit_code == 0
    assert "Skillpack Context" in result.output
    assert "invenio-framework" in result.output


def test_plan_manual_route_override_wins():
    result = CliRunner().invoke(app, ["plan", "--project", "nhrdm", "--use-skillpack", "--task", "Review", "--provider", "mock", "--model", "mock-model"])

    assert result.exit_code == 0
    assert "Selected provider: mock" in result.output
    assert "Selected model: mock-model" in result.output
