"""Planning prompt composition for Karakana."""

from __future__ import annotations

from pathlib import Path

from karakana.memory.ubongo import UbongoMemory
from karakana.skills.loader import SkillLoader


def compose_planning_prompt(project: str, skill: str, task: str, repo_root: Path, skillpack_context: str | None = None, allow_missing_memory: bool = False) -> str:
    """Compose a deterministic planning prompt from local repository context."""
    memory = UbongoMemory(repo_root)
    missing_memory = memory.validate_project(project)
    if missing_memory:
        if allow_missing_memory:
            project_memory = f"Project memory for '{project}' is incomplete or not initialized. Missing: {', '.join(missing_memory)}"
        else:
            missing = ", ".join(missing_memory)
            raise FileNotFoundError(f"Project '{project}' is missing required memory files: {missing}")
    else:
        project_memory = memory.summarize_project_context(project)

    skill_loader = SkillLoader(repo_root / "skills")
    selected_skill = skill_loader.load_skill(skill)
    project_contract = _read_optional(repo_root / "KARAKANA.md", "No KARAKANA.md found.")
    template = _read_optional(repo_root / "prompts" / "planner.prompt.md", _default_template())

    values = {
        "task": task,
        "project": project,
        "selected_skill": _render_skill(selected_skill),
        "project_memory": project_memory,
        "project_contract": project_contract,
        "required_output": _required_output(),
        "safety_rules": _safety_rules(),
    }
    prompt = template.format(**values).strip()
    if skillpack_context:
        prompt += "\n\n## Skillpack Context\n\n" + skillpack_context.strip()
    return prompt + "\n"


def write_planning_prompt(prompt: str, repo_root: Path, output_path: Path | None = None) -> Path:
    """Write a planning prompt to the runtime output directory."""
    path = output_path or repo_root / ".karakana" / "planning-task.md"
    if not path.is_absolute():
        path = repo_root / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(prompt, encoding="utf-8")
    return path


def _render_skill(skill) -> str:
    return f"""Name: {skill.name}
Description: {skill.description}
Version: {skill.version}
Risk level: {skill.risk_level}
Allowed tools: {", ".join(skill.allowed_tools)}
Requires approval for: {", ".join(skill.requires_approval_for)}

{skill.body.strip()}
"""


def _read_optional(path: Path, fallback: str) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return fallback


def _required_output() -> str:
    return """Return a structured implementation plan with:
- summary
- files to inspect
- implementation steps
- risks
- tests to run
- approval requirements"""


def _safety_rules() -> str:
    return """- Do not call external model APIs.
- Do not execute Codex.
- Do not deploy.
- Do not touch secrets.
- Prefer reviewable patches.
- Flag risky changes that require approval."""


def _default_template() -> str:
    return """# Karakana Planning Task

## Task

{task}

## Project

{project}

## Selected Skill

{selected_skill}

## Project Memory

{project_memory}

## Project Contract

{project_contract}

## Required Output

{required_output}

## Safety Rules

{safety_rules}
"""
