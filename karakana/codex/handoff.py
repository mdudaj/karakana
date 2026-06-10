"""Generate Codex handoff tasks from action bundles."""

from __future__ import annotations

import json
import secrets
from datetime import datetime, timezone
from pathlib import Path

from karakana.actions.schemas import ActionBundle, ExtractedAction
from karakana.actions.store import ActionStore
from karakana.codex.schemas import CodexHandoffTask
from karakana.models.router import route_model


class CodexHandoffBuilder:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.store = ActionStore(repo_root)

    def build_from_action_bundle(
        self,
        action_run_id: str,
        action_id: str | None = None,
        project: str | None = None,
        skill: str | None = None,
        output_dir: Path | None = None,
        skillpack_context=None,
    ) -> list[Path]:
        bundle = self.store.load(action_run_id)
        actions = _codex_candidate_actions(bundle, action_id)
        paths = []
        for action in actions:
            task = _task_from_action(bundle, action, project=project, skill=skill, skillpack_context=skillpack_context)
            paths.append(self.write_task(task, output_dir=output_dir))
        return paths

    def write_task(self, task: CodexHandoffTask, output_dir: Path | None = None) -> Path:
        task_dir = _safe_task_dir(self.repo_root, task.task_id, output_dir)
        task_dir.mkdir(parents=True, exist_ok=True)
        (task_dir / "context").mkdir(exist_ok=True)
        task_json = task_dir / "codex-task.json"
        task_md = task_dir / "codex-task.md"
        task_json.write_text(json.dumps(task.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        task_md.write_text(render_codex_handoff_task(task), encoding="utf-8")
        return task_md


def render_codex_handoff_task(task: CodexHandoffTask) -> str:
    return f"""# Karakana Codex Handoff Task

## Task

{task.title}

{task.description}

## Source Action

- Action run ID: {task.source_action_run_id or ""}
- Action ID: {task.source_action_id or ""}

## Project

{task.project or ""}

## Skill

{task.skill or ""}

## Suggested Skills

{_bullets(task.suggested_skills)}

## Recommended Codex Model

- Provider: {task.recommended_provider}
- Model: {task.recommended_model}
- Escalate to: {task.escalation_model or ""}
- Rationale: {task.rationale or ""}

## Escalation Conditions

- Escalate routine work from `gpt-5.4-mini` to `gpt-5.4` when tests fail, more than three files change, refactoring is needed, CI fails, or framework understanding is required.
- Escalate to `gpt-5.5` for authentication, payments, migrations, OpenSearch index changes, Viewflow process-state changes, production deployment risk, high-risk review, or repeated failures.

## Context

{task.context or ""}

## Relevant Files and Artifacts

{_bullets(task.metadata.get("artifacts", []))}

## Required Output

- Reviewable diff summary.
- Files changed.
- Commands run.
- Tests run and results.
- Risks and TODOs.

## Safety Rules

{_bullets(task.safety_rules)}

## Tests to Run

{_bullets(task.tests_to_run)}

## Approval Requirements

{_bullets(task.approval_requirements)}

## Definition of Done

- Patch is reviewed by a human.
- Relevant tests pass or failures are documented.
- No commits, pushes, PRs, deployments, or auto-merges occur automatically.
"""


def _task_from_action(bundle: ActionBundle, action: ExtractedAction, project: str | None, skill: str | None, skillpack_context=None) -> CodexHandoffTask:
    route = _route_for_action(action)
    escalation = "gpt-5.5" if action.risk_level == "high" else "gpt-5.4"
    suggested_skills = action.suggested_skills or bundle.suggested_skills
    safety_rules = [
        "Do not commit.",
        "Do not push.",
        "Do not create pull requests.",
        "Do not deploy.",
        "Do not touch secrets or .env files.",
        "Work through reviewable diffs.",
    ]
    tests_to_run = ["Run focused tests for changed behavior.", "Run `pytest` when Python behavior changes."]
    approval_requirements = ["Human review is required before applying or publishing this patch."]
    if skillpack_context:
        suggested_skills = sorted(set([*suggested_skills, *skillpack_context.required_skills, *skillpack_context.optional_skills]))
        tests_to_run = sorted(set([*tests_to_run, *skillpack_context.test_commands]))
        safety_rules.extend([f"Treat `{path}` as high-risk." for path in skillpack_context.high_risk_paths])
        safety_rules.extend([f"Do not modify blocked path `{path}`." for path in skillpack_context.blocked_paths])
        approval_requirements.extend(skillpack_context.skillpack.safety.requires_approval_for)
    return CodexHandoffTask(
        task_id=generate_codex_task_id(),
        source_action_run_id=bundle.action_run_id,
        source_action_id=action.action_id,
        title=action.title,
        description=action.description,
        project=project or action.project,
        skill=skill or action.skill,
        suggested_skills=suggested_skills,
        recommended_provider=route["provider"],
        recommended_model=route["model"],
        escalation_model=escalation,
        risk_level=action.risk_level,
        rationale=route.get("rationale"),
        context=_context_for_action(bundle, action, skillpack_context=skillpack_context),
        safety_rules=safety_rules,
        tests_to_run=tests_to_run,
        approval_requirements=approval_requirements,
        metadata={"artifacts": [action.metadata.get("artifact_path")] if action.metadata.get("artifact_path") else [], "skillpack": skillpack_context.skillpack.name if skillpack_context else None},
    )


def _route_for_action(action: ExtractedAction) -> dict:
    if action.risk_level in {"high", "critical"}:
        return route_model("high_risk_code_review")
    if action.action_type in {"codex_task", "implementation_checklist"}:
        return route_model("routine_code_implementation")
    return route_model("codex_task_drafting")


def _context_for_action(bundle: ActionBundle, action: ExtractedAction, skillpack_context=None) -> str:
    lines = [f"Bundle summary: {bundle.summary}", f"Action evidence: {', '.join(action.evidence)}"]
    if bundle.standards_spec_context:
        lines.append(f"Standards summary: {bundle.standards_spec_context.standards_summary or ''}")
        lines.append(f"Spec summary: {bundle.standards_spec_context.spec_summary or ''}")
    if skillpack_context:
        lines.append(f"Skillpack: {skillpack_context.skillpack.name}")
        lines.append("Skillpack conventions: " + "; ".join(skillpack_context.conventions))
    return "\n".join(lines)


def _codex_candidate_actions(bundle: ActionBundle, action_id: str | None) -> list[ExtractedAction]:
    actions = [action for action in bundle.actions if action.action_id == action_id] if action_id else list(bundle.actions)
    return [action for action in actions if action.action_type in {"codex_task", "implementation_checklist", "manual_review", "follow_up_plan", "handoff"}]


def _safe_task_dir(repo_root: Path, task_id: str, output_dir: Path | None) -> Path:
    if output_dir is None:
        return repo_root / ".karakana" / "codex" / task_id
    path = output_dir if output_dir.is_absolute() else repo_root / output_dir
    resolved = path.resolve()
    root = (repo_root / ".karakana").resolve()
    if not (resolved == root or resolved.is_relative_to(root)):
        raise ValueError("Codex handoff output must be under .karakana/.")
    return path / task_id if path.name != task_id else path


def generate_codex_task_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"{timestamp}-codex-{secrets.token_hex(3)}"


def _bullets(values: list[str]) -> str:
    cleaned = [value for value in values if value]
    if not cleaned:
        return "- None"
    return "\n".join(f"- {value}" for value in cleaned)
