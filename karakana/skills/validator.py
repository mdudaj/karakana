"""Validate Karakana skill directories."""

from __future__ import annotations

from pathlib import Path

import yaml

from karakana.skills.loader import parse_skill_markdown
from karakana.skills.schemas import ValidationResult

REQUIRED_METADATA = [
    "name",
    "description",
    "version",
    "risk_level",
    "allowed_tools",
    "requires_approval_for",
]

ALLOWED_RISK_LEVELS = {"low", "medium", "high", "critical"}
ALLOWED_SCOPES = {"bundled", "optional", "project"}
ALLOWED_CATEGORIES = {"development", "research", "infrastructure", "documentation", "self-improvement", "domain"}

REQUIRED_SECTIONS = [
    "# ",
    "## Purpose",
    "## When to use this skill",
    "## When not to use this skill",
    "## Core concepts",
    "## Standard workflow",
    "## Safety rules",
    "## Required checks",
    "## Output format",
    "## Examples",
]

RECOMMENDED_SECTIONS = [
    "## Quick Reference",
    "## Pitfalls",
    "## Verification",
]


class SkillValidator:
    """Validate skill metadata and markdown structure."""

    def validate(self, path: Path) -> ValidationResult:
        skill_file = path / "SKILL.md" if path.is_dir() else path
        result = ValidationResult(path=skill_file)

        if not skill_file.exists():
            result.errors.append(f"Missing SKILL.md: {skill_file}")
            return result

        text = skill_file.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            result.errors.append("Missing YAML front matter")
            metadata, body = {}, text
        else:
            try:
                metadata, body = parse_skill_markdown(text)
            except yaml.YAMLError as exc:
                result.errors.append(f"Invalid YAML front matter: {exc}")
                metadata, body = {}, text

        for field in REQUIRED_METADATA:
            if field not in metadata:
                result.errors.append(f"Missing required metadata: {field}")

        name = metadata.get("name")
        if isinstance(name, str) and skill_file.parent.name != name:
            result.errors.append(f"Skill name '{name}' does not match directory '{skill_file.parent.name}'")

        description = metadata.get("description")
        if isinstance(description, str) and not description.strip():
            result.errors.append("description must not be empty")

        risk_level = metadata.get("risk_level")
        if risk_level and risk_level not in ALLOWED_RISK_LEVELS:
            result.errors.append(f"Invalid risk_level: {risk_level}")

        if "allowed_tools" in metadata and not isinstance(metadata["allowed_tools"], list):
            result.errors.append("allowed_tools must be a list")

        if "requires_approval_for" in metadata and not isinstance(metadata["requires_approval_for"], list):
            result.errors.append("requires_approval_for must be a list")

        scope = metadata.get("scope")
        if scope is not None and scope not in ALLOWED_SCOPES:
            result.errors.append(f"Invalid scope: {scope}")

        category = metadata.get("category")
        if category is not None and category not in ALLOWED_CATEGORIES:
            result.warnings.append(f"Unknown category: {category}")

        activation = metadata.get("activation")
        if activation is not None:
            self._validate_activation(activation, result)

        for section in REQUIRED_SECTIONS:
            if section not in body:
                result.warnings.append(f"Missing required section: {section}")

        for section in RECOMMENDED_SECTIONS:
            if section not in body:
                result.warnings.append(f"Missing recommended section: {section}")

        return result

    @staticmethod
    def _validate_activation(activation, result: ValidationResult) -> None:
        if not isinstance(activation, dict):
            result.errors.append("activation must be a mapping")
            return
        allowed_fields = {"keywords", "required_files", "optional_tools"}
        for key in activation:
            if key not in allowed_fields:
                result.warnings.append(f"Unknown activation field: {key}")
        for field in allowed_fields:
            if field in activation and not _is_string_list(activation[field]):
                result.errors.append(f"activation.{field} must be a list of strings")


def validate_skill(path: Path) -> ValidationResult:
    return SkillValidator().validate(path)


def _is_string_list(value) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)
