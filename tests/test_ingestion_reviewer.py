from karakana.ingestion.reviewer import review_ingestion_bundle
from karakana.ingestion.schemas import IngestionCandidate, IngestionSource
from karakana.ingestion.store import IngestionStore, create_bundle


def test_review_blocks_unsafe_target_and_missing_evidence(tmp_path):
    candidate = IngestionCandidate(candidate_id="candidate-1", candidate_type="safety_update", title="Unsafe", summary="Unsafe", target_path="karakana/safety/model.py", proposed_content="note", risk_level="high", evidence=[])
    bundle = create_bundle("karakana", None, [IngestionSource(source_type="manual_note")], [candidate], False, [])
    IngestionStore(tmp_path).save(bundle)

    result, path = review_ingestion_bundle(tmp_path, bundle.ingest_id)

    assert result["blocked"] is True
    assert path.exists()
    assert "blocked" in path.read_text(encoding="utf-8").lower()
