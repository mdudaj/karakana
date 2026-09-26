---
contract_version: '0.1'
namespace: pilot-checklist
document_id: DOC-DESIGN
document_type: document
content_version: '0.1'
status: draft
owner: unconfirmed
requested_action: review controlled synthetic pilot
source_authority: authored Markdown
---
# Pilot proposed decision and design views

This draft describes a fictional reader. The machine contract fixture remains
authoritative for its candidate syntax; prose does not alter it. ADR-01 is Proposed,
with no decision-owner acceptance or superseded real architecture.

<a id="context"></a>
## Context and drivers

The brief requires read-only local use and explicit invalid-input states. Drivers
are source integrity, understandable failures, and a bounded first implementation.
Stakeholders are a reader concerned with finding items and a maintainer concerned
with invalid data. No production trust boundary or security assurance is supplied.

<a id="alternatives"></a>
## Alternatives and consequences

Option A streams partially parsed items: lower startup work, but malformed input
could expose a misleading partial list. Option B parses and checks the complete
catalogue before displaying any items: simpler all-or-error reasoning, but holds
all items in memory. Option C uses a remote searchable store: suitable for shared
editing, but outside the offline/read-only scope and adds deployment/authentication.

Propose B for the scoped first slice. It supports distinct errors and byte-preserving
reads. Negative consequences: memory use grows with catalogue size; maximum workload
and latency thresholds require agreement before claiming performance. Reject A for
partial-list ambiguity and defer C because collaboration is expressly excluded.
Reconsider when a measured catalogue workload makes whole-file reading unsuitable.

<a id="decisions"></a>
## ADRs

| ADR ID | Title | Status | Decision Summary | Rationale Summary | Consequences Summary | Decision Owner | Source Artifact ID | Superseded By | Decision Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ADR-01 | Validate whole input before showing items | Proposed | Propose full parse/check then read-only filtering. | Explicit all-or-error behavior fits the scoped need. | Memory/workload limits remain unresolved; no partial display. | unconfirmed | DOC-DESIGN |  |  |

<a id="adr-sections"></a>
## ADR Source Sections

| ADR ID | Section | Sequence | Summary / Excerpt | Source Artifact ID | Source Section | Source Revision |
| --- | --- | --- | --- | --- | --- | --- |
| ADR-01 | Alternatives | 1 | Excerpt: streaming partial results; whole-input validation; remote store. | DOC-DESIGN | alternatives | 0.1 |
| ADR-01 | Consequences | 2 | Excerpt: whole-input memory cost; performance thresholds unconfirmed. | DOC-DESIGN | alternatives | 0.1 |

<a id="views"></a>
## Design Views

| Design ID | View ID | Stakeholder / Concern | Viewpoint / Scope | Elements / Interfaces | Scenario | Quality Constraint | Diagram / Schema Link | Source Artifact ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DESIGN-01 | VIEW-01 | reader / exact lookup and error clarity | Read-only interaction boundary | Local file -> parser/contract check -> filter -> item list | Open, filter, empty or invalid state | Input unchanged; no partial display for invalid data | catalogue.schema.json candidate-0.1 | ADR-01 |
| DESIGN-01 | VIEW-02 | maintainer / corruption and workload | Failure and data boundary | Validation errors and in-memory items | Reject malformed data before listing | Size and latency acceptance need a real workload | design.md#alternatives | ADR-01 |

<a id="contracts"></a>
## UX and Contracts

| Element ID | Behavior / States | Copy / Interaction | Accessibility | Shared Components / Tokens | Contract Link / Version | Examples / Constraints | Source Artifact ID |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CONTRACT-UX | Loading, items, empty and error states; no editable fields | Label Category; distinguish No items in this category from Cannot read checklist | Persistent labels, visible focus, keyboard filter, announced errors; not tested | Later implementation must reuse its actual shared design system; none selected in this fictional scenario | catalogue.schema.json / candidate-0.1 | No screenshot or implemented page claimed; read-only source | DESIGN-01 |

<a id="machine-sources"></a>
## Source Manifest

| Source ID | Source Kind | Path | Selector | Revision | SHA-256 | Authority | Full-Source Link |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MANIFEST-SCHEMA | Machine source | catalogue.schema.json |  | candidate-0.1 | 8e06fa19a78185e365fd5bc3fbc6566a6954d0813c19bc583adfe812e102bf46 | Machine source | catalogue.schema.json |
| MANIFEST-DATA | Machine source | catalogue.json |  | fixture-0.1 | 6d275a938bf00ed83c20b2926dff58fc9248d39168e320c0ca68facd9bdc8479 | Machine source | catalogue.json |
| MANIFEST-BRIEF | Authored Markdown | brief.md |  | pilot-0.1 | e7764b6a4c70bd76b27dcab48902fdafe8cb9e40f14ded01678588cb1fa5ade9 | Authored Markdown | brief.md |
