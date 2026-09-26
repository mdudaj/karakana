---
contract_version: "0.1"
namespace: "example"
document_id: "DOC-002"
document_type: "document"
content_version: "0.1"
status: "draft"
owner: "unconfirmed"
requested_action: "review synthetic example"
source_authority: "authored Markdown with explicitly linked engine-owned fields"
---

# Synthetic feature and source-binding example

This is a domain-neutral documentation illustration, not a product feature or
project draft. Namespace `example` is an explicit fixture namespace, not a
project inferred from a repository. JSON fixtures intentionally have no project;
a real adapter must ask the caller to confirm the namespace before exporting.
Engine-owned values below are read-only references; narrative and binding choices
are authored Markdown. No generated source files are edited by this example. Native identity, actor/goal
and criterion strings belong to engine JSON; local story/task draft status and
review/implementation narrative are authored Markdown, not invented engine fields.

<a id="fixture-intent"></a>
## Context and scope

A reviewer needs to inspect the origin of a shared record. The synthetic source
contains one requirement, one story and one issue, each with its own source-owned
identity. Outcome: source identity/link survives sharing. Non-goals: real product
scope, actual user acceptance, publishing, deployment or source synchronization.

<a id="artifact-register"></a>
## Artifact Register

| Artifact ID | Type | Title | Status | Owner | Markdown Path | Source Section | Source Revision | Source SHA-256 | Source Authority | Supersedes ID | Machine Source Link |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| req-example | prd | Generic source sharing fixture | draft | unconfirmed | feature.md | fixture-intent | fixture-content-0.1 | 128185bb0a335a024c7e7ee42bb0f7b44d0d63633a714e97d6a91e873dbcdf8e | Engine JSON native fields; Markdown narrative/local status |  | engine-fixture/prd.json |
| req-example-story-1 | story | Review a traceable source record | draft | unconfirmed | feature.md | stories | fixture-content-0.1 | e7c55d66be10da881144c8f67d78fd17232ecd62f2b2789990af200546d34ece | Engine JSON native fields; Markdown narrative/local status |  | engine-fixture/stories.json |
| req-example-issue-1 | task | Synthetic draft only | draft | unconfirmed | feature.md | implementation-tasks | fixture-content-0.1 | 838665893e6f54e27ec8a7f3f6df4a5612db0b445c6f98f768aa14c40ccd2a1a | Engine JSON native fields; Markdown narrative/local status |  | engine-fixture/issues.json |

<a id="requirements"></a>
## Requirements

| Requirement ID | Class | Statement | Rationale | Source ID | Proposed Priority | Agreed Priority | Decision Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| REQ-001 | Stakeholder | The shared view includes the source record ID and full-source link. | Traceability needs survive audience sharing. | SRC-001 | unconfirmed | unconfirmed | none | unconfirmed | draft |

<a id="stories"></a>
## Stories

| Story ID | Actor | Goal | Benefit | Conversation / Scope | Dependency IDs | Estimate / Basis | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| req-example-story-1 | reviewer | a source ID and full-source link in the shared view | I can inspect its complete context | Synthetic source values; open question: target office application is unconfirmed. | REQ-001 | unconfirmed | unconfirmed | draft |

<a id="acceptance"></a>
## Acceptance

| Criterion ID | Context | Event | Expected Outcome | Measure / Threshold | Verification Method | Source Artifact ID | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AC-001 | Identified source record | View is shared | ID and full-source link are present | Both fields present and resolve to the declared source | Inspect source/export pair | req-example | unconfirmed |
| AC-002 | Identified source record | View is shared | ID and full-source link are present | Same text, separate story-owner association | Inspect story export | req-example-story-1 | unconfirmed |
| AC-003 | Identified source record | View is shared | ID and full-source link are present | Same text, separate issue-owner association | Inspect issue export | req-example-issue-1 | unconfirmed |

The three imported criterion strings are identical. Their IDs are deliberately
owner-scoped. Explicit `derived_from` links record lineage; text equality does
not merge them. The chosen resolved bindings below are synthetic illustration,
not an actual stakeholder review or proof that adapter code has run.

<a id="source-bindings"></a>
## Source Bindings

| Binding ID | Record Type | Record ID | Native Owner ID | Source Path | Source Kind | Source Field | Source Locator | Source Text SHA-256 | Source File SHA-256 | Binding Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BIND-001 | requirement | REQ-001 | req-example | engine-fixture/prd.json | Engine JSON | functional_requirements | [0] | 6d655a2bc9ea27074dd1572d639f53e82d5de8105a0b67e36e402d899d851e1e | 128185bb0a335a024c7e7ee42bb0f7b44d0d63633a714e97d6a91e873dbcdf8e | resolved |
| BIND-002 | criterion | AC-001 | req-example | engine-fixture/prd.json | Engine JSON | standards_spec.acceptance_criteria | [0] | 76fbbe7a94d544cb1ab5ff4ff8361dfa6e16876b0d0a75bee3c5347ef7c59a0a | 128185bb0a335a024c7e7ee42bb0f7b44d0d63633a714e97d6a91e873dbcdf8e | resolved |
| BIND-003 | criterion | AC-002 | req-example-story-1 | engine-fixture/stories.json | Engine JSON | acceptance_criteria | owner=req-example-story-1; [0] | 76fbbe7a94d544cb1ab5ff4ff8361dfa6e16876b0d0a75bee3c5347ef7c59a0a | e7c55d66be10da881144c8f67d78fd17232ecd62f2b2789990af200546d34ece | resolved |
| BIND-004 | criterion | AC-003 | req-example-issue-1 | engine-fixture/issues.json | Engine JSON | acceptance_criteria | owner=req-example-issue-1; [0] | 76fbbe7a94d544cb1ab5ff4ff8361dfa6e16876b0d0a75bee3c5347ef7c59a0a | 838665893e6f54e27ec8a7f3f6df4a5612db0b445c6f98f768aa14c40ccd2a1a | resolved |

<a id="links"></a>
## Links

| Link ID | From Namespace | From Type | From ID | Relation | To Namespace | To Type | To ID | Rationale |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LINK-001 | example | requirement | REQ-001 | derived_from | example | source | SRC-001 | Synthetic source need |
| LINK-002 | example | story | req-example-story-1 | satisfies | example | requirement | REQ-001 | User outcome |
| LINK-003 | example | criterion | AC-002 | derived_from | example | criterion | AC-001 | Explicit owner-scoped copy |
| LINK-004 | example | criterion | AC-003 | derived_from | example | criterion | AC-002 | Explicit issue lineage |
| LINK-005 | example | test_case | TC-001 | verifies | example | criterion | AC-001 | Source ID/link check |

<a id="sources"></a>
## Sources

| Source ID | Publisher / Owner | URI / Path | Edition / Revision | Inspected Date | Supported Claim | Limitations |
| --- | --- | --- | --- | --- | --- | --- |
| SRC-001 | synthetic fixture | feature.md#fixture-intent | fixture-content-0.1 | synthetic scenario | Reviewer needs traceable context | Not stakeholder evidence; no real project facts |

<a id="test-cases"></a>
## Test Cases

| Test ID | Criterion ID | Preconditions | Steps | Expected Result | Method / Test Source | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| TC-001 | AC-001 | Future adapter exists; source and registry hashes validated | Generate a view; inspect ID/link against source | Both fields match the declared baseline | Future isolated source/export fixture | unconfirmed |

<a id="test-runs"></a>
## Test Runs

| Run ID | Test ID | Result | Actual Observation | Revision | Environment | Executed UTC | Executor | Evidence ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RUN-001 | TC-001 | Not run | Adapter is not implemented in P01 | fixture-content-0.1 | not executed |  |  |  |

<a id="implementation-tasks"></a>
## Implementation Tasks

| Task ID | Inspect References / Revision | Files / Interfaces | Implementation Steps | Check / Expected Result | Dependencies | Owner | Approvals / Recovery | Source Artifact ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| req-example-issue-1 | Engine fixture and generic contract 0.1 | Future adapter read/export boundary | Preserve native IDs; reconcile binding proposals; export source ID/link | Future TC-001; no engine writes | P02 implementation and reviewed bindings | unconfirmed | Review before integration; preserve prior exports | req-example |

<a id="binding-change-cases"></a>
## Binding change cases and sharing

Moving the unique requirement to another list position retains `REQ-001` only
through a reviewed locator/hash refresh. Changing its text requires a reviewed
old/new association. Adding identical text leaves matching unresolved; regenerating
stories/issues is never an export step. Missing namespace cannot be inferred.

Business view includes need/story/criterion and unconfirmed priority. Engineering
also sees native ownership/bindings. QA sees TC-001 and Not run. All views declare
source baselines and limitations; none imply completed delivery or acceptance.
