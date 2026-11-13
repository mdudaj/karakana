# Programme record portal — requirements

| Document information | Value |
| --- | --- |
| Document ID | EX-REQ |
| Revision | 0.1 |
| Date | 2026-11-13 |
| Product / release applicability | Synthetic programme record portal; no real product release |
| Canonical source / baseline | This worked example, revision 0.1 |

## Standards and references

This synthetic specification uses a tailored approach informed by
ISO/IEC/IEEE 29148:2018. Quality concerns use ISO/IEC 25010:2023 as a reference;
documentation content is tailored with reference to ISO/IEC/IEEE 15289:2019.
These references inform the example; no conformity assessment was performed.

| Reference | Edition | Application |
| --- | --- | --- |
| [Requirements engineering](https://www.iso.org/standard/72089.html) | ISO/IEC/IEEE 29148:2018 | Requirement content and verifiable statements |
| [Product quality model](https://www.iso.org/standard/78176.html) | ISO/IEC 25010:2023 | Applicable quality concerns and measures |
| [Documentation content](https://www.iso.org/standard/74909.html) | ISO/IEC/IEEE 15289:2019 | Tailored information content |

## Purpose and scope

Programme readers need to consult approved records within their assigned scope.
The intended outcome is consistent permitted access through lists and direct
record requests, with no disclosure of restricted record details.

Scope: record-list and record-detail reading after authentication. An external
programme-review process supplies each record's approval state.

Exclusions: record submission, approval execution, exports, attachments and
account provisioning. The scenario and rules are illustrative product inputs.

## Context and users

A reader has an authenticated identity, read permission and zero or more current
programme assignments. An identity adapter supplies the identity; the portal owns
current programme assignments and reads record approval state. Product terminology
uses “approved” for the product record state, independently of document review.

## Functional requirements

| ID | Requirement | Rationale / source | Acceptance criteria |
| --- | --- | --- | --- |
| REQ-01 | The portal shall permit record reading only when the reader has read permission and a current assignment to the record's programme. | Scoped reading outcome in Purpose and scope | AC-01, AC-02 |
| REQ-02 | The portal shall display records to readers only when the programme-review process marks them approved. | Programme-review dependency in Context and users | AC-03 |
| REQ-03 | The portal shall apply removal of a programme assignment to the next application request after that removal is committed. | Current-assignment rule in Context and users | AC-04 |
| REQ-04 | The portal shall deny record reading when it cannot establish the required identity, permission or current assignment. | Scope cannot be established safely during dependency failure | AC-05 |

## Quality requirements and constraints

| ID | Requirement / constraint | Conditions and measure | Verification reference |
| --- | --- | --- | --- |
| REQ-05 | A denied response shall omit record contents and restricted programme details. | Denied list/detail and dependency-failure responses; inspect body, headers and exposed diagnostics | AC-02, AC-05 |
| REQ-06 | The record list shall satisfy the agreed response-time target under the selected workload and environment. | Target percentile, duration, workload and environment are unresolved in Q-01 | AC-06; acceptance blocked by Q-01 |

## Interfaces and data

The portal consumes an authenticated subject ID and uses its own assignment and
permission records. Each programme record has a stable ID, programme ID and
approval state. The record read service evaluates both permission and assignment;
approval state further limits reader-visible records. No API/schema implementation
exists for this illustrative scenario. Deployment-specific identity and error
contracts must be established before real integration.

## Acceptance and verification

| Criterion ID | Requirement ID | Conditions / event | Expected outcome | Verification method |
| --- | --- | --- | --- | --- |
| AC-01 | REQ-01 | Reader has permission and assignment; approved matching record is listed/opened | Matching record is accessible through both paths | Defined integration cases for list and direct detail |
| AC-02 | REQ-01, REQ-05 | Reader lacks permission or matching assignment and requests list/detail | Record is omitted or access denied without restricted details | Defined positive/negative scope matrix and response inspection |
| AC-03 | REQ-02 | Matching assigned record is pending approval | Record is absent from reader results and direct reading is denied | Defined state-boundary cases |
| AC-04 | REQ-03 | Assignment removal commits before the next request | List/detail applies the removed assignment on that request | Defined sequential revocation case |
| AC-05 | REQ-04, REQ-05 | Identity/permission/assignment cannot be established | Reading is denied without restricted details | Defined dependency-failure cases and diagnostic inspection |
| AC-06 | REQ-06 | Agreed workload/environment is exercised | Agreed response-time target is met | Proposed measured run after Q-01 resolution; not executed |

## Unresolved matters

| ID | Unresolved fact / assumption | Effect on acceptance | Resolution source / role |
| --- | --- | --- | --- |
| Q-01 | Response-time percentile/target, workload and representative environment | REQ-06 acceptance cannot be determined | Product and operations roles must select and document the measure |
| Q-02 | Actual identity adapter and deployment-specific error/diagnostic contract | Real integration and disclosure review cannot be completed | Identity/interface sources and operating constraints |

The cases above define expected outcomes. No application was implemented and no
test runs or product acceptance are recorded by this example.
