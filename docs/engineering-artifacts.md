# Engineering artifact content and sharing contract

Version: 0.1. Status: P01–P03 local implementation delivered for review.
This defines generic content and compatibility rules. The opt-in local
[tool and usage guide](skills/engineering-artifact-catalogue/P02.md) implements
validation, source adapters, audience exports and feedback reports.
[P03 focused skills](skills/engineering-artifact-catalogue/P03.md) add experimental
authoring/export guidance. Discovery, project pilots and integration remain future
slices; existing approval rules apply.
Start with the [blank Markdown template](skills/engineering-artifact-catalogue/TEMPLATE.md)
and [Excel companion](skills/engineering-artifact-catalogue/engineering-artifacts-template.xlsx).

## Source authority

Markdown is the primary authoring, review and version-history format for engineering
documentation. Excel is a derived view for an identified audience and baseline.
Generated JSON snapshots are intermediates, not another editable master.
Global skills/templates contain generic conventions and blank data; particular
project names, features, ownership, commitments and release facts belong in copies.

Authority is explicit per record/field group:

| Source kind | Owns | Documentation/export rule |
| --- | --- | --- |
| Authored Markdown | Needs, stories, criteria, ADR/design reasoning, planning, release communication and documented review history | Review/edit canonical Markdown; derive workbook views |
| Existing engine JSON | Native PRD/story/issue fields and readiness results managed by an existing store | Import read-only; preserve native IDs, values and source hashes; link rather than edit generated Markdown |
| Machine schema / diagram / test source | Executable contract, diagram source or actual observation | Link path/version and scoped evidence; summaries cannot replace source authority |
| Audience workbook | Reviewer feedback against a specified baseline | Archive and compare proposed feedback; never automatically update source content or approval |

Do not override authoritative engine fields with independently editable Markdown
copies. A Markdown record may add documented rationale or a proposed amendment,
clearly distinguished from imported facts. Updating engine data requires its own
authorized store workflow and reconciliation. A generated Markdown file is not
automatically an authored Markdown master. Unknown/conflicting ownership blocks
export of the affected record until resolved; no engine-wide migration is implied.

## Common identity, metadata and revision

Qualified record identity is the tuple `(namespace, record_type, record_id)`.
Revision is separate. Types distinguish a PRD aggregate from an individual
requirement and distinguish a case from a run. Native IDs are reused exactly;
new IDs are allocated once and persisted in source, never derived from row order,
title, statement text or a content hash. A displayed short ID is not sufficient
to join records across namespaces. Cross-namespace links require explicit intent
and both endpoint baselines; do not infer a namespace from repository names.

Required metadata for an instantiated document: `contract_version`, `namespace`,
`document_id`, `document_type`, `content_version`, `status`, `owner`, `requested_action`
and `source_authority`. Unknown owner is explicitly `unconfirmed`; acceptance or
approval cannot use it. Namespace/identity/authority cannot be blank in a real
export. Baseline revision and exact file hash live in the export source manifest,
so a document does not need to contain its own hash or current commit identifier.
Dates are actual observations or labelled forecasts, never invented defaults.

Use a short YAML frontmatter block for these scalar strings in authored documents.
Quote versions and date-like strings. Human narrative follows in Markdown;
record tables follow the blank template's exact headers. Parsing uses a safe YAML
loader, rejects duplicate metadata keys and unsupported tags, and never evaluates
code or interpolates values. Contract versions are explicit; unsupported versions
are reported rather than silently upgraded.

Record types are `prd`, `requirement`, `story`, `criterion`, `adr`, `design`,
`contract`, `outcome`, `milestone`, `task`, `release`, `release_note`, `test_case`,
`test_run`, `risk`, `review`, `evidence`, `guide`, `change`, `source`, `binding`,
`link` and `document`. Preserve native source statuses independently of local
document status; do not collapse them into a single readiness/approval enum.
If an imported source says `approved` but its review evidence is unavailable,
preserve that recorded source value with the evidence limitation. Do not represent
it as independently verified approval or permission to execute an external action.

Authored document status uses `draft`, `in_review`, `accepted`, `superseded` or
`withdrawn`; acceptance needs reviewer identity/role, source revision, decision,
time and evidence under the governing process. Existing engine statuses remain
exactly as stored. ADR decision status uses `Proposed`, `Accepted` or `Superseded`,
separately from the containing document's status. Preserve retained decisions and
their history. Test and release states have their own meanings below. Format/export
validation never advances any status.

For stable source locations, use explicit section anchors such as
`<a id="requirements"></a>` followed by a heading. Identify table records by
section anchor + record type + record ID; do not use a spreadsheet row number or
an automatic title slug as identity. Retain anchors on revisions; superseding a
record keeps the old ID/history. Markdown table values encode a literal pipe as
`&#124;` and an in-cell line break as `<br>`; full narratives stay outside cells.
P02 implements this narrow convention, not a general Markdown editor.

## Content profiles and proportional use

Select applicable records, not every possible document for every task. A tiny
mechanical correction can use a compact intent/change/check record. A meaningful
feature needs a source need, acceptance and verification approach. A consequential
choice needs retained decision rationale. Release planning needs scoped facts and
readiness/recovery evidence. Mark non-applicability with a reason; absence is not
success. The global template is a library, not a requirement to create every tab.

| Artifact | Minimum substantive content |
| --- | --- |
| PRD / requirements | Context/problem, users, outcome, scope/non-goals, source IDs, functional/quality/transition needs, rationale, priorities and uncertainty |
| Stories / criteria | Actor/goal/benefit and conversation; stable criterion IDs; observable context/event/outcome, agreed measure when applicable, verification method and owner |
| ADR | Context/drivers, plausible alternatives, decision/status, rationale, positive/negative consequences, actual authority evidence and supersession history |
| Design / UX / contracts | Relevant stakeholder concerns/views; behavior and look/feel when affected; quality/security/data/operations concerns; authoritative diagram/schema links and limits |
| Roadmap / milestones | Outcomes and measures, horizon/confidence, dependencies/review trigger; milestone output/acceptance and forecast/commitment evidence |
| Implementation plan | References/revisions to inspect, files/interfaces, bounded steps/dependencies, observable checks, applicable approvals and recovery |
| Release plan / assurance | Candidate scope/version/target, actual readiness evidence/gaps, rollout/recovery/support, compatibility/migration and review/authorization needs |
| Release notes | Delivered scope supported by source evidence, user impact, compatibility/migration, known limits and audience; planned scope stays in the plan |
| Testing / UAT | Defined cases and criteria, separately observed runs with revision/environment/time/executor/result/evidence; acceptance is its own actual review |
| Risks / reviews / history | Uncertainty, impact/options/owner; scoped reviewer decision/evidence; changed/superseded versions and reconsidered approvals |
| Guidance / handover | Audience/task, usable instructions and support/runbook links, tested revision, limits, remaining work and exact next action |

Test result values: `Not run`, `Blocked`, `Skipped`, `Fail`, `Pass`; cases do not
imply runs. Pass needs an actual scoped observation. Release facts separately
record candidate verification, merge, publication, deployment and acceptance;
one event does not imply the others. Release versioning uses the project's declared
scheme; no universal SemVer assumption. Proposed priority and agreed priority
remain separate; forecasts require uncertainty and agreement requires evidence.

## Existing-source binding registry

The compatibility adapter reads authoritative source objects and a persisted
Markdown `Source Bindings` table. Existing string lists are not modified merely
to add identity. The registry records binding ID, record type/ID, native owner
ID, source path/kind, field, locator, exact source-text SHA-256, whole-source
SHA-256 and binding status. A source index is a locator, never identity.
New authored records already have IDs; they need no legacy list registry unless
they bind to external fields. The registry itself is canonical, reviewed and
included in the source manifest whenever it affects the export.

Binding lifecycle:

1. **Bootstrap:** propose mappings from current source files; allocate persistent
   individual IDs once. Unique text within the declared owner/field may locate an
   entry. Duplicates and unexplained owner conflicts are unresolved, not guessed.
   Explicitly review/persist the mappings before authoritative export.
2. **Unchanged or reordered source:** reuse IDs only when the existing owner/field
   association and exact text resolve uniquely. Report the new locator/hash as a
   proposed registry refresh; exporting cannot silently write it. A changed source
   hash requires reconciliation even when semantic meaning appears unchanged.
3. **Edited text:** retain identity only through a reviewed association between
   the old record and new entry. Content hash changes are expected on edits; they
   do not allocate a new identity or prove semantic equivalence automatically.
4. **Duplicate text / regeneration:** do not match by index alone, deduplicate
   across owners or assume an unchanged generated native ID describes unchanged
   intent. Compare baseline ownership/content and require review of ambiguous
   moves or generator output. Export never invokes a generator.
5. **Removal/split/merge:** retire retained mappings with reasons; create explicit
   replacement/supersession relationships for new records. Never recycle IDs.

Use `proposed`, `resolved`, `unresolved`, `retired` binding states. Only resolved
bindings at the declared source hashes participate in a normal export. If a
reviewer explicitly requests a diagnostic draft, list unresolved rows as blockers,
identify them as unbound and prohibit approval/readiness claims.

The same text copied into PRD, story and issue lists does not prove it is the same
criterion. Keep owner-scoped identities unless an explicit source relationship
declares shared/referenced criteria. The adapter may preserve a copied string as
a summary while linking the canonical criterion; it must not merge identities
based only on string equality. Native issue/story lineage remains explicit.

## Links, evidence and integrity

Each link has its own ID and qualified source/target identity, relation and scoped
baseline. Supported starter relations are `derived_from`, `satisfies`, `verifies`,
`included_in`, `supersedes`, `depends_on` and `refers_to`. One relation per row;
many-to-many relationships use several rows. Reject duplicate IDs, unresolved
endpoints or conflicting endpoint versions. References omitted from an audience
projection still resolve through its full-source links and manifest.

Requiredness is profile-dependent. Validate actual values/IDs/links/authority,
source freshness, applicable provenance, table ranges and enum meanings.
Empty templates are allowed; an empty template cannot pass as delivered content.
Structural integrity and factual observations are distinguished from substantive
adequacy, independent review, user acceptance and operational authorization.
Existing presence checks are unchanged and provide only file-presence evidence.

## Audience export contract

Every real workbook includes Control, Artifact Register and Source Manifest plus
applicable data/review/traceability tables. The global blank template is an
unpopulated library; it has no real source-baseline, stakeholder or release facts.

The manifest records `export_id`, contract/template/profile versions, audience,
namespace, requested action, actual generation UTC, baseline reference and owner,
full-source links and explicit omission reasons. Each included source file has
path, source kind/authority, selector if applicable, revision and exact-byte
SHA-256. Include registry/diagram/schema/evidence files where they affect the view,
or identify remote reference revision/unavailable freshness honestly. Never invent
a remote hash or fetch unrequested external systems to fill it. Unknown freshness
is a visible limitation; material unavailable readiness evidence is a blocker.

Profile version 0.1 selects these views; optional means relevant to the scoped work,
not a license to conceal adverse facts:

| Audience | Main data tables | Additional applicable views | Retain in every applicable view |
| --- | --- | --- | --- |
| Business / product | Requirements, Stories, Acceptance, Roadmap, Milestones, Release Notes | Risks and Decisions; Test Runs/acceptance evidence; Guidance | Unconfirmed priority/forecasts, dependencies, acceptance gaps, planned versus delivered scope |
| Engineering | Requirements, Acceptance, ADRs, Design Views, UX and Contracts, Implementation Tasks | Source Bindings; Release Plan/Notes; Test Cases/Runs | Decision status, security/quality constraints, compatibility/test gaps and unresolved bindings |
| QA / UAT | Acceptance, Test Cases, Test Runs, Evidence, Reviews and Approvals | Requirements/Stories; Release Plan; Risks and Decisions | Not run/blocked/skipped/fail, candidate/environment, unresolved criteria, evidence/reviewer limits |
| Operations / release | Release Plan, Release Notes, Guidance and Handover, Evidence | UX and Contracts/migration; Risks and Decisions; readiness/Test Runs | Recovery/restore gaps, readiness blockers, limits, authorization/environment state |
| Executive / sponsor | Roadmap, Milestones, Risks and Decisions; Release Plan summary | Release Notes/outcome measures and decisions needed | Material blockers, uncertainty, forecasts versus commitments and deployed/accepted distinctions |

Selection specifies both tables and field-level summaries; a shared row's qualified
ID/source version always survives. Summaries label excerpts and link complete
source. Include Links/Evidence when needed to interpret claims. Control explicitly
lists omitted detailed views. Profiles may suppress irrelevant detail or private
fields after review, but cannot drop a material blocker: propagate it into the
selected risk/readiness summary. If safe projection is impossible, report that
limitation rather than exporting a falsely reassuring view.

## Freshness, feedback and conflicts

An export is a historical snapshot. A commit reference alone does not establish
freshness when source files are dirty; compare every manifest hash with current
declared source bytes, including the registry. A mismatch marks the view stale.
Record deleted/unavailable sources; never silently certify their old exports.
Refreshing an export creates a new ID/file and preserves the original.

Compare three inputs: the immutable original exported baseline, current canonical
source and the returned annotated workbook. Identify record/field changes by
qualified source identity and revision; added/deleted rows, headers, unknown
sheets and formulas must also be reported. Preserve unrecognized content; do not
resave unsupported complex workbook features merely to obtain feedback.

| Situation | Required handling |
| --- | --- |
| Comment-only feedback | Preserve annotated file; record proposal ID, source/export identity, reviewer and comment; review normally |
| Changed field, source unchanged | Report proposed old/new values; source mutation still requires an explicit reviewed action |
| Same field changed in current source and returned workbook | Flag conflict with all three values; no last-writer-wins or automatic resolution |
| Source changed elsewhere | Mark baseline stale; show unaffected-looking feedback as a proposal against an old revision; recheck meaning against current source |
| Two workbooks propose different values | Preserve both inputs and proposals; flag conflict; do not import either by timestamp |
| Added/deleted row or changed identity | Proposed source addition/removal, never silent insertion/deletion or ID reassignment |
| Agreement, acceptance or approval cell changed | Treat as reviewer feedback only; actual canonical decision needs governing review evidence and authority |

Reviewed proposals can be accepted/rejected/deferred/conflicted. Record reviewer,
reason, reconciled source revision and resulting change ID; archive annotations.
Generate new audience views only from the resulting reviewed baseline. This is
an explicit documentation review operation, not two-way master synchronization.

## Workbook and source handling

Use named tables, clear headers, stable ID columns, wrap/readable sizes, navigation,
text statuses and meaningful source links; no merged data cells or color-only
meaning. Preserve reviewer annotations; no-overwrite is the default. Define the
supported office/library feature scope before editing existing workbooks. Entry
dropdowns assist users but are not integrity or authorization enforcement.

All untrusted strings, including leading `=`, `+`, `-` or `@`, are literal text.
No macros or external calculation dependencies by default. If calculation is
specifically needed, use known expected results and actual recalculation evidence;
never equate cached values with a calculation performed by the writer library.
Keep real personal/secret data out of global templates/examples; export only
fields explicitly in scope, never dump raw legacy metadata indiscriminately.

Resolve source/output paths against declared roots; reject traversal and escaping
symlinks. Native IDs are data, never path components without validation. Reading
links is not permission to fetch, execute or publish. Output generation, registry
changes and source edits have separate authorization boundaries. No automatic
remote writes, deployment or model execution follows from artifact drafting.

## Examples, compatibility and verification

Complete synthetic examples: [tiny task](skills/engineering-artifact-catalogue/examples/tiny.md),
[feature/traceability](skills/engineering-artifact-catalogue/examples/feature.md),
[ADR/design](skills/engineering-artifact-catalogue/examples/design.md), and
[roadmap/release](skills/engineering-artifact-catalogue/examples/release.md).
They are illustrations, separate from blank assets; they name no real project or
domain feature and do not assert actual user approvals/test passes/releases.

[P01](skills/engineering-artifact-catalogue/P01.md) records exact inspected engine
fields and implementation instructions. [P02](skills/engineering-artifact-catalogue/P02.md)
records the opt-in tool, usage, persisted native/string IDs, binding reconciliation,
missing namespace/hash checks, audience blocker retention/omissions, three-way
feedback, literal text and immutable outputs. Existing store compatibility is
covered by the repository suite; export does not invoke engine generators.
The package's template renderer remains a separate blank/research-pack helper.

Contract changes need versioned documentation, updated neutral templates/examples,
compatibility review and appropriate tests/evals when executable behavior changes.
Do not migrate existing artifacts or approve a new contract version silently.
