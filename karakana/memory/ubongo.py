"""Loader and validator for durable ubongo markdown memory."""

from __future__ import annotations

from pathlib import Path

from karakana.memory.schemas import MemoryFile, ProjectMemory

REQUIRED_PROJECT_FILES = [
    "overview.md",
    "architecture.md",
    "decisions.md",
    "deployment.md",
    "known-issues.md",
    "open-issues.md",
]

REQUIRED_GLOBAL_FILES = [
    "engineering-standards.md",
    "user-preferences.md",
    "security-principles.md",
    "prompt-patterns.md",
    "lessons-learned.md",
]


class UbongoMemory:
    """File-based access to Karakana durable memory."""

    def __init__(self, root: Path):
        self.root = root
        self.ubongo_root = root / "ubongo"
        self.global_root = self.ubongo_root / "global"
        self.projects_root = self.ubongo_root / "projects"

    def list_projects(self) -> list[str]:
        if not self.projects_root.exists():
            return []
        return sorted(path.name for path in self.projects_root.iterdir() if path.is_dir())

    def load_global_memory(self) -> dict[str, MemoryFile]:
        return self._load_files(self.global_root, REQUIRED_GLOBAL_FILES)

    def load_project_memory(self, project: str) -> dict[str, MemoryFile]:
        return self._load_files(self.projects_root / project, REQUIRED_PROJECT_FILES)

    def load_project_context(self, project: str) -> ProjectMemory:
        return ProjectMemory(
            project=project,
            global_memory=self.load_global_memory(),
            project_memory=self.load_project_memory(project),
        )

    def validate_project(self, project: str) -> list[str]:
        missing: list[str] = []
        project_root = self.projects_root / project
        for filename in REQUIRED_PROJECT_FILES:
            if not (project_root / filename).exists():
                missing.append(filename)
        return missing

    def summarize_project_context(self, project: str) -> str:
        return self.load_project_context(project).as_markdown()

    def _load_files(self, directory: Path, filenames: list[str]) -> dict[str, MemoryFile]:
        memory: dict[str, MemoryFile] = {}
        for filename in filenames:
            path = directory / filename
            if path.exists():
                content = path.read_text(encoding="utf-8")
                memory[filename] = MemoryFile(name=filename, path=path, content=content)
        return memory
