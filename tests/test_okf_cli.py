from typer.testing import CliRunner

from karakana.cli import app


def test_okf_validate_cli_passes_for_repository_bundle():
    result = CliRunner().invoke(app, ["okf", "validate"])

    assert result.exit_code == 0
    assert "OKF validation: passed" in result.output
    assert "Concepts by type:" in result.output
    assert "Concepts by project:" in result.output
    assert "karakana" in result.output
    assert "msc-platform" in result.output


def test_okf_validate_cli_accepts_explicit_file():
    result = CliRunner().invoke(app, ["okf", "validate", "okf/karakana/project.md"])

    assert result.exit_code == 0
    assert "Concepts: 1" in result.output
    assert "Project: 1" in result.output
