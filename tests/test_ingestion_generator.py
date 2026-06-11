from karakana.ingestion.generator import generate_candidates
from karakana.ingestion.schemas import IngestionSource


def test_candidate_target_path_generation():
    source = IngestionSource(source_type="manual_note", project="nhrdm", title="note")

    candidates = generate_candidates(source, "architecture decision command troubleshooting note", project="nhrdm")

    assert candidates[0].candidate_type == "ubongo_memory"
    assert candidates[0].target_path.startswith("ubongo/projects/nhrdm/")
    assert candidates[0].evidence
