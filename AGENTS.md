# Agent Instructions

This repository uses Karakana.

## Repository Entry Points

- CLI entrypoint: `karakana/cli.py`
- Durable memory loader: `karakana/memory/ubongo.py`
- Skill loader and validator: `karakana/skills/loader.py`, `karakana/skills/validator.py`
- Model routing and providers: `karakana/models/`
- GitHub context and API tooling: `karakana/tools/github.py`, `karakana/tools/github_api.py`
- Trace storage: `karakana/traces/`
- Improvement proposals: `karakana/improvement/`
- Evaluation harness: `karakana/evals/`
- Project contract: `KARAKANA.md`
- Agent guide: `KARAKANA_AGENT_GUIDE.md`

## Standard Commands

```bash
karakana --help
karakana skill validate-all
karakana eval run
pytest
```

Use focused commands when possible:

```bash
karakana memory validate --project karakana
karakana model check
karakana model route --task-type planning
karakana trace latest
karakana skillpack validate-all
```

## Start Every Task

Codex should run the project-local `.codex/hooks.json` `SessionStart` hook on trusted projects. If Codex reports that hooks need review, open `/hooks`, review the Karakana handoff hook, and trust it before relying on automatic loading.

1. Run `karakana handoff load --project <project> --skillpack <skillpack>`.
   If `karakana` is not on PATH, run `.venv/bin/karakana handoff load --project <project> --skillpack <skillpack>` from the repository root.
2. Read mandatory repository instructions, then inspect only the files listed under `Files to Inspect First`.
3. Treat `Files Not to Reread` as advisory; it never overrides `AGENTS.md`, `KARAKANA.md`, safety rules, or files required by the current task.
4. Verify recovered or stale handoffs before acting.
5. For non-trivial work, run `karakana protocol start --task "<task>" --project <project> --write-plan` or classify the task with the active protocol before editing.

## End Every Task

Run:

```bash
karakana handoff refresh \
  --project <project> \
  --skillpack <skillpack> \
  --purpose "End of task handoff"
```

Record verification, unresolved findings, changed references, and the exact next action. Handoffs are append-only runtime artifacts under `.karakana/handoffs/` and must not be committed.

If the active trace has protocol-required artifacts, run `karakana protocol check --trace <run-id>` before or during handoff refresh. Use `karakana protocol missing`, `karakana protocol template`, and `karakana protocol attach` to close artifact gaps.

Use project skillpacks when available:

```bash
karakana skillpack list
karakana skillpack activate karakana
karakana protocol start --task "Review project risk" --project karakana --write-plan
karakana plan --use-current-skillpack --task "Review project risk"
karakana workspace list
karakana workspace status
karakana workspace handoff --project karakana
```

## Model Routing

Use cost-effective routing by default:

- Claude Haiku 4.5 for lightweight documentation, issue triage, changelog, and summary work.
- GPT-5 mini for planning, architecture reasoning, reflection, skill design, and action extraction review.
- Codex GPT-5.4-mini for routine code edits, simple tests, and Codex task drafting.
- Codex GPT-5.4 for refactoring, CI repair, deep PR review, and framework-level implementation.
- Codex GPT-5.5 only for high-risk or stuck work: authentication, authorization, payment, billing, migrations, OpenSearch index changes, Viewflow process-state changes, production deployment risk, or repeated failures.

Manual overrides are allowed, but record the rationale in traces or task notes.

## How to Add a Skill

1. Create `skills/<skill-name>/SKILL.md`.
2. Include required front matter: `name`, `description`, `version`, `risk_level`, `allowed_tools`, and `requires_approval_for`.
3. Add optional governance metadata when useful: `activation`, `category`, and `scope`.
4. Include the standard sections plus recommended sections: `Quick Reference`, `Pitfalls`, and `Verification`.
5. Add evals under `skills/<skill-name>/evals/` for important workflows.
6. Run `karakana skill validate-all` and `karakana eval run`.

Use `viewflow-framework` for workflow, frontend, process-state, task-transition, approval, assignment, and workflow-permission tasks.
Combine it with `django-debugging` for general Django errors.
Combine it with `gepg-billing` when billing workflows use Viewflow.
Combine it with `invenio-framework` when repository or project workflows use Viewflow.

## How to Add a Tool

1. Prefer a skill when workflow guidance is enough.
2. Create a tool when deterministic execution, parsing, authentication, API handling, binary data, or programmatic safety gates are required.
3. Place tool code under `karakana/tools/` unless a narrower package owns it.
4. Add safety checks for write operations, credentials, destructive behavior, and production risk.
5. Add tests that do not require network access or real credentials.
6. Keep tools tightly scoped and avoid autonomous mutation.

## How to Update Ubongo

1. Edit markdown under `ubongo/global/` or `ubongo/projects/<project>/`.
2. Preserve human-readable source-of-truth memory.
3. Do not store secrets, tokens, `.env` content, or private key material.
4. Run `karakana memory validate --project <project>`.
5. Add or update evals if memory changes alter expected workflows.

## How to Run Evals

Use local deterministic evals before changing skills, prompts, routing, providers, safety policies, GitHub automation, or self-improvement behavior.

```bash
karakana eval list
karakana eval run
karakana eval run --skill invenio-framework
karakana eval run --suite safety
```

Eval reports are written under `.karakana/eval-runs/` and must not be committed.

## How to Use Workspaces

Use workspaces for multi-project visibility without context mixing:

```bash
karakana workspace validate-all
karakana workspace activate nimr
karakana workspace status --project nhrdm
karakana workspace plan --project billing --task "Review GePG callback issue"
karakana crosslink scan --workspace nimr --projects billing,lims
```

Workspace commands must stay read-only unless a later explicit project-specific command is used. Do not use workspace commands to bulk execute Codex, apply patches, ingest all projects, push, create PRs, deploy, or mix one project memory path into another project.

For the MSc implementation platform, use project ID `msc-platform`, skillpack `msc-platform`, and path `../stemgen-platform`. This repository was previously named `msc-dissertation`; treat it as a research software platform, not as the dissertation manuscript.

## How to Use Crosslinks

Use crosslinks to detect reusable lessons, shared risks, skill gaps, and eval opportunities across workspace projects without copying project-specific memory:

```bash
karakana crosslink scan --workspace nimr
karakana crosslink review <crosslink-id>
karakana crosslink propose <crosslink-id>
karakana crosslink apply <crosslink-id>
```

Crosslink apply is dry-run by default. Do not use crosslinks to write `ubongo/projects/*/`, mutate source code, execute Codex, push, create PRs, deploy, or move one project's memory into another project.

## Safety Rules

Before planning or editing code:

1. Read `KARAKANA.md`.
2. Read relevant files under `ubongo/projects/<project>/`.
3. Load any relevant skill from `skills/<skill>/SKILL.md`.
4. Respect safety rules.
5. Prefer patches and pull requests over direct changes.
6. Do not touch secrets.
7. Run relevant tests.
8. Document risks.

Never commit or print secrets, tokens, `.env` contents, API keys, authorization headers, or private key material.
Do not deploy, auto-merge, push to protected branches, or run destructive commands without explicit approval.
Live model calls and GitHub writes must remain explicit opt-in.

## Files Requiring Extra Caution

- `.github/workflows/**`
- `karakana/tools/github_api.py`
- `karakana/safety/**`
- `karakana/models/providers/**`
- `karakana/models/router.py`
- `karakana/models/escalation.py`
- `karakana/improvement/**`
- `KARAKANA.md`
- `AGENTS.md`
- `pyproject.toml`
- Any migration, deployment, authentication, permission, billing, or secret-related file

## Pull Request Expectations

Prefer reviewable patches and pull requests over direct changes.
Every behavior change should include tests or eval coverage.
Summaries should list changed files, commands run, test results, risks, and remaining TODOs.
Generated runtime artifacts under `.karakana/` must not be committed.

## Code Review

For code review:

- Flag serious correctness issues.
- Flag security regressions.
- Flag unsafe migrations.
- Flag missing tests.
- Flag production deployment risks.
- Do not over-comment on style-only issues unless they affect maintainability.
