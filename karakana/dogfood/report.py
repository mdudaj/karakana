"""Dogfood report generation."""

from __future__ import annotations

from pathlib import Path

from karakana.dogfood.summary import DogfoodStore, render_dogfood_report


def generate_report(repo_root: Path, dogfood_id: str) -> Path:
    store = DogfoodStore(repo_root)
    run = store.load(dogfood_id)
    path = store.run_dir(dogfood_id) / "dogfood.md"
    path.write_text(render_dogfood_report(run), encoding="utf-8")
    return path
