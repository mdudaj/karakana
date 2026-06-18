"""Markdown rendering for next-milestone decisions."""

from __future__ import annotations

from karakana.milestones.schemas import NextMilestoneDecision


def render_next_milestone(decision: NextMilestoneDecision) -> str:
    lines = [
        "# Next Milestone Decision",
        "",
        "## Run Metadata",
        "",
        f"- Run ID: {decision.run_id}",
        f"- Created at: {decision.created_at}",
        f"- Workspace: {decision.workspace or 'None'}",
        f"- Project: {decision.project}",
        f"- Skillpack: {decision.skillpack}",
        f"- Brainstorm used: {decision.brainstorm_used}",
        f"- Strict blockers: {'yes' if decision.blocked else 'no'}",
        "",
        "## Current State Summary",
        "",
        decision.current_state_summary,
        "",
        "## Evidence Consulted",
        "",
    ]
    lines.extend(
        f"- {item.source_type}: {item.source_id or 'current'} - {item.summary} "
        f"[relevance: {item.relevance}, score: {item.relevance_score:.4f}, "
        f"matched: {', '.join(item.matched_terms) or 'none'}] ({item.path or 'no path'})"
        for item in decision.evidence
    )
    if not decision.evidence:
        lines.append("- No durable evidence was found; decision confidence is limited.")
    lines.extend(["", "## Open Findings", ""])
    lines.extend(f"- {item}" for item in decision.open_findings or ["No unresolved findings were identified from available artifacts."])
    lines.extend(
        [
            "",
            "## Candidate Milestones",
            "",
            "The criterion scores use a 0-5 ordinal scale. Decision weights are normalized score shares, not probabilities.",
            "",
            "### Decision Criteria",
            "",
            "| Criterion | Weight | Description |",
            "|---|---:|---|",
        ]
    )
    for criterion in decision.criteria:
        lines.append(f"| {criterion.name} | {criterion.weight:.2f} | {criterion.description} |")
    lines.extend(
        [
            "",
            "### Ranked Candidates",
            "",
            "| Candidate | Score | Decision Weight | Rationale | Risks | Cost | Reversibility |",
            "|---|---:|---:|---|---|---|---|",
        ]
    )
    for candidate in decision.candidates:
        lines.append(
            f"| {candidate.title} | {candidate.decision_score:.3f} | {candidate.decision_weight:.4f} | {candidate.rationale} | "
            f"{candidate.risks} | {candidate.cost} | {candidate.reversibility} |"
        )
    lines.extend(
        [
            "",
            "### Criterion Matrix",
            "",
            "| Candidate | " + " | ".join(item.name for item in decision.criteria) + " |",
            "|---|" + "---:|" * len(decision.criteria),
        ]
    )
    for candidate in decision.candidates:
        lines.append(
            f"| {candidate.title} | "
            + " | ".join(f"{candidate.criterion_scores[item.name]:.1f}" for item in decision.criteria)
            + " |"
        )
    lines.extend(
        [
            "",
            "## Sensitivity Analysis",
            "",
            f"- Method: {decision.sensitivity.method}",
            f"- Scenarios tested: {decision.sensitivity.scenarios_tested}",
            f"- Baseline margin: {decision.sensitivity.baseline_margin:.4f}",
            f"- Robust winner: {'yes' if decision.sensitivity.robust else 'no'}",
            f"- Alternate winners: {', '.join(decision.sensitivity.alternate_winners) or 'none'}",
            f"- Critical criteria: {', '.join(decision.sensitivity.critical_criteria) or 'none'}",
            "",
            "## Recommended Milestone",
            "",
            decision.recommended_milestone,
            "",
            "## Decision Rationale",
            "",
            decision.decision_rationale,
            "",
            "## Rejected Alternatives",
            "",
            *[f"- {item}" for item in decision.rejected_alternatives],
            "",
            "## Generated Instructions",
            "",
            decision.generated_instructions,
            "",
            "## Verification Plan",
            "",
            *[f"- {item}" for item in decision.verification_plan],
            "",
            "## Definition of Done",
            "",
            *[f"- {item}" for item in decision.definition_of_done],
            "",
            "## Safety Notes",
            "",
            *[f"- {item}" for item in decision.safety_notes],
        ]
    )
    if decision.blockers:
        lines.extend(["", "## Strict Mode Blockers", "", *[f"- {item}" for item in decision.blockers]])
    if decision.warnings:
        lines.extend(["", "## Warnings", "", *[f"- {item}" for item in decision.warnings]])
    return "\n".join(lines).rstrip() + "\n"
