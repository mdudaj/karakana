from pathlib import Path

from karakana.crosslinks.reviewer import review_crosslink
from karakana.crosslinks.schemas import CrosslinkPattern, CrosslinkProjectRef, CrosslinkProposal
from karakana.crosslinks.store import CrosslinkStore, create_bundle


def test_crosslink_review_blocks_project_memory_copy(tmp_path: Path):
    store = CrosslinkStore(tmp_path)
    bundle = create_bundle(
        "nimr",
        [CrosslinkProjectRef(project_id="billing"), CrosslinkProjectRef(project_id="lims")],
        [
            CrosslinkPattern(
                pattern_id="pattern-1",
                pattern_type="shared_risk",
                title="Shared risk",
                summary="Risk evidence.",
                projects=["billing", "lims"],
            )
        ],
    )
    bundle.proposals = [
        CrosslinkProposal(
            proposal_id="proposal-1",
            proposal_type="project_specific_follow_up",
            title="Bad project write",
            summary="Should not write project memory.",
            target_path="ubongo/projects/billing/workflows.md",
            affected_projects=["billing"],
        )
    ]
    store.save(bundle)

    result, review_path = review_crosslink(tmp_path, bundle.crosslink_id)

    assert result["blocked"] is True
    assert review_path.exists()
    assert "ubongo/projects" in review_path.read_text(encoding="utf-8")

