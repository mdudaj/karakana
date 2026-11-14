---
status: resolved_no_change
question: Which accepted requirements govern explicit task-time document resource selection and mechanical result reporting before a separate design round?
evidence:
  - source: karakana/agents/planner.py
    finding: compose_planning_prompt loads one selected skill; linked guides and templates are not recursively included and no content check runs.
  - source: skills/engineering-documentation-conventions/references/document-map.md
    finding: Requirements and system-design have narrative packs; other types have guidance but no equivalent clean pack or registered content profile.
  - source: karakana/tools/engineering_content.py
    finding: Explicit context check and saved-report verify already exist; current checks separate unsupported content and recomputed freshness from acceptance.
  - source: docs/delivery/2026-11-14-kdx10-workflow-qualification.md
    finding: Actual frontmatter input was unsupported; requirements and patch-gate CLIs can exit0 with typed not_ready or blocked results. Authentic action and sibling evidence remain held.
requirements:
  - decision: Owner accepted TT01-TT12 revision0.1 with explicit opt-in selection/checking, scoped typed reporting and no new default lifecycle enforcement.
    acceptance: Owner replied accepted after the self-contained requirements summary on 2026-11-14; A01-A12 remain future verification definitions, not implemented behavior.
    artifact: docs/research/2026-11-14-task-time-content-requirements.md
design:
  - choice: For this requirements round, compare existing producers, consumers and contrary states; reuse accepted CP/CD/M2 contracts and defer new runtime architecture to a separate accepted-requirements design round.
    rationale: Resolves the requested behavior and limits without prematurely choosing command syntax, storage or lifecycle integration.
    artifact: docs/research/2026-11-14-task-time-content-requirements.md
artifact_choices:
  - kind: requirements
    disposition: updated
    path: docs/research/2026-11-14-task-time-content-requirements.md
    rationale: One compact governing requirements, acceptance, UX and research-closeout record for this bounded slice.
  - kind: design
    disposition: updated
    path: docs/research/2026-11-14-task-time-content-requirements.md
    rationale: Records the evidence-review method and the explicit boundary for the later runtime design; it does not claim that design is complete.
  - kind: backlog
    disposition: updated
    path: ubongo/projects/karakana/open-issues.md
    rationale: Expose accepted requirements and separate design continuation without closing held KDX10 evidence.
  - kind: checker_design
    disposition: reused
    path: docs/skills/engineering-artifact-catalogue/CONTENT-PROFILE-DESIGN-2026-11-13.md
    rationale: Accepted CP/CD/M2 scope and context contracts remain governing; no checker redesign.
  - kind: runtime_schema
    disposition: not_applicable
    rationale: This requirements-only round defines observable information needs; schema and interface design follow acceptance.
authority:
  state: approved
  evidence: Owner replied accepted on 2026-11-14 after the self-contained TT01-TT12 revision0.1 summary, without revisions. Standing acceptance-means-normal-validated-documentary-PR/squash authority applies. Runtime design, implementation and default activation are separate; resolved_no_change closes this requirements round without authorising runtime changes.
pending_decisions: []
next_action: Complete validated documentary PR/squash integration of accepted revision0.1, then present the separate design task brief; do not execute design or code from requirements acceptance alone.
---

# KDX11 task-time document selection and result requirements

| Document information | Value |
| --- | --- |
| Document ID | KDX11-TT-REQ |
| Revision / date | 0.1 / 2026-11-14 |
| Product applicability | Karakana task preparation and explicit local engineering-content check/report workflow after M2 |
| Canonical source / baseline | This file; inspected executable baseline `335a0fbb71743c88a8160f3aee835346859f5450` |

Current status: **TT01-TT12 revision0.1 accepted** by the owner on2026-11-14,
without revisions. The history below preserves the preceding review checkpoint.
Acceptance resolves this requirements round; runtime design and implementation
remain separate. No checker or task-time behavior is activated by this record.

## Purpose, users and scope

A task author needs to know which document resources apply and what a selected
mechanical check actually established. A reviewer needs scoped results without
mistaking prompt preparation, process success or content completeness for approval.
An automation consumer needs typed results it can interpret without scraping prose.
The project owner retains requirements, design and release decisions.

Proposed first scope: explicit selection of requirements/system-design authoring
resources during task preparation, plus explicitly requested M2 check/verify and
transparent reporting. Template use and checking are separate choices. Preparing
a task does not execute a model or check unfinished content. Existing supported
M2 multi-document contexts and tailored coverage remain available.

Excluded: new document packs, native/P02 adapters, exports, automatic catalogue
activation, new default stage enforcement, semantic/evidence-authenticity judgment,
automatic approval, live models, source application, outreach and deployment.
KDX10's genuine-action and sibling-project qualification gaps stay open but do
not prevent this independent requirements review.

## Standards and references

Reuse the [accepted CP requirements](../skills/engineering-artifact-catalogue/CONTENT-PROFILE-REQUIREMENTS-2026-11-13.md),
[CD design](../skills/engineering-artifact-catalogue/CONTENT-PROFILE-DESIGN-2026-11-13.md)
and [M2 plan/results](../skills/engineering-artifact-catalogue/CONTENT-PROFILE-IMPLEMENTATION-PLAN-2026-11-14.md).
Their accepted tailored references remain: ISO/IEC/IEEE 29148:2018 for verifiable
requirements, ISO/IEC/IEEE 42010:2022 for the subsequent architecture description,
ISO/IEC 25010:2023 for applicable quality concerns, and ISO/IEC/IEEE 15289:2019 for
information-item purpose/content. No new standards obligation, normative-text
review or conformity/certification claim is introduced.

The [requirements guide](../../skills/engineering-requirements/references/requirements-template-guide.md),
[document map](../../skills/engineering-documentation-conventions/references/document-map.md),
[UX copy patterns](../../skills/ux-writing/references/interface-copy-patterns.md)
and [engineering process](../engineering-process.md) govern tailoring.
New interface research on 2026-11-14 used the authors' [Command Line Interface
Guidelines](https://clig.dev/#output) for human-readable output, machine formats
and concise errors, and [W3C error-identification guidance](https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html)
for text that identifies the affected input. The latter informs terminal copy;
this is not a web-accessibility conformity assessment.

## Functional requirements

The owner accepted all TT requirements for this first scope. No separate priority
ordering was agreed. The acceptance cases below are definitions, not claims of
implemented or passed behavior.

| ID | Required observable behavior | Rationale / source | Criterion |
| --- | --- | --- | --- |
| TT01 | Task preparation shall distinguish requested action (inquiry, analysis/review, author/revise, planning or mechanical fix), artifact type, audience, project/root, scope and revision. It shall offer relevant resource choices without silently selecting or running them. | Preserve request type; planner and document map. | A01 |
| TT02 | The author shall be able to explicitly select the owning guide/template and, separately, a registered check profile/version and context. The effective selection shall identify its origin and any permitted override; absent or conflicting choices shall remain visible. | Shared conventions and current explicit M2 context. | A02 |
| TT03 | Only selected, permitted resources and explicitly declared dependencies shall enter task context. Catalogue links, examples and source content shall not trigger recursive loading, commands, network retrieval or model execution. | SkillLoader loads one file; bounded M2 local reads. | A03 |
| TT04 | Selection and reporting shall preserve declared source authority and supported format/version boundaries. The workflow shall refuse unsupported selections without conversion, fallback profile substitution or a claim of checked coverage. | Accepted CP/CD; actual KDX10 frontmatter refusal. | A04 |
| TT05 | Task preparation shall identify whether a check is requested. Checking shall require an explicit existing context and declared existing source inputs, including drafts when selected; missing inputs shall give a located corrective action rather than inventing a context, product facts or a pass. | Existing check/verify API; template is a starter, not a completed source. | A05 |
| TT06 | Reporting shall preserve selection/execution outcome, completeness, freshness, warnings, coverage/unassessed scope, unresolved effects, readiness and acceptance as distinct information. It shall consume typed producer results, never infer domain success from exit0. | M2 report and KDX10 exit0 counterexamples. | A06 |
| TT07 | Results shall identify the task/project/scope/revision, selected resource identities and actual contents, context/source/evidence provenance, profile/checker/parser identity and applicable report time. Saved-result reuse shall require current recomputation and selection-provenance validation. | M2 manifest/verify and scoped revision authority. | A07 |
| TT08 | Open items and held evidence shall retain their affected scopes, effects, responsible resolver and next action where declared; missing details shall remain unknown. Unrelated authorised work shall not inherit a global hold. | Accepted scoped M2 gaps; held KDX10 chains. | A08 |
| TT09 | A mechanical result shall never advance owner acceptance, readiness approval, merge, release or deployment. Existing scoped decisions may be referenced with their actual revision/evidence; changed content shall not inherit approval automatically. | CP08/CD08 and engineering process. | A09 |
| TT10 | Human output shall lead with the selected document/scope and actual outcome, then concise located findings and available next actions; it shall visibly retain unresolved/unassessed/review states. | UX-writing and current render_text conventions. | A10 |
| TT11 | An explicit machine-output choice shall return a versioned, parseable result preserving the same domain information and the underlying M2 report contract. Requested check refusal/incompleteness or stale verification shall signal command failure; warnings/gaps alone shall retain their typed effects. | Existing M2 text/JSON, exit0/2; reliable automation. | A11 |
| TT12 | Existing unselected planning/skill loading, protocol checks, direct M2 check/verify, P02/native validation and root/output safety shall remain compatible. Selection/check failures shall not modify governing source, accepted history or existing output. | Accepted opt-in scope; current loader and write_new protections. | A12 |

### Proposed applicability and precedence

| Task / input | Resource behavior | Check behavior |
| --- | --- | --- |
| Requirements or system-design author/revise/review | Offer mapped owning resources; include only explicit choices | Run only when explicitly requested with supported source/context; template selection alone runs no check |
| Inquiry, ordinary analysis/planning or mechanical fix | No blanket document pack requirement; reference existing affected artifacts as needed | No implicit check; an explicitly requested applicable document check remains possible |
| ADR, release notes, user guide, UAT or other type | Existing owning guidance remains usable; do not advertise an unavailable clean pack/profile | Report unsupported if a corresponding unregistered content profile is requested |
| Native/frontmatter/P02 source | Preserve native authority and existing validator/export path | Narrative selection reports unsupported; no automatic adapter |
| No selection / ambiguous type | Show unselected state or bounded recommendation; retain ordinary task preparation | Not checked, never complete; if checking was explicitly requested, hold that operation pending the exact missing choice |

Explicit task choices take precedence over overridable project resource defaults,
then selected skill guidance and catalogue recommendations. Mandatory project and
higher-priority safety/source-authority rules still govern; an apparent conflicting
task choice requires resolution rather than silent override. Show the displaced
choice and reason when an override is permitted. No new project defaults are
activated by this proposal. Ambiguity holds only the affected selection/check;
non-interactive use returns the missing choice without a hidden prompt or guessing.

The proposed policy is **explicit opt-in and advisory lifecycle integration**:
a requested check honestly fails its own operation on incomplete/unsupported/stale
input, but introduces no automatic protocol-stage block. Warnings remain warnings;
unresolved items preserve scope/effect and cannot become accepted merely because
completeness is complete. Existing project gates still apply. A future mandatory
policy would require a separately selected scope and owner decision.

### Result meaning and look and feel

`complete`, `incomplete` and `unsupported` describe M2 completeness. `current` and
`stale_or_mismatched` describe saved verification; unperformed checks/verification
must be explicitly unassessed. `blocked` or `not_ready` from other producers are
retained with their producer/meaning, not flattened into completeness. Missing
selection/context is an operation hold, not a fabricated content assessment.
`review_required`, scoped gaps, readiness and actual acceptance remain separate.
Exact new field names, command names and persistence layout belong to design.

Follow existing line-oriented terminal output: plain words, stable labels, paths
and line/record locators where available; no required color, icons, animations,
interactive wizard or full-width table. Summary first, detail progressively
available; never hide blocking findings or imply complete coverage through a
truncated list. JSON output must contain no prose, progress banners or ANSI
decoration. These technical diagnostic surfaces may name profiles and readiness.

Illustrative message requirements, not an approved command/schema design:

```text
docs/spec.md — content incomplete; requirements 0.1; selected scope only.
docs/spec.md:24 — Required coverage is missing. Add the requirement or declare its governing source in the check context.
Review required. Readiness unresolved; acceptance not assessed.
```

For missing context: “Content was not checked. Select a check context for this
document.” For unsupported content: name the selected format/profile and the
supported boundary. Do not offer conversion or retry as a recovery if no such
operation exists. Do not expose source contents or credential paths in diagnostics.

## Acceptance and verification definitions

Each A case is linked to the matching TT requirement. Future implementation must
exercise these behaviors with isolated roots and real API/CLI results; source-text
wording tests alone cannot establish them.

| ID | Conditions / event | Expected outcome | Verification method |
| --- | --- | --- | --- |
| A01 | Compare authoring, review, inquiry and mechanical-fix tasks; vary project and artifact type | Correct bounded recommendations; no artifact creation or checking merely from a keyword; scope/revision explicit or missing information named | Task/prompt integration cases |
| A02 | Explicit guide/template selection, permitted project override, missing version and contradictory mandatory convention | Effective resources/origin visible; allowed override recorded; contradiction/unknown version not guessed; one unresolved choice does not block unrelated preparation | Selection positive/negative cases |
| A03 | Selected guide contains links to unrelated packs, secret/outside-root paths or executable instructions; example unselected | Only permitted declared resources loaded; dependencies bounded and shown; no crawling/execution/network/model call; synthetic example facts never become project facts | Read/call spies and guarded-path cases |
| A04 | Requirements/system-design narrative profiles0.1 with context0.1/0.2; frontmatter/P02, unknown profile/version, context0.1 links or unavailable parser | Supported M2 behavior preserved; unsupported inputs remain refused/visible; no silent downgrade, stripped frontmatter or fabricated coverage | Existing M2 controls plus integration cases |
| A05 | Choose template only; request check without context; declare missing source; explicitly check a valid completed source | Preparation runs no check; requests with absent inputs held with specific correction and no pass; valid request invokes actual checker for exactly its declared scope | Invocation spies and actual CLI outcomes |
| A06 | Complete result with a gap, unsupported document, and recorded producers returning blocked/not_ready despite exit0 | All outcome axes/coverage retained; complete does not imply ready; no domain-success inference from process code or missing result fields | Typed-result consumer cases, including malformed/missing output refusal |
| A07 | Reuse saved result after changing document, evidence, context, selected guide/template, profile/checker/parser or persisted acceptance field | Recompute/refuse stale or mismatched result and identify safe regeneration; equal semantic digest or old timestamp alone is insufficient; same bytes under a different declared scope do not silently inherit authority | Manifest/recompute/tamper and selection-provenance cases |
| A08 | One governing open item affects a selected slice; unrelated KDX10 authentic-action evidence remains held; some resolver detail missing | Affected scopes/effects retained, missing detail remains unknown; no global readiness/hold invented; independent requirements work remains available | Scoped gap/held/missing-detail cases |
| A09 | Mechanically complete source with no owner acceptance; accepted revision later edited; real scoped prior decision supplied | No automatic acceptance, ready approval, source apply, merge or release; prior decision displayed only within its scope; changed revision requires applicable review | Authority/state-preservation cases |
| A10 | Complete-with-gaps, incomplete, unsupported and missing-context terminal output, color disabled and narrow terminal | Scope/outcome first; concise textual cause and available recovery; locators preserved; gaps/unassessed/review state visible without color; no unavailable action offered | Captured actual text and manual readability review |
| A11 | Parse JSON for positive/negative outcomes; warnings-only complete input, incomplete check and stale verify | Version/domain fields retained without decoration; complete warning-only check may exit0 but gaps remain; failed requested check/verify returns nonzero; existing producer exit0 blocked cannot become success | Subprocess JSON/exit-code matrix |
| A12 | No-selection legacy calls, direct M2 and native/P02 controls; attempted overwrite/outside-root output; identical repeated preparation | Existing behavior/contracts unchanged; no implicit checks, network or source mutation; new output only; repeated same inputs yield equivalent selections/findings apart from declared run metadata | Compatibility, byte-preservation and determinism regressions |

Quality constraints: bounded local work uses existing safety limits rather than
unbounded catalogue traversal (TT03); equal inputs produce equivalent semantic
results apart from declared run metadata (TT07/TT12); text and machine output
agree on domain states (TT06/TT10/TT11); refusal preserves source/output bytes
(TT12). No unsupported latency target or cross-platform certification is invented.

## Evidence review, alternatives and limits

| Material claim challenged | Producer → consumer / contrary evidence | Requirements consequence |
| --- | --- | --- |
| Resource links already provide task-time content | `SkillLoader.load_skill` → `compose_planning_prompt`; only selected SKILL.md body is rendered | TT01-TT03 add explicit preparation behavior; no claim that it is implemented |
| A mechanical pass establishes lifecycle readiness | M2 `build_report` → `render_text`; complete can retain gaps/review and acceptance not_assessed. KDX10 gate/readiness exit0 negatives | TT06/TT09/TT11 require independent typed axes and no new lifecycle gate |
| Any current accepted document is supported narrative | Context validation/reader → checker; actual KDX10 accepted CP frontmatter refused | TT04 preserves refusal and native authority |
| Cached digest proves freshness | `check_content` → `verify_report` recomputes fields, input/profile/code/parser manifests; existing evidence/symlink/tamper tests | TT07 reuses actual verification and extends provenance needs to selected resources, without redesigning M2 |
| Protocol pass settles meaning/approval | `protocols/checks.py` checks files and research structure, not semantic quality | Owner decision remains pending despite structural pass |

Preferred: explicit selection plus transparent reporting. This fits the accepted
opt-in M2 boundary, reduces hidden context loading and can be verified without
inventing release authority. Cost: authors must make a selection and still review
semantic quality; unsupported native sources remain outside narrative coverage.

Alternative: keep manual guide reading and standalone checker only. Lowest change
cost and fully valid now, but leaves repeated resource-selection work and result
interpretation outside task preparation. Alternative: automatically choose packs
and block lifecycle stages. Less manual work, but requires additional ambiguity,
scope/override and enforcement-policy decisions, and risks false coverage for
native sources; not recommended for this first slice or authorised here.

Inspected planner, SkillLoader, M2 schema/loader/report/check/verify, protocol
lifecycle/checks, relevant tests, resource map, accepted CP/CD/M2 and KDX10 actual
outcomes. Existing tests establish current behavior only; A01-A12 remain planned.
This review does not establish independent reader acceptance, Windows behavior,
authentic external-action qualification, semantic correctness or evidence authenticity.

## Requirements review checkpoint, before owner acceptance

Research method: resolve requirements by source/consumer comparison and contrary
cases, reusing the already accepted checker design. The only material decision
needed for this round is the owner's acceptance/revision of TT01-TT12, including
explicit opt-in, no new default stage gates, supported-format limits and distinct
states. No missing site fact prevents that decision. Safe now: review/revise this
proposal. Held: runtime design until requirements are accepted; code until later
design/plan authority. KDX10 held evidence has its separate owners/actions in its
qualification record.

After acceptance, record the actual words/revision here and follow the standing
validated documentary PR/squash integration convention; present the **design**
task brief next. Design must settle command/API entry points, selection/provenance
representation, bounded resource loading, compatibility and result mapping against
TT01-TT12. Reuse M2; do not reopen accepted CP/CD or implement during design review.
Then produce a bounded plan and run its own prerequisite gate before code.

Requirements drafted; current proposal acceptance pending. No runtime behavior
implemented, no new product tests passed, no current-slice merge or deployment.
Verification receipts and append-only handoff are trace-bound runtime artifacts.
Current checks:187 existing planner/loader/protocol/documentation/M2 tests passed
in5.06s; requirements-skill deterministic evals6/6 passed with zero warnings
(`20261114-084853-eval-ca640f`); project memory validation passed. These are current
compatibility/instruction checks, not execution of the proposed A01-A12 cases.
Recommend GPT-6 Sol medium for the owner review, high for subsequent workflow/state
integrity design; recommendations do not assert active-model identity/availability.
A fresh conversation may help the later design, while this review can continue here.

## Owner acceptance — 2026-11-14

The owner replied **“accepted”** after the self-contained requirements summary.
This accepts TT01-TT12 and A01-A12 revision0.1 without revisions, including explicit
opt-in selection/checking, advisory lifecycle integration with no new default stage
gates, supported-format boundaries and independent outcome/authority states.
Earlier proposed/pending wording records the review checkpoint, not an outstanding
requirements decision. No requirement or acceptance case changed in this update.

Under the standing agreement, this completed documentary slice proceeds through
normal validation, PR and squash integration. Design is the recommended next task,
with its own brief and selection; requirements acceptance does not execute it or
authorise code, live models, automatic enforcement or deployment. KDX10's held
qualification areas remain held. Integration receipts and subsequent continuation
are retained in the exact release trace/handoff rather than guessed in advance.
