"""Schemas for Karakana project skillpacks."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

ALLOWED_SKILLPACK_STATUSES = {"stable", "experimental", "in-progress", "deprecated"}


@dataclass
class SkillpackProject:
    id: str
    display_name: str | None = None
    memory: str | None = None
    contract: str | None = None


@dataclass
class SkillpackSkills:
    required: list[str] = field(default_factory=list)
    optional: list[str] = field(default_factory=list)


@dataclass
class SkillpackModelRoute:
    provider: str
    model: str
    rationale: str | None = None


@dataclass
class SkillpackSafety:
    high_risk_paths: list[str] = field(default_factory=list)
    blocked_paths: list[str] = field(default_factory=list)
    requires_approval_for: list[str] = field(default_factory=list)


@dataclass
class SkillpackTests:
    commands: list[str] = field(default_factory=list)
    recommended_before_commit: list[str] = field(default_factory=list)


@dataclass
class SkillpackConventions:
    notes: list[str] = field(default_factory=list)


@dataclass
class Skillpack:
    name: str
    description: str
    version: str
    status: str
    project: SkillpackProject
    skills: SkillpackSkills
    model_routes: dict[str, SkillpackModelRoute] = field(default_factory=dict)
    safety: SkillpackSafety = field(default_factory=SkillpackSafety)
    tests: SkillpackTests = field(default_factory=SkillpackTests)
    conventions: SkillpackConventions = field(default_factory=SkillpackConventions)
    path: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.status not in ALLOWED_SKILLPACK_STATUSES:
            raise ValueError(f"Invalid skillpack status: {self.status}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class SkillpackValidationResult:
    name: str
    path: str | None = None
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


@dataclass
class ResolvedSkillpackContext:
    skillpack: Skillpack
    required_skills: list[str]
    optional_skills: list[str]
    memory_path: str | None
    model_routes: dict[str, dict]
    high_risk_paths: list[str]
    blocked_paths: list[str]
    test_commands: list[str]
    conventions: list[str]
