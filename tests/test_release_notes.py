from pathlib import Path

from karakana.release.notes import generate_release_notes


def test_release_notes_generation():
    notes_id, path = generate_release_notes(Path.cwd(), version="0.1.0")

    assert notes_id
    text = path.read_text(encoding="utf-8")
    assert "# Karakana Release Notes" in text
    assert "## Safety" in text
    assert "No publishing" in text

