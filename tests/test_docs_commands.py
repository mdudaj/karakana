from pathlib import Path

from typer.testing import CliRunner

from karakana.cli import app
from karakana.docs.command_reference import render_command_reference
from karakana.docs.generator import check_docs, command_reference


def test_command_reference_includes_core_groups():
    text = render_command_reference()

    for group in ["version", "doctor", "config", "workspace", "requirements", "crosslink", "release", "docs"]:
        assert f"## {group}" in text


def test_docs_command_reference_dry_run_and_write(tmp_path: Path):
    text, path = command_reference(tmp_path, write=False)
    assert "## version" in text
    assert not path.exists()

    _, path = command_reference(tmp_path, write=True)
    assert path.exists()


def test_docs_cli_commands():
    runner = CliRunner()
    preview = runner.invoke(app, ["docs", "command-reference"])
    assert preview.exit_code == 0
    assert "# Karakana Command Reference" in preview.output

    write = runner.invoke(app, ["docs", "command-reference", "--write"])
    assert write.exit_code == 0
    assert "Command reference written" in write.output

    check = runner.invoke(app, ["docs", "check"])
    assert check.exit_code == 0
    assert "Docs check: passed" in check.output


def test_docs_check_required_docs():
    missing, warnings = check_docs(Path.cwd())
    assert missing == []
    assert warnings == []

