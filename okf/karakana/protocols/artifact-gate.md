---
id: karakana.protocol.artifact-gate
type: Verification
title: Protocol Artifact Gate
status: active
owner: karakana
project: karakana
summary: Verification gate that checks whether a run trace satisfies evidence-backed PRD, readiness, traceability, UX, architecture, and verification artifacts derived from its work protocol.
source: karakana/protocols/checks.py
tags: [karakana, protocol, verification, reproducibility]
updated: 2026-07-03
relationships:
  related_to:
    - karakana.protocol.system
    - karakana.protocol.python-code-change
    - karakana.safety.rules
---

# Protocol Artifact Gate

The protocol artifact gate loads a trace, reads its selected protocol metadata and required artifacts, then checks for matching trace artifacts, outputs, or known stored evidence.

The gate blocks reproducibility claims when required artifacts are missing and records a reviewable JSON and Markdown result under `.karakana/protocol-checks/`.

Artifact aliases include generated requirements PRDs, requirements readiness outputs, traceability matrices, design/UX evidence, ADRs, schema contracts, tests/evals, and handoffs so agents can satisfy the gate through either protocol templates or higher-level Karakana requirements workflows.
