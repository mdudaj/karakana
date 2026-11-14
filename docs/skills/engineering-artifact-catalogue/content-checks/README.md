# Opt-in narrative content checks

Explicitly check the standard or tailored **requirements and system-design narrative
profiles**. Results separate mechanical completeness, review warnings and unresolved
acceptance items. A mechanical pass never establishes factual truth, standards
conformity, product readiness, independent review or acceptance.

This is separate from [P02](../P02.md): exact-table validation, native bindings,
workbook exports and feedback retain their contracts. Narrative checking does not
add P02 export support. No planner, hook, skill selection or protocol runs it automatically.

## Explicit task preparation (S1)

`karakana docs content prepare` prepares a prompt and task result from an explicit
request. It does not draft product documents, check content, run a model, load a
handoff or activate a policy. Text is default; JSON stdout contains one result.

```bash
karakana docs content prepare --request docs/skills/engineering-artifact-catalogue/content-checks/prepare-example.json
karakana docs content prepare --request docs/skills/engineering-artifact-catalogue/content-checks/prepare-example.json --format json
```

The [example request](prepare-example.json) is an illustrative instruction with no
product facts or acceptance. Adapt task/action/audience/types/scope/revision and
selected resources to the real task. A request must declare request_version0.1,
project, skill, task, resources, use_project_defaults and nullable context. See the
[accepted request/policy/result contracts](../../../research/2026-11-14-task-time-content-design.md).
All paths except --root are root-relative. Selected resources are literal local
inputs, not recursively followed links; examples remain labelled synthetic. An
empty resource list is valid and leaves recommendations unselected. Checkout
skills/memory/assets must exist when required; the wheel does not contain them.
Preparation works without the optional content parser.

The prepared prompt preserves explicit action, task text, audience, scope and
revision, including when a custom planner template omits task/output fields.
Author/review/inquiry requests are not silently converted to implementation plans.

Only the fixed optional `docs/content-policy.json` is considered. Project defaults
require `use_project_defaults: true`; task overrides are recorded. Declared locks
require an identical explicit selection, and cannot be waived by a command flag.
Absent policy is recorded; no policy file is installed or activated by this feature.
Prose instructions and scoped owner authority remain subject to substantive review.

Optional context0.1/0.2 selects profiles/versions through the existing M2 contract.
Preparation validates declarations only: it does not read document sources or
assess content. Sources may not exist yet; unsafe declarations or unsupported
formats/profiles are refused, with no conversion or fallback. Requests cannot
filter a context's document/profile types out of coverage.

Successful calls create a fresh `.karakana/document-tasks/<run-id>/` with
`prompt.md` and `result.json`. --output can choose another fresh directory under
.karakana/; existing directories/files are refused. Inputs are captured/hashed
and rechecked for bytes, target and presence drift, along with wrapper code.
Limits:32 physical inputs,2MB per input,16MB total,128KB per JSON configuration;
result JSON is at most2MB. Failures preserve sources/old outputs; nonempty partial
bundles remain incomplete evidence, never silently overwritten or accepted.

Exit0 means the prompt was prepared, not product readiness. Content report is null;
completeness/readiness/acceptance/saved verification remain not assessed. Exit2
means refusal or I/O/drift failure, with safe located corrections. CLI syntax
errors use stderr with empty stdout; valid JSON-mode invocations return typed JSON
even for domain failures. No new protocol-stage gate is introduced. Explicit
task-time check/verify is available separately below; preparation never invokes it.

## Explicit task checking and saved-bundle verification (S2)

`karakana docs content check` requires a request with an existing supported context.
It uses the unchanged M2 checker, preserving every declared document, finding,
coverage field and scoped gap. All context profile types must appear in the task's
artifact_types; there is no filtering or substitute profile. The
[check request](check-example.json) selects the existing synthetic default-pack
context and no guide/template; adapt it to actual sources before product use.

```bash
karakana docs content check --request docs/skills/engineering-artifact-catalogue/content-checks/check-example.json --format json --output .karakana/examples/kdx11-check
karakana docs content verify --request docs/skills/engineering-artifact-catalogue/content-checks/check-example.json --bundle .karakana/examples/kdx11-check --format json --output .karakana/examples/kdx11-verified
```

Each output must be fresh; choose new names on subsequent runs. Both commands
write a bare M2 `content-report.json` and a task result0.1 `result.json` with an
equal nested report. Default output is a fresh `.karakana/document-tasks/<run-id>/`.
No source or old output is rewritten. Incomplete/unsupported assessments may still
produce diagnostic bundles; a partial write is never successful and its nonempty
files remain incomplete evidence.

Task checking captures the request, optional fixed `docs/content-policy.json`,
explicit resources and context, plus optional AGENTS.md/KARAKANA.md presence/bytes.
It does not render planning instructions or require checkout skills/memory when
resources are empty. The request's skill/action/audience/scope/revision remain
caller declarations, not evidence of actual document metadata or authorisation.
Preparation still requires its selected checkout assets. Parser loading is lazy;
missing content support refuses the check, without an automatic install or download.

`check_task(root, request_path, output=None)` and
`verify_task(root, request_path, bundle, output=None)` in `karakana.document_tasks`
return the same task result as the CLI. Exit0 means `checked` or `verified` with
mechanically complete content; warnings/gaps can remain. Exit2 means a blocked,
unsupported, incomplete, stale/mismatched or failed operation. Readiness and
acceptance never advance automatically; review is required. No aggregate
product-ready or accepted boolean is provided.

Saved verification reads strict bounded JSON, requires equal raw/nested report
copies, delegates bare-report verification to M2 and independently recomputes
every deterministic task field. Guide/policy/request/code/optional-presence drift
can make the whole bundle stale even when raw content is current; both states are
visible. Changed saved acceptance/outcome cannot hide behind a matching digest.
Only validated run ID/generation/output metadata and M2 generation time are
volatile; successful verification metadata follows M2's existing rules. Check
bundles and successful verify bundles are supported; preparation-only, foreign,
unsupported-version, malformed and partial bundles refuse. A current incomplete
check remains incomplete and exits2. Saved input is rechecked and never updated.

Wrapper captures retain32 physical inputs/2MB each/16MB total/128KB configuration;
M2 has its separate unchanged32-file/16MB budget (combined at most64/32MB). Saved
result/report files each have a2MB read/write limit. Plain text shows scope first,
separate states, all findings and scoped gap details, with terminal controls escaped.
JSON stdout is one object; CLI syntax errors use stderr and empty stdout. These
commands add no protocol gate, model call, source apply, export or deployment.

## Direct M2 check and verify

Install the optional content dependency. Development installation supplies the same
pinned parser; other Karakana/P02 commands remain usable without it.

```bash
python -m pip install -e '.[content]'
python -m karakana.tools.engineering_content --root . check --context docs/skills/engineering-artifact-catalogue/content-checks/default-packs.json
python -m karakana.tools.engineering_content --root . check --context docs/skills/engineering-artifact-catalogue/content-checks/evidence.json --format json --output new-content-report.json
python -m karakana.tools.engineering_content --root . verify --context docs/skills/engineering-artifact-catalogue/content-checks/evidence.json --report new-content-report.json
```

The [default context](default-packs.json) checks the accepted examples, retaining their
Q-01/Q-02 and design gaps. The [tailored context](tailored.json) reads a compact source
and its governing records. The [evidence context](evidence.json) additionally checks a
source-selected open item and synthetic observation fields/local evidence. These use
[test-data sources](../../../../tests/fixtures/engineering_content/compact.md), not facts
or executed results about a real product. Copy/edit configuration for the requested
sources; never copy synthetic facts into a project baseline.

Python APIs: `check_content(root, context_path)` and
`verify_report(root, context_path, report_path)` return `ContentReport`. `.ok` means
scoped mechanical completeness, not acceptance. `.to_dict()` gives the JSON report.
Exit0 means mechanical checks passed (and, for verify, the report matches); warnings
and unresolved items may remain. Exit2 means incomplete/unsupported input, stale or
mismatched verification, missing dependency or refused I/O. Text is default; JSON
stdout contains only JSON. Optional check output creates a new file, even for an
incomplete assessment; an existing output is preserved. No sources are rewritten.

## Context versions and source authority

Both context0.1 and0.2 support the strict `namespace`, `documents`, `references`,
`coverage`, `omissions`, `open_items` and `claims` contracts. Missing optional arrays
mean empty. Version0.2 additionally permits `links`; **even empty links fails under0.1**.
Unknown versions, keys, duplicate JSON keys and nonstandard numeric constants refuse.
Namespace is explicit. Document IDs/revisions/canonical source come from actual
source metadata, never context overrides. Design documents declare their requirements
baseline keys. Profiles remain requirements/system-design0.1 and narrative-0.1;
P02/frontmatter sources use their independent validator/exporter.

`references` entries have unique `key`, root-relative `path`, `purpose`, and optional
`format: narrative-0.1`. Every declared file is bounded/read/hashed. Opaque files may
be referenced, but cannot replace narrative explanation or supply record inventories.
Document/reference keys share a namespace; duplicate physical declarations refuse.
References are not recursively fetched or executed.

A Locator names `document` (a declared key) and exactly one `anchor` or complete
`heading` array, with optional `record_id` and `field` for registered rows/cells.
Heading paths are exact H2-and-deeper paths; no fuzzy matching, regex, row numbers or
implicit slugs. Use actual `<a id="unique-name"></a>` anchors outside code. A standalone
anchor before a heading selects its section; an inline row/cell anchor selects that
row. Multiple candidates fail. Rows without IDs need unique row/cell anchors plus
field; an anchor on a multirow section cannot select its first cell implicitly.
The checker never inserts anchors. Headings/anchors are selectors, not native IDs.

Registered tables use complete `| cell |` raw boundaries, `---` separators, `&#124;`
for a cell pipe and `<br>` for a cell line break. Malformed/short/wide/detached rows
cannot disappear through token normalization. Existing IDs are preserved exactly;
ranges resolve against the bounded declared inventory. Literal code/fenced/quoted
examples do not supply missing content or executable diagrams.

## Tailoring and explicit links

`coverage` maps a `document` and registered `slot` to a `source` Locator. The selected
view must have the required explanation/registered table shape; opaque files, blank
headings and substitution prompts do not count. Coverage cycles refuse. Document
identity remains in its own metadata. Governing records retain their physical source
locations and are associated with the checked baseline that actually selects them.
Local declared rows/errors cannot be hidden with another view or competing copy.

`omissions` maps an absent conditional `slot` to a nonempty `rationale` Locator.
Required/core content cannot be waived. Rationale existence is checked; applicability
and adequacy remain reviewer decisions. Existing content still gets checked.

Version0.2 `links` entries have exactly `from` and `to` Locators. `from` includes a
registered nonempty reference field. `to` includes an actual `record_id`, without
`field`, of the required kind in the declared baseline. Multiple entries may map one
cell to several targets. The canonical target set, when present, must equal the
explicit set. Dangling IDs, malformed ranges, missing/extra/conflicting targets and
duplicate resolved edges refuse even beside valid mappings. Custom prose without
canonical target IDs requires a complete explicit target set or stays unsupported.
Canonical and explicit agreement is corroboration; it does not duplicate graph edges.
Forward/reverse requirement/criterion consistency and design coverage still apply.
Q/unknown references retain unresolved effects. A mapping does not prove prose meaning.

## Open items and claim evidence

`open_items` maps `item`, a nonempty `affected` locator list, `effect`, `resolver`, and
`next_action`. Each refers to actual source content; configuration does not duplicate
facts. Missing located details fail; matched source gaps are enriched rather than
removed. Map each canonical row once; different cell selectors cannot overwrite
one item’s affected scope. Affected requirements/scopes are explicit. Document readiness reflects its
own affected scope; an unrelated document is not declared unresolved by that mapping.
No unknown threshold, resolution or readiness is invented.

`claims` maps `source`, `kind` (`test_result` or `decision`), and `fields`: revision,
actor, result, timezone-aware time and evidence; test results additionally require
environment. Planned/proposed work is not an actual observation. Located declarations
are not authenticated facts. Accepted-decision rows need actual field mappings;
likely unmapped prose claims warn rather than receive a word-based certification.
Product approval/audit requirements remain legitimate product content.

Evidence fields contain a local relative path or Markdown link(s), resolved from the
evidence source's directory through the same root/secret guard. Local files must
exist and are hashed. HTTP(S) evidence is **not fetched or authenticated**, remains an
explicit review warning/limit, and cannot establish independent acceptance. Credential-
bearing URLs and unsupported URI schemes refuse. No evidence text is executed.

## Reports, freshness and limits

Report version0.2 retains `completeness`, located rule/severity/action findings,
checked/reference/omission coverage, source-selected claim provenance and
`open_acceptance_items`. `review_required` is always true. `readiness` is unresolved
for affected declared gaps, otherwise not_assessed; `acceptance` is not_assessed.
Diagnostics contain locations, not source-value excerpts or arbitrary metadata.

`manifest` records exact context/source/evidence bytes, profiles, checker components
and parser version. `assessment_digest` separately covers canonical assessment fields.
LF/CRLF or context enumeration changes can preserve semantic equality while changing
raw hashes. `verify` recomputes using the same checker and compares **both** the raw
manifest and every persisted assessment/status/coverage field; no saved pass/digest
is trusted. Tampered, missing, stale and incompatible reports refuse. M1 report0.1
must be regenerated with check. A current incomplete report still exits2; verifying
freshness does not turn its findings into a pass. Reports are not signed attestations.

Inputs are capped at2MB per document/reference/evidence/report,128KB per context/
profile,32 files including context and16MB aggregate check inputs. Configuration
arrays have at most256 entries and JSON nesting at most64 levels. Installation
resources are independently fingerprinted. Sources/profiles/checker/parser are
rechecked within a run and before new output; verify also rechecks its saved input.
Absolute/escaping/credential paths, unsafe symlinks, drift and overwrites refuse.
Sources, HTML, formulas, diagrams and configuration are never executed.

See the [accepted design](../CONTENT-PROFILE-DESIGN-2026-11-13.md) and
[implementation plan](../CONTENT-PROFILE-IMPLEMENTATION-PLAN-2026-11-14.md).
Automatic selection/enforcement, other templates/exports and client/pilot work remain later.
