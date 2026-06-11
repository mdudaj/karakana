"""Workspace project handoff generation."""

from __future__ import annotations

import json
import secrets
from datetime import datetime, timezone
from pathlib import Path

from karakana.skillpacks.loader import SkillpackLoader
from karakana.workspaces.boundaries import find_project
from karakana.workspaces.schemas import Workspace, WorkspaceStatus


def write_workspace_handoff(repo_root: Path, workspace: Workspace, status: WorkspaceStatus, project_id: str) -> tuple[str, Path]:
    project = find_project(workspace, project_id)
    project_status = next(item for item in status.project_statuses if item.project_id == project_id)
    handoff_id = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + f"-workspace-handoff-{secrets.token_hex(3)}"
    out_dir = repo_root / ".karakana" / "workspace-handoffs" / handoff_id
    out_dir.mkdir(parents=True, exist_ok=True)
    data = {"handoff_id": handoff_id, "workspace": workspace.name, "project": project.id, "status": project_status.to_dict()}
    (out_dir / "handoff.json").write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    skills = _suggested_skills(repo_root, project.skillpack)
    (out_dir / "handoff.md").write_text(_render_handoff(workspace, project, project_status, skills), encoding="utf-8")
    return handoff_id, out_dir / "handoff.md"


def _render_handoff(workspace, project, status, skills: list[str]) -> str:
    return f"""# Workspace Project Handoff

## Project

- ID: {project.id}
- Display name: {project.display_name or ""}
- Path: {status.path}
- Path exists: {status.path_exists}

## Workspace

- Name: {workspace.name}
- Description: {workspace.description}

## Current State

- Git branch: {status.git_branch or ""}
- Git status: {status.git_status or ""}

## Skillpack

- Skillpack: {project.skillpack or ""}
- Valid: {status.skillpack_valid}

## Memory

- Path: {project.memory or ""}
- Exists: {status.memory_exists}

## Recent Artifacts

- Traces: {status.trace_count}
- Actions: {status.action_count}
- Requirements: {status.requirement_count}
- Patches: {status.patch_count}

## Suggested Skills

{_bullets(skills)}

## Recommended Next Actions

- Review project-specific status.
- Generate requirements or a plan before implementation.
- Keep project memory and skillpack boundaries separate.

## Risks and Constraints

- Do not mutate project files from workspace commands.
- Do not mix another project's memory or skillpack.
- Do not execute Codex, push, create PRs, or deploy.

## Commands to Run

{_bullets(project.standard_commands.validate)}

## Definition of Done

- Handoff reviewed by a human.
- Next action is project-specific and reviewable.
"""


def _bullets(values: list[str]) -> str:
    return "\n".join(f"- `{value}`" for value in values) if values else "- Needs review"


def _suggested_skills(repo_root: Path, skillpack: str | None) -> list[str]:
    if not skillpack:
        return ["karakana-handoff"]
    try:
        loaded = SkillpackLoader(repo_root).load(skillpack)
    except Exception:
        return [skillpack]
    return list(loaded.skills.required) or [skillpack]
