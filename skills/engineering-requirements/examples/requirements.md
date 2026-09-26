---
contract_version: '0.1'
namespace: example
document_id: DOC-R01
document_type: document
content_version: '0.1'
status: draft
owner: unconfirmed
requested_action: review synthetic illustration
source_authority: authored Markdown
---
# Synthetic requirements, stories and verification example

This is an original domain-neutral illustration, not project scope or stakeholder
agreement. The desired outcome is understandable source context in a shared record.
Owners, priorities and acceptance are unconfirmed. No real test was performed.

<a id="context"></a>
## Problem and scope

A reader should be able to inspect the origin and limitations of a shared record.
Scope: visible source identity and complete-context reference. Non-goals: changing
sources, publishing a release or approving any content. Open question: which
recipient environment must resolve the link? That affects acceptance but does not
justify an invented application or passing result.

<a id="sources"></a>
## Sources

| Source ID | Publisher / Owner | URI / Path | Edition / Revision | Inspected Date | Supported Claim | Limitations |
| --- | --- | --- | --- | --- | --- | --- |
| SRC-R01 | synthetic scenario | requirements.md#context | 0.1 | illustrative; not an actual interview | A reader needs source context | Not stakeholder evidence |

<a id="requirements"></a>
## Requirements

| Requirement ID | Class | Statement | Rationale | Source ID | Proposed Priority | Agreed Priority | Decision Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| REQ-R01 | Stakeholder | A shared record displays its stable source ID and complete-source link. | Readers need to inspect context and limitations. | SRC-R01 | unconfirmed | unconfirmed |  | unconfirmed | draft |

<a id="stories"></a>
## Stories

| Story ID | Actor | Goal | Benefit | Conversation / Scope | Dependency IDs | Estimate / Basis | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| STORY-R01 | reader | locate a shared record source | I can inspect its complete context | Recipient link environment is unresolved. | REQ-R01 | unconfirmed | unconfirmed | draft |

<a id="acceptance"></a>
## Acceptance

| Criterion ID | Context | Event | Expected Outcome | Measure / Threshold | Verification Method | Source Artifact ID | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AC-R01 | A record has a declared source baseline | A reader opens its shared view | Stable source ID and complete-source link are visible | Both present; link-resolution environment remains an open decision | Inspect source/view pair, then recipient walkthrough | STORY-R01 | unconfirmed |

<a id="tests"></a>
## Test Cases

| Test ID | Criterion ID | Preconditions | Steps | Expected Result | Method / Test Source | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| TC-R01 | AC-R01 | Source and intended recipient environment established | Open view; inspect ID/link; resolve source in that environment | ID matches source; complete context opens | Planned walkthrough; no run yet | unconfirmed |

<a id="runs"></a>
## Test Runs

| Run ID | Test ID | Result | Actual Observation | Revision | Environment | Executed UTC | Executor | Evidence ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RUN-R01 | TC-R01 | Blocked | Recipient environment not selected | 0.1 | unconfirmed |  |  |  |

<a id="links"></a>
## Links

| Link ID | From Namespace | From Type | From ID | Relation | To Namespace | To Type | To ID | Rationale |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LINK-R01 | example | requirement | REQ-R01 | derived_from | example | source | SRC-R01 | Illustrative origin |
| LINK-R02 | example | story | STORY-R01 | satisfies | example | requirement | REQ-R01 | Reader outcome |
| LINK-R03 | example | criterion | AC-R01 | refers_to | example | story | STORY-R01 | Criterion scope |
| LINK-R04 | example | test_case | TC-R01 | verifies | example | criterion | AC-R01 | Planned verification, not observed pass |

An agreed link environment should update the criterion revision and test case;
retain IDs and reconsider prior review. This source currently claims no acceptance.
