---
id: karakana.protocol.core-work-protocols
type: WorkProtocol
title: Core Work Protocols
status: active
owner: karakana
project: karakana
summary: Protocol set covering requirements, architecture, UX, data migration, safety policy, skill, memory, release, and Python implementation work.
source: protocols
tags: [karakana, protocol, governance, reproducibility]
updated: 2026-07-03
relationships:
  related_to:
    - karakana.protocol.system
    - karakana.protocol.python-code-change
    - karakana.protocol.artifact-gate
---

# Core Work Protocols

Karakana core work protocols define deterministic steps, roles, artifacts, approval gates, and verification expectations by work category.

The core set currently includes:

- `requirements-change`
- `architecture-decision`
- `ux-change`
- `data-migration`
- `safety-policy-change`
- `skill-update`
- `memory-update`
- `release-change`
- `python-code-change`

Skillpacks map work categories to these protocols so classification can select category-specific artifact gates.

The `requirements-change` path requires PRD, requirements, user-story, acceptance, traceability, readiness, definition-of-done, verification, and handoff artifacts before implementation handoff.

The `ux-change` and UX-conditioned `python-code-change` paths require behavior and look-and-feel requirements, task-specific best-practice research, design-system fit, accessibility checks, render evidence, and artifact readiness. Behavior-changing implementation paths also require PRD/requirements coverage, user stories, acceptance criteria, definition of done, traceability, and test/eval rationale.
