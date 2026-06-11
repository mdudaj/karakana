"""Generate crosslink proposal artifacts."""

from __future__ import annotations

import secrets
from pathlib import Path

from karakana.crosslinks.classifier import classify_pattern
from karakana.crosslinks.schemas import CrosslinkProposal
from karakana.crosslinks.store import CrosslinkStore


def generate_proposals(repo_root: Path, crosslink_id: str) -> tuple[list[CrosslinkProposal], Path]:
    store = CrosslinkStore(repo_root)
    bundle = store.load(crosslink_id)
    proposals: list[CrosslinkProposal] = []
    for pattern in bundle.patterns:
        classification = classify_pattern(pattern)
        proposal = CrosslinkProposal(
            proposal_id=f"proposal-{secrets.token_hex(3)}",
            proposal_type=classification["proposal_type"],
            title=f"Proposal: {pattern.title}",
            summary=pattern.summary,
            target_path=classification["target"],
            proposed_content=_content(pattern, classification),
            affected_projects=list(pattern.projects),
            source_patterns=[pattern.pattern_id],
            risk_level=pattern.risk_level,
            metadata={"classification": classification},
        )
        proposals.append(proposal)
    bundle.proposals = proposals
    bundle.status = "ready_for_review"
    path = store.save(bundle)
    _write_proposal_files(store.bundle_dir(crosslink_id), proposals)
    return proposals, path


def _content(pattern, classification: dict) -> str:
    scope = classification.get("scope")
    projects = ", ".join(pattern.projects)
    return f"""## Crosslink Candidate

Pattern: {pattern.title}
Scope: {scope}
Affected projects: {projects}

{pattern.summary}

This is a reviewable proposal only. Do not copy project-specific memory between projects.
"""


def _write_proposal_files(root: Path, proposals: list[CrosslinkProposal]) -> None:
    mapping = {
        "global_ubongo_update": "global-ubongo",
        "shared_skill_update": "skills",
        "shared_eval_update": "evals",
        "shared_prompt_update": "prompts",
        "skillpack_update": "skillpacks",
        "cross_project_issue_draft": "issues",
        "project_specific_follow_up": "issues",
        "manual_review": "issues",
    }
    for proposal in proposals:
        subdir = root / "proposed-updates" / mapping.get(proposal.proposal_type, "issues")
        subdir.mkdir(parents=True, exist_ok=True)
        (subdir / f"{proposal.proposal_id}.md").write_text(proposal.proposed_content or proposal.summary, encoding="utf-8")
