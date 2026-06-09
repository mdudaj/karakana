"""Report rendering and storage for model response reviews."""

from __future__ import annotations

import json
from pathlib import Path

from karakana.models.review.schemas import ResponseReview


def write_review_artifacts(review: ResponseReview, output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "response-review.json"
    markdown_path = output_dir / "response-review.md"
    json_path.write_text(json.dumps(review.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(render_review_markdown(review), encoding="utf-8")
    return json_path, markdown_path


def render_review_markdown(review: ResponseReview) -> str:
    lines = [
        "# Karakana Model Response Review",
        "",
        "## Summary",
        "",
        f"- Status: {review.status}",
        f"- Blocked: {review.blocked}",
        f"- Requires human review: {review.requires_human_review}",
        "",
        "## Findings",
        "",
    ]
    if review.findings:
        for finding in review.findings:
            lines.extend(
                [
                    f"- {finding.finding_type} ({finding.severity}): {finding.message}",
                    f"  Evidence: {finding.evidence or ''}",
                ]
            )
    else:
        lines.append("- None")
    lines.extend(["", "## Warnings", ""])
    if review.warnings:
        lines.extend(f"- {warning}" for warning in review.warnings)
    else:
        lines.append("- None")
    return "\n".join(lines).rstrip() + "\n"
