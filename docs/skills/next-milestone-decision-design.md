# Next-Milestone Decision Design

## Purpose

Design a Karakana-native way to answer "what next?" from local project evidence and generate a copy-ready instruction without requiring an external ChatGPT planning pass.

## Current Harness Capabilities

Karakana already provides project memory, reusable skills, project skillpacks, workspaces, deterministic evals, requirements PRDs/stories/issues/readiness, dogfood findings/backlogs/reports, ingestion candidates, action/Codex handoffs, patch review/gates, trace storage, and safe local artifact conventions. Existing commands expose each subsystem separately but do not synthesize them into a project-sequencing decision.

## Available State Sources

- workspace project path, branch, dirty state, skillpack validity, memory availability, and artifact counts;
- project skillpack skills, conventions, high-risk paths, approval rules, and test commands;
- `ubongo/projects/<project>/` memory;
- dogfood status, findings, P0-P3 backlog, and next actions;
- requirements PRD, issues, and readiness failures;
- ingestion candidates and blocked/high-risk items;
- prior next-milestone decisions;
- current repository state and optional user-supplied note;
- patch, review, gate, test, eval, and trace artifacts for agent-led review.

## Missing Capability

No subsystem currently owns cross-store evidence collection, candidate next-milestone generation, blocker-aware selection, or instruction generation. Requirements owns specification artifacts; dogfood owns harness/project review; neither should own overall sequencing.

## Candidate Designs

| Option | Fit | Cost | Testability | Main Trade-off |
|---|---|---|---|---|
| A. Skill only | Medium | Low | Medium | Good judgment guidance but no repeatable state collection or durable run artifact |
| B. `karakana milestone next` | High | Medium | High | Deterministic and durable, but richer judgment still needs skill guidance |
| C. `karakana requirements next` | Medium | Medium | High | Misstates ownership because dogfood, patch, and ingestion evidence are peers |
| D. `karakana dogfood next` | Medium | Medium | High | Makes dogfood mandatory and cannot naturally represent requirements-only transitions |
| E. Skill plus milestone CLI | Very high | Medium | High | Adds a focused package and command but keeps judgment and mechanics separate |
| F. Keep external ChatGPT flow | Low | None | Low | Preserves repeated context transfer and loses local artifact integration |

## Verbalized-Sampling Brainstorm

Decision question: Should Karakana implement next-milestone decisioning as a skill-only workflow, a CLI command, a requirements subcommand, a dogfood subcommand, or a combined skill plus CLI artifact generator?

The following weights are subjective decision aids, not objective probabilities.

| Option | Probability | Why It Might Be Right | Risks | Cost | Reversibility |
|---|---:|---|---|---|---|
| A. Skill-only workflow | 0.12 | Minimal implementation and broadly reusable guidance | Continues manual evidence gathering and inconsistent artifacts | Low | High |
| B. New `milestone next` CLI | 0.22 | Clear ownership, deterministic collection, strong testability | Deterministic rules alone can appear more authoritative than their evidence | Medium | High |
| C. Requirements subcommand | 0.10 | Reuses structured PRD/readiness state | Excludes dogfood and review as equal sequencing inputs | Medium | Medium |
| D. Dogfood subcommand | 0.09 | Natural after a dogfood report | Cannot handle projects with requirements or notes but no recent dogfood | Medium | Medium |
| E. Combined skill plus CLI | 0.42 | Combines reusable judgment with deterministic state collection and durable instructions | Requires a new small artifact model and careful strict-mode semantics | Medium | High |
| F. Keep manual ChatGPT planning | 0.05 | No code or maintenance cost | Repeats context transfer and underuses Karakana evidence | None | High |

## Decision

Implement **E: combined `next-milestone-decision` skill plus `karakana milestone next` CLI**. The CLI is artifact-only and deterministic: it gathers local evidence, applies transparent multi-criteria scoring, runs sensitivity analysis, and writes Markdown/JSON. The skill supplies the general reasoning discipline and governs agent-led use of verbalized sampling to diversify candidate generation when ambiguity warrants it. Deterministic decision weights are normalized score shares, not simulated probabilities.

This design avoids live model calls and remains reversible. A user can inspect or discard the local artifact without changing project state.

## Proposed User Flow

```bash
karakana milestone next \
  --project msc-platform \
  --skillpack msc-platform \
  --workspace nimr \
  --from-note "Current user-reported state" \
  --write-instructions
```

Review `.karakana/milestones/<run-id>/next-milestone.md`, then explicitly hand the generated `instructions.md` to an implementation agent only when the decision is approved.

## Proposed Agent Flow

1. Load `next-milestone-decision` and relevant project skills.
2. Resolve project, skillpack, optional workspace, memory, and local artifact stores.
3. Classify unresolved P0/P1 findings before considering implementation.
4. Generate common and project-specific milestone candidates.
5. Use verbalized sampling when several candidates remain credible.
6. Select the evidence-adjusted direction.
7. Generate bounded instructions, verification, Definition of Done, safety notes, and rejected alternatives.
8. Stop after writing local artifacts.

## Artifact Model

Each run writes:

```text
.karakana/milestones/<run-id>/
├── next-milestone.md
├── next-milestone.json
└── instructions.md          # only with --write-instructions
```

The JSON sidecar preserves run metadata, evidence references and relevance scores, criterion definitions, candidate score matrices, sensitivity results, recommendation, instructions, verification, Definition of Done, warnings, and strict blockers.

## CLI Design

Use the standalone `milestone` namespace because next-step sequencing consumes requirements, dogfood, ingestion, workspace, memory, and repository state without belonging to any one source subsystem.

Supported options include `--workspace`, `--from-dogfood`, `--from-requirements`, `--from-note`, `--write-instructions`, `--format markdown|json`, `--no-brainstorm`, and `--strict`.

Strict mode writes the diagnostic artifact but exits non-zero when project context or skillpack validation fails, P0/P1 backlog remains, requirements are missing/generic, or the latest dogfood state is blocked/failed.

## Skill Design

The skill is general-purpose. It defines state-source discovery, blocker precedence, candidate generation, verbalized-sampling selection, and instruction generation. Karakana paths and the CLI are optional integrations, not assumptions about every project.

## Safety Rules

- Artifact generation never executes the recommendation.
- No live model or network access is required.
- P0/P1 planning blockers preclude implementation recommendations.
- Generated instructions preserve skillpack constraints and patch/review gates.
- Push and deployment remain explicit separate actions.
- Criterion weights and ordinal scores are explicit policy judgments.
- Normalized decision weights are score shares, not probabilities.
- Ranking robustness is reported through criterion-removal and weight-perturbation sensitivity analysis.
- Notes and stored output use Karakana redaction helpers.

## Implementation Plan

1. Add milestone schemas, evidence collection, deterministic candidate scoring, rendering, and storage.
2. Add the `milestone next` CLI and run trace integration.
3. Add `next-milestone-decision` with a deterministic eval.
4. Wire the skill into project skillpacks and user documentation.
5. Test artifact creation, required sections, strict blocking, note influence, no-brainstorm mode, and safety text.
6. Dogfood against the reported `msc-platform` Slice 1 state without implementing Slice 1.1.
