# Karakana

Karakana is a GitHub-native AI agent harness for managing multiple software, research, and infrastructure projects.

The goal is to provide a disciplined technical workshop where durable memory, reusable skills, model routing, GitHub workflows, evaluations, and human review work together.

```text
Karakana thinks and remembers.
Codex codes and tests.
GitHub governs.
Humans approve.
```

## MVP Scope

The first version focuses on a simple, reviewable local harness:

- Python package and CLI named `karakana`
- durable markdown memory under `ubongo/`
- reusable skills under `skills/`
- safe model routing policy
- Codex-ready task prompt generation
- skill validation and lightweight evaluations
- GitHub Actions for reviewable automation

## Planned CLI

```bash
karakana init --project nhrdm
karakana plan --project nhrdm --skill invenio-framework --task "Review custom field design"
karakana codex run --project billing --skill gepg-billing --task "Fix payment callback idempotency"
karakana reflect --project karakana --since "7 days"
karakana skill validate skills/invenio-framework
karakana eval run --skill invenio-framework
```

## Repository Layout

```text
karakana/
├── karakana/          # Python package
├── ubongo/            # durable project memory
├── skills/            # reusable workflow skills
├── prompts/           # prompt templates
├── evals/             # regression and validation cases
├── .github/workflows/ # GitHub automation
├── AGENTS.md          # coding-agent instructions
├── KARAKANA.md        # project contract
└── instructions.md    # implementation guide
```

## Safety Principles

- Important changes should be traceable through GitHub.
- Memory and skill changes should be proposed through pull requests.
- Risky actions require explicit human approval.
- The harness must not silently mutate production systems, secrets, or protected branches.
- The MVP should prefer markdown, YAML, and JSON over databases.

## Development Status

This repository is at the bootstrap stage. The implementation guide is in `instructions.md`.
