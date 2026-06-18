"""Workspace-aware planning prompt generation."""

from __future__ import annotations

from pathlib import Path

from karakana.agents.planner import compose_planning_prompt, write_planning_prompt
from karakana.skillpacks.loader import SkillpackLoader
from karakana.workspaces.boundaries import find_project, resolve_project_root
from karakana.workspaces.schemas import Workspace


def build_workspace_plan(repo_root: Path, workspace: Workspace, project_id: str, task: str, output: Path | None = None, handoff_context: str | None = None) -> Path:
    project = find_project(workspace, project_id)
    project_root = resolve_project_root(workspace, project_id, repo_root=repo_root)
    skill = _primary_skill(repo_root, project.skillpack)
    prompt = compose_planning_prompt(
        project=project.id,
        skill=skill,
        task=task,
        repo_root=repo_root,
        skillpack_context=_workspace_context(workspace, project_id, project_root) + ("\n\n" + handoff_context if handoff_context else ""),
        allow_missing_memory=True,
    )
    path = output or (repo_root / ".karakana" / "workspace-plans" / f"{workspace.name}-{project_id}-plan.md")
    return write_planning_prompt(prompt, repo_root=repo_root, output_path=path)


def _workspace_context(workspace: Workspace, project_id: str, project_root: Path) -> str:
    project = find_project(workspace, project_id)
    return f"""# Workspace Context

Workspace: {workspace.name}
Project: {project.id}
Project path: {project_root}
Skillpack: {project.skillpack or "None"}
Memory: {project.memory or "None"}

## Boundary Rules

- Operate only on this project's configured path.
- Use only this project's configured memory path.
- Do not apply patches, ingest all projects, execute Codex, push, deploy, or create PRs from workspace planning.
"""


def _primary_skill(repo_root: Path, skillpack: str | None) -> str:
    if not skillpack:
        return "karakana-self-improvement"
    try:
        loaded = SkillpackLoader(repo_root).load(skillpack)
    except Exception:
        return "karakana-self-improvement"
    return loaded.skills.required[0] if loaded.skills.required else "karakana-self-improvement"
