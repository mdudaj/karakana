"""Markdown rendering for action bundles and action artifacts."""

from __future__ import annotations

from karakana.actions.schemas import ActionBundle, ExtractedAction, StandardsSpecContext
from karakana.models.router import route_model


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
        "## Suggested Skills",
        "",
        *_list_lines(bundle.suggested_skills),
        "",
        "## Standards-vs-Spec Context",
        "",
        _standards_spec_markdown(bundle.standards_spec_context),
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
                f"- Suggested skills: {', '.join(action.suggested_skills)}",
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
    lines.extend(
        [
            "## Handoff",
            "",
            "See `handoff.md` in this action bundle.",
            "",
            "## Warnings",
            "",
            *_list_lines(bundle.warnings),
            "",
            "## Next Steps",
            "",
            *_list_lines(bundle.next_steps),
            "",
        ]
    )
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

## Suggested Skills

{_bullet_block(action.suggested_skills)}

## Standards-vs-Spec Context

{_standards_spec_markdown(action.standards_spec_context)}

## Recommended Model Route

{_recommended_route_markdown(action)}

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

## Suggested Skills

{_bullet_block(action.suggested_skills)}

## Standards-vs-Spec Context

{_standards_spec_markdown(action.standards_spec_context)}

## Recommended Model Route

{_recommended_route_markdown(action)}

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

## Suggested Skills

{_bullet_block(action.suggested_skills)}

## Recommended Model Route

{_recommended_route_markdown(action)}

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

## Suggested Skills

{_bullet_block(action.suggested_skills)}

## Recommended Model Route

{_recommended_route_markdown(action)}

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


def render_handoff(bundle: ActionBundle, artifact_paths: dict[str, str] | None = None) -> str:
    artifact_paths = artifact_paths or {}
    actions = [f"- {action.title} ({action.action_type}, {action.risk_level})" for action in bundle.actions]
    artifacts = [f"- {path}" for path in artifact_paths.values()]
    return f"""# Handoff

## Current Goal

Convert a reviewed model response into explicit, reviewable next-action artifacts.

## What Was Done

{bundle.summary}

## Current State

- Action run ID: {bundle.action_run_id}
- Status: {bundle.status}
- Source response: {bundle.source.path or ""}
- Response review status: {bundle.source.review_status or ""}

## Relevant Files and Artifacts

{chr(10).join(artifacts) if artifacts else "- None"}
- actions.json
- actions.md
- handoff.md

## Suggested Skills

{_bullet_block(bundle.suggested_skills)}

## Recommended Model Route

{_bundle_route_markdown(bundle)}

## Escalation Conditions

- Escalate routine coding from `gpt-5.4-mini` to `gpt-5.4` when tests fail, more than three files change, refactoring is needed, CI fails, or framework understanding is required.
- Escalate to `gpt-5.5` only for authentication, payments, migrations, process state, production deployment risk, high-risk review, or repeated failures.

## Suggested Next Actions

{chr(10).join(actions) if actions else "- Manually review the source response."}

## Risks and Constraints

{_risk_summary(bundle)}

## Commands to Run

- karakana action show {bundle.action_run_id}
- karakana action publish {bundle.action_run_id}

## Definition of Done

- A human reviews the action bundle.
- Any publishing uses explicit opt-in flags.
- No generated action is applied without review.
"""


def _risk_summary(bundle: ActionBundle) -> str:
    risks = sorted({action.risk_level for action in bundle.actions})
    warnings = bundle.warnings
    lines = [f"- Risk levels present: {', '.join(risks) if risks else 'none'}"]
    lines.extend(f"- Warning: {warning}" for warning in warnings)
    lines.append("- Do not execute Codex, deploy, or publish without explicit opt-in.")
    return "\n".join(lines)


def _recommended_route_markdown(action: ExtractedAction) -> str:
    route = _route_for_action(action)
    return "\n".join(
        [
            f"- Provider: {route['provider']}",
            f"- Model: {route['model']}",
            f"- Rationale: {route.get('rationale', '')}",
            "- Escalation triggers: tests fail, task grows past routine scope, security/auth/payment/migration/process-state risk appears, or work is stuck.",
        ]
    )


def _bundle_route_markdown(bundle: ActionBundle) -> str:
    if any(action.risk_level == "high" for action in bundle.actions):
        route = route_model("high_risk_code_review")
    elif any(action.action_type == "codex_task" for action in bundle.actions):
        route = route_model("routine_code_implementation")
    else:
        route = route_model("action_extraction_review")
    return "\n".join(
        [
            f"- Provider: {route['provider']}",
            f"- Model: {route['model']}",
            f"- Rationale: {route.get('rationale', '')}",
        ]
    )


def _route_for_action(action: ExtractedAction) -> dict:
    if action.risk_level == "high":
        return route_model("high_risk_code_review")
    if action.action_type == "codex_task":
        return route_model("routine_code_implementation")
    if action.action_type in {"documentation_update", "github_issue_draft"}:
        return route_model("documentation")
    return route_model("action_extraction_review")


def _standards_spec_markdown(context: StandardsSpecContext | None) -> str:
    if context is None:
        return "- None"
    lines = [
        f"- Standards summary: {context.standards_summary or ''}",
        f"- Spec summary: {context.spec_summary or ''}",
        "- Acceptance criteria:",
        *_indent(_list_lines(context.acceptance_criteria)),
        "- Standards risks:",
        *_indent(_list_lines(context.standards_risks)),
        "- Spec gaps:",
        *_indent(_list_lines(context.spec_gaps)),
    ]
    return "\n".join(lines)


def _bullet_block(values: list[str]) -> str:
    return "\n".join(_list_lines(values))


def _indent(lines: list[str]) -> list[str]:
    return [f"  {line}" for line in lines]


def _list_lines(values: list[str]) -> list[str]:
    if not values:
        return ["- None"]
    return [f"- {value}" for value in values]
