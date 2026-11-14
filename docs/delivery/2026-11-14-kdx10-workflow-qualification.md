# KDX10 local workflow qualification

Assessment trace: `20261114-081522-0d8d53`. Date:2026-11-14.
Owner selected **“execute”** after the concrete KDX10 brief. This authorises the
local assessment, not source application, paid models, external communication,
default enforcement, publishing or deployment. Classification is assessment-review;
its keyword-derived permission/safety flags do not describe an actual policy change.
The governing scope/method is the [post-M2 decision](../research/2026-11-14-post-m2-next-milestone.md).

## Outcome

The bounded assessment is completed, with **partial workflow qualification**.
Applicable local drafting, source capture/review/gating, learning analysis, M2
verification and full-release checks were actually exercised. The authentic
model-response/action-to-handoff chain remains held: all27 original action bundles
inspected point to dogfood-generated fixture responses, with no non-fixture source
candidate. Direct prompt generation and synthetic action fixtures are separately
recorded, never promoted into genuine model/action execution.

The full-release tool reports pass for24 components, including its pytest/eval
subprocesses. The safe dogfood run reports completed_with_warnings:8 passed command
results and2 workspace-related warnings. Sibling checkouts were intentionally not
copied; this is not a claim that those actual projects fail or are absent on the
operator's host. A passing local tool report does not establish whole-workspace,
end-to-end live-action, operational or recipient readiness. KDX10 stays open only
for its explicitly held qualification scope; no source defect requiring a patch
was established by the observations below.

## Qualified source and isolation

- Exact integrated executable revision: `da3d29ddb5e0886741a4c4273a6ff0a3a27413e4`
  (accepted M2/PR40), branch `qualify/kdx10-20261114` in a separate local public
  clone. Current review/qualification documentation remains a working-branch
  overlay in `assess/post-m2-workflow-qualification-20261114`.
- All30 integrated M2 file hashes match the preserved publication manifest.
  Tracked/public checkout status is clean; no patch was applied and no source
  commit was made in the qualification checkout.
- The existing dependency environment was reused through an explicit `.venv`
  link, with subprocess PYTHONPATH set to the qualification checkout. Imports of
  `karakana` and `karakana.cli` were verified from that checkout. The link initially
  appeared as untracked; a documented local Git exclude corrected this setup-only
  noise. Original observations were retained; no tracked ignore/default changed.
- Existing source/runtime artifacts were read-only. New outputs, task-scope notes
  and controlled adverse copies were written under isolated ignored runtime.
  Redacted/source-scoped evidence was then retained in the original project's
  `.karakana/reviews/20261114-kdx10/evidence/`, with a188-file SHA256 manifest.
  Absolute isolated paths in original receipts describe where execution happened;
  retained copies allow review without depending solely on temporary paths.

## Actual workflow and evidence matrix

| Workflow | Genuine input / observed exercise | Actual outcome | Disposition and limit |
| --- | --- | --- | --- |
| Safe runner | `dogfood run --project karakana --skillpack karakana --full --json`; run `20261114-082000-dogfood-266a40` |9 allowlisted commands plus fixture preparation;8 results passed, workspace status/validation warned | Exercised with environmental warnings. `--full` does not cover all real workflow chains. |
| Requirements draft/readiness | Actual owner-selected KDX10 task-scope note, linked to the governing record/current trace; PRD `20261114-082032-req-9830a6` |5 source-grounded functional needs,5 stories and5 issue drafts; readiness `ready:true`, no warnings | Exercised. Manually authored real task note is explicitly not a model response; generated artifacts are drafts, not new accepted product requirements. |
| Requirements contrary state | Deliberately generic source control | `ready:false`, status not_ready | Exercised refusal state. Process exit0 alone does not establish readiness. |
| Direct task prompt | `codex run --project karakana --skill github-pr-review` for this actual M2 archival review task | Prompt generated; CLI explicitly says Codex execution was not run | Exercised prompt generation only. No model/Codex execution or action lineage is claimed. |
| Authentic response -> action -> handoff | Original runtime action provenance inventory | All27 action inputs are under dogfood fixture sources; no actual reviewed non-fixture response/action candidate | Held. Owner/input/next action below. Fixture preparation exercised tooling only. |
| Current diff capture | `codex capture-diff --project karakana --skillpack karakana --json` in unchanged qualified source | Empty diff, zero changed files and explicit no-working-tree-changes warning after setup exclusion | Exercised truthful empty-state capture. It is not an unapplied M2 patch. |
| Historical actual M2 diff/review/gate | Read-only `git diff --binary af27b67 da3d29d`,30 files; official PatchArtifact wrapper labelled historical replay with no source-task ID | Deterministic review warning/high risk, not blocked;142 actual focused tests attached; gate warning/high risk, not blocked, no failed checks | Exercised historical review/gate consumption. Broad risk keyword findings are prompts for review, not proof of billing/migration changes or independent review. No current task-to-apply lifecycle or permission to apply is claimed. |
| Patch contrary state | Deliberately absent patch/review input | Gate status blocked, blocked:true, missing patch/diff/review checks | Exercised refusal state. CLI process still exits0; consumers must inspect structured gate fields. |
| Ingestion | Actual task-scope note and actual M2 archival patch-review artifact; classify and review only | Bundles/candidates generated; reviews remain reviewable/non-applied | Exercised analysis. No candidate was written into durable memory or source; candidate quality/applicability still needs review. |
| Crosslink | Default workspace with explicit `--projects karakana`, actual requirements/patch-review evidence, then review | Exactly one project selected, one pattern, review not blocked | Exercised project-bound analysis. No sibling project was ingested or changed; cross-project transfer is not qualified by this single-project exercise. |
| M2 check/verify | Controlled copies of shipped source/context examples under ignored runtime; actual module CLI | Complete/current, review_required true and acceptance not_assessed | Exercised tool behavior on labelled neutral sources, not real product acceptance. |
| M2 contrary states | Altered acceptance flag, changed local evidence bytes, and actual accepted CP source selected as narrative input | Tamper/staleness exit2 and stale_or_mismatched; actual CP frontmatter source refused as unsupported, exit2 | Exercised. Existing frontmatter/P02 versus narrative support boundaries remain explicit; no adapter or forced pass was invented. |
| Full local release | `release check --full --json`; run `20261114-082001-release-check-911306` |24 components pass, including skills/skillpacks/workspaces/evals/pytest exit0 | Exercised local tool gate. Wrapper status does not reproduce nested warning detail or certify external environment/end-to-end readiness. |
| Actual task protocol/handoff | Current assessment trace, safety/evidence record and append-only return handoff | Completion/doctor/load checks recorded at closeout | Exercised current task lifecycle; artifact-presence checks are not semantic approval. |

Exact command arguments, exit codes, elapsed times and redacted stdout/stderr are
retained for28 commands in `evidence/qualification/commands/` and command-index.json.
Original source artifacts have explicit provenance; archival/controlled/synthetic
inputs are labelled. This matrix does not count mock/fixture generation as an
actual external action. The archive's wrapper records actual current branch/state
and commit-range provenance; it does not manufacture an executed source task.

## Warnings, contrary results and remaining qualification

1. **Authentic action chain held.** Owner: Karakana maintainer/project owner.
   Missing input: an existing non-fixture model response, scoped review/authority
   and resulting action source for an actual authorised task. Next action: select
   that genuine retained input when available and replay extraction/handoff
   generation locally, without execution. A future live call would need its own
   explicit opt-in; none was made here. Do not create a fake response to close this
   row. Safe requirements/provenance research can continue independently.
2. **Sibling-project qualification held/outside isolated scope.** Owner: relevant
   workspace/project maintainer. `crdb-mel`, `ilms`, `lims`, `msc-platform` paths
   are absent in the isolated parent; default status/validation warnings identify
   those paths. Next action if whole-workspace qualification is requested: verify
   actual paths/authority and run project-scoped read-only checks there. No source
   configuration or optionality was changed merely to remove warnings.
3. **Live patch application and recipient/production checks not applicable to
   this authorised assessment.** No patch apply/commit, ingestion/crosslink apply,
   live model/Codex execution, messages, source promotion or deployment occurred.
   Historical replay and local tool checks do not qualify these excluded actions.
4. **Structured state is authoritative.** Requirements and patch-gate commands can
   exit0 while returning not_ready/blocked. A future task-time integration must
   consume their actual typed status/blocked/readiness and coverage fields, not
   infer authority from process success. M2's exit2 refusals were also verified.
5. **Supported format matters.** The actual accepted CP record uses frontmatter
   and is not a narrative-profile input. This was explicitly refused; completeness
   enforcement must choose a supported context or expose unsupported coverage,
   never silently rewrite it, invent an adapter or claim M2 checked everything.

These are source-backed boundaries/held evidence, not automatically new code
bugs. No high-priority implementation defect was established by this bounded
assessment. Preserve the existing P2 end-to-end evidence gap until its genuine
inputs are available; do not turn local pass counts into a release decision.

## Verification, artifacts and next task

- Full local release:24 components pass, including actual pytest subprocess exit0.
  The wrapper records exit states, not the full pytest numeric summary. No invented
  fresh test count is attributed to it.
- Actual eval run:186/186 passed, zero warnings;
  `20261114-082002-eval-a53667` in isolated runner evidence.
- Captured focused M2 tests:142 passed in2.63s, result
  `20261114-082150-test-b57786`, attached to archival patch gate.
- Positive/negative task-readiness, missing-review blocking, M2 current/stale/tamper/
  unsupported, ingestion and scoped crosslink outcomes inspected as JSON, not
  inferred from command success. Checkout/import/hash/source-preservation proof
  passed. No source behavior or new default policy changed.

The current selection/reconciliation docs are carried with this assessment as one
reviewable documentation slice. Owner delivery review/integration is next; no PR,
merge or deployment for these current records is claimed. Existing M2 PR40 remains
accepted/merged. Research/standards/architecture were reused; no new requirement or
policy is silently activated. Existing engineering/source-authority rules govern.

Recommended next task after this review: **requirements review for explicit
task-time document/profile selection and mechanical result reporting**. Bring
applicability, supported source formats, user-visible decisions, status handling,
unsupported/held behavior and human approval boundaries here before design/code.
Keep default enforcement, automatic ready/accepted states and implicit model/source
execution out of scope unless separately selected. Retain the two held qualification
areas with their exact owners; they do not block independent requirements research.
Recommend GPT-6 Sol medium for that requirements decision (high for later workflow/
approval integrity design). Continue here for review; fresh conversation useful for
subsequent requirements work. Recommendations do not switch models or assert availability.


## Current documentation closeout

The five carried selection/reconciliation files plus this qualification record
are local/uncommitted on the assessment branch. Current focused documentation/
handoff checks:51 passed in2.78s; coordinator instruction evals3/3, zero warnings;
coordinator skill and Karakana memory validate. Local links/research structure
and whitespace checks pass. These are separate from the isolated baseline's
24 full-release components,186 evals and142 captured M2 tests. Current task
completion/doctor/load receipts and exact source/evidence manifests are retained
under `.karakana/reviews/20261114-kdx10/`. No accepted-document integration or
next requirements implementation is implied by these checks.


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
