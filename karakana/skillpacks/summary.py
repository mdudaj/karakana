"""Render skillpack summaries."""

from __future__ import annotations

from dataclasses import asdict

from karakana.skillpacks.schemas import Skillpack


def render_skillpack_summary(skillpack: Skillpack) -> str:
    return f"""# Karakana Skillpack Summary

## Skillpack

- Name: {skillpack.name}
- Description: {skillpack.description}
- Status: {skillpack.status}
- Project: {skillpack.project.id}

## Required Skills

{_bullets(skillpack.skills.required)}

## Optional Skills

{_bullets(skillpack.skills.optional)}

## Project Memory

{skillpack.project.memory or ""}

## Model Routes

{_routes(skillpack)}

## Safety

### High-Risk Paths

{_bullets(skillpack.safety.high_risk_paths)}

### Blocked Paths

{_bullets(skillpack.safety.blocked_paths)}

### Approval Requirements

{_bullets(skillpack.safety.requires_approval_for)}

## Recommended Tests

{_bullets(skillpack.tests.commands + skillpack.tests.recommended_before_commit)}

## Conventions

{_bullets(skillpack.conventions.notes)}
"""


def _routes(skillpack: Skillpack) -> str:
    if not skillpack.model_routes:
        return "- None"
    lines = []
    for task_type, route in sorted(skillpack.model_routes.items()):
        data = asdict(route)
        lines.append(f"- `{task_type}`: {data['provider']} / {data['model']}" + (f" - {data['rationale']}" if data.get("rationale") else ""))
    return "\n".join(lines)


def _bullets(values: list[str]) -> str:
    if not values:
        return "- None"
    return "\n".join(f"- {value}" for value in values)
