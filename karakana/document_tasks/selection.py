"""Small explicit recommendations and task/default/lock resolution; no crawling."""

from karakana.content_profiles.loader import sha
from .inputs import MAX_CONFIG_BYTES
from .schemas import TaskError, decode, validate_policy


POLICY_PATH = "docs/content-policy.json"
INVENTORY = {
    "requirements": {"owner": "engineering-requirements", "version": "0.1",
                     "guide": "skills/engineering-requirements/references/requirements-template-guide.md",
                     "template": "skills/engineering-requirements/assets/requirements-template.md",
                     "example": "skills/engineering-requirements/assets/requirements-example.md"},
    "system-design": {"owner": "engineering-design-records", "version": "0.1",
                      "guide": "skills/engineering-design-records/references/system-design-template-guide.md",
                      "template": "skills/engineering-design-records/assets/system-design-template.md",
                      "example": "skills/engineering-design-records/assets/system-design-example.md"},
}


def recommendations(types):
    return [{"artifact_type": kind, "owning_skill": INVENTORY[kind]["owner"],
             "profile": {"id": kind, "version": "0.1"},
             "resources": [{"role": role, "path": INVENTORY[kind][role], "revision": "0.1"}
                           for role in ("guide", "template", "example")], "selected": False}
            for kind in sorted(types) if kind in INVENTORY]


def resolve_selection(request, inputs):
    raw = inputs.read(POLICY_PATH, "project_policy", optional=True, limit=MAX_CONFIG_BYTES)
    try:
        policy = validate_policy(decode(raw), request["project"]) if raw is not None else {"bindings": []}
    except TaskError as exc:
        exc.location = {"path": POLICY_PATH, "pointer": exc.location.get("pointer", "").removeprefix("/policy")}
        raise
    for i, binding in enumerate(policy["bindings"]):
        try:
            inputs.path(binding["path"])  # Validate declarations without loading unselected defaults.
        except TaskError as exc:
            exc.location = {"path": POLICY_PATH, "pointer": f"/bindings/{i}/path"}
            raise
    effective, overrides = {}, []
    for entry in request["resources"]:
        key = entry["artifact_type"], entry["role"], entry["path"] if entry["role"] == "reference" else ""
        effective[key] = {**entry, "origin": "task"}
    for binding in policy["bindings"]:
        if binding["artifact_type"] not in request["task"]["artifact_types"]:
            continue
        entry = {key: binding[key] for key in ("artifact_type", "role", "path", "revision")}
        key = entry["artifact_type"], entry["role"], ""
        current = effective.get(key)
        if binding["mode"] == "locked":
            if current is None or any(current[k] != v for k, v in entry.items()):
                raise TaskError("Select the exact resource required by the project lock; resolve a conflict through project review.",
                                code="DT-LOCK-001", pointer="/resources")
        elif current is not None:
            if any(current[k] != v for k, v in entry.items()):
                overrides.append({"previous": entry, "effective": {k: current[k] for k in entry},
                                  "reason": "Explicit task selection overrides an overridable project default."})
        elif request["use_project_defaults"]:
            effective[key] = {**entry, "origin": "project_default"}
    result, seen = [], {}
    for key, entry in sorted(effective.items()):
        raw = inputs.read(entry["path"], "resource:" + entry["role"])
        physical = inputs.path(entry["path"])
        previous = seen.get(physical)
        if previous and (previous["revision"] != entry["revision"] or entry["role"] == "reference" or previous["role"] == "reference"):
            raise TaskError("The same physical resource has conflicting or duplicate declarations.", code="DT-RESOURCE-001", pointer="/resources")
        seen[physical] = entry
        inventory = INVENTORY.get(entry["artifact_type"], {})
        registered = inventory.get(entry["role"]) in {entry["path"], physical.relative_to(inputs.root).as_posix()}
        if registered and entry["revision"] != inventory["version"]:
            raise TaskError("Select the supported resource pack revision 0.1.", code="DT-RESOURCE-001", outcome="unsupported", pointer="/resources")
        result.append({**entry, "owning_skill": inventory.get("owner"),
                       "revision_basis": "inventory" if registered else "caller_declared",
                       "resolved": physical.relative_to(inputs.root).as_posix(), "sha256": sha(raw)})
    return {"state": "selected" if result else "not_selected", "effective": result,
            "overrides": overrides, "recommendations": recommendations(request["task"]["artifact_types"])}
