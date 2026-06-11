"""Load workspace YAML definitions."""

from __future__ import annotations

from pathlib import Path

import yaml

from karakana.workspaces.schemas import Workspace, WorkspaceCommandSet, WorkspaceDefaults, WorkspaceProject


class WorkspaceLoader:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.root = repo_root / "workspaces"

    def discover_paths(self) -> list[Path]:
        if not self.root.exists():
            return []
        return sorted([*self.root.glob("*.yml"), *self.root.glob("*.yaml")])

    def list_workspaces(self) -> list[str]:
        return [path.stem for path in self.discover_paths()]

    def exists(self, name: str) -> bool:
        return self._path(name).exists()

    def load(self, name: str) -> Workspace:
        path = self._path(name)
        if not path.exists():
            raise FileNotFoundError(f"Workspace not found: {name}")
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        defaults = WorkspaceDefaults(**(data.get("defaults") or {}))
        projects = []
        for item in data.get("projects") or []:
            commands = WorkspaceCommandSet(**(item.get("standard_commands") or {}))
            payload = dict(item)
            payload["standard_commands"] = commands
            projects.append(WorkspaceProject(**payload))
        return Workspace(
            name=data["name"],
            description=data["description"],
            version=data["version"],
            status=data["status"],
            defaults=defaults,
            projects=projects,
            path=str(path),
            metadata={key: value for key, value in data.items() if key not in {"name", "description", "version", "status", "defaults", "projects"}},
        )

    def _path(self, name: str) -> Path:
        yml = self.root / f"{name}.yml"
        return yml if yml.exists() else self.root / f"{name}.yaml"
