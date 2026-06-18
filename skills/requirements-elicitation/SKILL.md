---
name: requirements-elicitation
description: Elicit requirements for any project by grounding ambiguous goals in available evidence, asking targeted questions, comparing plausible options, and producing specification-ready context.
version: 0.1.0
risk_level: medium
category: productivity
scope: bundled
status: experimental
visibility: public
bucket: productivity
activation:
  keywords:
    - elicit requirements
    - clarify requirements
    - prepare specification
    - ambiguous request
    - grill the plan
  required_files: []
  optional_tools:
    - grep
    - git
allowed_tools:
  - read_file
  - grep
  - code_search
requires_approval_for:
  - high_risk_requirement_decision
---
# requirements-elicitation

## Purpose

Turn an ambiguous goal into grounded, specification-ready context for any software, research, infrastructure, documentation, operations, or product project. The skill is independent of framework, repository layout, issue tracker, and final specification format.

## When to use this skill

Use before writing a PRD, specification, proposal, plan, backlog, issue set, research protocol, or implementation brief when scope, terminology, stakeholders, evidence, constraints, acceptance behavior, or delivery direction is unresolved. Use it when premature decomposition would encode guesses.

## When not to use this skill

Do not use when an approved specification already resolves the important decisions. Do not generate implementation tasks from this skill; hand the resolved result to the project's existing planning or requirements workflow.

## Quick Reference

- Read project docs and code before asking questions.
- Ask only questions that local evidence cannot answer.
- Ask one targeted question at a time when user input is required.
- Use `brainstorm-verbalized-sampling` when several valid approaches remain.
- Resolve scope and decisions before specification or task generation.

## Inputs

- user goal or note;
- the user's goal, stakeholders, and intended outcome;
- any project contract, instructions, durable memory, or governance profile;
- product, research, operational, or policy plans; decision records; glossary/domain docs; schemas; and existing implementation when relevant;
- prior decisions, requirements artifacts, issue discussions, and review findings.

## Core concepts

- Elicitation resolves intent; a downstream specification structures the resolved intent.
- Local evidence should answer discoverable questions before the user is interrupted.
- One-question-at-a-time grilling reduces confusion and lets later questions depend on earlier answers.
- Domain terms must match project language or be explicitly corrected.
- A specification seed must separate known decisions, assumptions, open questions, and out-of-scope work.

## Standard workflow

Follow the `Process` below to move from evidence grounding to targeted questions, resolved decisions, and a reviewed specification handoff.

## Process

1. Discover and read the available project instructions, plans, decision records, domain language, prior requirements, implementation, and tests. Do not assume a particular file layout or that the project is software.
2. Restate the user goal and identify stakeholders, desired outcomes, project value, and expected evidence or deliverables.
3. Separate facts, constraints, assumptions, contradictions, and unknowns.
4. Answer codebase- or document-discoverable questions directly. Record the source.
5. Prioritize ambiguities that change scope, architecture, safety, acceptance criteria, or issue decomposition.
6. Ask targeted questions one at a time when user intent is genuinely required. Include a recommended answer and its trade-off.
7. Grill the emerging plan against available evidence, decision records, domain language, existing behavior, verification mechanisms, and safety rules.
8. When multiple credible paths remain, run the `brainstorm-verbalized-sampling` decision step and record its weights as subjective decision aids.
9. Resolve the recommended scope, out-of-scope boundaries, acceptance behavior, evidence artifacts, tests, and remaining open questions.
10. Produce the elicitation artifact and mark it ready only when no unresolved question would materially change the downstream specification or task breakdown.
11. Pass the artifact to the project's existing PRD, specification, proposal, planning, or issue workflow. Do not recreate downstream tooling inside this skill.

## Grill Questions

- Who experiences the problem, and what observable outcome changes?
- Which term is ambiguous or conflicts with the project's domain language?
- What must be true for this work to be considered complete?
- Which existing behavior, module, workflow, or evidence artifact does this extend?
- What is explicitly out of scope?
- Which decision is expensive or hard to reverse?
- Which assumption lacks evidence?
- What can fail, and what is the safe default?
- Which tests, evals, or review artifacts prove the requirement?
- Is the proposed slice independently demoable or verifiable?

## Document Grounding

Use whatever authoritative evidence the project provides: user instructions, contracts, policies, durable memory, governance profiles, glossary/context docs, decision records, research/product/operational plans, schemas, tests, code, tickets, or prior artifacts. Cite paths or references in `Existing Context`. If evidence is absent, state that and elicit from the user rather than inventing context. If sources conflict, surface the conflict and resolve which source should change. Suggest updates; do not silently rewrite durable decisions.

## Verbalized-Sampling Decision Step

When two or more valid approaches survive document grounding, invoke `brainstorm-verbalized-sampling`. Generate 4-7 plausible options with uncalibrated verbalized probabilities, uncertainty flags, evidence needs, cost, risk, reversibility, project-doc alignment, and user-intent alignment. Select through an explicit criterion matrix and sensitivity analysis. Record the selected decision and why alternatives were rejected; normalized decision weights are score shares, not probabilities.

## Pitfalls

- Asking the user questions the repository can answer.
- Asking a batch of interdependent questions at once.
- Jumping from a vague request directly to issue drafts.
- Treating current code as authoritative when an accepted ADR says otherwise.
- Expanding the specification seed into implementation details that will quickly go stale.

## Verification

- Check every material ambiguity is resolved or explicitly open.
- Check domain terms and decisions against cited docs.
- Check scope, non-goals, evidence, tests, and safety constraints are present.
- Check the specification readiness answer matches the remaining open questions.

## Safety rules

- Do not invent user intent.
- Do not weaken approval, secret, deployment, data, privacy, or production gates during elicitation.
- High-risk or irreversible decisions require evidence and human review.
- Keep live model calls and GitHub writes explicit opt-in.
- Preserve dry-run defaults and do not begin implementation from an elicitation artifact.

## Required checks

- Project docs were read before questions were asked.
- Discoverable questions were answered from local evidence.
- Multiple plausible approaches used the verbalized-sampling step.
- Decisions and open questions are distinguishable.
- The result is suitable input to the project's existing specification or planning workflow.

## Output

```markdown
# Requirements Elicitation Result

## User Goal

## Existing Context

## Ambiguities

## Questions Asked

## Decisions Made

## Open Questions

## Recommended Scope

## Out of Scope

## Ready for Specification / PRD?

## Specification / PRD Seed
```

## Hand-off to Specification

Hand the reviewed artifact to whatever the project already uses: a PRD template, RFC, design document, research protocol, proposal, issue tracker, roadmap, or implementation-plan generator. Preserve the separation between elicitation and decomposition.

### Karakana integration

In a Karakana-managed project, save the reviewed result as markdown and use the existing command:

```bash
karakana requirements prd \
  --from-file <elicitation-artifact.md> \
  --project <project> \
  --skillpack <skillpack>
```

Continue with `requirements stories`, `requirements issues`, and `requirements ready` only after the PRD artifact is reviewed. This is an optional Karakana adapter, not a requirement of the skill. A dedicated `requirements elicit` command remains deferred until a stable elicitation schema and artifact store are justified.

## Output format

Return the `Requirements Elicitation Result` structure above. Keep the specification seed concise, evidence-linked, and free of unresolved implementation guesses.

## Examples

- Clarify whether a dashboard change is status-only, action-oriented, or a complete workflow surface before generating a PRD.
- Resolve domain language and an ADR conflict before decomposing a data workflow into vertical slices.
