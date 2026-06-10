"""Load skillpack YAML files."""

from __future__ import annotations

from pathlib import Path

import yaml

from karakana.skillpacks.schemas import (
    Skillpack,
    SkillpackConventions,
    SkillpackModelRoute,
    SkillpackProject,
    SkillpackSafety,
    SkillpackSkills,
    SkillpackTests,
)


class SkillpackLoader:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.skillpacks_root = repo_root / "skillpacks"

    def discover_paths(self) -> list[Path]:
        if not self.skillpacks_root.exists():
            return []
        return sorted([*self.skillpacks_root.glob("*.yml"), *self.skillpacks_root.glob("*.yaml")])

    def list_skillpacks(self) -> list[str]:
        return [path.stem for path in self.discover_paths()]

    def exists(self, name: str) -> bool:
        return self._path_for(name).exists()

    def load(self, name: str) -> Skillpack:
        path = self._path_for(name)
        if not path.exists():
            raise FileNotFoundError(f"Skillpack not found: {name}")
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        return skillpack_from_dict(data, path)

    def _path_for(self, name: str) -> Path:
        yml = self.skillpacks_root / f"{name}.yml"
        if yml.exists():
            return yml
        return self.skillpacks_root / f"{name}.yaml"


def skillpack_from_dict(data: dict, path: Path | None = None) -> Skillpack:
    project = data.get("project") or {}
    skills = data.get("skills") or {}
    safety = data.get("safety") or {}
    tests = data.get("tests") or {}
    conventions = data.get("conventions") or {}
    routes = {
        str(task_type): SkillpackModelRoute(
            provider=str(route.get("provider", "")),
            model=str(route.get("model", "")),
            rationale=route.get("rationale"),
        )
        for task_type, route in (data.get("model_routes") or {}).items()
        if isinstance(route, dict)
    }
    return Skillpack(
        name=str(data.get("name", path.stem if path else "")),
        description=str(data.get("description", "")),
        version=str(data.get("version", "")),
        status=str(data.get("status", "")),
        project=SkillpackProject(
            id=str(project.get("id", "")),
            display_name=project.get("display_name"),
            memory=project.get("memory"),
            contract=project.get("contract"),
        ),
        skills=SkillpackSkills(required=list(skills.get("required") or []), optional=list(skills.get("optional") or [])),
        model_routes=routes,
        safety=SkillpackSafety(
            high_risk_paths=list(safety.get("high_risk_paths") or []),
            blocked_paths=list(safety.get("blocked_paths") or []),
            requires_approval_for=list(safety.get("requires_approval_for") or []),
        ),
        tests=SkillpackTests(commands=list(tests.get("commands") or []), recommended_before_commit=list(tests.get("recommended_before_commit") or [])),
        conventions=SkillpackConventions(notes=list(conventions.get("notes") or [])),
        path=str(path) if path else None,
        metadata={key: value for key, value in data.items() if key not in {"name", "description", "version", "status", "project", "skills", "model_routes", "safety", "tests", "conventions"}},
    )
