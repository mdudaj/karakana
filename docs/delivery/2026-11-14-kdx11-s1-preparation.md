# KDX11 S1 explicit preparation delivery

Trace `20261114-095945-916585`, baseline `500123b`, branch
`feat/kdx11-s1-prepare-20261114`. Owner selected S1 with **“execute”** after its
concrete brief. This authorises S1.1-S1.5 implementation and local verification;
delivery acceptance/integration remains a later checkpoint. Stop before S2.

Current outcome: **S1 implemented, verified and accepted by the owner**.
Normal validated PR/squash integration is authorised. Earlier checkpoints below
are retained; exact publication/merge receipts govern the integration state.

## Governing artifacts and readiness

Reuse accepted [TT01-TT12](../research/2026-11-14-task-time-content-requirements.md),
[DD01-DD12](../research/2026-11-14-task-time-content-design.md) and
[IP01-IP08/S1.1-S1.5](../research/2026-11-14-task-time-content-implementation-plan.md).
They supply requirements, stories, criteria, UX, contracts, traceability and checks.
All are accepted/merged PR42-44; their scope/source was reviewed as current.
This compact record supplies S1 classification, readiness, implementation summary
and later actual verification; no duplicate PRD/ADR or architecture study.

Scope: strict explicit resource requests/policy precedence, guarded captured
inputs, shared pure rendering, `docs content prepare`, new-only prompt/result
bundles, neutral examples, compatibility/negative/packaging evidence and guidance.
No check/verify command, source/parser/model execution, active project policy,
P02 adapter, lifecycle-stage enforcement, dependency or deployment change.
Protocol keyword category `github_ci` does not mean CI workflows are being changed.
Integrity risk is captured source/output provenance and compatibility, not a new
permission policy. Sol/high is the justified recommendation over the handoff's
routine default; actual session identity/availability is not established or switched.

## Implementation instructions and acceptance

Follow S1.1-S1.5 in the accepted plan. Inspect planner/SkillLoader, Ubongo fixed
lists/pure memory rendering, M2 strict JSON/path limits, new-only writer, CLI
registration and existing tests before edits. Capture complete legacy prompt
fixtures before refactoring. Add new behavior only in document_tasks plus bounded
shared renderer/skill construction and CLI registration. Update actual command
and owning skill guidance. Neutral examples do not become product facts.

Done for review when actual selected/unselected preparation, strict request and
policy failures, scoped context-declaration handling, no implicit reads/calls,
bounded path/byte/target/presence drift protection, exclusive output/partial-failure
handling, plain text/JSON/exit states, full legacy prompt equivalence and
wheel/optional-parser boundaries are verified. `content_report` remains null and
content/readiness/acceptance/saved verification unassessed. All planned new tests
must execute with temporary roots; final full pytest/evals/skill/docs/memory/diff
checks and task protocol/handoff follow focused checks.

Existing source authority, instruction review and scope/acceptance distinctions
remain. Guarded failures preserve sources/old outputs and do not block unrelated
tasks. On a material TT/DD departure, stop for a bounded evidence-backed amendment;
after two unsuccessful diagnostics stop speculative edits and replan. Recovery
is a task-branch fix or reviewed correction/revert PR, never force/reset/overwrite.
No production, migration, auth, independent-reader or live-action proof applies.

## Delivery state

Prerequisite inspection complete. Implementation and verification in progress;
no completed S1, owner delivery acceptance, PR/merge or deployment claimed here.

## Implemented S1 and reviewed boundaries

Added the eight-module `karakana/document_tasks/` package and explicit prepare
API/CLI. Strict request0.1/policy0.1, source/context declarations, two-type resource
inventory, origin/overrides/locks, fixed memory/skill/template capture and source/
code manifests are implemented. Shared `PlanningInputs`/pure prompt rendering and
`skill_from_markdown` retain legacy signatures and output, protected by five
complete prompt byte/hash baselines captured before refactoring at `500123b`.
Old writers, routing policy, M2/P02 schemas/tools and dependency/package-data
configuration are unchanged. New CLI glue and the generated command-reference
source describe actual preparation capability, not S2 check/verify.

New bundles reserve a fresh runtime directory and publish prompt/result with
exclusive writes. Captures are bounded, hashed and rechecked for bytes, resolved
target and optional presence, plus wrapper code. Unsafe paths, credential names
(including case variants), foreign durable-memory namespaces, malformed policy,
lock conflicts, incompatible declarations, drift and output failures refuse.
Only explicit defaults are opted into; no active policy was added. Error messages
identify malformed policy/context files without echoing rejected credential paths.
Nonempty partial outputs remain incomplete evidence. This is current local
consistency, not an adversarial filesystem transaction or secret-content classifier.

Plain text is literal, scoped and color-independent; JSON is one typed result.
`content_report` is null and content/readiness/acceptance/saved verification remain
unassessed. No checker/parser/model or recursive source action is performed.
Actual project CLI smoke created a selected two-resource prompt/result with primary
skill0.2.3; receipt is `.karakana/reviews/20261114-kdx11-s1/cli-smoke.json`.
Its illustrative task is labelled, not an accepted product specification or a model
response. Captured inputs are a timestamped run snapshot, not a forever-current pass.

Neutral fixtures, source/read/call spies, actual CLI subprocess text/JSON/exit
checks, partial-write/drift controls and installed-wheel API/CLI tests are included.
The wheel is exercised outside the checkout with markdown_it/openpyxl imports
blocked; preparation succeeds using explicit local inputs, and absent checkout
assets are refused rather than fetched. No Windows or independent reader proof.
Owning skill patch versions and a deterministic coordinator eval now carry this
boundary; examples remain synthetic, actual document acceptance remains human.

Review corrections have executable regressions: foreign project memory and
unselected unsafe policy declarations are refused, known credential names are
case-insensitive, undecodable roots return typed JSON failures, and malformed
context/policy JSON points to its actual file. An initial test collection import
used the wrong package path and was corrected from inspected repository patterns;
there is no unresolved diagnostic loop. Runtime patches/harness artifacts are not
committed. Self-review and final actual gates are recorded at closeout below.

The producer/consumer intent check found that the native planner's default
required output was always an implementation plan. S1 now supplies action-specific
output guidance and explicit audience/scope/revision/type metadata, while legacy
calls keep the same default and byte baselines. A custom template cannot silently
omit the declared action: the request/output contract is also appended literally.
Selected context version/profile/document declarations remain visible but unassessed.
Seven action regressions exercise inquiry, analysis, review, author, revise, plan
and mechanical fix; these verify supplied prompt instructions, not model obedience.
An actual seven-case adverse run demonstrated that a custom template could omit
the task text. The complete request declaration is now appended independently,
and those same custom-template/action regressions must pass at the final gate.

## Actual final verification and review — 2026-11-14

- Full `.venv/bin/pytest -q`: **1058 passed in28.36s** on final executable source;
 97 new tests over the961-test baseline. Earlier successful1045/1047/1051 and
 pre-custom-template1058 runs are historical intermediate gates, not final proof.
- Focused preparation/legacy/docs gate:140 passed in5.31s before the final custom
 template edge refinement; its seven adverse cases then reproduced missing task
 text, passed7/7 after the direct fix, and are included in the final full gate.
- `.venv/bin/karakana eval run`:187/187, zero warnings;
 `20261114-103405-eval-3241cd`, including the added source-text preparation rule.
 This is instruction coverage, not model-behavior or recipient-acceptance evidence.
- Skill validate-all, docs check, Karakana memory validation, generated command
 reference, changed local links and whitespace checks passed. Final source/scope
 manifest and exact task protocol/handoff receipts are in ignored runtime.
- Default release check:19 components pass, zero warnings;
 `20261114-103405-release-check-4737b4`. Full pytest/evals above ran separately;
 this is not a `release check --full` or deployment claim.
- Actual package tests built/installed a wheel outside the checkout, exercised
 real API and CLI prepare with markdown_it/openpyxl imports blocked, and refused
 missing checkout resources. Five frozen full-prompt byte/hash cases and existing
 direct plan/Codex/live/P02/M2 suites protect the shared refactor.
- Environment: Python3.14.4, Typer0.27.1, PyYAML6.0.3, pytest9.1.1,
 markdown-it-py4.3.0. No new dependency or Windows qualification is claimed.

Self-review challenged producer/consumer request intent, policy/context locations,
credential/project paths, byte/target/presence/code drift, no implicit reads/calls,
new-only/partial output and scope/authority interpretation. The discovered cases
have actual regressions; no blocking finding remains in the inspected S1 scope.
This is self-review, not independent technical approval or exhaustive assurance.
Whole-feature check/verify and saved assessment freshness belong to S2.

Changed groups: new document_tasks implementation, bounded planner/SkillLoader/CLI
sharing, command-reference source/output, preparation guide/example and owning
skill/map/eval, neutral fixtures and six test suites, plan/backlog/current delivery
history. M2/P02 implementation/profile JSON, model policy, dependencies, AGENTS and
KARAKANA were not changed. Sources and pre-existing output are preserved in actual
negative cases. No live model/Codex, external writes, source apply or deployment.

Recommended next task: owner review of S1's demonstrated preparation and stated
limits. Acceptance authorises normal validated PR/squash integration under the
standing convention; verify exact published head/CI/source/tree/postmerge then
offer S2's separate execution brief. S1 review/integration must finish before S2.
Use Sol/high for provenance/authority integrity review; fresh conversation may
benefit S2 after integration, not a requirement to interrupt current review.
Exact-task completion, source-manifest, handoff/doctor/load receipts are retained
under `.karakana/reviews/20261114-kdx11-s1/`; runtime artifacts are not committed.

## Owner S1 delivery acceptance — 2026-11-14

The owner replied **“accepted”** after the completed S1 delivery summary, without
revisions. This accepts the implemented preparation feature and its stated limits,
including1058 passing tests/187 evals, explicit task intent, captured resource and
output protection, unassessed content/acceptance and the intentional S2 boundary.
The exact reviewed33-file tree was `8c109839248a29430501c78ed7164d144d850300`;
its source hashes were rechecked before acceptance-only notes. Executable code,
tests, schemas, skill content and usage examples are unchanged by this update.

The standing agreement authorises normal validated publication, PR and squash
merge of S1 without a second integration confirmation. Check actual exact-head
CI and resulting tree/parent/postmerge state; receipts are retained under
`.karakana/reviews/20261114-kdx11-s1-integration/` and the release-trace handoff.
S2 execution and deployment are not selected by S1 acceptance. Once S1 integration
is complete, present S2's bounded implementation brief without reopening TT/DD/IP.
