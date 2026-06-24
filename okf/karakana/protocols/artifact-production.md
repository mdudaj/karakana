---
id: karakana.protocol.artifact-production
type: WorkProtocol
title: Protocol Artifact Production
status: active
owner: karakana
project: karakana
summary: Template and attachment workflow for producing evidence that satisfies protocol-required artifacts.
source: karakana/protocols/artifacts.py
tags: [karakana, protocol, artifacts, reproducibility]
updated: 2026-06-24
relationships:
  related_to:
    - karakana.protocol.system
    - karakana.protocol.artifact-gate
    - karakana.protocol.rollout
    - karakana.protocol.task-start
---

# Protocol Artifact Production

Protocol artifact production provides templates and trace attachment commands for missing required artifacts.

The intended loop is classify, inspect missing artifacts, render or write templates, attach completed artifacts to the trace, and run the protocol check again.

Operational usage is documented in `docs/protocols.md`.

UX-impacting feature artifacts must include behavior requirements, look-and-feel requirements, best-practice research for the delivered task, and design-system fit.
