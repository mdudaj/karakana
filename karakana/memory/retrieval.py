"""Simple file-based text retrieval for ubongo memory."""

from __future__ import annotations

from karakana.memory.schemas import ProjectMemory


def search_project_memory(memory: ProjectMemory, query: str) -> list[str]:
    """Return memory file names whose content contains at least one query term."""
    terms = [term.lower() for term in query.split() if term.strip()]
    if not terms:
        return []

    matches: list[str] = []
    all_files = {**memory.global_memory, **memory.project_memory}
    for name, memory_file in all_files.items():
        content = memory_file.content.lower()
        if any(term in content for term in terms):
            matches.append(name)
    return sorted(matches)
