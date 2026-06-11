from typer.testing import CliRunner

from karakana.cli import app


def test_version_command_is_polished():
    result = CliRunner().invoke(app, ["version"])

    assert result.exit_code == 0
    assert "Karakana version:" in result.output
    assert "Package: karakana" in result.output
    assert "Python:" in result.output
    assert "Status:" in result.output

