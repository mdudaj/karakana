---
status: ready_for_implementation
question: Which bounded next task should follow accepted and merged M2 without treating old backlog status or missing workflow evidence as current readiness?
evidence:
  - source: docs/karakana-dogfood-assessment-2026-10-01.md
    finding: The historical safe allowlist run passed but left real requirements/action/patch/ingestion/crosslink/full-release qualification unexercised; its P2 manual review remains distinct from feature tests.
  - source: docs/delivery/2026-10-29-handoff-quick-reference.md
    finding: GitHub PR32 and local ancestry verify this delivery was squash integrated at a1eb2ea; earlier unmerged wording is stale and has been reconciled.
  - source: docs/skills/engineering-artifact-catalogue/CONTENT-PROFILE-IMPLEMENTATION-PLAN-2026-11-14.md
    finding: M2 is owner-accepted and merged PR40 at da3d29d, with961 tests/186 evals, wheel and explicit CLI checks; task-time selection/enforcement remains a separately selected future slice.
  - source: karakana/dogfood/runner.py
    finding: Full mode runs9 allowlisted commands plus synthetic fixture preparation. It does not itself run the checklist's actual workflow chains or release check --full.
  - source: karakana/agents/planner.py
    finding: Planning explicitly loads one selected skill body; SkillLoader reads one SKILL.md and neither path recursively loads document resources or invokes the content checker.
requirements:
  - decision: Prefer one local artifact-backed workflow qualification slice before the next task-time integration implementation; current task only selects and documents the proposal.
    acceptance: Every examined workflow has its current revision, real source artifacts, actual command/result and evidence limits, or a named held/not-applicable disposition; no fixture or zero-finding flag substitutes for an unperformed workflow.
    artifact: docs/research/2026-11-14-post-m2-next-milestone.md
design:
  - choice: Reuse existing safe runner/checklist plus explicit local workflow probes in an isolated public-source checkout; inspect provenance before running commands and report each outcome separately.
    rationale: Closes an existing P2 evidence gap without changing default gates, activating models or touching clients; requirements-only integration work is the closest alternative, not discarded as invalid.
    artifact: docs/research/2026-11-14-post-m2-next-milestone.md
artifact_choices:
  - kind: requirements
    disposition: updated
    path: docs/research/2026-11-14-post-m2-next-milestone.md
    rationale: Compact scope, acceptance and copy-ready next-task instruction; no speculative feature PRD.
  - kind: design
    disposition: updated
    path: docs/research/2026-11-14-post-m2-next-milestone.md
    rationale: Chooses a concrete qualification method, bounded artifact inventory, conditional held paths and alternatives.
  - kind: plan
    disposition: updated
    path: ubongo/projects/karakana/open-issues.md
    rationale: Reconcile verified KDX09 integration; expose proposed KDX10 with explicit owner-review status and current acceptance.
  - kind: test
    disposition: reused
    path: tests/test_handoff_quick_reference.py
    rationale: Existing actual-output/legacy/provenance tests verify the completed KDX09 behavior; the future task uses actual workflow outcomes, not wording-only tests.
  - kind: schema
    disposition: not_applicable
    rationale: Current changes correct documentation/backlog and select a future method; no runtime schema or source behavior changes.
  - kind: UX
    disposition: not_applicable
    rationale: No product interface changes; preserve the existing self-contained review-summary convention and actual diagnostic contracts.
authority:
  state: approved
  evidence: Owner selected KDX10 with execute after the self-contained task brief on 2026-11-14. The local qualification scope/method is approved; no patch application, live models, outreach, default activation or deployment follows.
pending_decisions: []
next_action: Complete accepted KDX10 documentary PR/squash, then present the KDX11 requirements-only task brief; retain held qualification gaps.
next_action: Complete accepted KDX10 documentary PR/squash, then present the KDX11 requirements-only task brief; retain held qualification gaps.
---

# Post-M2 next milestone decision

Revision0.1,2026-11-14. Trace `20261114-080423-8758ab`; branch
`research/post-m2-next-milestone-20261114` from merged M2 `da3d29d`.
Request: reconcile current evidence and recommend the next bounded task. This
record does not implement the recommendation or reopen accepted CP/CD/M2.

## Current state and evidence consulted

M1, the context0.2 amendment and M2 are accepted and merged through PRs38–40.
M2's961 tests,186 evals, installed-wheel/API/CLI and postmerge release checks are
real feature evidence. They do not prove independent workbook comprehension,
new task-time defaults or every action/patch/learning workflow.

KDX09 was merged in [PR32](https://github.com/mdudaj/karakana/pull/32) at
`a1eb2eac5a8ebd5f73c7746497f2f7ae14c4b0f5` on2026-10-29. The connector's
actual merge metadata, local ancestor check,17-file commit footprint and current
project load support reconciliation to merged. The old `8ff3467` dependency is
historical, not an outstanding cherry-pick/merge. The old delivery note and backlog
now preserve that history with a current integration entry. No deployment or
independent acceptance is inferred.

The resource map had a stale M1-only paragraph. Corrected it to the actual M2
capabilities while retaining explicit selection, P02 isolation and no automatic
enforcement; owning skill receives a patch version. No runtime code change.

Inspected: KARAKANA/AGENTS/current project memory and skillpack; latest handoff;
CP requirements/design/plan and catalogue PLAN; current planner, skill loader,
protocol lifecycle; dogfood runner/checklist/backlog and historical assessment;
quick-reference delivery/source/tests; audience-pilot scope. The pilot still
requires independent role-matched readers/coordinator authority; no new outreach
or recipient-acceptance evidence is available in this task.

## Open findings and uncertainty

No current P0/P1 defect was identified in the inspected source/evidence. This is
not an exhaustive repository safety assessment. Stale KDX09/M1 text is corrected
in this local patch. The P2 real-workflow qualification gap is still open; a safe
runner's zero findings does not close it. Actual non-synthetic artifacts may be
missing for some chains. Locate them before claiming coverage and hold only the
affected chain, with owner and exact next action. Do not invent a reviewed model
response, operational result, source acceptance or reader session.

## Candidate milestones and criterion matrix

Five distinct options were generated using next-milestone-decision and
brainstorm-verbalized-sampling. The generation weights below are **uncalibrated
option-generation metadata**, not evidence, likelihood estimates or decision weights:
A task-time selection requirements0.35; B remaining authoring packs0.15;
C independent reader pilot0.15; D workflow qualification0.25;
E mandatory-enforcement policy study0.10 (sum1). No external model call was used.

Normative criteria/weights were fixed before scoring: project/user fit0.30,
current evidence0.20, prerequisite readiness0.15, risk control0.15,
reversibility0.10, cost efficiency0.10 (sum1). Scores are ordinal1–5;5 is better.
Risk/cost ratings concern the bounded task, not a claim about observed duration.
Weighted score is the sum of score times criterion weight. Decision weight is
score divided by all scores; it is **not a probability**. All options retain
existing approval rules; an unsafe action cannot win authority through scoring.

| Candidate | Fit | Evidence | Ready | Risk | Reversible | Cost | Score | Decision weight |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| D artifact-backed workflow qualification | 4 | 5 | 4 | 5 | 5 | 4 | 4.45 | 0.2438 |
| A task-time selection requirements | 5 | 4 | 3 | 4 | 5 | 4 | 4.25 | 0.2329 |
| B remaining authoring packs | 4 | 4 | 3 | 4 | 5 | 3 | 3.85 | 0.2110 |
| C independent audience pilot | 3 | 4 | 1 | 3 | 4 | 2 | 2.90 | 0.1589 |
| E mandatory enforcement policy study | 4 | 3 | 2 | 2 | 2 | 2 | 2.80 | 0.1534 |

A fits the delivered checker and avoids activation, but task-time applicability,
selection behavior and failure policy still need requirements/design acceptance.
B adds useful clean packs using existing guidance, but does not close the current
workflow evidence gap. C would add independent usefulness evidence, but coordinator/
reader access and outreach are unselected; source preparation is already available.
D reuses existing commands/evidence and an explicit open P2 follow-up with no new
code defaults. E is a broader policy study with larger authority and scope decisions;
mandatory activation cannot be inferred from CP/M2 or this selection task.

## Sensitivity analysis

Leave-one-criterion-out weights are renormalised; winners/ties are:

| Omitted criterion | Winner(s) |
| --- | --- |
| project_fit | D artifact-backed workflow qualification |
| evidence | A task-time selection requirements; D artifact-backed workflow qualification |
| readiness | D artifact-backed workflow qualification |
| risk_control | D artifact-backed workflow qualification |
| reversibility | D artifact-backed workflow qualification |
| cost | D artifact-backed workflow qualification |

Each criterion was also multiplied by0.8 and1.2 in turn, then all weights renormalised:

| Perturbed criterion | -20% winner | +20% winner |
| --- | --- | --- |
| project_fit | D artifact-backed workflow qualification | D artifact-backed workflow qualification |
| evidence | D artifact-backed workflow qualification | D artifact-backed workflow qualification |
| readiness | D artifact-backed workflow qualification | D artifact-backed workflow qualification |
| risk_control | D artifact-backed workflow qualification | D artifact-backed workflow qualification |
| reversibility | D artifact-backed workflow qualification | D artifact-backed workflow qualification |
| cost | D artifact-backed workflow qualification | D artifact-backed workflow qualification |

D wins all12 weight perturbations and5 of6 leave-one-out scenarios; dropping
current evidence ties D with A at4.3125. It is therefore preferred with an explicit
sensitivity limit, not an invariant/objective winner. If the owner prioritises new
integration requirements over closing the existing evidence gap, A is a defensible
revision; record that choice and retain the qualification follow-up.

## Recommended milestone and copy-ready task brief

**KDX10 — qualify current local harness workflows with real artifacts.**
Goal: establish which post-M2 workflows have actually been exercised before new
task-time behavior or release-readiness claims are proposed.

1. Load the handoff and accepted current sources; use this record, the existing
   dogfood assessment/checklist, runner/backlog, M2 delivery/merge/CLI receipts and
   real requirements/action/patch/ingestion/crosslink stores as evidence. Start a
   task trace and an isolated public-source checkout from the actual integrated
   revision. Keep original artifacts read-only; write fresh ignored runtime outputs
   in isolation. Current runtime receipts have local-only availability, so name
   exact files present before replay; do not assume an old ID exists elsewhere.
2. Inventory each proposed chain's provenance, revision, approvals and side effects.
   Use real accepted M2 source/diff/protocol/handoff evidence where applicable.
   For an absent actual response/action, record that exact missing input and owner;
   synthetic fixture preparation may test a tool but cannot become an actual action.
   Inapplicable items require evidence-based reasons. Do not expose secret payloads.
3. Run the safe current command allowlist and inspect actual outputs. Exercise
   requirements readiness, action-to-handoff, patch capture/review/gate and local
   ingestion/crosslink **analysis/dry-run only** where authentic inputs and existing
   authority suffice. Inspect current help/source before commands; never use model
   execution, patch apply/commit, ingestion/crosslink apply, bulk client mutation or
   external contact as an implicit qualification step. No new permission policy.
4. Include M2's real module check/verify and stale/tampered-report contrary cases;
   retain review-required and no checker-granted acceptance. Run the required local
   regression/evals/full-release check for the qualified revision and review its
   actual component results. Runner `--full` alone is9 checks plus fixture setup,
   not the checklist's full workflow or `release check --full`.
5. Produce one compact per-workflow matrix: revision/input/actual command/result,
   observed output, source-backed contrary state, limits and exercised/held/not-
   applicable disposition. Separate tool health, workflow coverage and release
   readiness. Close KDX10 only for the claimed scope; an unexercised chain stays
   explicitly open with owner/next action. Propose a fix only for a reproduced
   finding, with its own bounded implementation gate. End with an exact-trace
   return handoff and a next task brief (normally task-time selection requirements).

Definition of Done: the matrix and actual outcomes/limits are reviewed; no fixture
or stale pass is counted as real workflow success; all applicable safe checks have
results, and unavailable/inapplicable chains have exact dispositions. No release
candidate, deployment or independent reader acceptance follows automatically.
If current sources contradict an old follow-up, document and retire it rather
than repeat obsolete work. No new GUI/standards/architecture research is needed.
Use karakana-self-improvement/delivery-artifact-gate/karakana-handoff; reuse existing
methods. Recommend GPT-6 Sol high for workflow/patch-approval integrity review;
a fresh conversation benefits execution after this scope/record is accepted.
Advice only; no active model switch or availability claim.

## Source-alignment challenge

| Material claim | Producer -> consumer / contrary state | Evidence-backed resolution |
| --- | --- | --- |
| KDX09 needs another source merge | PR32/local ancestor and source/test footprint -> backlog/actual load | Actual merged metadata and current quick-reference output contradict the old pending entry; reconcile memory/delivery note, retain history. |
| M2 success proves task-time integration | opt-in module -> planner/SkillLoader/protocol lifecycle | Loader reads one selected SKILL.md; resource links do not recurse and no invocation is introduced. Future task-time requirements are separate. |
| Full dogfood means all workflow checks ran | runner FULL_COMMAND_IDS/fixture preparer -> checklist/backlog |9 allowlisted checks plus fixtures exclude actual chains/full-release. A zero-finding summary cannot close the existing manual P2 item. |
| Local source/wheel/evals establish independent audience usefulness | frozen workbook/script/local observations -> recipient decisions | No independent sessions in inspected evidence; keep coordinator/reader authority explicit and do not fabricate results or contact readers. |
| Qualification requires live/external execution | actual artifact inventory -> current dry-run/review CLI paths | Bound local replay and evidence inspection; missing authentic inputs hold that chain, not a rationale to run paid models/apply sources or mark it passed. |

## Exact decision and remaining work

Preferred owner decision: accept KDX10 local qualification as the next task, or
revise priority to A's task-time requirements review. Safe work now completed:
source/backlog reconciliation, alternatives, concrete method and artifact choices.
Held work: executing the selected next milestone and any feature/default policy
change. Owner: project owner. This record remains decision_required and not
implementation-ready for the next task until the choice/task selection is recorded.
No new runtime/source behavior, new workflow qualification run, independent reader
session, remote publication, merge or deployment occurs in this selection task.
Prior M2 acceptance/merge remains settled. Acceptance of this completed review
includes its normal reviewed documentation integration; actual next-task execution
is a separate selection. Preserve later agreement/revisions here and in backlog.

## Verification performed for this selection

Current-source/Git/PR32 metadata and actual handoff load inspected. Matrix sums,
score derivation and sensitivity calculated locally; full numerical receipt in
ignored runtime `decision-matrix.json`. Focused quick-reference, document-resource,
skill/eval and memory checks plus local-reference/whitespace validation are recorded
at closeout. These validate reconciliation and source-text guidance, not execution
of KDX10, external authenticity, independent acceptance or a new full-suite claim.


## Standards, governance and final verification

Reuse the mandatory project engineering process and source/export/approval
boundaries. Accepted CP/CD standards guidance remains29148:2018,42010:2022,
25010:2023 and15289:2019 with its existing tailored use/limits; this selection
adds no standard edition, certification or qualification-policy claim.

Current focused checks: **51 tests passed in2.90s** across quick-reference,
continuation and document-resource contracts; **3/3 coordinator instruction evals
passed, zero warnings** (20261114-081019-eval-e9ad92). Coordinator skill validation
and Karakana memory validation passed. Local references, research closeout
structure, weight sums/score derivation/sensitivity and diff whitespace passed.
No full regression rerun was needed for this documentation/status patch; M2's961
tests/186 evals remain prior implementation evidence. No new qualification run,
source behavior, mandatory enforcement, independent reader work, remote PR/merge
or deployment is claimed. These five public files are local/uncommitted; owner
review/integration of this slice remains separate from execution of KDX10.


## KDX10 execution selected — 2026-11-14

The owner replied **“execute”** after the concrete KDX10 brief. This selects the
proposed local qualification scope/method and supersedes pending scope statements
above. Qualification trace `20261114-081522-0d8d53`; task branch
`assess/post-m2-workflow-qualification-20261114`. Preserve the five reviewable
selection/reconciliation files in this coherent delivery; merged executable
baseline is `da3d29d`, qualified in a separate public-source checkout. No prior
documentation PR or next-task approval loop blocks the explicitly selected local
assessment. No default gates, source application, live models or external contact
are selected. Results and any held chains will be recorded without inventing
missing evidence.


## KDX10 qualification outcome — 2026-11-14

The selected local assessment is complete; qualification remains partial with
named held chains. [Actual results](../delivery/2026-11-14-kdx10-workflow-qualification.md)
record full-release24 components pass,186 evals,142 captured focused tests,
source-grounded KDX10 drafts/readiness and generic refusal, direct prompt-only
handoff, historical actual M2 diff/gate, ingestion/crosslink analysis and M2
current/stale/tampered/unsupported outcomes. The runner is completed_with_warnings
because isolated sibling paths are absent; no whole-workspace readiness follows.
All27 original action inputs are dogfood fixtures; authentic response/action
qualification is held for its genuine source/review, owned by the maintainer.
No executable code/default policy, patch application, live model, contact or deployment
changed. Exact qualified revision da3d29d and publication hashes were preserved.

The next proposal is KDX11 requirements review for explicit task-time profile
selection/result reporting, informed by typed report states and supported-format
boundaries. It is not a selected implementation or new default enforcement rule.
Owner delivery review/integration of this evidence slice is next. Earlier pending
scope/execution statements are retained history and superseded by the selected
execution and actual qualification results. Do not repeat the selection review or
reopen M2 acceptance/integration. The full source-alignment/conditional method and
original alternatives remain available above.


## Owner delivery acceptance — 2026-11-14

The owner replied **“accepted, next task brief”** after the completed KDX10
assessment summary. This accepts the delivered assessment and documentary
reconciliation without revisions, including its explicit partial-qualification
limits. It does not close the authentic-action/sibling-project evidence gaps,
authorise deployment or select implementation of task-time integration. Under
the standing accepted-work clarification, normal reviewed task-branch commit/push,
PR publication and validated squash integration of these six files are included.
No separate integration confirmation is outstanding.

Release/continuation trace: `20261114-083414-ba2911`. All six reviewed file hashes
matched before this acceptance-only update; no executable/source behavior or
qualification result changed. Complete exact-head CI and guarded squash, verify
reviewed tree/sole parent and clean main/release checks, then present KDX11's
requirements-only task brief here. Earlier delivery-pending statements remain
preserved history. KDX11 scope/requirements/design/code remain separate stages;
accepted CP/CD/M2 and KDX10 scope/result need no repeated approval.
