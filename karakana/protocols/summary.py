"""Markdown summaries for deterministic work protocols."""

from __future__ import annotations

from karakana.protocols.schemas import WorkProtocol


def render_protocol_summary(protocol: WorkProtocol) -> str:
    lines = [
        f"# Protocol: {protocol.name}",
        "",
        f"- ID: {protocol.protocol_id}",
        f"- Version: {protocol.version}",
        f"- Category: {protocol.category}",
        f"- Risk floor: {protocol.risk_floor}",
        f"- Roles: {', '.join(protocol.roles)}",
        "",
        "## Summary",
        "",
        protocol.summary,
        "",
        "## Steps",
        "",
    ]
    lines.extend([f"- {step.step_id} ({step.action}): {step.instruction}" for step in protocol.steps])
    lines.extend(["", "## Always Required Artifacts", ""])
    lines.extend([f"- {artifact.kind}: {artifact.description}" for artifact in protocol.artifacts if not artifact.condition])
    lines.extend(["", "## Conditional Artifacts", ""])
    conditional = [artifact for artifact in protocol.artifacts if artifact.condition]
    if conditional:
        lines.extend([f"- {artifact.kind} when {artifact.condition}: {artifact.description}" for artifact in conditional])
    else:
        lines.append("- None")
    lines.extend(["", "## Verification", ""])
    lines.extend([f"- {item}" for item in protocol.verification] or ["- None"])
    lines.extend(["", "## Approval Gates", ""])
    lines.extend([f"- {gate}" for gate in protocol.approval_gates] or ["- None"])
    return "\n".join(lines)
