from karakana.improvement.schemas import EvidenceRef, ImprovementProposal, ProposedChange
from karakana.improvement.summary import render_proposal_markdown


def test_render_proposal_markdown():
    proposal = ImprovementProposal(
        proposal_id="proposal",
        project="karakana",
        status="ready_for_review",
        created_at="now",
        source_run_ids=["run"],
        summary="Summary",
        changes=[
            ProposedChange(
                target_path="README.md",
                change_type="doc_update",
                title="Document warning",
                rationale="A warning was observed.",
                proposed_content="Add a note.",
                evidence=[EvidenceRef(run_id="run", summary="warning")],
            )
        ],
    )

    markdown = render_proposal_markdown(proposal)

    assert "# Karakana Self-Improvement Proposal" in markdown
    assert "### Change 1: Document warning" in markdown
    assert "Run `run`" in markdown
    assert "Add a note." in markdown
