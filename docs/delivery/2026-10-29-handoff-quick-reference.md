---
status: ready_for_implementation
question: How can handoff loading show current backlog position, trustworthy status and actionable next work without burying them in historical notes?
evidence:
  - source: karakana/handoffs/summary.py and actual ent-meal handoff load
    finding: Load shows milestone and full next brief but lacks structured backlog/status; authors currently paste the entire backlog into the brief, and generic guidance crowds continuation.
  - source: karakana/handoffs/builder.py and schemas.py
    finding: The existing redacted continuation dictionary can carry optional quick-reference metadata without changing top-level handoff schema or old-artifact loading.
requirements:
  - decision: Add an explicit authored position, separate delivery states and sourced backlog snapshot to saved/load output; keep the complete next brief and expose supporting detail on demand.
    acceptance: CLI create/refresh/load tests prove exact data, legacy defaults, stale-source warnings, redaction, immutable history, project boundaries and full next-brief retention.
    artifact: /home/jmduda/KodeX/karakana/docs/delivery/2026-10-29-handoff-quick-reference.md
design:
  - choice: Store optional quick_reference under continuation; author with repeatable delivery-state/backlog-item flags and a validated backlog-source, render a status/backlog panel first, add load --details for long guidance.
    rationale: Deterministic explicit facts and source fingerprint avoid guessing progress from old prose; existing readers tolerate nested continuation metadata and no stored history is rewritten.
    artifact: /home/jmduda/KodeX/karakana/docs/delivery/2026-10-29-handoff-quick-reference.md
artifact_choices:
  - kind: requirements
    disposition: updated
    path: /home/jmduda/KodeX/karakana/docs/delivery/2026-10-29-handoff-quick-reference.md
    rationale: One compact requirements/research/design/acceptance record.
  - kind: design
    disposition: updated
    path: /home/jmduda/KodeX/karakana/docs/delivery/2026-10-29-handoff-quick-reference.md
    rationale: Optional metadata, explicit authoring, common rendering and provenance checks.
  - kind: architecture_schema
    disposition: reused
    path: /home/jmduda/KodeX/karakana/karakana/handoffs/schemas.py
    rationale: Preserve top-level schema; nested optional continuation data is recursively redacted and legacy readers already allow unknown nested keys.
authority:
  state: approved
  evidence: Owner explicitly requests research and enhancement of harness handoff output. Local reviewable code/tests/docs are in scope; no push, merge, external messages or deployment.
pending_decisions: []
next_action: Pass prerequisites, retain red CLI regressions, implement optional quick-reference authoring/rendering, verify full gates and actual app/harness handoffs.
---

# Handoff quick reference

The current handoff answered "what next" but required long pasted notes to answer
"where are we" and "what remains". The owner's repeated backlog/status requests
are the concrete failure case. Preserve the unmerged next-task-brief correction
`8ff3467` as the reviewed dependency; this feature branch
`feat/handoff-quick-reference` extends it without merging or rewriting that history.
Research trace `20261029-143753-739777`; implementation
`20261029-143753-e983e5`. This is an output/authoring enhancement, not a routing,
execution or approval-policy change. The parallel ent-meal flow task has separate
source, traces and verification; never mix its completion state into Karakana's.

## Research and selected approach

[CLI Guidelines](https://clig.dev/#saying-just-enough) explain how too little
information and pages of incidental output both obscure useful state. Their
[output guidance](https://clig.dev/#output) supports human-readable summaries with
structured data retained for tools. Apply that here as a concise default and an
explicit `--details` path, without truncating the next-task brief or hiding safety.

Google SRE's [state-document/handoff guidance](https://sre.google/sre-book/managing-incidents/)
puts important current information first, retains history and makes handover
explicit. This is an adaptation to agent continuation, not a claim that software
tasks are incidents: separate current position, recorded evidence/state, open
work, held decisions and next action; preserve older snapshots as history.

The source inspection shows why merely rendering state_summary would fail: it
mixes completed narrative with pending instructions, recovered references can be
old, and the generic memory backlog may describe bootstrap long since completed.
An automatically inferred completion percentage or checkbox extraction would
misrepresent source integration versus target acceptance. Prefer an authored,
bounded snapshot linked to the actual current backlog, with explicit unknowns
and a content fingerprint. The source remains authoritative, not this snapshot.

## Requirements, CLI contract and source alignment

- HQ01: `--backlog-position TEXT` states the current lane/milestone position.
  Missing legacy values use the recorded milestone as position only; never infer
  delivery completion from prose or commit-looking strings.
- HQ02: Repeatable `--delivery-state STAGE=VALUE` accepts implemented, verified,
  merged, deployed, accepted. Unrecorded stages stay explicitly "Not recorded".
  Free-text values carry receipts or limits; they are recorded claims, not an
  independent check or authority to execute. Duplicate/unknown stages fail.
- HQ03: `--backlog-source PATH` must resolve to an existing local file; retain its
  absolute reference and SHA256. Repeatable `--backlog-item ID|STATE|SUMMARY`
  accepts done, in_progress, next, queued, blocked, deferred, conditional. Require
  source for authored items; reject duplicate IDs and malformed/unknown states.
  Preserve every supplied item and explicit hold/deferral text; no guessed total
  backlog, completion percentage or automatic task selection.
- HQ04: Put Where we are, five delivery states, snapshot date/source and backlog
  rows before the full Next Task Brief in both persisted Markdown and load.
  Preserve exact next action and its routing meaning. Check source fingerprint
  read-only when rendering; missing/changed source warns prominently and requests
  reconciliation. Age/recovered warnings stay visible; never silently update a
  snapshot from a changed source or erase a deferral.
- HQ05: Default load retains full next brief, essential safety, inspect-first,
  selected nonempty OKF context and concise stage/model/conversation guidance.
  `--details` adds advisory reread/skills and full continuation explanation;
  saved full Markdown retains all existing detail. Explicitly advertise details.
- HQ06: Use existing recursive handoff redaction before persistence and display.
  Escape table delimiters/newlines for legibility. Old artifacts and nested-key-
  tolerant readers remain compatible; no top-level schema migration, provider,
  model switch, automatic agent, approval or production change.
- HQ07: Tests run in temporary repositories, never writing test runtime state to
  the working checkout. Cover actual CLI roundtrip, both renderers, immutable
  prior handoffs, missing/changed source, malformed input, unknown legacy data,
  redaction, complete multiline brief and default/detail output. Add deterministic
  eval coverage and update handoff skill/reference guidance. Validate actual
  ent-meal and Karakana loads with a real sourced snapshot before completion.

Data path: CLI options -> create_handoff -> validated quick-reference builder ->
continuation metadata -> HandoffArtifact recursive redaction -> append-only store
-> shared quick-reference renderer/session start. A sourced snapshot does not
prove the backlog's semantic currency; the author must reconcile the source.
Fingerprint checks detect changes, not truth or approval. Explicit source outranks
the generic memory backlog in inspect/reference selection. Known open findings,
recovered state, changed/missing source and age warnings cannot be lost in a
compact view. Missing metadata is a useful visible unknown, not an empty success.

## Artifact and safety readiness

This record supplies change summary, schema contract, migration plan (none;
optional nested metadata), owner approval record, traceability and safety/abuse
review. Do not parse/execute backlog text, infer permissions, send messages,
follow external URLs, modify source files or rewrite historical handoffs while
loading. Existing explicit load recovery remains unchanged; use --no-create for
a strictly non-creating probe. Source must be a file; errors avoid echoing raw
secret-like arguments. Rollback is a reviewed code revert; stored compatible
continuation dictionaries and prior artifacts remain readable.

## Verification and next action

Implemented explicit authoring in create/refresh, optional nested metadata,
shared quick-reference rendering, visible source/age/recovery attention, concise
default and --details output. Complete next-task text and essential safety/model/
stage/conversation/recommendation guidance remain in both load modes. Five delivery
stages never infer one another. Snapshot source outranks generic memory backlog
and is hashed read-only. Author-supplied text is redacted, table-escaped and stripped
of terminal controls. Missing/malformed metadata stays unknown with appropriate
warnings. Prior JSON/Markdown artifacts remain byte-for-byte unchanged.

Added KDX-09 to the harness-owned backlog and replaced ent-meal's historical
bootstrap list with an authoritative-ledger pointer. Actual application backlog
rows remain in their owning repository. Updated README usage and handoff skill;
the new deterministic eval encodes explicit status/source/deferral requirements.

| Gate | Result |
| --- | --- |
| Red | **5 failed,5 passed in0.69s**; new authoring/roundtrip/precedence absent, existing invalid-option rejection already held. |
| Focused | **55 passed in2.08s**, CLI/history/legacy/redaction/project/freshness/metadata/output coverage plus existing handoff contracts. |
| Full | **753 passed in20.64s**, including the final attention-vs-success regression. Earlier752-test results remain diagnostic history in the receipt logs. |
| Evals | **179/179 passed**, zero warnings. No live provider calls. |
| Validation | All skills and skillpacks passed; affected ent-meal and karakana memory complete; local links/whitespace and new Python lint checked. |

Only code/test files are treated as frozen source for the full gate; delivery
receipts and append-only handoffs record subsequent completion. No remote
publication or merge is inferred. Actual create/refresh/load and detailed-load
review for both live local projects completes below via ignored runtime receipts;
doctor and complete next-brief assertions must pass before reporting completion.
Next harness task is review/integration of retained `8ff3467` and this enhancement
as one coherent handoff PR, using exact commits and actual output evidence.

Actual local-project output review passed for ent-meal and karakana: quick reference
precedes the complete multiline brief, all authored backlog rows/delivery states
survive default and --details load, source fingerprints are current and doctor
passes (including backlog_snapshot_current). Successful protocol notices remain
in full saved history rather than creating a misleading default Attention block;
real findings, stale/recovered state and failed/source-change notices stay visible.
Runtime evidence is under `.karakana/reviews/20261029-handoff-quick-reference/`
and the app's separate form-flow evidence directory. Final post-commit handoffs
record exact local commits; no PR, merge, deploy or live provider call occurred.
