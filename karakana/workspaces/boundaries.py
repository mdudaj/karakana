"""Project boundary checks for workspace operations."""

from __future__ import annotations

from pathlib import Path

from karakana.workspaces.schemas import Workspace, WorkspaceProject


def find_project(workspace: Workspace, project_id: str) -> WorkspaceProject:
    for project in workspace.projects:
        if project.id == project_id:
            return project
    raise KeyError(f"Project not found in workspace: {project_id}")


def resolve_project_root(workspace: Workspace, project_id: str, repo_root: Path | None = None) -> Path:
    base = Path(workspace.defaults.root)
    if repo_root and not base.is_absolute():
        base = repo_root / base
    project = find_project(workspace, project_id)
    return (base / (project.path or ".")).resolve()


def ensure_project_path_allowed(workspace: Workspace, project_id: str, path: Path, repo_root: Path | None = None) -> list[str]:
    project_root = resolve_project_root(workspace, project_id, repo_root=repo_root)
    target = path.resolve()
    if not (target == project_root or target.is_relative_to(project_root)):
        return [f"Path is outside project boundary: {target} not under {project_root}"]
    return []


def validate_project_boundary(workspace: Workspace, project_id: str, target_path: Path, repo_root: Path | None = None) -> list[str]:
    warnings = ensure_project_path_allowed(workspace, project_id, target_path, repo_root=repo_root)
    project = find_project(workspace, project_id)
    if project.skillpack and project.skillpack != project_id and project_id in {"nhrdm", "billing", "lims", "msc-platform", "karakana"}:
        # Informational only: explicit workspace mapping is the source of truth.
        pass
    return warnings
