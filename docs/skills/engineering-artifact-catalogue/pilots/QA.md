# Pilot quality and transport observations

Observed locally on 2026-09-26 with Python 3.14.4, openpyxl 3.1.5 and LibreOffice
26.2.5.2 620(Build:2). [qa-observations.json](qa-observations.json) records actual UTC,
baseline/payload/snapshot/office-return hashes, profile counts and outcomes.
This Markdown is the review narrative. No product test, acceptance or release
authority is inferred from documentation/transport checks.

## Authoring self-review

The active author read the five skill entrypoints and applicable conditional guides,
then authored original scenario copies from brief.md. This exercises guidance in
one session; it is not independent review or a live-model behavior benchmark.

| Concern / skill | Evidence assessed | Result and limit |
| --- | --- | --- |
| Requirements / engineering-requirements | Context/non-goals, three needs, story, three observable criteria and separate cases/runs | Scenario intent resolves exact category scope; no agreed priority, owner, prototype or user result manufactured |
| Design / engineering-design-records | Three plausible alternatives, chosen proposal/drivers, negative memory consequence, review trigger, two concern views and candidate schema | ADR remains Proposed; whole-input choice is argued but workload/latency and acceptance unconfirmed |
| Planning / engineering-delivery-planning | Two outcomes, forecast horizons, one output checkpoint and two ordered implementation tasks | References, interfaces, steps, checks/dependencies/recovery supplied; no date, estimate or commitment invented |
| Release / engineering-release-documentation | Planned scope/gates, trial stop/recovery conditions, user versus operator guidance, empty delivered notes | No delivered reader exists; product states stay Not run/Blocked; support/restore/publication/deployment/acceptance absent |
| Sharing / engineering-workbooks | Five profiles, seven-source manifest, qualified IDs, full-source links, omissions and readiness propagation | Author-assessed useful tasks documented in README; actual domain audience sign-off remains pending |
| Change review | Retained requirements 0.1 and 0.2, same IDs, amended AC-01/TC-01 and history | Small wording clarification follows the brief; self-review only, no imported agreement or approval |

The first integrity check rejected a machine revision declared as document 0.1 in
the register but candidate-0.1 in its manifest. Corrected both to the actual machine
revision before final export. File revision and containing-document revision are
different facts; repeat references must agree. The final baseline also includes
the intent brief and sample input, so source drift is not hidden outside the manifest.

Final source integrity: 49 records in the original four-document pack, 50 in the
amended pack. Four documents + brief + two machine files yield seven source hashes.
The 14 functional checks cover cross-file validity, profile semantics, all six
committed workbook/snapshot pairs, source-link resolution, unchanged sources and
reviewed revision IDs/history. Tests validate actual outcomes, not human adequacy.

## Returned-input review

All six scenarios used actual copies of the final business 0.1 workbook and the
real P02 comparison. The current-source revision simulation used an isolated
copy, restored afterward. Original baselines, Markdown and every returned file
were byte-checked and preserved; no report applies a source/approval change.

| Scenario | Observed report | Review action |
| --- | --- | --- |
| Question in Feedback plus a cell comment | Two observations; field proposed, comment retained | Inspect both; a reviewer label is not authenticated authority |
| Two competing requirement values | Two field conflicts | Resolve against actual scope; do not choose the last file |
| Row removal versus field edit | Removal/edit conflicts plus a blank-identity anomaly from the returned sheet | Preserve the input and inspect identity/content; do not silently delete source |
| Formula and added worksheet | Formula input, field proposal and added-sheet finding | Formula never evaluated; retain additional context in the original returned file |
| Clarification after canonical amendment | Source stale; feedback proposed_stale | Rebase review on the actual revised source, not old approval |
| Old criterion edited against changed criterion | Source stale and field conflict | Review baseline/current/proposed values before any source amendment |

The separately authored 0.2 amendment clarifies whitespace already resolved by the
brief. It retains IDs and history; the new business export gets its own ID/baseline.
Both retained originals and all annotations survive. Draft status and unobserved
product runs stay unchanged. No workbook agreement was imported.

## Office and visual checks

Opened/saved all five 0.1 profiles and the revised business 0.2 view through
headless LibreOffice. Real feedback comparison reports zero semantic observations,
zero stale sources and zero source issues in all six returns. Returned bytes can
change through office serialization; the immutable original pair is kept unchanged.
These checks verify represented cells/identity, not every spreadsheet feature.

Rendered the executive view to a 21-page A3 PDF. Visually inspected readiness pages
5 and 6: draft/not-approval labels, Not run/Blocked tests, material risk, unconfirmed
candidate/support/recovery and planned release state remain visible. The
[page 5 preview](readiness-preview.png) is supporting evidence, not the whole pack.
Feedback is on separate horizontal pages. Long/wide tables and narrative are better
reviewed interactively with full-source links; PDF print output is not a concise
presentation or an accessible-document certification.

Runtime originals/returns/reports/PDF remain under
`.karakana/research/engineering-artifacts-20260926/p05/final-pilot-root/` in the
workspace. Reviewed source copies, XLSX/JSON companions and this scoped observation
record are deliberate documentation assets; harness runtime logs are not committed.

Native Excel desktop/Accessibility Checker, assistive technology, actual recipient
usability, independent author review and realistic project application are unperformed.
No formula modelling or feature compatibility beyond the supported P02 plain XLSX
scope is claimed. No new blocker requiring a parser/profile change was found.
Keep profile 0.1 as the bounded review baseline; real audience approval remains
separate. Skills stay experimental. P06 must review these limits and full evidence
before authorized integration; promotion and a real release pack need their own facts.
