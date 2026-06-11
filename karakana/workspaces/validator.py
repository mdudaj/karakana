"""Validate workspace definitions."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from karakana.skillpacks.loader import SkillpackLoader
from karakana.workspaces.loader import WorkspaceLoader
from karakana.workspaces.schemas import WORKSPACE_STATUSES, Workspace


@dataclass
class WorkspaceValidationResult:
    name: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


class WorkspaceValidator:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.loader = WorkspaceLoader(repo_root)

    def validate(self, name: str) -> WorkspaceValidationResult:
        result = WorkspaceValidationResult(name)
        path = self.loader.root / f"{name}.yml"
        if not path.exists():
            alt = self.loader.root / f"{name}.yaml"
            path = alt if alt.exists() else path
        if not path.exists():
            result.errors.append(f"Workspace file does not exist: {name}")
            return result
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            result.errors.append(f"YAML parse error: {exc}")
            return result
        for field_name in ["name", "description", "version", "status", "projects"]:
            if field_name not in data:
                result.errors.append(f"Missing required field: {field_name}")
        if result.errors:
            return result
        if data["name"] != name:
            result.errors.append("Workspace name must match file name.")
        if data["status"] not in WORKSPACE_STATUSES:
            result.errors.append(f"Invalid workspace status: {data['status']}")
        try:
            workspace = self.loader.load(name)
        except Exception as exc:
            result.errors.append(str(exc))
            return result
        self._validate_projects(workspace, result)
        return result

    def validate_all(self) -> list[WorkspaceValidationResult]:
        return [self.validate(name) for name in self.loader.list_workspaces()]

    def _validate_projects(self, workspace: Workspace, result: WorkspaceValidationResult) -> None:
        seen = set()
        skillpacks = SkillpackLoader(self.repo_root)
        for project in workspace.projects:
            if not project.id:
                result.errors.append("Project id is required.")
            if project.id in seen:
                result.errors.append(f"Duplicate project id: {project.id}")
            seen.add(project.id)
            if project.path is not None and not isinstance(project.path, str):
                result.errors.append(f"Project path must be a string: {project.id}")
            if project.memory is not None and not isinstance(project.memory, str):
                result.errors.append(f"Project memory must be a string: {project.id}")
            if project.skillpack and not skillpacks.exists(project.skillpack):
                result.warnings.append(f"Project skillpack not found for {project.id}: {project.skillpack}")
            for group_name in ["status", "validate", "test"]:
                values = getattr(project.standard_commands, group_name)
                if not isinstance(values, list) or not all(isinstance(value, str) for value in values):
                    result.errors.append(f"Project {project.id} command group {group_name} must be a list of strings.")
            root = (self.repo_root / workspace.defaults.root).resolve()
            project_path = (root / (project.path or ".")).resolve()
            if not project_path.exists():
                message = f"Project path does not exist for {project.id}: {project.path}"
                if workspace.defaults.require_existing_paths:
                    result.errors.append(message)
                else:
                    result.warnings.append(message)
            if project.path and any(part in {"secrets", ".env"} for part in Path(project.path).parts):
                result.errors.append(f"Workspace references blocked path for {project.id}: {project.path}")
