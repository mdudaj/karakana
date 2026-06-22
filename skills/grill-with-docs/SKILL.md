---
name: grill-with-docs
description: Challenge any project plan against available documents, decisions, domain language, implementation evidence, verification needs, and safety constraints.
version: 0.1.0
risk_level: medium
category: productivity
scope: bundled
status: experimental
visibility: public
bucket: productivity
activation:
  keywords:
    - grill with docs
    - challenge plan
    - review specification
    - stress test plan
    - ADR conflict
  required_files: []
  optional_tools:
    - grep
    - git
allowed_tools:
  - read_file
  - grep
  - code_search
  - run_tests
requires_approval_for:
  - durable_architecture_decision_change
---
# grill-with-docs

## Purpose

Stress-test a plan for any kind of project against its available contracts, policies, domain language, decision records, implementation evidence, verification expectations, and safety rules. Produce resolved decisions and documentation changes before the plan becomes a specification or task breakdown.

## When to use this skill

Use for ambiguous or consequential plans, specification review, architecture or process choices, scope challenges, and requirements preparation where project evidence should constrain the answer. The project may be software, research, infrastructure, documentation, operations, or product work.

## When not to use this skill

Do not use for a simple factual lookup, a concrete code review with an existing diff, or as permission to edit ADRs without review. Use `github-pr-review` for a PR and `requirements-elicitation` for the complete pre-PRD workflow.

## Quick Reference

- Read the available authoritative evidence before challenging the user.
- Extract canonical domain terms and constraints.
- Ask one unresolved question at a time and recommend an answer.
- Detect conflicts, scope creep, missing evidence, missing tests, and unsafe defaults.
- Suggest doc updates when the resolved plan changes durable knowledge.

## Core concepts

- Project docs constrain plans, but contradictions with code or newer accepted decisions must be surfaced rather than hidden.
- Shared domain language reduces ambiguity in specifications, tasks, implementation, and verification.
- Questions answerable from the repository are investigation tasks, not user questions.
- ADRs are appropriate only for consequential, hard-to-reverse trade-offs that would otherwise surprise future maintainers.
- A grilled plan is ready when material decision branches are resolved, not when every implementation detail is prescribed.

## Standard workflow

1. Restate the plan and its intended outcome.
2. Discover and read available project instructions, contracts, policies, governance profiles, durable memory, glossary/context docs, decision records, plans, schemas, implementation artifacts, and verification evidence. Do not assume a fixed repository layout.
3. Record every consulted document and extract canonical domain terms, constraints, accepted decisions, safety gates, and evidence obligations.
4. Compare the plan with those sources. Flag ambiguous terms, contradictions, obsolete assumptions, overbroad scope, missing artifacts, missing tests, and unsafe defaults.
5. Resolve repository-discoverable challenges by inspecting code and tests.
6. Ask remaining user-intent questions one at a time. For each, provide a recommended answer, evidence, and trade-off.
7. When several answers remain credible, use `brainstorm-verbalized-sampling` rather than choosing the most familiar answer.
8. Record resolved decisions, unresolved questions, scope corrections, and required doc updates.
9. Mark the plan ready only when unresolved questions cannot materially alter scope, safety, acceptance behavior, deliverables, or task boundaries.

## Challenge Checklist

- Does a plan term conflict with the glossary, ADRs, schema names, or code?
- Does the plan contradict an accepted ADR or silently reverse a decision?
- Is scope broader than the stated user or project outcome requires?
- Are source, evidence, provenance, review, or handoff artifacts missing?
- Are observable acceptance criteria, focused tests, evals, or manual verification missing?
- Does a write, deployment, external call, or automation default bypass a gate?
- Is an assistive model being treated as authoritative?
- Is a horizontal implementation layer being mistaken for a vertical slice?
- Does an existing workflow or command already own this behavior?

## Document Grounding

Prefer authoritative sources in this order unless the project says otherwise: explicit user decision, accepted contract/policy/decision record, durable project memory and domain docs, current specification, observable behavior and verification evidence, then informal notes. When a source category does not exist, skip it rather than inventing a substitute. Record conflicts instead of silently picking a source. Recommend precise updates for documents made stale by a resolved decision.

## Pitfalls

- Treating grilling as adversarial rather than decision-oriented.
- Re-asking questions already answered by docs or code.
- Updating a glossary with implementation detail.
- Proposing an ADR for an easy-to-reverse or unsurprising choice.
- Declaring readiness while acceptance or safety behavior remains ambiguous.

## Verification

- Confirm all documents listed under `Documents Consulted` were actually read.
- Confirm each challenge is tied to evidence or an explicit unknown.
- Confirm doc conflicts and scope corrections have an owner.
- Confirm readiness is false when a material question remains.

## Safety rules

- Do not alter accepted ADRs, contracts, or project memory without review.
- Do not print secrets or inspect secret-bearing files.
- Preserve explicit approval for high-risk, destructive, production, authentication, permission, data, and external-write decisions.
- Do not let model-generated options override evidence or human gates.
- Do not begin implementation as part of the grill.

## Required checks

- Relevant docs, ADRs, domain terms, code, and tests were considered.
- Conflicts, overbroad scope, missing evidence, missing verification, and unsafe defaults were checked.
- Resolved and unresolved decisions are separate.
- Required doc updates are explicit.
- Specification readiness is evidence-based.

## Output format

```markdown
# Grill-with-Docs Result

## Plan Under Review

## Documents Consulted

## Domain Terms

## Challenges

## Resolved Decisions

## Unresolved Questions

## Scope Corrections

## Required Doc Updates

## Ready for Specification / PRD?
```

## Examples

- Challenge a proposed workflow UI against an ADR that limits the current slice to artifact inspection.
- Resolve whether an overloaded project term refers to an actor, artifact, state, or process before writing acceptance criteria.
