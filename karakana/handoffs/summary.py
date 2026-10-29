"""Markdown rendering for Karakana handoffs."""

from __future__ import annotations

from datetime import datetime, timezone

from karakana.handoffs.schemas import HandoffArtifact
from karakana.handoffs.continuation import render_continuation
from karakana.handoffs.quick_reference import render_quick_reference, quick_reference_warnings


def render_handoff(handoff: HandoffArtifact) -> str:
    source = handoff.source_artifacts[0] if handoff.source_artifacts else "Recovered local state"
    return f"""# Karakana Handoff

## Run Metadata

- Handoff ID: {handoff.handoff_id}
- Created at: {handoff.created_at}
- Updated at: {handoff.updated_at}
- Workspace: {handoff.workspace or "None"}
- Project: {handoff.project}
- Skillpack: {handoff.skillpack}
- Current milestone: {handoff.current_milestone}
- Purpose: {handoff.purpose}
- Source run/artifact: {source}
- Recovered: {handoff.recovered}

{render_quick_reference(handoff)}

{_attention(handoff)}

## Next Task Brief

{handoff.next_task_brief or "No next-task brief recorded for this handoff."}

## Current State Summary

{handoff.state_summary or "No state summary was available."}

## Current Milestone

{handoff.current_milestone}

## Decisions Already Made

{_bullets(handoff.decisions)}

## Open Findings

{_bullets(handoff.open_findings)}

## Files to Inspect First

{_bullets(handoff.inspect_first)}

## Files Not to Reread

{_bullets(handoff.do_not_reread)}

## Artifacts to Reference, Not Duplicate

{_bullets(handoff.reference_artifacts)}

## OKF Concepts Loaded

{_bullets(handoff.okf_concepts_loaded)}

## OKF Concepts Changed

{_bullets(handoff.okf_concepts_changed)}

## Suggested Skills

{_bullets(handoff.suggested_skills)}

## Exact Next Action

{handoff.exact_next_action or "Verify current state and select one bounded next action."}

## Safety Constraints

{_bullets(handoff.safety_constraints)}

## Continuation Guidance

{render_continuation(handoff.continuation)}

## Return Handoff Expectations

{_return_expectation(handoff)}

## Staleness / Validity Notes

{_bullets(handoff.staleness_notes)}

## Warnings

{_bullets(handoff.warnings)}

## Notes for Fresh Agent

{_bullets(handoff.notes_for_fresh_agent)}
"""


def render_session_start(handoff: HandoffArtifact, path: str, *, details: bool = False) -> str:
    advisory = f"""## Do Not Reread Unless Needed

{_bullets(handoff.do_not_reread)}

## Suggested Skills

{_bullets(handoff.suggested_skills)}

""" if details else ""
    concepts = f"""## OKF Concepts

Loaded:
{_bullets(handoff.okf_concepts_loaded)}

Changed:
{_bullets(handoff.okf_concepts_changed)}

""" if details or handoff.okf_concepts_loaded or handoff.okf_concepts_changed else ""
    return f"""# Karakana Session Start

- Handoff: {path}
- Project: {handoff.project}
- Current milestone: {handoff.current_milestone}
- Purpose: {handoff.purpose}
- Recovered: {handoff.recovered}

{render_quick_reference(handoff)}

{_attention(handoff)}

## Next Task Brief

{handoff.next_task_brief or "No next-task brief recorded for this handoff."}

{concepts}## Inspect First

{_bullets(handoff.inspect_first)}

{advisory}## Safety

{_bullets(handoff.safety_constraints)}

## Continuation Guidance

{render_continuation(handoff.continuation, details=details)}

Use `handoff load --project {handoff.project} --details` for advisory references and full continuation guidance.
"""


def _attention(handoff: HandoffArtifact) -> str:
    # A successful protocol receipt is informational, not an attention item.
    # It remains available in the full saved handoff's Warnings/history section.
    actionable = [warning for warning in handoff.warnings if not (
        warning.startswith("Protocol check ") and warning.endswith(" is passed."))]
    values = [*handoff.open_findings, *actionable, *quick_reference_warnings(handoff)]
    if handoff.recovered:
        values.append("Recovered state: verify the current source and authority before acting.")
    try:
        age = (datetime.now(timezone.utc) - datetime.fromisoformat(handoff.updated_at)).total_seconds() / 86400
        if age > 7:
            values.append("Handoff is older than 7 days; recheck current source and backlog before acting.")
    except (ValueError, TypeError):
        values.append("Handoff timestamp is invalid; verify snapshot freshness.")
    return "## Attention\n\n" + _bullets(list(dict.fromkeys(values))) if values else ""


def _return_expectation(handoff: HandoffArtifact) -> str:
    if not handoff.return_handoff_expected:
        return "No return handoff was requested."
    return (
        "Before ending, create a new handoff that records completed work, "
        "verification, remaining findings, changed references, remaining "
        "tasks, the recommended next task, and the exact next action. "
        "Preserve this handoff as history."
    )


def _bullets(values: list[str]) -> str:
    if not values:
        return "- None"
    return "\n".join(f"- {item}" for item in values)
