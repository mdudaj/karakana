# Opt-in narrative content checks — M1

M1 checks the **standard requirements and system-design narrative packs** selected
by an explicit local context. It reports mechanical completeness, contextual
warnings and declared gaps. Substantive review remains required. A mechanical
pass never establishes factual truth, standards conformity, product readiness,
independent review or acceptance.

This is separate from [P02](../P02.md): existing exact-table validation, native
bindings, workbook exports and feedback retain their contract. Narrative content
checking does not add P02 export support. No planner, hook, skill selection or
protocol gate runs this checker automatically.

## Run a current check

Install the optional content dependency, then run the module explicitly from the
declared project root. Development installation also supplies the pinned parser.

```bash
python -m pip install -e '.[content]'
python -m karakana.tools.engineering_content --root . check --context docs/skills/engineering-artifact-catalogue/content-checks/default-packs.json
python -m karakana.tools.engineering_content --root . check --context docs/skills/engineering-artifact-catalogue/content-checks/default-packs.json --format json --output new-content-report.json
```

The [default context](default-packs.json) selects the two existing synthetic
examples. They retain their Q-01/Q-02 and design qualification gaps. A successful
check of these examples is not evidence that an application was implemented/tested
or that those gaps were resolved. Copy/edit a context for the requested sources;
never copy example facts into a real project baseline.

The Python API is `check_content(root, context_path) -> ContentReport`; `.ok` means
the scoped mechanical checks passed, and `.to_dict()` returns the JSON-compatible
report. Context/source/output paths are relative to `--root`. Namespace is explicit;
document IDs/revisions and other document information come from source, not context
overrides. A design explicitly names its requirements document keys.

Exit0 means supported mechanical checks passed. Warnings and unresolved acceptance
items can remain. Exit2 means incomplete/unsupported input or a refused operation.
The CLI prints text by default; `--format json` prints only JSON. Optional output
creates a new file, including an error report when inputs are incomplete; an
existing file is preserved and the operation returns2. No source is rewritten.

## Supported scope and refusals

| Supported in M1 | Limit |
| --- | --- |
| Explicit `context_version: "0.1"`, `narrative-0.1`, requirements/system-design profiles0.1 | Unknown keys/types, duplicate JSON keys, nonstandard constants, unsupported profiles/versions and P02/frontmatter inputs refuse |
| Accepted pack headings, document-information table and supported header variants | Required slots need actual prose/rows. Empty headings, required fields or substitution prompts do not count. Conditional omissions remain unassessed. |
| Exact raw `\| cell \|` table convention | Use `&#124;` for an in-cell pipe, `<br>` for a line break and `---` separators. Short/wide/detached/malformed neighboring rows cannot disappear through token normalization. Unsupported tables refuse. |
| Literal stable record IDs with uppercase prefix and numeric suffix, such as `REQ-01`, `AC-01`, `Q-01` | IDs are preserved exactly. This is M1 narrative syntax; no P02/native ID changes. Ranges resolve against existing inventory, without unbounded expansion. |
| Reciprocal requirements/criteria and selected design-baseline coverage | No fuzzy matching, arbitrary baselines, automatic namespace inference or source editing |
| Fenced/quoted/code examples distinguished from content | Code cannot supply missing required prose/sections. Literal substitution syntax inside an explanatory code span is allowed. Diagrams are not rendered or executed. |
| Located wording warnings and source-declared question/design gaps | Unknown thresholds remain unknown. Effect/resolver/action adequacy and unmapped prose/evidence claims require review; M1 does not validate advanced claim mappings. |
| New current-run text/JSON reports with raw-byte/code/profile/parser fingerprints | Saved-report verification is not supported in M1; run `check` again. No cached pass is accepted as fresh evidence. |

The context may omit `references`, `coverage`, `omissions`, `open_items` and `claims`
or supply empty arrays. A **nonempty request returns unsupported**, with no silent
ignore. `links` and context0.2 are not supported. Tailored/governing-view coverage,
explicit evidence/open-item mapping and recomputed `verify` belong to M2. The CLI
recognizes a `verify` request only to explain this refusal; it does not inspect or
certify a saved report.

Product approval/audit requirements remain legitimate. Likely authoring logistics
or vague wording warn in context; there is no ban on `approval` and no requirement
that every sentence contain `shall`. An observed-result/approval table outside the
profile is unsupported; clearly scoped accepted-decision status requires the later
evidence path. Prose heuristics cannot exhaustively detect or authenticate claims.

## Read the report

`completeness` is `complete`, `incomplete` or `unsupported` for the assessed scope.
`findings` identify rule, textual severity, relative source path/line and corrective
action without copying requirement statements or arbitrary metadata into diagnostics.
`coverage` states supported and unassessed capabilities. `open_acceptance_items`
retains located gaps with their source IDs where available; no IDs are invented for
design rows lacking an explicit gap identity.

Every report has `review_required: true`, `readiness: unresolved` when declared
gaps exist (otherwise `not_assessed`) and `acceptance: not_assessed`. Document-level
results and overall results agree on the worst mechanical outcome. Unsupported
coverage cannot be hidden by otherwise valid records.

The manifest records exact context/source bytes, profiles, checker components and
parser version. The assessment digest separately covers sorted findings/coverage
and identities. LF/CRLF may produce equal assessments while source hashes differ;
equal semantic digests alone do not establish freshness. Inputs/profiles/checker
are rechecked during this run and before optional output. Reports are historical
observations, not signed attestations or M2 verification results.

Inputs are bounded to 2MB per document, 128KB per context/profile, 32 local input
files including context, and 16MB aggregate local input bytes. Package resources and
checker components are trusted installation inputs, independently fingerprinted.
Absolute/escaping paths, known credential/environment/key locations, unsupported control
characters, source drift and overwrites refuse. Links are not fetched; sources,
HTML, diagrams, formulas and context data are never executed. Plain source hashes
and declarations do not prove evidence authenticity.

See the [accepted design](../CONTENT-PROFILE-DESIGN-2026-11-13.md) and
[bounded plan](../CONTENT-PROFILE-IMPLEMENTATION-PLAN-2026-11-14.md) for the remaining
M2 work and its separately proposed reference-edge amendment. No automatic task-time
enforcement, additional exports/templates or client revisions follow from this tool.
