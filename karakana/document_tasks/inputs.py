"""Captured bounded local bytes, optional presence and package-owned code identity."""

from importlib.resources import files
from pathlib import Path
import json

from karakana.content_profiles.loader import (
    local_path, sha, MAX_FILES, MAX_SOURCE_BYTES, MAX_TOTAL_BYTES, MAX_CONFIG_BYTES,
)
from karakana.content_profiles.schemas import ContentError
from . import VERSION
from .schemas import TaskError, literal


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")


def credential_path(path):
    return (path.suffix.lower() in {".pem", ".key"}
            or any(part.lower() in {".env", "secrets"} or part.lower().startswith(".env.") for part in path.parts))


def fingerprint():
    names = ["document_tasks/" + n + ".py" for n in
             ("__init__", "schemas", "inputs", "selection", "prepare", "assessment", "verify", "report", "bundles", "cli")]
    names += ["cli.py", "agents/planner.py", "skills/loader.py", "skills/schemas.py",
              "memory/ubongo.py", "memory/schemas.py", "models/router.py", "protocols/lifecycle.py",
              "content_profiles/schemas.py", "content_profiles/loader.py", "tools/engineering_artifacts.py"]
    package = files("karakana")
    components = [{"path": name, "sha256": sha(package.joinpath(name).read_bytes())} for name in sorted(names)]
    return {"version": VERSION, "components": components, "sha256": sha(json_bytes(components))}


class CapturedInputs:
    def __init__(self, root):
        try:
            self.root = Path(root).resolve()
            str(self.root).encode("utf-8")
            if credential_path(self.root):
                raise OSError()
            if not self.root.is_dir():
                raise OSError()
            local_path(self.root, ".")
        except (OSError, ValueError, RuntimeError, ContentError) as exc:
            raise TaskError("Select an existing local root directory.", code="DT-PATH-001") from exc
        self.entries = {}
        self.physical = {}
        self.total = 0
        self.project = None

    def path(self, requested):
        literal(requested)
        if credential_path(Path(requested)):
            raise TaskError("Select a permitted root-relative path outside credential locations.", code="DT-PATH-001")
        try:
            path = local_path(self.root, requested)
        except (ContentError, OSError, RuntimeError, ValueError) as exc:
            raise TaskError("Select a permitted root-relative path outside credential locations.", code="DT-PATH-001") from exc
        if credential_path(path):
            raise TaskError("Select a permitted root-relative path outside credential locations.", code="DT-PATH-001")
        parts = path.relative_to(self.root).parts
        if self.project and parts[:2] == ("ubongo", "projects") and (len(parts) < 3 or parts[2] != self.project):
            raise TaskError("Selected durable memory belongs to another project.", code="DT-PROJECT-001")
        return path

    def read(self, requested, role, *, optional=False, limit=MAX_SOURCE_BYTES):
        path = self.path(requested)
        try:
            present = path.exists()
            if not present and not optional:
                raise OSError()
            raw = None
            if present:
                if not path.is_file():
                    raise OSError()
                with path.open("rb") as stream:
                    raw = stream.read(limit + 1)
                if len(raw) > limit:
                    raise TaskError("Input exceeds its supported byte limit. Reduce the selected input.", code="DT-LIMIT-001")
                raw.decode("utf-8")
        except (OSError, UnicodeError) as exc:
            raise TaskError("A declared local input is missing, unreadable or not UTF-8.", code="DT-READ-001",
                            location={"path": path.relative_to(self.root).as_posix()}) from exc
        digest = sha(raw) if raw is not None else None
        previous = self.entries.get(requested)
        if previous:
            if previous["resolved"] != path or previous["sha256"] != digest or previous["present"] != present:
                raise TaskError("An input changed during preparation. Prepare again after inputs settle.", code="DT-DRIFT-001", outcome="failed")
            previous["roles"].add(role)
            previous["limit"] = min(previous["limit"], limit)
            return previous["raw"]
        # Physical aliases share the byte/file budget, but every requested alias is rechecked.
        physical = self.physical.get(path)
        if physical is not None and physical != digest:
            raise TaskError("A physical input changed during preparation.", code="DT-DRIFT-001", outcome="failed")
        if path not in self.physical:
            if len(self.physical) >= MAX_FILES or self.total + len(raw or b"") > MAX_TOTAL_BYTES:
                raise TaskError("Selected inputs exceed the supported file/total-byte limits.", code="DT-LIMIT-001")
            self.physical[path] = digest
            self.total += len(raw or b"")
        self.entries[requested] = {"resolved": path, "present": present, "sha256": digest,
                                   "roles": {role}, "raw": raw, "limit": limit, "optional": optional}
        return raw

    def recheck(self):
        for requested, entry in list(self.entries.items()):
            self.read(requested, next(iter(entry["roles"])), optional=entry["optional"], limit=entry["limit"])

    def manifest(self):
        return [{"requested": key, "resolved": entry["resolved"].relative_to(self.root).as_posix(),
                 "present": entry["present"], "sha256": entry["sha256"], "roles": sorted(entry["roles"])}
                for key, entry in sorted(self.entries.items())]
