---
id: karakana.protocol.task-start
type: WorkProtocol
title: Protocol Task Start
status: active
owner: karakana
project: karakana
summary: Task entry workflow that classifies work, resolves required artifacts, and presents template, approval, and verification guidance before execution.
source: karakana/protocols/start.py
tags: [karakana, protocol, task-start, reproducibility]
updated: 2026-06-23
relationships:
  related_to:
    - karakana.protocol.system
    - karakana.protocol.core-work-protocols
    - karakana.protocol.artifact-production
    - karakana.protocol.rollout
---

# Protocol Task Start

Protocol task start is the deterministic entry point for new work.

It classifies the task, selects the work protocol, records required artifacts, and presents template, approval, and verification guidance before implementation begins.

Operational usage is documented in `docs/protocols.md`.
