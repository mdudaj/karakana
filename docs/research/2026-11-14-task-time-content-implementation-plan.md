---
status: resolved_no_change
question: Which accepted plan governs the bounded KDX11 S1/S2 implementation sequence against accepted TT01-TT12 and DD01-DD12?
evidence:
  - source: docs/research/2026-11-14-task-time-content-requirements.md
    finding: TT01-TT12/A01-A12 revision0.1 are accepted and merged through PR42; no new requirements round is needed.
  - source: docs/research/2026-11-14-task-time-content-design.md
    finding: DD01-DD12 revision0.1 are accepted and merged through PR43; separate preparation and reporting milestones, exact contracts and safety boundaries already govern.
  - source: karakana/agents/planner.py
    finding: The current composer combines disk reads and rendering; its signature and legacy output can be protected while extracting the accepted pure renderer.
  - source: karakana/skills/loader.py
    finding: Existing skill parsing and metadata-to-Skill construction should be shared with captured preparation rather than copied.
  - source: karakana/tools/engineering_content.py
    finding: Existing check_content/verify_report APIs own M2 assessment and raw saved-report verification; the new adapter must preserve those contracts.
requirements:
  - decision: Reuse TT01-TT12 unchanged, delivering the S1 preparation subset first and the remaining S2 reporting/verification behavior second.
    acceptance: The coverage table assigns every A01-A12 criterion to a milestone, concrete test surfaces and actual future proof; partial scope is never reported as whole-feature completion.
    artifact: docs/research/2026-11-14-task-time-content-requirements.md
design:
  - choice: Reuse DD01-DD12 unchanged; IP01-IP08 specify exact file ownership, task sequence, fixtures, compatibility tests and review/recovery gates without adding architecture or policy.
    rationale: The direction is settled. Splitting prompt preparation from persisted assessment verification provides useful reviewable outputs and isolates failure diagnosis.
    artifact: docs/research/2026-11-14-task-time-content-design.md
artifact_choices:
  - kind: requirements
    disposition: reused
    path: docs/research/2026-11-14-task-time-content-requirements.md
    rationale: Accepted problem, users, behavior, quality and A01-A12 criteria govern implementation.
  - kind: design
    disposition: reused
    path: docs/research/2026-11-14-task-time-content-design.md
    rationale: Accepted interfaces, resource precedence, state/authority, UX, freshness and two-slice decisions remain authoritative.
  - kind: implementation_plan
    disposition: updated
    path: docs/research/2026-11-14-task-time-content-implementation-plan.md
    rationale: One compact milestone, task, verification, artifact-readiness and delivery record; no duplicate PRD, ADR or native issue store.
  - kind: backlog
    disposition: updated
    path: ubongo/projects/karakana/open-issues.md
    rationale: Record accepted planning round and separate S1 execution continuation without reopening earlier approvals.
  - kind: executable_schema
    disposition: not_applicable
    rationale: Executable schemas, examples and tests are named below for implementation; this planning round writes no runtime code or schemas.
authority:
  state: approved
  evidence: Owner replied accepted on2026-11-14 after the self-contained IP01-IP08 revision0.1 summary, without revisions. Standing acceptance-means-normal-validated-documentary-PR/squash authority applies. resolved_no_change closes this planning round without runtime changes; S1/S2 execution remains separately selected.
pending_decisions: []
next_action: Complete validated documentary PR/squash integration of accepted IP01-IP08 revision0.1, then present the exact S1 implementation task brief; do not execute code from plan acceptance alone.
---

# KDX11 task-time content implementation plan

| Plan information | Value |
| --- | --- |
| ID / revision / date | KDX11-TT-PLAN / 0.1 / 2026-11-14 |
| Source baseline | `29df39d6275f2702adf49e5e86aa65c847e9b544`, clean merged design PR43 |
| Governing requirements | [TT01-TT12/A01-A12 revision0.1](2026-11-14-task-time-content-requirements.md), accepted PR42 |
| Governing design | [DD01-DD12 revision0.1](2026-11-14-task-time-content-design.md), accepted PR43 |
| Current authority | IP01-IP08 revision0.1 accepted by owner; S1/S2 code execution remains separate |
| Ownership / forecast | Project owner accepts scope; the selected implementing agent owns each slice and its evidence. No calendar/effort commitment has been agreed. |

## Outcome, stories and bounded choices

As a task author, I can prepare a scoped prompt from explicit document resources
without running a model or content checker (S1; A01-A05/A09-A12 preparation subset).
As a reviewer or automation consumer, I can check selected content and verify saved
results without mistaking completeness/freshness for acceptance (S2; all applicable
A01-A12 including saved-report and typed-state negatives).

This plan operationalises accepted direction; it does not select another milestone,
rewrite contracts or start implementation. The accepted tailored standards/UX
references in TT/DD remain applicable; no new external research is necessary to
choose files/tests. Actual project-document drafting can already use existing
skills/templates and is not conditional on this optional automation.

| ID | Accepted delivery rule |
| --- | --- |
| IP01 | Deliver S1 resource selection/captured preparation first; expose only `docs content prepare` and explicit not-assessed content states until S2 is delivered. |
| IP02 | Deliver S2 actual M2 check/verify and two-layer saved-bundle verification only after S1 is verified, accepted and squash merged. |
| IP03 | Keep new request/policy/result/bundle behavior in `karakana/document_tasks/`; share existing parsing/rendering/path/write helpers and keep CLI glue thin. |
| IP04 | Freeze existing prompt output in compatibility tests before extracting pure rendering/skill construction; preserve legacy signatures, optional-file fallbacks and explicit live behavior. |
| IP05 | Add strict executable request/policy/result contracts and neutral fixtures from the accepted DD definitions; never install an active project policy or copy example facts into project requirements. |
| IP06 | Exercise real API/CLI/packaging and contrary outcomes with temporary roots; each slice runs focused checks, then required full regression/evals and exact-head CI before integration. |
| IP07 | Keep one milestone active, one task branch and one coherent PR per slice; record actual implementation, verification, acceptance, merge and deployment separately, with correction/revert recovery. |
| IP08 | Preserve no-new-stage-gate, no-live-model/source-apply/deployment and native/P02 boundaries. Routine construction may be delegated; a material TT/DD deviation requires a scoped amendment, not a speculative patch. |

A single large delivery is rejected because it combines prompt compatibility and
saved-result integrity into one debugging/review boundary. Smaller code-layer-only
slices would leave no usable command. S1's usable preparation and S2's complete
check/verify workflow are the preferred boundaries already chosen in DD12.

## Source and file ownership

Inspect the listed existing files before their task; proposed new paths below do
not claim files already exist. Keep executable schemas in owning Python modules,
not a competing Markdown or workbook master.

| Files / responsibility | Milestone and intended change |
| --- | --- |
| `karakana/document_tasks/__init__.py` | S1: package/version and public local API; no eager optional-parser import. |
| `karakana/document_tasks/schemas.py` | S1: strict request0.1/policy0.1 and prepare result0.1 validation/typed failures; S2: assessment result/bundle validation. Reuse M2 strict JSON behavior; don't fork M2 context/report semantics. |
| `karakana/document_tasks/selection.py` | S1: fixed two-type recommendations, explicit selections, defaults/locks/origin/override resolution; no recursive catalogue scan. |
| `karakana/document_tasks/inputs.py` | S1: bounded capture, deduplicated physical inputs, guard/recheck, optional-file presence and wrapper code fingerprint; S2: reuse for independent saved-wrapper provenance. |
| `karakana/document_tasks/prepare.py` | S1: capture fixed Ubongo/project/skill/planner inputs and selected resources, build shared planning inputs, append literal resource context, no check/model call. |
| `karakana/document_tasks/report.py` | S1: result builder, plain text/clean JSON and deterministic diagnostics; S2: preserve raw M2 report and typed state/freshness mapping. |
| `karakana/document_tasks/bundles.py` | S1: reserve fresh runtime directories and guarded prompt/result writes, partial-failure handling; S2: bare report/result equality, new verification bundles. |
| `karakana/document_tasks/cli.py` and `karakana/cli.py` | S1: thin nested `docs content prepare` registration; S2: add check/verify. Avoid changes to unrelated commands. |
| `karakana/agents/planner.py` | S1: extract `PlanningInputs`/pure rendering; preserve current `compose_planning_prompt` signature, loader behavior and old writer. |
| `karakana/skills/loader.py` | S1: extract shared pure metadata-to-Skill construction from captured Markdown; legacy SkillLoader delegates without semantic/metadata changes. |
| `karakana/document_tasks/assessment.py`, `karakana/document_tasks/verify.py` | S2: exact M2 API delegation, strict producer validation, raw-plus-wrapper recomputation and refusal semantics. |
| `karakana/memory/ubongo.py`, `karakana/memory/schemas.py`, `karakana/models/router.py`, `karakana/protocols/lifecycle.py` | Inspect/reuse required file lists, pure memory rendering, deterministic route guidance and lifecycle prompt. No policy/routing changes are planned. |
| `karakana/content_profiles/{schemas,loader,report}.py`, `karakana/tools/engineering_content.py`, `karakana/tools/engineering_artifacts.py` | Inspect/reuse context versions, registered profiles, raw check/verify, path bounds and `write_new`; no M2/P02 behavior change is planned. |
| `docs/command-reference.md`, `docs/skills/engineering-artifact-catalogue/content-checks/README.md` | Each slice: regenerate supported CLI reference and document actual available commands/states. No S2 support claim at S1. |
| `skills/engineering-documentation-conventions/references/document-map.md`; owning requirements/design/conventions `SKILL.md` files | Update only affected current-capability statements and version metadata with each delivered slice; keep explicit opt-in and P02 limits. Relevant instruction evals change only when behavior/instruction coverage warrants it. |
| This plan and `ubongo/projects/karakana/open-issues.md` | Append actual delivery/verification/acceptance history at each checkpoint; retain previously accepted artifacts unchanged unless a scoped correction is needed. |

`pyproject.toml` remains unchanged unless actual packaging evidence reveals a
specific blocker; automatic discovery already includes `karakana*`. Do not package
the skill catalogue, add dependencies or weaken parser optionality. Test package
boundaries rather than assuming an installed wheel contains checkout assets.

## S1 — usable explicit preparation

Prerequisites: accepted TT/DD, accepted plan, explicit S1 execution selection;
fresh task branch from current main; no unresolved material contract departure.
The S1 implementer owns the tasks and receipts; the project owner reviews delivery.

| Task / purpose | Ordered instructions and inspected evidence | Check / expected observation |
| --- | --- | --- |
| S1.1 Protect existing rendering | Read planner, SkillLoader and actual planner/plan/Codex/live tests. Add golden equivalence cases covering normal/missing optional files, skillpack context and explicit model_route; extract pure rendering/skill construction without changing legacy calls. | Existing and new compatibility tests compare full prompt bytes, metadata, signature behavior and fallbacks, not just headings. No model invocation. |
| S1.2 Resolve explicit requests/resources | Implement accepted strict request/policy shapes, bounds, physical capture and exact two-type inventory. Follow task → opted-in defaults → unselected recommendations precedence; enforce applicable locks, origin/revision basis and safe failures. | Request/policy/selection tests cover duplicates, unknown versions/types, no-selection, overrides, missing/conflicting locks, wrong project, outside-root/secret/symlink and file/byte limits. |
| S1.3 Build captured preparation | Use required memory filename constants and pure ProjectMemory/Skill rendering from captured bytes; include applicable AGENTS/KARAKANA/planner template and only explicit selected resources. Parse optional context declarations without reading document sources or importing the parser. | Read spies prove no unselected resource/project/source traversal. Changed bytes/targets/optional-file presence refuse before output. Synthetic examples remain labelled; no invented facts. |
| S1.4 Return and save the operation | Implement prepare result0.1, literal summary/diagnostics and new-only bundle writes; add CLI prepare only. Reserve exclusive directories, bound JSON output and handle partial writes without a success claim or source deletion. | Real subprocess and CliRunner outcomes: selected and unselected success0; semantic request/path/policy/output failures2 with clean JSON; CLI syntax2 on stderr with empty stdout; source/old output byte preservation. |
| S1.5 Document and qualify S1 | Add neutral request/policy examples, actual CLI docs and current skill guidance; verify absent parser still allows preparation and unselected resources remain unopened. Run the focused S1 commands, then full required gate. | Actual `prompt.md`/`result.json`; content_report null, saved verification not_assessed, no check/verify claim. Current direct plan/Codex/P02 behavior preserved. |

S1 exit: a reviewer can invoke prepare for a real scoped request, inspect selected
resource provenance and the generated prompt, and reproduce the failure matrix.
All S1 checks and full required regression/evals pass; review resolves blocking
findings; owner delivery acceptance and validated squash integration are recorded.
This is partial KDX11 completion: S2 criteria remain explicitly unimplemented.

## S2 — actual checking and saved-bundle verification

Entry: S1 accepted/merged source and evidence verified; exact current requirements,
design and plan still applicable; separate S2 implementation selection/trace. Do
not begin S2 code on the S1 branch while S1 review/integration is pending.

| Task / purpose | Ordered instructions and inspected evidence | Check / expected observation |
| --- | --- | --- |
| S2.1 Integrate M2 assessments | Inspect actual M2 check/verify/schema/report and tests. Add lazy direct API adapter and producer validation; preserve every document, finding, coverage and authority field. Validate task types against context profile types; never silently filter a context. | Actual two-profile/context0.1/0.2 positives, frontmatter/unknown profile/links0.1/parser absence and missing input refusals. Invalid/missing producer fields and exit0 blocked/not_ready controls cannot produce success. |
| S2.2 Write typed check bundles | Extend report/bundles with exact M2 report0.2 copies and independent wrapper manifest; emit raw `content-report.json` plus result.json, correct text/JSON/exit semantics and explicit unassessed scope. | Complete-with-gaps may exit0 but remains review_required/unresolved/not_assessed; incomplete/unsupported/output failure exits2. Raw report and nested copy equal, protected sources unchanged. |
| S2.3 Recompute saved verification | Validate saved bundle/version/operation and both report copies; call existing verify_report on the bare report, independently re-resolve current wrapper inputs and compare every deterministic field. Normalize only the accepted volatile metadata, and retain raw-current versus wrapper-stale distinction. | Document/evidence/context/resource/policy/optional-presence/profile/parser/checker/wrapper-code/scope/revision/target and saved-field tampering refuse. Verify check and successful verify bundles; reject prepare-only/foreign/partial bundles; write new output only. |
| S2.4 Qualify and document whole feature | Add check/verify CLI registration and neutral saved-bundle cases; complete actual text/JSON/exit matrix, optional parser and installed-wheel context-only proof; update guidance and run focused then full required gate. | Actual commands match accepted DD contracts, no new native/P02/export/gate/model behavior; whole-feature A01-A12 coverage demonstrable before acceptance/integration. |

S2 exit: every applicable A01-A12 case is demonstrated through actual local API/
CLI outcomes, saved reports are revalidated rather than trusted, full checks pass,
blocking review findings are closed and owner acceptance/validated squash are
recorded. No deployment or recipient acceptance is inferred.

## Fixtures, coverage and test ownership

New test files and fixture paths below are proposed implementation outputs.
Use temporary roots for anything writing harness runtime; never real checkout
.karakana. Place neutral fixture request0.1/policy0.1 and complete/warning/gap/
unsupported/tampered saved-bundle variants under
`tests/fixtures/document_tasks/`; label synthetic facts. Generate report metadata
from actual tool calls in temporary tests rather than checking in machine-specific
absolute paths or accepting edited expected passes. Reuse existing narrative
fixtures and examples through explicit test copies; don't change their facts.

| Criteria / decision | Owning planned tests | Milestone evidence |
| --- | --- | --- |
| A01-A02 / DD01-DD03 | `tests/test_document_task_selection.py`, `tests/test_document_task_cli.py` | S1 action/type/audience/project identity, unselected recommendations/default opt-in/lock/override cases; S2 matching context scope |
| A03 / DD03-DD04/DD11 | `tests/test_document_task_inputs.py`, `tests/test_document_task_prepare.py` | S1 bounded exact reads and no implicit file/network/model/subprocess actions; S2 separate unchanged M2 input budget |
| A04-A05 / DD01/DD05/DD11 | `tests/test_document_task_prepare.py`, `tests/test_document_task_assessment.py` | S1 no check/parser/source reads during preparation; S2 actual supported/unsupported check invocation |
| A06 / DD06/DD08/DD10 | `tests/test_document_task_assessment.py`, `tests/test_document_task_cli.py` | S1 no fabricated assessment; S2 typed missing/blocked/not_ready/malformed producer/complete-with-gaps controls |
| A07 / DD04/DD07 | `tests/test_document_task_inputs.py`, `tests/test_document_task_verify.py` | S1 captured bytes/presence/target/code provenance; S2 complete saved-field recomputation/tamper/reordering/volatile-metadata matrix |
| A08-A09 / DD06/DD08 | `tests/test_document_task_assessment.py`, `tests/test_document_task_verify.py` | S1 no automatic authority side effects; S2 preserve scoped gaps/resolver/unknown details and changed-revision review boundaries |
| A10-A11 / DD06-DD07/DD09-DD10 | `tests/test_document_task_cli.py`, `tests/test_document_task_bundles.py` | Both slices actual literal text/JSON/exit/output-refusal behavior; S2 actual check/current/stale/unsupported state combinations |
| A12 / DD01/DD04/DD07/DD11 | Existing planner/skill/plan/Codex/live/docs/M2/P02 tests plus `tests/test_document_task_packaging.py` | Both slices legacy equivalence, no overwrite/partial-success, deterministic semantics and wheel/optional-parser boundaries |

Coverage rows explicitly include A01 through A12 even when criteria are grouped.
Existing instruction evals prove instruction coverage, not model obedience, actual
document acceptance or evidence authenticity. Add assertions to the owning suite
for changed instructions, not tests that only restate the implementation.

## Verification commands and release gates

Run a task-specific pre-implementation protocol check after attaching accepted
TT/DD/plan, scope/readiness and the applicable evidence. A presence pass is not
approval or a passed test; inspect actual artifacts and owner authority.

S1 focused gate, after the proposed tests exist:

```bash
.venv/bin/pytest -q tests/test_document_task_selection.py tests/test_document_task_inputs.py tests/test_document_task_prepare.py tests/test_document_task_bundles.py tests/test_document_task_cli.py tests/test_document_task_packaging.py tests/test_planner.py tests/test_skill_loader.py tests/test_plan_cli.py tests/test_codex_cli.py tests/test_live_plan_cli.py tests/test_docs_commands.py
```

S2 focused gate:

```bash
.venv/bin/pytest -q tests/test_document_task_assessment.py tests/test_document_task_verify.py tests/test_document_task_bundles.py tests/test_document_task_cli.py tests/test_document_task_packaging.py tests/test_engineering_content.py tests/test_engineering_content_context.py tests/test_engineering_content_packaging.py tests/test_engineering_artifacts.py
```

Each slice's stabilised final regression gate:

```bash
.venv/bin/pytest -q
.venv/bin/karakana skill validate-all
.venv/bin/karakana eval run
.venv/bin/karakana docs check
.venv/bin/karakana memory validate --project karakana
git diff --check
```

Also validate any changed skillpack/workspace configuration only if such a change
is actually justified. Inspect real CLI help and generated command-reference
output; test new command text and JSON through subprocesses, not just help strings.
Exercise installed-wheel imports outside the source checkout, with and without
the optional parser: preparation needs selected checkout assets; context-only M2
checking can use packaged profiles. No network credentials/live models are needed.

Before publication: self-review exact diff and unresolved risks; record commands,
environment/source hashes and actual results, attach required artifacts and
refresh exact-trace handoff. On accepted delivery, validate applicable PR checks
on the exact head, squash merge and verify resulting source/tree/parent, clean
main and postmerge release check. No direct protected-branch commit/push.
Don't repeat successful broad gates without a new change/failure/concern.

## Artifact readiness, stop conditions and recovery

| Artifact / state | Disposition and effect |
| --- | --- |
| Requirements, criteria and intended users | Reuse accepted TT record; two scoped user stories above add no product scope. |
| Design/decision, UX and source contracts | Reuse accepted DD record including literal output, failure matrix, request/policy/result/bundle and version boundaries. |
| Milestone/traceability/Definition of Done | This plan's S1/S2 entry/exit, ordered tasks, coverage and gate sections; owner plan acceptance pending. |
| Executable schemas/examples/tests and actual delivery evidence | Implement only in authorised S1/S2; planned checks are not passed results. |
| Production deployment, migration, auth changes, external reader evidence | Not applicable: local opt-in CLI feature, no production/state migration or acceptance outreach selected. |
| Handoff | Always append-only and bound to exact task trace; current review summary must be exposed on actual load. |

Current blocker to code: owner plan review and separate milestone execution
selection; owner is the Karakana project owner. No new missing site fact or
unsettled architecture prevents plan review. Routine internal function naming
can be chosen by the implementer within the listed ownership and accepted contracts.

Stop an affected implementation if source invalidates TT/DD assumptions, a necessary
dependency/schema/policy change exceeds scope, or an accepted behavior cannot be
preserved. Bring the exact evidence and a bounded amendment/replan. After two
unsuccessful diagnostic attempts on the same issue, stop speculative patches and
carry the failed-attempt count into the handoff; model escalation is advisory.

Recovery: on refusal retain sources and pre-existing outputs; never force an
overwrite or fabricate a current/accepted state. Isolate unrelated safe work.
Before merge, fix the task branch; after integration use a reviewed correction/
revert PR for the exact slice, preserving acceptance history. No reset of main,
database operation, live call or deployment is needed. Partial nonempty runtime
bundles remain clearly incomplete evidence; don't delete user annotations.

## First execution brief and prior review checkpoint

**S1 execution brief after plan acceptance:** load the current Karakana handoff,
verify accepted TT/DD/this plan and clean current main; create one S1 task branch
and implementation trace. Attach governing artifacts and scope/readiness, run the
pre-implementation gate, then execute S1.1-S1.5 in order. Deliver working explicit
prepare, guarded new-only prompt/result output, unchanged legacy prompt bytes,
no-check/unselected/failure states, focused/full test/eval receipts and exact-trace
handoff. Stop before S2. No new active policy, automatic gating or model execution.
User delivery review/acceptance precedes normal validated PR/squash integration.

Current task: plan authored only; no feature code, fixtures, executable schemas,
new tests, live actions, merge or deployment. Owner review of IP01-IP08 revision0.1
is pending. After acceptance, record actual words/revision here, follow the standing
validated documentary PR/squash convention, then offer the exact S1 task brief.
Do not treat plan acceptance alone as execution selection.

Recommend GPT-6 Sol medium for bounded plan review and high for later provenance/
workflow integrity implementation; routing recommendations do not identify or
switch the active session or certify availability. Continue plan review here;
a fresh conversation benefits S1 after the approved handoff. KDX10's held
authentic-action and sibling-project evidence remains separate.

## Planning-round checks before acceptance

51 existing documentation/planner/loader/protocol/CLI/docs-command tests passed
in2.80s; delivery-planning instruction evals4/4 passed with zero warnings
(`20261114-093112-eval-4c5f4c`); project memory validation passed. Local links,
research-closeout structure, IP01-IP08, nine ordered tasks, coverage of all12
criteria, existing test paths, two-document scope and whitespace checks passed.
The route query recommends Sol/medium for bounded planning; no active-model
identity or switch is inferred. These checks validate this plan and existing
compatibility, not the proposed feature, future tests or owner plan acceptance.

## Owner acceptance — 2026-11-14

The owner replied **“accepted”** after the self-contained IP01-IP08 revision0.1
summary. This accepts the eight delivery rules, nine ordered tasks, file ownership,
acceptance/test mapping, verification/recovery gates and S1-before-S2 sequence
without revisions. Earlier pending/proposed wording is the prior review checkpoint;
plan acceptance is no longer outstanding. Task rows, rule rows, code examples and
verification commands were not changed by this acceptance update.

The standing agreement authorises normal validated documentary PR/squash
integration of this completed plan. Present S1's bounded execution brief next.
This acceptance does not start S1/S2 code, add automatic gates, invoke models or
deploy. TT/DD approvals remain settled, and KDX10's independent evidence holds
remain open. Exact integration/continuation receipts belong to the release
trace and append-only handoff; actual project-document drafting is independent.
