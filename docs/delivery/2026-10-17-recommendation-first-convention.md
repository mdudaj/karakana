---
status: ready_for_implementation
question: "How should every managed project offer a concrete recommendation before waiting on user or third-party input?"
evidence:
  - source: "User instruction, 17 October 2026; shared lifecycle renderer and its four consumers."
    finding: "The user explicitly selected the convention; existing shared guidance can propagate it without a new controller or project-specific policy copies."
  - source: "MADR template and AWS ADR process, checked 17 October 2026."
    finding: "Both support explicit choices, rationale and decision history; the user's instruction supplies the recommendation-before-escalation requirement."
requirements:
  - decision: "Present a preferred evidence-backed proposal, meaningful alternatives, assumptions and affected work before escalating a missing decision or fact; record agreement and user revisions."
    acceptance: "RF1-RF5 below hold in shared guidance and generated outputs for Karakana and other project IDs, with external-action boundaries preserved."
    artifact: docs/delivery/2026-10-17-recommendation-first-convention.md
design:
  - choice: "Extend global memory, existing lifecycle guidance and research artifacts; use deterministic generation tests and evals without changing approval or research schemas."
    rationale: "Reuses the four existing consumers and avoids a controller, backward-incompatible schema or bulk project edits."
    artifact: docs/delivery/2026-10-17-recommendation-first-convention.md
artifact_choices:
  - kind: requirements
    disposition: updated
    path: docs/delivery/2026-10-17-recommendation-first-convention.md
    rationale: "One compact record contains the user-approved requirement, acceptance, traceability and verification plan."
  - kind: design
    disposition: updated
    path: docs/delivery/2026-10-17-recommendation-first-convention.md
    rationale: "The selected shared-guidance extension and alternatives are fully described below."
authority:
  state: approved
  evidence: "The user directed this convention across the harness and projects; approval covers local workflow, memory, prompt and eval changes, not publication, target activation or third-party policy."
pending_decisions: []
next_action: "Deliver and verify this bounded local harness convention patch; publication and the separate ent-meal implementation retain their own gates."
---

# Recommendation before dependency escalation

## Classification, authority and problem

Task trace: `20261017-072653-366ae3`. User-authorized global harness workflow,
memory, prompt and eval improvement, 17 October 2026. Risk: high because shared
instructions govern consequential work; this patch changes guidance, not Python
authorization gates. Local reviewable delivery only; no remote publication,
model calls, deployment or changes to another project's accepted decisions.

The ent-meal review named open external decisions without first offering enough
concrete proposals for agreement. The user directed that every project should
receive the assistant's best evidence-backed recommendation and meaningful
alternatives before waiting for user/third-party input, followed by agreement,
artifact updates and later revisions when needed.

User story: as the project owner, I can review a practical recommendation and
its consequences instead of designing the solution through unanswered questions.
Existing agreements remain reusable; routine choices within delegated authority
continue without an extra approval exchange.

## Requirements and acceptance

| ID | Required behavior / observable acceptance | Implementation and regression evidence |
| --- | --- | --- |
| RF1 | Before requesting a decision or waiting on a dependency, offer one preferred feasible proposal with authoritative evidence, rationale, assumptions and consequences. Inspect current project conventions before researching new uncertainties. | Global preferences/standards, engineering process, shared lifecycle renderer; generated planning/coding/protocol/handoff tests. |
| RF2 | Include meaningful viable alternatives with trade-offs when they affect the decision. If only one feasible path exists, say why; do not manufacture options or call a guess best practice. For an unobservable site fact, recommend a conditional path and bounded verification rather than invent the fact. | Delivery-artifact skill, research protocol/template and deterministic evals. |
| RF3 | State what can proceed safely now, what is held, the decision/evidence owner, the exact confirmation needed and the relevant artifact. Agreement is distinct from evidence and external-action authorization; user silence is not agreement. | Shared prompts, skill and protocol guidance; generation tests assert boundaries. |
| RF4 | Present material proposals for agreement; record accepted choices and user revisions in the governing requirements/design/plan/workbook. Revalidate affected tests and approval scope; preserve accepted history through the project's revision/supersession convention. No new approval for already delegated routine decisions. | Global memory/process and research-template decision table. |
| RF5 | The convention reaches every managed project through shared memory, all four prompt-generation paths and session-start handoff loading, including legacy handoffs; do not bulk-edit project repos or replace project policy. | Planner/coding tests for Karakana and other project IDs; protocol-start/Codex-handoff assertions; CLI/legacy-handoff tests; generated-prompt eval. |

Definition of done: scoped patch reviewed against RF1–RF5, focused tests plus
full pytest and deterministic evals, memory/skill/protocol validation, diff check,
trace-bound append-only handoff. Report actual failures/omissions. Local delivery,
merge and rollout to other checkouts remain separate states.

## Evidence and design/method choice

Inspected `ubongo/global/user-preferences.md`, `engineering-standards.md`,
`docs/engineering-process.md`, `KARAKANA.md`, `AGENTS.md`, the self-improvement
and delivery-artifact skills, `karakana/memory/ubongo.py`, the shared lifecycle
renderer and its consumers: planner, Codex executor, protocol start and coding
handoff. Existing research-resolution guidance already asks for recommendations
when approval is missing; extend it into a consistent front-of-decision rule.

Selected method: add the convention to existing shared memory/process and
`render_engineering_process()`, plus the artifact skill and research template.
All task consumers already include the shared lifecycle. Its recommendation
function is also reused by continuation rendering so session-start handoff loads,
including older handoffs, carry the current rule. No new orchestration component
or per-project policy copying is needed. Preserve existing schemas/validators,
deterministic approval gates and current research outcome semantics.

Alternatives considered:

- Chat-only preference: too easy to lose at a fresh session or project switch.
- New mandatory decision schema/controller: disproportionate for an instruction
  gap and would break historical artifacts or add approval machinery.
- Chosen shared guidance with generation tests/evals: small, reviewable and
  compatible. Tests prove instruction propagation, not future model compliance.

Authoritative conventions checked 17 October:
[MADR's template](https://adr.github.io/madr/decisions/adr-template) records
context, decision drivers, considered options, chosen option and consequences.
[AWS's ADR process](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)
separates proposed/accepted decisions and preserves superseded history. Those
sources support the decision-record method; this user's requirement to recommend
before escalating and to continue independent work is the governing local policy,
not a claim that either reference mandates this whole workflow.

## Source-alignment challenge

Memory alone is insufficient when a generated task lacks global
memory or uses a synthetic project. The shared renderer is included independently
by all four task consumers; session-start continuation also renders the current
shared rule rather than trusting a stored historical handoff body. Regression
coverage checks actual outputs, including non-Karakana project IDs and legacy
handoffs. Conversely, including a preferred
choice must not turn `decision_required` into readiness or permit a target write;
the schema/checker is unchanged and existing research/gate tests remain required.

## Artifact readiness and implementation instructions

This compact record contains the requirement/PRD, story, acceptance criteria,
design rationale, implementation plan, traceability, eval rationale and readiness
evidence. User approval covers the requested local convention changes. A new
schema, product UX, migration or standalone ADR is not applicable: the chosen
method extends an existing guidance mechanism without changing executable gates.
The process branch starts from reviewed but unpublished `d7c954c`; preserve that
prior artifact-review improvement and record it as a dependency for integration.

Steps: update global preference/standards and entrypoint pointers; extend the
engineering guide/renderer and artifact skill/research protocol/template; add
RF1–RF5 assertions and evals; run focused checks, then the full required gate;
review scope and refresh the exact task handoff. Apply via a reviewable task-branch
patch. Do not launch agents, models or external applications.

Verification commands: `.venv/bin/pytest -q tests/test_engineering_process.py
tests/test_planner.py tests/test_codex_executor.py tests/test_research_resolution.py`,
then full `.venv/bin/pytest -q`; `karakana memory validate --project karakana`,
`skill validate-all`, `protocol validate-all`, `eval run`, and `git diff --check`.
Run pytest/evals using temporary repository state; never populate the working
checkout's `.karakana` stores with test fixtures. Existing runtime guards and
isolated-repository fixtures remain in force.

Rollback: revert this convention's patch through review, preserving the prior
process changes and append-only handoffs. Residual risk: textual instruction tests
cannot prove agent judgment; proposal quality and actual authority still require
substantive review. No global rollout or third-party acceptance is inferred.

## Delivery and verification

Implemented locally on `codex/recommendation-first-convention`:

- `AGENTS.md`, `KARAKANA.md`, `ubongo/global/user-preferences.md`,
  `ubongo/global/engineering-standards.md` and `docs/engineering-process.md`:
  global convention, agreement/revision rules and authority boundaries.
- `karakana/protocols/lifecycle.py` and `karakana/handoffs/continuation.py`:
  one recommendation renderer reused by task guidance and session starts.
- `protocols/research-resolution.yml`, `templates/protocols/research-resolution.md`
  and `skills/delivery-artifact-gate/SKILL.md` (0.3.2): research/artifact workflow.
- `tests/test_planner.py`, `test_codex_executor.py`, `test_engineering_process.py`
  and `test_handoff_continuation.py`: cross-project output and legacy-load guards.
  `evals/requirements/recommendation-first-planning.yml` and the artifact skill's
  `evals/recommendation-first.yml`: deterministic instruction regressions.
- This compact record supplies the scoped requirements, method and delivery evidence.

Verification performed:

- Regression-first: seven generated-output checks failed for the missing rule;
  two session-start/legacy-handoff checks then demonstrated the continuation gap.
  These expected red checks were closed by the implementation.
- Focused pytest including handoff continuation: **64 passed**.
- Final full pytest: **735 passed in 19.07s**. Executed from the source-only
  temporary copy `/tmp/karakana-recommendation-checks.d0b_4ci4`, using the existing
  Karakana Python environment and that copy on PYTHONPATH. The full gate was
  repeated after adding continuation propagation, not to debug a speculative patch.
- Final deterministic `karakana eval run`: **175 passed, zero failures/warnings**.
  Report: `/tmp/karakana-recommendation-checks.d0b_4ci4/.karakana/eval-runs/20261017-073142-eval-592593/report.md`.
  This uses local text/routing checks and no live model execution.
- Karakana memory validation, all skill validation and all protocol validation:
  passed. Scoped Ruff passed using the already installed sibling-environment
  executable (Karakana's venv has no Ruff); no package installation was needed.
  `git diff --check` and research-resolution structure/reference validation passed.
- Loading the existing ent-meal handoff with `--no-okf-context` displayed the
  preferred-proposal, conditional-verification, revision and authority rules.
  No ent-meal source or external CRDB artifact was edited by this harness slice.

Self-review found no blocking correctness or authority regression. No independent
review, GitHub publication/merge, deployment or rollout to other harness checkouts
is claimed. The branch includes the previously reviewed/unpublished `d7c954c`
artifact-review improvement; preserve/review that dependency when integrating.
Prompt propagation is verified; future agent compliance still needs substantive
review. The structural completion check and append-only handoff are trace-bound.

## Handoff and next action

Continuation clarification after user review: the initial handoff wrongly
foregrounded publication and left ent-meal's later slice agreement in long notes.
Its `research`-only reuse fields also suggested a new architecture stage for
completed harness work. Refined the handoff skill (0.4.1) and added an instruction
eval: expose one concrete project action, first files/command, expected output,
completion checks and current agreement; separate publication from engineering
continuation while retaining actual integration gates. Completed-stage reuse
must be accurate. The ent-meal next bounded action is to resolve only the local
driver-support uncertainty and present the conditional encryption recommendation
in its existing preparation record. This research/preparation can proceed while
publication is pending; implementation retains the one-active-milestone gate.
Correction verification: handoff skill validation and diff check passed; all
**176 deterministic evals passed** in the isolated verification copy. No Python
runtime changed, so the earlier 735-test result remains the code baseline rather
than a claimed new execution. Refresh both project handoffs with explicit scope,
agreement, first action and actual remaining integration/target gates.

Finish this bounded harness slice before returning to the agreed ent-meal
application-image/readiness slice. That follow-up should bring a concrete driver/
transport recommendation and alternatives, then update its governing artifacts;
unverified CRDB policy/access remains unverified. Publish/merge only with explicit
authority. Recommend GPT-6 Sol/high for the consequential follow-up; recommendation
does not switch the active model. No failed diagnostic loop is carried into this task.
