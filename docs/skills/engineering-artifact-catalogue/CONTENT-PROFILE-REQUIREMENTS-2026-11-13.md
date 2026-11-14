---
status: decision_required
question: What document-specific completeness and evidence requirements should govern the first content profiles without confusing structural validity, substantive review and readiness?
evidence:
  - source: docs/engineering-artifacts.md
    finding: Minimum content is already described by artifact type; structural integrity does not establish substantive adequacy, and narrative authoring packs are outside P02 export compatibility.
  - source: karakana/tools/engineering_artifacts.py
    finding: parse_document and _validate_records check declared structure and selected record/evidence rules; neither selects a document completeness profile. PROFILES selects workbook audiences, not content requirements.
  - source: skills/engineering-requirements/assets/requirements-example.md
    finding: The accepted synthetic example deliberately retains unresolved quality measures and defines criteria without claiming executed tests.
  - source: skills/engineering-design-records/assets/system-design-example.md
    finding: The matching design has requirement-linked concerns and scenarios while retaining unresolved deployment and interface choices.
requirements:
  - decision: Owner accepted CP01-CP10 and the initial requirements/system-design scope in this round; preserve the accepted tailoring and authority conventions.
    acceptance: The review matrix distinguishes deterministic errors, review warnings and unresolved readiness; accepted examples and contrary cases have explicit expected outcomes.
    artifact: docs/skills/engineering-artifact-catalogue/CONTENT-PROFILE-REQUIREMENTS-2026-11-13.md
design:
  - choice: Use source inspection, immutable temporary-input probes and existing compatibility tests as the review method; leave checker architecture and representation for the owner-selected design round.
    rationale: The owner explicitly requested requirements review before design; a concrete requirements proposal and evidence can be completed without prematurely selecting an adapter, schema or CLI.
    artifact: docs/skills/engineering-artifact-catalogue/CONTENT-PROFILE-REQUIREMENTS-2026-11-13.md
artifact_choices:
  - kind: requirements
    disposition: updated
    path: docs/skills/engineering-artifact-catalogue/CONTENT-PROFILE-REQUIREMENTS-2026-11-13.md
    rationale: One compact record holds the proposed requirements, observable examples, evidence and exact owner decision.
  - kind: design
    disposition: updated
    path: docs/skills/engineering-artifact-catalogue/CONTENT-PROFILE-REQUIREMENTS-2026-11-13.md
    rationale: Records the selected research method and boundaries for the next design review; it does not claim solution architecture is settled.
  - kind: example
    disposition: reused
    path: skills/engineering-requirements/assets/requirements-example.md
    rationale: Existing requirements and matching design examples are substantive positive controls with explicit unresolved facts; no template edits are required this round.
  - kind: test
    disposition: reused
    path: tests/test_engineering_artifacts.py
    rationale: Existing compatibility tests were run with documentation-skill and pilot tests; future profile-specific cases are specified below rather than implemented.
  - kind: plan
    disposition: not_applicable
    rationale: Implementation planning follows accepted requirements and the separate design review; this round names the exact next action and design questions only.
  - kind: schema
    disposition: not_applicable
    rationale: No profile schema, source format, API, snapshot or export contract is changed or selected in this requirements review.
  - kind: UX
    disposition: not_applicable
    rationale: No interface is delivered this round; CP09 specifies understandable diagnostic behavior for the later design and UX-writing review.
authority:
  state: pending
  evidence: Owner accepted the CP01-CP10 requirements review with "accepted" on 2026-11-13. Requirements/two-profile scope are accepted; CD01-CD12 design was subsequently accepted on 2026-11-14. M1 was subsequently selected with execute and is now locally implemented/verified. M1 source integration and M2 remain separate; no remote publication is authorised.
pending_decisions:
  - owner: Project owner
    question: Select source integration of locally verified M1, and separately review the exact M2 reference-edge amendment before M2?
    next_action: Reuse accepted CP/CD and M1 verification; review source and separately authorise PR/squash integration, preserving the M2-only amendment decision.
next_action: Review locally implemented/verified M1 and its source-integration evidence; M2 reference-edge amendment remains pending.
---

# Document content-profile requirements review

Revision 0.1, 2026-11-13. Project: Karakana engineering documentation.
Trace: `20261113-190330-d2169b`. Baseline: `fc93fbcf6b3d7f79fcffa6406c2bfc983b6f3654`
(PR #37). Branch: `research/engineering-content-profile-requirements-20261113`.
Current status: CP01-CP10 and the two-profile scope accepted by the owner on
2026-11-13. The original review below is retained as history; the acceptance
entries at the end govern continuation. CD01-CD12 design was also accepted on
2026-11-14. Overall implementation readiness still needs the separate bounded
plan/task selection; neither accepted review is outstanding.

## Problem, readers and intended outcome

Authors and reviewers need to distinguish a well-formed document from a sufficiently
complete specification or design. The accepted contract already describes minimum
content, but current execution checks only supported source structure and selected
record integrity. A template or an attached nonempty file cannot establish that the
required content exists, that a statement is meaningful, or that evidence is true.

The first profiles should cover the two accepted clean packs: requirements and
system design. They should describe applicable content and evidence rather than
force every library section into every document. Small changes may reuse a current
governing baseline and describe only their affected requirements or views.

## Current evidence and limits

Inspected the shared contract, CT01-CT08 accepted decisions, PI01-PI08 closeout,
P02 guide, shared conventions/resource map, requirements/design guides, clean
templates and examples, parser/validator/CLI, protocol checks and related tests.
`PROFILES` in `engineering_artifacts.py` is an audience projection map; it does
not implement the proposed content profiles. Generic protocol checks still assess
file presence; `research_resolution` additionally checks structure and references.

Temporary-directory probes reused the real `document()` test fixture and actual
`load_bundle` and validate CLI. No source bytes changed during validation.

| Probe at the recorded baseline | Records / outcome |
| --- | --- |
| Ordinary supported requirement | 1; no issues; CLI 0, explicitly structural only |
| Replace statement with meeting-arrangement prose | 1; no issues; CLI 0 |
| Replace statement with “The system shall be fast and secure.” | 1; no issues; CLI 0 |
| Supported all-empty Requirements table | 0; no issues; CLI 0 |
| Metadata-bearing narrative with only meeting prose | 0; no issues; CLI 0 |
| Each clean narrative requirements/design example passed to P02 | Refused for absent scalar YAML frontmatter; no P02 compatibility claimed |

Probe receipt: `/tmp/karakana-content-profile-probe.json` (supporting local runtime
evidence, not required on another machine). The table preserves portable results.
Existing focused artifact/documentation/pilot suite: **140 passed in 4.90s**.
No new validator, model evaluation or complete regression run is claimed.

## Proposed requirements and acceptance

| ID | Requirement | Observable acceptance / boundary |
| --- | --- | --- |
| CP01 | Check the explicitly selected document type, scope and supported profile/version. Start with requirements and system design; retain applicability and baseline references. | A requirements check cannot silently become a design or audience check. Unsupported inputs/versions are reported as unsupported, never complete. Automatic resource selection remains later work. |
| CP02 | Require applicable document identity/revision, scope/product applicability, canonical source/baseline and standards/reference use. Preserve source authority and accepted history. | Missing required information is identified; a scoped referenced baseline can supply unchanged context. No native field is overwritten or editable duplicate master created. Internal approval records need not be printed as repeated issued-document disclaimers. |
| CP03 | Requirements content shall cover problem/outcome, users/context, scope/non-goals, affected functional needs, applicable quality/constraints, rationale/source and linked criteria/verification. | An in-scope requirement has a stable ID and observable criterion/method; criteria link back to requirements. A compact change may reference existing requirements rather than duplicate them. Missing applicable coverage is reported; source and criterion prose still need substantive review. |
| CP04 | System-design content shall cover requirement baseline, concerns/boundaries, responsibilities, relevant runtime and failure paths, data/interfaces, security/quality, operations, consequential decisions and verification/gaps. | Required coverage is present or resolved through a current governing view. UX behavior/look and feel, migration and detailed views apply when affected. No fixed diagram count or mandatory full architecture for a tiny change. |
| CP05 | Enforce deterministic completeness rules for applicable required content while supporting justified tailoring. | Missing/empty required items, unresolved template substitution fields, duplicate identities and unresolved declared references fail the applicable check. Headings or blank rows alone do not satisfy content. Literal syntax examples are distinguished from unfilled fields. Optional omissions and referenced views are allowed with a recorded rationale where material. |
| CP06 | Preserve unknown facts and state their effect on acceptance/readiness rather than invent values. | An unresolved measure names the affected requirement, decision role/source and next resolution action. It may be reviewable content but cannot establish the affected readiness/acceptance claim. A missing threshold is not silently assigned or made irrelevant by an exclusion. |
| CP07 | Separate advisory wording diagnostics from deterministic failures and substantive review. | Vague/multi-claim requirements or likely authoring logistics in a product-requirements section prompt contextual review. The word “approval,” meeting-related product behavior or absence of “shall” does not itself cause rejection. Meeting minutes remain valid under their own applicable type. Human review determines intent and adequacy; no word list certifies them. |
| CP08 | Keep intended behavior, planned verification, observed results and actual scoped approval distinct. | A claimed executed result or accepted decision needs its applicable revision, actor/role, observation/decision and evidence; defined criteria alone do not count. Evidence fields/links establish declared provenance, not authenticity or independent review. No checker advances approval, release or deployment state. |
| CP09 | Report rule, severity, source location and actionable explanation, bound to the checked source/profile/checker versions. | Changed source/dependency/profile/checker invalidates reuse of the corresponding result. Diagnostics separate completeness errors, review warnings and unresolved acceptance effects, avoid exposing source cell contents, and state unsupported coverage. Visual rendering and substantive review remain separate checks. |
| CP10 | Preserve existing parser, binding, source-hash, export and safety behavior while introducing explicitly scoped content checking. | Existing structural validation and legitimate empty/narrative sources retain their contract. An empty template cannot pass as a completed requirements/design artifact when applicable content is absent. Clean narrative checking does not imply P02 export support. Sources remain unchanged; no automatic model calls, protocol activation or external writes. |

Required means applicable to the selected document and affected scope. An omission
reason can be checked for presence, but its truth and acceptability require review;
it cannot mechanically waive an essential requirement. Requirements and design are
the first two profiles, not a claim that all existing document types are covered.

## Expected review cases

| Input / claim | Required result under the proposal |
| --- | --- |
| Existing synthetic requirements/design pair | Content review can proceed; Q-01/Q-02 and design gaps remain visible, affected readiness unresolved, no application acceptance |
| Bare heading, whitespace, blank table or unchanged substitution fields used as required completed content | Applicable completeness error; blank authoring templates remain valid templates |
| Small interface change linking a current context/deployment baseline | Accept valid referenced coverage; review affected contracts and scenarios, no forced duplicate chapters |
| Meeting-arrangement statement in functional requirements | Review warning for misplaced authoring activity; not accepted as product behavior merely because it parses |
| Product requires independent approval before access | Valid requirement subject to ordinary source/criteria review; no banned-word rule |
| Quality target explicitly unresolved with effect and decision role | Reviewable unresolved content, affected readiness blocked; invented target is not a valid correction |
| Defined criterion or planned check described as a passed test | Refuse the executed-result claim without applicable scoped observation/evidence |
| Source/profile/checker or a governing referenced source changes | Previous result does not certify the new baseline; recompute applicable checks |
| Intentionally empty release table or supported narrative passed to structural validation | Existing result preserved; first-two-profile completion is neither automatically required nor inferred |
| Clean narrative assets sent to existing P02 without a supported adapter | Continue to report unsupported source shape; no silent conversion/export claim |

## Standards and references

Carry forward CT05 and the accepted guides. Official public catalogue pages were
checked on 2026-11-13; full normative texts and clause-level assessment were not
reviewed. These references inform tailored content, not certification. Mandatory
project obligations, if any, must be separately identified with their evidence.

| Reference | Application |
| --- | --- |
| [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html) | Requirements engineering/content and traceable verification guidance; retain the accepted edition rather than silently adopt a draft replacement |
| [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html) | Architecture-description concerns/views; does not prescribe the implementation or a tool/media format |
| [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html) | Reference model for applicable product-quality requirements, measures and evaluation |
| [ISO/IEC/IEEE 15289:2019](https://www.iso.org/standard/74909.html) | Purpose and content tailored to information-item type |
| [NASA requirement-writing checklist](https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/) | Supplemental clarity, traceability and verifiability review; local no-invented-facts and product-approval conventions govern tailoring |

## Source-alignment challenge

| Claim challenged | Producer / consumer / contrary state | Resolution |
| --- | --- | --- |
| Structural success proves complete requirements | Fixture -> parse_document -> load_bundle/_validate_records -> validate CLI accepts meeting/vague prose and zero rows | CP03/CP05/CP07 specify separate completeness and review; preserve the honest structural-only CLI claim |
| Every zero-row input is defective | parse_document deliberately skips all-empty starter rows; existing empty-release and narrative controls pass in the focused suite | CP10 preserves them; only an applicable selected profile may require substantive coverage |
| Narrative assets are already validated by the structured exporter | Both clean examples fail frontmatter preflight; resource map explicitly disclaims P02 compatibility | CP01/CP10 require explicit support reporting; design must choose a supported reading path before implementation |
| Accepted examples must show complete readiness | Requirements Q-01/Q-02 and matching design intentionally have unresolved measures/contracts | CP06 separates reviewable content from readiness; do not rewrite examples to fabricate answers |
| A profile check or evidence link proves truth/approval | _validate_records checks supplied fields/timestamps; generic protocol checks mostly check files, not provenance authenticity | CP08/CP09 report exact check limits and source binding without claiming independent acceptance |

## Recommendation, alternatives and owner decision

Recommend CP01-CP10 with two initial explicit profiles. It extends accepted content
guidance and protects real negative cases without expanding into automatic routing
or a universal document format. This assumes the two accepted packs remain the
immediate priority; the owner may revise the ordering during this review.

Templates/manual review alone has lower implementation cost but leaves missing
content and stale checks unenforced. A universal mandatory outline/positive-count
rule is simpler mechanically but rejects valid tailoring, narrative and deliberate
emptiness. Enforcing semantic quality using phrase bans creates false positives;
keep uncertain diagnostics advisory with substantive review. A general Markdown
engine or new source adapter is a design option, not a requirements decision made
here. Any broader compatibility cost must be made concrete in that next round.

Exact decision owner: project owner. Confirm acceptance of CP01-CP10 and the
requirements/system-design first scope, or specify revisions. **Pending.** User
silence is not acceptance. This review is self-review, not independent validation.

Safe work completed now: inspect current evidence, exercise existing validators,
draft requirements, expected cases and continuation. Held work: checker architecture,
profile representation/adapter/CLI design selection, implementation, new enforcement,
PR publication/merge and live actions. The staged requirements/design review is the
owner's explicit workflow; no additional approval process is introduced by a skill.

After acceptance, record the exact decision here and prepare the design review:
source representation and supported formats; applicability/exemption handling;
profile schema/version ownership; checks/severity/report contract and freshness;
compatibility and concrete regression cases. Implementation gets its own bounded
plan and gate after the design round. Source integration of this record also needs
its own authorised PR task. Remaining templates/exports, task selection/enforcement,
pilot and Jovina remain later work.

## Verification and continuation

Local baseline and instructions reconciled; five structural probes and two narrative
refusal controls ran without source changes; 140 focused tests passed. Research
closeout structure/local references and diff whitespace are checked before handoff.
These verify the review evidence and artifact, not a proposed checker. No production
code, tests, templates, protocol rules, client documents or deployment changed.

Next recommended task is owner requirements review, then the separate design round
once accepted. Continue this conversation for that decision; use GPT-6 Sol with high
reasoning for consequential integrity/gate design (recommendation only; active model
not independently observed or changed). Do not restart CT/PI research. Preserve
this proposal and append agreement/revision history rather than silently replacing
accepted choices.

Completion gate `20261113-190850-protocol-check-c4ef2e` passed for the bound
research trace: artifact presence plus research structure only. Its separate
outcome is `decision_required`, with `implementation_ready: false`. The final
append-only handoff carries this review and the exact owner decision.

## Owner acceptance — 2026-11-13

After the self-contained requirements review summary, the owner replied **“accepted.”**
This accepts CP01-CP10 and the requirements/system-design first scope for this
round, without revisions. Earlier proposal/pending wording above is historical;
requirements acceptance is no longer outstanding. This entry preserves the
original recommendation and its alternatives rather than rewriting that history.

Next task: prepare the separate design review against these requirements. Settle
supported narrative/structured inputs, profile representation/version ownership,
applicability and governing-view references, deterministic checks versus review
diagnostics, reporting/freshness and compatibility/regression strategy. Present
the proposal here before implementation. No implementation or publication has
been selected by this acceptance, and no new approval process is introduced.

Acceptance-record task: 20261113-191311-727b44 (administrative assessment only;
no new requirements or solution-design decision). Verified the owner statement,
unchanged CP01-CP10 scope and initial two profiles; closeout structure/references
remain valid, and whitespace is clean. The 140-test result above is reused from
the requirements review, not rerun for this decision-history edit. No runtime
behavior changed. Refresh the task-bound handoff so design can reuse this accepted
research/requirements evidence without repeating the requirements questionnaire.

## Design review prepared — 2026-11-13

The owner selected the separate design task with “execute” after its task brief.
[CD01-CD12](CONTENT-PROFILE-DESIGN-2026-11-13.md) now provides the concrete design,
source/CLI/report boundaries, trade-offs, negative-state evidence and delivery
outline. Design acceptance is pending. CP01-CP10 and their acceptance above remain
unchanged. No implementation, dependency change or remote publication is included.

## Design acceptance carried forward — 2026-11-14

The owner accepted the CD01-CD12 design summary with **“accepted”**, without
revisions. The [design acceptance history](CONTENT-PROFILE-DESIGN-2026-11-13.md)
governs continuation alongside CP01-CP10. Earlier design-pending wording above
is historical. Both reviews are settled; next is bounded implementation planning.
No requirements changed and no checker implementation or publication occurred.

## Bounded implementation plan — 2026-11-14

[The plan](CONTENT-PROFILE-IMPLEMENTATION-PLAN-2026-11-14.md) carries accepted CP/CD
choices into two sized, sequential implementation milestones. Requirements remain
unchanged; partial M1 delivery cannot claim all CP/CD completion. A proposed M2-only
reference-edge contract clarification is explicit there, with owner and exact
decision. No implementation or remote action follows from planning alone.

## M1 execution checkpoint — 2026-11-14

The owner selected local M1 implementation with “execute” after the bounded plan.
[M1 results](CONTENT-PROFILE-IMPLEMENTATION-PLAN-2026-11-14.md) record the delivered
standard-pack checker, 885 passing tests, 186 passing evals and unchanged P02/asset
baselines. Accepted CP/CD choices are preserved; this is partial local delivery,
not M2 completion or independent acceptance. Source review and separately
authorised PR/squash integration are next. No new PR/merge/deployment occurred.
