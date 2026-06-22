"""Dry-run and explicit application of crosslink proposals."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from karakana.crosslinks.boundaries import validate_proposal_boundary
from karakana.crosslinks.store import CrosslinkStore


def apply_crosslink(repo_root: Path, crosslink_id: str, *, write: bool = False, proposal_id: str | None = None, allow_high_risk: bool = False) -> tuple[dict, Path]:
    store = CrosslinkStore(repo_root)
    bundle = store.load(crosslink_id)
    selected = [proposal for proposal in bundle.proposals if proposal_id in {None, proposal.proposal_id}]
    if proposal_id and not selected:
        raise ValueError(f"Proposal not found: {proposal_id}")
    applied = []
    blocked = []
    warnings = []
    backups = []
    for proposal in selected:
        errors = validate_proposal_boundary(proposal)
        if write and proposal.risk_level in {"high", "critical"} and not allow_high_risk:
            errors.append(f"{proposal.proposal_id}: high-risk proposal requires --allow-high-risk.")
        if errors:
            blocked.append(proposal.proposal_id)
            warnings.extend(errors)
            continue
        if not write:
            if proposal.risk_level in {"high", "critical"}:
                warnings.append(f"{proposal.proposal_id}: high-risk proposal would require --allow-high-risk before --write.")
            continue
        target = repo_root / str(proposal.target_path)
        backup = _backup(repo_root, crosslink_id, target)
        if backup:
            backups.append(str(backup))
        target.parent.mkdir(parents=True, exist_ok=True)
        existing = target.read_text(encoding="utf-8") if target.exists() else ""
        separator = "\n" if existing and not existing.endswith("\n") else ""
        target.write_text(existing + separator + (proposal.proposed_content or proposal.summary).lstrip("\n"), encoding="utf-8")
        applied.append(proposal.proposal_id)
    status = "applied" if write and applied and not blocked else ("partially_applied" if write and applied else ("blocked" if blocked and write else "dry_run"))
    result = {"crosslink_id": crosslink_id, "status": status, "dry_run": not write, "write_requested": write, "applied_proposals": applied, "blocked_proposals": blocked, "warnings": warnings, "backups": backups}
    output = store.bundle_dir(crosslink_id) / "apply.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result, output


def _backup(repo_root: Path, crosslink_id: str, target: Path) -> Path | None:
    if not target.exists():
        return None
    backup = repo_root / ".karakana" / "crosslinks" / crosslink_id / "backups" / target.relative_to(repo_root)
    backup.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(target, backup)
    return backup
