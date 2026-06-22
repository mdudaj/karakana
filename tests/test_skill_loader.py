from pathlib import Path

from karakana.skills.loader import SkillLoader


def write_skill(root: Path, name: str) -> Path:
    skill_dir = root / "skills" / name
    skill_dir.mkdir(parents=True)
    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text(
        """---
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
""",
        encoding="utf-8",
    )
    return skill_file


def test_list_skills(tmp_path):
    write_skill(tmp_path, "example-skill")

    skills = SkillLoader(tmp_path / "skills").list_skills()

    assert skills == ["example-skill"]


def test_load_skill(tmp_path):
    write_skill(tmp_path, "example-skill")

    skill = SkillLoader(tmp_path / "skills").load_skill("example-skill")

    assert skill.name == "example-skill"
    assert skill.risk_level == "low"
    assert skill.allowed_tools == ["read_file"]
    assert "# Example Skill" in skill.body


def test_missing_skill_raises(tmp_path):
    loader = SkillLoader(tmp_path / "skills")

    try:
        loader.load_skill("missing")
    except FileNotFoundError as exc:
        assert "Skill not found" in str(exc)
    else:
        raise AssertionError("Expected FileNotFoundError")
