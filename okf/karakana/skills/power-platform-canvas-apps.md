---
id: karakana.skill.power-platform-canvas-apps
type: Skill
title: Power Platform Canvas Apps
status: active
owner: karakana
project: karakana
summary: Guides Power Apps canvas app architecture, Microsoft Lists/SharePoint data design, Power Fx validation, and form UX before TACATDP implementation.
source: skills/power-platform-canvas-apps/SKILL.md
tags: [skill, power-platform, canvas-apps, microsoft-lists, sharepoint, xlsform, ux, tacatdp]
updated: 2026-07-02
relationships:
  related_to:
    - karakana.skillpack
    - karakana.skill.delivery-artifact-gate
    - karakana.okf.profile
---

# Power Platform Canvas Apps

This skill is the durable pre-implementation context for TACATDP-style Power Apps canvas app work. It records the requirement to design Microsoft Lists/SharePoint data access, Power Fx validation, skip logic, and screen-level form UX before app implementation starts.

Key UX constraints include one field per row by default, visible labels, helper/error text near each input, consistent spacing, sectioned wizard navigation, accessible focus order, and explicit validation summaries.

Canvas source-control work must use the active Microsoft Source Code `*.pa.yaml` schema. Custom canvas component instances use `Control: CanvasComponent` with `ComponentName`; retired or preview-style `Control: Component` syntax is not import-safe.
