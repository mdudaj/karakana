from pathlib import Path

from karakana.dogfood.checklist import generate_checklist


def test_dogfood_checklist_generation_includes_core_workflows(tmp_path: Path):
    dogfood_id, path = generate_checklist(tmp_path, "karakana", "karakana")
    text = path.read_text(encoding="utf-8")

    assert dogfood_id
    assert "`karakana doctor`" in text
    assert "## Requirements Workflow" in text
    assert "## Action / Codex Workflow" in text
    assert "## Learning Workflow" in text
    assert "`karakana release check --full`" in text

