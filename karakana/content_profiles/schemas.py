"""Small strict data contracts for narrative content checks; no executable rule language."""

from copy import deepcopy
from dataclasses import dataclass, field
import json
import re


CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
ADVANCED = ("references", "coverage", "omissions", "open_items", "claims")


class ContentError(ValueError):
    def __init__(self, message, *, rule="CP-INPUT-001", unsupported=False, location=None):
        super().__init__(message)
        self.rule = rule
        self.unsupported = unsupported
        self.location = location or {}


def text(value):
    if not isinstance(value, str) or not value.strip() or CONTROL.search(value):
        raise ContentError("Use a nonempty literal string without control characters.")
    return value


def shape(value, required, optional=()):
    if (not isinstance(value, dict) or not set(required) <= value.keys()
            or value.keys() - set(required) - set(optional)):
        raise ContentError("Required fields are missing or unsupported fields were supplied.", rule="CP-CONTRACT-001")
    return value


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ContentError("Duplicate JSON keys are not supported.", rule="CP-CONTRACT-001")
            result[key] = value
        return result

    def constant(_):
        raise ContentError("Use standard JSON values, without NaN or Infinity.", rule="CP-CONTRACT-001")

    try:
        result = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=constant)
        pending = [(result, 0)]
        while pending:
            value, depth = pending.pop()
            if depth > 64:
                raise ContentError("JSON nesting exceeds the supported depth. Reduce nested input structures.", rule="CP-LIMIT-001")
            if isinstance(value, dict): pending.extend((v, depth+1) for v in value.values())
            elif isinstance(value, list): pending.extend((v, depth+1) for v in value)
        return result
    except ContentError:
        raise
    except (ValueError, RecursionError) as exc:
        raise ContentError("Read the input as supported UTF-8 JSON and correct its syntax.", rule="CP-CONTRACT-001") from exc


def locator(value):
    shape(value, ("document",), ("anchor", "heading", "record_id", "field"))
    text(value["document"])
    if ("anchor" in value) == ("heading" in value):
        raise ContentError("Select exactly one explicit anchor or complete heading path.", rule="CP-LOCATOR-001")
    if "anchor" in value:
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", text(value["anchor"])):
            raise ContentError("Use a literal supported source anchor.", rule="CP-LOCATOR-001")
    else:
        path = value["heading"]
        if not isinstance(path, list) or not 1 <= len(path) <= 16:
            raise ContentError("Use a nonempty bounded heading path.", rule="CP-LOCATOR-001")
        for part in path:
            text(part)
    for key in ("record_id", "field"):
        if key in value:
            text(value[key])
    return value


def validate_context(data):
    shape(data, ("context_version", "namespace", "documents"), (*ADVANCED, "links"))
    if data["context_version"] not in ("0.1", "0.2"):
        raise ContentError("Select supported context version 0.1 or 0.2.", unsupported=True)
    if data["context_version"] == "0.1" and "links" in data:
        raise ContentError("The links field requires context version 0.2; remove it for version 0.1.", rule="CP-CONTRACT-001")
    namespace = text(data["namespace"])
    if not re.fullmatch(r"[a-z][a-z0-9-]{0,62}", namespace):
        raise ContentError("Use an explicit simple namespace, without inferring it from a repository name.")
    for name in (*ADVANCED, "links"):
        if name in data and (not isinstance(data[name], list) or len(data[name]) > 256):
            raise ContentError("Context collections must be arrays with at most 256 entries.", rule="CP-LIMIT-001")
    docs = data["documents"]
    if not isinstance(docs, list) or not 1 <= len(docs) <= 32:
        raise ContentError("Declare between 1 and 32 source documents.")
    keys = set()
    def register(key):
        key = text(key)
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", key) or key in keys:
            raise ContentError("Document and reference keys must be unique simple identifiers.")
        keys.add(key)
    for doc in docs:
        shape(doc, ("key", "path", "format", "profile"), ("requirements",))
        register(doc["key"])
        text(doc["path"])
        if doc["format"] != "narrative-0.1":
            raise ContentError("Select narrative-0.1. P02 sources retain their separate validator/exporter.", unsupported=True)
        shape(doc["profile"], ("id", "version"))
        text(doc["profile"]["id"])
        text(doc["profile"]["version"])
        baselines = doc.get("requirements", [])
        if (not isinstance(baselines, list) or any(not isinstance(x, str) for x in baselines)
                or len(baselines) != len(set(baselines))):
            raise ContentError("Declare unique document keys in the requirements baseline list.")
    doc_keys = set(keys)
    for doc in docs:
        if not set(doc.get("requirements", [])) <= doc_keys or doc["key"] in doc.get("requirements", []):
            raise ContentError("Requirements baseline keys must resolve to other declared documents.", rule="CP-REFERENCE-001")
    for ref in data.get("references", []):
        shape(ref, ("key", "path", "purpose"), ("format",))
        register(ref["key"])
        text(ref["path"]); text(ref["purpose"])
        if "format" in ref and ref["format"] != "narrative-0.1":
            raise ContentError("Select narrative-0.1 for located reference content; omit format for opaque file references.", unsupported=True)
    for name, selector in (("coverage", "source"), ("omissions", "rationale")):
        seen = set()
        for entry in data.get(name, []):
            shape(entry, ("document", "slot", selector))
            text(entry["document"]); text(entry["slot"])
            if entry["document"] not in doc_keys or (entry["document"], entry["slot"]) in seen:
                raise ContentError("Declare each slot mapping once for an actual profiled document.", rule="CP-COVERAGE-001")
            seen.add((entry["document"], entry["slot"]))
            locator(entry[selector])
    for item in data.get("open_items", []):
        shape(item, ("item", "affected", "effect", "resolver", "next_action"))
        for field_name in ("item", "effect", "resolver", "next_action"):
            locator(item[field_name])
        if not isinstance(item["affected"], list) or not 1 <= len(item["affected"]) <= 256:
            raise ContentError("Locate at least one affected requirement or scope.")
        for value in item["affected"]:
            locator(value)
    for item in data.get("claims", []):
        shape(item, ("source", "kind", "fields"))
        locator(item["source"])
        if item["kind"] not in ("test_result", "decision"):
            raise ContentError("Select test_result or decision for an actual located claim.")
        fields = ("revision", "actor", "result", "time", "evidence")
        if item["kind"] == "test_result": fields += ("environment",)
        shape(item["fields"], fields)
        for value in item["fields"].values(): locator(value)
    for edge in data.get("links", []):
        shape(edge, ("from", "to"))
        locator(edge["from"]); locator(edge["to"])
        if "field" not in edge["from"] or "record_id" not in edge["to"] or "field" in edge["to"]:
            raise ContentError("Link from a registered reference cell to a whole identified target record.", rule="CP-REFERENCE-001")
    def declared(value):
        if isinstance(value, dict):
            if "document" in value and ("anchor" in value or "heading" in value) and value["document"] not in keys:
                raise ContentError("Locator document keys must name declared documents or references.", rule="CP-LOCATOR-001")
            for v in value.values(): declared(v)
        elif isinstance(value, list):
            for v in value: declared(v)
    declared(data)
    return data


@dataclass
class Row:
    values: dict
    line: int
    path: str = ""


@dataclass
class Section:
    heading: str
    line: int
    end: int
    prose: list = field(default_factory=list)
    path: tuple = ()


@dataclass
class Narrative:
    key: str
    path: str
    profile: dict
    sections: dict
    tables: dict
    metadata: dict
    prose: list
    source: object = None
    origins: dict = field(default_factory=dict)
    selections: dict = field(default_factory=dict)
    omissions: dict = field(default_factory=dict)
    native_tables: set = field(default_factory=set)


@dataclass
class ContentReport:
    data: dict

    @property
    def ok(self):
        return self.data["completeness"] == "complete"

    def to_dict(self):
        return deepcopy(self.data)
