from pathlib import Path

from karakana.skills.loader import SkillLoader


def write_skill(root: Path, metadata: str = "") -> Path:
    skill_root = root / "skills" / "demo-skill"
    skill_root.mkdir(parents=True)
    (skill_root / "SKILL.md").write_text(
        f"""---
name: demo-skill
description: Demo skill.
version: 0.1.0
risk_level: low
allowed_tools:
  - read_file
requires_approval_for: []
{metadata}---
# Demo Skill

## Purpose

Demo.

## When to use this skill

Use in tests.

## When not to use this skill

Do not use outside tests.

## Core concepts

- Demo.

## Standard workflow

1. Demo.

## Safety rules

- Stay local.

## Required checks

- Run tests.

## Output format

Return result.

## Examples

- Demo.
""",
        encoding="utf-8",
    )
    return skill_root


def test_optional_activation_scope_and_category_parse(tmp_path):
    write_skill(
        tmp_path,
        """activation:
  keywords:
    - django
  required_files:
    - manage.py
  optional_tools:
    - pytest
category: development
scope: project
""",
    )

    skill = SkillLoader(tmp_path / "skills").load_skill("demo-skill")

    assert skill.activation.keywords == ["django"]
    assert skill.activation.required_files == ["manage.py"]
    assert skill.activation.optional_tools == ["pytest"]
    assert skill.category == "development"
    assert skill.scope == "project"


def test_missing_optional_metadata_keeps_old_skill_loadable(tmp_path):
    write_skill(tmp_path)

    skill = SkillLoader(tmp_path / "skills").load_skill("demo-skill")

    assert skill.activation is None
    assert skill.category is None
    assert skill.scope is None
