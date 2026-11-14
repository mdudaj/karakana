"""Planning prompt composition for Karakana."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from karakana.memory.ubongo import UbongoMemory
from karakana.models.router import route_model
from karakana.protocols.lifecycle import render_engineering_process
from karakana.skills.loader import SkillLoader
from karakana.skills.schemas import Skill


@dataclass(frozen=True)
class PlanningInputs:
    """Already captured values for rendering; construction grants no execution."""

    project: str
    task: str
    selected_skill: Skill
    project_memory: str
    project_contract: str
    template: str
    model_route: dict
    skillpack_context: str | None = None
    required_output: str | None = None


def compose_planning_prompt(
    project: str,
    skill: str,
    task: str,
    repo_root: Path,
    skillpack_context: str | None = None,
    allow_missing_memory: bool = False,
    model_route: dict | None = None,
) -> str:
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

    route = model_route or route_model("planning")
    return render_planning_prompt(PlanningInputs(
        project, task, selected_skill, project_memory, project_contract, template,
        route, skillpack_context,
    ))


def render_planning_prompt(inputs: PlanningInputs) -> str:
    """Render captured values without reading files, writing output or calling models."""
    values = {
        "task": inputs.task,
        "project": inputs.project,
        "selected_skill": _render_skill(inputs.selected_skill),
        "project_memory": inputs.project_memory,
        "project_contract": inputs.project_contract,
        "model_role_guidance": _render_model_role_guidance(inputs.model_route),
        "required_output": inputs.required_output if inputs.required_output is not None else _required_output(),
        "safety_rules": _safety_rules(),
    }
    prompt = inputs.template.format(**values).strip()
    if inputs.skillpack_context:
        prompt += "\n\n## Skillpack Context\n\n" + inputs.skillpack_context.strip()
    return prompt + "\n\n" + render_engineering_process()


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


def _render_model_role_guidance(route: dict) -> str:
    return f"""- Provider: {route.get("provider")}
- Model: {route.get("model")}
- Role: {route.get("role")}
- Token budget: {route.get("token_budget")}
- Token policy: {route.get("token_policy")}
- Escalation policy: {route.get("escalation_policy")}
- Rationale: {route.get("rationale")}"""


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

## Model Role Guidance

{model_role_guidance}

## Required Output

{required_output}

## Safety Rules

{safety_rules}
"""
