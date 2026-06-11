"""Generate Karakana release checklist artifacts."""

from __future__ import annotations

import json
import secrets
from datetime import datetime, timezone
from pathlib import Path


CHECKLIST = """# Karakana Release Checklist

## Pre-Release

- [ ] `karakana doctor`
- [ ] `karakana config validate`
- [ ] `karakana skill validate-all`
- [ ] `karakana skillpack validate-all`
- [ ] `karakana workspace validate-all`
- [ ] `karakana eval run`
- [ ] `pytest`
- [ ] Review docs
- [ ] Review safety rules
- [ ] Review release notes

## Packaging

- [ ] Version updated
- [ ] Package metadata valid
- [ ] README updated
- [ ] CHANGELOG updated
- [ ] License present if required

## Safety

- [ ] No secrets committed
- [ ] `.karakana/` gitignored
- [ ] No live model calls required for tests
- [ ] No push/PR/deploy automation enabled by default

## Final Review

- [ ] Human review complete
- [ ] Tag manually if appropriate
- [ ] Publish manually if appropriate
"""


def write_release_checklist(repo_root: Path) -> tuple[str, Path]:
    run_id = _release_id("checklist")
    directory = repo_root / ".karakana" / "release" / run_id
    directory.mkdir(parents=True, exist_ok=True)
    md_path = directory / "release-checklist.md"
    json_path = directory / "release-checklist.json"
    md_path.write_text(CHECKLIST, encoding="utf-8")
    json_path.write_text(json.dumps({"release_checklist_id": run_id, "path": str(md_path)}, indent=2) + "\n", encoding="utf-8")
    return run_id, md_path


def _release_id(kind: str) -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + f"-{kind}-{secrets.token_hex(3)}"
