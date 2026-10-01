---
status: ready_for_implementation
question: "How should Karakana make research produce unblocking requirements, design and artifact choices?"
evidence:
  - source: "karakana/protocols/classifier.py and skillpacks/*.yml"
    finding: "Research was a recognized category but lacked a dedicated skillpack mapping and could fall back to an implementation protocol."
  - source: "protocols/assessment-review.yml and karakana/protocols/checks.py"
    finding: "Assessment could end with recommendations and generic checks only verified file presence."
  - source: "FR-07 design-acceptance handoff and docs/engineering-process.md"
    finding: "A complete proposed design needed a separate explicit acceptance step; the prior process did not record all readiness choices in one closeout."
requirements:
  - decision: "Every bounded research task records a requirement with observable acceptance, design or method choice, artifact disposition and exact readiness outcome."
    acceptance: "A research task cannot pass its closeout check with empty choices, placeholders, missing ready-state artifact files or unnamed blockers."
    artifact: "docs/adr/0006-research-resolution-readiness.md"
design:
  - choice: "Use a dedicated research-resolution protocol and structured Markdown closeout, with a narrow structural validator and human semantic review."
    rationale: "It routes research correctly and makes readiness checkable without falsely treating artifact presence as approval or requiring a separate PRD and ADR for every small study."
    artifact: "docs/adr/0006-research-resolution-readiness.md"
artifact_choices:
  - kind: requirements
    disposition: updated
    path: "docs/adr/0006-research-resolution-readiness.md"
    rationale: "The compact decision record includes RDR-1 through RDR-6, acceptance, story, readiness and traceability."
  - kind: design
    disposition: updated
    path: "docs/adr/0006-research-resolution-readiness.md"
    rationale: "The same record states the selected protocol/validator design, alternatives and rollback."
  - kind: plan
    disposition: updated
    path: "docs/engineering-process.md"
    rationale: "The lifecycle names the closeout states and handoff behavior."
  - kind: test
    disposition: updated
    path: "tests/test_research_resolution.py"
    rationale: "Routing, readiness, blockers and malformed records have regression coverage."
authority:
  state: approved
  evidence: "The user explicitly directed a protocol update on 1 October 2026; publication and merge remain separate actions."
pending_decisions: []
next_action: "Complete the final regression and review the task-branch diff, then prepare a reviewable PR when publication is authorized."
---

# Research Resolution

The selected contract separates *research completion* from *implementation readiness*. A blocked research task can be complete as an investigation while its implementation remains held by an exact decision or evidence gap. A ready result must point to the requirement and design artifacts and record applicable authority. The validator checks structure and local paths; a reviewer still checks whether the evidence actually supports the choices and whether the claimed approval is real.

The alternative of prose-only guidance would preserve the failure mode in which a vague recommendation passes a file-presence gate. The alternative of requiring a full PRD and ADR for every study would burden small research tasks without adding useful decisions. This combined record is appropriate for the present harness workflow change; future product research may link distinct requirements, UX, schema and ADR artifacts.
