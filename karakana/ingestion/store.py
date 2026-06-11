"""Storage for ingestion bundles."""

from __future__ import annotations

import json
import secrets
from datetime import datetime, timezone
from pathlib import Path

from karakana.ingestion.schemas import IngestionBundle
from karakana.ingestion.summary import render_candidates_markdown
from karakana.traces.schemas import now_utc


class IngestionStore:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.root = repo_root / ".karakana" / "ingestion"

    def save(self, bundle: IngestionBundle) -> Path:
        bundle_dir = self.bundle_dir(bundle.ingest_id)
        bundle_dir.mkdir(parents=True, exist_ok=True)
        for subdir in [
            "proposed-ubongo-updates",
            "proposed-skill-updates",
            "proposed-eval-updates",
            "proposed-prompt-updates",
            "proposed-safety-updates",
            "proposed-behavior-updates",
        ]:
            (bundle_dir / subdir).mkdir(exist_ok=True)
        (bundle_dir / "source.json").write_text(json.dumps([source.to_dict() for source in bundle.sources], indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (bundle_dir / "classification.json").write_text(json.dumps([candidate.classification.to_dict() if candidate.classification else {} for candidate in bundle.candidates], indent=2, sort_keys=True) + "\n", encoding="utf-8")
        candidates_path = bundle_dir / "candidates.json"
        candidates_path.write_text(json.dumps(bundle.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (bundle_dir / "candidates.md").write_text(render_candidates_markdown(bundle), encoding="utf-8")
        _write_candidate_files(bundle_dir, bundle)
        return candidates_path

    def load(self, ingest_id: str) -> IngestionBundle:
        path = self.bundle_dir(ingest_id) / "candidates.json"
        if not path.exists():
            raise FileNotFoundError(f"Ingestion bundle not found: {ingest_id}")
        return IngestionBundle.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def list(self, limit: int = 20) -> list[IngestionBundle]:
        if not self.root.exists():
            return []
        bundles = []
        for path in self.root.iterdir():
            candidate_json = path / "candidates.json"
            if candidate_json.exists():
                bundles.append(IngestionBundle.from_dict(json.loads(candidate_json.read_text(encoding="utf-8"))))
        return sorted(bundles, key=lambda bundle: bundle.created_at, reverse=True)[:limit]

    def bundle_dir(self, ingest_id: str) -> Path:
        return self.root / ingest_id


def create_bundle(project: str | None, skillpack: str | None, sources, candidates, redaction_applied: bool, warnings: list[str]) -> IngestionBundle:
    return IngestionBundle(
        ingest_id=generate_ingest_id(),
        project=project,
        skillpack=skillpack,
        status="ready_for_review",
        created_at=now_utc(),
        sources=sources,
        candidates=candidates,
        redaction_applied=redaction_applied,
        warnings=warnings,
        next_actions=["Review candidates.", "Run `karakana ingest review <ingest-id>`.", "Apply only with explicit --write."],
    )


def generate_ingest_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + f"-ingest-{secrets.token_hex(3)}"


def _write_candidate_files(bundle_dir: Path, bundle: IngestionBundle) -> None:
    mapping = {
        "ubongo_memory": "proposed-ubongo-updates",
        "skill_update": "proposed-skill-updates",
        "eval_update": "proposed-eval-updates",
        "prompt_update": "proposed-prompt-updates",
        "safety_update": "proposed-safety-updates",
        "behavior_update": "proposed-behavior-updates",
        "project_convention": "proposed-ubongo-updates",
    }
    for candidate in bundle.candidates:
        subdir = mapping.get(candidate.candidate_type)
        if not subdir:
            continue
        (bundle_dir / subdir / f"{candidate.candidate_id}.md").write_text(candidate.proposed_content or candidate.summary, encoding="utf-8")
