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

- Triage summarizer: GitHub inference with Claude Haiku 4.5 for issue triage, documentation, changelog, and simple summaries.
- Planner: GitHub inference with GPT-5 mini for planning, architecture review, requirements reasoning, reflection, skill design, and action extraction review.
- Routine implementer: Codex GPT-5.4-mini for bounded implementation, test generation, and Codex task drafting after requirements and design context exist.
- Serious implementer: Codex GPT-5.4 for CI repair, refactors, framework work, and repository-aware PR review.
- Principal reviewer: Codex GPT-5.5 for high-risk or stuck work, including authentication, authorization, billing, migrations, workflow state changes, and cross-project architecture.
- Skill improvement implementation: Codex GPT-5.4-mini for routine work, escalating to GPT-5.4 or GPT-5.5 when risk requires it.
- Skill improvement review: GitHub inference with GPT-5 mini.

Prefer Copilot Max/GitHub inference for non-mutating context, planning, requirements, and review-preparation work. Use Codex routes for repository mutation and deeper code reasoning. Use GPT-5.5 only when the work is high-risk, complex, or stuck, and record the escalation rationale in traces.

## Safety rules

- Never push directly to protected branches.
- Do all repository work on a task branch and integrate it through a pull request.
- Use squash merge for accepted work unless explicitly instructed otherwise.
- Never commit or print secrets.
- Never modify production secrets.
- Never run destructive database commands.
- All authentication and permission changes require human approval.
- All behavior changes require tests.
- Features with UX impact require behavior requirements, look-and-feel requirements, best-practice research for the task, and alignment with the existing design system before implementation.
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

- Codex task generation is implemented. Codex execution, evaluations, reflection, and GitHub Actions are not implemented yet.
