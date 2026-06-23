---
id: karakana.protocol.system
type: WorkProtocol
title: Karakana Work Protocol System
status: active
owner: karakana
project: karakana
summary: Deterministic protocol layer for classifying work, selecting roles, requiring artifacts, and recording reproducible trace evidence.
source: karakana/protocols/schemas.py
tags: [karakana, protocol, governance, reproducibility]
updated: 2026-06-23
relationships:
  related_to:
    - karakana.project
    - karakana.skillpack
    - karakana.safety.rules
    - karakana.protocol.artifact-gate
    - karakana.protocol.rollout
    - karakana.protocol.artifact-production
    - karakana.protocol.core-work-protocols
    - karakana.protocol.task-start
---

# Karakana Work Protocol System

Karakana work protocols classify tasks before execution and derive required artifacts from category, risk, and conditional impact flags.

The protocol system keeps work deterministic by defining roles, action steps, approval gates, verification expectations, and trace evidence requirements.
