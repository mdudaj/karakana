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


def test_msc_platform_dogfood_checklist_is_project_specific(tmp_path: Path):
    dogfood_id, path = generate_checklist(tmp_path, "msc-platform", "msc-platform")
    text = path.read_text(encoding="utf-8")

    assert dogfood_id
    assert "# msc-platform Dogfood Checklist" in text
    assert "## Curriculum-Data Readiness" in text
    assert "## Automated Review Safety" in text
    assert "## Slice 1 Readiness" in text
