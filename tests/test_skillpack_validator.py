from pathlib import Path

from karakana.skillpacks.validator import SkillpackValidator


def test_validate_starter_skillpack():
    result = SkillpackValidator(Path.cwd()).validate("karakana")

    assert result.ok


def test_validate_all_starter_skillpacks():
    results = SkillpackValidator(Path.cwd()).validate_all()

    assert all(result.ok for result in results)
    assert all(not result.warnings for result in results)


def test_missing_project_memory_still_warns(tmp_path):
    root = tmp_path / "skillpacks"
    root.mkdir()
    (root / "example.yml").write_text(
        "name: example\ndescription: Example\nversion: 0.1.0\nstatus: stable\n"
        "project:\n  id: example\n  memory: ubongo/projects/example\n"
        "skills:\n  required: []\n",
        encoding="utf-8",
    )

    result = SkillpackValidator(tmp_path).validate("example")

    assert result.ok
    assert result.warnings == ["Project memory path does not exist: ubongo/projects/example"]


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
