---
name: next-milestone-decision
description: Inspect current project evidence, compare plausible next milestones, select a grounded direction, and generate copy-ready execution instructions.
version: 0.1.0
risk_level: medium
category: productivity
scope: bundled
status: experimental
visibility: public
bucket: productivity
activation:
  keywords:
    - what next
    - next milestone
    - decide next work
    - milestone instructions
    - next project step
  required_files: []
  optional_tools:
    - git
    - grep
allowed_tools:
  - read_file
  - grep
  - code_search
requires_approval_for:
  - high_risk_milestone_execution
---
# next-milestone-decision

## Purpose

Decide what a project should do next from current evidence and produce a bounded, copy-ready task instruction. This skill is general-purpose and does not assume a framework, domain, repository layout, or planning format.

## When to use this skill

Use after a milestone, review, dogfood run, requirements cycle, patch gate, or material project-state change when the user asks what should happen next.

## When not to use this skill

Do not use when the next approved milestone is already explicit, when required context cannot be inspected, or to bypass unresolved planning and safety blockers. Do not execute the selected milestone as part of this skill.

## Quick Reference

- Inspect project state before proposing work.
- Prefer unresolved P0/P1 cleanup over new implementation.
- Generate 4-7 credible next milestones when direction is ambiguous.
- Use explicit multi-criteria scores and normalized decision weights, not invented probabilities.
- Report sensitivity to criterion removal and weight perturbation.
- Produce copy-ready instructions with verification and Definition of Done.

## Inputs

- current user-reported state or milestone completion report;
- project/workspace status and repository state;
- project instructions, memory, skillpack or governance constraints;
- latest dogfood, requirements, ingestion, milestone, patch, review, and gate artifacts;
- open findings, backlog priorities, readiness results, tests, and evals.

## State Sources

Use the most authoritative available sources. In Karakana-managed projects these commonly include workspaces, skillpacks, `ubongo/projects/`, `.karakana/dogfood/`, `.karakana/requirements/`, `.karakana/ingestion/`, `.karakana/milestones/`, patch/review/gate artifacts, traces, project docs, and current git status. Do not assume every project has every source. Record missing or conflicting evidence.

## Core concepts

- The next milestone is a decision over current evidence, not a continuation guessed from the last conversation.
- Blocker priority outranks novelty.
- A good milestone is bounded, evidence-linked, reversible where possible, and independently verifiable.
- Candidate generation and final selection are separate steps.
- Generated instructions are proposals for review, never implicit authorization to execute, push, or deploy.

## Standard workflow

Follow the `Process` below from state collection through candidate comparison and instruction generation.

## Process

1. Resolve the project, optional workspace, project governance/skillpack, and durable context.
2. Summarize completed work and current repository state.
3. Inspect recent dogfood, requirements/readiness, ingestion, milestone, patch/review/gate, test, and eval evidence when available.
4. Extract unresolved findings and classify P0/P1 blockers before considering implementation.
5. Identify whether requirements are current, project-specific, and ready.
6. Generate candidate milestone types appropriate to the evidence.
7. If several directions are plausible, use verbalized sampling to diversify candidate generation only.
8. Score every candidate against a published criterion matrix using one consistent ordinal scale.
9. Run leave-one-criterion-out and weight-perturbation sensitivity analysis.
10. Select the best robust evidence-adjusted milestone using project fit, cost, risk, reversibility, user experience, and integration value.
11. Generate direct execution instructions with explicit scope, non-goals, safety, verification, and Definition of Done.
12. Save or return the structured decision for human review. Do not execute it automatically.

## Candidate Milestone Generation

Consider cleanup, targeted dogfood rerun, requirements regeneration, skill adaptation, documentation hardening, implementation slice, schema/test hardening, patch review, release candidate, and deployment preparation. Add domain-specific milestones only when project evidence supports them.

Prefer cleanup before implementation when P0/P1 findings remain, dogfood after major planning changes, implementation after blockers and readiness gaps are resolved, schema/test hardening before data-producing behavior, and release hardening only after repeated green verification.

## Verbalized-Sampling Decision Step

Use `brainstorm-verbalized-sampling` when multiple next milestones remain credible. Generate 4-7 candidates and keep any model-verbalized probabilities explicitly uncalibrated. Select with a criterion matrix covering blocker priority, user alignment, evidence strength, readiness, risk control, reversibility, and cost efficiency. Normalized decision weights are score shares, not probabilities. Report sensitivity scenarios and do not present a fragile winner as robust.

## Instruction Generation

Generate an instruction that another agent can execute directly. Include the milestone title, current evidence, goal, required work, non-goals, files or artifacts to inspect when known, tests/evals, safety rules, verification plan, Definition of Done, and remaining risks. Preserve the project's native commands and governance.

## Pitfalls

- Recommending new implementation while unresolved P0/P1 findings remain.
- Treating the newest artifact as authoritative without checking its project and status.
- Producing a broad roadmap instead of one bounded milestone.
- Hiding missing evidence behind confident probabilities.
- Generating instructions that silently authorize writes, pushes, deployments, or safety changes.

## Verification

- Confirm evidence belongs to the selected project.
- Confirm criterion weights and normalized decision weights each sum to 1.0.
- Confirm the complete criterion matrix and sensitivity results are visible.
- Confirm strict blockers are visible and block when requested.
- Confirm instructions include safety, verification, and Definition of Done.
- Confirm no recommended work was executed by the decision step.

## Safety rules

- Do not recommend implementation when P0/P1 planning blockers remain.
- Do not skip dogfood/review when recent findings are unresolved.
- Do not recommend push/deploy by default.
- Do not generate instructions that weaken safety gates.
- Do not label normalized multi-criteria scores as probabilities.
- Do not ignore project skillpack constraints.
- Do not execute the generated instructions without a separate explicit request.

## Required checks

- Project context and governance resolve.
- Evidence and missing sources are listed.
- P0/P1 findings are classified before selection.
- Candidate milestones are materially distinct.
- Recommendation and rejected alternatives are explained.
- Instructions preserve project safety and non-goals.

## Output Shape

```markdown
# Next Milestone Decision

## Current State Summary

## Evidence Consulted

## Open Findings

## Candidate Milestones

| Candidate | Score | Decision Weight | Why It Might Be Right | Risks | Cost | Reversibility |
|---|---:|---:|---|---|---|---|

## Criterion Matrix

## Sensitivity Analysis

## Recommended Milestone

## Decision Rationale

## Rejected Alternatives

## Generated Instructions

## Verification Plan

## Definition of Done
```

## Output format

Return the `Next Milestone Decision` structure above. In Karakana, prefer the Markdown and JSON artifacts generated by `karakana milestone next`.

## Examples

- After a feature milestone, choose between fixing dogfood findings, regenerating requirements, hardening schemas, or beginning the next vertical slice.
- After planning changes, recommend a targeted dogfood rerun before implementation.
- For a research platform, choose a bounded evidence-producing slice while deferring unrelated workflow stages.
