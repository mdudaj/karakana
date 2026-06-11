"""Markdown rendering for crosslink bundles."""

from __future__ import annotations

from karakana.crosslinks.schemas import CrosslinkBundle


def render_crosslink(bundle: CrosslinkBundle) -> str:
    body = [
        "# Karakana Cross-Project Knowledge Link",
        "",
        "## Crosslink",
        "",
        f"- Crosslink ID: {bundle.crosslink_id}",
        f"- Workspace: {bundle.workspace}",
        f"- Status: {bundle.status}",
        f"- Created: {bundle.created_at}",
        "",
        "## Projects",
        "",
        *[f"- {project.project_id} ({project.skillpack or 'no skillpack'}): {', '.join(project.tags)}" for project in bundle.projects],
        "",
        "## Patterns",
        "",
    ]
    for pattern in bundle.patterns:
        body.extend(
            [
                f"### {pattern.title}",
                "",
                f"- Type: {pattern.pattern_type}",
                f"- Projects: {', '.join(pattern.projects)}",
                f"- Confidence: {pattern.confidence}",
                f"- Risk: {pattern.risk_level}",
                "",
                "#### Summary",
                "",
                pattern.summary,
                "",
                "#### Evidence",
                "",
                _bullets([f"{item.project_id}: {item.summary or item.source_type}" for item in pattern.evidence]),
                "",
                "#### Suggested Targets",
                "",
                _bullets(pattern.suggested_targets),
                "",
            ]
        )
    body.extend(["## Proposals", ""])
    for proposal in bundle.proposals:
        body.extend(
            [
                f"### {proposal.title}",
                "",
                f"- Type: {proposal.proposal_type}",
                f"- Target: {proposal.target_path or ''}",
                f"- Affected projects: {', '.join(proposal.affected_projects)}",
                f"- Risk: {proposal.risk_level}",
                f"- Requires human review: {proposal.requires_human_review}",
                "",
                "#### Summary",
                "",
                proposal.summary,
                "",
                "#### Proposed Content",
                "",
                proposal.proposed_content or "Needs review.",
                "",
            ]
        )
    body.extend(["## Boundary Review", "", "- Project-specific memory remains project-specific.", "- Crosslink apply does not write `ubongo/projects/*/`.", "- No cross-project mutation is performed.", "", "## Warnings", "", _bullets(bundle.warnings), "", "## Recommended Next Actions", "", _bullets(bundle.next_actions)])
    return "\n".join(body) + "\n"


def render_review(bundle: CrosslinkBundle, warnings: list[str], blocked: bool) -> str:
    return f"""# Karakana Crosslink Review

## Summary

- Crosslink ID: {bundle.crosslink_id}
- Workspace: {bundle.workspace}
- Blocked: {blocked}
- Patterns: {len(bundle.patterns)}
- Proposals: {len(bundle.proposals)}

## Warnings

{_bullets(warnings)}

## Boundary Review

- No project memory should be copied into another project.
- Global updates must be qualified by supporting projects.
- Project-specific follow-ups should remain issue drafts or manual review items.

## Recommended Next Actions

- Review proposals manually.
- Run `karakana crosslink propose {bundle.crosslink_id}` if proposals are missing.
- Use `karakana crosslink apply {bundle.crosslink_id}` for dry-run only before any explicit write.
"""


def _bullets(values: list[str]) -> str:
    return "\n".join(f"- {value}" for value in values) if values else "- None"
