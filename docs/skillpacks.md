# Skillpacks

Karakana skillpacks are project profiles stored under `skillpacks/<name>.yml`.

Skills describe reusable workflows. Skillpacks describe how Karakana should work on a specific project: which skills to load, where memory lives, which model routes to prefer, which paths are high-risk, which tests are expected, and which project conventions matter.

## Why Skillpacks Exist

A project should declare how Karakana should work on it. This keeps project-specific safety rules and conventions out of generic skills while making planning, patch gates, and Codex handoffs more precise.

## Creating a Skillpack

Create a YAML file under `skillpacks/` with:

- `name`, `description`, `version`, and `status`
- `project.id`, optional display name, memory path, and contract path
- required and optional skills
- model route overrides
- high-risk and blocked paths
- approval requirements
- test commands
- project conventions

## Validation

Validate one skillpack:

```bash
karakana skillpack validate nhrdm
```

Validate all skillpacks:

```bash
karakana skillpack validate-all
```

Missing required skills are errors. Missing optional skills or project memory paths are warnings. Missing memory is allowed because starter skillpacks may exist before durable memory is initialized.

## Activation

Activate a skillpack locally:

```bash
karakana skillpack activate nhrdm
```

Activation writes `.karakana/current-skillpack.json`. It does not modify source files, switch branches, run tests, call models, push, create PRs, or deploy.

Show the active skillpack:

```bash
karakana skillpack current
```

## Planning

Use a project skillpack explicitly:

```bash
karakana plan --project nhrdm --use-skillpack --task "Review custom field migration risks"
```

Use the active skillpack:

```bash
karakana plan --use-current-skillpack --task "Review project risk"
```

Skillpack planning includes required skills, optional skills, conventions, safety paths, approval requirements, recommended tests, and skillpack model routes.

## Model Routing

Skillpack model routes override global defaults for matching task types. Manual `--provider` and `--model` overrides still win and are recorded as manual overrides in traces.

## Patch Gates

Patch gates can use skillpack high-risk and blocked paths:

```bash
karakana patch gate --patch-run <patch-run-id> --skillpack nhrdm
```

If no skillpack is passed, Karakana uses the active skillpack when one exists.

## Codex Handoff

Codex handoff can include skillpack context:

```bash
karakana codex handoff <action-run-id> --skillpack nhrdm
```

The generated handoff includes skillpack skills, conventions, recommended tests, high-risk paths, blocked paths, and approval requirements.

## Workspaces

Workspaces group multiple projects and assign each project its own skillpack and memory path.

Use:

```bash
karakana workspace list
karakana workspace status --project nhrdm
```

Skillpacks remain project-level configuration. Workspaces coordinate visibility across projects while preserving each project's skillpack, memory, safety paths, and status.

## MSc Research Platform Skillpack

Use `msc-platform` for `stemgen-platform`, the MSc research implementation and evaluation platform. Use `research-platform` with `research-writing` so implementation work stays aligned with research objectives, evaluation activities, evidence generation, privacy, and reproducibility. Keep `msc-research` for manuscript-oriented research writing workflows.
