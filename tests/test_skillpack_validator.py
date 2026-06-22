from pathlib import Path

from karakana.skillpacks.validator import SkillpackValidator


def test_validate_starter_skillpack():
    result = SkillpackValidator(Path.cwd()).validate("karakana")

    assert result.ok


def test_validate_all_starter_skillpacks():
    results = SkillpackValidator(Path.cwd()).validate_all()

    assert all(result.ok for result in results)
    assert any(result.warnings for result in results)


def test_missing_required_skill_error(tmp_path):
    root = tmp_path
    (root / "skillpacks").mkdir()
    (root / "skills").mkdir()
    (root / "skillpacks" / "bad.yml").write_text(
        "name: bad\ndescription: Bad\nversion: 0.1.0\nstatus: stable\nproject:\n  id: bad\nskills:\n  required: [missing]\n",
        encoding="utf-8",
    )

    result = SkillpackValidator(root).validate("bad")

    assert not result.ok
    assert "Required skill not found: missing" in result.errors
