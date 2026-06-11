"""Boundary policy for cross-project knowledge links."""

from __future__ import annotations

from pathlib import Path

from karakana.ingestion.redaction import contains_secret

ALLOWED_ROOTS = {"ubongo", "skills", "evals", "docs"}
BLOCKED_PREFIXES = ("ubongo/projects/", "karakana/", ".github/workflows/", "secrets/")


def validate_crosslink_target(target_path: str | None) -> list[str]:
    if not target_path:
        return []
    target = Path(target_path)
    errors = []
    if target.is_absolute() or ".." in target.parts:
        errors.append(f"Unsafe target path: {target_path}")
    if target.name == ".env" or target.name.startswith(".env."):
        errors.append(f"Blocked env target: {target_path}")
    if any(target_path.startswith(prefix) for prefix in BLOCKED_PREFIXES):
        errors.append(f"Blocked crosslink target: {target_path}")
    if target.parts and target.parts[0] not in ALLOWED_ROOTS:
        errors.append(f"Crosslink apply target is not in an allowed root: {target_path}")
    return errors


def validate_proposal_boundary(proposal) -> list[str]:
    errors = validate_crosslink_target(proposal.target_path)
    if proposal.proposal_type == "manual_review":
        errors.append(f"{proposal.proposal_id}: manual review proposals cannot be applied.")
    if (proposal.metadata or {}).get("classification", {}).get("scope") == "conflicting":
        errors.append(f"{proposal.proposal_id}: conflicting proposals cannot be applied.")
    if proposal.proposed_content and contains_secret(proposal.proposed_content):
        errors.append(f"{proposal.proposal_id}: proposal contains secret-like content.")
    if proposal.proposal_type == "global_ubongo_update" and len(set(proposal.affected_projects)) < 2:
        errors.append(f"{proposal.proposal_id}: global memory updates require support from at least two projects.")
    return errors
