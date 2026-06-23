---
id: karakana.protocol.rollout
type: WorkProtocol
title: Protocol Enforcement Rollout
status: active
owner: karakana
project: karakana
summary: Warn-first rollout policy for protocol artifact checks with explicit enforcement flags for handoff and patch workflows.
source: karakana/cli.py
tags: [karakana, protocol, rollout, enforcement]
updated: 2026-06-23
relationships:
  related_to:
    - karakana.protocol.system
    - karakana.protocol.artifact-gate
    - karakana.skillpack
---

# Protocol Enforcement Rollout

Karakana rolls protocol artifact checks out in warning mode by default.

`handoff refresh` and `patch gate` record protocol-check status and missing artifacts without blocking normal work unless `--require-protocol-pass` is explicitly supplied.

This keeps reproducibility pressure visible while avoiding sudden breakage as protocols mature.
