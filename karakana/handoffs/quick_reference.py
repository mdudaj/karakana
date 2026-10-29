"""Explicit, sourced continuation snapshots; never infer delivery or approval."""
from __future__ import annotations

import hashlib
from html import escape
from pathlib import Path

from karakana.handoffs.redaction import redact_handoff_text

DELIVERY_STAGES = ("implemented", "verified", "merged", "deployed", "accepted")
BACKLOG_STATES = {"done", "in_progress", "next", "queued", "blocked", "deferred", "conditional"}


def build_quick_reference(repo_root: Path, position: str | None = None,
                          delivery_states: list[str] | None = None,
                          backlog_source: str | None = None,
                          backlog_items: list[str] | None = None) -> dict:
    """Validate authored claims and fingerprint their local backlog authority."""
    if not any((position, delivery_states, backlog_source, backlog_items)):
        return {}
    states = {}
    for entry in delivery_states or []:
        parts = entry.split("=", 1)
        if len(parts) != 2 or parts[0].strip() not in DELIVERY_STAGES or not parts[1].strip():
            raise ValueError("Delivery state must be STAGE=VALUE using implemented, verified, merged, deployed or accepted.")
        key, value = (part.strip() for part in parts)
        if key in states:
            raise ValueError("Duplicate delivery stage; provide each stage once.")
        states[key] = value
    items, seen = [], set()
    for entry in backlog_items or []:
        parts = [part.strip() for part in entry.split("|", 2)]
        if len(parts) != 3 or not all(parts) or parts[1] not in BACKLOG_STATES:
            raise ValueError("Backlog item must be ID|STATE|SUMMARY using a documented backlog state.")
        if parts[0] in seen:
            raise ValueError("Duplicate backlog item ID; provide each item once.")
        seen.add(parts[0])
        items.append(dict(zip(("id", "state", "summary"), parts)))
    if items and not backlog_source:
        raise ValueError("Authored backlog items require --backlog-source.")
    backlog = {"items": items}
    if backlog_source:
        source = Path(backlog_source)
        source = (repo_root / source).resolve() if not source.is_absolute() else source.resolve()
        if not source.is_file():
            raise ValueError("Backlog source must be an existing local file.")
        backlog.update(source=str(source), sha256=_digest(source))
    return {"position": position or "", "delivery_state": states, "backlog": backlog}


def quick_reference_data(handoff) -> dict:
    continuation = handoff.continuation if isinstance(handoff.continuation, dict) else {}
    value = continuation.get("quick_reference", {})
    return value if isinstance(value, dict) else {}


def quick_reference_warnings(handoff) -> list[str]:
    """Check the recorded source without changing the snapshot or source file."""
    continuation = handoff.continuation if isinstance(handoff.continuation, dict) else {}
    if "quick_reference" in continuation and not isinstance(continuation["quick_reference"], dict):
        return ["Quick-reference metadata is invalid; verify the recorded state before acting."]
    value = quick_reference_data(handoff)
    backlog = value.get("backlog", {})
    if not isinstance(backlog, dict):
        return ["Backlog snapshot metadata is invalid; reconcile it before acting."]
    items = backlog.get("items", [])
    if not isinstance(items, list) or any(not isinstance(item, dict) for item in items):
        return ["Backlog item metadata is invalid; reconcile the snapshot before acting."]
    source = backlog.get("source")
    if not source:
        return []
    try:
        digest = _digest(Path(source))
    except (OSError, TypeError, ValueError):
        return ["Backlog source missing or unreadable; reconcile the recorded snapshot before acting."]
    if not backlog.get("sha256") or digest != backlog["sha256"]:
        return ["Backlog source changed since this snapshot; reconcile position, states and next action before acting."]
    return []


def render_quick_reference(handoff) -> str:
    value = quick_reference_data(handoff)
    states = value.get("delivery_state", {})
    states = states if isinstance(states, dict) else {}
    backlog = value.get("backlog", {})
    backlog = backlog if isinstance(backlog, dict) else {}
    items = backlog.get("items", [])
    items = items if isinstance(items, list) else []
    lines = ["## Quick Reference", "",
             f"Where we are: {_cell(value.get('position') or handoff.current_milestone)}", "",
             "| Delivery stage | Recorded status |", "| --- | --- |"]
    lines.extend(f"| {stage.capitalize()} | {_cell(states.get(stage) or 'Not recorded')} |"
                 for stage in DELIVERY_STAGES)
    lines.extend(["", f"Snapshot: {_cell(handoff.updated_at)}. Recorded claims; recheck evidence before acting.",
                  f"Backlog source: {_cell(backlog.get('source') or 'Not recorded')}", ""])
    if items:
        lines.extend(["| Item | State | Current backlog snapshot |", "| --- | --- | --- |"])
        for item in items:
            if isinstance(item, dict):
                lines.append(f"| {_cell(item.get('id', '?'))} | {_cell(item.get('state', 'Not recorded'))} | {_cell(item.get('summary', 'Not recorded'))} |")
    else:
        lines.append("Backlog items: Not recorded. Supply --backlog-source and --backlog-item on refresh.")
    lines.extend(["", f"Next action: {_cell(handoff.exact_next_action or 'Verify current state and select one bounded action.')}"])
    return "\n".join(lines)


def _cell(value) -> str:
    # Hand-authored rows must not break the Markdown table or expose raw secrets.
    safe = redact_handoff_text(str(value))
    safe = "".join(char for char in safe if char in "\n\t" or (ord(char) >= 32 and not 127 <= ord(char) <= 159))
    return escape(safe, quote=False).replace("|", "\\|").replace("\n", " ")


def _digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()
