# KDX-06 source-specific requirements readiness

Status: implementation authorized by the user's 2026-10-01 instruction to execute the next proposed development task. This is one reviewable branch; remote publication, merge, deployment and live model calls require their existing separate authority.

## Requirements note and evidence

Requirement `20261001-154449-req-565169` was generated from a concrete Karakana delivery record but reported `ready: true`. Its PRD has fallback text for the problem and goal, generic requirements about generating PRDs, generic acceptance criteria, and generic story prose. `karakana/requirements/prd.py` supplies those fallbacks when it cannot read labeled fields; `karakana/requirements/readiness.py` currently checks only for nonempty values. The source-specific delivery record remains authoritative; the generated PRD was rejected for task planning. KDX-06 is the P2 backlog item for this false readiness result.

## Product requirements and user story

As a maintainer using `karakana requirements ready`, I need the readiness result to distinguish a concrete task specification from generator fallback text, so I do not hand a generic PRD to an implementation agent as if it were project-specific. A generator fallback is draft material for review, not evidence that the original task is specified. Existing structured `Specification / PRD Seed` inputs with specific Problem, Goal, Functional requirements and Acceptance criteria remain eligible for readiness when other checks pass. Separately generated stories and issue drafts still require human review.

The technical CLI presentation keeps its existing `Status`, `Ready`, `Failed Checks`, and `Recommended Next Actions` layout. New failed-check labels must name the missing source behavior directly; the action must tell the operator to add task-specific labeled fields and regenerate. There is no new graphical interface or styling. This follows the repository's requirements and `ux-writing` guidance for direct, actionable diagnostic copy.

## Acceptance criteria and traceability

| ID | Observable result | Source and check |
| --- | --- | --- |
| R1 | The stored Karakana PRD above becomes `not_ready` with `ready: false`; failed checks identify its generic problem, goal, functional requirements and acceptance criteria. | Saved `prd.json`; `check_readiness` regression and a read-only legacy-artifact check. |
| R2 | A generated PRD from an explicit, concrete seed passes those specificity checks and retains its source behavior in the report. | `karakana/requirements/prd.py`; positive regression. |
| R3 | Generic free-text notes remain generatable for review, but no longer receive a false `ready` result. Existing `requirements ready` CLI formatting and dry-run publishing behavior remain intact. | CLI regression and focused requirements suite. |
| R4 | Clear failed-check labels and a recovery action appear in `readiness.md` and CLI JSON without treating structural checks as semantic approval. | `karakana/requirements/readiness.py`, `summary.py`; copy review and assertions. |
| R5 | Full pytest, deterministic evals, skill and memory validation, a safe requirements command exercise, diff review and protocol completion pass before delivery. | Actual command receipts in this record and task trace. |

## Design, artifact readiness and implementation plan

Use exact generator fallback constants shared by PRD creation and readiness checks. Require at least one nonfallback functional requirement and acceptance criterion, as well as nonfallback problem and goal text. This deterministic rule catches both newly generated and legacy artifacts without guessing semantic similarity or changing the artifact schema. A specific but incorrect requirement can still pass; human review remains the semantic gate. A warning-only result would retain `ready: true`, so these obvious fallback cases must fail readiness. Keep the existing `not_ready` status and Markdown/JSON report shapes.

Inspect `KARAKANA.md`, the loaded handoff, project backlog, `docs/engineering-process.md`, `skills/engineering-requirements/SKILL.md`, `skills/ux-writing/SKILL.md`, the saved requirement, the PRD generator, readiness checker, renderer and focused tests. Add failing positive/negative tests; centralize the fallback text; add specificity checks and an actionable next step; then run focused and full gates. Update the project backlog with local verification and refresh the handoff. Revert the reviewable task commit to roll back. A new ADR, migration, UX mockup, or deployment artifact is not applicable: the change is a deterministic CLI readiness decision with unchanged storage and layout.

## Definition of done and verification summary

Complete when R1–R5 have actual evidence, the branch diff has no blocking finding, the protocol completion gate passes, and a task handoff names the remaining backlog and next action. Implemented, verified, merged, deployed and accepted are recorded separately.

The generator now records whether Problem, Goal, Functional requirements and Acceptance criteria came from labeled source fields. Readiness rejects fallback sections in new artifacts and recognizes the same fallback text in legacy artifacts without provenance metadata. The result uses existing `not_ready`/`Ready: False` presentation, four specific failed-check labels, and a recovery instruction to add a task-specific PRD seed. It leaves other readiness and dry-run publishing behavior intact.

The new negative regressions failed against the old behavior. The focused requirements suite passed **18/18** and the final edited code passed its focused PRD/readiness/CLI tests **11/11**; `karakana eval run --suite requirements` passed **10/10**. The final `pytest -q` gate passed **718/718**, full `karakana eval run` passed **173/173** with zero warnings (report `20261001-173227-eval-951535`), `karakana skill validate-all` passed, and `karakana memory validate --project karakana` reported the project memory complete. A read-only evaluation of saved PRD `20261001-154449-req-565169` found all four source-specificity failures; rerunning `karakana requirements ready <id> --json` persisted `status: not_ready`, `ready: false` and the recovery actions. Protocol completion is recorded in the task trace after handoff refresh.

The changed source paths are `karakana/requirements/prd.py` and `karakana/requirements/readiness.py`, with focused PRD, readiness and CLI tests. No storage schema, deployment or external API changes are required. The rule detects known generated fallback content and explicit source-field provenance; it does not prove semantic equivalence between a concrete PRD and the source. Human review remains necessary. Generic story and issue drafting for non-MSc projects is a separate KDX-08 follow-up, now tracked in the project backlog.

This branch is implemented and verified locally, awaiting PR review. Remaining open items are KDX-08 P2 and KDX-04/KDX-07 P3. The recommended next development task after integration is KDX-08; inspect the current renderer and story/issue generator, then use concrete and generic source examples to define acceptance before editing. GPT-6 Sol with high reasoning is appropriate for this cross-project generator behavior; a fresh conversation would help keep the next slice bounded.
