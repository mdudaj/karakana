---
id: karakana.protocol.python-code-change
type: WorkProtocol
title: Python Code Change Protocol
status: active
owner: karakana
project: karakana
summary: Protocol for Python implementation changes with conditional artifacts for behavior, UX, architecture, data/migration, and safety impact.
source: protocols/python-code-change.yml
tags: [karakana, protocol, python, implementation, reproducibility]
updated: 2026-06-23
relationships:
  related_to:
    - karakana.protocol.system
    - karakana.protocol.artifact-gate
    - karakana.skillpack
    - karakana.safety.rules
---

# Python Code Change Protocol

The Python code-change protocol defines the deterministic workflow for implementation work.

Always-required artifacts include task classification, trace, change summary, verification summary, and handoff.

Conditional artifacts add requirements notes, user stories, UX descriptions, ADRs, schema or migration plans, approval records, safety reviews, and threat or abuse-case notes when the classified task requires them.
