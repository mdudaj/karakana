"""Produce and attach protocol artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from karakana.protocols.checks import check_trace_protocol_artifacts
from karakana.traces.schemas import TraceArtifact
from karakana.traces.store import TraceStore

TEMPLATE_FILES = {
    "acceptance_criteria": "acceptance-criteria.md",
    "adr": "adr.md",
    "definition_of_done": "definition-of-done.md",
    "migration_plan": "migration-plan.md",
    "requirements_note": "requirements-note.md",
    "rollback_plan": "rollback-plan.md",
    "safety_review": "safety-review.md",
    "schema_contract": "schema-contract.md",
    "threat_or_abuse_case_note": "threat-or-abuse-case-note.md",
    "user_story": "user-story.md",
    "ux_description": "ux-description.md",
    "verification_summary": "verification-summary.md",
}


@dataclass(frozen=True)
class MissingArtifactSuggestion:
    artifact_kind: str
    template_command: str | None
    attach_command: str


def list_template_kinds(repo_root: Path) -> list[str]:
    return sorted(kind for kind in TEMPLATE_FILES if template_path(repo_root, kind).exists())


def template_path(repo_root: Path, artifact_kind: str) -> Path:
    filename = TEMPLATE_FILES.get(artifact_kind, artifact_kind.replace("_", "-") + ".md")
    return repo_root / "templates" / "protocols" / filename


def render_template(repo_root: Path, artifact_kind: str) -> str:
    path = template_path(repo_root, artifact_kind)
    if not path.exists():
        raise FileNotFoundError(f"Protocol artifact template not found for: {artifact_kind}")
    return path.read_text(encoding="utf-8")


def write_template(repo_root: Path, artifact_kind: str, output: Path, *, overwrite: bool = False) -> Path:
    target = output if output.is_absolute() else repo_root / output
    if target.exists() and not overwrite:
        raise FileExistsError(f"Refusing to overwrite existing file: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_template(repo_root, artifact_kind), encoding="utf-8")
    return target


def attach_artifact_to_trace(repo_root: Path, trace_id: str, artifact_kind: str, path: Path, description: str | None = None):
    store = TraceStore(repo_root)
    trace = store.load(trace_id)
    artifact_path = path if path.is_absolute() else repo_root / path
    if not artifact_path.exists():
        raise FileNotFoundError(f"Artifact path not found: {artifact_path}")
    trace.artifacts.append(
        TraceArtifact(
            path=str(artifact_path),
            kind=artifact_kind,
            description=description or f"Protocol artifact: {artifact_kind}",
        )
    )
    store.save(trace)
    return trace


def missing_artifact_suggestions(repo_root: Path, trace_id: str) -> list[MissingArtifactSuggestion]:
    trace = TraceStore(repo_root).load(trace_id)
    result = check_trace_protocol_artifacts(repo_root, trace)
    suggestions = []
    for artifact_kind in result.missing_artifacts:
        template_command = None
        if template_path(repo_root, artifact_kind).exists():
            template_command = f"karakana protocol template {artifact_kind} --output <path>"
        suggestions.append(
            MissingArtifactSuggestion(
                artifact_kind=artifact_kind,
                template_command=template_command,
                attach_command=f"karakana protocol attach --trace {trace_id} --kind {artifact_kind} --path <path>",
            )
        )
    return suggestions
