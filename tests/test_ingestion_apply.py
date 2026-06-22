from karakana.ingestion.apply import apply_ingestion_bundle
from karakana.ingestion.schemas import IngestionCandidate, IngestionSource
from karakana.ingestion.store import IngestionStore, create_bundle


def save_bundle(tmp_path, candidate):
    bundle = create_bundle("karakana", None, [IngestionSource(source_type="manual_note")], [candidate], False, [])
    IngestionStore(tmp_path).save(bundle)
    return bundle


def test_apply_is_dry_run_by_default(tmp_path):
    candidate = IngestionCandidate(candidate_id="candidate-1", candidate_type="ubongo_memory", title="Memory", summary="Summary", target_path="ubongo/projects/karakana/known-issues.md", proposed_content="New note", evidence=["note"])
    bundle = save_bundle(tmp_path, candidate)

    result, _ = apply_ingestion_bundle(tmp_path, bundle.ingest_id)

    assert result["dry_run"] is True
    assert not (tmp_path / "ubongo" / "projects" / "karakana" / "known-issues.md").exists()


def test_apply_with_write_creates_backup_and_refuses_blocked_paths(tmp_path):
    existing = tmp_path / "ubongo" / "projects" / "karakana" / "known-issues.md"
    existing.parent.mkdir(parents=True)
    existing.write_text("Old\n", encoding="utf-8")
    candidate = IngestionCandidate(candidate_id="candidate-1", candidate_type="ubongo_memory", title="Memory", summary="Summary", target_path="ubongo/projects/karakana/known-issues.md", proposed_content="New note", evidence=["note"])
    blocked = IngestionCandidate(candidate_id="candidate-2", candidate_type="safety_update", title="Blocked", summary="Summary", target_path="karakana/safety/model.py", proposed_content="New note", evidence=["note"])
    bundle = create_bundle("karakana", None, [IngestionSource(source_type="manual_note")], [candidate, blocked], False, [])
    IngestionStore(tmp_path).save(bundle)

    result, _ = apply_ingestion_bundle(tmp_path, bundle.ingest_id, write=True)

    assert "candidate-1" in result["applied_candidates"]
    assert "candidate-2" in result["blocked_candidates"]
    assert "New note" in existing.read_text(encoding="utf-8")
    assert result["backups"]


def test_high_risk_and_behavior_updates_require_overrides(tmp_path):
    high = IngestionCandidate(candidate_id="candidate-1", candidate_type="safety_update", title="High", summary="Summary", target_path="docs/safety.md", proposed_content="New note", risk_level="high", evidence=["note"])
    behavior = IngestionCandidate(candidate_id="candidate-2", candidate_type="behavior_update", title="Behavior", summary="Summary", target_path="ubongo/global/lessons-learned.md", proposed_content="New note", evidence=["note"])
    bundle = create_bundle("karakana", None, [IngestionSource(source_type="manual_note")], [high, behavior], False, [])
    IngestionStore(tmp_path).save(bundle)

    result, _ = apply_ingestion_bundle(tmp_path, bundle.ingest_id, write=True)

    assert set(result["blocked_candidates"]) == {"candidate-1", "candidate-2"}
