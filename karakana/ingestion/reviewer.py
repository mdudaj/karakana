"""Review ingestion candidates before any apply step."""

from __future__ import annotations

import json
from pathlib import Path

from karakana.ingestion.redaction import contains_secret
from karakana.ingestion.schemas import IngestionBundle
from karakana.ingestion.store import IngestionStore
from karakana.ingestion.summary import render_review_markdown


HIGH_RISK_TARGET_PREFIXES = ("karakana/", ".github/workflows/")
BLOCKED_TARGETS = (".env", ".env.", "secrets/")


def review_ingestion_bundle(repo_root: Path, ingest_id: str) -> tuple[dict, Path]:
    """Review a stored ingestion bundle and write review.md."""
    store = IngestionStore(repo_root)
    bundle = store.load(ingest_id)
    warnings: list[str] = []
    blocked = False

    for candidate in bundle.candidates:
        candidate_warnings, candidate_blocked = review_candidate(candidate.to_dict())
        warnings.extend(candidate_warnings)
        if candidate_blocked:
            blocked = True
            candidate.status = "blocked"

    status = "blocked" if blocked else ("warning" if warnings else "ready_for_review")
    if blocked:
        bundle.status = "blocked"
    result = {
        "ingest_id": ingest_id,
        "status": status,
        "blocked": blocked,
        "warnings": warnings,
        "candidate_count": len(bundle.candidates),
        "high_risk_candidates": [candidate.candidate_id for candidate in bundle.candidates if candidate.risk_level in {"high", "critical"}],
    }
    bundle_dir = store.bundle_dir(ingest_id)
    bundle_dir.mkdir(parents=True, exist_ok=True)
    review_path = bundle_dir / "review.md"
    review_path.write_text(render_review_markdown(bundle, warnings, blocked), encoding="utf-8")
    (bundle_dir / "review.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    store.save(bundle)
    return result, review_path


def review_candidate(candidate: dict) -> tuple[list[str], bool]:
    warnings: list[str] = []
    blocked = False
    target = candidate.get("target_path") or ""
    proposed = candidate.get("proposed_content") or ""
    evidence = candidate.get("evidence") or []

    if candidate.get("risk_level") in {"high", "critical"}:
        warnings.append(f"{candidate.get('candidate_id')}: high-risk candidate requires careful review.")
    if candidate.get("candidate_type") == "behavior_update":
        warnings.append(f"{candidate.get('candidate_id')}: behavior updates require explicit approval.")
    if any(target == blocked or target.startswith(blocked) for blocked in BLOCKED_TARGETS):
        warnings.append(f"{candidate.get('candidate_id')}: target path is blocked: {target}")
        blocked = True
    if target.startswith(HIGH_RISK_TARGET_PREFIXES):
        warnings.append(f"{candidate.get('candidate_id')}: target path is high-risk and proposal-only: {target}")
        blocked = True
    if target.startswith("/") or ".." in Path(target).parts:
        warnings.append(f"{candidate.get('candidate_id')}: unsafe target path: {target}")
        blocked = True
    if contains_secret(proposed):
        warnings.append(f"{candidate.get('candidate_id')}: proposed content still contains secret-like material.")
        blocked = True
    if not evidence:
        warnings.append(f"{candidate.get('candidate_id')}: candidate has no evidence.")
        blocked = True
    return warnings, blocked
