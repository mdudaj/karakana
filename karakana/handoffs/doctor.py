"""Validity checks for the latest project handoff."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from karakana.handoffs.redaction import contains_unredacted_secret
from karakana.handoffs.schemas import HandoffDoctorReport
from karakana.handoffs.store import HandoffStore


def diagnose_handoff(repo_root: Path, project: str, skillpack: str | None = None, stale_after_days: int = 7) -> HandoffDoctorReport:
    store = HandoffStore(repo_root)
    handoff = store.latest(project, skillpack)
    if not handoff:
        return HandoffDoctorReport(project, None, "error", {"exists": False}, errors=["No project handoff exists."])
    warnings: list[str] = []
    errors: list[str] = []
    markdown_path = store.run_dir(handoff.handoff_id) / "handoff.md"
    age_days = (datetime.now(timezone.utc) - datetime.fromisoformat(handoff.updated_at)).total_seconds() / 86400
    stale = age_days > stale_after_days
    if stale:
        warnings.append(f"Latest handoff is stale: {age_days:.1f} days old (limit {stale_after_days}).")
    missing = [path for path in handoff.reference_artifacts if not _resolve_reference(repo_root, path).exists()]
    if missing:
        errors.extend(f"Referenced artifact is missing: {path}" for path in missing)
    missing_skills = [name for name in handoff.suggested_skills if not (repo_root / "skills" / name / "SKILL.md").exists()]
    if missing_skills:
        errors.extend(f"Suggested skill is missing: {name}" for name in missing_skills)
    text = markdown_path.read_text(encoding="utf-8") if markdown_path.exists() else ""
    secret_safe = bool(text) and not contains_unredacted_secret(text)
    if not markdown_path.exists():
        errors.append(f"Handoff Markdown is missing: {markdown_path}")
    elif not secret_safe:
        errors.append("Handoff contains an unredacted secret-like value.")
    workspace_match = handoff.project == project and (skillpack is None or handoff.skillpack == skillpack)
    if not workspace_match:
        errors.append("Latest handoff project or skillpack does not match the request.")
    checks = {
        "exists": True,
        "not_stale": not stale,
        "references_exist": not missing,
        "suggested_skills_exist": not missing_skills,
        "secret_redaction": secret_safe,
        "project_matches": workspace_match,
    }
    status = "error" if errors else ("warning" if warnings else "passed")
    return HandoffDoctorReport(project, handoff.handoff_id, status, checks, warnings, errors)


def _resolve_reference(repo_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path
