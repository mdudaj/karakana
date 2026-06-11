from pathlib import Path

from karakana.crosslinks.proposer import generate_proposals
from karakana.crosslinks.schemas import CrosslinkPattern, CrosslinkProjectRef
from karakana.crosslinks.store import CrosslinkStore, create_bundle


def test_crosslink_proposer_writes_proposal_artifacts(tmp_path: Path):
    store = CrosslinkStore(tmp_path)
    bundle = create_bundle(
        "nimr",
        [CrosslinkProjectRef(project_id="billing"), CrosslinkProjectRef(project_id="lims")],
        [
            CrosslinkPattern(
                pattern_id="pattern-1",
                pattern_type="shared_eval_need",
                title="Missing regression test",
                summary="Two projects need the same regression test.",
                projects=["billing", "lims"],
            ),
            CrosslinkPattern(
                pattern_id="pattern-2",
                pattern_type="shared_workflow",
                title="Shared workflow",
                summary="Reusable workflow guidance.",
                projects=["billing", "lims"],
                suggested_targets=["skills/django-debugging/SKILL.md"],
            ),
        ],
    )
    store.save(bundle)

    proposals, path = generate_proposals(tmp_path, bundle.crosslink_id)

    assert path.exists()
    assert {proposal.proposal_type for proposal in proposals} >= {"shared_eval_update", "shared_skill_update"}
    assert list((path.parent / "proposed-updates").rglob("proposal-*.md"))

