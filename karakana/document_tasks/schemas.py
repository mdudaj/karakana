"""Strict S1 request/policy contracts; M2 context semantics stay in M2."""

from copy import deepcopy
import re

from karakana.content_profiles.schemas import ContentError, strict_json, shape, text


ACTIONS = {"inquiry", "analysis", "review", "author", "revise", "plan", "mechanical_fix"}
ROLES = {"guide", "template", "example", "reference"}
IDENTIFIER = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}")


class TaskError(ValueError):
    def __init__(self, message, *, code="DT-INPUT-001", outcome="blocked", pointer="", location=None):
        super().__init__(message)
        self.code, self.outcome = code, outcome
        self.location = location or {"input": "request", "pointer": pointer}


def literal(value, pointer="", *, limit=2048, multiline=False):
    try:
        text(value)
        value.encode("utf-8")
    except (ContentError, UnicodeError) as exc:
        raise TaskError("Use a nonempty UTF-8 literal without control characters.", pointer=pointer) from exc
    if len(value) > limit or (not multiline and any(c in value for c in "\r\n\t")):
        raise TaskError("Use a literal within the documented field length and line limits.", pointer=pointer)
    return value


def contract(value, required, pointer=""):
    try:
        shape(value, required)
    except ContentError as exc:
        raise TaskError("Required fields are missing or unexpected fields were supplied.", pointer=pointer) from exc


def decode(raw):
    try:
        return strict_json(raw)
    except (ContentError, UnicodeError) as exc:
        raise TaskError("Use strict UTF-8 JSON without duplicate keys, nonstandard numbers or excessive nesting.") from exc


def resource(value, pointer="", *, policy=False):
    fields = ("artifact_type", "role", "path", "revision") + (("mode",) if policy else ())
    contract(value, fields, pointer)
    for key in fields:
        literal(value[key], pointer + "/" + key)
    if value["role"] not in ROLES or (policy and value["role"] == "reference"):
        raise TaskError("Select a supported resource role.", pointer=pointer + "/role")
    if policy and value["mode"] not in {"default", "locked"}:
        raise TaskError("Select default or locked for a policy binding.", pointer=pointer + "/mode")


def validate_request(value):
    contract(value, ("request_version", "project", "skill", "task", "resources", "use_project_defaults", "context"))
    if value["request_version"] != "0.1":
        raise TaskError("Select request version 0.1.", outcome="unsupported", pointer="/request_version")
    for key in ("project", "skill"):
        if not IDENTIFIER.fullmatch(literal(value[key], "/" + key)):
            raise TaskError("Use a simple project or skill identifier without path components.", pointer="/" + key)
    task = value["task"]
    contract(task, ("id", "action", "text", "audience", "scope", "revision", "artifact_types"), "/task")
    for key in ("id", "action", "audience", "scope", "revision"):
        literal(task[key], "/task/" + key)
    literal(task["text"], "/task/text", limit=32768, multiline=True)
    if task["action"] not in ACTIONS:
        raise TaskError("Select a supported explicit task action.", pointer="/task/action")
    types = task["artifact_types"]
    if not isinstance(types, list) or len(types) > 32:
        raise TaskError("Declare at most32 unique artifact types.", pointer="/task/artifact_types")
    for item in types:
        literal(item, "/task/artifact_types")
    if len(set(types)) != len(types):
        raise TaskError("Declare each artifact type once.", pointer="/task/artifact_types")
    if type(value["use_project_defaults"]) is not bool:
        raise TaskError("Explicitly choose true or false for project defaults.", pointer="/use_project_defaults")
    if value["context"] is not None:
        literal(value["context"], "/context")
    resources = value["resources"]
    if not isinstance(resources, list) or len(resources) > 32:
        raise TaskError("Declare at most32 explicit resources.", pointer="/resources")
    slots = set()
    for i, entry in enumerate(resources):
        pointer = f"/resources/{i}"
        resource(entry, pointer)
        if entry["artifact_type"] not in types:
            raise TaskError("Declare this resource's artifact type in the task.", pointer=pointer)
        slot = (entry["artifact_type"], entry["role"], entry["path"] if entry["role"] == "reference" else "")
        if slot in slots:
            raise TaskError("Declare each resource slot once.", pointer=pointer)
        slots.add(slot)
    return deepcopy(value)


def validate_policy(value, project):
    contract(value, ("policy_version", "project", "bindings"), "/policy")
    if value["policy_version"] != "0.1":
        raise TaskError("Select policy version 0.1.", outcome="unsupported", pointer="/policy/policy_version")
    if value["project"] != project:
        raise TaskError("Project policy belongs to another project.", code="DT-POLICY-001", pointer="/policy/project")
    bindings = value["bindings"]
    if not isinstance(bindings, list) or len(bindings) > 64:
        raise TaskError("Declare at most64 policy bindings.", pointer="/policy/bindings")
    slots = set()
    for i, entry in enumerate(bindings):
        resource(entry, f"/policy/bindings/{i}", policy=True)
        slot = entry["artifact_type"], entry["role"]
        if slot in slots:
            raise TaskError("A policy slot has duplicate or conflicting bindings.", code="DT-POLICY-001", pointer="/policy/bindings")
        slots.add(slot)
    return deepcopy(value)
