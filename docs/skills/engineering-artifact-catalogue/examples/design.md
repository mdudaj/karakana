---
contract_version: "0.1"
namespace: "example"
document_id: "ADR-001"
document_type: "adr"
content_version: "0.1"
status: "draft"
owner: "unconfirmed"
requested_action: "review synthetic example"
source_authority: "authored Markdown"
---

# Synthetic ADR and design example

<a id="adr-001"></a>
## ADR-001: preserve source identity in a shared view

Decision status: Proposed. Context: a source owner and a reviewer need to discuss
the same record while using different views. Physical table positions can change;
the complete rationale must remain accessible. Drivers: stable identity, readable
sharing, explicit source authority and retained review history. Source: the generic
documentation scenario in [feature.md](feature.md#fixture-intent), not a real project.

| Alternative | Benefit | Consequence |
| --- | --- | --- |
| Identify by physical row | Easy initial reference | Sorting changes what the reference denotes |
| Identify by statement hash | Detects content differences | An edit changes identity; duplicate text is ambiguous |
| Persist record ID and link full source | Survives sort/edit and exposes context | Requires an explicit registry for older sources lacking IDs |

Proposed decision: persist qualified IDs and source-version links. Rationale:
identity describes the record, while hashes describe a source observation.
Positive consequences: viewers can resolve context; feedback can refer to a known
baseline. Negative consequences: a registry needs maintenance and ambiguous
matches require review. Rejected alternatives remain visible above.

Acceptance/decision owner: unconfirmed. Evidence: none; no decision is accepted.
Supersession: none. If replaced later, retain ADR-001 and link the successor.

<a id="design-views"></a>
## Design Views

| Design ID | View ID | Stakeholder / Concern | Viewpoint / Scope | Elements / Interfaces | Scenario | Quality Constraint | Diagram / Schema Link | Source Artifact ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DESIGN-001 | VIEW-001 | Source owner: editable authority | Context | Canonical source, binding registry, derived view, feedback report | Reviewer opens the full source from a summary | No competing editable master | [Source authority](../../../engineering-artifacts.md#source-authority) | ADR-001 |
| DESIGN-001 | VIEW-002 | Reviewer: baseline integrity | Runtime | Read source → check IDs/hashes → project audience view → archive feedback | Source changes before feedback returns | Stale baseline visibly reported; no silent import | [Feedback contract](../../../engineering-artifacts.md#freshness-feedback-and-conflicts) | ADR-001 |

These text views are the complete relevant description for this example; no
deployment diagram is required because no runtime system is being changed.
Authoritative executable schema, production topology and environment are not
applicable to this synthetic documentation choice. Future tool design will add
them if its actual scope needs them.

<a id="quality-and-review"></a>
## Quality, UX, security and verification

Behavior/look and feel: full Markdown reasoning; workbook summaries have labelled
source links, text status, stable ID columns, useful wrapping and no merged data
cells. A reader can see proposed status without relying on color. Security/data:
all example values are synthetic, formula-like strings stay literal, and source
links are not executable actions. Performance targets are unconfirmed rather
than invented; this example has no measurable runtime requirement.

Verification plan: sort a future fixture, edit a statement and return stale
feedback; IDs persist or ambiguity is reported, and the full ADR remains linked.
Result: **Not run**; future adapter implementation is needed. Review/approval:
unconfirmed. Main risk: an audience summary omits the reason or blocker; mitigate
with explicit excerpt labels/full-source links. Recovery: preserve prior source
and export, review corrected mapping, generate a new view. Next action: review
the proposed choice; this example performs no implementation or acceptance.
