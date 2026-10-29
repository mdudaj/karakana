# Explicit next-task briefs in handoff loading

The owner twice requested a next-task brief in the ent-meal handoff. The agent
put it in a long `--from-note` state summary and checked only substring presence
in the saved Markdown. `handoff load` uses `render_session_start`, which omits
state_summary. The brief therefore disappeared at the actual continuation entry
point. This is both an authoring/review miss and a missing structured output field.

## Requirement, design and readiness

As a continuing agent/user, I can read the next task's problem, preferred scope,
acceptance and first action directly when loading the handoff, without searching
the completed-work narrative. Add optional `next_task_brief` to the handoff
artifact, builder and create/refresh CLI (`--next-task-brief`). Render a dedicated
Next Task Brief section in saved Markdown and session-start output. Preserve
existing next-task routing and exact-action semantics; the brief is descriptive,
not authority to implement. Missing legacy values default empty and do not invent
a plan. Apply existing redaction before persistence/rendering. Append new handoffs;
never overwrite historical artifacts.

Inspect schemas, builder, summary renderer, create/refresh CLI and existing
session/continuation tests. Governing sources: AGENTS/KARAKANA, engineering process,
agent guide and karakana-handoff/self-improvement skills. This bounded optional
field requires no architecture, schema migration, routing/provider, external
service, safety-gate or deployment change. A state-summary dump in load would
bury the next task in completed history; an explicit field is preferred. One
compact record supplies requirements, story, design, readiness and traceability.

Plan: prerequisite gate; add CLI regression against temporary repositories,
observe failure; implement optional redacted field and two render paths; update
handoff skill/command guidance; run focused tests, full pytest, evals and skill
validation; refresh ent-meal with the actual next-task brief and verify load.
Keep this harness patch reviewable on its own branch; ent-meal PR103 integration
is a separate completed action. No automatic merge of this harness patch.

## Acceptance, test rationale and definition of done

R1: create and refresh store the exact safe multiline brief in JSON/Markdown and
print it under a dedicated heading in load. R2: injected secret-like text is
redacted in storage and load, using the existing policy. R3: legacy handoffs
without the new field load with an empty default. R4: refreshed handoffs preserve
prior artifacts unchanged; routing/exact-next-action remain intact. Cover these
through real CLI create/refresh/load and schema/renderer tests in temporary
repositories, not the working runtime store. Run current required gates before
claiming verified; record actual evidence below. Rollback: reviewed revert of
the optional-field change; historical artifacts remain intact.

## Delivery and continuation

Trace `20261027-112827-542437`. Checks and results appended after execution.
The corrected ent-meal handoff must summarize: consolidate repeated Tasks
restricted-worklist panels into one compact explicit access summary; preserve
authorized work, personal assignments, restricted counts/CTA boundaries and
legitimate export history; test manager/field/executive/external/revoked scope
and desktop/compact keyboard use. First action is to define that bounded slice
from the current merged source. It remains recommended, not implemented.

## Verification and review state

Prerequisite gate `20261027-112906-protocol-check-4b268d` passed before code edits.
All three new cases failed on old source (missing CLI flag/builder argument).
After the bounded optional-field patch, focused session/continuation/provenance/
skill tests passed **40/40 in 1.33s**. Full `pytest -q`: **738 passed in 20.56s**.
`karakana eval run`: **178/178 passed, zero warnings**, report
`20261027-112959-eval-3debbd`. All installed skills validate; whitespace passes.
The temporary-repository CLI tests verify the actual load heading/body, create
and refresh persistence, historical artifact bytes, secret redaction and missing
legacy-field behavior. No working runtime state was used by tests.

Changed schema/builder/renderers and create/refresh arguments, added three
regressions, documented the flag and updated the handoff skill to require checking
actual load output. No routes, models, approval gates or external execution policy
changed. This harness correction remains a local reviewable branch; it has not
been published/merged. Reverting/switching to code without this optional field
requires care when reading newly authored artifacts; integrate the reviewed
renderer patch before using those artifacts from an older checkout.

The report-row application work is separately squash merged through ent-meal
PR103 as `21586d5`, with one parent and the reviewed tree unchanged. Local app main
is clean and only its merged source branch was removed. Hosted CI/deployment
remain deferred/disabled as previously directed. The refreshed ent-meal handoff
will provide the dedicated brief in actual load output; preserve previous history.
