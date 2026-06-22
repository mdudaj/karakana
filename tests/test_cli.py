from typer.testing import CliRunner

from karakana import __version__
from karakana.cli import app


def test_cli_help_renders():
    result = CliRunner().invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Karakana AI agent harness skeleton" in result.output


def test_version_command_renders_package_version():
    result = CliRunner().invoke(app, ["version"])

    assert result.exit_code == 0
    assert f"karakana {__version__}" in result.output
