from pathlib import Path

from karakana.memory.retrieval import search_project_memory
from karakana.memory.ubongo import REQUIRED_GLOBAL_FILES, REQUIRED_PROJECT_FILES, UbongoMemory


def write_memory_tree(root: Path, project: str = "karakana") -> None:
    global_root = root / "ubongo" / "global"
    project_root = root / "ubongo" / "projects" / project
    global_root.mkdir(parents=True, exist_ok=True)
    project_root.mkdir(parents=True, exist_ok=True)
    for filename in REQUIRED_GLOBAL_FILES:
        (global_root / filename).write_text(f"# {filename}\n\nGlobal guidance.\n", encoding="utf-8")
    for filename in REQUIRED_PROJECT_FILES:
        (project_root / filename).write_text(f"# {filename}\n\nProject workshop context.\n", encoding="utf-8")


def test_list_projects(tmp_path):
    write_memory_tree(tmp_path, "karakana")
    write_memory_tree(tmp_path, "billing")

    memory = UbongoMemory(tmp_path)

    assert memory.list_projects() == ["billing", "karakana"]


def test_load_global_memory(tmp_path):
    write_memory_tree(tmp_path)

    memory = UbongoMemory(tmp_path).load_global_memory()

    assert sorted(memory) == sorted(REQUIRED_GLOBAL_FILES)
    assert memory["engineering-standards.md"].content.startswith("# engineering-standards.md")


def test_load_project_memory(tmp_path):
    write_memory_tree(tmp_path)

    memory = UbongoMemory(tmp_path).load_project_memory("karakana")

    assert sorted(memory) == sorted(REQUIRED_PROJECT_FILES)
    assert "Project workshop context" in memory["overview.md"].content


def test_validate_project_reports_missing_files(tmp_path):
    write_memory_tree(tmp_path)
    (tmp_path / "ubongo" / "projects" / "karakana" / "deployment.md").unlink()

    missing = UbongoMemory(tmp_path).validate_project("karakana")

    assert missing == ["deployment.md"]


def test_summarize_and_search_project_context(tmp_path):
    write_memory_tree(tmp_path)

    memory = UbongoMemory(tmp_path)
    context = memory.load_project_context("karakana")
    summary = memory.summarize_project_context("karakana")

    assert "# Ubongo Memory: karakana" in summary
    assert "## Global Memory" in summary
    assert "## Project Memory" in summary
    assert "overview.md" in search_project_memory(context, "workshop")
