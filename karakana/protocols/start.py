"""Protocol-aware task start artifacts."""

from __future__ import annotations

import json
import secrets
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from karakana.protocols.artifacts import MissingArtifactSuggestion, template_path
from karakana.protocols.classifier import ProtocolClassification
from karakana.protocols.loader import ProtocolLoader
from karakana.traces.schemas import redact_value


@dataclass
class ProtocolStartArtifact:
    start_id: str
    task: str
    classification: ProtocolClassification
    required_artifacts: list[str] = field(default_factory=list)
    missing_artifacts: list[str] = field(default_factory=list)
    template_suggestions: list[MissingArtifactSuggestion] = field(default_factory=list)
    approval_gates: list[str] = field(default_factory=list)
    verification: list[str] = field(default_factory=list)
    source: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return redact_value(asdict(self))


class ProtocolStartStore:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.root = repo_root / ".karakana" / "protocol-starts"

    def save(self, artifact: ProtocolStartArtifact) -> Path:
        start_dir = self.root / artifact.start_id
        start_dir.mkdir(parents=True, exist_ok=True)
        path = start_dir / "start.json"
        path.write_text(json.dumps(artifact.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (start_dir / "start.md").write_text(render_protocol_start(artifact), encoding="utf-8")
        (self.root / "latest").write_text(artifact.start_id + "\n", encoding="utf-8")
        return path


def build_protocol_start(repo_root: Path, classification: ProtocolClassification, *, source: dict[str, Any] | None = None) -> ProtocolStartArtifact:
    protocol = ProtocolLoader(repo_root).load(classification.protocol_id)
    suggestions = []
    for artifact_kind in classification.required_artifacts:
        path = template_path(repo_root, artifact_kind)
        template_command = f"karakana protocol template {artifact_kind} --output <path>" if path.exists() else None
        suggestions.append(
            MissingArtifactSuggestion(
                artifact_kind=artifact_kind,
                template_command=template_command,
                attach_command=f"karakana protocol attach --trace <trace-id> --kind {artifact_kind} --path <path>",
            )
        )
    return ProtocolStartArtifact(
        start_id=generate_protocol_start_id(),
        task=classification.task,
        classification=classification,
        required_artifacts=list(classification.required_artifacts),
        missing_artifacts=[artifact for artifact in classification.required_artifacts if artifact != "trace"],
        template_suggestions=suggestions,
        approval_gates=list(protocol.approval_gates),
        verification=list(protocol.verification),
        source=source or {},
    )


def render_protocol_start(artifact: ProtocolStartArtifact) -> str:
    classification = artifact.classification
    return f"""# Karakana Protocol Start

## Summary

- Start ID: {artifact.start_id}
- Protocol: {classification.protocol_id}
- Category: {classification.work_category}
- Risk: {classification.risk_level}
- Project: {classification.project or ""}
- Skillpack: {classification.skillpack or ""}

## Task

{artifact.task}

## Required Artifacts

{_bullets(artifact.required_artifacts)}

## Missing Artifacts

{_bullets(artifact.missing_artifacts)}

## Template / Attach Commands

{_suggestions(artifact.template_suggestions)}

## Approval Gates

{_bullets(artifact.approval_gates)}

## Verification

{_bullets(artifact.verification)}

## Rationale

{_bullets(classification.rationale)}
"""


def generate_protocol_start_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + f"-protocol-start-{secrets.token_hex(3)}"


def _suggestions(suggestions: list[MissingArtifactSuggestion]) -> str:
    if not suggestions:
        return "- None"
    lines = []
    for suggestion in suggestions:
        lines.append(f"- {suggestion.artifact_kind}")
        if suggestion.template_command:
            lines.append(f"  - template: `{suggestion.template_command}`")
        lines.append(f"  - attach: `{suggestion.attach_command}`")
    return "\n".join(lines)


def _bullets(values: list[str]) -> str:
    if not values:
        return "- None"
    return "\n".join(f"- {value}" for value in values)
