import json

from karakana.actions.schemas import ActionBundle, ActionSource
from karakana.actions.store import ActionStore
from karakana.improvement.schemas import ImprovementProposal, ProposedChange
from karakana.improvement.store import ProposalStore
from karakana.ingestion.schemas import IngestionSource
from karakana.ingestion.store import IngestionStore, create_bundle
from karakana.requirements.sources import (
    load_action_requirement_source,
    load_file_requirement_source,
    load_ingest_requirement_source,
    load_note_requirement_source,
    load_patch_review_requirement_source,
    load_proposal_requirement_source,
)


def test_requirements_source_loading(tmp_path):
    action = ActionBundle(action_run_id="20260101-000000-actions-aaaaaa", status="ready_for_review", created_at="now", source=ActionSource(source_type="model_response"), summary="Action summary")
    ActionStore(tmp_path).save(action)
    source, content = load_action_requirement_source(tmp_path, action.action_run_id)
    assert source.source_type == "action"
    assert "Action summary" in content

    ingest = create_bundle("karakana", None, [IngestionSource(source_type="manual_note")], [], False, [])
    IngestionStore(tmp_path).save(ingest)
    source, content = load_ingest_requirement_source(tmp_path, ingest.ingest_id)
    assert source.source_type == "ingest"
    assert ingest.ingest_id in content

    review_dir = tmp_path / ".karakana" / "patch-reviews" / "review-1"
    review_dir.mkdir(parents=True)
    (review_dir / "review.json").write_text(json.dumps({"status": "warning"}), encoding="utf-8")
    source, content = load_patch_review_requirement_source(tmp_path, "review-1")
    assert source.source_type == "patch_review"
    assert "warning" in content

    proposal = ImprovementProposal(
        proposal_id="20260101-000000-improve-aaaaaa",
        project="karakana",
        status="ready_for_review",
        created_at="now",
        source_run_ids=["run"],
        summary="Proposal",
        changes=[ProposedChange(target_path="docs/x.md", change_type="doc_update", title="Doc", rationale="Because")],
    )
    ProposalStore(tmp_path).save(proposal)
    source, content = load_proposal_requirement_source(tmp_path, proposal.proposal_id)
    assert source.source_type == "proposal"
    assert "Proposal" in content

    (tmp_path / "README.md").write_text("Add requirements CLI", encoding="utf-8")
    source, content = load_file_requirement_source(tmp_path, tmp_path / "README.md")
    assert source.source_type == "file"
    assert "requirements CLI" in content

    source, content = load_note_requirement_source("Add a safe requirements layer")
    assert source.source_type == "note"
    assert "requirements layer" in content
