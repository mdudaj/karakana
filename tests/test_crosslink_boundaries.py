from karakana.crosslinks.boundaries import validate_crosslink_target, validate_proposal_boundary
from karakana.crosslinks.schemas import CrosslinkProposal


def test_boundary_blocks_project_ubongo_and_source_paths():
    assert validate_crosslink_target("ubongo/projects/nhrdm/workflows.md")
    assert validate_crosslink_target("karakana/safety/model.py")
    assert validate_crosslink_target(".github/workflows/ci.yml")
    assert validate_crosslink_target(".env")


def test_global_ubongo_requires_multiple_projects():
    proposal = CrosslinkProposal(
        proposal_id="proposal-1",
        proposal_type="global_ubongo_update",
        title="Global update",
        summary="Needs qualification.",
        target_path="ubongo/global/lessons-learned.md",
        affected_projects=["billing"],
    )

    warnings = validate_proposal_boundary(proposal)

    assert any("at least two projects" in warning for warning in warnings)

