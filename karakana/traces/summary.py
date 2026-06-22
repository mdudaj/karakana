"""Markdown summaries for Karakana run traces."""

from __future__ import annotations

import json

from karakana.traces.schemas import RunTrace


def render_summary(trace: RunTrace) -> str:
    lines: list[str] = [
        "# Karakana Run Summary",
        "",
        "## Run",
        "",
        f"- Run ID: {trace.run_id}",
        f"- Status: {trace.status}",
        f"- Command: {trace.command}",
        f"- Project: {trace.project or ''}",
        f"- Skill: {trace.skill or ''}",
        f"- Task type: {trace.task_type or ''}",
        f"- Selected model: {trace.selected_model or ''}",
        f"- Started: {trace.started_at}",
        f"- Finished: {trace.finished_at or ''}",
        "",
        "## Task",
        "",
        trace.task or "",
        "",
        "## Inputs",
        "",
        _json_block(trace.inputs),
        "",
        "## Outputs",
        "",
        _json_block(trace.outputs),
        "",
        "## Artifacts",
        "",
        *_artifact_lines(trace),
        "",
        "## Safety Checks",
        "",
        *_safety_lines(trace),
        "",
        "## Warnings",
        "",
        *_list_lines(trace.warnings),
        "",
        "## Errors",
        "",
        *_list_lines(trace.errors),
        "",
        "## Next Actions",
        "",
        *_list_lines(trace.next_actions),
        "",
    ]
    return "\n".join(lines)


def _json_block(value: dict) -> str:
    return "```json\n" + json.dumps(value, indent=2, sort_keys=True) + "\n```"


def _artifact_lines(trace: RunTrace) -> list[str]:
    if not trace.artifacts:
        return ["- None"]
    return [
        f"- `{artifact.path}` ({artifact.kind})"
        + (f": {artifact.description}" if artifact.description else "")
        for artifact in trace.artifacts
    ]


def _safety_lines(trace: RunTrace) -> list[str]:
    if not trace.safety_checks:
        return ["- None"]
    return [
        f"- {check.name}: {check.status}" + (f" - {check.message}" if check.message else "")
        for check in trace.safety_checks
    ]


def _list_lines(values: list[str]) -> list[str]:
    if not values:
        return ["- None"]
    return [f"- {value}" for value in values]
