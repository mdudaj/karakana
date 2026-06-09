"""Structured types for Karakana skills."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class SkillActivation:
    keywords: list[str] = field(default_factory=list)
    required_files: list[str] = field(default_factory=list)
    optional_tools: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Skill:
    name: str
    description: str
    version: str
    risk_level: str
    allowed_tools: list[str]
    requires_approval_for: list[str]
    body: str
    path: Path
    metadata: dict
    activation: SkillActivation | None = None
    category: str | None = None
    scope: str | None = None


@dataclass
class ValidationResult:
    path: Path
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not self.errors
