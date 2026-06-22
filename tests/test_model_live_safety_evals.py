from typer.testing import CliRunner

from karakana.cli import app


def test_model_safety_eval_suite_passes():
    result = CliRunner().invoke(app, ["eval", "run", "--suite", "model"])

    assert result.exit_code == 0
    assert "Status: passed" in result.output
