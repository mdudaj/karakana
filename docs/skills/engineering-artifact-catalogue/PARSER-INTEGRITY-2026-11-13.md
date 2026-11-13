---
status: ready_for_implementation
question: How can structured artifact parsing avoid line-ending and partial-row data loss while preserving narrative sources and deliberately empty tables?
evidence:
  - source: karakana/tools/engineering_artifacts.py
    finding: parse_document decodes original bytes without newline normalization; the multiline heading match retains CR and fails the known-table lookup. Row filtering also silently discards unsupported pipe-row shapes.
  - source: tests/test_engineering_artifacts.py
    finding: Current fixtures and tests cover ordinary LF parsing, invalid columns/classes, explicit anchors, native bindings, freshness and narrative export, but not the reproduced line-ending and filtered-row gaps.
  - source: skills/engineering-release-documentation/examples/release.md
    finding: A supported instantiated example intentionally has a correctly parsed empty Release Notes table; zero records alone cannot establish a parser error.
  - source: docs/skills/engineering-artifact-catalogue/examples/release.md
    finding: The legacy catalogue release example also retains an empty Release Notes table with explicit no-delivered-change meaning.
requirements:
  - decision: Select PI01-PI08 below for a bounded parser-completeness fix; retain structural-versus-content adequacy distinctions.
    acceptance: Equivalent LF/CRLF input produces equivalent records and validation outcomes; malformed declared rows are refused; narratives, deliberate emptiness and raw-byte provenance remain supported.
    artifact: docs/skills/engineering-artifact-catalogue/PARSER-INTEGRITY-2026-11-13.md
design:
  - choice: Normalize CRLF only in the parsing view, share known-heading recognition, verify declared-section consumption and refuse unconsumed pipe-shaped rows inside structured sections.
    rationale: Corrects the demonstrated producer/consumer losses in the existing narrow parser without adding a Markdown framework, mandatory record-count profile or new export schema.
    artifact: docs/skills/engineering-artifact-catalogue/PARSER-INTEGRITY-2026-11-13.md
artifact_choices:
  - kind: requirements
    disposition: updated
    path: docs/skills/engineering-artifact-catalogue/PARSER-INTEGRITY-2026-11-13.md
    rationale: This compact closeout contains the reproduced evidence, selected requirements and observable compatibility criteria.
  - kind: design
    disposition: updated
    path: docs/skills/engineering-artifact-catalogue/PARSER-INTEGRITY-2026-11-13.md
    rationale: This record resolves the smallest parser method, alternatives, source-alignment challenges and rollback.
  - kind: plan
    disposition: updated
    path: docs/skills/engineering-artifact-catalogue/PARSER-INTEGRITY-2026-11-13.md
    rationale: Names exact implementation files, steps, regression cases and verification commands.
  - kind: test
    disposition: reused
    path: tests/test_engineering_artifacts.py
    rationale: Existing real fixture and consumer tests were inspected and executed; add the selected regressions there during the separate implementation task.
  - kind: example
    disposition: reused
    path: skills/engineering-release-documentation/examples/release.md
    rationale: This existing intentionally empty table is a required compatibility control, not a fixture to rewrite.
  - kind: schema
    disposition: not_applicable
    rationale: Preserve contract 0.1, public signatures, return keys, headers, IDs, snapshot format and exact-byte hashing; no new mandatory profile or source metadata.
  - kind: UX
    disposition: not_applicable
    rationale: No application interaction or visual artifact change; only existing parser errors and structural CLI outcomes are specified.
authority:
  state: approved
  evidence: After the completed research closeout the owner requested "execute", selecting local PI01-PI08 production implementation and regression verification. Publication/merge and later slices remain separate.
pending_decisions: []
next_action: Review the locally verified PI01-PI08 patch and evidence, then publish/integrate through a PR when that separate task is authorised.
---

# Artifact parser integrity resolution

The research baseline and its observed failures are retained below. The owner
subsequently selected implementation; current execution/results are recorded in
the implementation sections rather than rewriting the original observations.

Research trace: `20261113-180109-b6c290`. Inspected source: `f2319cc22107dc924648b10bc8f2c2565a0684af`,
verified current `main` against fetched `origin/main` before starting. Work is on
`research/engineering-artifact-parser-integrity-20261113`. PR #36 and CT01–CT08
remain integrated; their completed requirements/design reviews are reused.

This task closes the current evidence and method questions. No production parser,
tests, schemas, skill instructions or client documents were changed. The remaining
owner action is selection of implementation, not another requirements questionnaire.

## Current observations

The probe used the real `document()` fixture from `tests/test_engineering_artifacts.py`
and actual `parse_document`, `load_bundle`, module CLI and workbook exporter.
Every mutated source/export lived under `TemporaryDirectory`; source bytes were
checked unchanged after each operation. “CLI 0” means structural validation exited
successfully, not that content was complete or accepted.

| Synthetic input / operation | Observed on current source | Required next behavior |
| --- | --- | --- |
| Ordinary LF requirement table | One record, Requirements table present, no issues; CLI 0; business export contains one requirement | Preserve |
| Byte-equivalent CRLF document | Zero records, no parsed tables, no issues; CLI 0; business export has no Requirements sheet | Parse the same record/values as LF |
| LF frontmatter / CRLF body | Zero records and no issues; CLI 0 | Same as LF |
| CRLF frontmatter / LF body | One record; CLI 0 | Preserve |
| LF numbered `## 04 Requirements` | One record; CLI 0 | Preserve |
| LF known heading with trailing space/tab | Zero records, no parsed tables; CLI 0 | Recognize the same declared table |
| Known section containing prose only | Existing `ArtifactError`, CLI 2 | Preserve refusal: a known structured declaration needs its table |
| Correct header/separator plus explicit all-empty row | Parsed Requirements table with zero rows; CLI 0 | Retain deliberate empty-table representation; do not infer delivery readiness |
| Valid row followed by malformed `\|REQ-002 ...` | Only the first record survives; CLI 0 and export succeeds | Refuse the unsupported candidate row rather than drop it |
| All-empty row followed by malformed row | Parsed table has zero rows; CLI 0 | Refuse the malformed candidate even beside a blank starter |
| Valid row followed by row missing final pipe | Only the first record survives; CLI 0 | Refuse incomplete candidate row |
| Valid row followed by row missing initial pipe | Only the first record survives; CLI 0 | Refuse incomplete candidate row |
| Recognized row with wrong column count | Existing `ArtifactError`, CLI 2 | Preserve refusal |
| LF requirement with invalid class | Existing `ArtifactError`, CLI 2 | Preserve refusal |
| Same invalid-class input with CRLF | Zero records and no issues; CLI 0 | Match the LF refusal; row validation must receive the record |
| Known section without explicit anchor | Existing `ArtifactError`, CLI 2 | Preserve refusal |
| Properly metadata-bearing pure narrative | Zero records, no issues; CLI 0 and business export succeeds | Preserve valid narrative support |
| Unknown heading `Requirement overview` | Narrative, zero records; CLI 0 | Preserve unknown-heading narrative behavior; no fuzzy intent inference |

Two independent existing corpora confirm this is not just a minimal-fixture effect:

| Corpus | LF result | CRLF result |
| --- | --- | --- |
| Four catalogue examples and unchanged native JSON dependencies | 27 records, 16 structured tables, zero issues | Zero records/tables, zero issues |
| Four owning-skill examples | 23 records, 20 structured tables, zero issues | Zero records/tables, zero issues |

Both LF corpora contain one deliberately empty Release Notes table. The new clean
narrative `assets/` packs remain outside this structured-source parser contract.

## Selected requirements

Triage: newline/heading misrecognition and silently filtered malformed rows are
P1 source-integrity findings because a successful structural result can omit data
or skip record validation. The demonstrated scope is this local import/export
tool; no production data change or application compromise is claimed.

| ID | Requirement / acceptance |
| --- | --- |
| PI01 | LF, CRLF and the tested mixed LF/CRLF forms produce equivalent metadata, section identities, rows/values and validation outcomes for supported syntax. Source files are never rewritten. |
| PI02 | Preserve SHA-256 over original bytes. LF and CRLF hashes differ, even when parsed data is equivalent; existing source-manifest/freshness and feedback behavior continues to detect byte changes. |
| PI03 | Use the same recognition of known H2 table headings in anchor preflight, anchored extraction and completeness checks. Retain optional two-digit numbering; ignore horizontal whitespace around the title. Every recognized declaration must produce its structured-table entry or an `ArtifactError`. |
| PI04 | In a known structured section, every pipe-shaped candidate line must be consumed under the supported table grammar or refused. Malformed leading/trailing delimiters, separators, headers or column counts cannot disappear beside valid or blank rows. Refusal is structural even with `strict=False`. |
| PI05 | Preserve correctly parsed empty tables and legitimate narrative-only documents. Empty Release Notes tables remain present in parsed documents and omitted from record-driven exports as before. Do not implement a global nonzero-record rule. |
| PI06 | Preserve exact headers, explicit-anchor/identity checks, encoded `&#124;`/`<br>` behavior, literal/formula-looking values, duplicate detection, native binding authority and existing LF fixture results. |
| PI07 | Actual validate/export/feedback consumers see the same complete parse or structural refusal. The CLI returns 2 on malformed structured input; export refuses before creating workbook/snapshot output. A CRLF invalid-class row must fail like LF. |
| PI08 | Add real regression cases for these behaviors and preserve both existing corpus counts, legitimate empty/narrative controls and source immutability. Run focused then required full regression and deterministic evals during implementation. |

“Required structured section” here means a known structured declaration already
covered by the narrow contract. An unparsed declared table is a parser failure;
a correctly parsed, intentionally empty table is not. The current API has no
mandatory-content profile declaring that every document must have positive
Requirements or Test Runs counts. Such profile/readiness rules remain later work.
Unknown headings and well-shaped but substantively poor prose are not made valid
requirements by this fix; semantic adequacy remains a separate check.

## Selected method and alternatives

Keep `CONTRACT_VERSION = "0.1"` and public API/return shapes. In `parse_document`:

1. Decode raw UTF-8 as today; create an LF parsing view by replacing CRLF with LF.
   Preserve the original `raw` buffer for all hashes and source comparisons. Lone
   CR, BOM handling and a general Markdown grammar are outside this slice.
2. Use a small shared heading recognizer for existing H2 syntax, optional two-digit
   numbering and insignificant horizontal title whitespace. Apply it consistently
   in preflight and extraction; do not case-fold or fuzzy-match unknown titles.
3. Track known structured declarations and verify their consumption after anchored
   parsing. Preserve duplicate/invalid anchor and duplicate-table refusals.
4. Replace the silent pipe-line filter with explicit candidate validation within
   declared structured sections. A candidate has a leading or trailing boundary
   pipe after horizontal whitespace is disregarded for detection. Retain the
   supported row/header grammar and
   reject unsupported pipe-shaped lines with section/anchor context, without
   printing source cell contents. Retain surrounding prose and all-empty starter
   rows; they are not malformed record data.
5. Keep `load_bundle`, `_validate_records`, exporter and feedback authority/freshness
   behavior. Check consumers through tests rather than introducing another parser
   or changing warning/error semantics to hide incomplete parsing.

Interior-only pipes in ordinary prose do not declare a table row. Intent cannot
be recovered from arbitrary prose with both row borders absent; mandatory record
counts and richer Markdown interpretation remain the later profile/adapter work.
The new refusal boundary is explicit for unsupported boundary-pipe candidates in
known structured sections; use narrative sections for literal table illustrations.

| Alternative | Consequence / disposition |
| --- | --- |
| Only trim the captured heading | Addresses some CRLF symptoms but leaves inconsistent recognition and silent row loss; insufficient |
| Reject every zero-record document/table | Breaks supported narrative and deliberately empty release tables; rejected |
| Rewrite LF/CRLF sources before import | Changes source bytes and freshness/baseline evidence; rejected |
| Add a general Markdown engine or mandatory content profile now | Larger compatibility/API scope and new dependency/policy choices; defer |
| Selected local normalization and complete consumption | Addresses demonstrated losses while retaining the existing source/export contract; preferred |

## Source-alignment challenge

| Claim | Producer / consumer and contrary case | Resolution |
| --- | --- | --- |
| Metadata accepts CRLF, so structured records should also work | Frontmatter regex accepts CRLF; body multiline heading regex includes the trailing CR, so title lookup fails. Mixed-front/body probes isolate the body defect. | Normalize the parsing view and share heading recognition; do not equate metadata success with complete body parsing. |
| Successful validation means export has the requirement | `parse_document` -> `load_bundle` -> `_validate_records` -> `_project` -> `export_workbook`: CRLF yields no records, bypasses the invalid-class check and emits a business workbook without a Requirements sheet. | Test record presence and invalid-source refusal through actual CLI/export paths. No claim that all document-level checks are bypassed. |
| A malformed extra row will be rejected by width validation | The pre-filter drops a pipe line before `cells()`/width checks; valid and blank neighbors mask the loss. | Validate all candidates before filtering; preserve structural refusal under diagnostic `strict=False`. |
| Zero rows always means a parser failure | Existing release examples explicitly declare empty Release Notes; valid narrative has no structured table at all. | Retain these controls; distinguish missing/unconsumed declarations from valid empty output. |
| Newline equivalence permits equal source hashes | `_sha(raw)`, source manifests, export freshness and feedback use exact bytes. | Compare semantic parse results separately; assert different LF/CRLF hashes and stale-source detection after newline-only edits. |

## Reproduce the core findings

Run from repository root with the existing virtual environment. This uses the
real test fixture and temporary directories; it does not write the working
checkout's `.karakana` or modify production source.

```bash
.venv/bin/python - <<'PY'
from pathlib import Path
from contextlib import redirect_stdout
import hashlib, io, runpy, tempfile
from karakana.tools import engineering_artifacts as t
make = runpy.run_path('tests/test_engineering_artifacts.py')['document']
with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    source = make(root)
    lf = source.read_bytes()
    row = next(x for x in lf.decode().splitlines() if x.startswith('| REQ-001 |'))
    blank = '| ' + ' | '.join([''] * len(t.TABLE_HEADERS['Requirements'])) + ' |'
    extra = row.replace('REQ-001', 'REQ-002').replace('| REQ-002', '|REQ-002', 1)
    samples = {
        'LF': lf,
        'CRLF': lf.replace(b'\n', b'\r\n'),
        'LF extra malformed row': lf + extra.encode() + b'\n',
        'LF deliberate blank table': lf.replace(row.encode(), blank.encode()),
    }
    for label, raw in samples.items():
        source.write_bytes(raw)
        try:
            doc = t.parse_document(root, source, 'example')
            bundle = t.load_bundle(root, [source], 'example')
            count, tables = len(bundle.records), list(doc['tables'])
            assert doc['sha256'] == hashlib.sha256(raw).hexdigest()
        except t.ArtifactError as exc:
            count, tables = 'refused', str(exc)
        capture = io.StringIO()
        with redirect_stdout(capture):
            code = t.main(['--root', str(root), 'validate', '--source', str(source), '--namespace', 'example'])
        assert source.read_bytes() == raw
        print(label, count, tables, code, capture.getvalue().strip())
PY
```

Full matrix/export and corpus receipts for this session are
`/tmp/karakana-parser-integrity-results.json` (18 synthetic cases plus two existing
empty-table controls) and `/tmp/karakana-parser-integrity-corpus.json`. The full
probe is `/tmp/karakana-parser-integrity-probe.py`. The portable results and method
are recorded above so these local receipts are not required on another machine.

## Bounded implementation instructions

Use this record with the original [documentation plan](DRAFTING-CONVENTIONS-2026-11-13.md),
[source contract](../../engineering-artifacts.md), repository instructions and
`karakana-self-improvement`. Select a separate `python-code-change` task and pass
its prerequisite gate before production edits. No requirements/design re-review
is needed unless the method or compatibility boundary materially changes.

1. Add regressions to `tests/test_engineering_artifacts.py`: LF/CRLF/mixed and
   numbered/trailing-whitespace headings; invalid class in both endings; malformed
   extra/blank-neighbor/missing-tail/missing-start rows; `strict=False` structural refusal; raw
   hashes and unchanged files; deliberate empty-table and narrative controls.
2. Exercise validate/export refusal through the existing module CLI; verify no
   partial outputs. Reuse existing freshness/feedback and literal/encoded-cell
   tests, adding a newline-only source-drift case. Parametrize corpus compatibility
   where it adds actual record/identity evidence rather than static wording checks.
3. Implement the narrow method in `karakana/tools/engineering_artifacts.py` only.
   No requiredness flags, schema version, provider, routing or workflow changes.
4. Clarify supported heading/newline/candidate-row behavior and structural-versus-
   semantic limits in `docs/engineering-artifacts.md` and the
   [P02 tool guide](P02.md). Record actual results in this closeout and the handoff.
5. Run `.venv/bin/pytest -q tests/test_engineering_artifacts.py tests/test_engineering_documentation_skills.py tests/test_engineering_artifact_pilots.py`
   then the required stable `.venv/bin/pytest -q` and `.venv/bin/karakana eval run`.
   Check `git diff --check`, source preservation and the task completion protocol.

Recovery is a reviewed revert/fix PR if implemented behavior regresses; preserve
original sources/exports and runtime evidence. New refusals intentionally replace
silent losses; errors should identify the offending section, not expose raw values.
No migration, client revision, live model call or deployment is part of the slice.

## Implementation selection and readiness

After this research closeout, the owner requested “execute”, selecting PI01–PI08
implementation. The frontmatter now records that resolved authority; the original
research-only scope and its earlier decision-required checkpoint below remain
history. Implementation trace: `20261113-181553-72eaf6`.

User outcome: as a documentation author/reviewer, I need supported source records
to reach validation and exports consistently across LF/CRLF, and malformed rows
to be refused, so structural success cannot hide omitted input. PI01–PI08 define
the acceptance criteria and scope; code changes belong in `parse_document` and
small private helpers, with regressions in `tests/test_engineering_artifacts.py`.

| Criteria | Implementation surface | Verification |
| --- | --- | --- |
| PI01–PI03 | Parsing view, common heading recognition and declaration consumption | Newline/heading and raw-byte/hash regressions |
| PI04, PI07 | Structured candidate-line handling and existing CLI consumers | Malformed-row, diagnostic strict=False and no-partial-export cases |
| PI05–PI06 | Existing empty/narrative/identity/native-source behavior retained | Explicit controls and both legacy fixture corpora |
| PI02, PI06–PI08 | Existing export/feedback source freshness and error paths | Newline-only freshness regression, focused and full suites/evals |

Definition of ready: current source and prior evidence inspected; exact behavior,
method, file plan, compatibility, recovery and execution authority are settled.
No separate PRD/ADR/schema/visual artifact is necessary for this bounded fix:
this record contains its problem/user outcome, requirements, design, alternatives,
traceability and test method; no source schema or application UX is changed.
Definition of done: PI01–PI08 regressions and existing compatibility tests pass,
full required pytest/evals pass, the actual patch receives substantive self-review,
remaining limits and delivery state are recorded, and the task-bound handoff and
completion check pass. Source publication and integration are distinct later states.

Implementation review substantiated two additional instances of the selected
criteria: the old parser accepted a one-cell separator under a ten-column header,
and a set-only consumption check could miss a duplicate known declaration hidden
inside a narrative block after a valid table. Both were given failing regressions
before correction. Separator width is now checked and declarations must be unique
in preflight as well as extraction; these enforce PI03/PI04 without broadening the
selected method or adding a new profile. The embedded reproduction also handles
refused inputs so it can be rerun on the corrected parser while retaining the
pre-fix observations above.

## Verification and readiness

Current research verification: 88 existing focused parser/documentation/pilot tests
passed in 4.33s; all 18 synthetic probes and two intentional-empty controls ran,
plus four corpus combinations. Byte preservation and original-byte hashes were
asserted in the actual operations. No production patch or new automated tests were
created, so no full regression gate for a hypothetical fix is claimed.

The evidence, compatibility choices, method and file/test plan are resolved.
Implementation authority remains the user's next task selection under the
research-only brief, so the machine outcome is `decision_required`, not automatic
implementation readiness. No site fact or third-party decision blocks this local
work. Safe work completed is this research closeout; held work is production
implementation and any later publication/merge. The exact next action is the
bounded PI01–PI08 implementation if selected.

Model guidance: retain the active session; its model was not independently
verified through repository tooling and no switch or provider call occurred.
The protocol classified this integrity task high risk. For the later fail-closed
parser change, recommend GPT-6 Sol with high reasoning; a fresh conversation can
reuse this complete record and the current handoff without repeating broad research.

## PI01–PI08 local implementation results

The owner selected implementation after research. The local patch is complete
under trace `20261113-181553-72eaf6` on
`research/engineering-artifact-parser-integrity-20261113`, from `f2319cc`.
This section records the local checkpoint before publication, including the
preceding research documents. The owner later executed the stated source-review
and PR-integration next step, authorising task-branch publication and squash
integration after checks. Exact integration receipts belong to the associated PR
and final handoff; no deployment is included.

| Surface | Delivered behavior |
| --- | --- |
| `karakana/tools/engineering_artifacts.py` | CRLF normalization in parsing view only; one private shared heading recognizer; unique declaration preflight and consumption check; explicit boundary-pipe row refusal; separator-width validation. Other function bodies, public signatures, constants and return shape are retained. |
| `tests/test_engineering_artifacts.py` | 52 additional regression cases covering parsing/hash equivalence, heading/anchor consistency, partial-row loss under both strict modes, CLI refusal before output, deliberate emptiness/narrative, declaration loss/duplicates, separator width, both fixture corpora, real CRLF export and feedback/freshness. Baseline bytes are explicit across host newline conventions. |
| Source contract and P02 guide | Supported headings/newlines/rows and intentional stricter refusal boundary documented; structural versus semantic completeness and narrative-asset limits retained. |
| This record and parent plan pointer | Research/authority history, actual results and current continuation retained; no duplicated research or client revision. |

| Verification | Result |
| --- | --- |
| Pre-implementation gate | Passed `20261113-181721-protocol-check-50e772`; artifact presence only |
| Initial regression run on old code | 37 failed, 11 passed; two separator-width cases also failed before the correction |
| Declaration review regression | A hidden duplicate after a valid table failed before the additional uniqueness check; then passed |
| Final focused parser/documentation/pilot gate | 140 passed in 4.64s |
| Final full regression | 818 passed in 21.54s |
| Deterministic evals | 183/183 passed, zero warnings; report `20261113-182346-eval-9ba603` |
| Actual portable reproduction | LF/CRLF each produce one record; malformed row refuses with CLI 2; deliberately empty table remains valid with zero rows |
| Compatibility inspection | Public signatures, contract/header/profile/metadata constants unchanged; all other production function bodies unchanged; 13 legacy fixture/blank files byte-identical to `HEAD` |
| Patch | `git diff --check` passed; substantive self-review completed |

The final full run followed a test-only portability correction to ensure fixture
bytes genuinely represent LF/CRLF on either host. An earlier full run also passed
818 tests; only the final stable result above is used for completion. These runs
are local; no native Windows installation or independent reviewer acceptance is
certified. No fixture writes touched the working checkout's runtime stores.

PI01–PI08 self-review confirmed that raw source hashes still distinguish newline
changes, current rows retain identity in feedback, strict=False cannot bypass a
malformed table refusal, and exact empty/narrative controls remain supported.
The code does not impose positive record counts, perform semantic language checks,
add a Markdown engine or change source/export ownership. Unsupported boundary-pipe
illustrations in a declared structured section now fail explicitly; place those
in narrative sections. Lone CR/BOM handling and richer content profiles remain
outside this slice.

Remaining: source review and authorised PR integration of this bounded patch,
then selection of the next content-profile/checks or routing/enforcement slice
from the original roadmap. No new code should be started merely from this
completion note. Recommend GPT-6 Sol high for integrity review; a fresh
conversation can reuse the exact evidence above and the current handoff.

Publication preparation also refreshes the portable continuation note to reference
the PI results and current branch/main state rather than the earlier CT-only
checkpoint. The wrapper's refresh/load behavior is unchanged. Verify current Git
and PR state before choosing work; a merged slice must not be reopened from an
older checkpoint. This is continuation maintenance, not new parser scope.
