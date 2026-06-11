from pathlib import Path

from karakana.dogfood.backlog import generate_backlog
from karakana.dogfood.schemas import DogfoodFinding
from karakana.dogfood.summary import DogfoodStore, new_dogfood_run


def test_dogfood_backlog_prioritizes_release_blockers(tmp_path: Path):
    run = new_dogfood_run("karakana", "karakana")
    run.findings = [DogfoodFinding(finding_id="f1", finding_type="broken_command", title="Doctor failed", summary="Core workflow failed.", severity="high")]
    DogfoodStore(tmp_path).save(run)

    items, path = generate_backlog(tmp_path, run.dogfood_id)

    assert path.exists()
    assert items[0].priority == "p0"
    assert items[0].item_type == "bug"

