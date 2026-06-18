# Matt Pocock Skills Review

## Purpose

Review Matt Pocock's public skills as reference patterns and decide which concepts belong in Karakana. This is not an installation or vendoring decision.

## Source Reviewed

Reviewed on 2026-06-18:

- [repository README](https://github.com/mattpocock/skills/blob/main/README.md)
- [repository license](https://github.com/mattpocock/skills/blob/main/LICENSE)
- [`grill-me`](https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md)
- [`grilling`](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md)
- [`grill-with-docs`](https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md)
- [`domain-modeling`](https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/SKILL.md)
- [`to-prd`](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-prd/SKILL.md)
- [`to-issues`](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-issues/SKILL.md)
- [`handoff`](https://github.com/mattpocock/skills/blob/main/skills/productivity/handoff/SKILL.md)
- [`triage`](https://github.com/mattpocock/skills/blob/main/skills/engineering/triage/SKILL.md)
- [`tdd`](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md)
- [`prototype`](https://github.com/mattpocock/skills/blob/main/skills/engineering/prototype/SKILL.md)
- [`diagnosing-bugs`](https://github.com/mattpocock/skills/blob/main/skills/engineering/diagnosing-bugs/SKILL.md)

The repository was read through GitHub rather than executed or installed. Skill names and behavior in this review come from the verified files above.

## Skills Identified

| Skill Name | Purpose | Useful Pattern | Karakana Equivalent | Adaptation Decision | Reason |
|---|---|---|---|---|---|
| `grill-me` | Start a plan/design interview | Small user-invoked wrapper over reusable grilling | No direct equivalent | `adapt` | Add the behavior inside native elicitation rather than a duplicate wrapper |
| `grilling` | Resolve a design tree through questions | One question at a time; inspect code instead of asking discoverable questions; recommend an answer | Planning and memory loading only | `adapt` | Directly addresses Karakana's pre-PRD gap |
| `grill-with-docs` | Combine grilling with domain modeling | Compose small disciplines rather than one large process | Partial grounding through memory/skillpacks | `adapt` | Karakana needs explicit ADR/doc/spec challenges |
| `domain-modeling` | Maintain canonical terms and selective ADRs | Challenge fuzzy terms; concrete scenarios; ADRs only for durable trade-offs | Ubongo, ADRs, project docs | `reference_only` | Do not impose external `CONTEXT.md` layout or inline mutation rules |
| `to-prd` | Synthesize conversation into a PRD | Explore current code and respect glossary/ADRs before synthesis | `karakana requirements prd` | `already_covered` | Existing schemas, artifacts, skillpacks, routing, and safety are richer and authoritative |
| `to-issues` | Create tracer-bullet vertical issues | Complete, demoable slices; review granularity and dependencies | `requirements stories/issues/ready` | `already_covered` | Karakana already generates vertical slices and readiness artifacts |
| `handoff` | Compact work for a new agent | Reference durable artifacts; redact sensitive data; suggest skills | `karakana-handoff`, action/Codex/workspace handoff | `already_covered` | Existing handoffs are project-aware and gated |
| `triage` | Move issues through triage roles | Explicit state vocabulary; reproduce bugs before grilling; preserve prior answers | GitHub issue-triage and actions | `reference_only` | Useful future enhancement, but importing its label state machine would conflict with local project policies |
| `tdd` | Run behavior-first red/green loops | One vertical behavior at a time; public-interface tests | Test/eval expectations and domain skills | `defer` | Valuable development skill, outside requirement-elicitation scope |
| `prototype` | Build disposable logic or UI experiments | A prototype answers one question and is deleted or absorbed | Research-platform prototype boundaries | `defer` | Needs project-specific artifact and cleanup policy before adoption |
| `diagnosing-bugs` | Build a feedback loop and test hypotheses | Reproduce/minimize before hypothesizing; ranked falsifiable hypotheses | `django-debugging`, CI analysis | `reference_only` | Useful concepts, but not needed for Milestone 22.6C |
| setup/router/misc skills | Configure or route the external collection | Explicit configuration and composability | Karakana skillpacks, activation, safety | `ignore` | Karakana already has its own metadata, routing, workspaces, and policy system |

## Requirement-Elicitation Patterns

The most useful pattern is the reusable grilling loop: walk dependent decisions one at a time, recommend an answer with each question, and investigate the repository instead of asking the user for discoverable facts. Karakana adapts this into `requirements-elicitation` and adds evidence, safety, research, and PRD-readiness fields.

The external flow assumes an interactive user session. Karakana also needs a reviewable artifact, explicit open questions, project memory, skillpack constraints, and a clean handoff into deterministic requirements generation.

## PRD Patterns

`to-prd` usefully separates elicitation from synthesis, asks the agent to explore the repository, and respects domain vocabulary and ADRs. Karakana should keep that separation. It should not import the external PRD template or automatic issue-tracker publication because Karakana's PRD schema already includes standards/spec separation, risks, safety constraints, suggested skills/skillpack, model routing, tests/evals, and rollout/review.

## Issue-Decomposition Patterns

`to-issues` reinforces Karakana's existing vertical-slice direction: each issue should deliver a narrow end-to-end behavior and be independently verifiable. Its user review of granularity and dependencies is worth retaining as an optional review step before publishing. No new issue generator is needed.

## Grill / Interview Patterns

Adapt:

- ask one question at a time;
- let later questions depend on resolved earlier decisions;
- recommend an answer and explain the trade-off;
- inspect docs, code, and tests before asking;
- challenge ambiguous domain terms;
- use concrete edge cases;
- reserve ADRs for hard-to-reverse, surprising, genuine trade-offs.

Rewrite for Karakana:

- ground in `KARAKANA.md`, Ubongo, skillpacks, project docs, schemas, and safety policy;
- record resolved and unresolved decisions in an artifact;
- do not mutate durable docs inline by default;
- use verbalized sampling when several credible answers remain.

## Review Patterns

The external repository emphasizes codebase exploration, behavioral tests, feedback loops, and specification alignment. Karakana already has a stronger review chain: `github-pr-review`, standards-vs-spec review, patch review, patch gate, CI analysis, and explicit approval policy. These concepts may inform future refinements but should not create another generic `review` skill.

## Handoff Patterns

The external handoff's strongest ideas are to avoid duplicating existing artifacts, reference paths/URLs, suggest applicable skills, and redact sensitive data. `karakana-handoff` already includes these concerns and additionally records repository state, verification, risk, and definition of done.

## What Karakana Should Adapt

- The one-question-at-a-time grilling loop.
- Repository investigation before user questions.
- Recommended answers and explicit trade-offs.
- Domain-language and ADR challenges.
- Vertical, independently verifiable issue review.
- Composition of small skills: elicitation calls grill-with-docs and verbalized sampling only when needed.

## What Karakana Should Not Adapt

- Automatic installation or execution of the external repository.
- Full external skill files, setup conventions, issue labels, or `CONTEXT.md` layout.
- Automatic PRD/issue publication.
- Duplicate `to-prd`, `to-issues`, handoff, review, or routing commands.
- Inline writes to glossary/ADR files without Karakana review and safety policy.
- TDD and prototype skills in this milestone without evidence of a repeated Karakana gap.

## License / Attribution Considerations

The source repository declares the MIT License. Copying substantial source text would require preserving the copyright and permission notice. This milestone instead credits the repository and rewrites general workflow concepts into Karakana-native skills, metadata, output schemas, project grounding, and safety rules. No external skill file is vendored or used as a runtime dependency.

## Decision

Adapt concepts, not files. Create `requirements-elicitation`, `grill-with-docs`, and `brainstorm-verbalized-sampling`; keep Karakana's requirements, review, handoff, triage, routing, and publishing systems authoritative. Defer TDD, prototype, and richer triage adaptation until separate evidence shows that existing Karakana skills cannot cover those workflows.
