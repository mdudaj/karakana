from pathlib import Path

from karakana.skills.validator import SkillValidator


def test_karakana_handoff_skill_validates():
    result = SkillValidator().validate(Path("skills/karakana-handoff"))

    assert result.is_valid


def test_karakana_handoff_output_format_contains_required_sections():
    text = Path("skills/karakana-handoff/SKILL.md").read_text(encoding="utf-8")

    assert "# Handoff" in text
    assert "## Suggested Skills" in text
    assert "## Definition of Done" in text
