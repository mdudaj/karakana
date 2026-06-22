"""Read-only workspace status collection."""

from __future__ import annotations

import subprocess
from pathlib import Path

from karakana.skillpacks.validator import SkillpackValidator
from karakana.workspaces.boundaries import resolve_project_root
from karakana.workspaces.schemas import ProjectStatus, Workspace, WorkspaceStatus


def collect_workspace_status(repo_root: Path, workspace: Workspace, project_id: str | None = None) -> WorkspaceStatus:
    statuses = []
    warnings: list[str] = []
    errors: list[str] = []
    for project in workspace.projects:
        if project_id and project.id != project_id:
            continue
        status = collect_project_status(repo_root, workspace, project.id)
        statuses.append(status)
        warnings.extend(status.warnings)
        errors.extend(status.errors)
    if project_id and not statuses:
        errors.append(f"Project not found: {project_id}")
    return WorkspaceStatus(workspace=workspace.name, status="warning" if warnings and not errors else ("error" if errors else "ok"), project_statuses=statuses, warnings=warnings, errors=errors)


def collect_project_status(repo_root: Path, workspace: Workspace, project_id: str) -> ProjectStatus:
    project = next(item for item in workspace.projects if item.id == project_id)
    path = resolve_project_root(workspace, project.id, repo_root=repo_root)
    warnings: list[str] = []
    errors: list[str] = []
    path_exists = path.exists()
    if not path_exists:
        warnings.append(f"Project path missing: {project.id} -> {path}")
    branch = _git(path, ["branch", "--show-current"]) if path_exists else None
    git_status = _git(path, ["status", "--short"]) if path_exists else None
    skillpack_valid = None
    if project.skillpack:
        validation = SkillpackValidator(repo_root).validate(project.skillpack)
        skillpack_valid = validation.ok
        warnings.extend([f"{project.id} skillpack warning: {warning}" for warning in validation.warnings])
        errors.extend([f"{project.id} skillpack error: {error}" for error in validation.errors])
    memory_path = project.memory
    memory_exists = (repo_root / memory_path).exists() if memory_path else None
    if memory_path and not memory_exists:
        warnings.append(f"Project memory path missing: {project.id} -> {memory_path}")
    return ProjectStatus(
        project_id=project.id,
        display_name=project.display_name,
        path=str(path),
        path_exists=path_exists,
        git_branch=branch,
        git_status=git_status,
        skillpack=project.skillpack,
        skillpack_valid=skillpack_valid,
        memory_path=memory_path,
        memory_exists=memory_exists,
        trace_count=_count_artifacts(repo_root / ".karakana" / "runs"),
        action_count=_count_artifacts(repo_root / ".karakana" / "actions"),
        requirement_count=_count_artifacts(repo_root / ".karakana" / "requirements"),
        patch_count=_count_artifacts(repo_root / ".karakana" / "patches"),
        warnings=warnings,
        errors=errors,
    )


def _git(path: Path, args: list[str]) -> str | None:
    result = subprocess.run(["git", *args], cwd=path, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def _count_artifacts(path: Path) -> int:
    if not path.exists():
        return 0
    return len([item for item in path.iterdir() if item.is_dir()])
