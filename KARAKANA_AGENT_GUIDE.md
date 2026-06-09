# Karakana Agent Instruction Guide

## 1. Mission

You are an implementation agent responsible for delivering  **Karakana** , a GitHub-native AI agent harness for managing multiple software, research, and infrastructure projects.

**Karakana** means “workshop” in Swahili. The harness should behave like a disciplined technical workshop where models, tools, project memory, skills, GitHub workflows, evaluations, and human review work together.

The goal is not to create an uncontrolled autonomous agent. The goal is to build a safe, extensible, self-reflecting engineering harness that can:

* understand multiple projects,
* retrieve durable project knowledge,
* use reusable skills,
* route work to the right model,
* assist with coding, reviewing, documenting, debugging, and planning,
* propose improvements to itself,
* update memory and skills through pull requests,
* and preserve human approval for risky changes.

The guiding principle is:

```text
Karakana thinks and remembers.
Codex codes and tests.
GitHub governs.
Humans approve.
```

---

## 2. Core Design Principles

### 2.1 GitHub-first

Karakana must integrate naturally with GitHub:

* GitHub repositories
* GitHub Issues
* GitHub Pull Requests
* GitHub Actions
* GitHub Models
* GitHub code review
* GitHub branch protection
* GitHub approvals

All important changes must be traceable through GitHub.

### 2.2 Safe self-improvement

Karakana may reflect on its own performance, but it must not silently rewrite itself.

Self-improvement must follow this loop:

```text
Task execution
  ↓
Trace capture
  ↓
Reflection
  ↓
Proposed memory / skill / prompt / eval update
  ↓
Pull request
  ↓
CI and evaluation checks
  ↓
Human review
  ↓
Merge
```

The agent must never directly mutate production systems, secrets, or protected branches.

### 2.3 Memory is explicit

Durable memory must be stored in the `ubongo/` directory.

`ubongo` means “brain” or “intelligence” in Swahili.

The `ubongo/` directory is the human-readable source of truth for durable knowledge.

Embeddings or vector indexes may be used for search, but they must not replace the markdown memory files.

### 2.4 Skills are modular

Reusable capabilities must be packaged as skills under `skills/`.

Each skill should contain:

* `SKILL.md`
* optional scripts
* examples
* templates
* evaluation cases
* references

Skills should encode repeated workflows, project-specific conventions, edge cases, tool usage, and known pitfalls.

### 2.5 Models have roles

Do not treat all models as interchangeable.

The default routing is:

| Model            | Role                                                                        |
| ---------------- | --------------------------------------------------------------------------- |
| GPT-5 mini       | planning, reasoning, reflection, architecture analysis, issue decomposition |
| Claude Haiku 4.5 | fast summaries, documentation, changelogs, lightweight issue triage         |
| Codex GPT-5.5    | code implementation, refactoring, tests, CI repair, deep PR review          |
| Human            | approval, prioritization, production-risk decisions                         |

### 2.6 Patches before writes

The harness should prefer generating patches, pull requests, comments, and plans over direct mutation.

Default rule:

```text
Read freely.
Suggest confidently.
Write through patches.
Execute in sandbox.
Deploy only after approval.
```

---

## 3. Target Repository Structure

Implement the initial repository as follows:

```text
karakana/
├── .github/
│   ├── workflows/
│   │   ├── issue-triage.yml
│   │   ├── pr-review.yml
│   │   ├── ci-failure-analysis.yml
│   │   ├── skill-eval.yml
│   │   └── nightly-reflection.yml
│   └── ISSUE_TEMPLATE/
│
├── karakana/
│   ├── __init__.py
│   ├── cli.py
│   ├── orchestrator.py
│   ├── router.py
│   ├── config.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── planner.py
│   │   ├── researcher.py
│   │   ├── reviewer.py
│   │   ├── implementer.py
│   │   ├── tester.py
│   │   └── reflector.py
│   ├── memory/
│   │   ├── __init__.py
│   │   ├── ubongo.py
│   │   ├── retrieval.py
│   │   ├── consolidation.py
│   │   └── schemas.py
│   ├── skills/
│   │   ├── __init__.py
│   │   ├── loader.py
│   │   ├── validator.py
│   │   └── runner.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── github.py
│   │   ├── filesystem.py
│   │   ├── shell.py
│   │   ├── code_search.py
│   │   ├── test_runner.py
│   │   └── codex_executor.py
│   ├── evals/
│   │   ├── __init__.py
│   │   ├── runner.py
│   │   └── judges.py
│   └── safety/
│       ├── __init__.py
│       ├── permissions.py
│       ├── policy.py
│       └── approval.py
│
├── ubongo/
│   ├── global/
│   │   ├── engineering-standards.md
│   │   ├── user-preferences.md
│   │   ├── security-principles.md
│   │   ├── prompt-patterns.md
│   │   └── lessons-learned.md
│   ├── projects/
│   │   ├── karakana/
│   │   │   ├── overview.md
│   │   │   ├── architecture.md
│   │   │   ├── decisions.md
│   │   │   ├── known-issues.md
│   │   │   └── open-issues.md
│   │   ├── nhrdm/
│   │   ├── billing/
│   │   ├── lims/
│   │   └── msc-research/
│   └── inbox/
│
├── skills/
│   ├── invenio-framework/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   ├── scripts/
│   │   ├── templates/
│   │   └── evals/
│   ├── gepg-billing/
│   ├── django-debugging/
│   ├── github-pr-review/
│   ├── ci-failure-analysis/
│   ├── research-writing/
│   └── karakana-self-improvement/
│
├── prompts/
│   ├── issue_triage.prompt.md
│   ├── pr_review.prompt.md
│   ├── reflection.prompt.md
│   ├── codex_task.prompt.md
│   └── skill_author.prompt.md
│
├── evals/
│   ├── skill-evals/
│   ├── regression-cases/
│   └── prompt-evals/
│
├── AGENTS.md
├── KARAKANA.md
├── README.md
├── pyproject.toml
└── .gitignore
```

---

## 4. Initial CLI Requirements

Implement a CLI named `karakana`.

Use Python with a clean CLI framework such as Typer.

The first version must support the following commands.

### 4.1 Initialize a project

```bash
karakana init --project nhrdm
```

Expected behavior:

* create required `ubongo/projects/<project>/` files if missing,
* create `KARAKANA.md` if missing,
* create or update `AGENTS.md`,
* detect repository metadata,
* register the project in Karakana config.

### 4.2 Plan a task

```bash
karakana plan \
  --project nhrdm \
  --skill invenio-framework \
  --task "Design category-guided deposit forms"
```

Expected behavior:

* load project memory from `ubongo/projects/nhrdm/`,
* load selected skill from `skills/invenio-framework/SKILL.md`,
* route to GPT-5 mini by default,
* produce a structured implementation plan,
* include risks, files to inspect, tests, and approval requirements.

### 4.3 Run a Codex coding task

```bash
karakana codex run \
  --project nhrdm \
  --skill invenio-framework \
  --task "Implement vocabulary validation tests"
```

Expected behavior:

* build a Codex-ready task prompt,
* include relevant `ubongo/` memory,
* include selected skill instructions,
* include safety rules,
* write the generated task to `.karakana/codex-task.md`,
* optionally launch Codex CLI if available,
* collect the resulting diff if possible,
* recommend tests.

### 4.4 Review a PR

```bash
karakana review \
  --project nhrdm \
  --skill invenio-framework \
  --diff path/to/diff.patch
```

Expected behavior:

* inspect diff,
* load project memory,
* load relevant skill,
* route to GPT-5 mini or Codex depending on complexity,
* produce review sections:
  * summary,
  * blocking issues,
  * non-blocking suggestions,
  * test gaps,
  * security risks,
  * deployment risks.

### 4.5 Reflect on recent work

```bash
karakana reflect \
  --project nhrdm \
  --since "7 days"
```

Expected behavior:

* inspect recent commits, merged PRs, closed issues, and captured traces where available,
* identify missing memory,
* identify missing or weak skills,
* identify possible prompt improvements,
* propose eval additions,
* generate a proposed PR plan for updating `ubongo/`, `skills/`, `prompts/`, or `evals/`.

### 4.6 Validate a skill

```bash
karakana skill validate skills/invenio-framework
```

Expected behavior:

* confirm `SKILL.md` exists,
* validate metadata,
* validate required sections,
* check allowed tools,
* check approval requirements,
* check examples/templates/evals if present,
* report warnings and errors.

### 4.7 Run evaluations

```bash
karakana eval run --skill invenio-framework
```

Expected behavior:

* discover eval files,
* run prompt or skill regression cases,
* compare outputs where applicable,
* report pass/fail,
* block unsafe skill degradation in CI.

---

## 5. Skill Specification

Each skill must be a directory with this basic structure:

```text
skills/<skill-name>/
├── SKILL.md
├── references/
├── scripts/
├── templates/
└── evals/
```

Only `SKILL.md` is required in the first version.

### 5.1 Required `SKILL.md` front matter

Each `SKILL.md` must start with YAML front matter:

```yaml
---
name: invenio-framework
description: Use this skill when working on Invenio Framework, InvenioRDM, NHRDM, custom fields, vocabularies, OAuth/SSO, OpenSearch, dashboards, permissions, records, deposits, or migrations.
version: 0.1.0
risk_level: high
allowed_tools:
  - read_file
  - grep
  - code_search
  - run_tests
  - python
requires_approval_for:
  - database_migration
  - production_config_change
  - authentication_change
  - permission_change
  - index_rebuild
  - destructive_command
---
```

### 5.2 Required skill sections

Each skill should include:

```markdown
# Skill Name

## Purpose

## When to use this skill

## When not to use this skill

## Core concepts

## Standard workflow

## Safety rules

## Required checks

## Output format

## Examples
```

---

## 6. Required Initial Skills

Implement these first.

### 6.1 `invenio-framework`

This is a broad Invenio ecosystem skill, not only an InvenioRDM skill.

It must cover:

* Invenio Framework
* InvenioRDM
* Flask extension patterns
* SQLAlchemy models
* Alembic migrations
* services/resources
* records and drafts
* custom fields
* vocabularies
* subjects
* OAuth/SSO
* OpenSearch indexing
* user dashboard customization
* deposit forms
* permissions
* communities
* requests
* background jobs
* deployment checks

Use this skill for NHRDM-related work.

### 6.2 `gepg-billing`

Use this for the NIMR billing system and GePG integration.

It must cover:

* Django billing models,
* control number generation,
* payment callbacks,
* idempotency,
* reconciliation,
* cancellations,
* invoices,
* receipts,
* Celery tasks,
* Redis/RabbitMQ,
* callback logs,
* duplicate payment prevention.

### 6.3 `django-debugging`

Use this for general Django debugging.

It must cover:

* views,
* models,
* migrations,
* forms,
* serializers,
* Celery,
* tests,
* settings,
* performance,
* pagination,
* logging.

### 6.4 `github-pr-review`

Use this for reviewing GitHub pull requests.

It must cover:

* correctness,
* security,
* maintainability,
* tests,
* migrations,
* deployment risk,
* documentation,
* backwards compatibility.

### 6.5 `ci-failure-analysis`

Use this for failed GitHub Actions or CI logs.

It must cover:

* log reduction,
* failure classification,
* likely root cause,
* affected files,
* suggested patch,
* rerun guidance,
* missing dependency detection.

### 6.6 `research-writing`

Use this for academic and concept-note writing.

It must cover:

* proposal structure,
* literature review,
* methodology,
* objectives,
* significance,
* scope,
* risk analysis,
* grant/call requirement analysis.

### 6.7 `karakana-self-improvement`

Use this when Karakana reflects on its own memory, skills, prompts, tests, or workflows.

It must cover:

* reflection,
* memory update proposals,
* skill update proposals,
* prompt update proposals,
* eval generation,
* PR creation,
* regression protection.

---

## 7. `ubongo/` Memory Specification

The `ubongo/` directory stores durable project knowledge.

### 7.1 Global memory

Use:

```text
ubongo/global/
├── engineering-standards.md
├── user-preferences.md
├── security-principles.md
├── prompt-patterns.md
└── lessons-learned.md
```

### 7.2 Project memory

Each project should have:

```text
ubongo/projects/<project>/
├── overview.md
├── architecture.md
├── decisions.md
├── deployment.md
├── known-issues.md
└── open-issues.md
```

### 7.3 Memory rules

The agent must follow these rules:

1. Treat markdown files in `ubongo/` as durable source-of-truth memory.
2. Do not store secrets in `ubongo/`.
3. Do not overwrite memory without preserving useful previous knowledge.
4. Prefer small, reviewable updates.
5. Memory updates must be proposed through pull requests.
6. If memory conflicts with repository code, flag the conflict.
7. If memory is stale, propose an update rather than silently relying on it.

---

## 8. Model Routing Policy

Implement a router that selects a model based on task type.

### 8.1 Default routing

```yaml
planning: gpt-5-mini
architecture_review: gpt-5-mini
reflection: gpt-5-mini
skill_design: gpt-5-mini
issue_triage: claude-haiku-4.5
documentation: claude-haiku-4.5
changelog: claude-haiku-4.5
simple_summary: claude-haiku-4.5
code_implementation: codex-gpt-5.5
refactoring: codex-gpt-5.5
ci_repair: codex-gpt-5.5
deep_pr_review: codex-gpt-5.5
migration_review: codex-gpt-5.5
```

### 8.2 Escalation rules

Escalate from Claude Haiku 4.5 to GPT-5 mini when:

* task involves architecture,
* task involves security,
* issue is ambiguous,
* issue affects production,
* issue requires multi-step reasoning,
* previous answer confidence is low.

Escalate from GPT-5 mini to Codex GPT-5.5 when:

* repository edits are required,
* tests must be run,
* CI must be repaired,
* large codebase inspection is required,
* migrations are involved,
* refactoring is requested,
* PR review requires file-level code reasoning.

---

## 9. Codex Integration Requirements

Codex GPT-5.5 should be treated as a coding executor and reviewer, not only a text model.

### 9.1 Local Codex mode

The command:

```bash
karakana codex run --project <project> --skill <skill> --task "<task>"
```

should:

1. load project memory,
2. load skill instructions,
3. inspect repository metadata,
4. create `.karakana/codex-task.md`,
5. include safety rules,
6. instruct Codex to work on a branch,
7. instruct Codex to show diffs,
8. instruct Codex to run relevant tests,
9. instruct Codex not to touch secrets,
10. instruct Codex not to deploy.

### 9.2 Codex task prompt format

The generated Codex task should include:

```markdown
# Karakana Codex Task

## Task

## Project

## Relevant Ubongo Memory

## Selected Skill

## Repository Instructions

## Files likely relevant

## Safety Rules

## Required Output

## Tests to Run

## Approval Requirements
```

### 9.3 PR review mode

Karakana should support preparing Codex review instructions for GitHub PRs.

Expected command:

```bash
karakana codex review --repo <owner/repo> --pr <number> --focus "<focus>"
```

The review should focus on serious issues:

* correctness,
* security,
* migrations,
* data loss risk,
* permission regressions,
* production deployment risk,
* missing tests.

---

## 10. Safety and Approval Policy

Implement safety at the framework level.

### 10.1 Risk levels

Supported risk levels:

```text
low
medium
high
critical
```

### 10.2 High-risk actions

These require explicit approval:

* database migration,
* data migration,
* production configuration change,
* authentication change,
* permission change,
* payment logic change,
* destructive shell command,
* Kubernetes write action,
* deployment,
* secret handling,
* OpenSearch index rebuild,
* deleting files,
* modifying CI secrets.

### 10.3 Forbidden by default

The agent must not:

* push directly to `main`,
* commit secrets,
* print secrets,
* modify `.env` files without approval,
* run destructive database commands,
* deploy to production,
* delete production data,
* bypass failing tests,
* mark a risky change as safe without evidence.

---

## 11. GitHub Actions Workflows

Implement these workflows.

### 11.1 Issue triage

File:

```text
.github/workflows/issue-triage.yml
```

Behavior:

* triggered on opened or edited issues,
* classify project,
* suggest labels,
* suggest skill,
* summarize issue,
* propose next steps,
* comment on issue.

### 11.2 PR review

File:

```text
.github/workflows/pr-review.yml
```

Behavior:

* triggered on pull request opened or synchronized,
* inspect diff,
* load project contract,
* load relevant skill,
* generate structured review,
* comment on PR.

### 11.3 CI failure analysis

File:

```text
.github/workflows/ci-failure-analysis.yml
```

Behavior:

* triggered on workflow failure,
* collect logs,
* reduce noisy output,
* identify likely root cause,
* suggest fix,
* comment on PR or issue.

### 11.4 Skill evaluation

File:

```text
.github/workflows/skill-eval.yml
```

Behavior:

* triggered when files under `skills/`, `prompts/`, or `evals/` change,
* run skill validation,
* run regression evals,
* fail CI on dangerous regression.

### 11.5 Nightly reflection

File:

```text
.github/workflows/nightly-reflection.yml
```

Behavior:

* scheduled nightly or weekly,
* inspect recent merged PRs and closed issues,
* propose `ubongo/`, skill, prompt, or eval updates,
* open a PR instead of direct modification.

---

## 12. `AGENTS.md` Requirements

Create a root `AGENTS.md` file.

It should instruct coding agents as follows:

```markdown
# Agent Instructions

This repository uses Karakana.

Before planning or editing code:

1. Read `KARAKANA.md`.
2. Read relevant files under `ubongo/projects/<project>/`.
3. Load any relevant skill from `skills/<skill>/SKILL.md`.
4. Respect safety rules.
5. Prefer patches and pull requests over direct changes.
6. Do not touch secrets.
7. Run relevant tests.
8. Document risks.

For code review:

- Flag serious correctness issues.
- Flag security regressions.
- Flag unsafe migrations.
- Flag missing tests.
- Flag production deployment risks.
- Do not over-comment on style-only issues unless they affect maintainability.
```

---

## 13. `KARAKANA.md` Requirements

Each project should have a `KARAKANA.md`.

Template:

```markdown
# Karakana Project Contract

## Project name

## Project type

## Durable memory

## Required skills

## Model routing

## Safety rules

## Test commands

## Deployment notes

## Approval requirements

## Known risks
```

Example for NHRDM:

```markdown
# Karakana Project Contract

## Project name

NHRDM

## Project type

Invenio Framework / InvenioRDM-based national health research data repository.

## Durable memory

Use:

- `ubongo/projects/nhrdm/overview.md`
- `ubongo/projects/nhrdm/architecture.md`
- `ubongo/projects/nhrdm/decisions.md`
- `ubongo/projects/nhrdm/deployment.md`
- `ubongo/projects/nhrdm/known-issues.md`

## Required skills

- `invenio-framework`
- `github-pr-review`
- `ci-failure-analysis`
- `python-debugging`
- `karakana-self-improvement`

## Model routing

- Planning: GPT-5 mini
- Lightweight documentation: Claude Haiku 4.5
- Complex coding: Codex GPT-5.5
- Code review: Codex GPT-5.5 plus GPT-5 mini summary
- Reflection: GPT-5 mini
- Skill improvement implementation: Codex GPT-5.5
- Skill improvement review: GPT-5 mini

## Safety rules

- Never push directly to main.
- Never modify production secrets.
- Never run destructive database commands.
- All schema changes require migration review.
- All authentication and permission changes require human approval.
- All OpenSearch index/mapping changes require explicit review.
- All behavior changes require tests.
```

---

## 14. Reflection Engine Requirements

The reflection engine must produce structured output.

Example:

```json
{
  "project": "nhrdm",
  "period": "7 days",
  "memory_updates": [
    {
      "target": "ubongo/projects/nhrdm/known-issues.md",
      "summary": "Add note about OAuth invalid_client troubleshooting",
      "risk": "low"
    }
  ],
  "skill_updates": [
    {
      "skill": "invenio-framework",
      "summary": "Add OAuth provider callback checklist",
      "risk": "medium"
    }
  ],
  "eval_updates": [
    {
      "name": "oauth-invalid-client-regression",
      "summary": "Ensure future reviews check client_id, redirect URI, provider config, and secret handling"
    }
  ],
  "requires_pr": true,
  "requires_human_review": true
}
```

Reflection must not silently apply high-risk changes.

---

## 15. Evaluation Requirements

Every skill should eventually have regression cases.

Initial evaluation types:

```text
- skill metadata validation
- prompt output shape validation
- safety rule validation
- known failure regression
- PR review quality checks
```

Examples:

```text
skills/gepg-billing/evals/
├── duplicate-payment-callback.yml
├── missing-idempotency-check.yml
└── reconciliation-mismatch.yml

skills/invenio-framework/evals/
├── custom-field-loader.yml
├── oauth-invalid-client.yml
├── opensearch-replica-yellow.yml
└── dashboard-menu-override.yml
```

Evaluations should be run in CI when skills, prompts, or core routing logic changes.

---

## 16. MVP Delivery Plan

Deliver Karakana in small increments.

### Milestone 1: Skeleton

Deliver:

* repository structure,
* `pyproject.toml`,
* CLI entrypoint,
* empty but valid modules,
* base `README.md`,
* base `AGENTS.md`,
* base `KARAKANA.md`.

### Milestone 2: `ubongo/`

Deliver:

* global memory templates,
* project memory templates,
* loader for project memory,
* simple text retrieval using file reading and search.

### Milestone 3: Skills

Deliver:

* skill loader,
* skill validator,
* initial skills:
  * `invenio-framework`,
  * `gepg-billing`,
  * `django-debugging`,
  * `github-pr-review`,
  * `ci-failure-analysis`,
  * `karakana-self-improvement`.

### Milestone 4: Router

Deliver:

* task classification,
* model routing configuration,
* fallback/escalation logic,
* prompt composition.

### Milestone 5: Codex integration

Deliver:

* `karakana codex run`,
* `.karakana/codex-task.md` generation,
* Codex task template,
* safety restrictions in prompt,
* diff/test capture if feasible.

### Milestone 6: GitHub workflows

Deliver:

* issue triage workflow,
* PR review workflow,
* skill evaluation workflow,
* CI failure analysis workflow,
* nightly reflection workflow.

### Milestone 7: Reflection and self-improvement

Deliver:

* trace format,
* reflection command,
* memory update proposals,
* skill update proposals,
* eval update proposals,
* PR creation plan.

---

## 17. Definition of Done

The first usable version of Karakana is complete when:

1. `karakana init --project <name>` creates project memory and config.
2. `karakana plan` loads `ubongo/` and a skill, then produces a structured plan.
3. `karakana skill validate` validates at least one skill.
4. `karakana codex run` generates a complete Codex task prompt.
5. The `invenio-framework` skill exists and is usable.
6. The `gepg-billing` skill exists and is usable.
7. The root `AGENTS.md` and `KARAKANA.md` exist.
8. At least one GitHub Action workflow runs.
9. Reflection can propose, but not silently apply, memory or skill updates.
10. All risky actions require approval.

---

## 18. Implementation Constraints

Follow these constraints:

* Use Python.
* Keep the first version simple.
* Prefer markdown, YAML, and JSON files over databases in the MVP.
* Avoid premature vector database complexity.
* Keep all generated changes reviewable.
* Do not implement uncontrolled autonomous loops.
* Do not require production credentials.
* Do not assume a single project.
* Design for multiple projects from day one.
* Keep naming consistent:
  * use `Karakana` for the harness,
  * use `ubongo/` for durable memory,
  * use `skills/` for reusable capabilities,
  * use `invenio-framework` for the Invenio skill.

---

## 19. Final Agent Instruction

Build Karakana as a disciplined, extensible AI workshop.

Do not chase unnecessary complexity.

Start with a strong file structure, clear memory, useful skills, safe model routing, Codex-ready task generation, and GitHub-governed improvement.

The first release should make it easy to say:

```bash
karakana plan --project nhrdm --skill invenio-framework --task "Review custom field design"
karakana codex run --project billing --skill gepg-billing --task "Fix payment callback idempotency"
karakana reflect --project karakana --since "7 days"
```

The system should improve over time, but every improvement must be visible, reviewable, testable, and reversible.
