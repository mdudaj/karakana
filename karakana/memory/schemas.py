"""Structured types for ubongo memory."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class MemoryFile:
    """A single markdown memory file loaded from disk."""

    name: str
    path: Path
    content: str


@dataclass(frozen=True)
class ProjectMemory:
    """Global and project memory for one Karakana project."""

    project: str
    global_memory: dict[str, MemoryFile]
    project_memory: dict[str, MemoryFile]

    def as_markdown(self) -> str:
        sections: list[str] = [f"# Ubongo Memory: {self.project}", ""]
        sections.append("## Global Memory")
        sections.extend(_render_files(self.global_memory))
        sections.append("## Project Memory")
        sections.extend(_render_files(self.project_memory))
        return "\n".join(sections).strip() + "\n"


def _render_files(files: dict[str, MemoryFile]) -> list[str]:
    lines: list[str] = []
    for name in sorted(files):
        memory_file = files[name]
        lines.append(f"### {name}")
        lines.append("")
        lines.append(memory_file.content.strip() or "_No content yet._")
        lines.append("")
    return lines
