# KDX11 S2 — content assessment and saved verification

Revision0.1;2026-11-14; local Karakana CLI, not deployment.
Trace `20261114-105904-203af5`; branch `feat/kdx11-s2-check-verify-20261114`.

## Scope and authority

The owner selected S2 with “execute” after S1 was accepted and squash merged
through PR45, `d04bef7d252ef1a77f116a284839a2e390fef251`. Clean source and the
current handoff were checked at entry. S1's1058 tests/187 evals, exact-head CI,
postmerge release and actual CLI receipts are prior evidence, not fresh S2 tests.
This authorises S2 implementation/local verification; completed delivery review,
integration and deployment remain distinct states.

Reuse accepted [TT01-TT12/A01-A12](../research/2026-11-14-task-time-content-requirements.md),
[DD01-DD12](../research/2026-11-14-task-time-content-design.md) and
[IP01-IP08/S2.1-S2.4](../research/2026-11-14-task-time-content-implementation-plan.md).
Their user stories, interfaces, UX research, standards tailoring, alternatives,
traceability and Definition of Done remain applicable. No new PRD/ADR/research
round or standards certification is needed. This record tracks actual delivery.

## Artifact gate and implementation instructions

Work type: high-risk local report/provenance integrity; no Viewflow process,
authentication, migration or live execution change. Read actual S1 modules and
tests, M2 `engineering_content.py`, profile schema/loader/report and M2 tests
before adapting them. Shared process, delivery-artifact-gate, documentation
conventions and UX-writing govern. Preserve explicit opt-in and plain terminal
copy from accepted DD09; technical report fields remain visible on this diagnostic
surface. Existing CLI/W3C/Typer/package-resource research suffices.

1. Add lazy M2 assessment adapter/producer validation; preserve report0.2 exactly,
   all declared documents and scoped gaps. Reuse S1 captured selection without
   requiring planning resources in context-only check installations.
2. Extend result/bundles/CLI with check and fresh raw report/result files. Keep
   completeness, operation outcome, freshness, readiness and acceptance separate.
3. Add strict bounded saved verification: compare raw/nested copies, delegate bare
   report verification, independently recompute all deterministic wrapper fields.
   Normalize only accepted run/M2 volatile metadata, not authority/outcome fields.
4. Exercise actual API/CLI, two profiles/context versions, malformed producers,
   absent parser, scope/paths/physical targets, drift/tamper and new-only writes;
   installed-wheel context-only behavior and legacy planner/M2/P02 compatibility.
   Update current capability docs, examples, instruction evals and command reference.

Executable request/policy/result schemas and neutral fixtures are owning contracts;
no duplicate Markdown schema master. Accepted plan maps every A01-A12 criterion
to test owners; delivery evidence below will identify actual checks/results.
Pre-implementation protocol presence pass is necessary, not semantic approval.
Full gate: focused S2 tests, full pytest, skill validation/evals, docs check,
Karakana memory validation, generated command reference and diff review. Runtime
evidence belongs under ignored `.karakana/reviews/20261114-kdx11-s2/`; tests use
temporary roots. Owner delivery review precedes normal exact-head CI/squash flow.

## Safety review and source-alignment challenge

M2 `.ok` only represents completeness; report0.2 requires exact typed invariant
checks so an exit0 blocked/not_ready producer cannot become success. A complete
report with gaps retains unresolved readiness, review required and unassessed
acceptance. Existing verify_report expects a bare report and recomputes every
assessment field; wrapper selection/policy/request/code require independent
recomputation. A matching digest alone never establishes freshness or authority.
Preserve raw-current versus wrapper-stale evidence. Saved generation/run/output
metadata may vary only within validated timezone/path/type rules.

Threat/abuse cases: forged saved acceptance/outcome or unknown fields; equal
edited report copies; optional policy arrival; symlink redirection; protected or
foreign-project paths; stale code/profile/parser; oversized/duplicate/deep JSON;
partial output and overwrite; terminal controls. Enforce existing bounds before
reading, never follow content links or launch subprocess/model calls, and retain
nonempty incomplete evidence. No semantic-truth/authenticity/Windows certificate.
Native/P02, model routing, dependencies, default gates and source files retain
their existing behavior. KDX10 authentic-input/sibling qualification remains held
independently; no ent-meal context enters this task.

Rollback: reviewed correction/revert PR scoped to S2; preserve S1, source documents,
runtime bundles and accepted decision history. No destructive cleanup/main reset.
Recommended route: Sol/high for integrity. Existing session continues under owner
selection; exact active model identity is not independently exposed here, so no
availability/switch claim or automatic model call is made.

## Delivery evidence

Prior readiness checkpoint: implementation and verification were pending.
The following actual closeout supersedes that state; history is retained.


## Implemented and verified — owner delivery review pending

S2.1-S2.4 are implemented: lazy direct M2 assessment/strict producer validation,
check bundles, independent saved task recomputation and check/verify CLI/API.
No requirements/design/plan contract changed. Context-only checks need no checkout
skill/memory resources; check captures request/policy/resources/context plus optional
AGENTS/KARAKANA, while prepare retains its planning inputs. Wrapper version0.2.0,
request/policy/result0.1, raw report0.2/checker0.2.0. Existing bundle provenance may
be stale across code changes by design; no saved approval is inherited.

Before code, exact-trace pre-implementation check
`20261114-110000-protocol-check-dccb19` passed (artifact presence only). Initial
43-case S1 regression had two expected scope/version assertion failures; their
expectations were updated for newly delivered S2 commands/wrapper version. No
M2/P02/routing/dependency/source behavior was patched to force those expectations.
Intermediate119 tests and41 output/CLI/wheel tests passed; the required focused
S2 plus M2/P02 gate367 passed in31.09s. Final producer/verify contract gate79
passed in15.90s; final full regression below covers subsequent guards/copy.
No unresolved diagnostic loop remains.

Actual final verification:

- `.venv/bin/pytest -q`: **1164 passed in51.45s**,106 new over accepted S1.
- `.venv/bin/karakana skill validate-all`: passed.
- `.venv/bin/karakana eval run`: **187/187 passed**, zero warnings,
  `20261114-111312-eval-6bb475`. Updated coordinator instruction eval remains
  source-text coverage, not a model-behavior or factual-truth test.
- `.venv/bin/karakana docs check` and `memory validate --project karakana`: passed.
- `.venv/bin/karakana docs command-reference --write`: generated current reference;
  deterministic comparison and local links/scope/JSON/diff checks are retained.
- `.venv/bin/karakana release check --json`: default19/19 pass, no errors/warnings,
  `20261114-111313-release-check-663220`; full tests/evals ran separately.
- Actual installed wheel outside checkout: API/CLI preparation without parser,
  context-only check/verify without skills/memory, supported parser present and
  controlled parser absence; missing assets/parser refused with supported states.
- Actual documented checkout check, verify, verify-of-verify and text commands:
  both synthetic documents preserved, seven source gaps; checked/verified0,
  readiness unresolved, acceptance not_assessed, saved freshness separate. Raw
  files equal their nested reports. These are example checks, not product facts.
- Parameterised saved-field tampering changes every deterministic leaf for both
  check and successful verify bundles, including equal edited report copies;
  all refuse. Only documented validated run/M2 generation metadata and object
  member order may vary. Source/evidence/context/guide/policy/optional-presence/
  profile/parser/checker/wrapper code and equal-byte symlink target drift refuse.
- Actual CLI text/JSON/exit matrix covers complete-with-gaps, incomplete,
  unsupported, missing context, current/stale/foreign/incomplete verification;
  malformed producers and exit0 blocked/not_ready states cannot become success.
  Raw-current/wrapper-stale remains visible. Strict JSON rejects duplicate keys,
  deep/oversized/partial input, nonfinite exponent overflow and escaped surrogates.
- New-only output/partial-write, source/resource/code/target drift and existing
  annotation preservation tested for check and verify. Legacy prompt byte baselines,
  M2/P02, planning/skill/protocol contracts pass in full regression.

Environment: Python3.14.4, Typer0.27.1, PyYAML6.0.3, pytest9.1.1, markdown-it-py4.3.0.
Runtime receipts: `.karakana/reviews/20261114-kdx11-s2/verification.json`,
`pytest-full.*`, `gates.json`, individual gate stdout/stderr, actual CLI receipts
and fresh example bundles. Source manifest and handoff are linked by exact trace.

Self-review inspected actual producer/consumer/status/capture/write/verify paths
and contrary states; no blocking finding remains in inspected scope. It is not
independent review, Windows qualification, model obedience, evidence authenticity
or recipient acceptance. Bounded local consistency is not an adversarial concurrent
filesystem transaction. KDX10 evidence holds remain outside this qualification.

State: S2 implemented/locally verified on task branch; owner delivery acceptance,
publication/PR/exact-head CI and squash merge pending; no deployment. Review this
completed S2 scope and evidence. On acceptance, use standing normal validated
publication/PR/squash authority, verify exact source/tree/parent and postmerge gates,
then return to the selected project-document drafting task with its own handoff.
S2 delivery acceptance is not automatic operational/product acceptance. No further
KDX11 research/design/planning task is required.


## Changed files

- `docs/command-reference.md`
- `docs/delivery/2026-11-14-kdx11-s2-assessment.md`
- `docs/research/2026-11-14-task-time-content-implementation-plan.md`
- `docs/skills/engineering-artifact-catalogue/content-checks/README.md`
- `docs/skills/engineering-artifact-catalogue/content-checks/check-example.json`
- `karakana/docs/command_reference.py`
- `karakana/document_tasks/__init__.py`
- `karakana/document_tasks/assessment.py`
- `karakana/document_tasks/bundles.py`
- `karakana/document_tasks/cli.py`
- `karakana/document_tasks/inputs.py`
- `karakana/document_tasks/report.py`
- `karakana/document_tasks/schemas.py`
- `karakana/document_tasks/verify.py`
- `skills/engineering-design-records/SKILL.md`
- `skills/engineering-documentation-conventions/SKILL.md`
- `skills/engineering-documentation-conventions/evals/preparation.yml`
- `skills/engineering-documentation-conventions/references/document-map.md`
- `skills/engineering-requirements/SKILL.md`
- `tests/document_task_support.py`
- `tests/test_document_task_assessment.py`
- `tests/test_document_task_bundles.py`
- `tests/test_document_task_cli.py`
- `tests/test_document_task_packaging.py`
- `tests/test_document_task_prepare.py`
- `tests/test_document_task_verify.py`
- `ubongo/projects/karakana/open-issues.md`


## Owner acceptance — 2026-11-14

The owner replied “accepted, when do we start doc refinement?” after the complete
S2 delivery summary. This accepts the implemented/verified S2 scope and limits
without revisions. The standing normal publication/PR/validated squash authority
applies; no separate merge-permission round is required. Prior pending-review
statements are historical checkpoints. Only acceptance-history metadata changes
in this integration; reviewed code/tests/skills/examples remain byte-identical.

Complete exact-head CI and guarded squash integration, record actual tree/parent/
clean-main and postmerge checks in the release trace/handoff, then return directly
to ent-meal document refinement from its own latest handoff. No additional Karakana
feature/research/design/plan task is selected before that. No deployment, product
readiness or authenticated evidence acceptance is inferred. This is the authorised
prepublication checkpoint; final integration receipts govern actual merge state.
