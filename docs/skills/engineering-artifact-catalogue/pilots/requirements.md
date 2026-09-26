---
contract_version: '0.1'
namespace: pilot-checklist
document_id: DOC-REQ
document_type: document
content_version: '0.1'
status: draft
owner: unconfirmed
requested_action: review controlled synthetic pilot
source_authority: authored Markdown
---
# Pilot requirements, story and verification boundaries

Authored from [the synthetic brief](brief.md). All product claims are proposed;
there are no interviews, implemented reader or observed product tests. This source
is an instantiated pilot copy, not the global template.

<a id="context"></a>
## Context and scope

The reader wants to locate checklist items without modifying a catalogue. Exact
category filtering is the selected scenario scope; it is not a design endorsement.
Non-goals include editing, remote services and deployment. Product acceptance and
performance targets remain unconfirmed. Native engine stores are not involved.

<a id="register"></a>
## Artifact Register

| Artifact ID | Type | Title | Status | Owner | Markdown Path | Source Section | Source Revision | Source SHA-256 | Source Authority | Supersedes ID | Machine Source Link |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DOC-REQ | document | Reader need and criteria | draft | unconfirmed | requirements.md | context | 0.1 |  | Authored Markdown |  |  |
| DOC-DESIGN | document | Proposed input boundary | draft | unconfirmed | design.md | context | 0.1 |  | Authored Markdown |  |  |
| DOC-PLAN | document | Outcome and learning plan | draft | unconfirmed | plan.md | context | 0.1 |  | Authored Markdown |  |  |
| DOC-RELEASE | document | Release gaps and adoption | draft | unconfirmed | release.md | context | 0.1 |  | Authored Markdown |  |  |
| CONTRACT-CATALOGUE | contract | Candidate catalogue schema | draft | unconfirmed | design.md | contracts | candidate-0.1 | 8e06fa19a78185e365fd5bc3fbc6566a6954d0813c19bc583adfe812e102bf46 | Machine source |  | catalogue.schema.json |

<a id="sources"></a>
## Sources

| Source ID | Publisher / Owner | URI / Path | Edition / Revision | Inspected Date | Supported Claim | Limitations |
| --- | --- | --- | --- | --- | --- | --- |
| SRC-BRIEF | synthetic scenario author | brief.md | pilot-0.1 | 2026-09-26; authored seed | Read-only exact category lookup and explicit errors | Fictional intent; no stakeholder agreement |
| SRC-CONTRACT | synthetic contract author | catalogue.schema.json | candidate-0.1 | 2026-09-26; local file | Proposed object fields | No accepted interface or implementation |

<a id="requirements"></a>
## Requirements

| Requirement ID | Class | Statement | Rationale | Source ID | Proposed Priority | Agreed Priority | Decision Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| REQ-01 | Stakeholder | A reader can list items for an exact case-sensitive category. | Locate relevant checklist items. | SRC-BRIEF | proposed high | unconfirmed |  | unconfirmed | draft |
| REQ-02 | Solution | Empty matches and malformed input produce distinct explanatory states with no partial malformed list. | Avoid confusing absence with parse failure. | SRC-BRIEF | proposed high | unconfirmed |  | unconfirmed | draft |
| REQ-03 | Solution | Opening and filtering a catalogue leave its input bytes unchanged. | Preserve the supplied checklist. | SRC-BRIEF | proposed high | unconfirmed |  | unconfirmed | draft |

<a id="stories"></a>
## Stories

| Story ID | Actor | Goal | Benefit | Conversation / Scope | Dependency IDs | Estimate / Basis | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| STORY-01 | checklist reader | locate items in a category | I can focus on the relevant checklist | Exact category; empty/error handling; no editing or authentication. | REQ-01; REQ-02; REQ-03 | unconfirmed | unconfirmed | draft |

<a id="acceptance"></a>
## Acceptance

| Criterion ID | Context | Event | Expected Outcome | Measure / Threshold | Verification Method | Source Artifact ID | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AC-01 | Catalogue has category review and category planning | Reader filters review | Only ITEM-01 is shown; stable item ID and title are visible | Exact case-sensitive match; whitespace handling not yet explicit | Fixture-driven functional test plus actual user walkthrough | STORY-01 | unconfirmed |
| AC-02 | One valid empty-match input and one malformed input are supplied | Reader opens/filters each input | No matches shows No items in this category; malformed input shows Cannot read checklist with no partial list | Two distinct states; keyboard focus and assistive announcements need observation | Error/empty-state tests and keyboard/screen-reader review | REQ-02 | unconfirmed |
| AC-03 | An input-byte hash is recorded before opening | Reader opens and filters the catalogue | After closing, input-byte hash is identical | Byte identity; no silent save | Before/after hash comparison in a selected runtime | REQ-03 | unconfirmed |

<a id="test-cases"></a>
## Test Cases

| Test ID | Criterion ID | Preconditions | Steps | Expected Result | Method / Test Source | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| TC-01 | AC-01 | Reader prototype and runtime selected | Open catalogue.json; filter review; inspect item IDs/titles | Only ITEM-01; exact match semantics | Planned fixture check; no implementation | unconfirmed |
| TC-02 | AC-02 | Prototype, invalid input and accessibility environment selected | Exercise unmatched category then invalid JSON; inspect states/focus | Distinct empty/error state; no partial malformed list | Planned behavior and assistive walkthrough | unconfirmed |
| TC-03 | AC-03 | Prototype exists; local source file can be hashed | Hash input; open/filter/close; hash again | Hashes identical | Planned file-integrity observation | unconfirmed |

<a id="test-runs"></a>
## Test Runs

| Run ID | Test ID | Result | Actual Observation | Revision | Environment | Executed UTC | Executor | Evidence ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RUN-01 | TC-01 | Not run | No reader prototype | unconfirmed | unconfirmed |  |  |  |
| RUN-02 | TC-02 | Blocked | No prototype or assistive test environment | unconfirmed | unconfirmed |  |  |  |
| RUN-03 | TC-03 | Not run | No reader prototype | unconfirmed | unconfirmed |  |  |  |

<a id="links"></a>
## Links

| Link ID | From Namespace | From Type | From ID | Relation | To Namespace | To Type | To ID | Rationale |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LINK-NEED-1 | pilot-checklist | requirement | REQ-01 | derived_from | pilot-checklist | source | SRC-BRIEF | Scenario intent |
| LINK-CASE-1 | pilot-checklist | test_case | TC-01 | verifies | pilot-checklist | criterion | AC-01 | Defined case; not an observed result |
| LINK-NEED-2 | pilot-checklist | requirement | REQ-02 | derived_from | pilot-checklist | source | SRC-BRIEF | Scenario intent |
| LINK-CASE-2 | pilot-checklist | test_case | TC-02 | verifies | pilot-checklist | criterion | AC-02 | Defined case; not an observed result |
| LINK-NEED-3 | pilot-checklist | requirement | REQ-03 | derived_from | pilot-checklist | source | SRC-BRIEF | Scenario intent |
| LINK-CASE-3 | pilot-checklist | test_case | TC-03 | verifies | pilot-checklist | criterion | AC-03 | Defined case; not an observed result |
| LINK-STORY | pilot-checklist | story | STORY-01 | satisfies | pilot-checklist | requirement | REQ-01 | Reader outcome |
| LINK-ADR | pilot-checklist | adr | ADR-01 | refers_to | pilot-checklist | requirement | REQ-03 | Design considers read-only boundary |
| LINK-MILE | pilot-checklist | milestone | MILE-01 | refers_to | pilot-checklist | outcome | OUT-01 | Learning output |
| LINK-RELEASE | pilot-checklist | release | REL-01 | depends_on | pilot-checklist | milestone | MILE-01 | Evidence before release |
