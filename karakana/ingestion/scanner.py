"""Conservative source scanner for ingestion."""

from __future__ import annotations

from pathlib import Path

from karakana.ingestion.sources import load_action_source, load_file_source, load_patch_review_source, load_proposal_source, load_trace_source


DEFAULT_DOC_FILES = ("README.md", "KARAKANA.md", "AGENTS.md")


def scan_sources(
    repo_root: Path,
    *,
    project: str | None = None,
    skillpack: str | None = None,
    includes: list[str] | None = None,
    max_files: int = 20,
) -> list[tuple]:
    """Scan only conservative documentation and Karakana artifact locations."""
    requested = set(includes or ["docs"])
    items: list[tuple] = []
    if "docs" in requested:
        for path in _doc_paths(repo_root, max_files=max_files):
            items.append(load_file_source(repo_root, path.relative_to(repo_root), project=project, skillpack=skillpack))
            if len(items) >= max_files:
                return items
    if "traces" in requested:
        items.extend(_latest_artifacts(repo_root / ".karakana" / "runs", "trace", load_trace_source, repo_root, project, skillpack, max_files - len(items)))
    if "actions" in requested:
        items.extend(_latest_artifacts(repo_root / ".karakana" / "actions", "action", load_action_source, repo_root, project, skillpack, max_files - len(items)))
    if "patch-reviews" in requested:
        items.extend(_latest_artifacts(repo_root / ".karakana" / "patch-reviews", "patch_review", load_patch_review_source, repo_root, project, skillpack, max_files - len(items)))
    if "proposals" in requested:
        items.extend(_latest_artifacts(repo_root / ".karakana" / "proposals", "proposal", load_proposal_source, repo_root, project, skillpack, max_files - len(items)))
    return items[:max_files]


def _doc_paths(repo_root: Path, max_files: int) -> list[Path]:
    paths = [repo_root / name for name in DEFAULT_DOC_FILES if (repo_root / name).exists()]
    docs = repo_root / "docs"
    if docs.exists():
        paths.extend(sorted(path for path in docs.rglob("*.md") if path.is_file()))
    return paths[:max_files]


def _latest_artifacts(root: Path, _kind: str, loader, repo_root: Path, project: str | None, skillpack: str | None, limit: int) -> list[tuple]:
    if limit <= 0 or not root.exists():
        return []
    items = []
    for path in sorted((item for item in root.iterdir() if item.is_dir()), key=lambda item: item.name, reverse=True)[:limit]:
        try:
            items.append(loader(repo_root, path.name, project=project, skillpack=skillpack))
        except Exception:
            continue
    return items
