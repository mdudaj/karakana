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
updated: 2026-06-24
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

The `ux-change` and UX-conditioned `python-code-change` paths require a requirements note that describes intended behavior, look and feel, task-specific best-practice research, and alignment with the existing design system.
