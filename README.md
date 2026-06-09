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
```

## Skills and Tools

Skills live under `skills/<name>/SKILL.md` and describe repeatable workflows, risks, checks, and output expectations.
Tools live under `karakana/tools/` and execute tightly scoped deterministic operations.

Use `viewflow-framework` for Django Viewflow workflow, frontend, process-state, task-transition, approval, assignment, and workflow-permission tasks.
Combine it with `django-debugging` for general Django errors, `gepg-billing` when billing workflows use Viewflow, and `invenio-framework` when repository or project workflows use Viewflow.

See:

- `docs/skills.md`
- `docs/skill-vs-tool-policy.md`

## Repository Layout

```text
karakana/
├── karakana/          # Python package
├── skills/            # reusable skill instructions
├── evals/             # built-in evaluation cases
├── ubongo/            # durable project and global memory
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
