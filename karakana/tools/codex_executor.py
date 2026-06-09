"""Generate Codex-ready Karakana task prompts without executing Codex."""

from __future__ import annotations

from pathlib import Path

from karakana.memory.ubongo import UbongoMemory
from karakana.skills.loader import SkillLoader
from karakana.tools.code_search import collect_repository_context


class CodexExecutor:
    """Build and write Codex task prompts from local repository context."""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root

    def build_task_prompt(self, project: str, skill: str, task: str, focus: str | None = None) -> str:
        memory = UbongoMemory(self.repo_root)
        missing_memory = memory.validate_project(project)
        if missing_memory:
            missing = ", ".join(missing_memory)
            raise FileNotFoundError(f"Project '{project}' is missing required memory files: {missing}")

        selected_skill = SkillLoader(self.repo_root / "skills").load_skill(skill)
        template = _read_optional(self.repo_root / "prompts" / "codex_task.prompt.md", _default_template())
        values = {
            "task": _render_task(task, focus),
            "project": project,
            "selected_skill": _render_skill(selected_skill),
            "memory": memory.summarize_project_context(project),
            "project_contract": _read_optional(self.repo_root / "KARAKANA.md", "No KARAKANA.md found."),
            "repository_instructions": _read_optional(self.repo_root / "AGENTS.md", "No AGENTS.md found."),
            "repository_context": collect_repository_context(self.repo_root),
            "files_likely_relevant": _files_likely_relevant(project, skill),
            "safety_rules": _safety_rules(),
            "required_output": _required_output(),
            "tests_to_run": _tests_to_run(),
            "approval_requirements": _approval_requirements(selected_skill.requires_approval_for),
            "constraints": _constraints(),
        }
        return template.format(**values).strip() + "\n"

    def write_task_prompt(self, prompt: str, output_path: Path | None = None) -> Path:
        path = output_path or self.repo_root / ".karakana" / "codex-task.md"
        if not path.is_absolute():
            path = self.repo_root / path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(prompt, encoding="utf-8")
        return path


def _render_task(task: str, focus: str | None) -> str:
    if focus:
        return f"{task}\n\nFocus: {focus}"
    return task


def _render_skill(skill) -> str:
    return f"""Name: {skill.name}
Description: {skill.description}
Version: {skill.version}
Risk level: {skill.risk_level}
Allowed tools: {", ".join(skill.allowed_tools)}
Requires approval for: {", ".join(skill.requires_approval_for)}

{skill.body.strip()}
"""


def _files_likely_relevant(project: str, skill: str) -> str:
    return f"""- `KARAKANA.md`
- `AGENTS.md`
- `ubongo/projects/{project}/`
- `skills/{skill}/SKILL.md`
- Files named by the task after repository inspection."""


def _safety_rules() -> str:
    return """- Do not push directly to main or protected branches.
- Do not modify secrets.
- Do not edit `.env` files unless explicitly requested and approved.
- Do not run destructive commands.
- Do not deploy.
- Work through reviewable diffs.
- Run tests where possible.
- Report commands run.
- Report files changed.
- Report risks and TODOs."""


def _required_output() -> str:
    return """Return:
- summary of changes
- files changed
- commands run
- tests run and results
- risks
- TODOs or follow-up work
- approval requirements"""


def _tests_to_run() -> str:
    return """- Run focused tests for changed behavior.
- Run `python -m pytest` when Python behavior changes.
- Explain any tests that could not be run."""


def _approval_requirements(requirements: list[str]) -> str:
    if not requirements:
        return "No skill-specific approval requirements listed. Apply repository safety rules."
    return "\n".join(f"- {requirement}" for requirement in requirements)


def _constraints() -> str:
    return """- Do not require Codex CLI for prompt generation.
- Do not call external model APIs.
- Do not automatically execute Codex.
- Do not implement GitHub Actions.
- Do not implement reflection.
- Do not mutate code unless this prompt is later handed to a coding executor."""


def _read_optional(path: Path, fallback: str) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return fallback


def _default_template() -> str:
    return """# Karakana Codex Task

## Task

{task}

## Project

{project}

## Selected Skill

{selected_skill}

## Relevant Ubongo Memory

{memory}

## Project Contract

{project_contract}

## Repository Instructions

{repository_instructions}

## Repository Context

{repository_context}

## Files Likely Relevant

{files_likely_relevant}

## Safety Rules

{safety_rules}

## Required Output

{required_output}

## Tests to Run

{tests_to_run}

## Approval Requirements

{approval_requirements}

## Constraints

{constraints}
"""
