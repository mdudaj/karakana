---
# Choose ready_for_implementation, resolved_no_change, decision_required, or evidence_blocked.
status: decision_required
question: "TODO: bounded question and decision this research must resolve"
evidence:
  - source: "TODO: repository path, primary source or observed test"
    finding: "TODO: precise observation and its limit"
requirements:
  - decision: "TODO: selected behavior or constraint"
    acceptance: "TODO: observable pass/fail outcome"
    artifact: "TODO: path to updated or reused requirements; this record if compact"
design:
  - choice: "TODO: selected design or method"
    rationale: "TODO: why it fits current architecture and rejected alternative"
    artifact: "TODO: path to updated or reused ADR/design; this record if compact"
artifact_choices:
  - kind: requirements
    disposition: planned
    path: "TODO: requirements artifact path"
    rationale: "TODO: update, reuse or compact record rationale"
  - kind: design
    disposition: planned
    path: "TODO: design artifact path"
    rationale: "TODO: ADR, design note or compact record rationale"
# Add plan, UX, schema, example, test or eval choices when relevant.
# For a non-applicable optional artifact use disposition: not_applicable and explain why.
authority:
  state: pending
  evidence: "TODO: existing approval, no-approval rationale or specific missing authority"
pending_decisions:
  - owner: "TODO: decision or evidence owner"
    question: "TODO: exact yes/no decision or missing fact"
    next_action: "TODO: concrete action to obtain it"
next_action: "TODO: exact next bounded task"
---

# Research Resolution

Explain the evidence, competing options, trade-offs, requirement and design choices, artifact changes, risk and verification. Replace every TODO. A structural protocol pass does not certify the research or grant approval. If a material fact or authority remains open, keep the status blocked and name the owner and next action.
