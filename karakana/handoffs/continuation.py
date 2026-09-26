"""Deterministic continuation recommendations; never executes a model."""

from __future__ import annotations

import hashlib
from pathlib import Path

from karakana.models.router import infer_task_type, route_model

STAGES = ("research", "architect", "plan")
EFFICIENCY_RULES = (
    "Research new uncertainties only; reuse applicable approved evidence.",
    "Focused tests while debugging; full required regression gate before completion.",
    "Bound tool output to relevant failures, functions and diffs.",
    "One compact delivery record plus linked append-only handoff; do not duplicate artifacts.",
    "After two unsuccessful diagnostic attempts, stop speculative patches and escalate/replan.",
    "No automatic multi-agent fan-out or maximum reasoning; record a specific benefit first.",
)


def build_continuation(repo_root: Path, task: str | None, routes: dict,
                       reuse_stages: list[str] | None = None, reviewed: bool = False,
                       slice_complete: bool = False, failed_attempts: int = 0) -> dict:
    if failed_attempts < 0:
        raise ValueError("Failed attempts cannot be negative.")
    evidence = {}
    if reuse_stages and (not reviewed or not task):
        raise ValueError("Stage reuse requires --next-task and --reuse-reviewed applicability review.")
    for entry in reuse_stages or []:
        stage, separator, reference = entry.partition("=")
        if not separator or stage not in STAGES or not reference or stage in evidence:
            raise ValueError("Use one --reuse-stage STAGE=PATH per research, architect, or plan stage.")
        path = (repo_root / reference).resolve()
        if not path.is_file():
            raise ValueError(f"Reuse evidence is not a file: {path}")
        evidence[stage] = {"path": str(path), "sha256": _digest(path)}
    task_type = "high_risk_code_review" if failed_attempts >= 2 else infer_task_type(task or "Review recovered project state")
    route = route_model(task_type, skillpack_routes=routes)
    fresh = slice_complete or failed_attempts >= 2
    reason = (
        "Two failed diagnostic attempts: preserve hypotheses/results and start a focused diagnostic review."
        if failed_attempts >= 2 else
        "Completed slice: start a fresh conversation with this handoff for the next bounded task."
        if slice_complete else
        "Continue the unfinished task; start fresh if context is crowded or the project/model changes."
    )
    return {
        "next_task": task or "Confirm the next bounded task before selecting a model.",
        "model_route": route if task else {},
        "selection_status": "recommendation_only; availability and active model unverified",
        "conversation": "new" if fresh else "continue",
        "conversation_reason": reason,
        "failed_attempts": failed_attempts,
        "evidence": evidence,
    }


def _digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def next_stage(guidance: dict) -> str:
    if guidance.get("failed_attempts", 0) >= 2:
        return "research (diagnostic escalation; review failed hypotheses before further edits)"
    for stage in STAGES:
        reference = guidance.get("evidence", {}).get(stage)
        if not reference:
            return stage
        try:
            if _digest(Path(reference["path"])) != reference["sha256"]:
                return stage
        except (OSError, KeyError):
            return stage
    return "deliver"


def render_continuation(guidance: dict) -> str:
    route = guidance.get("model_route", {})
    model = f"{route.get('provider')} / {route.get('model')} ({route.get('role')})" if route else "Not selected: supply the next bounded task."
    lines = [
        f"- Next task: {guidance.get('next_task', 'Confirm the next bounded task.')}",
        f"- Next stage: {next_stage(guidance)}. Recheck applicability against current source and approvals.",
        f"- Recommended model: {model}",
        f"- Reasoning: {route.get('reasoning_effort') or 'provider default'}; availability fallback: {route.get('fallback_model') or 'none'} (explicit selection only).",
        "- Recommendation only: check availability and the active session model; no automatic switch or launch.",
        f"- Conversation: {guidance.get('conversation', 'continue')} — {guidance.get('conversation_reason', 'Verify current state first.')}",
    ]
    lines.extend(f"- Reuse {stage}: {ref['path']} (hash checked at load)" for stage, ref in guidance.get("evidence", {}).items())
    lines.extend(f"- {rule}" for rule in EFFICIENCY_RULES)
    return "\n".join(lines)
