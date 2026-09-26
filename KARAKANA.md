# Karakana Project Contract

## Project name

Karakana

## Project type

GitHub-native AI agent harness for durable project memory, reusable skills, safe model routing, Codex task generation, evaluation, and reviewable self-improvement.

## Durable memory

Use:

- `ubongo/global/engineering-standards.md`
- `ubongo/global/user-preferences.md`
- `ubongo/global/security-principles.md`
- `ubongo/global/prompt-patterns.md`
- `ubongo/global/lessons-learned.md`
- `ubongo/projects/karakana/overview.md`
- `ubongo/projects/karakana/architecture.md`
- `ubongo/projects/karakana/decisions.md`
- `ubongo/projects/karakana/deployment.md`
- `ubongo/projects/karakana/known-issues.md`
- `ubongo/projects/karakana/open-issues.md`

Every fresh session must load the latest matching project handoff before planning or editing. Every bounded task must finish by refreshing an append-only handoff summary that records verification, unresolved findings, changed references, remaining tasks, the recommended next task, and the exact next action. New handoff artifacts are organized by project under `.karakana/handoffs/<project>/<handoff-id>/`; legacy flat handoffs remain readable only for backward compatibility.

## Required skills

Use:

- `invenio-framework`
- `gepg-billing`
- `django-debugging`
- `github-pr-review`
- `ci-failure-analysis`
- `research-writing`
- `karakana-self-improvement`

## Model routing

Task continuation follows `docs/cost-aware-continuation.md`: reuse verified
research, architecture and plans, then deliver without restarting satisfied stages.
Handoffs must recommend the next bounded task's model and conversation boundary.
Routing recommendations are not observed model switches. Apply the six efficiency
rules there, without reducing safety or the final required verification gate.

Use the active policy in `docs/gpt-6-routing.md`: GPT-6 Sol for control-plane
judgment and consequential work (medium; high for risk), GPT-6 Luna for bounded
execution (high), and GPT-6 Astra only by explicit exceptional-task selection.
GPT-5.6 Luna/Sol remain explicit availability fallbacks, not automatic retries.
Legacy provider overrides remain supported. Python owns gates and routing.

## Safety rules

Engineering lifecycle and proportional stage gates: `docs/engineering-process.md`.
Check prerequisite artifacts before non-trivial implementation, and all required
artifacts at completion. Presence checks are not substantive approval or proof
of passing tests. Preserve request type, scope and external-action permissions.

- Never push directly to protected branches.
- Do all repository work on a task branch and integrate it through a pull request.
- Use squash merge for accepted work unless explicitly instructed otherwise.
- Never commit or print secrets.
- Never modify production secrets.
- Never run destructive database commands.
- Deliver research, brainstorming, implementation, debugging, and documentation from inspected evidence. Do not treat assumptions as facts when authoritative docs, schemas, exported artifacts, runtime errors, repository source, tests, or project memory can be checked.
- Every non-trivial implementation path must name the evidence to inspect, the skill or project instruction that governs the work, the exact implementation steps, and the verification gates before or during delivery.
- Repeated failures or learned constraints must be encoded into durable memory, skills, docs, validators, or evals so later agents inherit the rule instead of relying on chat history.
- Load the latest matching project handoff at session and task entry before planning or editing.
- Refresh the project handoff at the end of every bounded task so the next session has current continuation context.
- Preserve project/status boundaries during concept traversal. Bind completion to the exact task trace when available; classification-only traces are not task evidence. Verified explicit state can omit artifact recovery without deleting history. See `docs/handoff-provenance.md`.
- After each completed slice, the task completion summary must list remaining
  tasks or known follow-ups and state the recommended next task.
- All authentication and permission changes require human approval.
- All behavior changes require tests.
- Features with UX impact require behavior requirements, look-and-feel requirements, best-practice research for the task, alignment with the existing design system, and `ux-writing` review for user-facing labels, help text, status messages, empty states, warnings, and instructions before implementation.
- Non-trivial delivery requires an artifact-readiness check before implementation and before marking work done. Required requirements, ADR, milestone, delivery, UX, schema/example, test/eval, and handoff artifacts must exist, or the PR must explicitly record why a normally required artifact is not applicable.
- Self-improvement must produce reviewable proposals.
- Non-trivial work should start with `karakana protocol start` and end with a protocol check when required artifacts are present.

## Test commands

```bash
python -m pytest
karakana --help
```

## Deployment notes

No production deployment exists for the Milestone 2 memory implementation.

## Approval requirements

Explicit approval is required for destructive commands, secret handling, deployment, authentication changes, permission changes, database migrations, and CI secret changes.

## Known risks

- Task generation, explicit Codex execution, evaluations, reflection and GitHub
  workflows exist. Their availability does not authorize live execution.
- Protocol checks validate artifact presence, not semantic correctness.
- Handoff recovery can include unrelated/test-generated references; verify
  provenance before relying on recovered context (see engineering-process audit).
