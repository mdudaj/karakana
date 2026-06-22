from pathlib import Path

from karakana.crosslinks.apply import apply_crosslink
from karakana.crosslinks.schemas import CrosslinkPattern, CrosslinkProjectRef, CrosslinkProposal
from karakana.crosslinks.store import CrosslinkStore, create_bundle


def _bundle_with_proposals(tmp_path: Path, proposals: list[CrosslinkProposal]):
    store = CrosslinkStore(tmp_path)
    bundle = create_bundle(
        "nimr",
        [CrosslinkProjectRef(project_id="billing"), CrosslinkProjectRef(project_id="lims")],
        [
            CrosslinkPattern(
                pattern_id="pattern-1",
                pattern_type="shared_project_convention",
                title="Shared convention",
                summary="A reusable convention.",
                projects=["billing", "lims"],
            )
        ],
    )
    bundle.proposals = proposals
    store.save(bundle)
    return bundle


def test_crosslink_apply_is_dry_run_by_default(tmp_path: Path):
    bundle = _bundle_with_proposals(
        tmp_path,
        [
            CrosslinkProposal(
                proposal_id="proposal-1",
                proposal_type="global_ubongo_update",
                title="Global note",
                summary="Dry run note.",
                target_path="ubongo/global/lessons-learned.md",
                proposed_content="Reusable lesson.",
                affected_projects=["billing", "lims"],
            )
        ],
    )

    result, path = apply_crosslink(tmp_path, bundle.crosslink_id)

    assert result["dry_run"] is True
    assert result["applied_proposals"] == []
    assert not (tmp_path / "ubongo/global/lessons-learned.md").exists()
    assert path.exists()


def test_crosslink_apply_blocks_project_ubongo_writes(tmp_path: Path):
    bundle = _bundle_with_proposals(
        tmp_path,
        [
            CrosslinkProposal(
                proposal_id="proposal-1",
                proposal_type="project_specific_follow_up",
                title="Project note",
                summary="Project memory should not be written.",
                target_path="ubongo/projects/billing/workflows.md",
                proposed_content="Project-specific note.",
                affected_projects=["billing"],
            )
        ],
    )

    result, _ = apply_crosslink(tmp_path, bundle.crosslink_id, write=True)

    assert result["status"] in {"blocked", "partial"}
    assert result["blocked_proposals"] == ["proposal-1"]
    assert not (tmp_path / "ubongo/projects/billing/workflows.md").exists()


def test_crosslink_apply_high_risk_requires_override(tmp_path: Path):
    bundle = _bundle_with_proposals(
        tmp_path,
        [
            CrosslinkProposal(
                proposal_id="proposal-1",
                proposal_type="global_ubongo_update",
                title="High risk",
                summary="High-risk shared rule.",
                target_path="ubongo/global/engineering-standards.md",
                proposed_content="Payment changes require review.",
                affected_projects=["billing", "nhrdm"],
                risk_level="high",
            )
        ],
    )

    result, _ = apply_crosslink(tmp_path, bundle.crosslink_id, write=True)

    assert result["blocked_proposals"] == ["proposal-1"]

