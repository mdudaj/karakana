# ADR 0006: Research must close with implementation choices

Date: 2026-10-01
Status: Accepted for this user-authorized protocol change; integration review pending.

## Problem and evidence

Karakana's lifecycle asks agents to research unresolved questions, but its research category has no dedicated protocol mapping. `ProtocolClassifier._protocol_for` can therefore choose a project default such as `python-code-change`. `assessment-review` asks for recommendations and a handoff but does not require choices for requirements, design or the artifacts that should carry them. The generic protocol check confirms only that a file exists. This allowed an FR-07 research sequence to leave a complete technical recommendation marked proposed, with no single closeout decision showing precisely what was settled, what approval remained and what the next implementation slice could do.

The user requires every research task to end with clear, unblocking requirements, design and related artifact choices. This is a workflow contract, not permission to invent evidence or mark an unapproved decision accepted.

## Requirements and acceptance criteria

| ID | Requirement | Acceptance evidence |
| --- | --- | --- |
| RDR-1 | Route an inferred or explicit `research` task to one dedicated research protocol across project profiles, unless a project explicitly overrides it. | Classifier and skillpack tests; no implementation or UX artifacts from a research-only task. |
| RDR-2 | A research closeout must state the bounded question, checked evidence, a requirements choice with observable acceptance, a design or method choice with rationale, and the disposition of related artifacts. | Structured closeout validation rejects missing, placeholder or incomplete fields. |
| RDR-3 | Separate a decision ready for implementation from a concrete approval request, an evidence blocker and a resolved no-change conclusion. No unknown material choice may be labelled ready. | Tests cover every outcome, conflicting blockers and required owner/next action. |
| RDR-4 | Ready research links readable requirements and design artifacts, names its authority evidence, and gives the exact implementation start and verification. Review and blocked outcomes name the owner and exact decision/evidence needed. | Validator checks artifact references and required structured fields; human review checks truth and suitability. |
| RDR-5 | Research updates its actual governing requirements/ADR/plan or explicitly selects a compact combined record when appropriate. Research does not automatically authorize code, PR publication, migration or deployment. | Protocol/template/process guidance and deterministic eval; diff review. |
| RDR-6 | Existing non-research protocols and legacy traces remain valid. | Focused and full regression, protocol/skillpack validation, deterministic evals. |

User story: as an implementation agent taking over a research result, I can identify the accepted requirement and design, the governing artifact paths, the exact next action and tests, or a named blocker without repeating the investigation or guessing at authority.

Definition of ready for this change: current protocol and classifier behavior inspected; the accepted user direction, this ADR, test matrix and rollback are recorded; task pre-implementation artifact check passes. Definition of done: RDR-1–6 pass in focused tests and deterministic evals, required full suite and protocol validation run, and the reviewable branch diff has no unexplained behavior change.

## Decision

Add `research-resolution`, a dedicated protocol for the existing `research` category. Its required `research_resolution` artifact is a human-readable Markdown record with a small YAML front matter for deterministic structure checks. It can link to a compact combined requirements/design record for a small task; consequential design and UX/data changes still update their proper ADR, UX or schema artifacts. The closeout has one of four states:

- `ready_for_implementation`: material requirements/design choices and required approvals are recorded; referenced artifacts exist; no blocker remains. This permits the next authorized implementation task to run its own pre-implementation gate. It does not itself grant implementation or external-action authority.
- `resolved_no_change`: evidence supports retaining current behavior; requirements/design choices and artifact disposition are still explicit.
- `decision_required`: a concrete recommended choice is complete but named approval or material product choice remains. State the owner, exact question and next action; do not mark implementation ready.
- `evidence_blocked`: the answer cannot responsibly be chosen from current evidence. State the missing evidence, owner, bounded acquisition step and independent work that can continue.

The closeout front matter requires `question`, `evidence`, `requirements`, `design`, `artifact_choices`, `status`, `authority`, `pending_decisions` and `next_action`. Requirements include a decision, observable acceptance and artifact path; design includes a choice, rationale and artifact path. Artifact choices name kind, disposition, path or non-applicability rationale. For `ready_for_implementation`, referenced requirement/design artifacts must be readable files, authority must be stated and pending decisions must be empty. For blocked states, a pending decision has owner, question and exact next action. A file with only headings, placeholders or a vague “review later” cannot pass.

The new check verifies **structure and local reference existence**, not the truth of evidence, the adequacy of a choice or the validity of claimed approval. It reports the declared outcome and `implementation_ready` separately from the protocol pass, so completed blocked research cannot be mistaken for a ready implementation. A human must review those claims. Existing artifact checks remain presence checks. Do not create a generic semantic judge or autonomous stage promotion.

Fix the narrow classifier defect where `ui` inside `requirements` incorrectly turns a research task into a UX change. Keep project-specific explicit protocol mappings authoritative; use `research-resolution` as the category fallback before a skillpack's default. Add explicit research mappings to active skillpacks, document the routing and update the shared process guidance and artifact-gate skill.

## Alternatives and consequences

Prose-only instruction would repeat the current failure: a filled but vague note could pass a presence gate. Requiring a separate PRD and ADR for every research task would add unnecessary artifacts to small assessments. A compact structured closeout with actual artifact choices keeps the gate proportional while preventing an empty recommendation from being called ready. The YAML front matter is intentionally small; Markdown carries the rationale and can be reviewed in a PR.

Research may end blocked when facts or authority are unavailable; that is an honest outcome, not a compromised or implicit implementation plan. The unresolved item must be actionable and attributed. A later task rechecks evidence currency and approval before reusing the closeout. Existing research notes without the new contract remain historical evidence; new research tasks use the new protocol.

## Implementation and verification instructions

Inspect `karakana/protocols/{classifier,checks,schemas,artifacts,lifecycle}.py`, `protocols/assessment-review.yml`, `skillpacks/*.yml`, `docs/{engineering-process,protocols,cost-aware-continuation}.md`, and focused tests before editing. Add the protocol, template and validator, then route research to it. Update shared guidance, artifact-gate skill and OKF protocol description. Verify valid ready/no-change/decision-required/evidence-blocked records, empty placeholders, missing paths, missing authority, conflicting blockers and classifier routing. Run focused protocol tests, full `pytest`, protocol/skillpack/skill validation and deterministic evals. Review the diff and report any skipped checks. Rollback is a reviewed revert of this branch; append-only traces and handoffs remain intact.

Traceability: RDR-1 → classifier, skillpacks and `tests/test_protocols.py`; RDR-2–4 → template, validator, checker and `tests/test_research_resolution.py`; RDR-5 → lifecycle/process/skill/OKF plus eval; RDR-6 → existing protocol tests and full gates.
