import re

from karakana.improvement.schemas import ImprovementProposal, ProposedChange
from karakana.improvement.store import generate_proposal_id


def test_proposal_id_generation_shape():
    assert re.match(r"^\d{8}-\d{6}-improve-[0-9a-f]{6}$", generate_proposal_id())


def test_proposal_serialization_redacts_secret_content():
    proposal = ImprovementProposal(
        proposal_id="p",
        project="karakana",
        status="ready_for_review",
        created_at="now",
        source_run_ids=["run"],
        summary="Summary",
        changes=[
            ProposedChange(
                target_path="README.md",
                change_type="doc_update",
                title="Document",
                rationale="Because",
                proposed_content={"client_secret": "value"},
            )
        ],
    )

    data = proposal.to_dict()

    assert data["changes"][0]["proposed_content"]["client_secret"] == "[REDACTED]"


def test_invalid_change_type_fails():
    try:
        ProposedChange(target_path="x", change_type="bad", title="t", rationale="r")
    except ValueError as exc:
        assert "Invalid change type" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
