---
status: decision_required
question: "What bounded local pilot can test whether the existing executive workbook helps independent readers find release decisions, blockers and source evidence?"
evidence:
  - source: "docs/skills/engineering-artifact-catalogue/P05.md and pilots/QA.md"
    finding: "The synthetic export, source parity and LibreOffice transport were checked, but independent executive-reader understanding and native Excel accessibility were not."
  - source: "docs/skills/engineering-artifact-catalogue/pilots/exports/executive-v0.1.xlsx and .json"
    finding: "The pinned executive workbook has 11 sheets; Readiness and Blockers is fourth after Read Me, Control and Source Manifest. Its baseline pair is immutable and contains seven source hashes."
  - source: "skills/engineering-workbooks/SKILL.md and references/audience-profiles.md"
    finding: "The skill already retains material uncertainty, source links and an executive profile; deterministic evals test instruction coverage rather than recipient comprehension."
  - source: "AREX-Skill assessment, 2026-09-26, pinned upstream ac3fe1afa80fb9a09775ecfb2b6cc3ba850a2db6"
    finding: "The read-only assessment recommends provenance and realistic use cases in existing skills; its reported benchmark gains were not reproduced or shown to transfer to workbooks."
  - source: "Digital.gov usability-testing guide and Microsoft Excel accessibility guidance, checked 2026-10-01"
    finding: "Task-based sessions with three to five intended readers and comparative order balancing can test understanding; Excel accessibility needs structured tables and actual application/assistive checks."
requirements:
  - decision: "Use the existing neutral P05 checklist-reader pack and its committed executive 0.1 workbook/snapshot as the frozen baseline."
    acceptance: "Baseline hashes, seven canonical source files, profile version and export identity match the recorded P05 receipt before any session; neither baseline file is overwritten."
    artifact: "docs/research/2026-10-01-engineering-workbooks-audience-pilot.md"
  - decision: "Test decision finding, blocker understanding, planned-versus-delivered status and source traceability with independent executive-role readers."
    acceptance: "At least three role-matched non-authors attempt the same scripted tasks without hints; each critical false-ready claim is recorded and prevents an audience-usefulness pass."
    artifact: "docs/research/2026-10-01-engineering-workbooks-audience-pilot.md"
  - decision: "Preserve Markdown and declared machine sources as authority; audience feedback stays a proposal against an immutable workbook baseline."
    acceptance: "Any candidate uses a new source revision and new XLSX/JSON filenames, retains qualified IDs and all material blockers, and shows no source or approval mutation from workbook feedback."
    artifact: "docs/research/2026-10-01-engineering-workbooks-audience-pilot.md"
  - decision: "Check practical navigation, readable text statuses and application accessibility without treating a rendered PDF or deterministic eval as audience acceptance."
    acceptance: "The review records worksheet/header structure, keyboard navigation, wrap/source links, the tested app and version, actual accessibility-checker or assistive results, and every unperformed check."
    artifact: "docs/research/2026-10-01-engineering-workbooks-audience-pilot.md"
design:
  - choice: "Run a staged, task-based review of the existing executive profile: freeze provenance and baseline first, observe readers, then make at most one evidence-led source/guidance revision and retest the same tasks."
    rationale: "P05 already proves transport and blocker retention. Testing comprehension before changing the exporter identifies the actual failure and keeps the pilot bounded; matching tasks and source facts make a later comparison interpretable."
    artifact: "docs/research/2026-10-01-engineering-workbooks-audience-pilot.md"
  - choice: "Use the existing P02 exporter and feedback report, a neutral script, a source/claim ledger and separate structural, tool, reader and acceptance receipts."
    rationale: "Existing authority and immutable-baseline controls stay intact. Separating receipt types prevents source validation, author self-review or synthetic results from being presented as independent audience acceptance."
    artifact: "docs/research/2026-10-01-engineering-workbooks-audience-pilot.md"
artifact_choices:
  - kind: requirements
    disposition: updated
    path: "docs/research/2026-10-01-engineering-workbooks-audience-pilot.md"
    rationale: "This bounded record states behavior, observable thresholds, provenance and safety constraints without a new PRD."
  - kind: design
    disposition: updated
    path: "docs/research/2026-10-01-engineering-workbooks-audience-pilot.md"
    rationale: "The same record defines staged method, comparison, role criteria, evidence separation and alternatives; no architecture change needs an ADR."
  - kind: plan
    disposition: updated
    path: "docs/skills/engineering-artifact-catalogue/PLAN.md"
    rationale: "PL06 now points to this bounded execution order, exact inputs, checks, stop rules and next step."
  - kind: ux
    disposition: updated
    path: "docs/research/2026-10-01-engineering-workbooks-audience-pilot.md"
    rationale: "The reader tasks and workbook look-and-feel criteria are defined before any presentation change."
  - kind: test
    disposition: updated
    path: "docs/research/2026-10-01-engineering-workbooks-audience-pilot.md"
    rationale: "The rubric separates automated parity, office/accessibility and observed reader outcomes."
  - kind: schema
    disposition: not_applicable
    rationale: "The local pilot reuses the existing P02 contract and profile 0.1; a later exporter/schema change would require its own design and tests."
authority:
  state: pending
  evidence: "The user directed this bounded pilot-definition research on 2026-10-01. Independent-reader recruitment and outreach, any live model calls and later implementation have not been authorized by that instruction."
pending_decisions:
  - owner: "Karakana maintainer"
    question: "Approve coordinator-led recruitment of three to five independent executive-role readers for the synthetic workbook review, with private observation handling."
    next_action: "Review this proposed method, name or authorize a coordinator and eligible readers, then run the scripted sessions under a separate task."
next_action: "Prepare the frozen P05 baseline receipt and neutral task script locally; hold independent-reader sessions until the maintainer names or authorizes a coordinator."
---

# Executive workbook audience pilot: resolved scope and method

## Decision and limits

The next pilot uses the existing synthetic `pilot-checklist` executive export. It tests whether intended readers can locate a release decision and its basis. It does not repeat P05's five-profile integrity exercise or assume that its 14 functional tests and LibreOffice round trips prove usefulness. The [P05 QA record](../skills/engineering-artifact-catalogue/pilots/QA.md) already states that native Excel, assistive technology and recipient usability were untested. The viewed [readiness preview](../skills/engineering-artifact-catalogue/pilots/readiness-preview.png) has visible blockers but long, dense rows; this is a reason to test navigation, not a measured reader failure.

The requirements and method are resolved for review, but the audience session is **decision required**: a Karakana maintainer must authorize a coordinator and independent readers before outreach. Local baseline verification and script preparation can proceed without that outreach. This record does not claim recipient acceptance or authorize a skill/exporter implementation change.

The read-only AREX assessment at `.karakana/research/arex-skill-20260926/review.md` is local runtime evidence, not a committed dependency. The public [paper](https://arxiv.org/abs/2609.02749) and [pinned library](https://github.com/VectorSpaceLab/AREX-Skill/tree/ac3fe1afa80fb9a09775ecfb2b6cc3ba850a2db6) explain the provenance/use-case inspiration. Its benchmark results were not reproduced here. This pilot measures a documentation package, not AREX effectiveness, autonomous skill use or model quality.

## Frozen input and provenance

Use `docs/skills/engineering-artifact-catalogue/pilots/` as the declared source root. Freeze the existing `exports/executive-v0.1.xlsx` (`sha256:6f58fdfb31ce6dd8222518095e3cd27f1786fdb403190fba111b1105e808327c`) and matching `executive-v0.1.json` (`sha256:766bff7af53196c04e85ee753d4ba9905f8d3243128ff6f2ac73a2a808f9ae83`). Their recorded baseline is `pilot-0.1-unaccepted`, profile 0.1, with seven source hashes. Validate those bytes and every source path against the committed [observation ledger](../skills/engineering-artifact-catalogue/pilots/qa-observations.json) before sharing. A hash or commit identifies bytes; it does not prove human approval.

The pilot receipt must list for every claim: governing path/version or upstream commit, checked date, tested capability, observed result, omission and a refresh trigger. At minimum, changes to any of the seven source files, the P02 contract/exporter, executive profile, skill guidance or office application version trigger review of affected claims. Keep the original XLSX/JSON and any annotated copies unchanged. New exports get new IDs and filenames. This follows the existing [source authority contract](../engineering-artifacts.md); it does not create another master.

## Reader task script and acceptance rubric

Recruit three to five readers who would consume an executive release view and who did not author this pack. Record role and relevant familiarity; avoid names or personal data in the committed synthetic fixture. Moderated sessions can be about 30 minutes. Give all readers the same neutral, fictional decision brief and workbook, with no tutorial on where answers live. Ask them to think aloud. The [Digital.gov guidance](https://digital.gov/guides/plain-language/test/usability-testing) supports testing whole-document finding/understanding with a small set of intended readers; for a later baseline/candidate comparison, alternate which version readers see first.

| Task | Observable answer | Pass / failure signal |
| --- | --- | --- |
| T1: Can this fictional release proceed now? | No: product runs are `Not run`/`Blocked`, owner/recovery are unconfirmed and no deployment or acceptance is recorded. | Every reader must reject a ready/approved claim and cite at least two source-backed blockers. Any false-ready claim is a critical failure. |
| T2: What decision or evidence is needed next? | Identify the open workload/performance decision or the named release-evidence gap, then open its source. | At least 80% of readers, with a minimum of three, locate a correct item and source link without hints; record time, path and incorrect interpretations, not only a yes/no score. |
| T3: What is forecast versus delivered? | Roadmap/milestone are proposals; there is no delivered release note or observed product test. | Every reader keeps `planned`, `verified`, `deployed` and `accepted` distinct. Any invented delivered outcome is a critical failure. |
| T4: Can the claim be traced? | Find baseline identity, canonical document and full source for one release or risk statement. | At least 80% of readers, with a minimum of three, find the correct source and can state that the workbook is a derived view. |

T1 and T3 are hard safety gates. A candidate is useful only if those gates pass for all observed readers, at least 80% of readers (minimum three) complete T2 and T4 without moderator hints, and no material blocker or source identity disappears. With fewer than three independent readers, record observations but leave audience usefulness **unverified**. Record per-task answers, path taken, hints, confusion and debrief comments; small-sample counts are local evidence, not population statistics. Do not substitute author self-review or deterministic evals for these sessions.

Check workbook look and feel with the actual application/version: unique descriptive sheet names, simple named tables and headers, frozen identity columns, readable wrapped rows, text status alongside color, complete-source links and visible omissions. Inspect keyboard navigation, the Excel Accessibility Checker and a screen-reader path if the tools are available; record each check actually performed and failures. [Microsoft's Excel guidance](https://support.microsoft.com/en-us/accessibility/excel/accessibility-best-practices-with-excel-spreadsheets) supports these checks. LibreOffice/PDF inspection is separate transport/visual evidence and cannot certify Excel desktop or assistive use. The P05 executive PDF spanned 21 A3 pages, so print concision is an explicit observation, not an assumed pass.

## Bounded execution and change rule

1. **Prepare:** verify immutable baseline and seven sources; record claim provenance, reader eligibility, task script and stop rule. Run the existing P02 validate/export parity checks and focused pilot tests. Use synthetic content only.
2. **Observe:** run the scripted baseline with independently recruited, authorized readers. Keep their feedback as attributed observations in private review records; publish only de-identified findings. Do not silently alter source or treat a feedback cell as approval.
3. **Revise only on evidence:** if a task fails, first identify whether source wording, `engineering-workbooks` guidance, profile layout or application accessibility caused it. Limit the first candidate to one source/guidance presentation change using the same fictional facts, preserved qualified IDs and status, a new reviewed source revision, and a new XLSX/JSON pair. A profile/exporter/schema change opens a separate implementation slice with its own UX/contract/version review. If baseline passes, record a no-change result.
4. **Retest and decide:** give baseline and candidate the same tasks, balance order where practical, and retain all raw observations and immutable pairs. Compare critical errors, independent task completion, navigation paths and accessibility findings. Report preparation, authoring, tool, reader and review effort. A candidate that fails the safety gates is not accepted even if it looks shorter.

The follow-up implementation task inspects this record, [P02](../skills/engineering-artifact-catalogue/P02.md), [P05](../skills/engineering-artifact-catalogue/P05.md), the [workbook skill](../../skills/engineering-workbooks/SKILL.md), its evals, source/export tests and current requirements before edits. It starts its own protocol and pre-implementation check. Verify focused affected tests, skill/eval validation and the required broader regression gate; review actual workbook output and source parity. No live model call, external reviewer contact, real project release claim, skill promotion, remote merge or deployment follows from this research closeout.

## Verification of this research closeout

On 2026-10-01, `tests/test_engineering_artifact_pilots.py` passed all 14 cases, P02 validated 49 synthetic records, and all three `engineering-workbooks` deterministic eval cases passed. The existing executive workbook and snapshot SHA-256 values matched their committed observation ledger. I inspected the executive workbook's sheet order and the P05 readiness preview, checked the new local Markdown links, and ran the research-resolution structural validator. These are current source and local-tool checks; no independent reader, native Excel Accessibility Checker, screen reader or live-model trial was run. A full code regression suite is deferred because this change adds a research record and plan pointer without executable behavior.

## Alternative considered

Repeating P05's deterministic export and instruction-coverage checks would add no independent comprehension evidence. Rebuilding the exporter before observing readers would enlarge the change and confound the reason for it. The staged baseline first method reuses verified infrastructure and lets an observed failure determine whether the smallest correction is prose, guidance or a separately scoped profile change.
