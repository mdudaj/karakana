from pathlib import Path

from karakana.skills.validator import SkillValidator


def test_write_karakana_skill_validates():
    result = SkillValidator().validate(Path("skills/write-karakana-skill"))

    assert result.is_valid


def test_write_karakana_skill_requires_evals_for_non_trivial_skills():
    text = Path("skills/write-karakana-skill/SKILL.md").read_text(encoding="utf-8")

    assert "eval cases" in text
    assert "metadata" in text
    assert "safety rules" in text
    assert "karakana skill validate" in text
