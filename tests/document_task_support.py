"""Synthetic setup only; no model output, approval or real runtime imported."""

from pathlib import Path
import json

from tests.test_planner import write_memory_tree, write_skill

FIXTURES = Path(__file__).parent / "fixtures/document_tasks"


def make_task(root):
    write_memory_tree(root, "example")
    write_skill(root)
    (root / "docs").mkdir()
    (root / "docs/guide.md").write_text("# Selected synthetic guide\n\n[Unselected link](unselected.md)\nUse selected evidence.\n")
    (root / "docs/template.md").write_text("# Synthetic blank template\n\n{{scope}}\n")
    request = json.loads((FIXTURES / "request.json").read_text())
    save_request(root, request)
    return request


def save_request(root, request):
    (root / "request.json").write_text(json.dumps(request))


def add_policy(root, *, mode="default"):
    policy = json.loads((FIXTURES / "policy.json").read_text())
    policy["bindings"][0]["mode"] = mode
    (root / "docs/content-policy.json").write_text(json.dumps(policy))
    return policy
