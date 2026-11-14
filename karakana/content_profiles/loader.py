"""Bounded immutable local reads and registered packaged profile loading."""

import hashlib
from importlib.resources import files
from pathlib import Path

from karakana.tools.engineering_artifacts import _path, ArtifactError
from .schemas import ContentError, shape, strict_json, text


MAX_SOURCE_BYTES = 2_000_000
MAX_TOTAL_BYTES = 16_000_000
MAX_FILES = 32
MAX_CONFIG_BYTES = 128_000
REGISTRY = {("requirements", "0.1"): "requirements-0.1.json",
            ("system-design", "0.1"): "system-design-0.1.json"}
CHECKS = {"metadata", "coverage", "records", "references", "wording", "gaps", "claims"}
RECORD_TYPES = {"metadata", "standard", "requirement", "criterion", "gap", "component",
                "design_response", "decision", "verification"}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def local_path(root, value):
    value = text(value)
    path = Path(value)
    if (path.is_absolute() or path.suffix in {".pem", ".key"}
            or any(p == ".env" or p.startswith(".env.") or p == "secrets" for p in path.parts)):
        raise ContentError("Use a root-relative path outside credential/environment locations.", rule="CP-PATH-001")
    try:
        return _path(root, path)
    except (ArtifactError, OSError, ValueError, RuntimeError) as exc:
        raise ContentError("The path is outside the declared local scope. Select a permitted source/output.", rule="CP-PATH-001") from exc


class Inputs:
    def __init__(self, root):
        try:
            self.root = Path(root).resolve()
            if not self.root.is_dir():
                raise OSError("not a local directory")
        except (OSError, ValueError, RuntimeError) as exc:
            raise ContentError("Select an existing resolvable local root directory.", rule="CP-PATH-001") from exc
        self.sources = {}
        self.total = 0

    def read(self, value, role, limit=MAX_SOURCE_BYTES):
        path = local_path(self.root, value)
        try:
            with path.open("rb") as stream:
                raw = stream.read(limit + 1)
        except OSError as exc:
            raise ContentError("The local input is missing or unreadable. Check the declared path.", rule="CP-READ-001") from exc
        if len(raw) > limit:
            raise ContentError("The input exceeds the supported byte limit. Reduce or split the source.", rule="CP-LIMIT-001")
        key = str(value)
        previous = self.sources.get(key)
        if previous:
            if previous["sha256"] != sha(raw) or previous["resolved"] != path:
                raise ContentError("A source changed during this check. Run the check again.", rule="CP-DRIFT-001")
            previous["roles"].add(role)
        else:
            if len(self.sources) >= MAX_FILES or self.total + len(raw) > MAX_TOTAL_BYTES:
                raise ContentError("The input set exceeds the supported file/byte limits. Split the check context.", rule="CP-LIMIT-001")
            self.total += len(raw)
            self.sources[key] = {"path": path.relative_to(self.root).as_posix(), "resolved": path,
                                 "requested": key, "sha256": sha(raw), "roles": {role}, "limit": limit}
        return raw, self.sources[key]["path"]

    def manifest(self):
        return sorted(({"path": item["path"], "requested": item["requested"], "sha256": item["sha256"],
                        "roles": sorted(item["roles"])} for item in self.sources.values()),
                      key=lambda x: (x["path"], x["requested"]))

    def recheck(self):
        for item in list(self.sources.values()):
            self.read(item["requested"], next(iter(item["roles"])), item["limit"])


def load_profile(profile_id, version):
    name = REGISTRY.get((profile_id, version))
    if name is None:
        raise ContentError("Select a registered content profile and version supported in M1.",
                           rule="CP-PROFILE-001", unsupported=True)
    raw = files("karakana.content_profiles").joinpath(name).read_bytes()
    if len(raw) > MAX_CONFIG_BYTES:
        raise ContentError("The packaged profile exceeds its supported size.", rule="CP-PROFILE-001")
    data = strict_json(raw)
    shape(data, ("profile_id", "profile_version", "formats", "slots", "tables", "checks"))
    if data["profile_id"] != profile_id or data["profile_version"] != version or data["formats"] != ["narrative-0.1"]:
        raise ContentError("The packaged profile identity or format is inconsistent.", rule="CP-PROFILE-001")
    if (not isinstance(data["checks"], list) or not all(isinstance(v, str) for v in data["checks"])
            or len(data["checks"]) != len(CHECKS) or set(data["checks"]) != CHECKS):
        raise ContentError("The packaged profile requests unsupported checks.", rule="CP-PROFILE-001")
    if not isinstance(data["slots"], list) or not isinstance(data["tables"], list):
        raise ContentError("The packaged profile needs slot and table arrays.", rule="CP-PROFILE-001")
    ids = set()
    for slot in data["slots"]:
        shape(slot, ("id", "heading", "required", "kind"))
        text(slot["id"])
        text(slot["kind"])
        if slot["id"] in ids or not isinstance(slot["heading"], str) or type(slot["required"]) is not bool or slot["kind"] not in {"prose", "table", "mixed"}:
            raise ContentError("The packaged slot definition is invalid.", rule="CP-PROFILE-001")
        ids.add(slot["id"])
    table_ids = set()
    for table in data["tables"]:
        shape(table, ("id", "slot", "headers", "required_fields", "record_type", "identity", "min_rows"))
        text(table["id"])
        text(table["slot"])
        if (table["id"] in table_ids or table["slot"] not in ids or type(table["min_rows"]) is not int
                or not 0 <= table["min_rows"] <= 1):
            raise ContentError("The packaged table definition is invalid.", rule="CP-PROFILE-001")
        table_ids.add(text(table["id"]))
        if text(table["record_type"]) not in RECORD_TYPES:
            raise ContentError("The packaged table requests an unsupported record kind.", rule="CP-PROFILE-001")
        if not isinstance(table["identity"], str) or not isinstance(table["headers"], list) or not table["headers"]:
            raise ContentError("The packaged table header definition is invalid.", rule="CP-PROFILE-001")
        for header in table["headers"]:
            if (not isinstance(header, list) or not header or not all(isinstance(v, str) for v in header)
                    or len(set(header)) != len(header)):
                raise ContentError("The packaged table columns are invalid.", rule="CP-PROFILE-001")
            for value in header:
                text(value)
            if (not isinstance(table["required_fields"], list)
                    or not all(isinstance(v, str) for v in table["required_fields"])
                    or not set(table["required_fields"]) <= set(header)):
                raise ContentError("Required profile fields do not exist in the header.", rule="CP-PROFILE-001")
            if table["identity"] and table["identity"] not in header:
                raise ContentError("Profile identity does not exist in the header.", rule="CP-PROFILE-001")
    return data, {"id": profile_id, "version": version, "sha256": sha(raw)}
