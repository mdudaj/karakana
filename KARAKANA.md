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

- Planning: GPT-5 mini
- Lightweight documentation: Claude Haiku 4.5
- Routine coding: Codex GPT-5.4-mini
- Serious coding, refactors, and CI repair: Codex GPT-5.4
- High-risk or stuck coding: Codex GPT-5.5
- Code review: Codex GPT-5.4 by default; Codex GPT-5.5 for high-risk review
- Reflection: GPT-5 mini
- Skill improvement implementation: Codex GPT-5.4-mini for routine work, escalating to GPT-5.4 or GPT-5.5 when risk requires it
- Skill improvement review: GPT-5 mini

Use GPT-5.5 only when the work is high-risk, complex, or stuck.

## Safety rules

- Never push directly to protected branches.
- Never commit or print secrets.
- Never modify production secrets.
- Never run destructive database commands.
- All authentication and permission changes require human approval.
- All behavior changes require tests.
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
