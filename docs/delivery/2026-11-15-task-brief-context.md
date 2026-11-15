# KDX-12: first-encounter task brief context

## Problem, scope and authority
A developer encountering a task for the first time needs to know the product,
related feature, affected people/workflow and why the task matters before its
technical instructions. The EDCS jobs brief exposed this gap: task mechanisms
were explained, but the product/feature relationship was assumed. User asked to
research the improvement and update the harness on15 November2026. This authorizes
local guidance, prompt/rendering, regression/eval and memory changes. Publication,
merge, live model calls and changing execution/approval policy are outside scope.
EDCS jobs work is held while this harness correction is delivered.

Current public base3278889 includes KDX11 S2, shared documentation conventions,
explicit next_task_brief loading and sourced handoff quick references. Original
root254d463 has unrelated dirty governance/EDCS work and older Karakana memory;
all source changes belong in isolated feat/task-brief-context-20261115. Preserve
root929-file/index/head baseline. KDX09 viewer remains deferred; KDX10/11 histories
are not reopened or silently reclassified.

## Research resolution and applicability
Primary references checked15 November:
- [arc42 introduction/goals](https://docs.arc42.org/section-1/): driving goals,
  essential features, stakeholders and their expectations establish orientation.
- [C4 system context](https://c4model.com/diagrams/system-context): start with the
  system, people and relationships before low-level technologies.
- [Shape Up pitch](https://basecamp.com/shapeup/1.5-chapter-06): a concrete problem,
  boundaries and exclusions let an unfamiliar team understand and judge the work.
- [GitHub task guidance](https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results):
  a scoped problem, acceptance criteria and relevant files support actionable tasks.
These are architecture/team/agent documentation methods, not evidence that a
particular prompt improves model performance or establishes ISO conformance.
Synthesis: a small orientation block plus existing scope/acceptance/instructions.
No mandatory diagram, full PRD duplication, inferred feature taxonomy or invented
business benefit. Human first-encounter review remains necessary.

Alternatives: documentation-only is cheapest but leaves generated tasks without
visible context; a new mandatory readiness/execute gate would break legacy tasks
and KDX11's explicit advisory boundary. Select shared conditional guidance,
reusable blank template and an optional authored brief_context map in existing
Codex metadata, visibly reporting missing context. No execution gate/schema/version
migration. Completeness is structural; never correctness, readiness or approval.

## Requirements, story and observable acceptance
Story: as a developer new to the project, I can explain what product and feature
this task serves, for whom, why now and what changes, using the opening brief.
- R1: introduce project purpose and related feature/capability in plain language;
  IDs/acronyms alone and links alone are insufficient. Expand local abbreviations.
- R2: name affected people/workflow, problem/relevance now, current state/prerequisites,
  intended outcome and scope/authority. Distinguish current/target and accepted/
  proposed facts. Keep the orientation before technical execution/model metadata.
- R3: reference governing evidence without copying whole histories; provenance
  and staleness still need review. Missing facts stay explicitly unconfirmed.
- R4: manual task/next-task briefs, planning guidance, Codex handoffs and durable
  session next_task_brief authoring share the contract. Guidance is conditional
  on creating a brief and must preserve inquiry/review/document action types.
- R5: existing Codex JSON/metadata remains readable. Optional brief_context uses
  project_purpose, related_feature, beneficiary, task_relevance, current_state,
  intended_outcome, scope_and_authority strings and references string list.
  Invalid/missing/placeholder values render explicit gaps; never infer project
  purpose, authorisation or stakeholder benefit from a task ID or bundle summary.
- R6: existing redaction applies; references are never auto-loaded. No routing,
  permissions, default document gates, live calls or automatic execution change.
- R7: tests exercise source-to-rendered output and legacy/partial/adversarial
  metadata, redaction, ordering and request-type conditions; evals cover the actual
  guidance paths. Structural passes do not certify model behavior or relevance.
- R8: a fictional worked example and corrected EDCS opening demonstrate the
  first-encounter questions; keep project-specific facts out of global memory.

## Design, artifact choices and implementation instructions
Inspect lifecycle renderers, agents/planner.py, codex/handoff.py and schemas,
handoff summary/load/skill, documentation-conventions and delivery-planning skills,
protocol artifact templates and eval harness. Governance: current AGENTS/KARAKANA,
self-improvement/artifact/handoff skills and accepted KDX11 advisory contracts.
1. Add one pure brief-context helper for labels, explicit-gap assessment, safe
   rendering and conditional authoring guidance. Keep optional data in existing
   metadata; no new authority field participates in execution.
2. Reuse guidance in shared lifecycle; render Codex context immediately below the
   title and before description/technical details. Carry only explicitly authored
   action metadata. Do not auto-fill parent feature from incidental text.
3. Add task_brief protocol template and generic documentation/example. Update
   owning documentation/planning/next-milestone/handoff skills and central global
   preference/process references so chat-written next briefs follow the same rule.
4. Add focused regression tests and deterministic instruction evals; preserve
   legacy task parsing, explicit doc-task semantics and existing safety gates.
5. Run focused then full required pytest/evals/skill validation in temp repositories,
   review actual examples and diff. Save reviewable local commit/patch; no remote
   write without authority. Refresh current project handoff with exact trace.

This compact record owns requirements/story/design/readiness/traceability/plan;
no root PRD, product UX, database migration or independent architecture ADR is
needed. Blank template/example are authoring aids, not new P02/M2 input profiles.
No source/parser contract is silently added to those systems.

## Safety, rollback and definition of done
Threats: fabricated relevance, stale state presented as current, leaked secrets,
reference auto-reading, missing context labelled ready and scope text mistaken for
permission. Mitigate explicit authored data, existing redaction, visible gaps,
no dereference, structural-only status and unchanged execution approvals. Long or
false prose still needs human review; tests cannot establish truth or acceptance.
Rollback the bounded patch on a review branch; optional metadata is ignored by
older renderers and historical artifacts remain untouched. Do not delete artifacts.
Done is R1-R8 implemented/verified locally with source-alignment evidence, full
required checks and refreshed handoff. User acceptance/publication/integration
remain distinct. RecommendedSol/medium, activeidentifier unverified/manual current-
session override; no model switch, paid call or agent fan-out.

## Source-alignment challenge
- Manual brief path: shared convention/owning skills/template -> authored brief;
  test guidance/links and human-review the fictional example; prose truth remains
  outside deterministic enforcement.
- Planning and document preparation: shared lifecycle -> both captured/direct
  renderers; regressions must preserve request-type-specific required_output.
- Action metadata -> Codex task JSON -> renderer: test supplied context survives,
  missing/invalid/placeholder/unknown values remain gaps, legacy payloads load,
  secrets redact and references are never opened. No executor change is permitted.
- Session next_task_brief -> create/refresh/load: preserve existing explicit field
  and append-only/redaction behavior; authoring rule changes, not schema or routing.
Actual verification results will be appended after implementation.

## Implemented result and verification —15 November2026
Implemented shared conditional guidance, authored Codex context before details,
explicit partial/legacy gaps and structural-only completeness, strong existing
redaction in JSON/Markdown and project-override context isolation. Added a blank
protocol task_brief template, first-encounter guide/fictional example, owning
skills/process/global preference and regression/eval coverage. Existing optional
next_task_brief field/load path remains unchanged; its authoring skill now requires
the same opening in actual load output. No schema/migration/routing/execute gate
or default M2/P02 enforcement change. The new briefs.py rendering dependency is
included in existing document-task provenance fingerprints; old bundles require
normal freshness verification, not automatic rewriting.

Focused producer/consumer checks67passed, then33 representative realparser/context
checks after environment repair. Final full pytest:1192passed in69.93s. All190
deterministic evals passed with zero warnings; allskills validate, Karakana
skillpack strict and memory validation pass. Installed wheel preparation/check/
verify tests pass outside the checkout with optional parser absence cases. Tests
and CLI verification ran in temporary source copies/stores, never the working
checkout runtime. Historical S1 prompt hashes were preserved: the one explicitly
added shared guidance block is removed only for historical byte comparison, and
new behavior is independently tested. Human comprehension/acceptance is pending;
structural coverage cannot certify truth, relevance or a model's output quality.

Diagnostic history retained in ignored task runtime: initial import smoke exposed
a dependency cycle through handoff package initialization; deferred existing
redactor import fixed it and normal import/tests pass. Firstfull run used older
rootenv Markdown4.2.0 and returned116parser-dependent failures/1075passed; current
base requires4.3.0. Offline cache lacked pin. Explicit environment replan used a
separate declared-dependency env; secondfull1189passed/3wheel tests failed because
pip was absent. After testtools pip/setuptools/wheel preflight, all3packaging cases
and the finalfullgate passed. No product workaround, skippedtest, dependency pin
change, rootenv mutation, livecall or paid modelretry. Attempt logs remain separate.

Self-review found no unresolved blocking issue. User-visible context labels and
unknown-state recovery copy were reviewed for plain language and no invented
facts/authority; this is developer documentation/diagnostic output, not a new
application screen. Source-alignment claims above are covered by actual field
ordering/save-load/redaction/no-reference-read/project-override/partial-context/
request-type/provenance/legacy cases. Examples remain illustrative. Full current
request readiness covers local patch only; publication/merge/acceptance are pending.
EDCS jobs stays paused. Next action: review this bounded patch and obtain explicit
PR publication/integration authority, then reissue the EDCS jobs brief with its
product/feature relevance before any jobs research/execution.
