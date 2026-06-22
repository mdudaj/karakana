# Karakana

Karakana is a GitHub-native AI agent harness for managing multiple software, research, and infrastructure projects.

The goal is to provide a disciplined technical workshop where durable memory, reusable skills, model routing, GitHub workflows, evaluations, and human review work together.

```text
Karakana thinks and remembers.
Codex codes and tests.
GitHub governs.
Humans approve.
```

## Current Scope

The current implementation covers the local Karakana harness through evaluation and governance cleanup:

- Python package and CLI named `karakana`
- durable markdown memory under `ubongo/`
- project memory loading, validation, listing, and summary display
- reusable markdown skills under `skills/`
- prompt generation for planning, GitHub tasks, and Codex task prompts
- local traces under `.karakana/runs/`
- self-improvement proposal artifacts under `.karakana/proposals/`
- deterministic eval reports under `.karakana/eval-runs/`
- model provider abstraction with dry-run defaults
- cost-effective model routing and escalation guidance
- GitHub workflow scaffolding and explicit opt-in GitHub writes

## CLI

```bash
karakana --help
karakana version
karakana memory list-projects
karakana memory validate --project karakana
karakana memory show --project karakana
karakana skill list
karakana skill show invenio-framework
karakana skill validate skills/invenio-framework
karakana skill validate-all
karakana plan --project karakana --skill karakana-self-improvement --task "Design the next improvement loop"
karakana codex run --project karakana --skill karakana-self-improvement --task "Implement reflection trace schema"
karakana eval run
karakana model route --task-type planning
karakana model route --task-type routine_code_implementation
karakana skillpack list
karakana skillpack validate-all
karakana handoff load --project msc-platform --skillpack msc-platform
karakana milestone next --project msc-platform --skillpack msc-platform --write-instructions
karakana workspace list
karakana workspace status
karakana crosslink scan --workspace nimr
```

## Model Routing

Karakana uses the cheapest capable model first:

- Claude Haiku 4.5: fast low-cost issue triage, documentation, changelog, and summaries.
- GPT-5 mini: planning, architecture reasoning, reflection, skill design, and action extraction review.
- Codex GPT-5.4-mini: routine code implementation, simple tests, and Codex task drafting.
- Codex GPT-5.4: serious day-to-day coding, refactoring, CI repair, framework implementation, and deep PR review.
- Codex GPT-5.5: principal-level escalation for authentication, payments, migrations, process-state changes, production risk, high-risk review, or repeated failures.

Inspect routing decisions with:

```bash
karakana model route --task-type payment_or_billing_logic
```

## Skills and Tools

Skills live under `skills/<name>/SKILL.md` and describe repeatable workflows, risks, checks, and output expectations.
Tools live under `karakana/tools/` and execute tightly scoped deterministic operations.

Use `viewflow-framework` for Django Viewflow workflow, frontend, process-state, task-transition, approval, assignment, and workflow-permission tasks.
Combine it with `django-debugging` for general Django errors, `gepg-billing` when billing workflows use Viewflow, and `invenio-framework` when repository or project workflows use Viewflow.

See:

- `docs/skills.md`
- `docs/skillpacks.md`
- `docs/workspaces.md`
- `docs/skill-vs-tool-policy.md`

## Repository Layout

```text
karakana/
├── karakana/          # Python package
├── skills/            # reusable skill instructions
├── evals/             # built-in evaluation cases
├── ubongo/            # durable project and global memory
├── workspaces/        # multi-project workspace definitions
├── docs/              # governance and contributor guidance
├── AGENTS.md          # coding-agent instructions
├── KARAKANA.md        # project contract
└── KARAKANA_AGENT_GUIDE.md
```

## Safety Principles

- Important changes should be traceable through GitHub.
- Memory and skill changes should be proposed through pull requests.
- Risky actions require explicit human approval.
- The harness must not silently mutate production systems, secrets, or protected branches.
- The MVP should prefer markdown, YAML, and JSON over databases.

## Development Status

Live model calls, Codex execution, GitHub writes, and proposal application remain explicit opt-in paths. The default workflow is local, deterministic, artifact-based, and reviewable.

## Workspaces

Workspaces group projects while keeping their memory, skillpacks, paths, and status separate.

```bash
karakana workspace list
karakana workspace validate nimr
karakana workspace activate nimr
karakana workspace status --project nhrdm
karakana workspace handoff --project nhrdm
```

Workspace commands are read-only by default and do not run arbitrary project commands, execute Codex, apply patches, push, create PRs, deploy, or mix project memory.

The `nimr` workspace includes `msc-platform` at `../stemgen-platform`, the MSc research implementation and evaluation platform. This repository was previously named `msc-dissertation`; Karakana treats it as software for prototype workflow, evaluation support, and evidence generation rather than as a dissertation manuscript repository.

## Next Milestone Decisions

Before returning to an external assistant to ask "what next?", generate a local evidence-based decision:

```bash
karakana milestone next \
  --project msc-platform \
  --skillpack msc-platform \
  --workspace nimr \
  --write-instructions
```

The command inspects local project context and recent artifacts, writes a multi-criteria candidate decision under `.karakana/milestones/`, refreshes the project handoff unless opted out, and never executes, pushes, or deploys the generated instruction.

## Session Handoffs

This repository includes a project-local Codex `SessionStart` hook in `.codex/hooks.json`. In a trusted Codex project, the hook runs `.codex/hooks/karakana_session_start.sh` on startup or resume, loads the Karakana handoff, and writes the rendered session context to `.karakana/session-start.md`. Treat the hook as a durable local artifact writer; Codex hook stdout can appear after the first prompt in local UI builds.

Codex requires review and trust for non-managed project hooks. If a new session warns that hooks need review, open `/hooks`, inspect the Karakana handoff hook, and trust it before relying on automatic loading.

Start every task by loading the latest project handoff. If none exists, Karakana recovers a lightweight handoff from bounded recent artifacts:

```bash
karakana handoff load --project <project> --skillpack <skillpack>
```

To start an interactive agent while making the handoff visible before the agent UI takes over, use the Karakana launchers:

```bash
karakana codex start --project <project> --skillpack <skillpack> -- [codex args...]
karakana copilot start --project <project> --skillpack <skillpack> -- [copilot args...]
```

The launchers write `.karakana/session-start.md`, print and flush the session-start context, and then start the target CLI. For fresh interactive Codex launches, `karakana codex start` also writes `.karakana/codex-initial-prompt.md` and passes that context as Codex's initial prompt, so the model receives the handoff before the first user task instead of relying on delayed hook stdout. It skips prompt injection for Codex subcommands such as `resume`, for existing user prompts, and when `--no-inject-prompt` is used. `karakana codex start` bootstraps a missing project `.venv` by running `python -m venv .venv` and `.venv/bin/python -m pip install -e ".[dev]"` before launching Codex when a Karakana entrypoint is already available. If `karakana` is not on `PATH` and `.venv` is missing, run `python -m karakana codex start --project <project>` from the source checkout to bootstrap and re-enter through the new venv. Use `--no-bootstrap` to skip setup. `--print-only` previews without creating the environment or launching Codex. `karakana codex start --inline` passes `--no-alt-screen` to Codex so the printed context remains in terminal scrollback. Without `--inline`, both launchers pause before starting the target CLI unless `--no-pause` is used.

Read mandatory repository instructions and the listed inspect-first files. Do not reread files marked advisory unless the current task needs them.

End every task with an append-only refresh:

```bash
karakana handoff refresh --project <project> --skillpack <skillpack> --purpose "End of task handoff"
karakana handoff doctor --project <project>
```

Planning commands autoload the matching handoff unless `--no-handoff` is used. `milestone next` appends a handoff unless `--no-handoff-refresh` is used. Other project commands record a refresh reminder in their trace.

## Cross-Project Knowledge Links

Crosslinks scan workspace metadata, skillpacks, and safe artifact summaries to find reusable patterns without copying project memory:

```bash
karakana crosslink scan --workspace nimr
karakana crosslink scan --workspace nimr --projects billing,lims
karakana crosslink review <crosslink-id>
karakana crosslink propose <crosslink-id>
karakana crosslink apply <crosslink-id>
```

Crosslink apply is dry-run by default. Explicit writes are limited to shared knowledge paths and must not write to `ubongo/projects/*/`, mutate source code, execute Codex, push, create PRs, or deploy.
