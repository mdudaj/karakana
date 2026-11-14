# System-design template authoring guide

Content pack version: 0.1. Use the
[clean template](../assets/system-design-template.md) and
[worked example](../assets/system-design-example.md) for requested design work.
They are narrative assets, not supported P02 structured-export inputs. Retain
declared authority for existing schemas, diagram sources and native engine fields.

For explicitly requested mechanical checks of a completed standard or tailored pack, use
the [content checker](../../../docs/skills/engineering-artifact-catalogue/content-checks/README.md)
with an explicit context. It reports source-located errors/warnings and unresolved
gaps. Explicit source mappings and saved-report verification are supported;
verify recomputes raw manifests and assessments rather than trusting a saved pass. A blank template is a valid starter, not completed content. Keep
substantive review and actual acceptance separate from this check.

## Selection and tailoring

Start from the governing requirements and existing design. Define the affected
scope, audience and concerns before selecting views. Replace `{{fields}}` from
inspected evidence; keep authoring instructions in this guide. State canonical
source/baseline and product/release applicability where relevant.

A system design normally covers context, structure, runtime scenarios, data and
interfaces, security/quality, deployment/operations, decisions and verification.
A small change can reference current governing views and describe only affected
parts. Explain material omissions in the working record; omit empty sections.
Add detailed UX, migration/transition, schemas or component views when needed.

For UX changes, describe behavior and look/feel, states, copy, keyboard/assistive
interaction and the shared design-system patterns. A diagram is not enough to
specify user interaction. Domain and UX skills govern the actual stack.

## Views and contracts

For each view identify its purpose, boundary and stakeholder concern; explain the
diagram in text. Use consistent component, state and data names across views.
Keep editable diagram source with the document or link its authoritative revision.
Start with context/major components where useful; add detail to resolve concerns.

Walk through input/actor, responsible components, state/data transitions,
observable outcome and failure/recovery. Inspect real entry paths for an actual
application design: hiding a button does not establish server-side authorisation.
Describe interface inputs/outputs, validation, error semantics and compatibility
at the level the change needs; link executable contracts instead of duplicating
them as another editable master.

| Design statement | Review result |
| --- | --- |
| A server-side read policy applies current assignment and permission checks to both list and detail handlers. | Identifies responsibility and entry paths; inspect actual implementation and negative cases when delivering the application. |
| The diagram shows a secure portal. | Needs trust boundaries, failure behavior, concrete controls and verification references. |
| Response times satisfy the target. | Needs agreed measure and actual scoped run evidence; a proposed test is not an observed result. |
| The read policy requires the record's independent approval state. | Legitimate product rule when supported by requirements; distinguish product state from document acceptance. |

## Decisions and evidence

Summarise consequential choices and link full ADRs when needed. Reuse
[ADR guidance](adr.md): context/drivers, plausible alternatives, selection,
rationale, positive/negative consequences and actual decision status/authority.
Preserve superseded reasoning and link replacements. A proposed solution and an
accepted template structure do not prove acceptance of a real architecture.

Link requirements to design coverage and proposed checks. Retain unknown quality
thresholds and source/interface decisions explicitly. An example or planned check
does not constitute implementation, a test run or operational readiness.

## Standards and references

Suggested wording when supported: “This design uses a tailored approach informed
by ISO/IEC/IEEE 42010:2022. Quality concerns use ISO/IEC 25010:2023 as a reference;
documentation content is tailored with reference to ISO/IEC/IEEE 15289:2019.”
Give exact editions and their use. Applicable mandatory project obligations need
their own identified requirements and verification.

[arc42](https://arc42.org/overview/) informs content selection and
[C4](https://c4model.com/diagrams) informs diagram depth; these are practical
guidance, not ISO standards or mandatory diagram counts. Use original local text
and reference the source. Public summaries informed this pack; no clause-level
conformity or certification assessment was performed.

## Completion review

- Trace important requirements to responsibilities, scenarios and proposed checks.
- Reconcile names, boundaries, states and contracts across text and diagrams.
- Challenge failure, permission, integrity and recovery paths against actual
  sources when reviewing a real application design.
- Check quality measures, alternatives/consequences, unresolved facts and decision
  history. Keep planned checks distinct from executed evidence.
- Remove unfilled substitution fields and authoring/review logistics from the
  completed artifact; preserve genuine operating and product approval constraints.
- State actual review/verification limits. Structural checks and source-text evals
  do not demonstrate technical correctness, independent acceptance or deployment.
