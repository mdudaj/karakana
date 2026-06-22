"""Markdown rendering for Karakana handoffs."""

from __future__ import annotations

from karakana.handoffs.schemas import HandoffArtifact


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

## Return Handoff Expectations

{_return_expectation(handoff)}

## Staleness / Validity Notes

{_bullets(handoff.staleness_notes)}

## Notes for Fresh Agent

{_bullets(handoff.notes_for_fresh_agent)}
"""


def render_session_start(handoff: HandoffArtifact, path: str) -> str:
    return f"""# Karakana Session Start

- Handoff: {path}
- Project: {handoff.project}
- Current milestone: {handoff.current_milestone}
- Purpose: {handoff.purpose}
- Recovered: {handoff.recovered}

## OKF Concepts

Loaded:
{_bullets(handoff.okf_concepts_loaded)}

Changed:
{_bullets(handoff.okf_concepts_changed)}

## Inspect First

{_bullets(handoff.inspect_first)}

## Do Not Reread Unless Needed

{_bullets(handoff.do_not_reread)}

## Suggested Skills

{_bullets(handoff.suggested_skills)}

## Exact Next Action

{handoff.exact_next_action}

## Safety

{_bullets(handoff.safety_constraints)}
"""


def _return_expectation(handoff: HandoffArtifact) -> str:
    if not handoff.return_handoff_expected:
        return "No return handoff was requested."
    return "Before ending, create a new handoff that records completed work, verification, remaining findings, changed references, and the exact next action. Preserve this handoff as history."


def _bullets(values: list[str]) -> str:
    if not values:
        return "- None"
    return "\n".join(f"- {item}" for item in values)
