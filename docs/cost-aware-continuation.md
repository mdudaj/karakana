# Cost-aware task continuation

## Requirements and decision

Implement research → architect → plan → deliver, reusing current, applicable
evidence rather than recreating completed stages. Existence alone is not approval.
The existing router classifies difficulty and risk; a recommendation does not
change an already-running interactive session's model.

[Codex model documentation](https://learn.chatgpt.com/docs/models) describes
`/model` for interactive switching and `-m` for launching a selected model. Check
account/client availability. This change does not migrate the model catalog or
certify availability. No live model calls or remote writes are authorized here.

The subsequent model-catalog migration is specified in `docs/gpt-6-routing.md`.
Its approved commit/push/squash-merge scope supersedes this slice's original
local-only delivery boundary; neither document authorizes live model calls.

## Architecture and acceptance criteria

1. An explicit next task outranks recovered stale milestone text. Use the existing
   router and project overrides, never a second model-routing policy.
2. Repeatable `--reuse-stage STAGE=PATH` references research, architect and plan
   evidence; `--reuse-reviewed` attests scope, currency, applicability and approval
   were checked. A compact artifact may cover all stages, including justified
   non-applicability. Missing files fail creation. Hash changes reopen the stage;
   hashes do not prove semantic applicability. Recheck source changes at task entry.
3. All stages reviewed and unchanged → deliver directly; otherwise start with the
   first unsatisfied stage while retaining later reusable evidence.
4. `--slice-complete` recommends a fresh conversation at a boundary. Otherwise
   continue the unfinished task. Two failed diagnostic attempts recommend a fresh
   diagnostic review and high-risk review model. Do not infer context usage.
5. Full handoff and session-start output include model, stage and conversation
   guidance. Old handoffs remain readable and request explicit task/reuse review.
6. Explicit Codex task execution passes its structured recommended model. Missing
   model metadata fails before launch. Recommendation never authorizes execution.

## Execution discipline (suggestions 2–7)

- Research new uncertainties only; reuse approved references and decisions.
- Focused tests during debugging; full required regression gate once stabilized.
  A failed/skipped final gate is not completion.
- Bound output to relevant failures, functions and diffs; avoid repeated dumps.
- One compact delivery record plus linked handoff, not duplicate PRDs/ADRs.
- After two unsuccessful diagnostic attempts on the same issue, stop speculative
  patches, record hypotheses/results, escalate or replan. Escalate sooner for risk;
  a new conversation must not erase failed-attempt history.
- One agent and ordinary reasoning by default. Fan-out or maximum reasoning needs
  a recorded benefit. Independent read-only checks can still run concurrently.

## Implementation, traceability and verification

Inspect `handoffs/{builder,schemas,summary}.py`, `models/router.py`, CLI handoff
commands and `codex/executor.py`. Extend structured continuation with backward
compatible defaults and redaction. Tests map to criteria 1–6: precedence, stage
reuse/invalidation, risk routing, project overrides, conversation boundaries,
legacy artifacts and explicit launch argv. Run focused tests, then full pytest,
skill validation and deterministic evals. No application UI or deployment changes.

Rollback: revert the patch; prior append-only handoffs remain available. New
metadata lives in ignored runtime artifacts. Current task risk is high because
it changes execution guidance, though no routing tiers or approval gates change.

## Usage

```bash
karakana handoff refresh --project PROJECT --skillpack PROJECT \
  --next-task "Implement approved export tests" --slice-complete \
  --reuse-stage research=docs/export-plan.md \
  --reuse-stage architect=docs/export-plan.md \
  --reuse-stage plan=docs/export-plan.md --reuse-reviewed
```

Use the bounded next task as classifier input, not the entire project history.
Record overrides if an available equivalent model is needed. Neither switching
models nor starting a new conversation resets account usage allowances.

## Delivery record — 2026-09-26

Implemented criteria 1–6 on `fix/cost-aware-continuation`, including CLI options,
structured/redacted handoff metadata, load-time evidence hashes, shared guidance,
existing skill updates and explicit executor model propagation. The current
interactive session is not switched. No model calls, commits, pushes or deployments.

Verification:

- Full pytest: 539 passed.
- Skill validation: all passed. Skillpacks passed with existing missing-memory
  warnings for billing, msc-research and nhrdm.
- Handoff evals: 5 passed. Full deterministic evals: 143/144 passed. Existing
  `material-record-list` fails because its forbidden phrase `color alone` also
  matches the instruction “Do not rely on color alone”; both source files are
  unchanged. This is recorded, not silently waived as an all-green gate.
- `git diff --check` passed. Explicit launches tested with a mocked subprocess;
  account-specific availability and real CLI execution were not exercised.

Next: review this high-risk harness change before integration. Separately refresh
the available model catalog against the actual account/client; configured names
are recommendations, not guarantees. Fix the unrelated eval false positive in a
bounded follow-up. Start a fresh conversation when returning to an application
project and load that project's own handoff; do not mix project context.
