"""Load ingestion sources without mutation."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from karakana.actions.store import ActionStore
from karakana.improvement.store import ProposalStore
from karakana.ingestion.redaction import mostly_secret, redact_text
from karakana.ingestion.schemas import IngestionSource
from karakana.traces.store import TraceStore
from karakana.traces.schemas import now_utc


def load_file_source(repo_root: Path, path: Path, project: str | None = None, skillpack: str | None = None, max_size: int = 200_000) -> tuple[IngestionSource, str, bool, list[str]]:
    file_path = path if path.is_absolute() else repo_root / path
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    data = file_path.read_bytes()
    if len(data) > max_size:
        raise ValueError(f"File exceeds max size: {path}")
    if b"\x00" in data:
        raise ValueError(f"Binary file rejected: {path}")
    text = data.decode("utf-8")
    if mostly_secret(text):
        raise ValueError("Source appears to be mostly secret material.")
    redacted, applied, warnings = redact_text(text)
    source = _source("file", str(path), str(path), project, skillpack, file_path.name, redacted)
    return source, redacted, applied, warnings


def load_trace_source(repo_root: Path, run_id: str, project: str | None = None, skillpack: str | None = None) -> tuple[IngestionSource, str, bool, list[str]]:
    trace = TraceStore(repo_root).load(run_id)
    text = json.dumps(trace.to_dict(), indent=2, sort_keys=True)
    redacted, applied, warnings = redact_text(text)
    return _source("trace", run_id, f".karakana/runs/{run_id}", project, skillpack, trace.command, redacted), redacted, applied, warnings


def load_action_source(repo_root: Path, action_run_id: str, project: str | None = None, skillpack: str | None = None) -> tuple[IngestionSource, str, bool, list[str]]:
    bundle = ActionStore(repo_root).load(action_run_id)
    text = json.dumps(bundle.to_dict(), indent=2, sort_keys=True)
    redacted, applied, warnings = redact_text(text)
    return _source("action", action_run_id, f".karakana/actions/{action_run_id}", project, skillpack, bundle.summary, redacted), redacted, applied, warnings


def load_patch_review_source(repo_root: Path, patch_review_id: str, project: str | None = None, skillpack: str | None = None) -> tuple[IngestionSource, str, bool, list[str]]:
    review_path = repo_root / ".karakana" / "patch-reviews" / patch_review_id / "review.json"
    if not review_path.exists():
        raise FileNotFoundError(f"Patch review not found: {patch_review_id}")
    text = review_path.read_text(encoding="utf-8")
    redacted, applied, warnings = redact_text(text)
    return _source("patch_review", patch_review_id, str(review_path), project, skillpack, "Patch review", redacted), redacted, applied, warnings


def load_proposal_source(repo_root: Path, proposal_id: str, project: str | None = None, skillpack: str | None = None) -> tuple[IngestionSource, str, bool, list[str]]:
    proposal = ProposalStore(repo_root).load(proposal_id)
    text = json.dumps(proposal.to_dict(), indent=2, sort_keys=True)
    redacted, applied, warnings = redact_text(text)
    return _source("proposal", proposal_id, f".karakana/proposals/{proposal_id}", project, skillpack, proposal.summary, redacted), redacted, applied, warnings


def load_codex_task_source(repo_root: Path, codex_task_id: str, project: str | None = None, skillpack: str | None = None) -> tuple[IngestionSource, str, bool, list[str]]:
    task_dir = repo_root / ".karakana" / "codex" / codex_task_id
    task_path = task_dir / "codex-task.md"
    if not task_path.exists():
        raise FileNotFoundError(f"Codex task not found: {codex_task_id}")
    text = task_path.read_text(encoding="utf-8")
    if mostly_secret(text):
        raise ValueError("Codex task appears to be mostly secret material.")
    redacted, applied, warnings = redact_text(text)
    return _source("codex_task", codex_task_id, str(task_path), project, skillpack, "Codex task", redacted), redacted, applied, warnings


def load_test_run_source(repo_root: Path, test_run_id: str, project: str | None = None, skillpack: str | None = None) -> tuple[IngestionSource, str, bool, list[str]]:
    test_dir = repo_root / ".karakana" / "test-runs" / test_run_id
    result_path = test_dir / "result.json"
    summary_path = test_dir / "summary.md"
    if result_path.exists():
        text = result_path.read_text(encoding="utf-8")
    elif summary_path.exists():
        text = summary_path.read_text(encoding="utf-8")
    else:
        raise FileNotFoundError(f"Test run not found: {test_run_id}")
    redacted, applied, warnings = redact_text(text)
    return _source("test_run", test_run_id, str(result_path if result_path.exists() else summary_path), project, skillpack, "Test run", redacted), redacted, applied, warnings


def load_note_source(text: str, project: str | None = None, skillpack: str | None = None) -> tuple[IngestionSource, str, bool, list[str]]:
    if mostly_secret(text):
        raise ValueError("Manual note appears to be mostly secret material.")
    redacted, applied, warnings = redact_text(text)
    return _source("manual_note", None, None, project, skillpack, "Manual note", redacted), redacted, applied, warnings


def _source(source_type: str, source_id: str | None, path: str | None, project: str | None, skillpack: str | None, title: str | None, content: str) -> IngestionSource:
    return IngestionSource(
        source_type=source_type,
        source_id=source_id,
        path=path,
        project=project,
        skillpack=skillpack,
        title=title,
        content_hash=hashlib.sha256(content.encode("utf-8")).hexdigest(),
        collected_at=now_utc(),
        metadata={"content_length": len(content)},
    )
