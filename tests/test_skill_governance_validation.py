from pathlib import Path

from typer.testing import CliRunner

from karakana.cli import app
from karakana.skills.validator import SkillValidator
from tests.test_skill_optional_metadata import write_skill


def test_invalid_scope_is_validation_error(tmp_path):
    skill_root = write_skill(tmp_path, "scope: remote\n")

    result = SkillValidator().validate(skill_root)

    assert "Invalid scope: remote" in result.errors


def test_unknown_category_is_warning(tmp_path):
    skill_root = write_skill(tmp_path, "category: experimental\n")

    result = SkillValidator().validate(skill_root)

    assert "Unknown category: experimental" in result.warnings
    assert result.is_valid


def test_invalid_activation_is_validation_error(tmp_path):
    skill_root = write_skill(
        tmp_path,
        """activation:
  keywords: django
""",
    )

    result = SkillValidator().validate(skill_root)

    assert "activation.keywords must be a list of strings" in result.errors


def test_missing_recommended_sections_warn_but_do_not_fail(tmp_path):
    skill_root = write_skill(tmp_path)

    result = SkillValidator().validate(skill_root)

    assert "Missing recommended section: ## Quick Reference" in result.warnings
    assert "Missing recommended section: ## Pitfalls" in result.warnings
    assert "Missing recommended section: ## Verification" in result.warnings
    assert result.is_valid


def test_existing_skills_validate_all(tmp_path, monkeypatch):
    monkeypatch.chdir(Path(__file__).resolve().parents[1])

    result = CliRunner().invoke(app, ["skill", "validate-all"])

    assert result.exit_code == 0
    assert "Invalid scope" not in result.output
