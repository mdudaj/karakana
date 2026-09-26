# Engineering process

Status: accepted harness process, 2026-09-26. Applies to Karakana-managed tasks;
project contracts and authorization boundaries remain in force.

## Research and rationale

This is a tailored engineering workflow, not a claim of standards certification.
Only public summaries of the ISO/IEEE standards were reviewed, not their paid
normative text. Sources checked on 2026-09-26:

| Reference | Application here |
| --- | --- |
| [ISO/IEC/IEEE 12207:2026](https://www.iso.org/standard/90219.html) | Consider the lifecycle from requirements through operation and retirement; processes can be iterative rather than a fixed waterfall. |
| [ISO/IEC/IEEE 29148:2018](https://standards.ieee.org/ieee/29148/6937/) | Keep requirements, acceptance evidence and changes traceable. |
| [NIST SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final) | Integrate security into the existing lifecycle rather than adding a final security-only stage. |
| [OWASP SAMM](https://owaspsamm.org/model/) | Include governance, design, implementation, verification and operations in improvement planning. |
| [DORA small batches](https://dora.dev/capabilities/working-in-small-batches/) and [test automation](https://dora.dev/capabilities/test-automation/) | Deliver bounded changes with fast feedback and regression protection. |
| [Google engineering review](https://google.github.io/eng-practices/review/reviewer/looking-for.html) | Review design, functionality, complexity, tests and documentation, not merely style. |
| [W3C accessibility planning](https://www.w3.org/WAI/planning/) | Include accessibility in planning and evaluation throughout UX delivery. |

These sources inform the policy below; the precise gates, commands and artifact
mapping are Karakana design decisions, not requirements attributed to a standard.

## Current harness audit

| Finding | Evidence | Disposition |
| --- | --- | --- |
| Classification, task-specific protocols, conditional artifacts and approval gates already exist. | `karakana/protocols/`, `protocols/`, `skillpacks/` | Extend these; do not create another orchestration framework. |
| A missing artifact path is returned as evidence and passes the gate. Arbitrary output values also count. | `protocols/checks.py::_artifact_evidence` | Require accessible, nonempty files for file evidence; retain explicit inline classification only. |
| Completion checks require output artifacts even before implementation. | `check_trace_protocol_artifacts` | Add a pre-implementation stage which defers only delivery outputs. Default completion still checks all required artifacts. |
| Instructions exist in skills but generated task prompts do not consistently carry a shared engineering lifecycle. | `agents/planner.py`, `tools/codex_executor.py`, `codex/handoff.py`, `protocols/start.py` | Inject one shared compact process contract into all four surfaces. |
| Artifact presence is not proof of correct requirements, passing tests, approval or deployment. | Existing alias-based checks | State the limit in machine-readable check metadata and agent instructions. Require substantive review of evidence. |
| Recovered handoff includes unrelated concepts and test-generated planning artifacts. | Handoff `20260926-061008-handoff-14c610` | Follow-up: isolate test runtime and enforce project provenance in recovery. Do not silently rely on these references. |
| Project overview is a placeholder; contract's execution status is stale. | `ubongo/projects/karakana/overview.md`, `KARAKANA.md` | Correct the overview and stale status; do not infer production deployment. |

## Lifecycle and decision gates

Stages are iterative. Reopen only the affected stage when evidence, scope or risk
changes. Reuse approved current artifacts; a small task can use one compact record
covering several concerns, with explicit sections and links rather than duplicates.

| Stage | Required decision / evidence before proceeding |
| --- | --- |
| Orient and classify | Verify project, repository, branch, current handoff, request type and authority. Identify risk, affected users/subsystems and governing skills. Analysis is not authorization to implement. |
| Define | State the bounded outcome, non-goals and observable acceptance criteria. Link existing requirements; resolve material ambiguity. Record changes to agreed scope instead of silently enlarging it. |
| Research and design | Inspect current code, contracts and tests; research only unresolved questions using authoritative sources. Record alternatives and trade-offs for consequential decisions; include UX, security, privacy, data and operational effects when applicable. |
| Plan | Name affected files, steps, test cases, regression scope, approvals and rollback when relevant. Run the pre-implementation artifact gate for non-trivial implementation. |
| Implement | Work on a task branch in small reviewable changes. Reproduce bugs and add a failing regression test when feasible. Extend established abstractions; do not implement speculative future features. Stay within approved scope. |
| Verify and validate | Verify against specifications with focused tests then the required broader suite. Validate user outcomes through relevant browser, accessibility, data or operational checks. Record commands, results, environment/revision, omissions and residual risk. |
| Review and integrate | Review the diff and acceptance evidence. Resolve P0/P1 findings. A self-review is not an independent review. Check artifacts at completion; publish/merge only with authorization and required CI/review. |
| Release and operate | Only for authorized release tasks: identify immutable release, target, backup/rollback, configuration and monitoring; verify after deployment. Merged, deployed and accepted are different states. |
| Handoff and improve | Record exact completion state, unresolved work, recommended next task/model/conversation and evidence. Encode repeated failures into a regression guard. Never call unrun checks passed. |

The requester owns intended outcomes and scope approval; the agent proposes and
implements within that scope; reviewers assess the diff and evidence; authorized
operators approve/perform releases. Role names do not imply separate agents or
automatic delegation. Record who reviewed and do not label self-review independent.

Before implementation, acceptance criteria must be observable and the test plan
must address applicable quality attributes: correctness, security/privacy,
accessibility, reliability, performance, compatibility and maintainability.
Before calling a slice complete, required checks must pass and blocking findings
must be resolved. If a check cannot run, state the limitation and do not claim the
associated behavior verified; distinguish local implementation from acceptance.

## Proportional application

- Analysis/research/review: findings, evidence and handoff; no implementation ADR
  or rollback unless the task actually makes a consequential decision/change.
- Tiny mechanical/docs-only work: concise intent, diff review and applicable
  validation. No new PRD or ADR just to satisfy ceremony.
- Bug fix: observed failure, cause evidence, regression test where feasible and
  relevant integration checks. After two unsuccessful diagnostic attempts, stop
  speculative patches, summarize findings and replan.
- Feature/refactor: reuse or refine requirements, architecture and test strategy.
  UX work includes behavior, look/feel, state, copy, accessibility and render checks.
- Security/data/workflow/release: use the specialized protocol, threat/abuse or
  integrity checks, compatibility/migration and recovery evidence as applicable.
- One compact file may cover multiple artifact kinds only if it genuinely
  contains their content. Attaching an unrelated file is not compliance.
- Non-applicability must be justified and reviewed in the scope record. There is
  no generic CLI bypass for missing required artifacts; use the correct protocol.
- Slice approval covers ordinary in-scope implementation steps, not new scope,
  credentials, live model calls, remote publishing or deployment permissions.

## Commands and enforcement boundary

```bash
karakana handoff load --project <project> --skillpack <skillpack>
karakana protocol start --task "<bounded outcome>" --project <project> --write-plan
karakana protocol attach --trace <id> --kind <kind> --path <evidence-file>
karakana protocol check --trace <id> --stage pre-implementation
# Implement, test, review and attach the resulting evidence.
karakana handoff refresh --project <project> --skillpack <skillpack> --next-task "<next action>"
karakana protocol attach --trace <id> --kind handoff --path <new-handoff.md>
karakana protocol check --trace <id> --stage completion
```

Refresh again when necessary to record the final check result. The initial
handoff may record an outstanding check; it is not a claim of completion.

The pre-implementation check defers change summary, verification summary,
render evidence and handoff. Other required artifacts are checked. Completion is
the default for compatibility. A pre-implementation pass is never a completion
pass. Stage is recorded in check metadata and CLI output.

Checks validate artifact **presence**, not semantic quality or authenticity.
They do not execute commands, grant approval, prove all tests passed or guarantee
an agent followed instructions. Attached local evidence must be a readable,
nonempty regular file; a directory, missing path or bare output string is not
evidence. Legacy output paths are supported only if they resolve to such files.
Inline protocol classification remains supported as structured trace metadata.
External evidence should be summarized in a local review record with its source,
revision, outcome and limitations; the harness does not fetch remote artifacts.

These are CLI checks plus shared agent instructions, not a shell-interception
system. Existing patch/handoff protocol checks remain explicit; no hidden model
execution, automatic stage advancement or new live actions are introduced.

## This update: requirements, architecture and delivery plan

Outcome: agents receive consistent lifecycle guidance and stage-specific checks
cannot pass on nonexistent file evidence. User approved local process updates,
then accepted review/integration with "acceptable, continue" on 2026-09-26.
Integration scope: commit the reviewed change, publish a task-branch PR, wait for
required CI and squash merge. No deployment or live model execution is included.

| Requirement | Implementation | Verification |
| --- | --- | --- |
| ENG-1: Reject missing, empty, directory and non-file output evidence. | `protocols/checks.py` | File-evidence regression tests, valid legacy file paths still pass. |
| ENG-2: Check prerequisite artifacts separately from outputs. | `protocols/lifecycle.py`, checks and CLI | Pre-implementation passes without delivery outputs; completion fails until they exist; unknown stage rejected. |
| ENG-3: One shared lifecycle contract in every primary task-generation path. | Protocol start, planner, Codex prompt and handoff renderers | Generated-output integration tests. |
| ENG-4: Tailor process, preserve safety and distinguish presence from truth. | This document, delivery skill, global memory and AGENTS | Instruction eval plus manual diff/contract review. |

ADR: extend the existing checker with an optional stage and a shared lifecycle
renderer. Do not introduce a second task state machine, automatic authorization,
or semantic certification from arbitrary files. Default completion preserves
call signatures; legacy false-positive evidence intentionally stops passing.
Tests must use temporary repositories to avoid contaminating handoff recovery.

Implementation order: write regression tests; confirm failures; add lifecycle
module and evidence checks; wire CLI and prompt surfaces; update concise entry
instructions; run focused tests then full pytest, skill/protocol validation and
deterministic evals. Review diff for scope and compatibility.

Rollback: revert this task's changes through a reviewed patch, without deleting
runtime traces or handoffs. Prefer repairing broken legacy evidence paths over
restoring false-positive passes. No schema migration or deployment is involved.

## Verification and remaining work

- Regression-first: 13 failing tests reproduced the missing checks; one legacy
  valid-file case passed before the implementation.
- Focused suite: 48 tests passed after implementation.
- Full suite: 566 tests passed again in `/tmp/karakana-engineering-tests.GtR5e9`, a copy
  of tracked/nonignored task files, using the repository virtual environment.
- Deterministic evals: 145 passed. Skills, protocols and project memory validate.
- Skillpacks validate with existing missing-memory warnings for billing,
  msc-research and nhrdm; no new warnings introduced.
- Diff whitespace check passed. No live model calls or deployment. Agent
  self-review performed; user accepted integration. This is not a claim of
  independent technical review. Integration results are recorded in the handoff.
- Completion artifact check and handoff doctor passed (trace
  `20260926-063900-ec75bd`). These establish presence/structural validity only.
- Recommended follow-up after integration: fix project-provenance
  filtering and test-runtime isolation in handoff recovery as a separate slice.
