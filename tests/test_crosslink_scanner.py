from pathlib import Path

from karakana.crosslinks.scanner import scan_workspace


def test_crosslink_scanner_selects_projects_and_loads_skillpacks():
    bundle = scan_workspace(Path.cwd(), "nimr", project_ids=["billing", "lims"])

    assert bundle.workspace == "nimr"
    assert {project.project_id for project in bundle.projects} == {"billing", "lims"}
    assert {project.skillpack for project in bundle.projects} == {"billing", "lims"}
    assert bundle.patterns


def test_crosslink_scanner_defaults_to_conservative_sources():
    bundle = scan_workspace(Path.cwd(), "default")

    assert bundle.projects
    assert bundle.status == "ready_for_review"
    assert all(project.path for project in bundle.projects)

