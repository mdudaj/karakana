from karakana.ingestion.generator import generate_candidates
from karakana.ingestion.schemas import IngestionSource
from karakana.ingestion.store import IngestionStore, create_bundle


def test_ingestion_store_writes_artifacts(tmp_path):
    source = IngestionSource(source_type="manual_note", project="karakana", title="Note")
    candidates = generate_candidates(source, "architecture decision command", project="karakana")
    bundle = create_bundle("karakana", None, [source], candidates, False, [])

    path = IngestionStore(tmp_path).save(bundle)

    assert path.exists()
    assert (path.parent / "source.json").exists()
    assert (path.parent / "classification.json").exists()
    assert (path.parent / "candidates.md").exists()
    assert IngestionStore(tmp_path).load(bundle.ingest_id).ingest_id == bundle.ingest_id
