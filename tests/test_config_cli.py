from typer.testing import CliRunner

from karakana.cli import app


def test_config_cli_show_validate_paths():
    runner = CliRunner()

    show = runner.invoke(app, ["config", "show"])
    assert show.exit_code == 0
    assert "default_workspace" in show.output

    validate = runner.invoke(app, ["config", "validate"])
    assert validate.exit_code == 0
    assert "Config validation: passed" in validate.output

    paths = runner.invoke(app, ["config", "paths"])
    assert paths.exit_code == 0
    assert "artifact root" in paths.output

