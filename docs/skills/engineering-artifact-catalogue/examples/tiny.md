---
contract_version: "0.1"
namespace: "example"
document_id: "DOC-001"
document_type: "change"
content_version: "0.1"
status: "draft"
owner: "unconfirmed"
requested_action: "review synthetic example"
source_authority: "authored Markdown"
---

# Synthetic tiny-task example

<a id="compact-change"></a>
## Intent, scope and verification

Intent: correct a spelling error in one documentation label. This is an
illustration, not a change to any project. Expected outcome: the label is correct
and its meaning is unchanged. Non-goals: change runtime behavior, rename IDs or
reopen architecture. Source: this explicitly synthetic scenario.

Record ID: CHG-001. Proposed before/after: “Reveiw” → “Review”.
Applicable artifacts: this compact change record and final handoff if carried out.
PRD, story, ADR, release plan and workbook export are not applicable: a mechanical
label correction has no new user behavior, data contract or release commitment.

Verification plan: inspect the one-line diff, ensure only the intended label
changes, and run the relevant documentation check. Result: **Not run**, because
this file illustrates the shape rather than executing that hypothetical change.
No automated application test is needed for a label-only correction.

Review: unconfirmed; no approval implied. Recovery: restore the prior label through
a reviewed patch if the correction changes intended meaning. Remaining action:
perform the actual small correction only within its requested scope. Sharing can
use the compact Markdown record; no full workbook or binding registry is required.
