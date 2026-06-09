from karakana.improvement.schemas import ImprovementProposal, ProposedChange
from karakana.improvement.store import ProposalStore


def proposal(proposal_id: str) -> ImprovementProposal:
    return ImprovementProposal(
        proposal_id=proposal_id,
        project="karakana",
        status="ready_for_review",
        created_at=proposal_id,
        source_run_ids=["run"],
        summary="Summary",
        changes=[ProposedChange(target_path="README.md", change_type="doc_update", title="Doc", rationale="Because")],
    )


def test_save_load_list_latest(tmp_path):
    store = ProposalStore(tmp_path)
    first = proposal("20260101-000000-improve-aaaaaa")
    second = proposal("20260102-000000-improve-bbbbbb")

    path = store.save(first)
    store.save(second)

    assert path == tmp_path / ".karakana" / "proposals" / first.proposal_id / "proposal.json"
    assert store.load(first.proposal_id).proposal_id == first.proposal_id
    assert store.list_proposals()[0].proposal_id == second.proposal_id
    assert store.latest().proposal_id == second.proposal_id
    assert (tmp_path / ".karakana" / "proposals" / first.proposal_id / "proposal.md").exists()
