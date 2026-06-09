"""Load Karakana skills from markdown files."""

from __future__ import annotations

from pathlib import Path

import yaml

from karakana.skills.schemas import Skill, SkillActivation


class SkillLoader:
    """Discover and load markdown skills from a skills root."""

    def __init__(self, skills_root: Path):
        self.skills_root = skills_root

    def list_skills(self) -> list[str]:
        if not self.skills_root.exists():
            return []
        return sorted(
            path.name
            for path in self.skills_root.iterdir()
            if path.is_dir() and (path / "SKILL.md").exists()
        )

    def skill_exists(self, name: str) -> bool:
        return (self.skills_root / name / "SKILL.md").exists()

    def load_skill(self, name: str) -> Skill:
        skill_path = self.skills_root / name / "SKILL.md"
        if not skill_path.exists():
            raise FileNotFoundError(f"Skill not found: {skill_path}")

        metadata, body = parse_skill_markdown(skill_path.read_text(encoding="utf-8"))
        activation = _parse_activation(metadata.get("activation"))
        return Skill(
            name=str(metadata.get("name", name)),
            description=str(metadata.get("description", "")),
            version=str(metadata.get("version", "")),
            risk_level=str(metadata.get("risk_level", "")),
            allowed_tools=list(metadata.get("allowed_tools") or []),
            requires_approval_for=list(metadata.get("requires_approval_for") or []),
            body=body,
            path=skill_path,
            metadata=metadata,
            activation=activation,
            category=metadata.get("category"),
            scope=metadata.get("scope"),
            status=metadata.get("status"),
            visibility=metadata.get("visibility"),
            bucket=metadata.get("bucket"),
        )


def parse_skill_markdown(text: str) -> tuple[dict, str]:
    """Parse YAML front matter and markdown body from a skill file."""
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    metadata = yaml.safe_load(parts[1]) or {}
    return metadata, parts[2].lstrip()


def _parse_activation(value) -> SkillActivation | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        return None
    return SkillActivation(
        keywords=list(value.get("keywords") or []),
        required_files=list(value.get("required_files") or []),
        optional_tools=list(value.get("optional_tools") or []),
    )
