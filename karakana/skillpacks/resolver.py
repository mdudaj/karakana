"""Resolve project skillpack context."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from karakana.skillpacks.activation import SkillpackActivation
from karakana.skillpacks.loader import SkillpackLoader
from karakana.skillpacks.schemas import ResolvedSkillpackContext, Skillpack


class SkillpackResolver:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.loader = SkillpackLoader(repo_root)

    def resolve_for_project(self, project: str | None = None) -> ResolvedSkillpackContext:
        if not project:
            current = self.resolve_current()
            if current:
                return current
            raise FileNotFoundError("No project or active skillpack provided.")
        skillpack = self.loader.load(project)
        return resolve_skillpack(skillpack)

    def resolve_current(self) -> ResolvedSkillpackContext | None:
        skillpack = SkillpackActivation(self.repo_root).current_skillpack()
        return resolve_skillpack(skillpack) if skillpack else None


def resolve_skillpack(skillpack: Skillpack) -> ResolvedSkillpackContext:
    return ResolvedSkillpackContext(
        skillpack=skillpack,
        required_skills=list(skillpack.skills.required),
        optional_skills=list(skillpack.skills.optional),
        memory_path=skillpack.project.memory,
        model_routes={task_type: asdict(route) for task_type, route in skillpack.model_routes.items()},
        protocols=({"default": skillpack.protocols.default} if skillpack.protocols.default else {}) | skillpack.protocols.categories,
        high_risk_paths=list(skillpack.safety.high_risk_paths),
        blocked_paths=list(skillpack.safety.blocked_paths),
        test_commands=list(skillpack.tests.commands) + list(skillpack.tests.recommended_before_commit),
        conventions=list(skillpack.conventions.notes),
    )


def route_from_skillpack(skillpack: Skillpack | None, task_type: str) -> dict | None:
    if not skillpack:
        return None
    route = skillpack.model_routes.get(task_type)
    if not route:
        return None
    return {"provider": route.provider, "model": route.model, "rationale": route.rationale, "route_source": "skillpack"}
