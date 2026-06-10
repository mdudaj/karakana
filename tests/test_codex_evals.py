from typer.testing import CliRunner

from karakana.cli import app


def test_codex_eval_suite_passes():
    result = CliRunner().invoke(app, ["eval", "run", "--suite", "codex"])

    assert result.exit_code == 0
    assert "Status: passed" in result.output
