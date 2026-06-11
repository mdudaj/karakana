"""Markdown summaries for workspaces."""

from __future__ import annotations

from karakana.workspaces.schemas import Workspace, WorkspaceStatus


def render_workspace_summary(workspace: Workspace, status: WorkspaceStatus | None = None) -> str:
    status_by_project = {item.project_id: item for item in status.project_statuses} if status else {}
    body = [
        "# Karakana Workspace Summary",
        "",
        "## Workspace",
        "",
        f"- Name: {workspace.name}",
        f"- Description: {workspace.description}",
        f"- Status: {workspace.status}",
        "",
        "## Projects",
        "",
    ]
    for project in workspace.projects:
        project_status = status_by_project.get(project.id)
        body.extend(
            [
                f"### {project.id}",
                "",
                f"- Display name: {project.display_name or ''}",
                f"- Path: {project_status.path if project_status else project.path}",
                f"- Path exists: {project_status.path_exists if project_status else 'not checked'}",
                f"- Skillpack: {project.skillpack or ''}",
                f"- Memory: {project.memory or ''}",
                f"- Git branch: {project_status.git_branch if project_status else ''}",
                f"- Git status: {project_status.git_status if project_status else ''}",
                "",
            ]
        )
    warnings = status.warnings if status else []
    body.extend(["## Warnings", "", _bullets(warnings), "", "## Recommended Next Actions", "", "- Validate workspace before planning.", "- Run project-specific status before handoff.", "- Keep project memory and skillpacks separated."])
    return "\n".join(body) + "\n"


def render_status(status: WorkspaceStatus) -> str:
    return render_workspace_summary(Workspace(name=status.workspace, description="", version="", status=status.status), status)


def _bullets(values: list[str]) -> str:
    return "\n".join(f"- {value}" for value in values) if values else "- None"
