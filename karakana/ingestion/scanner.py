"""Conservative source scanner for ingestion."""

from __future__ import annotations

from pathlib import Path

from karakana.ingestion.sources import load_action_source, load_file_source, load_patch_review_source, load_proposal_source, load_trace_source


DEFAULT_DOC_FILES = ("README.md", "KARAKANA.md", "AGENTS.md")

MSC_PLATFORM_DOC_PATTERNS = (
    "docs/research/**/*.md",
    "docs/curriculum/**/*.md",
    "docs/evaluation/**/*.md",
    "docs/platform/vertical-slice-roadmap.md",
    "docs/platform/configurable-research-workflow-engine.md",
    "docs/platform/lims-workflow-patterns-review.md",
    "docs/adr/**/*.md",
    "PRODUCT.md",
    "RESEARCH-SCOPE.md",
    "ARCHITECTURE.md",
    "VERIFICATION.md",
)

BLOCKED_SCAN_PARTS = {".env", "secrets", "artifacts", "exports", "datasets"}


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
        if project == "msc-platform":
            for base_root, source_path in _msc_platform_doc_paths(repo_root, max_files=max_files):
                items.append(load_file_source(base_root, source_path, project=project, skillpack=skillpack))
                if len(items) >= max_files:
                    return items
        else:
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


def _msc_platform_doc_paths(repo_root: Path, max_files: int) -> list[tuple[Path, Path]]:
    project_root = repo_root.parent / "stemgen-platform"
    if not project_root.exists():
        return [(repo_root, path.relative_to(repo_root)) for path in _doc_paths(repo_root, max_files)]

    selected: list[Path] = []
    for pattern in MSC_PLATFORM_DOC_PATTERNS:
        selected.extend(sorted(path for path in project_root.glob(pattern) if path.is_file() and _safe_scan_path(path)))

    unique: list[Path] = []
    seen: set[Path] = set()
    for path in selected:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        unique.append(path)
        if len(unique) >= max_files:
            break
    return [(project_root, path.relative_to(project_root)) for path in unique]


def _safe_scan_path(path: Path) -> bool:
    parts = set(path.parts)
    if parts & BLOCKED_SCAN_PARTS:
        return False
    if path.name.startswith(".env"):
        return False
    if path.suffix.lower() not in {".md", ".json", ".yml", ".yaml"}:
        return False
    return True


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
