---
contract_version: '0.1'
namespace: example
document_id: DOC-D01
document_type: document
content_version: '0.1'
status: draft
owner: unconfirmed
requested_action: review synthetic illustration
source_authority: authored Markdown
---
# Synthetic decision and design example

An original neutral illustration. Proposed choices below are not actual authority
or evidence of a real release. The containing document remains draft.

<a id="decision-context"></a>
## Context and drivers

A shared view can drift from the editable documentation. Reviewers need readable
history, one declared field authority and meaningful source provenance.

<a id="alternatives"></a>
## Alternatives and consequences

A workbook master simplifies familiar cell editing but makes separate audience copies
compete and history harder to inspect. Replacing every native store with Markdown
would simplify one representation but require unsupported migration. The proposed
choice is versioned Markdown documentation with explicit native-source exceptions
and derived views. It preserves history but adds baseline/feedback maintenance.
No existing accepted decision is replaced by this illustration.

<a id="decisions"></a>
## ADRs

| ADR ID | Title | Status | Decision Summary | Rationale Summary | Consequences Summary | Decision Owner | Source Artifact ID | Superseded By | Decision Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ADR-D01 | Retain one declared documentation authority | Proposed | Use Markdown documentation and explicit native-source ownership. | Reviewable history without competing audience masters. | Derived views need freshness and feedback reconciliation. | unconfirmed | DOC-D01 |  |  |

<a id="source-sections"></a>
## ADR Source Sections

| ADR ID | Section | Sequence | Summary / Excerpt | Source Artifact ID | Source Section | Source Revision |
| --- | --- | --- | --- | --- | --- | --- |
| ADR-D01 | Alternatives | 1 | Summary only: workbook master; native-store replacement; explicit authority and derived views. | DOC-D01 | alternatives | 0.1 |

<a id="views"></a>
## Design Views

| Design ID | View ID | Stakeholder / Concern | Viewpoint / Scope | Elements / Interfaces | Scenario | Quality Constraint | Diagram / Schema Link | Source Artifact ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DESIGN-D01 | VIEW-D01 | reader / complete source context | Sharing boundary | Canonical source -> audience view -> proposed feedback | Source changes after sharing | Never silently replace authority or approval. | design.md#sharing-scenario | ADR-D01 |

<a id="contracts"></a>
## UX and Contracts

| Element ID | Behavior / States | Copy / Interaction | Accessibility | Shared Components / Tokens | Contract Link / Version | Examples / Constraints | Source Artifact ID |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CONTRACT-D01 | Draft view shows source identity, baseline and known limits. | Use explicit draft and feedback labels. | Source links need meaningful labels; actual assistive review unperformed. | Reuse the project shared system; none selected in this fixture. | Unconfirmed machine contract; no schema replacement | Example view is illustrative, not operational evidence. | DESIGN-D01 |

<a id="sharing-scenario"></a>
## Sharing and failure scenario

A source author creates a derived view; a reviewer proposes changes. If current source
has changed, the comparison reports staleness/conflicts. Source approval stays with
its governing process. This describes intended behavior, not an executed observation.
