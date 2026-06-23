"""Deterministic task classification for work protocols."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path

from karakana.protocols.loader import ProtocolLoader
from karakana.protocols.resolver import ProtocolResolver
from karakana.protocols.schemas import RISK_LEVELS, WORK_CATEGORIES
from karakana.skillpacks.loader import SkillpackLoader

HIGH_RISK_TERMS = {
    "auth",
    "authentication",
    "authorization",
    "permission",
    "payment",
    "billing",
    "migration",
    "schema",
    "database",
    "deploy",
    "production",
    "secret",
    "token",
    "safety",
    "policy",
    "workflow",
    "model route",
    "model routing",
}

CATEGORY_TERMS = {
    "requirements": {"requirement", "prd", "user story", "acceptance criteria", "definition of ready"},
    "research": {"research", "paper", "literature", "arxiv", "study"},
    "architecture": {"architecture", "adr", "decision record", "design decision"},
    "frontend": {"ui", "ux", "frontend", "screen", "page", "template", "css"},
    "migration": {"migration", "schema", "database", "data contract"},
    "safety": {"safety", "security", "secret", "approval", "policy"},
    "skill": {"skill", "skillpack"},
    "memory": {"ubongo", "memory"},
    "release": {"release", "version", "publish"},
    "model_routing": {"model route", "model routing", "provider", "gpt", "claude"},
    "github_ci": {"github", "ci", "workflow", "actions"},
    "implementation": {"code", "implement", "fix", "bug", "refactor", "python"},
    "test_eval": {"test", "eval", "regression", "coverage"},
    "documentation": {"docs", "documentation", "readme", "guide"},
}


@dataclass
class ProtocolClassification:
    task: str
    project: str | None
    skillpack: str | None
    protocol_id: str
    work_category: str
    risk_level: str
    behavior_change: bool = False
    ux_change: bool = False
    architecture_change: bool = False
    data_or_migration_change: bool = False
    safety_or_permission_change: bool = False
    required_artifacts: list[str] = field(default_factory=list)
    rationale: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


class ProtocolClassifier:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root

    def classify(
        self,
        task: str,
        *,
        project: str | None = None,
        skillpack: str | None = None,
        category: str | None = None,
        risk_level: str | None = None,
        protocol_id: str | None = None,
        behavior_change: bool | None = None,
        ux_change: bool | None = None,
        architecture_change: bool | None = None,
        data_or_migration_change: bool | None = None,
        safety_or_permission_change: bool | None = None,
    ) -> ProtocolClassification:
        normalized = task.lower()
        inferred_category, category_reason = _infer_category(normalized)
        selected_category = category or inferred_category
        if selected_category not in WORK_CATEGORIES:
            raise ValueError(f"Invalid work category: {selected_category}")

        inferred_risk, risk_reason = _infer_risk(normalized)
        selected_risk = risk_level or inferred_risk
        if selected_risk not in RISK_LEVELS:
            raise ValueError(f"Invalid risk level: {selected_risk}")

        flags = {
            "behavior_change": _flag(behavior_change, _contains_any(normalized, {"behavior", "feature", "workflow", "change", "fix", "implement"})),
            "ux_change": _flag(ux_change, selected_category == "frontend" or _contains_any(normalized, CATEGORY_TERMS["frontend"])),
            "architecture_change": _flag(architecture_change, selected_category == "architecture" or _contains_any(normalized, CATEGORY_TERMS["architecture"])),
            "data_or_migration_change": _flag(data_or_migration_change, selected_category == "migration" or _contains_any(normalized, CATEGORY_TERMS["migration"])),
            "safety_or_permission_change": _flag(safety_or_permission_change, selected_category == "safety" or _contains_any(normalized, {"auth", "authentication", "authorization", "permission", "safety", "security", "secret", "policy"})),
        }
        selected_protocol = protocol_id or self._protocol_for(skillpack or project, selected_category)
        artifacts = ProtocolResolver(self.repo_root).required_artifacts(selected_protocol, {"risk_level": selected_risk, **flags})
        return ProtocolClassification(
            task=task,
            project=project,
            skillpack=skillpack,
            protocol_id=selected_protocol,
            work_category=selected_category,
            risk_level=selected_risk,
            required_artifacts=[artifact.kind for artifact in artifacts],
            rationale=[category_reason, risk_reason, f"Protocol selected for category `{selected_category}`."],
            **flags,
        )

    def _protocol_for(self, skillpack_name: str | None, category: str) -> str:
        if skillpack_name:
            try:
                skillpack = SkillpackLoader(self.repo_root).load(skillpack_name)
                if category in skillpack.protocols.categories:
                    return skillpack.protocols.categories[category]
                if skillpack.protocols.default:
                    return skillpack.protocols.default
            except FileNotFoundError:
                pass
        loader = ProtocolLoader(self.repo_root)
        if loader.exists("python-code-change"):
            return "python-code-change"
        protocols = loader.list_protocols()
        if not protocols:
            raise FileNotFoundError("No work protocols found.")
        return protocols[0]


def _infer_category(normalized_task: str) -> tuple[str, str]:
    for category, terms in CATEGORY_TERMS.items():
        if _contains_any(normalized_task, terms):
            return category, f"Matched `{category}` keyword."
    return "implementation", "Defaulted to implementation because no category keyword matched."


def _infer_risk(normalized_task: str) -> tuple[str, str]:
    if _contains_any(normalized_task, HIGH_RISK_TERMS):
        return "high", "Matched high-risk keyword."
    if _contains_any(normalized_task, {"refactor", "shared", "governance", "protocol", "skillpack"}):
        return "medium", "Matched medium-risk keyword."
    return "low", "No elevated risk keyword matched."


def _contains_any(value: str, terms: set[str]) -> bool:
    return any(term in value for term in terms)


def _flag(explicit: bool | None, inferred: bool) -> bool:
    return inferred if explicit is None else explicit
