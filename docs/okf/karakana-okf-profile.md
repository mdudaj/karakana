# Karakana OKF Profile

Status: Draft
Date: 2026-06-22

## Purpose

Define the Karakana profile for Open Knowledge Format concepts. This profile makes OKF first-class for Karakana's own self-evolving knowledge base and for projects developed through Karakana.

The profile is intentionally file-native. Concepts are Markdown files with YAML frontmatter and normal Markdown bodies. The profile should support deterministic validation and code review without requiring a hosted catalog, network service, vector database, or external provider.

## Design Principles

- OKF concepts are durable knowledge, not transient logs.
- Runtime artifacts under `.karakana/` are evidence; promotion into OKF is explicit and reviewable.
- Concepts should reference source artifacts instead of duplicating large documents.
- Agents should be able to traverse concepts by type, tags, project, status, and relationships.
- Human review remains required for safety, workflow, model, patch, and GitHub write changes.
- Project-specific OKF bundles must not contaminate global or other-project memory.

## Required Frontmatter

Every Karakana OKF concept must include:

```yaml
---
id: karakana.example.concept-id
type: Skill
title: Human-readable title
status: draft
owner: karakana
project: karakana
summary: One sentence summary.
source: path/to/source.md
tags: [karakana]
updated: 2026-06-22
---
```

## Field Rules

`id`
: Stable dotted identifier. Use `karakana.*` for harness concepts and `<project-id>.*` for project concepts.

`type`
: Required concept type. The validator must reject missing or empty values.

`title`
: Human-readable label.

`status`
: One of `draft`, `active`, `deprecated`, `superseded`, `runtime-evidence`, or `proposed`.

`owner`
: Owning knowledge domain, such as `karakana`, `msc-platform`, or `global`.

`project`
: Project ID when project-specific. Use `global` for global engineering knowledge.

`summary`
: One sentence summary for context loaders.

`source`
: Source artifact path or URL. Local paths are preferred for repository-owned knowledge.

`tags`
: Lowercase tags for retrieval.

`updated`
: ISO date.

## Recommended Frontmatter

```yaml
relationships:
  implements: []
  depends_on: []
  supersedes: []
  related_to: []
safety:
  requires_approval_for: []
  blocked_paths: []
verification:
  commands: []
```

## Concept Types

Initial allowed types:

- `Project`
- `Skill`
- `Skillpack`
- `ADR`
- `Requirement`
- `UserStory`
- `Milestone`
- `ImplementationInstruction`
- `Handoff`
- `Schema`
- `CodeComponent`
- `Workflow`
- `SafetyRule`
- `ModelRoute`
- `Eval`
- `Verification`
- `DesignSystemRule`
- `ResearchEvidenceContract`
- `Lesson`
- `ImprovementProposal`
- `RuntimeEvidence`

The type list should be versioned by this profile. New types require a profile update and validator tests.

## Repository Layout

Recommended generated and curated layout:

```text
okf/
  index.md
  karakana/
    project.md
    skills/
    skillpacks/
    adr/
    safety/
    model-routes/
    improvement/
  projects/
    msc-platform/
      index.md
      requirements/
      schemas/
      design-system/
      curriculum/
      workflows/
      verification/
  logs/
    promotion-log.md
```

## Runtime Artifact Promotion

Promotion from `.karakana/` to OKF must record:

- source runtime artifact path
- promoted concept ID
- reason for promotion
- reviewer or approving user
- date
- changed source references
- verification command

Runtime artifacts must not be bulk-promoted by default.

## Validator Requirements

`karakana okf validate` must:

- parse Markdown frontmatter deterministically
- reject missing `type`
- reject missing required fields
- reject unknown type values unless `--allow-unknown-types` is passed
- warn on missing local source paths
- warn on unresolved local concept relationships
- reject project concepts that claim another project without explicit crosslink metadata
- reject blocked paths and secret-like source paths
- report concept counts by type and project

## Context Loader Requirements

OKF-aware context loading must:

- load only relevant concepts for the current project and task
- prefer active concepts over draft or deprecated concepts
- follow relationships with a bounded depth
- include source paths so agents can inspect authoritative files
- avoid loading raw runtime logs unless the task explicitly requires them
- record loaded concept IDs in the handoff

## First Bundles

Karakana bundle:

- project overview
- `KARAKANA.md`
- active skillpack
- delivery artifact gate skill
- Karakana self-improvement skill
- handoff model
- safety rules
- model routing policy
- OKF ADR and profile

`msc-platform` bundle:

- project overview
- active skillpack
- curriculum source/snapshot evidence contract
- dashboard/design-system contract
- schema contracts
- evaluation workflow contracts
- latest relevant handoff references

## Verification

Initial verification should include:

- unit tests for parser and validator
- fixture tests for valid and invalid concepts
- CLI tests for `karakana okf validate`
- context-selection tests with bounded traversal
- `karakana skill validate-all`
- focused evals for self-improvement and handoff behavior
