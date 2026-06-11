from pathlib import Path

from typer.testing import CliRunner

from karakana.cli import app
from karakana.release.checks import run_release_check


def test_release_check_basic_mode():
    report, path = run_release_check(Path.cwd(), full=False)

    assert report.status in {"pass", "warning"}
    assert path.exists()
    assert any(check.name == "karakana-gitignored" for check in report.checks)


def test_release_check_cli():
    result = CliRunner().invoke(app, ["release", "check"])

    assert result.exit_code == 0
    assert "Release check status:" in result.output

