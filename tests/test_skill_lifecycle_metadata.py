from pathlib import Path

from karakana.skills.loader import SkillLoader
from karakana.skills.validator import SkillValidator
from tests.test_skill_optional_metadata import write_skill


def test_lifecycle_metadata_parses(tmp_path: Path):
    write_skill(
        tmp_path,
        """status: experimental
visibility: internal
bucket: productivity
""",
    )

    skill = SkillLoader(tmp_path / "skills").load_skill("demo-skill")

    assert skill.status == "experimental"
    assert skill.visibility == "internal"
    assert skill.bucket == "productivity"


def test_invalid_status_is_validation_error(tmp_path: Path):
    skill_root = write_skill(tmp_path, "status: retired\n")

    result = SkillValidator().validate(skill_root)

    assert "Invalid status: retired" in result.errors


def test_invalid_visibility_is_validation_error(tmp_path: Path):
    skill_root = write_skill(tmp_path, "visibility: secret\n")

    result = SkillValidator().validate(skill_root)

    assert "Invalid visibility: secret" in result.errors


def test_invalid_bucket_is_validation_error(tmp_path: Path):
    skill_root = write_skill(tmp_path, "bucket: operations\n")

    result = SkillValidator().validate(skill_root)

    assert "Invalid bucket: operations" in result.errors


def test_deprecated_skill_warns(tmp_path: Path):
    skill_root = write_skill(tmp_path, "status: deprecated\n")

    result = SkillValidator().validate(skill_root)

    assert "Skill is deprecated" in result.warnings
    assert result.is_valid
