from karakana.crosslinks.schemas import CrosslinkPattern, CrosslinkProjectRef
from karakana.crosslinks.store import create_bundle
from karakana.crosslinks.summary import render_crosslink


def test_crosslink_summary_includes_required_sections():
    bundle = create_bundle(
        "nimr",
        [CrosslinkProjectRef(project_id="billing")],
        [
            CrosslinkPattern(
                pattern_id="pattern-1",
                pattern_type="shared_workflow",
                title="Shared workflow",
                summary="Reusable workflow.",
                projects=["billing", "lims"],
            )
        ],
    )

    text = render_crosslink(bundle)

    assert "# Karakana Cross-Project Knowledge Link" in text
    assert "## Projects" in text
    assert "## Patterns" in text
    assert "## Boundary Review" in text

