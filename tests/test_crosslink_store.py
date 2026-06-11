from pathlib import Path

from karakana.crosslinks.schemas import CrosslinkPattern, CrosslinkProjectRef
from karakana.crosslinks.store import CrosslinkStore, create_bundle


def test_crosslink_store_save_load_list_latest(tmp_path: Path):
    store = CrosslinkStore(tmp_path)
    bundle = create_bundle(
        "nimr",
        [CrosslinkProjectRef(project_id="billing"), CrosslinkProjectRef(project_id="lims")],
        [
            CrosslinkPattern(
                pattern_id="pattern-1",
                pattern_type="shared_workflow",
                title="Shared Django",
                summary="Projects share Django.",
                projects=["billing", "lims"],
            )
        ],
    )

    path = store.save(bundle)
    loaded = store.load(bundle.crosslink_id)

    assert path.exists()
    assert loaded.crosslink_id == bundle.crosslink_id
    assert store.list()[0].crosslink_id == bundle.crosslink_id
    assert store.latest().crosslink_id == bundle.crosslink_id
    assert (path.parent / "crosslink.md").exists()

