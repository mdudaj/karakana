# ADR 0005: Markdown engineering content and stable source bindings

Status: P02 implementation direction authorized by requester, 2026-09-26;
local implementation awaits independent review/integration.
Scope: global generic engineering documentation; existing engine schemas and
stores unchanged. P01 proposed this design; the requester subsequently agreed
to deliver P02. That authorization is not independent review or release approval.

## Context and decision drivers

Engineering artifacts must be reviewable/versioned in Markdown while supporting
audience Excel views. Existing requirements loaders own JSON and regenerate
Markdown. Individual requirement/criterion strings lack IDs; story/issue
generators allocate IDs from enumeration. Workbook rows, titles or content hashes
cannot provide lasting identity across source edits. Exporting must preserve
legacy consumers and must not create approvals or project-specific global assets.

## Options

| Option | Benefits | Costs / failure modes |
| --- | --- | --- |
| Workbook is the content master | Familiar review interface | Binary history, conflicting audience copies and source drift; conflicts with accepted Markdown-primary direction |
| Replace engine schemas with a Markdown-only store | One authoring representation | Breaks existing consumers, requires migration and changes readiness/store behavior beyond P01 |
| Add IDs directly to every legacy string/schema now | Structured references in engine | Unknown fields fail current constructors; criteria/string consumers need coordinated migration |
| Read engine-owned sources and persist stable associations in a separate Markdown registry | Preserves current IDs/loaders and Markdown documentation authority; supports reviewable reconciliation | Needs explicit ownership, matching and staleness rules; ambiguous source changes require review |

## Decision for the authorized P02 slice

Use the final option. The [content contract](../engineering-artifacts.md) owns
human documentation format and identity/revision/export rules. Engine JSON and
machine schemas remain authoritative for their own fields; Markdown records
identify those exceptions. Generated engine Markdown is not hand-edited as a
master. The global blank template contains no populated project data.

Reuse PRD/story/issue IDs exactly. Define qualified identity as a namespace/type/ID
tuple, separate from revision. Persist assigned individual requirement/criterion
IDs and source associations in a Markdown registry. Source index/text hash helps
locate a list entry but never becomes its ID. Bootstrap ambiguity, edits and
regeneration need reviewed mappings; exporting is read-only with respect to the
engine and source registry. Duplicate text across owners is not automatic identity.

Generate audience workbooks as new derived outputs with all source-file hashes,
baseline revision, profile/version, generation time, omissions and full-source
links. Review feedback is compared against the original baseline and current
source; it is proposed input, never an automatic source or approval update.

## Consequences and limits

Existing schemas/store/readiness/generators stay compatible. Markdown review and
audience selection are explicit; no second state machine or approval framework
is introduced. The registry adds a maintained artifact, tailored away for tiny
work with no legacy list binding. Multiple authoritative fields require a clear
authority map and hashes for every relevant source; one aggregate revision is
insufficient when the underlying working tree changes.

P02 implements an opt-in local adapter, exporter and feedback reporter; see its
[delivery and usage record](../skills/engineering-artifact-catalogue/P02.md).
Functional tests cover binding persistence, stale/conflict detection and legacy
compatibility. Catalogue skills, project pilots and rollout remain outstanding.
Semantics still require substantive review.
Project-specific authorization and schema migrations remain separate decisions.

## Verification and recovery

P01 inspects actual schemas/store/generators, exercises existing models and store
in an isolated compatibility probe, validates example references and template
parity, and records limitations. P02 records executable coverage and local office
checks in its delivery record. Revise this ADR if evidence changes; preserve its
history. Revert the opt-in module/dependency/docs through a reviewed change if
rejected; no engine migration,
production deployment or deletion of annotated exports is necessary.

References: [P01 evidence/mapping](../skills/engineering-artifact-catalogue/P01.md),
[research](../skills/engineering-artifact-catalogue/RESEARCH.md),
[existing lifecycle](../engineering-process.md).
