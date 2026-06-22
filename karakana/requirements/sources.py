"""Load selected sources for requirement generation."""

from __future__ import annotations

import json
from pathlib import Path

from karakana.actions.store import ActionStore
from karakana.improvement.store import ProposalStore
from karakana.ingestion.redaction import mostly_secret, redact_text
from karakana.ingestion.store import IngestionStore
from karakana.requirements.schemas import RequirementSource


MAX_SOURCE_CHARS = 12_000


def load_action_requirement_source(repo_root: Path, action_run_id: str, project: str | None = None, skillpack: str | None = None) -> tuple[RequirementSource, str]:
    bundle = ActionStore(repo_root).load(action_run_id)
    text = json.dumps(bundle.to_dict(), indent=2, sort_keys=True)
    return _source("action", action_run_id, f".karakana/actions/{action_run_id}", project, skillpack, bundle.summary, text)


def load_ingest_requirement_source(repo_root: Path, ingest_id: str, project: str | None = None, skillpack: str | None = None) -> tuple[RequirementSource, str]:
    bundle = IngestionStore(repo_root).load(ingest_id)
    text = json.dumps(bundle.to_dict(), indent=2, sort_keys=True)
    return _source("ingest", ingest_id, f".karakana/ingestion/{ingest_id}", project or bundle.project, skillpack or bundle.skillpack, "Ingestion bundle", text)


def load_patch_review_requirement_source(repo_root: Path, patch_review_id: str, project: str | None = None, skillpack: str | None = None) -> tuple[RequirementSource, str]:
    path = repo_root / ".karakana" / "patch-reviews" / patch_review_id / "review.json"
    if not path.exists():
        raise FileNotFoundError(f"Patch review not found: {patch_review_id}")
    return _source("patch_review", patch_review_id, str(path), project, skillpack, "Patch review", path.read_text(encoding="utf-8"))


def load_proposal_requirement_source(repo_root: Path, proposal_id: str, project: str | None = None, skillpack: str | None = None) -> tuple[RequirementSource, str]:
    proposal = ProposalStore(repo_root).load(proposal_id)
    text = json.dumps(proposal.to_dict(), indent=2, sort_keys=True)
    return _source("proposal", proposal_id, f".karakana/proposals/{proposal_id}", project or proposal.project, skillpack, proposal.summary, text)


def load_file_requirement_source(repo_root: Path, path: Path, project: str | None = None, skillpack: str | None = None) -> tuple[RequirementSource, str]:
    file_path = path if path.is_absolute() else repo_root / path
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    data = file_path.read_bytes()
    if b"\x00" in data:
        raise ValueError(f"Binary file rejected: {path}")
    text = data.decode("utf-8")
    return _source("file", str(path), str(path), project, skillpack, file_path.name, text)


def load_note_requirement_source(text: str, project: str | None = None, skillpack: str | None = None) -> tuple[RequirementSource, str]:
    return _source("note", None, None, project, skillpack, "Manual note", text)


def load_handoff_requirement_source(repo_root: Path, path: Path, project: str | None = None, skillpack: str | None = None) -> tuple[RequirementSource, str]:
    handoff = path if path.is_absolute() else repo_root / path
    if not handoff.exists():
        raise FileNotFoundError(f"Handoff file not found: {path}")
    return _source("handoff", str(path), str(path), project, skillpack, handoff.name, handoff.read_text(encoding="utf-8"))


def _source(source_type: str, source_id: str | None, path: str | None, project: str | None, skillpack: str | None, title: str | None, text: str) -> tuple[RequirementSource, str]:
    if mostly_secret(text):
        raise ValueError("Requirement source appears to be mostly secret material.")
    redacted, applied, warnings = redact_text(text)
    content = redacted[:MAX_SOURCE_CHARS]
    source = RequirementSource(
        source_type=source_type,
        source_id=source_id,
        path=path,
        project=project,
        skillpack=skillpack,
        title=title,
        metadata={"content_length": len(text), "truncated": len(redacted) > MAX_SOURCE_CHARS, "redaction_applied": applied, "warnings": warnings},
    )
    return source, content
