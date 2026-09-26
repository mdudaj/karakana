# Handoff provenance and test isolation

## Scope and evidence

Approved task: repair cross-project handoff context and test-runtime contamination.
No deployment, live model call or history deletion is included.

Observed on 2026-09-26: Karakana handoff loaded CRDB concepts; focused protocol
tests wrote trace `20260926-064233-4cff57` into the real checkout and that trace
was selected during integration handoff refresh. Dogfood tests also wrote mock
requirements into the real recovery stores.

Source audit:

- `okf/context.py`: relationship traversal bypasses project/status constraints.
- `cli.py`: latest protocol selection includes classification-only commands and
  applies a global 50-record limit before project filtering.
- `handoffs/builder.py`: automatic artifact recovery has no explicit opt-out.
- `tests/test_protocols.py`, dogfood/workspace tests: mutating calls use real cwd.
- `handoffs/store.py`: skillpack filtering occurs after the 20-handoff limit.

Research: [pytest temporary directories](https://docs.pytest.org/en/stable/how-to/tmp_path.html)
and [Click testing](https://click.palletsprojects.com/en/stable/testing/) recommend
temporary filesystem contexts for tests. The CLI resolves cwd, so these tests
will use a copied context under `tmp_path` plus `monkeypatch.chdir`, not threaded
CLI invocations. Reuse `docs/engineering-process.md`; no new lifecycle needed.

## Requirements and acceptance

| ID | Requirement | Verification |
| --- | --- | --- |
| HP-1 | Project-scoped concept traversal cannot cross into another project or include disallowed statuses. Type/tag filters still select starting concepts, not all dependencies. | Synthetic cross-project/cyclic graph and real Karakana context tests. |
| HP-2 | Refresh can select an exact protocol trace, rejects wrong-project/non-protocol traces, and does not let classification-only activity supersede a task. | CLI and selection tests, including >50 unrelated traces. |
| HP-3 | Strict protocol mode fails if no eligible trace exists. | Negative CLI test. |
| HP-4 | Explicit current-state refresh can omit automatic artifact recovery without deleting history or suppressing protocol checks. | Empty recovered references with supplied state, previous handoff preserved. |
| HP-5 | Test runtime writes cannot modify the checkout through the harness's pathlib write paths. Mutating repo-context tests use temporary copies. | Autouse guard and complete pytest suite; runtime inventory unchanged. |
| HP-6 | Skillpack and project filtering precede handoff/trace limits. | Older matching handoff survives >20 unrelated skillpack records. |

## Architecture and implementation plan

Use existing stores; add optional filters before limiting results, an explicit
`handoff refresh --protocol-trace <id>` and `--no-recover-artifacts`. Do not add a
new database, automatically delete records, or guess whether old artifacts are
fake based on their names. A supplied trace must belong to the selected project
and contain protocol requirements. Default selection skips classification-only
and handoff/check records; callers with concurrent tasks should bind a trace.

Constrain graph traversal by project and status, retaining same-project related
concepts of other types/tags. Cross-project exploration remains possible through
an unscoped OKF query, not a project handoff.

Test fixture: copy only tracked-like source/config directories required by the
integration tests, never real `.karakana`, credentials, `.git` or virtualenvs.
Guard real checkout `.karakana` writes through `Path.open`/`Path.mkdir`; this is a
test regression guard, not a security sandbox for arbitrary subprocesses.

Steps: write failing regressions; implement the bounded changes; move mutating
tests to temporary contexts; run full pytest and evals; create clean append-only
handoff from explicit state and exact trace. Preserve prior runtime records.

Rollback: revert code/instructions through a reviewed patch; no storage migration
or deletion. Existing handoffs remain readable. New flags are optional. Stricter
missing-trace behavior applies only when protocol-pass mode is requested.

## Verification

Verified on 2026-09-26:

- Initial focused regressions: seven failures reproduced the missing boundaries.
- Full pytest after repair: **578 passed** (12.27 seconds).
- `karakana eval run`: **145 passed**, zero failures/warnings.
- Skill validation, project memory validation and `git diff --check`: passed.
- Completion protocol check passed after attaching the append-only handoff;
  handoff doctor passed. Reloaded Karakana context contained only Karakana
  concepts, with no CRDB concepts or recovered test artifacts.
- Real runtime inventory (path, size, mtime) SHA-256 before/after pytest:
  `8f6c96b18fdc79a0f045535dab4196fce15bcd02a0931b18325725b0d9b2e6e8`
  on both sides. No harness commands ran during this measurement.
- Added negative tests for classification, missing/foreign/path-traversal trace
  IDs, absent strict-mode trace, and real-checkout runtime writes. Project store
  filtering is tested beyond the old limit; clean explicit recovery retains
  existing history.

Tests reuse temporary copies as recommended by pytest and Click. The guard only
covers the harness's pathlib write paths, not arbitrary subprocesses. Legacy
runtime artifacts remain intact and must still be verified before recovery.
Use an explicit current-state refresh for this completed slice.

Integration: the user approved squash merge on 2026-09-26. Submit the reviewed
branch through a pull request, check CI, and record the merge in the append-only
handoff. No deployment or live model calls were performed.
