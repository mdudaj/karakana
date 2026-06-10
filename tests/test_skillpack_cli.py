from typer.testing import CliRunner

from karakana.cli import app


def test_skillpack_list_cli():
    result = CliRunner().invoke(app, ["skillpack", "list"])

    assert result.exit_code == 0
    assert "nhrdm" in result.output


def test_skillpack_validate_cli():
    result = CliRunner().invoke(app, ["skillpack", "validate", "nhrdm"])

    assert result.exit_code == 0
    assert "OK" in result.output


def test_skillpack_summary_cli():
    result = CliRunner().invoke(app, ["skillpack", "summary", "nhrdm"])

    assert result.exit_code == 0
    assert "NHRDM" in result.output
