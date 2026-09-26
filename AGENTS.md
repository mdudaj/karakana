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

Every fresh agent session and every new bounded task starts from the latest project handoff summary.

1. Run `karakana handoff load --project <project> --skillpack <skillpack>`.
   If `karakana` is not on PATH, run `.venv/bin/karakana handoff load --project <project> --skillpack <skillpack>` from the repository root.
2. Read mandatory repository instructions, then inspect only the files listed under `Files to Inspect First`.
3. Treat `Files Not to Reread` as advisory; it never overrides `AGENTS.md`, `KARAKANA.md`, safety rules, or files required by the current task.
4. Verify recovered or stale handoffs before acting.
5. For non-trivial work, run `karakana protocol start --task "<task>" --project <project> --write-plan` or classify the task with the active protocol before editing.

## Engineering Process

Follow `docs/engineering-process.md`: orient/classify → define acceptance →
research/design → plan → implement → verify/validate → review → authorized
release → handoff. Reuse current approved artifacts; reopen only affected stages.
Tailor to the request and risk: analysis is not implementation authorization, and
a mechanical fix does not need a fresh PRD/ADR. Keep one compact delivery record.

For non-trivial implementation, attach prerequisite evidence and run
`karakana protocol check --trace <id> --stage pre-implementation` before code.
After verification and handoff, run `--stage completion` (the default).
These checks validate artifact presence, not semantic correctness, test success
or approval. Review the actual outcomes; never substitute attachment for review.
Report implemented, verified, merged, deployed and accepted as distinct states.
Use existing task approval for in-scope work without repeatedly asking, but stop
for new scope, missing material decisions or actions requiring new authority.

## End Every Task

Every bounded task must finish with an append-only handoff refresh so the next session can load current continuation context.

Run:

```bash
karakana handoff refresh \
  --project <project> \
  --skillpack <skillpack> \
  --purpose "End of task handoff"
```

Record verification, unresolved findings, changed references, remaining tasks,
the recommended next task, and the exact next action. New handoffs are
append-only runtime artifacts under `.karakana/handoffs/<project>/` and must
not be committed. Legacy flat handoffs under `.karakana/handoffs/<handoff-id>/`
may be read for backward compatibility only.

Every completed slice summary must include:

- what was completed;
- verification performed;
- remaining tasks or known follow-ups;
- the recommended next task.

If the active trace has protocol-required artifacts, run `karakana protocol check --trace <run-id>` before or during handoff refresh. Use `karakana protocol missing`, `karakana protocol template`, and `karakana protocol attach` to close artifact gaps.

Use project skillpacks when available:

```bash
karakana skillpack list
karakana skillpack activate karakana
karakana protocol start --task "Review project risk" --project karakana --write-plan
karakana protocol start --task "Assess harness state" --project karakana --category assessment --write-plan
karakana plan --use-current-skillpack --task "Review project risk"
karakana workspace list
karakana workspace status
karakana workspace handoff --project karakana
```

## Model Routing

### Cost-aware execution and continuation

Follow `docs/cost-aware-continuation.md`: research → architect → plan → deliver.
Inspect existing evidence for currency, applicability and approval; skip satisfied
stages and go straight to delivery when all prerequisites hold. Do not repeat
broad research or create duplicate architecture/planning artifacts.

Apply suggestions 2–7: research only new uncertainties; focused debugging tests
then the full required regression gate; bounded tool output; one compact delivery
record plus linked handoff; stop speculative patches after two failed diagnostic
attempts and escalate/replan; no automatic agent fan-out or maximum reasoning.

At handoff refresh supply `--next-task`, reviewed `--reuse-stage STAGE=PATH`
references with `--reuse-reviewed`, `--slice-complete` at a completed boundary,
and `--failed-attempts` for an unresolved diagnostic loop. Report the recommended
model and whether a fresh conversation benefits the next task. Recommendations
do not switch an active session or certify model availability. Verify the active
model; record an override when necessary. Preserve failures across conversations.

Use cost-effective routing by default:

- GPT-6 Sol, medium reasoning: control-plane judgment, planning, architecture, coordinated implementation and review.
- GPT-6 Luna, high reasoning (documented starting setting): bounded research, summaries, routine edits, tests and documentation.
- GPT-6 Sol, high reasoning: authentication, authorization, billing, migrations, workflow state, model routing, safety policy and production risk.
- GPT-6 Astra, low reasoning initially: explicit exceptional-task override after a recorded justification; never the automatic default or automatic response to a failed test.
- GPT-5.6 Luna/Sol: explicit availability fallback for the matching capability tier. No silent downgrade or automatic paid retry. Retain other legacy models as manual overrides.

See `docs/gpt-6-routing.md`. Routing and approval checks stay deterministic; no
always-running controller or automatic agent fan-out. After two failed diagnostic
attempts, stop speculative edits and replan/escalate; Sol-to-Astra is advisory only.

Manual overrides are allowed, but record the rationale in traces or task notes.

Karakana should infer the model route from the natural-language task whenever possible. Use explicit `karakana model route --task-type ...` only when deterministic routing is needed; otherwise prefer `karakana model route --task "<task>"` or entrypoints such as `karakana plan --task "<task>"` that classify the task automatically.

Use the `assessment` protocol for analysis-only harness reviews, recommendations, and state assessments that should not require ADR or rollback artifacts unless a later implementation changes architecture or behavior.

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

All research, brainstorming, implementation, debugging, documentation, and review must be evidence-grounded. Check authoritative project artifacts, relevant skills, repository source, schemas, exported/generated artifacts, official docs for unstable external systems, runtime output, and tests/evals before treating a claim as fact. Non-trivial delivery must include implementation instructions that name what to inspect, what references govern the work, what steps to follow, and how to verify. If a repeated miss reveals a reusable rule, update durable memory, skills, docs, validators, or evals before considering the lesson handled.

Never commit or print secrets, tokens, `.env` contents, API keys, authorization headers, or private key material.
Do not deploy, auto-merge, push to protected branches, or run destructive commands without explicit approval.
Live model calls and GitHub writes must remain explicit opt-in.
All repository work must happen on a non-protected branch and be delivered through a pull request. When the user asks to merge completed work, squash merge the PR into the target branch after validation instead of committing or merging directly on `main`.
Features with UX impact must have requirements that describe both intended behavior and look and feel before implementation. Default to researching current best practices for the delivered task and applying them through the existing project design system rather than inventing page-local styling.

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

Use reviewable patches and pull requests for all repository changes.
Create or switch to a task branch before editing files.
Every behavior change should include tests or eval coverage.
When work is accepted for integration, use a squash merge unless the user explicitly requests a different merge strategy.
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
