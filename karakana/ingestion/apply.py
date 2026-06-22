"""Explicit application of reviewed ingestion candidates."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from karakana.ingestion.redaction import contains_secret
from karakana.ingestion.store import IngestionStore


ALLOWED_ROOTS = {"ubongo", "skills", "evals", "prompts", "docs"}
BLOCKED_ROOTS = {"karakana", ".github", "secrets"}


def apply_ingestion_bundle(
    repo_root: Path,
    ingest_id: str,
    *,
    write: bool = False,
    candidate_id: str | None = None,
    allow_high_risk: bool = False,
    allow_behavior_update: bool = False,
) -> tuple[dict, Path]:
    """Apply accepted candidates only when explicitly requested."""
    store = IngestionStore(repo_root)
    bundle = store.load(ingest_id)
    selected = [candidate for candidate in bundle.candidates if candidate_id in {None, candidate.candidate_id}]
    if candidate_id and not selected:
        raise ValueError(f"Candidate not found: {candidate_id}")

    applied: list[str] = []
    blocked: list[str] = []
    warnings: list[str] = []
    backups: list[str] = []

    for candidate in selected:
        try:
            target = _safe_target(repo_root, candidate.target_path)
            _validate_candidate(candidate, write=write, allow_high_risk=allow_high_risk, allow_behavior_update=allow_behavior_update)
        except ValueError as exc:
            blocked.append(candidate.candidate_id)
            warnings.append(str(exc))
            continue
        if not write and candidate.risk_level in {"high", "critical"}:
            warnings.append(f"{candidate.candidate_id}: high-risk candidate would require --allow-high-risk before --write.")
        if not write and candidate.candidate_type == "behavior_update":
            warnings.append(f"{candidate.candidate_id}: behavior update would require --allow-behavior-update before --write.")
        if write:
            backup = _backup_existing(repo_root, ingest_id, target)
            if backup:
                backups.append(str(backup))
            target.parent.mkdir(parents=True, exist_ok=True)
            existing = target.read_text(encoding="utf-8") if target.exists() else ""
            separator = "\n" if existing and not existing.endswith("\n") else ""
            target.write_text(existing + separator + (candidate.proposed_content or candidate.summary).lstrip("\n"), encoding="utf-8")
            candidate.status = "applied"
            applied.append(candidate.candidate_id)

    status = "applied" if write and applied and not blocked else ("partially_applied" if write and applied else ("blocked" if blocked else "dry_run"))
    if write and applied:
        bundle.status = "partially_applied" if blocked else "applied"
        store.save(bundle)
    result = {
        "ingest_id": ingest_id,
        "status": status,
        "dry_run": not write,
        "write_requested": write,
        "applied_candidates": applied,
        "blocked_candidates": blocked,
        "warnings": warnings,
        "backups": backups,
    }
    output = store.bundle_dir(ingest_id) / "apply.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result, output


def _validate_candidate(candidate, *, write: bool, allow_high_risk: bool, allow_behavior_update: bool) -> None:
    if candidate.status == "blocked":
        raise ValueError(f"{candidate.candidate_id}: blocked candidates cannot be applied.")
    if write and candidate.risk_level in {"high", "critical"} and not allow_high_risk:
        raise ValueError(f"{candidate.candidate_id}: high-risk candidate requires --allow-high-risk.")
    if write and candidate.candidate_type == "behavior_update" and not allow_behavior_update:
        raise ValueError(f"{candidate.candidate_id}: behavior update requires --allow-behavior-update.")
    if contains_secret(candidate.proposed_content or ""):
        raise ValueError(f"{candidate.candidate_id}: candidate content contains secret-like material.")


def _safe_target(repo_root: Path, target_path: str | None) -> Path:
    if not target_path:
        raise ValueError("Candidate has no target path.")
    target = Path(target_path)
    if target.is_absolute() or ".." in target.parts:
        raise ValueError(f"Refusing unsafe target path: {target_path}")
    if target.name == ".env" or target.name.startswith(".env."):
        raise ValueError(f"Refusing env target path: {target_path}")
    if target.parts and target.parts[0] in BLOCKED_ROOTS:
        raise ValueError(f"Refusing blocked target path: {target_path}")
    if not target.parts or target.parts[0] not in ALLOWED_ROOTS:
        raise ValueError(f"Target path is not in an allowed ingestion apply root: {target_path}")
    resolved = (repo_root / target).resolve()
    if not resolved.is_relative_to(repo_root.resolve()):
        raise ValueError(f"Refusing target outside repository: {target_path}")
    return resolved


def _backup_existing(repo_root: Path, ingest_id: str, target: Path) -> Path | None:
    if not target.exists():
        return None
    relative = target.relative_to(repo_root)
    backup = repo_root / ".karakana" / "ingestion" / ingest_id / "backups" / relative
    backup.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(target, backup)
    return backup
