# R1-A5 artifact review miss: protocol clarity and source challenge

Status: bounded Karakana improvement proposal, 13 October 2026. The ent-meal R1-A5 source contract correction is a separate docs-only branch. This proposal does not change protocol outcome semantics or authorize source migration, permissions, remote publishing or deployment.

## Observed result and cause

The earlier R1-A5 research trace `20261013-101023-ef9517` passed completion check `20261013-102736-protocol-check-eb8593`. Its JSON records `research_outcome: decision_required` and `implementation_ready: false`. The short CLI output said only `Protocol check: passed` and `evidence scope: artifact presence only`; it did not show the recorded outcome or readiness. The Markdown check report did. Karakana's [research protocol](../../protocols/research-resolution.yml), [validator](../../karakana/protocols/research_resolution.py) and [ADR 0006](../adr/0006-research-resolution-readiness.md) deliberately check structure and local references, not whether a helper actually performs the claimed validation. The artifact authoring/review missed two source counterexamples: a stale calculated value can retain its review status, and `describe(report)` does not read retained bytes. The protocol operated as designed; the semantic review and CLI communication were insufficient.

## Requirements and acceptance

| ID | Requirement | Acceptance |
| --- | --- | --- |
| AR-1 | The short `protocol check` output must show the actual evidence scope and, for research checks, the recorded research outcome and implementation-ready boolean. | A structurally passing `decision_required` closeout prints `Implementation ready: false`; JSON and Markdown retain their existing fields; non-research output stays clear. |
| AR-2 | Before an artifact is described as source-ready, its reviewer must challenge consequential claims against the producer, consumer, negative lifecycle/failure paths and existing tests. A helper's name is not proof that it checks storage bytes, currentness or authority. | Research protocol, template, delivery-artifact-gate skill and engineering process ask for a compact claim/counterexample table or justified non-applicability; the reviewed artifact records how each finding was resolved. |
| AR-3 | The workflow must distinguish a structural pass from substantive review, approval and implementation readiness. | No checker changes its pass/fail semantics, invents a semantic certification or auto-promotes a blocked outcome. The guidance and CLI say the limit plainly. |
| AR-4 | Regression coverage must protect the CLI and guidance change. | Focused CLI test, deterministic skill eval, protocol/skill validation and relevant regression suite pass; actual outcomes are recorded. |

## Method, scope and verification

Reuse `research-resolution` and its accepted structural checker. Change only `karakana/cli.py` rendering, the research protocol review instruction, its Markdown template, shared process guidance and the existing artifact-gate skill/eval. Keep the source challenge proportional: select at least one negative lifecycle/failure state for each consequential eligibility, integrity or authority claim, or say why no source-level challenge applies. Inspect the full producer and consumer, not only a named helper. This is a human/model review record, not a deterministic proof of semantics.

Verify a blocked but structurally valid research closeout through `CliRunner`; inspect a valid ready closeout and a non-research check; run focused protocol tests, `karakana protocol validate-all`, `karakana skill validate-all`, the affected skill eval and full `pytest` if the shared CLI change passes focused checks. Review the diff for unrelated behavior. Rollback is a reviewed revert of this small branch; runtime traces/handoffs stay append-only.

## Test and eval rationale

The prior failure signature is a short CLI success that hides `implementation_ready: false`, plus artifact guidance that allows a helper-level claim without probing its negative cases. A CLI regression test can directly protect the former. A deterministic skill eval and protocol/template assertions can protect the presence of source-challenge instructions. Neither test can prove the next agent's substantive reasoning; reviewers still inspect the completed challenge and source references.
