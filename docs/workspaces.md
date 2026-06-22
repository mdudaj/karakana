# Karakana Workspaces

Workspaces describe a set of projects Karakana can coordinate without mixing their state.

## Purpose

A workspace gives Karakana read-only visibility across projects while preserving project boundaries. It records each project path, skillpack, memory path, standard commands, tags, and expected validation routines.

## Workspaces vs Skillpacks

Skills describe reusable workflows. Skillpacks describe how Karakana should work on one project. Workspaces group multiple projects and point each project at its own skillpack and memory.

## Creating a Workspace

Create a YAML file under `workspaces/` with `name`, `description`, `version`, `status`, `defaults`, and `projects`.

Each project should include:

- `id`
- `path`
- `skillpack`
- `memory`
- `standard_commands`

## Validation

Run:

```bash
karakana workspace validate nimr
karakana workspace validate-all
```

When `require_existing_paths` is false, missing project directories produce warnings. When true, missing paths are errors.

## Activation

Activation writes `.karakana/current-workspace.json` and does not modify source files:

```bash
karakana workspace activate nimr
karakana workspace current
```

## Status

Workspace status is read-only. It checks configured paths, git branch, git status, skillpack validity, memory existence, and local Karakana artifact counts.

## Planning

Workspace planning prepares one project-specific planning prompt at a time:

```bash
karakana workspace plan --project billing --task "Review GePG callback issue"
```

It does not execute Codex or mutate project files.

Workspace planning autoloads or recovers the selected project's session handoff. Use `--no-handoff` only when intentionally starting without prior continuation context.

After reviewing workspace status, optionally include that project-specific state in a next-milestone decision:

```bash
karakana milestone next --workspace nimr --project msc-platform --skillpack msc-platform --write-instructions
```

The command reads one project's workspace status and keeps project memory boundaries intact.

## Handoff

Workspace handoff creates `.karakana/workspace-handoffs/<handoff-id>/` with a project-specific handoff document.

Workspace handoff is a status snapshot. Cross-session continuation uses the project handoff store:

```bash
karakana handoff load --workspace nimr --project msc-platform --skillpack msc-platform
karakana handoff refresh --workspace nimr --project msc-platform --skillpack msc-platform --purpose "End of task handoff"
```

## Cross-Project Knowledge Links

Crosslinks compare workspace project metadata, skillpacks, and safe artifact summaries to detect shared workflow patterns, shared risks, shared skill needs, shared eval needs, and conflicting conventions:

```bash
karakana crosslink scan --workspace nimr
karakana crosslink scan --workspace nimr --projects billing,lims
karakana crosslink review <crosslink-id>
karakana crosslink propose <crosslink-id>
karakana crosslink apply <crosslink-id>
```

Crosslink artifacts are written under `.karakana/crosslinks/`. Proposal generation is reviewable and apply is dry-run by default. Crosslink apply may write only explicit shared knowledge updates and must not write project-specific `ubongo/projects/*/` memory.

## Boundary Rules

- Do not mix project memory.
- Do not silently substitute skillpacks.
- Do not apply patches across projects.
- Do not bulk execute Codex.
- Do not ingest all projects automatically.
- Do not copy project-specific memory through crosslinks.
- Do not push, create PRs, deploy, or mutate source files from workspace commands.

## MSc Research Platform

The `nimr` workspace uses `msc-platform` for the repository at `../stemgen-platform`. This repository was previously referenced as `msc-dissertation`, but Karakana treats it as a research software platform for prototype implementation, evaluation workflow support, and evidence generation. It is not treated as the dissertation manuscript repository.
