"""Schemas for Karakana OKF concepts."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ALLOWED_CONCEPT_TYPES = {
    "Project",
    "Skill",
    "Skillpack",
    "ADR",
    "Requirement",
    "UserStory",
    "Milestone",
    "ImplementationInstruction",
    "Handoff",
    "Schema",
    "CodeComponent",
    "Workflow",
    "SafetyRule",
    "ModelRoute",
    "Eval",
    "Verification",
    "DesignSystemRule",
    "ResearchEvidenceContract",
    "Lesson",
    "ImprovementProposal",
    "RuntimeEvidence",
    "WorkProtocol",
}

ALLOWED_STATUSES = {"draft", "active", "deprecated", "superseded", "runtime-evidence", "proposed"}

REQUIRED_FIELDS = ["id", "type", "title", "status", "owner", "project", "summary", "source", "tags", "updated"]

BLOCKED_SOURCE_PATTERNS = (".env", ".env.", "secrets/")


@dataclass(frozen=True)
class OkfConcept:
    path: Path
    metadata: dict[str, Any]
    body: str

    @property
    def concept_id(self) -> str:
        return str(self.metadata.get("id", ""))

    @property
    def concept_type(self) -> str:
        return str(self.metadata.get("type", ""))

    @property
    def project(self) -> str:
        return str(self.metadata.get("project", ""))

    @property
    def status(self) -> str:
        return str(self.metadata.get("status", ""))

    @property
    def tags(self) -> set[str]:
        raw = self.metadata.get("tags") or []
        return {str(tag) for tag in raw if isinstance(tag, str)}

    @property
    def relationships(self) -> dict[str, list[str]]:
        raw = self.metadata.get("relationships") or {}
        if not isinstance(raw, dict):
            return {}
        relationships: dict[str, list[str]] = {}
        for key, value in raw.items():
            if isinstance(value, list):
                relationships[str(key)] = [str(item) for item in value if isinstance(item, str)]
        return relationships


@dataclass
class OkfIssue:
    path: Path
    message: str


@dataclass
class OkfValidationResult:
    path: Path
    concepts: list[OkfConcept] = field(default_factory=list)
    errors: list[OkfIssue] = field(default_factory=list)
    warnings: list[OkfIssue] = field(default_factory=list)
    counts_by_type: dict[str, int] = field(default_factory=dict)
    counts_by_project: dict[str, int] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return not self.errors
