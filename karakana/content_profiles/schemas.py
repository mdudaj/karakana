"""Small strict data contracts for the M1 checker; no executable rule language."""

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
        return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=constant)
    except ContentError:
        raise
    except (ValueError, RecursionError) as exc:
        raise ContentError("Read the input as supported UTF-8 JSON and correct its syntax.", rule="CP-CONTRACT-001") from exc


def validate_context(data):
    shape(data, ("context_version", "namespace", "documents"), ADVANCED)
    if data["context_version"] != "0.1":
        raise ContentError("Select supported context version 0.1; context 0.2 is not supported in M1.", unsupported=True)
    namespace = text(data["namespace"])
    if not re.fullmatch(r"[a-z][a-z0-9-]{0,62}", namespace):
        raise ContentError("Use an explicit simple namespace, without inferring it from a repository name.")
    for name in ADVANCED:
        if name in data:
            if not isinstance(data[name], list):
                raise ContentError("Optional context collections must be JSON arrays.")
            if data[name]:
                raise ContentError(f"The {name} capability is not supported in M1. Use a standard-pack context.",
                                   rule="CP-CAPABILITY-001", unsupported=True)
    docs = data["documents"]
    if not isinstance(docs, list) or not 1 <= len(docs) <= 32:
        raise ContentError("Declare between 1 and 32 source documents.")
    keys = set()
    for doc in docs:
        shape(doc, ("key", "path", "format", "profile"), ("requirements",))
        key = text(doc["key"])
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", key) or key in keys:
            raise ContentError("Document keys must be unique simple identifiers.")
        keys.add(key)
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
    for doc in docs:
        if not set(doc.get("requirements", [])) <= keys or doc["key"] in doc.get("requirements", []):
            raise ContentError("Requirements baseline keys must resolve to other declared documents.", rule="CP-REFERENCE-001")
    return data


@dataclass
class Row:
    values: dict
    line: int


@dataclass
class Section:
    heading: str
    line: int
    end: int
    prose: list = field(default_factory=list)


@dataclass
class Narrative:
    key: str
    path: str
    profile: dict
    sections: dict
    tables: dict
    metadata: dict
    prose: list


@dataclass
class ContentReport:
    data: dict

    @property
    def ok(self):
        return self.data["completeness"] == "complete"

    def to_dict(self):
        return deepcopy(self.data)
