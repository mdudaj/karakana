# Harness Skill State Review

## Purpose

Review Karakana's existing harness before adding requirement-elicitation and brainstorming guidance. The aim is to fill workflow gaps without creating alternate PRD, issue, review, handoff, or safety systems.

## Existing Skill System

Karakana stores reusable workflow guidance in `skills/<name>/SKILL.md`. `karakana.skills.loader.SkillLoader` discovers and parses YAML-front-matter skills, while `karakana.skills.validator.SkillValidator` checks required metadata, risk levels, tool and approval lists, lifecycle metadata, activation hints, and standard sections.

The CLI already provides:

```bash
karakana skill list
karakana skill show <name>
karakana skill validate <name-or-path>
karakana skill validate-all
karakana skill index
```

Skills are guidance, not autonomous plugins. They do not gain execution authority from prose. Deterministic or authenticated behavior belongs in tightly scoped tools.

## Existing Skillpack System

Skillpacks are project profiles in `skillpacks/*.yml`. They select required and optional skills, project memory, model routes, high-risk and blocked paths, approval gates, tests, and conventions. Validation rejects missing required skills and warns for missing optional skills.

`msc-platform` already combines research-platform, research-writing, PR review, CI analysis, and handoff guidance. Its conventions establish official curriculum sources, deterministic extraction, separate assistive review, human selection, schema-backed evidence, and gated repository writes.

## Existing Requirements Workflow

The `karakana requirements` workflow already owns structured requirement artifacts:

1. `requirements prd` accepts one selected action, ingestion bundle, patch review, proposal, file, or note.
2. `requirements stories` generates actor/outcome stories with acceptance criteria, risks, skills, tests, and readiness/done checks.
3. `requirements issues` generates independently grabbable vertical-slice drafts with scope, non-goals, implementation notes, model routing, safety constraints, and tests/evals.
4. `requirements ready` checks the Definition of Ready.
5. `requirements publish` remains an explicit GitHub write path rather than a generation side effect.

The `msc-platform` requirements adapter already maps curriculum intake into schema/evidence-oriented slices. What is missing is a durable discipline for resolving ambiguous intent before `requirements prd`, not another PRD or issue generator.

## Existing Ingestion Workflow

`karakana ingest` loads explicitly selected files, traces, action bundles, patch reviews, dogfood runs, and requirement artifacts. It scans for secrets and unsafe targets, generates reviewable memory/skill/eval candidates, supports a review step, and keeps application dry-run by default. Ingestion is for distilling evidence after work; it is not an interactive requirement interview.

## Existing Dogfood Workflow

`karakana dogfood` can create a checklist, run a safe allowlist, analyze findings, generate a backlog and report, and convert that backlog into requirements. It prohibits implicit Codex execution, patch application, and GitHub writes. This provides a suitable artifact location and governance pattern for testing the new brainstorming skill, but it does not currently execute arbitrary skills.

## Existing Review / Patch / Handoff Workflow

Karakana already covers:

- PR review through `github-pr-review` and GitHub prompt tooling;
- patch capture and deterministic patch review through `karakana codex review-patch`;
- path/risk/test/secret gates through `karakana patch gate`;
- action and workspace handoffs through `karakana-handoff`, Codex handoff, and workspace handoff;
- issue triage prompt generation with explicit GitHub-write opt-in;
- CI failure diagnosis through `ci-failure-analysis`;
- dry-run branch, apply, stage, commit, and push policies.

These should be reused rather than wrapped in imported review, handoff, or triage skills.

## Capability Comparison

| External-style capability | Karakana state | Decision |
|---|---|---|
| `grill-me` | No focused interview skill; planning prompts exist | Adapt the targeted-question discipline inside `requirements-elicitation` |
| `grill-with-docs` | Memory, skillpack, plans, ADRs, and code can be loaded, but no dedicated challenge workflow | Add a Karakana-native skill |
| `to-prd` | `karakana requirements prd` already owns PRD artifacts | Already covered; add a pre-PRD handoff |
| `to-issues` / `prd-to-issues` | Stories, vertical issues, readiness, routing, and safety already implemented | Already covered |
| `review` | PR review, patch review, patch gate, and standards-vs-spec review exist | Already covered |
| `handoff` | Skill, action handoff, Codex handoff, and workspace handoff exist | Already covered |
| `triage` | GitHub issue-triage prompt and action extraction exist | Reference only; defer richer state-machine work |
| `tdd` | Tests/evals and implementation guidance exist, but no general TDD skill | Defer; useful but outside this milestone |
| `prototype` | Research-platform skill bounds prototype scope, but no throwaway-prototype workflow | Defer until a concrete repeated need exists |

## Strengths

- Markdown/YAML artifacts are reviewable and easy to validate.
- Skill metadata declares risk, allowed tools, approval needs, lifecycle, and activation.
- Skillpacks keep project context and safety rules separate.
- Requirements already preserve standards versus specification, safety constraints, routing, tests, and vertical slices.
- Generated runtime artifacts stay under `.karakana/` and are ignored by Git.
- Live model calls and GitHub writes require explicit opt-in.
- Research-platform guidance already separates deterministic curriculum facts from optional verbalized-sampling-inspired review.

## Gaps

- There was no explicit pre-PRD elicitation artifact or readiness discipline.
- No skill required questions to be answered from docs/code before asking the user.
- No reusable distribution-level brainstorming output schema existed.
- No focused workflow challenged plans against domain terms, ADRs, evidence artifacts, tests, and unsafe defaults.
- `skill validate` accepted a path but documentation and user expectations naturally use a skill name.

## Duplication Risks

- A new `to-prd` or `prd-to-issues` skill would compete with structured requirements artifacts and readiness checks.
- A new requirements CLI without a stable elicitation schema would add an under-specified artifact store and migration burden.
- Imported handoff/review/triage skills could bypass Karakana's safety gates and trace conventions.
- Copying external skill text would create lifecycle, metadata, tool, and licensing inconsistencies.
- Automatically activating brainstorming for every task would add cost and noise where the decision is already clear.

## Recommendations

1. Add `requirements-elicitation` as a pre-PRD workflow, not a generator replacement.
2. Add `grill-with-docs` for plan challenges grounded in Karakana memory, project docs, ADRs, code, tests, and evidence needs.
3. Add `brainstorm-verbalized-sampling` for ambiguous decisions and require subjective-weight disclaimers.
4. Keep the skills general-purpose and expose them as optional in every project skillpack. Make them required only in `msc-platform`, where the immediate milestone depends on them.
5. Pass reviewed elicitation markdown to `requirements prd --from-file`; defer `requirements elicit` until a stable schema and repeated artifact lifecycle justify code.
6. Keep existing review, handoff, triage, PRD, issue, dogfood, ingestion, and patch systems authoritative.
7. Add deterministic skill-content tests and eval fixtures; do not require live model calls.
