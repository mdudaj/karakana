from karakana.ingestion.schemas import ClassificationResult, IngestionBundle, IngestionCandidate, IngestionSource


def test_ingestion_schema_round_trip():
    source = IngestionSource(source_type="file", path="README.md", project="karakana")
    classification = ClassificationResult(category="ubongo_memory", confidence=0.8, rationale="matched", suggested_targets=["ubongo/projects/karakana/known-issues.md"])
    candidate = IngestionCandidate(candidate_id="candidate-1", candidate_type="ubongo_memory", title="Memory", summary="Summary", classification=classification, target_path="ubongo/projects/karakana/known-issues.md")
    bundle = IngestionBundle(ingest_id="ingest", project="karakana", skillpack="karakana", status="ready_for_review", created_at="now", sources=[source], candidates=[candidate])

    loaded = IngestionBundle.from_dict(bundle.to_dict())

    assert loaded.sources[0].source_type == "file"
    assert loaded.candidates[0].classification.category == "ubongo_memory"
