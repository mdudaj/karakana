# Requirements template authoring guide

Content pack version: 0.1. Use the
[clean template](../assets/requirements-template.md) for a requested readable
specification and the [worked example](../assets/requirements-example.md) for
context. These narrative assets are not supported P02 structured-export inputs.
Keep the existing source/export contract when an exact-table export is requested.

## Selection and tailoring

Identify audience, governing source and applicable product/release. Replace each
`{{field}}` from evidence; keep authoring instructions in this guide. Record the
canonical source/baseline so the copy does not become a competing editable master.
Copy only applicable sections into the project artifact.

Keep purpose/scope, context/users, functional and quality requirements,
acceptance/verification and references. Include interfaces/data and unresolved
matters when present; delete empty sections. A small change can reference an
existing context or quality baseline and define the affected requirements only.
Add glossary, stories/journeys, migration/transition needs or detailed data and
traceability tables when readers need them. A story is useful context, not a
mandatory substitute for a requirement.

Title, document revision, actual date and product/release applicability describe
the artifact. Add owners/priorities when relevant or project-required. Canonical
export metadata remains governed by the existing contract; simplifying issued
presentation does not delete internal authority or review records.

## Statements and criteria

Retain stable requirement IDs on edits and update their revision and affected
criteria. Record one observable behavior or constraint per requirement, with a
relevant rationale/source and criterion/method reference. Use consistent mandatory
language; `shall` is a useful pattern, not a requirement for every explanatory
sentence. Avoid prescribing implementation details unless they are real constraints.

| Pattern | Review result |
| --- | --- |
| The system shall prevent a reader from viewing a record outside the reader's assigned programme scope. | Observable permission boundary; define list/direct access and revoked-scope criteria. |
| The system shall be fast and secure. | Needs workload, environment, measure and acceptance threshold; split unrelated claims. |
| We will arrange a meeting to agree the requirements. | Authoring activity; place in the working/review record rather than product requirements. |
| The system shall display a record to readers only after the required independent approval is recorded. | Valid product approval behavior when supported by the product requirements; define who may approve and the applicable states. |

Define criteria as conditions/event and expected outcome, with a method or test
reference. Cover relevant success, failure, permission and quality boundaries.
Keep criterion definition, test case and actual run separate. An expected result
does not justify `Pass`; a run needs revision/environment/executor/time/evidence.

An unknown measure remains an explicit open acceptance decision. State what it
blocks and the role/source that can resolve it. Do not substitute a convenient
number, owner, deadline or agreement. See the worked example's latency question.

## Standards and references

Use a short explanation plus exact editions and their relevant application.
Suggested wording when supported: “This specification uses a tailored approach
informed by ISO/IEC/IEEE 29148:2018. Quality requirements use ISO/IEC 25010:2023
as a reference, and documentation content is tailored with reference to
ISO/IEC/IEEE 15289:2019.” The
[NASA writing checklist](https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/)
is supplemental guidance. Identify actual contractually required standards and
obligations separately. Public summaries informed this pack; no full normative
conformity assessment or certification is claimed.

## Completion review

- Check scope, users and terms against actual sources; remove unresolved conflicts
  rather than blending them into an apparently agreed statement.
- Trace meaningful needs to requirements and criteria; check for unjustified
  features/tests as well as uncovered requirements.
- Check IDs, references, measures and permission/failure boundaries. Retain the
  limits of unresolved acceptance and changed baseline approvals.
- Read the complete artifact for useful technical content. Remove unfilled
  substitution fields, template instructions and meeting/reviewer logistics.
  Retain legitimate product audit/approval and operating requirements.
- Record actual checks performed and remaining gaps. Source-text instruction
  evals and structural integrity do not establish factual correctness or acceptance.
