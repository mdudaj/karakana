# Generic engineering artifact template

Kind: template
Status: Blank template
Package version: 0.1
Template date: 2026-09-26
Export audience: template-library

This is the primary Markdown template. Copy only the relevant sections into the
canonical documentation for a task; populate them with inspected evidence.
The accompanying workbook is a blank library for source-derived audience views.
Keep complete ADR/design reasoning in Markdown; use the optional summary and
source-section tables for sharing. Empty rows are starter rows, not real records.

No project names, features, release scope, ownership or delivery dates are prefilled.
Project-specific data belongs only in instantiated copies, never in this global asset.

The width comments below guide Excel presentation; they do not define artifact meaning.

## 00 Read Me

Purpose: Reusable blank library. Select relevant sections for the task and audience; all delivery data is empty.

<!-- workbook-widths: [42, 42] -->

| Topic | Instruction |
| --- | --- |
| Purpose | Global generic engineering artifact template. No project names, product features, release commitments or operational facts are prefilled. |
| Primary format | Author and review complete engineering artifacts in Markdown. The workbook is an accompanying sharing/review view. |
| Start | Copy this template for the task. Complete only relevant Markdown sections with inspected evidence; keep unused sections out of audience exports. |
| Blank rows | Operational tables contain one empty starter row. Blank means not recorded, never approved, passed or delivered. |
| Identity | Assign stable artifact/requirement/story/criterion/test IDs in the source. Do not use row position as identity. Link the Artifact Register to full Markdown paths/sections/revisions. |
| Sharing | Choose an audience from Audience Profiles. Share only relevant source-derived tables and declare omissions/full-source links in Control. Keep material blockers and limitations visible. |
| Source authority | Markdown owns documentation narrative/history. Link authoritative machine schemas/diagrams separately; avoid a second editable master. |
| Review feedback | Workbook comments/decisions are proposed feedback. Archive annotated exports, compare source ID/revision, and review changes into Markdown before regenerating. |
| Freshness | Complete source revision/hash and export metadata when producing a real view. The template hash in document properties identifies this blank asset only, not a project baseline. |
| Decision evidence | Review labels and names typed in a cell are not signatures or authorization. Approval evidence must be real, scoped and recorded through the governing review process. |
| Test truth | Keep case definition and execution separate. Use Not run, Blocked, Skipped, Fail or Pass only when their meaning is supported by evidence. |
| Release truth | Keep planned, locally verified, merged, published, deployed and accepted separate. Release notes describe delivered scope; forecasts remain forecasts until agreed. |
| Narrative | Write complete ADR/design rationale in Markdown. Workbook summaries link the full source; never truncate reasoning into cells. |
| Editing tables | In Excel, enter data in the blank starter row and use Tab from the last table cell to append rows. Preserve IDs when sorting/filtering. Confirm table ranges after editing in other applications. |
| Accessibility | Use text statuses as well as styling; check wrapping, links and assistive accessibility in the supported application before sharing. |
| Scope | This asset is a template library. It does not implement automatic audience exports, source validation, feedback reconciliation or a new approval workflow. |

## 01 Control

Purpose: Fill only from the source baseline and actual export/review context.

<!-- workbook-widths: [42, 42, 42] -->

| Field | Value | Guidance |
| --- | --- | --- |
| Project identity |  | Enter the identity only in a project-specific copy. |
| Artifact baseline |  | Reference the reviewed Markdown baseline. |
| Document version |  | Keep template, document and product versions distinct. |
| Template version | 0.1 | Version of this generic template asset. |
| Source Markdown paths |  | Full artifact paths; source sections listed in Artifact Register. |
| Source revision |  | Actual source revision used to export. |
| Source SHA-256 |  | Hash actual source content, not this template. |
| Author / owner |  | Use confirmed ownership. |
| Requested action |  | Research, planning, drafting, review or another agreed action. |
| Export ID |  | Assign when producing a derived view. |
| Audience / profile |  | Select relevant views; record profile/version. |
| Generated UTC |  | Actual generation timestamp. |
| Omitted content |  | Declare omitted detail and why. |
| Full-source links |  | Provide links to complete canonical artifacts. |
| Relevant blockers / limits |  | Retain material blockers even in brief summaries. |
| Feedback source export |  | Identify the baseline/export reviewed. |
| Feedback reconciliation status |  | Proposed, reviewed or reconciled, with evidence. |

## 02 Artifact Register

Purpose: Identify complete Markdown records and explicitly linked authoritative machine sources.

<!-- workbook-widths: [16, 28, 42, 28, 42, 42, 42, 42, 16, 42] -->

| Artifact ID | Type | Title | Status | Owner | Markdown Path | Source Section | Source Revision | Supersedes ID | Machine Source Link |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |  |

## 03 Sources

Purpose: Record inspected sources and their actual authority, revision and limits.

<!-- workbook-widths: [16, 42, 42, 42, 42, 42, 42] -->

| Source ID | Publisher / Owner | URI / Path | Edition / Revision | Inspected Date | Supported Claim | Limitations |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

## 04 Requirements

Purpose: One observable need or constraint per source record; retain unconfirmed priorities.

<!-- workbook-widths: [16, 28, 42, 42, 16, 42, 42, 42, 42, 28] -->

| Requirement ID | Class | Statement | Rationale | Source ID | Proposed Priority | Agreed Priority | Decision Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |  |

## 05 Stories

Purpose: Use actor, goal, benefit and conversation; link relevant needs through Links.

<!-- workbook-widths: [16, 42, 42, 42, 42, 42, 42, 42, 28] -->

| Story ID | Actor | Goal | Benefit | Conversation / Scope | Dependency IDs | Estimate / Basis | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |

## 06 Acceptance

Purpose: Define stable measurable criteria separately from actual test runs.

<!-- workbook-widths: [16, 42, 42, 42, 42, 42, 16, 42] -->

| Criterion ID | Context | Event | Expected Outcome | Measure / Threshold | Verification Method | Source Artifact ID | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |

## 07 ADRs

Purpose: Summarize decisions; full context, alternatives, rationale, consequences and history stay in Markdown.

<!-- workbook-widths: [16, 42, 28, 42, 42, 42, 42, 16, 42, 42] -->

| ADR ID | Title | Status | Decision Summary | Rationale Summary | Consequences Summary | Decision Owner | Source Artifact ID | Superseded By | Decision Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |  |

## 08 ADR Source Sections

Purpose: Optional section locators or excerpts for complete Markdown ADR reasoning.

<!-- workbook-widths: [16, 42, 42, 42, 16, 42, 42] -->

| ADR ID | Section | Sequence | Summary / Excerpt | Source Artifact ID | Source Section | Source Revision |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

## 09 Design Views

Purpose: Select views for real stakeholder concerns; link complete narrative and source diagrams.

<!-- workbook-widths: [16, 16, 42, 42, 42, 42, 42, 42, 16] -->

| Design ID | View ID | Stakeholder / Concern | Viewpoint / Scope | Elements / Interfaces | Scenario | Quality Constraint | Diagram / Schema Link | Source Artifact ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |

## 10 UX and Contracts

Purpose: Describe intended behavior and look/feel; link actual versioned machine contracts.

<!-- workbook-widths: [16, 42, 42, 42, 42, 42, 42, 16] -->

| Element ID | Behavior / States | Copy / Interaction | Accessibility | Shared Components / Tokens | Contract Link / Version | Examples / Constraints | Source Artifact ID |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |

## 11 Roadmap

Purpose: Describe outcomes and success measures; distinguish horizon/confidence from commitments.

<!-- workbook-widths: [16, 28, 42, 42, 42, 28, 42, 42, 42, 16] -->

| Outcome ID | Audience | Outcome | Success Measure | Horizon | Confidence | Proposal / Commitment | Dependencies | Review Trigger | Source Artifact ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |  |

## 12 Milestones

Purpose: Record goals, evidence of acceptance and explicit forecast/agreement basis.

<!-- workbook-widths: [16, 42, 42, 42, 42, 42, 42, 42, 28, 16] -->

| Milestone ID | Goal | Output | Owner | Checkpoint | Acceptance | Estimate / Basis | Forecast / Agreement Evidence | Status | Source Artifact ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |  |

## 13 Implementation Tasks

Purpose: Name inspected references, files, interfaces, steps and observable checks before execution.

<!-- workbook-widths: [16, 42, 42, 42, 42, 42, 42, 42, 16] -->

| Task ID | Inspect References / Revision | Files / Interfaces | Implementation Steps | Check / Expected Result | Dependencies | Owner | Approvals / Recovery | Source Artifact ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |

## 14 Release Plan

Purpose: Record candidate scope, target, readiness, rollout and recovery without implying execution.

<!-- workbook-widths: [16, 42, 42, 42, 42, 42, 42, 42, 42, 28] -->

| Release ID | Scope Baseline | Version Scheme | Candidate Revision | Target / Environment | Readiness Gates | Rollout | Recovery | Support / Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |  |

## 15 Release Notes

Purpose: Share delivered changes with the intended audience; link evidence and compatibility limits.

<!-- workbook-widths: [16, 16, 42, 28, 42, 42, 42, 42, 16, 16] -->

| Note ID | Release ID | Category | Audience | Delivered Change | Affected Behavior | Compatibility / Migration | Known Limits | Evidence ID | Source Artifact ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |  |

## 16 Test Cases

Purpose: Case definitions are not execution results.

<!-- workbook-widths: [16, 16, 42, 42, 42, 42, 42] -->

| Test ID | Criterion ID | Preconditions | Steps | Expected Result | Method / Test Source | Owner |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

## 17 Test Runs

Purpose: Record actual observations, revision, environment, time and evidence; leave unperformed runs empty.

<!-- workbook-widths: [16, 16, 28, 42, 28, 42, 42, 42, 16] -->

| Run ID | Test ID | Result | Actual Observation | Revision | Environment | Executed UTC | Executor | Evidence ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |

## 18 Risks and Decisions

Purpose: Record actual uncertainty and decisions needed; leave unconfirmed owners/dates unconfirmed.

<!-- workbook-widths: [16, 28, 42, 42, 42, 42, 42, 28, 16] -->

| Item ID | Type | Uncertainty / Decision Needed | Impact | Mitigation / Options | Trigger / Horizon | Owner | Status | Evidence ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |

## 19 Links

Purpose: Use stable qualified IDs and typed relationships rather than physical row numbers.

<!-- workbook-widths: [16, 42, 42, 16, 28, 42, 42, 16, 42] -->

| Link ID | From Namespace | From Type | From ID | Relation | To Namespace | To Type | To ID | Rationale |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |

## 20 Evidence

Purpose: Evidence must identify a scoped observation; a file path alone is insufficient.

<!-- workbook-widths: [16, 16, 42, 28, 42, 42, 42, 42, 42] -->

| Evidence ID | Related Artifact / Run ID | URI / Path | Revision | Environment | Observed Result | Observed UTC | Limitations | Content Hash |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |

## 21 Reviews and Approvals

Purpose: Capture proposed feedback and link real review evidence; no automatic import of agreement or approvals.

<!-- workbook-widths: [16, 16, 42, 42, 42, 42, 42, 42, 16, 42] -->

| Review ID | Source Artifact ID | Source Revision | Reviewer / Role | Review Type | Review Decision | Reviewer Comments | Reviewed UTC | Evidence ID | Reconciliation Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |  |

## 22 Change History

Purpose: Derive history from reviewed source changes; changed content requires reconsideration of earlier approvals.

<!-- workbook-widths: [16, 16, 42, 42, 42, 42, 42, 16, 16] -->

| Change ID | Artifact ID | Old Revision | New Revision | Reason / Impact | Author | Reviewer | Evidence ID | Feedback Export ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |

## 23 Guidance and Handover

Purpose: Select task-oriented guidance for the audience and reference actual tested runbooks.

<!-- workbook-widths: [16, 28, 42, 42, 42, 42, 42, 42] -->

| Guide ID | Audience | Task | Steps / Guidance Link | Support / Runbook Link | Known Limits | Owner | Tested Revision |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |

## 24 Vocabulary

Purpose: Suggested meanings, not mandatory project policies. Agree vocabularies in a project-specific copy.

<!-- workbook-widths: [42, 42, 42] -->

| Field | Value | Meaning |
| --- | --- | --- |
| Requirement class | Business | Organization outcome or need. |
| Requirement class | Stakeholder | Need of a stakeholder or actor. |
| Requirement class | Solution | Behavior or quality expected from the solution. |
| Requirement class | Transition | Temporary change/adoption need. |
| Test result | Not run | No execution recorded. |
| Test result | Blocked | Execution prevented by an unresolved condition. |
| Test result | Skipped | Intentionally omitted with recorded reason. |
| Test result | Fail | Observed result did not satisfy expected conditions. |
| Test result | Pass | Observed result satisfied expected conditions with scoped evidence. |
| ADR status | Proposed | Decision under consideration. |
| ADR status | Accepted | Decision accepted with real review evidence. |
| ADR status | Superseded | Replaced by another retained decision record. |
| Review Decision | Not reviewed | No substantive review response recorded. |
| Review Decision | Agree with proposal | Reviewer feedback; not external action permission. |
| Review Decision | Requires revision | Reviewer requests changes. |
| Review Decision | Needs decision | Explicit unresolved decision remains. |
| Relation | derived_from | Record originates from a source need or artifact. |
| Relation | satisfies | Record addresses a requirement or criterion. |
| Relation | verifies | Case or evidence checks an expected condition. |
| Relation | included_in | Record belongs to a scoped milestone or release. |
| Relation | supersedes | Record replaces another while preserving history. |

## 25 Audience Profiles

Purpose: Choose relevant sections; always retain applicable blockers, limits and source traceability.

<!-- workbook-widths: [28, 42, 42, 42] -->

| Audience | Selected Views | Always Retain | Full-Source / Review Boundary |
| --- | --- | --- | --- |
| Business / product | Requirements, stories, acceptance, roadmap and user-facing release notes | Dependencies; uncertain priority/forecasts; acceptance gaps; delivered versus planned scope | Link full Markdown source baseline; workbook changes remain proposed feedback. |
| Engineering | Requirements, acceptance, ADR summaries, design/contract links, tasks and technical changes | Decision status; quality/security constraints; test/compatibility gaps | Complete ADR/design content and machine schemas remain at authoritative source paths. |
| QA / UAT | Criteria, cases, actual runs, candidate/environment, evidence and defects | Not run/blocked/skipped/fail; unresolved criteria; evidence limits | Case definition and result remain separate; feedback is not imported sign-off. |
| Operations / release | Readiness, rollout/recovery, migration, monitoring, support and runbook links | Release blockers; restore gaps; known limits; authorization/environment status | Generating or sharing a view does not execute deployment or grant operational approval. |
| Executive / sponsor | Outcomes, milestones, confidence, material risks and decisions needed | Material blockers; forecasts versus commitments; deployed/accepted distinctions | Declare omitted details and link the complete source baseline. |
