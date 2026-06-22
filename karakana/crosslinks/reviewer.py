"""Review crosslink bundles for boundary and safety issues."""

from __future__ import annotations

import json
from pathlib import Path

from karakana.crosslinks.boundaries import validate_proposal_boundary
from karakana.crosslinks.store import CrosslinkStore
from karakana.crosslinks.summary import render_review


def review_crosslink(repo_root: Path, crosslink_id: str) -> tuple[dict, Path]:
    store = CrosslinkStore(repo_root)
    bundle = store.load(crosslink_id)
    warnings = []
    blocked = False
    if not bundle.patterns:
        warnings.append("No patterns were detected.")
    for pattern in bundle.patterns:
        if not pattern.evidence and pattern.pattern_type != "manual_review":
            warnings.append(f"{pattern.pattern_id}: pattern has no evidence.")
        if pattern.pattern_type == "conflicting_memory":
            warnings.append(f"{pattern.pattern_id}: conflicting memory requires manual review.")
    for proposal in bundle.proposals:
        errors = validate_proposal_boundary(proposal)
        warnings.extend(errors)
        if errors:
            blocked = True
    result = {"crosslink_id": crosslink_id, "status": "blocked" if blocked else "reviewed", "blocked": blocked, "warnings": warnings, "patterns": len(bundle.patterns), "proposals": len(bundle.proposals)}
    bundle.status = "blocked" if blocked else "reviewed"
    path = store.bundle_dir(crosslink_id) / "review.md"
    path.write_text(render_review(bundle, warnings, blocked), encoding="utf-8")
    (path.parent / "review.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    store.save(bundle)
    return result, path
