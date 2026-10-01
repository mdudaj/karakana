"""Structural closeout check for research decisions; not semantic approval."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

OUTCOMES = {"ready_for_implementation", "resolved_no_change", "decision_required", "evidence_blocked"}
DISPOSITIONS = {"updated", "reused", "planned", "not_applicable"}
AUTHORITY_STATES = {"approved", "not_required", "pending"}
PLACEHOLDERS = {"", "tbd", "todo", "unknown", "none", "n/a", "later", "review later", "...", "<...>"}


def research_resolution_outcome(path: Path) -> str | None:
    """Read the declared outcome after structural validation has passed."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
        if not lines or lines[0] != "---":
            return None
        end = lines.index("---", 1)
        data = yaml.safe_load("\n".join(lines[1:end]))
    except (OSError, UnicodeError, ValueError, yaml.YAMLError):
        return None
    outcome = data.get("status") if isinstance(data, dict) else None
    return outcome if isinstance(outcome, str) and outcome in OUTCOMES else None


def validate_research_resolution(repo_root: Path, path: Path) -> list[str]:
    """Check required decisions and references without judging their truth or quality."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError):
        return ["research_resolution must be a readable Markdown file"]
    if not lines or lines[0] != "---":
        return ["research_resolution needs YAML front matter"]
    try:
        end = lines.index("---", 1)
    except ValueError:
        return ["research_resolution front matter has no closing delimiter"]
    try:
        data = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError:
        return ["research_resolution front matter is invalid YAML"]
    if not isinstance(data, dict):
        return ["research_resolution front matter must be a mapping"]

    errors: list[str] = []
    if not any(line.strip() for line in lines[end + 1:]):
        errors.append("research_resolution needs a Markdown rationale body")
    status = data.get("status")
    if not isinstance(status, str) or status not in OUTCOMES:
        errors.append("status must be a supported research outcome")
        status = None
    for field in ("question", "next_action"):
        if not _meaningful(data.get(field)):
            errors.append(f"{field} must name a concrete research question or action")

    evidence = _rows(data.get("evidence"), "evidence", errors)
    for index, row in enumerate(evidence):
        _require(row, ("source", "finding"), f"evidence[{index}]", errors)

    decision_paths: dict[str, set[str]] = {"requirements": set(), "design": set()}
    for field, required in (("requirements", ("decision", "acceptance", "artifact")),
                            ("design", ("choice", "rationale", "artifact"))):
        for index, row in enumerate(_rows(data.get(field), field, errors)):
            _require(row, required, f"{field}[{index}]", errors)
            if isinstance(row, dict) and _meaningful(row.get("artifact")):
                decision_paths[field].add(row["artifact"])
            if isinstance(row, dict) and status in {"ready_for_implementation", "resolved_no_change", "decision_required"}:
                _require_file(repo_root, row.get("artifact"), f"{field}[{index}].artifact", errors)

    choices = _rows(data.get("artifact_choices"), "artifact_choices", errors)
    chosen_kinds: set[str] = set()
    chosen_paths: dict[str, set[str]] = {"requirements": set(), "design": set()}
    for index, row in enumerate(choices):
        label = f"artifact_choices[{index}]"
        _require(row, ("kind", "disposition", "rationale"), label, errors)
        if not isinstance(row, dict):
            continue
        kind = row.get("kind")
        if _meaningful(kind):
            chosen_kinds.add(kind)
        if isinstance(kind, str) and kind in chosen_paths and _meaningful(row.get("path")):
            chosen_paths[kind].add(row["path"])
        disposition = row.get("disposition")
        if not isinstance(disposition, str) or disposition not in DISPOSITIONS:
            errors.append(f"{label}.disposition must be updated, reused, planned or not_applicable")
        if isinstance(kind, str) and kind in {"requirements", "design"} and disposition == "not_applicable":
            errors.append(f"{label} cannot omit a requirements or design choice")
        if status == "decision_required" and isinstance(kind, str) and kind in {"requirements", "design"} and disposition == "planned":
            errors.append(f"{label} must be reviewable before requesting a decision")
        if disposition != "not_applicable" and not _meaningful(row.get("path")):
            errors.append(f"{label}.path must identify the chosen artifact")
        if status in {"ready_for_implementation", "resolved_no_change", "decision_required"}:
            if disposition == "planned":
                errors.append(f"{label} cannot remain planned in a resolved closeout")
            elif isinstance(disposition, str) and disposition in {"updated", "reused"}:
                _require_file(repo_root, row.get("path"), f"{label}.path", errors)
    if not {"requirements", "design"} <= chosen_kinds:
        errors.append("artifact_choices must cover requirements and design")
    for field in ("requirements", "design"):
        if not decision_paths[field] <= chosen_paths[field]:
            errors.append(f"{field} artifacts must match artifact_choices paths")

    authority = data.get("authority")
    if not isinstance(authority, dict):
        errors.append("authority must state its status and evidence")
    else:
        if not isinstance(authority.get("state"), str) or authority.get("state") not in AUTHORITY_STATES:
            errors.append("authority.state must be approved, not_required or pending")
        if not _meaningful(authority.get("evidence")):
            errors.append("authority.evidence must identify the applicable authorization or limit")
        if status in {"ready_for_implementation", "resolved_no_change"} and authority.get("state") not in ("approved", "not_required"):
            errors.append("resolved research cannot have pending authority")

    pending = data.get("pending_decisions")
    if not isinstance(pending, list):
        errors.append("pending_decisions must be a list")
        pending = []
    if status in {"ready_for_implementation", "resolved_no_change"} and pending:
        errors.append("resolved research cannot have pending decisions")
    if status in {"decision_required", "evidence_blocked"} and not pending:
        errors.append("blocked research must name a pending decision or evidence gap")
    for index, row in enumerate(pending):
        _require(row, ("owner", "question", "next_action"), f"pending_decisions[{index}]", errors)
    return errors


def _rows(value: Any, field: str, errors: list[str]) -> list[Any]:
    if not isinstance(value, list) or not value:
        errors.append(f"{field} must contain at least one concrete entry")
        return []
    return value


def _require(row: Any, fields: tuple[str, ...], label: str, errors: list[str]) -> None:
    if not isinstance(row, dict):
        errors.append(f"{label} must be a mapping")
        return
    for field in fields:
        if not _meaningful(row.get(field)):
            errors.append(f"{label}.{field} must be concrete")


def _require_file(repo_root: Path, value: Any, label: str, errors: list[str]) -> None:
    if not _meaningful(value):
        return  # The field-level check already reports this.
    try:
        file_path = Path(value)
        if not file_path.is_absolute():
            file_path = repo_root / file_path
        if not file_path.is_file():
            errors.append(f"{label} must point to a nonempty local file")
        else:
            with file_path.open("rb") as stream:
                if not stream.read(1):
                    errors.append(f"{label} must point to a nonempty local file")
    except (OSError, TypeError, ValueError):
        errors.append(f"{label} must point to a nonempty local file")


def _meaningful(value: Any) -> bool:
    return isinstance(value, str) and value.strip().lower() not in PLACEHOLDERS and bool(value.strip())
