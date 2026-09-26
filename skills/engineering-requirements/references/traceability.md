# Traceability, authority and revisions

Qualified identity is namespace/type/ID; revision is separate. Persist an ID once.
Do not allocate identity from title, current position, text hash or Excel row number.
Keep duplicate text across owners separate unless explicit source lineage establishes
its relationship. A content hash proves byte equality, not meaning or approval.

Build only useful typed edges: source -> requirement (`derived_from`), story ->
requirement (`satisfies`), test -> criterion (`verifies`), item -> release (`included_in`),
new -> old (`supersedes`) or dependency (`depends_on`). Declare namespaces and endpoints.
Retain unresolved/omitted endpoints as a gap; do not invent placeholder success.
P02 currently validates one explicit namespace bundle; cross-namespace baselines need
separate supported review and cannot be inferred from repository names.

Inspect native JSON IDs, fields and source hashes before importing. P02's Source
Bindings registry gives legacy string entries persistent IDs without modifying engine
schemas. New/reconciled mappings are proposed/unresolved until reviewed; changed file
hashes block normal export even if an old text match still appears. Edited/split/merged
intent requires reviewed association/supersession, not index-only guessing.

On a material edit: preserve ID/history, advance content revision, record reason and
impact, update affected links/verification, and reconsider previous acceptance for the
changed baseline. Retain prior exports/reviews as history. Do not carry approval from
an older or annotated workbook onto changed canonical content.

Check endpoint existence and coverage in both directions: needs without criteria/tests,
and tests/features without a justified need. No coverage percentage proves adequacy.
For field authority, native engine JSON and machine schema/diagram sources retain
ownership; Markdown adds rationale or explicitly proposed amendments. Conflicting or
unknown authority blocks export. Use [P02](../../../docs/skills/engineering-artifact-catalogue/P02.md),
the shared contract, and PLAN S01/S07/L02 as governing references.
