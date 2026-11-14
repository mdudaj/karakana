"""Synthetic setup only; no model output, approval or real runtime imported."""

from pathlib import Path
import json
import shutil

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


def make_assessment(root, *, version="0.2", both=True):
    request = make_task(root)
    request["context"] = "context.json"
    request["task"]["action"] = "review"
    request["task"]["artifact_types"] = ["requirements", "system-design"] if both else ["requirements"]
    context = {"context_version": version, "namespace": "example", "documents": []}
    for key, owner, kind in [("req", "requirements", "requirements"), ("design", "design-records", "system-design")][:2 if both else 1]:
        shutil.copyfile(Path(__file__).parents[1] / f"skills/engineering-{owner}/assets/{kind}-example.md", root / (key + ".md"))
        entry = {"key": key, "path": key + ".md", "format": "narrative-0.1", "profile": {"id": kind, "version": "0.1"}}
        if key == "design":
            entry["requirements"] = ["req"]
        context["documents"].append(entry)
    save_request(root, request)
    save_context(root, context)
    return request, context


def save_context(root, context):
    (root / "context.json").write_text(json.dumps(context))
