from typer.testing import CliRunner

from karakana.cli import app


def test_skill_list_cli():
    result = CliRunner().invoke(app, ["skill", "list"])

    assert result.exit_code == 0
    assert "invenio-framework" in result.output
    assert "karakana-self-improvement" in result.output


def test_skill_show_cli():
    result = CliRunner().invoke(app, ["skill", "show", "invenio-framework"])

    assert result.exit_code == 0
    assert "Name: invenio-framework" in result.output
    assert "Risk level: high" in result.output


def test_skill_validate_cli():
    result = CliRunner().invoke(app, ["skill", "validate", "skills/invenio-framework"])

    assert result.exit_code == 0
    assert "OK" in result.output


def test_skill_validate_all_cli():
    result = CliRunner().invoke(app, ["skill", "validate-all"])

    assert result.exit_code == 0
    assert "skills/invenio-framework/SKILL.md" in result.output
