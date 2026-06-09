"""Markdown rendering for action bundles and action artifacts."""

from __future__ import annotations

from karakana.actions.schemas import ActionBundle, ExtractedAction


def render_action_bundle(bundle: ActionBundle, artifact_paths: dict[str, str] | None = None) -> str:
    artifact_paths = artifact_paths or {}
    lines = [
        "# Karakana Action Bundle",
        "",
        "## Summary",
        "",
        f"- Action run ID: {bundle.action_run_id}",
        f"- Status: {bundle.status}",
        f"- Source: {bundle.source.path or ''}",
        f"- Review status: {bundle.source.review_status or ''}",
        f"- Created: {bundle.created_at}",
        "",
        bundle.summary,
        "",
        "## Actions",
        "",
    ]
    if not bundle.actions:
        lines.append("- None")
    for action in bundle.actions:
        lines.extend(
            [
                f"### {action.action_id}: {action.title}",
                "",
                f"- Type: {action.action_type}",
                f"- Risk: {action.risk_level}",
                f"- Project: {action.project or ''}",
                f"- Skill: {action.skill or ''}",
                f"- Requires human review: {action.requires_human_review}",
                f"- Requires explicit opt-in: {action.requires_explicit_opt_in}",
                "",
                "#### Description",
                "",
                action.description,
                "",
                "#### Suggested Command",
                "",
                action.suggested_command or "",
                "",
                "#### Artifact",
                "",
                artifact_paths.get(action.action_id, ""),
                "",
            ]
        )
    lines.extend(["## Warnings", "", *_list_lines(bundle.warnings), "", "## Next Steps", "", *_list_lines(bundle.next_steps), ""])
    return "\n".join(lines)


def render_action_artifact(action: ExtractedAction, source_path: str | None = None) -> str:
    if action.action_type == "codex_task":
        return _codex_task(action, source_path)
    if action.action_type == "github_issue_draft":
        return _issue_draft(action, source_path)
    if action.action_type in {"improvement_proposal", "memory_update", "skill_update", "prompt_update", "eval_case", "documentation_update"}:
        return _improvement_action(action)
    return _checklist(action)


def _codex_task(action: ExtractedAction, source_path: str | None) -> str:
    return f"""# Karakana Codex Task

## Source

{source_path or ""}

## Task

{action.description}

## Project

{action.project or ""}

## Skill

{action.skill or ""}

## Context

Evidence: {", ".join(action.evidence)}

## Required Output

Return a reviewable diff summary, files changed, tests run, risks, and TODOs.

## Safety Rules

- Do not push directly to main.
- Do not touch secrets.
- Do not deploy.
- Work through reviewable diffs.

## Tests to Run

- Run focused tests for changed behavior.

## Approval Requirements

Human review is required before applying output.
"""


def _issue_draft(action: ExtractedAction, source_path: str | None) -> str:
    return f"""# GitHub Issue Draft

## Title

{action.title}

## Summary

{action.description}

## Context

Source: {source_path or ""}

## Proposed Work

{action.proposed_content or action.description}

## Acceptance Criteria

- Action is reviewed by a human.
- Required tests or evals are identified.

## Risks

{action.risk_level}

## Labels

karakana, needs-review
"""


def _improvement_action(action: ExtractedAction) -> str:
    return f"""# Karakana Improvement Action

## Type

{action.action_type}

## Target

{action.target_path or ""}

## Rationale

{action.description}

## Proposed Content

{action.proposed_content or ""}

## Evidence

{chr(10).join(f"- {item}" for item in action.evidence) if action.evidence else "- None"}

## Risk

{action.risk_level}

## Requires Human Review

{action.requires_human_review}
"""


def _checklist(action: ExtractedAction) -> str:
    return f"""# Karakana Action Checklist

## Goal

{action.title}

## Steps

- {action.description}

## Tests

- Identify and run relevant tests.

## Risks

{action.risk_level}

## Done When

- Action is reviewed.
- Any follow-up implementation is tracked separately.
"""


def _list_lines(values: list[str]) -> list[str]:
    if not values:
        return ["- None"]
    return [f"- {value}" for value in values]
