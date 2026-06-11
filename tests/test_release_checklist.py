from pathlib import Path

from karakana.release.checklist import write_release_checklist


def test_release_checklist_generation():
    _, path = write_release_checklist(Path.cwd())

    text = path.read_text(encoding="utf-8")
    assert "# Karakana Release Checklist" in text
    assert "`karakana doctor`" in text
    assert "Tag manually" in text

