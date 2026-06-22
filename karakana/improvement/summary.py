"""Markdown rendering for self-improvement proposals."""

from __future__ import annotations

from karakana.improvement.schemas import ImprovementProposal


def render_proposal_markdown(proposal: ImprovementProposal) -> str:
    lines: list[str] = [
        "# Karakana Self-Improvement Proposal",
        "",
        "## Proposal",
        "",
        f"- Proposal ID: {proposal.proposal_id}",
        f"- Project: {proposal.project or ''}",
        f"- Status: {proposal.status}",
        f"- Created: {proposal.created_at}",
        f"- Source runs: {', '.join(proposal.source_run_ids) if proposal.source_run_ids else 'None'}",
        "",
        "## Summary",
        "",
        proposal.summary,
        "",
        "## Findings",
        "",
    ]
    if proposal.changes:
        for change in proposal.changes:
            for evidence in change.evidence:
                lines.append(f"- {change.title}: {evidence.summary or 'See evidence'}")
    else:
        lines.append("- No findings generated.")

    lines.extend(["", "## Proposed Changes", ""])
    if not proposal.changes:
        lines.append("- No proposed changes.")
    for index, change in enumerate(proposal.changes, start=1):
        lines.extend(
            [
                f"### Change {index}: {change.title}",
                "",
                f"- Type: {change.change_type}",
                f"- Target: {change.target_path}",
                f"- Risk: {change.risk_level}",
                f"- Requires human review: {change.requires_human_review}",
                "",
                "#### Rationale",
                "",
                change.rationale,
                "",
                "#### Evidence",
                "",
            ]
        )
        if change.evidence:
            for evidence in change.evidence:
                lines.append(
                    f"- Run `{evidence.run_id}`"
                    + (f", artifact `{evidence.artifact_path}`" if evidence.artifact_path else "")
                    + (f": {evidence.summary}" if evidence.summary else "")
                )
        else:
            lines.append("- No evidence references.")
        lines.extend(["", "#### Proposed Content", "", change.proposed_content or "_No direct content proposed._", ""])

    lines.extend(["## Warnings", ""])
    lines.extend(_list_lines(proposal.warnings))
    lines.extend(["", "## Next Actions", ""])
    lines.extend(_list_lines(proposal.next_actions))
    lines.append("")
    return "\n".join(lines)


def _list_lines(values: list[str]) -> list[str]:
    if not values:
        return ["- None"]
    return [f"- {value}" for value in values]
