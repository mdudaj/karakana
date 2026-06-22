"""Render OKF validation results."""

from __future__ import annotations

from karakana.okf.schemas import OkfValidationResult


def render_validation_result(result: OkfValidationResult) -> str:
    lines = [
        f"OKF validation: {'passed' if result.ok else 'failed'}",
        f"Path: {result.path}",
        f"Concepts: {len(result.concepts)}",
    ]
    if result.counts_by_type:
        lines.append("Concepts by type:")
        for concept_type, count in sorted(result.counts_by_type.items()):
            lines.append(f"- {concept_type}: {count}")
    if result.counts_by_project:
        lines.append("Concepts by project:")
        for project, count in sorted(result.counts_by_project.items()):
            lines.append(f"- {project}: {count}")
    if result.errors:
        lines.append("Errors:")
        for issue in result.errors:
            lines.append(f"- {issue.path}: {issue.message}")
    if result.warnings:
        lines.append("Warnings:")
        for issue in result.warnings:
            lines.append(f"- {issue.path}: {issue.message}")
    return "\n".join(lines) + "\n"
