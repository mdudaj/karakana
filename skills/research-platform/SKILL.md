---
name: research-platform
description: Use this skill when working on software platforms that implement a research prototype, evaluation workflow, experiment design, data collection, or evidence generation for a dissertation or research project.
version: 0.1.0
risk_level: medium
allowed_tools:
  - read_file
  - grep
  - code_search
  - pytest
requires_approval_for:
  - evaluation_protocol_change
  - participant_data_change
  - model_provider_change
  - production_config_change
activation:
  keywords:
    - research platform
    - prototype
    - evaluation workflow
    - experiment
    - evidence generation
    - participant data
  required_files: []
  optional_tools:
    - grep
category: research
scope: bundled
status: experimental
visibility: public
bucket: research
---
# Research Platform

## Purpose

Guide work on research software platforms that implement prototypes, evaluation workflows, experiment support, data collection, and evidence generation.

## When to use this skill

Use for software that supports a dissertation or research project through implementation, evaluation, logging, export, reproducibility, or participant-facing workflows.

## When not to use this skill

Do not use this skill for dissertation chapter writing, literature review editing, citation cleanup, or submission formatting. Use `research-writing` for manuscript and methodology text.

## Core concepts

- Every feature should map to a research objective or evaluation activity.
- Prototype scope should stay bounded by dissertation evidence needs.
- Evaluation workflows must preserve reproducibility and traceability.
- Participant-sensitive data must not be stored in Git or exposed in artifacts.
- Result exports should make evidence reviewable without requiring production deployment.

## Standard workflow

1. Identify the research objective the platform work supports.
2. Identify the evaluation activity the work enables.
3. Identify the evidence the platform should generate.
4. Check whether the feature is necessary for dissertation evaluation or overbuilt.
5. Review privacy, ethics, data retention, and reproducibility risks.
6. Define tests or eval checks for the user flow, data capture, and exports.

## Safety rules

- Do not ingest `.env`, secrets, participant data, or generated evaluation data unless explicitly selected and redacted.
- Treat changes to evaluation protocol, data collection, model providers, prompts, exports, and participant workflows as high risk.
- Do not deploy, publish, or push research platform changes without explicit human action.
- Keep generated evidence reproducible and clearly linked to the evaluation activity.

## Required checks

- Which research objective does this support?
- Which evaluation activity does this enable?
- What evidence will this produce?
- Is this needed for the dissertation, or is it overengineering?
- What data or privacy risk is introduced?
- What test, eval, or manual review proves the workflow is ready?

## Output format

Return a concise assessment with research objective alignment, evaluation readiness, evidence output, risks, tests, and next actions.

## Examples

- Review whether a prototype feature supports a stated research objective and evaluation activity.
- Check that an evaluation export produces reviewable evidence without exposing participant-sensitive data.
- Split a platform backlog into dissertation-required work and non-essential product polish.

## Quick Reference

- Map features to objectives, activities, and evidence.
- Prefer evaluation-ready slices over broad product features.
- Preserve reproducibility and privacy.
- Use `research-writing` for manuscript text and `research-platform` for implementation/evaluation support.

## Pitfalls

- Building polished product features that do not support the dissertation evaluation.
- Treating prototype logs or exports as safe to commit.
- Changing evaluation protocol without review.
- Losing the link between platform behavior and research evidence.

## Verification

- Review a feature list against research objectives.
- Review evaluation setup for reproducibility and privacy.
- Check result export paths and logs for sensitive data risks.
- Check tests cover the prototype workflow and evidence generation path.
