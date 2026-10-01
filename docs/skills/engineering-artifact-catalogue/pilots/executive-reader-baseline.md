# Executive workbook reader pilot: frozen baseline and facilitator receipt

Status: **prepared locally on 2026-10-01; no reader session or audience acceptance**. This is a facilitator record for the [bounded pilot method](../../../research/2026-10-01-engineering-workbooks-audience-pilot.md). Give readers only the [neutral handout](executive-reader-script.md), the workbook and its linked synthetic source folder. Do not give them the claim key below.

## Frozen receipt

The source is the synthetic `pilot-checklist` pack at Karakana `main` commit `c6d4502e9d5bd469b72e48d4ec46133b8cf10310`. The immutable pair is [executive-v0.1.xlsx](exports/executive-v0.1.xlsx) and [executive-v0.1.json](exports/executive-v0.1.json). Its export ID is `EXPORT-f39d54f4e8fe43d6bad8fecf06ac3fcf`, audience `executive`, contract/profile `0.1`, and caller baseline `pilot-0.1-unaccepted`. The label and hashes identify bytes; they do not confer approval. The pair has 11 sheets and 55 data rows. The first four sheets are Read Me, Control, Source Manifest, and Readiness and Blockers.

| Frozen file | SHA-256 checked against [the P05 observation ledger](qa-observations.json) |
| --- | --- |
| `exports/executive-v0.1.xlsx` | `6f58fdfb31ce6dd8222518095e3cd27f1786fdb403190fba111b1105e808327c` |
| `exports/executive-v0.1.json` | `766bff7af53196c04e85ee753d4ba9905f8d3243128ff6f2ac73a2a808f9ae83` |

The snapshot's seven-source manifest was checked against the actual files on 2026-10-01. The four Markdown documents are the declared authored sources; the brief is the fictional intent seed; the JSON files are proposed machine schema/fixture, not an implemented product or accepted interface. Preserve these exact files and the pair throughout baseline sessions.

For an authorized reader session, make a separate copy containing **only** the seven source files in the table below, `exports/executive-v0.1.xlsx`, `exports/executive-v0.1.json` and `executive-reader-script.md`. Keep the `exports/` subdirectory so the workbook's `../source` links resolve. Verify the copied hashes and links. Do not include this facilitator receipt, `qa-observations.json`, other profile exports or amended source revisions in the reader copy. Keep the original files untouched.

| Source in this folder | Declared revision | Authority | Verified SHA-256 |
| --- | --- | --- | --- |
| [requirements.md](requirements.md) | `0.1` | Authored Markdown | `c95d03feeb17abd558286b94fca6033c61421bf67d43a1f50e2304b123b9fe97` |
| [design.md](design.md) | `0.1` | Authored Markdown | `984f43be167a81a571a0f895d4a2ef257b0a4604482ec1353c39ed65a2c3402b` |
| [plan.md](plan.md) | `0.1` | Authored Markdown | `96a467cf536e0efa5be4c46966fe3541956a860de7b538edd59912a1f257680a` |
| [release.md](release.md) | `0.1` | Authored Markdown | `5512c49a81d5fd494a80b862c278616b5b3f2d3f16345bbb2179e9211f4f08c4` |
| [catalogue.schema.json](catalogue.schema.json) | `candidate-0.1` | Machine source | `8e06fa19a78185e365fd5bc3fbc6566a6954d0813c19bc583adfe812e102bf46` |
| [catalogue.json](catalogue.json) | `fixture-0.1` | Machine source | `6d275a938bf00ed83c20b2926dff58fc9248d39168e320c0ca68facd9bdc8479` |
| [brief.md](brief.md) | `pilot-0.1` | Authored Markdown | `e7764b6a4c70bd76b27dcab48902fdafe8cb9e40f14ded01678588cb1fa5ade9` |

The executive projection deliberately omits detailed requirements, stories, acceptance, ADR/design, cases/runs, implementation tasks, guidance and full narrative. Control declares omissions and Source Manifest retains seven source identities and hashes; the complete Markdown sources remain available through workbook links. An omission labelled `Source Manifest` refers to the authored registry detail being projected into the generated manifest, not to absent provenance. The workbook is a derived view, never the primary source or an approval record.

## Facilitator claim and source key — do not share with readers

| Reader task | Workbook evidence to watch for | Governing source and expected interpretation |
| --- | --- | --- |
| T1, release decision | Readiness and Blockers rows `Test Runs:RUN-01`–`RUN-03`, `Risks and Decisions:RISK-01`, and `Release Plan:REL-01` | [requirements.md#test-runs](requirements.md#test-runs) says Not run / Blocked; [plan.md#risks](plan.md#risks) says no implemented reader, product tests, support or recovery; [release.md#release-plan](release.md#release-plan) is planned. A ready, published, deployed or accepted claim is false. Reader must reject proceeding and cite two source-backed blockers. |
| T2, next decision/evidence | Risks and Decisions `RISK-02` and `RISK-01`, plus their source links | [plan.md#risks](plan.md#risks) leaves workload/performance threshold open; `RISK-01` and [release.md#release-plan](release.md#release-plan) identify candidate, product-test, support and recovery gaps. A correct item and its source must be found without hints. |
| T3, forecast versus delivered | Roadmap `OUT-01`/`OUT-02`, Milestones `MILE-01`, Release Plan `REL-01`, and Readiness and Blockers | [plan.md#roadmap](plan.md#roadmap) and [plan.md#milestones](plan.md#milestones) are proposals/forecasts; [release.md#release-notes](release.md#release-notes) has no delivered row; [requirements.md#test-runs](requirements.md#test-runs) has no completed product run. Never turn a forecast or local export check into delivery, deployment or acceptance. |
| T4, provenance | Control export/baseline identity, generated Source Manifest and a complete-source link | The selected claim should resolve to one of the seven source paths/revisions above. The reader should identify the workbook as a derived view and open the complete governing file. A hash identifies bytes, not human agreement. |

## Session procedure and blank observation record

**Outreach gate:** a Karakana maintainer must first name or authorize a coordinator and three to five independent executive-role, non-author readers. This preparation is not that authorization. Keep actual identifiable responses in a private review store; publish only de-identified findings. Use synthetic content only. Each reader receives the same [handout](executive-reader-script.md), immutable workbook copy and linked source folder; do not give a navigation tutorial or the claim key. Ask the reader to think aloud and record spontaneous path, answer, source, elapsed time, hints and confusion. A generic “continue as you normally would” prompt is allowed; record any substantive hint. Aim for roughly 30 minutes, without forcing an answer.

Copy this blank form into the private observation store for each authorized session; do not commit completed participant records:

| Field | Record |
| --- | --- |
| Coded session ID; role; relevant familiarity; non-author eligibility |  |
| Session UTC; facilitator; application/version; workbook pair/export ID and hash check |  |
| T1 answer; two cited blockers/sources; path/time; hints; false-ready claim |  |
| T2 decision/evidence and source; path/time; hints; incorrect interpretations |  |
| T3 planned/verified/deployed/accepted distinction; path/time; hints; invented delivery |  |
| T4 selected claim, source path/revision and derived-view explanation; path/time; hints |  |
| Navigation/accessibility observation; debrief; unperformed checks |  |

T1 and T3 must pass for **every** reader; any false-ready or invented-delivered claim is a critical failure of audience usefulness, even if the session continues for observation. At least 80% of readers, with a minimum of three, must complete T2 and T4 without hints. Fewer than three independent readers leave usefulness **unverified**. Record every deviation and unperformed check; no parser, author self-review, office round trip or deterministic eval substitutes for these observations. If a candidate is later justified, keep this pair and raw observations intact, use a new reviewed source revision and filenames, and retest the same tasks. A profile/exporter/schema change is a separate implementation slice.

## Recheck and limits

Before any session, recheck the exact two pair hashes and all seven source hashes against this receipt and snapshot; stop if any differ or a source link is missing. Changes to the source files, P02 contract/exporter, executive profile, workbook guidance or office application/version trigger review of affected claims. Run P02 source validation and the focused pilot tests. On 2026-10-01, P02 reported 49 structurally valid records; independent baseline checks matched the pair, seven source hashes, profile/contract identity and sheet order. Native Excel Accessibility Checker, keyboard/assistive use and human recipient understanding have **not** been tested in this preparation.
