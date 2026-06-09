from pathlib import Path

from karakana.skills.validator import SkillValidator


VALID_SKILL = """---
name: example-skill
description: Use this skill for tests.
version: 0.1.0
risk_level: low
allowed_tools:
  - read_file
requires_approval_for: []
---
# Example Skill

## Purpose

Testing.

## When to use this skill

Use in tests.

## When not to use this skill

Do not use outside tests.

## Core concepts

- Keep fixtures small.

## Standard workflow

1. Arrange.
2. Act.
3. Assert.

## Safety rules

- Do not mutate unrelated files.

## Required checks

- Run tests.

## Output format

Return test result.

## Examples

- Validate a fixture.

## Quick Reference

- Use this fixture for validation tests.

## Pitfalls

- Keep fixture expectations explicit.

## Verification

- Run skill validator tests.
"""


def write_skill(root: Path, body: str = VALID_SKILL, dirname: str = "example-skill") -> Path:
    skill_dir = root / dirname
    skill_dir.mkdir(parents=True)
    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text(body, encoding="utf-8")
    return skill_dir


def test_valid_skill_passes(tmp_path):
    skill_dir = write_skill(tmp_path)

    result = SkillValidator().validate(skill_dir)

    assert result.is_valid
    assert result.errors == []
    assert result.warnings == []


def test_missing_skill_file_fails(tmp_path):
    skill_dir = tmp_path / "missing"
    skill_dir.mkdir()

    result = SkillValidator().validate(skill_dir)

    assert not result.is_valid
    assert "Missing SKILL.md" in result.errors[0]


def test_missing_front_matter_fails(tmp_path):
    skill_dir = write_skill(tmp_path, "# No Front Matter\n")

    result = SkillValidator().validate(skill_dir)

    assert not result.is_valid
    assert "Missing YAML front matter" in result.errors


def test_missing_required_field_fails(tmp_path):
    body = VALID_SKILL.replace("version: 0.1.0\n", "")
    skill_dir = write_skill(tmp_path, body)

    result = SkillValidator().validate(skill_dir)

    assert "Missing required metadata: version" in result.errors


def test_invalid_risk_level_fails(tmp_path):
    body = VALID_SKILL.replace("risk_level: low", "risk_level: unsafe")
    skill_dir = write_skill(tmp_path, body)

    result = SkillValidator().validate(skill_dir)

    assert "Invalid risk_level: unsafe" in result.errors


def test_required_section_warning(tmp_path):
    body = VALID_SKILL.replace("## Examples\n\n- Validate a fixture.\n", "")
    skill_dir = write_skill(tmp_path, body)

    result = SkillValidator().validate(skill_dir)

    assert result.is_valid
    assert "Missing required section: ## Examples" in result.warnings


def test_name_must_match_directory(tmp_path):
    skill_dir = write_skill(tmp_path, dirname="wrong-name")

    result = SkillValidator().validate(skill_dir)

    assert "Skill name 'example-skill' does not match directory 'wrong-name'" in result.errors
