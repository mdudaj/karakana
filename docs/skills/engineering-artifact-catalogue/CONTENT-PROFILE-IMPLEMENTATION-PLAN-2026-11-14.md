---
status: ready_for_implementation
question: How should accepted CP01-CP10 and CD01-CD12 be delivered as bounded useful milestones, including the missing explicit-reference mapping shape?
evidence:
  - source: docs/skills/engineering-artifact-catalogue/CONTENT-PROFILE-REQUIREMENTS-2026-11-13.md
    finding: CP01-CP10 and the initial requirements/system-design scope are accepted; implementation is a separate task.
  - source: docs/skills/engineering-artifact-catalogue/CONTENT-PROFILE-DESIGN-2026-11-13.md
    finding: CD01-CD12 is accepted and permits sizing-based delivery splits. It promises explicit source-cell/target mapping but its exhaustive context shape has no edge field.
  - source: pyproject.toml
    finding: Merged M1 declares the optional content/dev parser and packaged profiles. Existing installation/CI paths remain applicable; this amendment changes no dependency or workflow.
  - source: tests/test_engineering_documentation_skills.py
    finding: Tests protect the two-file narrative asset packs and collect legacy examples as P02 inputs; new context examples belong outside those collections.
requirements:
  - decision: Reuse accepted requirements; deliver a usable default-pack checker first, then the remaining tailoring/evidence/freshness capabilities without implying the first milestone implements all CP/CD coverage.
    acceptance: M1 supports both standard narrative packs and refuses nonempty deferred-feature requests. M2 completes the accepted explicit-context design; any reference-edge amendment is separately recorded before it is activated.
    artifact: docs/skills/engineering-artifact-catalogue/CONTENT-PROFILE-REQUIREMENTS-2026-11-13.md
design:
  - choice: Reuse accepted CD01-CD12 and recommend two sequential milestones; propose a context0.2 links array for explicit source-cell/target edges while retaining context0.1 compatibility.
    rationale: Concrete work groups exceed one milestone's sizing target. The small versioned edge shape fulfils an already-described operation without overloading coverage locators or silently changing a strict context0.1 contract.
    artifact: docs/skills/engineering-artifact-catalogue/CONTENT-PROFILE-IMPLEMENTATION-PLAN-2026-11-14.md
artifact_choices:
  - kind: requirements
    disposition: reused
    path: docs/skills/engineering-artifact-catalogue/CONTENT-PROFILE-REQUIREMENTS-2026-11-13.md
    rationale: Actual accepted requirement set; no requirements restart.
  - kind: design
    disposition: updated
    path: docs/skills/engineering-artifact-catalogue/CONTENT-PROFILE-IMPLEMENTATION-PLAN-2026-11-14.md
    rationale: Accepted architecture remains authoritative; this plan records delivery boundaries and one concrete proposed schema clarification with its owner decision.
  - kind: plan
    disposition: updated
    path: docs/skills/engineering-artifact-catalogue/CONTENT-PROFILE-IMPLEMENTATION-PLAN-2026-11-14.md
    rationale: Exact file boundaries, prerequisites, ordered steps, tests, sizing and recovery.
  - kind: schema
    disposition: updated
    path: docs/skills/engineering-artifact-catalogue/CONTENT-PROFILE-IMPLEMENTATION-PLAN-2026-11-14.md
    rationale: Defines milestone capabilities, freshness digest separation and the proposed context0.2 edge shape; production validators/resources are not delivered by this plan.
  - kind: example
    disposition: reused
    path: skills/engineering-requirements/assets/requirements-example.md
    rationale: Both actual accepted narrative examples are baseline controls; the design's concrete context example is reused.
  - kind: test
    disposition: reused
    path: tests/test_engineering_artifacts.py
    rationale: Existing tests remain compatibility controls; this plan maps actual future cases rather than adding wording-only tests.
authority:
  state: approved
  evidence: Owner accepted the reviewed context0.2 links amendment with "accepted" on 2026-11-14 after its self-contained review summary. Existing CP/CD and M1 acceptance remain intact. Standing clarification that accepted work includes normal validated PR/squash integration applies to this completed documentation slice; M2 code execution is a separate next task.
pending_decisions: []
next_action: Complete owner-approved M2 source PR and validated squash integration; release-check/sync and refresh the handoff, then select the next bounded task.
next_action: Complete owner-approved M2 source PR and validated squash integration; release-check/sync and refresh the handoff, then select the next bounded task.
---

# Content-profile checker implementation plan

Revision 0.1, 2026-11-14. Planning trace: `20261114-050550-9e5288`.
Baseline verified after `git fetch origin`: local HEAD and `origin/main` both
`fc93fbcf6b3d7f79fcffa6406c2bfc983b6f3654`. Current branch:
`research/engineering-content-profile-requirements-20261113`. The accepted
requirements and design are local uncommitted documents; preserve them.

Current execution: **M1 is implemented, verified, owner-accepted and squash merged**
through PR38 at `208bf72`; release checks passed. The M2 amendment review is
prepared below and in design revision0.2; its acceptance remains pending. Earlier
plan/local-only wording is retained as history, superseded by the current entries.

This is an implementation **plan**, not code delivery. It reuses
[CP01-CP10](CONTENT-PROFILE-REQUIREMENTS-2026-11-13.md) and
[CD01-CD12](CONTENT-PROFILE-DESIGN-2026-11-13.md), whose owner acceptance is settled.
The architecture-decision protocol is used proportionately for planning against
that existing ADR; it does not reopen architecture approval. The front matter
also records the bounded research-resolution for the schema omission below.

## Delivery choice and estimate basis

Recommend two independently useful milestones. The accepted design explicitly
permits a split when concrete sizing exceeds the repository target. These are
engineering estimates, not measured duration, named-owner commitments or dates.
They cover regression-first implementation; final verification/review is additional.

| Work group | Estimate basis / forecast |
| --- | --- |
| Contract/profile loading, source reader and raw-table consumption | Two profiles, three strict contracts, code/fence/source-map and malformed-row boundaries: 2-3 hours |
| Default record/coverage checks, results and CLI/package integration | Two real source packs, bidirectional IDs/criteria, honest report states, optional dependency/wheel isolation: 2.5-4 hours |
| Tailored source locators, coverage references and omission graph | Unique location resolution, baselines, wrong-kind/cyclic/core-waiver cases: 2-3 hours |
| Open-item/claim mappings and freshness verification | Scoped evidence/unknowns plus changed-input/tamper/recompute paths: 2-4 hours |

Combined forecast is approximately 8.5-14 implementation hours. Split into M1
(4.5-7 hours) and M2 (4-7 hours) to fit roughly half-to-one-day implementation
milestones, followed by their own verification/review. Re-estimate from actual
evidence if a group proves larger; never omit checks to meet the forecast.

| Milestone | Usable result | Held boundary / prerequisite |
| --- | --- | --- |
| M1 — standard narrative packs | Authors can explicitly check requirements and system-design packs, see source-located errors/warnings and unresolved facts, and create immutable current-run reports. | Default profile coverage only. Nonempty `references`, `coverage`, `omissions`, `open_items`, `claims` requests return unsupported; no verification/reuse claim. No `verify` command yet. |
| M2 — tailored sources and verified reports | Authors can check compact/governing views, actual mapped claims/open items and verify saved reports by recomputation. | Starts only after M1 is validated, authorised squash integrated and release checked. The explicit-reference-edge amendment below needs agreement before its use. |

Both milestones preserve narrative-only support in the new checker, P02's existing
structural/export authority, immutable source bytes and accepted CP/CD direction.
M1 is **partial delivery** of the overall checker, not completion of all CP01-CP10.
Its report's existing `coverage` object lists supported checks, unassessed areas and
unsupported requested features. A request for an unavailable feature is an error,
never silently dropped. Every report retains `review_required: true`, readiness
`unresolved`/`not_assessed` and acceptance `not_assessed`. No automatic gates.

Keeping all groups in one PR avoids a temporary capability boundary but exceeds
the sizing forecast and enlarges review. A contracts-only first milestone is
smaller but gives authors no usable check. The selected first milestone produces
an actual author-facing outcome while rejecting requests beyond its support.

## Exact file boundaries

| File | M1 work | M2 work |
| --- | --- | --- |
| `karakana/tools/engineering_content.py` | Thin module CLI, `check_content`, `check`, text/JSON and optional new output; named unsupported command/feature behavior | Add `verify` using the same checker, no trust in a stored passed flag |
| `karakana/content_profiles/__init__.py` | Package boundary; registered profile IDs | No dynamic plugin/custom-profile loading |
| `karakana/content_profiles/schemas.py` | Strict context/profile/report/location types; duplicate/unknown-key/type/version/control-character refusal; reserved advanced arrays rejected when nonempty | Extend typed advanced mappings and agreed context0.2 edge support; retain0.1 compatibility |
| `karakana/content_profiles/loader.py` | Registered ID/version -> fixed packaged JSON resource, strict decoder and caps | No arbitrary resource paths; extend context-version validation only as agreed |
| `karakana/content_profiles/reader.py` | Immutable bytes, token/source maps, headings/anchors, metadata/record tables, raw complete consumption | Unique explicit locator resolution, supported governing sections/cells |
| `karakana/content_profiles/checks.py` | Default slots, IDs/references, required values/substitutions, contextual warnings and visible source-declared gaps | Reference/coverage graphs, conditional rationale, source-mapped open items/observations/decisions |
| `karakana/content_profiles/report.py` | Deterministic findings/coverage, current-run manifest/code/profile/parser fingerprints, original-byte drift recheck | Canonical recomputation comparison and saved-report validation |
| `karakana/content_profiles/requirements-0.1.json`, `system-design-0.1.json` | Two packaged data-only profiles with accepted actual headings/header variants and fixed check IDs | Only necessary capability/rule updates with explicit version/hash compatibility review |
| `pyproject.toml` | Optional `content` extra and dev `markdown-it-py==4.3.0`; explicit package data `"karakana.content_profiles" = ["*.json"]` | No dependency expansion anticipated |
| `tests/test_engineering_content.py` | API/real default packs, source-loss/negative/CLI/immutability/partial-support cases | Extend actual advanced context/evidence/verification cases |
| `tests/test_engineering_content_packaging.py` | Built-wheel resource and optional-dependency/import isolation tests | Verify wheel-installed `verify` also uses packaged profiles/code fingerprints |
| `tests/test_engineering_content_context.py` | Not needed until advanced contexts are implemented | Locator/reference/omission/open-item/claim/cycle/version tests |
| `docs/skills/engineering-artifact-catalogue/content-checks/README.md`, `default-packs.json` | Actual check usage, capability table, read-only default context referencing the accepted assets | Advanced context and verify instructions; explicit version compatibility |
| `docs/skills/engineering-artifact-catalogue/content-checks/tailored.json`, `evidence.json` | Do not create inactive examples | Add working neutral contexts after their supported sources/tests exist |
| `tests/fixtures/engineering_content/compact.md`, `governing.md`, `observations.md` | Use actual accepted assets copied to temporary roots; no new duplicate full pack needed | Neutral actual sources for advanced positive/negative fixtures |
| `docs/engineering-artifacts.md` | Distinguish opt-in narrative checks from P02/export/enforcement; name M1 limits | Update supported features after actual M2 verification |
| Shared/owning `SKILL.md` and requirements/design template guides | Short opt-in guide links and precise support limits; bump changed skill patch versions | Update capability wording without changing existing request/authority rules |
| Shared/owning `evals/content-checks.yml` | Add instruction coverage only for changed skill instructions, including explicit selection and partial-support limits | Update cases for supported advanced features, retaining instruction-only limits |
| `tests/test_engineering_documentation_skills.py` | Extend meaningful guide/discovery linkage if required; keep two-file assets/legacy collections intact | Update only when M2 resources justify coverage changes |
| Accepted CP/CD records and this plan | Carry task authority/history and actual M1 delivery results | Append M2 outcomes, reference-amendment agreement and closeout |

The shared/owning skills are `engineering-documentation-conventions`,
`engineering-requirements` and `engineering-design-records`. Avoid new `.md` files
inside their two-file `assets/` packs or legacy P02 `examples/` collections. Do not
change `karakana/tools/engineering_artifacts.py`, protocol/planner/routing code,
skillpacks, workflow YAML, native stores, existing blank assets or client files.
The three local CP/CD/plan documents belong in the eventual M1 PR; runtime does not.

## M1 execution instructions

Before editing code, load the latest handoff, verify the accepted files and fetched
baseline, read the delivery gate, self-improvement, skill-authoring and UX-writing
instructions applicable to changed guidance. Preserve all three local records.
Use the current non-protected branch or create a feature branch from it without
discarding the documents. Do not mix a second active milestone or parallel PR.

1. Start a new `python-code-change` trace for M1 with an honest medium/high risk
   classification. Review actual inferred artifact flags; new JSON contracts,
   CLI copy and architecture reuse may add schema/UX/ADR evidence. Do not manipulate
   task wording to avoid conditional gates. The artifact map below closes them.
2. Attach accepted requirements/design, this plan and task-selection evidence.
   Run the exact trace's pre-implementation gate; inspect the result and content.
   Resolve missing artifacts before code; a presence pass is not implementation
   approval, a passed test or review. No publication authority is inferred.
3. Add failing real tests and two profile resources. Implement strict JSON parsing
   (including duplicate keys and non-JSON numeric constants), trusted resource
   registry, caps and explicit default-only capability refusal. Profiles are data,
   never executable rules or untrusted import/resource paths.
4. Implement reader/source maps. Require supported complete raw table rows before
   token-derived identities or coverage; reject malformed neighboring rows rather
   than count normalized token cells. Retain heading/anchor uniqueness, code/fence
   exclusion, required text, actual IDs and bounded inventory-based ranges. Decode
   only the supported cell convention; do not reuse an XLSX whole-cell limit for
   an entire narrative document. Keep the accepted 2MB/file and aggregate limits.
5. Implement both default profiles and cross-document requirement/criterion checks.
   Read metadata from source, never from competing context values. Preserve known
   Q-01/Q-02 and design gaps with located unassessed resolution-detail coverage;
   do not mark them resolved. M1 does not validate advanced fact/claim mappings.
   Declared advanced requests or unsupported claim-table shapes cannot pass.
6. Add current-run reports/CLI and drift checks using the existing local root,
   secret-path and no-overwrite guards without changing P02 behavior. Text and JSON
   share findings; JSON stdout has no banners. `check` exit0 means the scoped
   mechanical checks passed, with review/gaps possible; refused/unsupported is2.
   A saved M1 report is historical, with **verification not yet supported**;
   users must run `check` again rather than reuse it as fresh evidence.
7. Add the optional pinned parser extra/dev dependency and JSON package data.
   Once M1 implementation is selected, ordinary in-scope local dependency setup is
   `.venv/bin/python -m pip install -e '.[dev,content]'`. This planning task does
   not run it. Import the optional parser lazily; no implicit install/download.
8. Add working default context and exact capability/CLI guidance. Preserve the
   statement that narrative packs are not P02 structured-export inputs. Patch-version
   changed skills and update only relevant instruction evals/discovery links.
9. Run focused tests while iterating; after stable source, run the full required
   gate once, substantive diff/real-output review, trace completion and handoff.
   Record implemented/verified/merged/deployed/accepted separately. Publish/merge
   only when separately authorised; squash PR and release-check before M2.

## M2 execution instructions and exact dependency

M2 starts from verified, squash-integrated M1 and its release/handoff receipts;
review the actual source and adjust estimates only for new facts. Use its own task
branch/trace/prerequisite gate. Do not carry forward a passed M1 report as evidence
that advanced features or M2 code are verified.

1. Add failing real context fixtures and tests, then unique locator resolution,
   declared governing views, coverage graph/cycles, conditional rationale and
   core-waiver refusal. Empty optional arrays retain0.1 behavior; nonempty arrays
   now run actual supported checks instead of unsupported reporting.
2. Implement source-mapped open-item effects/resolver/action and actual claim fields,
   scoped local evidence hashes and external-evidence limits. Preserve unresolved
   facts; a defined criterion/proposed ADR does not become observed/accepted.
3. After the agreement below, implement explicit reference edges in context0.2.
   Continue reading valid0.1 contexts;0.1 plus a `links` key fails instead of silently
   extending that contract. Add the cross-document/ambiguous syntax controls.
4. Implement `verify` by recomputing via `check_content`, comparing the manifest,
   assessment and coverage, and rejecting stale/tampered/incompatible input. Test
   raw-byte/context/profile/checker/parser/reference changes and within-run drift.
5. Ship working tailored/evidence contexts and updated guide/evals. Re-run actual
   default-pack and P02 compatibility, focused M2 tests then final full gates,
   substantive review and exact-trace handoff. Complete authorised PR/squash/release
   before starting automatic selection/enforcement or another milestone.

### Targeted context clarification for owner agreement

The design's reader/reference section permits explicit source-cell/target locators
for ambiguous/nonstandard references. Its exhaustive context table provides no
field holding both endpoints: `coverage` has a slot and one source; `references`
only registers source files. Do not silently overload either as record edges.

Preferred amendment: optional `links` in **context0.2**, preserving context0.1.
Each entry has exactly `from` and `to`, both existing Locator shapes. `from`
must resolve to a registered reference-bearing source cell; `to` to an actual
declared target record in the selected baseline. No new IDs, facts, severity
overrides or source writes. Reject duplicate edges, wrong kinds/baselines,
unresolved targets and mappings that conflict with canonical IDs. Unmapped or
uninterpretable remaining references remain unsupported, not silently consumed.
References still need substantive review of meaning.

```json
{
  "from": {"document": "req", "heading": ["Functional requirements"], "record_id": "REQ-01", "field": "Acceptance criteria"},
  "to": {"document": "req", "heading": ["Acceptance and verification"], "record_id": "AC-01"}
}
```

Alternative: keep the existing shape and report that reference syntax unsupported;
smaller implementation but it does not deliver the promised explicit disambiguation.
Overloading `coverage` avoids a version but confuses content coverage with record
edges and changes its accepted meaning; not recommended. A universal expression
language is unnecessary scope. Exact decision owner: project owner. Confirm the
small context0.2 amendment before M2 uses it. M1 remains safe independent work;
its0.1 context rejects `links`/0.2 rather than claiming forward support.

### Fingerprint and ordering clarification

Keep byte freshness separate from semantic comparison. `manifest` includes raw
context/source/profile/checker hashes and parser version; any changed byte makes
the corresponding old report stale. `assessment_digest` covers canonical sorted
findings/coverage/identities, excluding generation time and manifest hashes. It
may remain equal when only LF/CRLF or enumeration order changes. `verify` requires
both current manifest **and** recomputed assessment to agree; equal semantic
digests alone never establish freshness. This spells out CP09/CD09 without
contradicting raw hashing or the design's enumeration-order independence.

## Prerequisite artifact map and traceability

### Source-alignment challenge

| Claim / boundary | Producer -> consumer and contrary state | Resolution / evidence limit |
| --- | --- | --- |
| Explicit reference mapping has a representable shape | Accepted CD reference rule -> exhaustive Context/Coverage/Reference types; no type stores both cell and target | The omission is real in the inspected artifact. Proposed0.2 `links` shape is concrete and held for owner agreement; no claim that a new validator already supports it. |
| Source-tree resources prove installed profiles work | New profile JSON -> setuptools package discovery -> installed reader; a source import can succeed while a wheel omits JSON | Existing pyproject has no content package data. Actual wheel/target import is a required implementation check, not a planning result. |
| Semantic equality establishes freshness | `_sha(raw)` preserves bytes; canonical findings may stay identical after LF/CRLF/context enumeration edits | Compare raw manifest and assessment separately. Current parser probes support semantic equivalence; the new verify path still requires implementation/tests. |
| M1 can appear to support deferred context features | Strict context -> proposed checker -> coverage report; ignored nonempty arrays could produce a false complete result | M1 must refuse requested unavailable capabilities and explicitly list assessed scope; this is an unrun acceptance case, not delivered behavior. |
| Optional dependency and tests are already ready | Actual pyproject/environment -> future dev install/test/CI | Parser4.2.0 is available only incidentally; build module absent. Plan uses available pip backend and requires actual4.3.0/installed-wheel qualification later. |

| Gate kind / concern | Actual governing artifact or implementation evidence |
| --- | --- |
| Requirements/PRD, acceptance, DoD | CP record for problem/readers/outcome and CP01-CP10; this plan for the selected milestone's exact support and exit criteria |
| ADR/architecture | Accepted CD record; this plan records permitted sizing split and the proposed M2-only amendment |
| User stories | Author: check the supported document against selected content rules without altering sources. Reviewer: distinguish findings/gaps from approval and, in M2, verify current inputs rather than trust a saved pass. |
| Schema/example | CD context/profile/report contracts and real embedded default context; M2 amendment/edge example here. Production schemas/fixtures are to be implemented, not already present. |
| Requirements traceability | CP01/02/10 -> schema/loader/reader/CLI/package and refusal/isolation cases; CP03/04/05 -> profiles/checks and real coverage/ID cases; CP06/07/08 -> source gaps/warnings then M2 evidence mappings; CP09 -> manifests/current-run drift then M2 verification. |
| Artifact readiness | Accepted CP/CD, current plan, source reconciliation, actual task selection and required attach/check receipts. No reliance on future nonexistent paths. |
| UX/accessibility | CD CLI states/copy and this support boundary; severity/location/action in text, stable JSON, no color-only meaning or sensitive cell excerpts. Record real stdout/stderr captures as output evidence; no GUI/browser render applies. |
| Migration/rollback if inferred | New opt-in contracts only, no migration of native stores/P02 sources.0.1 remains supported;0.2 amendment is explicit. Reviewed revert/fix PR; preserve sources/reports/runtime. |
| Safety/threat/approval if inferred | Read-only roots, symlink/secret/size checks, no remote/HTML/code/model execution, immutable reports and no trust in self-authored pass. Owner's selected implementation scope supplies in-scope authority, not external permissions. |
| Delivery outputs | Actual changed-file summary, test/eval/CLI/wheel receipts and source-preservation evidence appended to this compact delivery record, plus exact-trace handoff. |

Attach multiple relevant files where needed rather than claiming one unrelated
file satisfies everything. Use `protocol missing/template/attach` for the actual
implementation trace's kinds, then `protocol check --stage pre-implementation`
before code and completion after actual verification/handoff. CLI render captures
are delivery outputs, not fabricated prerequisite screenshots. An attachment
proves neither semantic quality, test success nor valid authority.

## Test and verification plan — commands are unrun for the checker

| Check | Cases / expected observation |
| --- | --- |
| M1 real inputs | Both actual accepted packs copied to temporary roots; metadata/IDs/criteria retained; Q/gap visibility and review-required state; root fixtures never rewritten |
| M1 loss/negative cases | Empty/heading-only/placeholder content; duplicate/missing IDs; dangling/wrong-baseline references; short/wide/malformed neighboring rows; fences/quoted/code examples; literal syntax and actual product approval behavior |
| M1 support and I/O | Nonempty reserved arrays, unsupported P02/format/version/capability and verify request refuse honestly; actual API/CLI agreement; JSON stdout; dependency absence without breaking P02; roots/symlinks/secret paths/size/drift/overwrite refusal |
| M2 tailoring | Actual compact/governing views, unique selectors, absent/ambiguous/wrong-kind locators, cycles, conditional rationale and core-waiver refusal; agreed0.2 edges and0.1 compatibility |
| M2 claims | Planned versus actual results/decisions; missing actor/revision/time/environment/evidence; local evidence mutation/unavailable external evidence; unknown effect/resolver/action; unrelated scope remains independent |
| M2 freshness | Source/context/profile/checker/parser/reference changes, changed hashes despite equal semantics, report tampering, within-run drift, ordering stability, LF/CRLF and no source rewrite |
| Both packaging/compatibility | Built wheel contains both JSON profiles and runs outside checkout; optional dependency metadata/import behavior; legacy examples/blank assets/P02 API, exports, feedback and native authority retain expected results |

During M1: `.venv/bin/pytest -q tests/test_engineering_content.py tests/test_engineering_content_packaging.py`.
During M2 add `tests/test_engineering_content_context.py`. Stable focused gate for
each milestone also includes `tests/test_engineering_artifacts.py`,
`tests/test_engineering_documentation_skills.py`, `tests/test_engineering_artifact_pilots.py`
and changed discovery/link tests. Use actual assertions on outputs/data/refusals,
not tests that merely mirror implementation or match planning text.

Wheel qualification is an actual temporary build/install/import test, not a source
tree import. Use `isolated_repo` or a public-source-only temporary copy and run
`.venv/bin/python -m pip wheel --no-deps --no-build-isolation --no-index --wheel-dir <temp-wheels> <temp-source>`.
Install that wheel with pip `--no-deps --no-index --target <temp-site>` and run an
isolated subprocess outside the checkout, putting only that target before ordinary
runtime dependencies. Assert module locations come from the target and load the
two registered resources using positional `importlib.resources.files(...)`.
Do not let an editable source import mask missing wheel data. Inspect wheel
METADATA for the optional parser extra. Missing-parser subprocess/import tests
must actually block that import, not just assert a help string.

Local planning preflight found pip26.2.1, setuptools84.0.0, wheel0.47.0 and parser4.2.0;
`build` is absent. The commands above use available pip/build backend, not an
assumed `python -m build`. Implementation installation must qualify the selected
4.3.0 dependency. Package-data/runtime-reading method is grounded in the official
[setuptools data-file documentation](https://setuptools.pypa.io/en/latest/userguide/datafiles.html)
and [Python resource API](https://docs.python.org/3/library/importlib.resources.html).
Use a fixed registry, never user-controlled resource paths. No dependency or build
was performed by this planning task.

For each stable milestone run `.venv/bin/pytest -q`,
`.venv/bin/karakana skill validate-all`, applicable skillpack validation and
`.venv/bin/karakana eval run`; use focused skill evals while editing instructions.
Record instruction evals as source-text coverage, not model behavior. Review actual
CLI outputs, profile/rule coverage, wheel resources and source-preservation evidence.
Tests use `tmp_path`/`isolated_repo`; subprocesses also run there because the checkout
runtime guard is not a subprocess sandbox. No real model calls or Windows install
qualification are implied by portable LF/CRLF fixtures.

Before integration: whitespace/diff review, all blocking findings resolved and
actual completion gate/handoff. With separate remote-write authority, publish a
single PR, validate its exact head, squash merge and release-check/sync. Do not
start M2 while M1 integration is pending. Record product/independent acceptance
separately from implementation, verification, merge and deployment.

## Recovery, current verification and exact next action

No existing database/source migration is required. A failed diagnostic loop gets
two evidence-backed attempts, then replan; do not switch models or fan out agents
automatically. Revert/repair through a reviewed PR, retaining original sources,
reports, feedback and append-only runtime. Do not reset/delete history or restore
silent acceptance as a shortcut. A dependency/package regression can be repaired
or reverted with the new optional feature without changing base/P02 dependencies.

Verified for this planning task: fetched baseline/branch and accepted CP/CD history,
actual source/helpers, package configuration, test isolation/asset collection,
available build tools and instruction eval boundaries. New uncertainty was the
missing explicit-reference edge shape; the preferred proposal and exact M2 owner
decision are concrete above. Check local references, embedded JSON, accepted-ID
coverage, whitespace and exact-trace completion/handoff before ending. No new
checker tests/full suite/build are claimed run. Reuse the recorded 140 compatibility
tests and actual parser probes as context, not as implementation verification.

M1 has no outstanding design choice; it needs normal task selection and its own
prerequisite gate. M2 has the exact context0.2 agreement described above, owned by
the project owner; no vague design handoff or broad requirements/design restart.
Recommended next task: **implement M1 standard narrative-pack checker**. First
action: load current handoff and this plan, preserve the three local docs, select
the M1 task branch/trace and close its pre-implementation artifact gate.

Planning/model recommendation: GPT-6 Sol high for integrity-sensitive implementation;
a fresh conversation benefits the implementation boundary with CP/CD/plan reuse.
This is not an observed model switch or availability claim. No implementation,
new PR/merge/deployment, live call or client revision occurred here. Remaining work:
M1, authorised M1 integration, M2 after its agreement/dependency, then the original
automatic selection/enforcement, remaining templates/exports, pilot and Jovina.

Planning completion protocol check passed for trace `20261114-050550-9e5288`
(artifact-presence evidence only). The nested research closeout was separately
validated for structure/local paths, with `decision_required` for the exact M2
amendment. Neither check certifies implementation or grants code/remote authority.
Final append-only handoff carries the complete M1 brief and M2 owner decision.

## M1 local delivery results — 2026-11-14

Owner selected M1 with **“execute”** after the completed plan. Implementation
trace: `20261114-055012-b0306c`, high-risk `python-code-change`; task branch
`feat/engineering-content-checker-m1-20261114` from `fc93fbc`. Pre-implementation
gate passed before code (`20261114-055059-protocol-check-641500`). This authority
covered local M1 and routine optional-dependency setup, not M2/links0.2, remote
publication, source integration, deployment or live model calls.

Implemented the named module/API, six content-profile Python modules and two
packaged data-only JSON profiles; strict context/schema/version and raw table
consumption; default record/coverage/reference checks; located warnings/gaps;
immutable current-run text/JSON reports with byte/code/profile/parser fingerprints.
Deferred mappings/unsupported shapes and verify refuse explicitly. Failed-source
assessments remain visible. Within-run code/profile/source and pre-output drift
(including equal-byte symlink retargets) refuse. No source/approval state is changed.

Added the optional content/dev pin to markdown-it-py4.3.0 and JSON package data;
workbooks/base dependency declarations remain separate. Three experimental owning/
shared skills received patch versions, opt-in guide links and instruction-only
evals. Added a neutral default context and guide outside the protected asset/
legacy-example collections. Generated index was reconciled without an index diff.

Verification actually performed:

- Regression-first collection initially failed for the absent module; new actual
  consumer tests now pass. A code-drift counterexample exposed the need for a
  before/after checker fingerprint; that mechanism and regression are included.
- Final **885 full tests passed in 23.50s**, including **67 new cases**, actual wheel
  build/install/import outside the checkout, optional-parser blocking with P02
  Markdown still working, API/CLI/refusal/immutability and negative input cases.
  Earlier expanded focused gate: 232 passed; final full gate includes subsequent
  malformed JSON/profile-data controls. No tests write working-checkout runtime.
- **186/186 deterministic evals passed, zero warnings**. Receipt:
  `.karakana/eval-runs/20261114-062508-eval-f9fd91/`. Instruction cases do not claim
  model authoring quality. Skill and skillpack validation passed; no warnings.
- Actual module CLI checked both accepted examples and wrote a new JSON report
  matching stdout; text output retained seven source gap entries, readiness
  unresolved, acceptance not_assessed. Verify exited2 with the explicit M1 refusal.
  CLI evidence: `.karakana/reviews/20261114-content-m1/cli-evidence.md`.
- Sixteen original assets/legacy examples and the existing P02 module are
  byte-identical to captured baseline hashes. Root/secret/symlink/size/drift,
  malformed rows/IDs/references, literal code and product-approval controls passed.
  Source footprint and whitespace reviewed; no protected subsystem, workflow,
  skillpack, native store or client changes. No native Windows installation
  qualification is claimed; tests exercise actual LF/CRLF bytes.

The compact runtime delivery record and reviewed hashes live under
`.karakana/reviews/20261114-content-m1/` and are not committed. Actual source review
is self-review, not independent acceptance. M1 implements only its declared partial
capabilities; M2 remains queued behind authorised M1 squash integration/release
checks and its exact reference-edge agreement.

Current states: implemented and verified locally; uncommitted/unpublished, no new
PR or merge, no deployment. Owner selected implementation; independent product/
standards acceptance is unclaimed. Recommended next task: review M1 source and
verification evidence, then separately authorised PR publication/squash integration.
Completion protocol/handoff receipts are recorded in the task-bound runtime record.

## Owner M1 delivery acceptance — 2026-11-14

After the completion summary reporting885 passing tests,186 passing evals and
the local uncommitted state, the owner replied **“accepted.”** This accepts the
verified local M1 delivery for this round without revisions. CP01-CP10 and
CD01-CD12 acceptance remains intact. This is scoped owner delivery acceptance,
not independent technical review or standards certification.

Next task remains source/evidence review and separately authorised PR publication/
squash integration. Acceptance alone does not select remote writes, deployment,
M2 implementation or the proposed context0.2 links amendment. The M2 dependency
and exact owner decision above remain outstanding. No code/dependency/test edits
occurred in this acceptance-record update; prior885/186 evidence is reused.
Owner statement/scope, source hashes, closeout structure and whitespace were
verified; append-only task-bound handoff refreshed for integration continuation.

## Source-integration approval clarified — 2026-11-14

The owner stated **“squash merge, thats approved means.”** This confirms that
acceptance of this completed M1 delivery includes its normal task-branch commit/
push, PR publication and squash integration after validation. The earlier
local-only interpretation is superseded for M1 integration; do not request the
same approval again. Acceptance of a requirements/design round remains scoped to
that round, and no deployment or M2/context0.2 authority is inferred here.

Carry this concrete agreement into the PR and handoff. Complete current source
review, exact-head CI and guarded squash, verify resulting tree/parent and clean
main synchronization, then release-check and refresh continuation. Prior885 tests/
186 evals are reused only after source-hash reconciliation; publication-note
changes do not replace that review or imply independent technical acceptance.


## M1 merge receipt and M2 amendment review — 2026-11-14

M1 integrated through [PR38](https://github.com/mdudaj/karakana/pull/38), squash
`208bf72b11d9178696fa904f7eec133cfa012d20`, parent
`fc93fbcf6b3d7f79fcffa6406c2bfc983b6f3654`, reviewed tree
`1ec24a94fb239083a94fe5c5c6eec4a3be75b9e6`. Exact-head CI, tree/parent proof,
postmerge release and CLI checks passed; main was clean/synced before this review
branch. Prior885 tests/186 evals are M1 evidence, not M2 results. No deployment.
M1 integration is satisfied; earlier integration-pending instructions are history.

Owner selected this amendment review with **“execute”** after the next-task brief.
Trace: `20261114-071536-43dc7e`; branch:
`docs/content-m2-links-amendment-20261114`. The governing proposed contract is
[design revision0.2](CONTENT-PROFILE-DESIGN-2026-11-13.md#m2-reference-link-amendment--revision-02-proposed-2026-11-14).
It expands the earlier two-endpoint sketch with exact cell/record resolution,
registered field kinds, one-to-many sets, canonical-reference conflict handling,
non-ID row anchors, version compatibility and executable acceptance cases.
Requirements CP01-CP10 remain accepted unchanged. This review selects a concrete
preferred proposal, not owner acceptance of its resulting revision or M2 code.

### Incremental M2 implementation instructions after agreement/task selection

1. Inspect accepted CP/CD, the revision0.2 contract, this plan, actual
   `karakana/content_profiles/{schemas,reader,checks,report,loader}.py`, both
   packaged profiles, `karakana/tools/engineering_content.py` and
   `tests/test_engineering_content*.py`. Reuse M1 outcomes; inspect affected
   producer/consumer interfaces rather than repeating broad research.
2. Record the actual owner decision and affected revisions here and in CD; start
   M2's own implementation trace/branch after this documentation slice has been
   accepted/integrated. Close its pre-implementation artifact gate before code.
3. Add actual regression cases in `tests/test_engineering_content_context.py` for
   version0.1 refusal/compatibility and the revision0.2 case list. Implement strict
   typed locators/links in schemas, actual anchor-to-cell/source mapping in reader,
   registered field-to-record-kind relationships in the profile/check layer and
   canonical/explicit graph reconciliation in checks. No duplicate fact store.
4. Preserve the remaining accepted M2 work in the existing execution instructions:
   governing coverage, conditional omissions, open-item/claim evidence and saved
   report verification. Include every read source/context input in the raw manifest,
   and recompute the semantic assessment. An unchanged digest is not freshness.
5. Run focused content/context and P02/source-compatibility tests, then the existing
   full pytest, validation/eval, actual CLI/wheel and source-preservation gates.
   Review source-located failures, positive/negative context cases and both byte
   and semantic drift. Use temporary roots for tests; no working runtime fixtures.
   Actual commands/results must be appended at delivery, not inferred from this plan.

Artifacts: reuse CP and accepted CD reasoning; update only this plan and CD's
schema/example/review appendix, plus CP's current continuation/history. No new
PRD/ADR file, workbook, GUI/render artifact, dependency, migration or production
schema is needed for this documentation slice. Local references, example JSON,
whitespace and relevant existing M1 checks are the proportional verification.

Research outcome: **decision_required**; implementation readiness: **false**.
Exact owner/action: project owner accepts or revises design revision0.2 links
contract, or chooses retained unsupported custom syntax. Then record that choice
and select M2. This is the only open amendment decision. No code/skill/workflow,
publication, merge, deployment or live-model change occurs in this review task.
Recommendation: GPT-6 Sol high for integrity-sensitive implementation after its
prerequisites; continue this conversation for scoped design acceptance, with a
fresh conversation useful for the subsequent implementation boundary.


## Owner amendment acceptance — 2026-11-14

The owner replied **“accepted”** after the completed amendment review summary.
This accepts design revision0.2's context0.2 `links` contract without revisions:
unique source cells, one-to-many target sets, registered target types/baselines,
anchors for non-ID rows, canonical-reference reconciliation and context0.1
compatibility. The original CP01-CP10/CD01-CD12 acceptance and tailored standards
remain intact. Earlier proposed/pending/readiness-false entries are review history;
this scoped acceptance supersedes them for the amendment decision.

Acceptance trace: `20261114-072153-949637`. Research outcome is now
`ready_for_implementation` for the resolved design/plan, with no material amendment
decision outstanding. This readiness does not execute M2 or claim that its code,
new tests or verification are delivered. The owner's standing clarification that
accepted work includes its normal validated PR/squash integration is applied to
this completed documentation slice. Complete that integration, then present the
M2 implementation brief; deployment and live model calls remain separate.

Only acceptance/continuation metadata and this history entry changed after the
reviewed proposal. Reuse its66 passing content tests and source-backed review;
validate current YAML/JSON/links, diff scope and acceptance consistency before
integration. Do not repeat the already accepted requirements/design review or ask
again for M1 integration or this amendment's acceptance.


## M2 execution selected — 2026-11-14

Owner selected the completed M2 implementation brief with **“execute”**. Trace
`20261114-072845-d267f5`; branch `feat/content-m2-contexts-verify-20261114` from
`af27b67` (PR39). Accepted CP/CD/revision0.2 govern without reopening design.
This selects in-scope implementation, temporary regression fixtures, verification
and review; normal validated integration follows owner acceptance of delivery.
No deployment/live model calls or automatic task enforcement are selected.

Implementation follows the existing file/test boundaries. The reader will retain
actual heading paths/anchors and registered raw-table cells; context resolution
and graph/evidence checks may use a small owning module in content_profiles,
included in the checker fingerprint. References remain bounded local reads.
Review source-kind/baseline and canonical-ID reconciliation on the resolved graph;
verify recomputes all report assessment fields and raw manifests, never trusting
a supplied digest or passed flag. Invalid/incompatible reports refuse explicitly.

Reuse accepted CLI diagnostic requirements and ux-writing's source-located,
actionable state-copy pattern; no GUI or render artifact applies. Research/ADR/
requirements/standards are settled and reused. New implementation facts or
necessary choices are recorded here with their evidence and limits.


## M2 local delivery results — 2026-11-14

Implementation trace `20261114-072845-d267f5`; prerequisite gate passed before
code (`20261114-073043-protocol-check-a3db71`). Owner's **“execute”** selected this
M2 delivery against the settled artifacts. Branch:
`feat/content-m2-contexts-verify-20261114`, base `af27b67` (PR39).

Delivered strict advanced context0.1/0.2 schemas and actual heading-path/anchor/
registered-cell source maps; governing coverage and cycle/conditional-omission
checks; version0.2 from/to edges with canonical-set, kind, baseline, uniqueness
and graph reconciliation; located open-item effects/resolver/action/affected
scopes; observed-result/decision fields, timezone-aware time and local evidence
hashes/external-evidence limits. `verify_report` and module `verify` recompute
current input manifests and every persisted assessment/status/coverage field;
forged digests/pass flags, report tampering, byte drift and incompatible report
versions refuse. Context0.1 remains supported; even empty links requires0.2.
Report0.2/checker0.2.0 are explicit; M1 report0.1 must be regenerated, not upgraded
silently. Packaged profiles and dependency pins remain unchanged.

Added working neutral compact/governing/observation/evidence fixtures and tailored/
evidence contexts outside protected asset/legacy-example collections. Updated
three experimental skill patch versions, their instruction-only evals and owning
references, shared contract and guide. Generated skill index reconciled with no
diff. P02/native/export/feedback, workflow/protocol/model policies and clients are
unchanged. Nothing runs automatically and no remote/model/evidence fetch is added.

### Source-alignment closeout and regression evidence

| Material claim / contrary probe | Source producer -> consumer | Resolution and artifact choice |
| --- | --- | --- |
| Non-ID design rows and renamed/repeated headings can select one actual cell | reader source paths/anchors/raw tables -> context resolver -> typed graph checks | Actual row/cell anchors, full heading paths, ambiguous-selector and normalized duplicate-edge cases implemented; no new native IDs or fuzzy/row-number selector. Reuse accepted locator contract. |
| Governing records might be mistaken for copied facts or lose baseline authority | selected raw Source rows -> canonical physical identity/checked baseline owner -> reference/effect checks | Keep physical path/line, resolve authority from declared checked views; same physical record reused is not a new record, while competing physical IDs still fail. Positive/negative fixture tests and code encode this implementation choice. |
| Optional mappings could hide existing content or unknown effects | native table inventory/default gaps -> coverage projections/open-item enrichment | Preserve original declared rows; refuse unselected native tables. Enrich a canonical gap once instead of suppressing it. Two cell selectors cannot overwrite one row's affected scope. New counterexamples failed before their fixes and pass afterward. |
| A test result could supply accepted-decision evidence | declared claim kind/location -> accepted-decision row check | Require decision-kind coverage; wrong-kind counterexample reproduced and now refuses. Fields/hashes show declared provenance only, never authenticity or checker-granted approval. |
| Saved semantic equality/digest could certify freshness | all source/context/evidence/profile/code/parser bytes -> manifest plus recomputed report | Exact raw comparison AND all assessment/status fields required. Changed evidence, LF/CRLF, order-only changes, parser/profile/code/source drift, tampered or deep malformed reports covered. JSON nesting bounded64; strict schema/unknown-key/caps preserved. |

Research/method outcome is resolved using the accepted contracts and existing
plan; no new material owner choice or external-framework research was needed.
Requirements CP01-CP10 and design/revision0.2 are reused; schema/example/test/UX
and delivery documentation now reflect actual implementation. An extra ADR/PRD,
GUI/render record, migration or workbook is not applicable. The implementation
choices above do not change source authority or accepted requirements.

### Verification actually performed

- Final **961 tests passed in25.66s**, including **76 new cases** over baseline885.
  Focused compatibility gate passed278 before later integrity cases; final full
  gate includes all subsequent fixes and wheel qualification. New tests assert
  actual consumer behavior rather than planning text.
- **186/186 deterministic evals passed, zero warnings**; final receipt
  `.karakana/eval-runs/20261114-075135-eval-c5c8a3/`. Skill and skillpack validation
  passed. Instruction cases cover source text, not model execution or authoring quality.
- Actual built wheel installed into a temporary target outside the checkout ran
  default check plus tailored/evidence check and API/CLI verify. Optional parser
  imports were actually blocked in a separate installed subprocess; P02 Markdown
  still worked. No dependency expansion or native Windows install claim.
- Actual final module CLI checked/wrote/verified default, tailored and evidence
  contexts. Defaults kept7 gaps, evidence kept1 and1 declared claim; acceptance
  stayed not_assessed/review_required true. Tailored had no declared gaps and
  readiness not_assessed. Runtime receipts: `.karakana/reviews/20261114-content-m2/`.
- All16 protected originals (accepted assets, P02 module, legacy examples, native
  fixtures and workbook/template) remain byte-identical. Actual LF/CRLF fixtures
  exercise semantic equality with raw staleness. Guide links/JSON/context sources,
  diff scope and whitespace checked. No test writes checkout runtime.

Final source review is agent self-review, not independent acceptance or standards
certification. Evidence locations/declarations do not authenticate facts; omission
applicability, unmapped prose and substantive adequacy remain review concerns.
Raw reports are not signed attestations. No unresolved implementation blocker is
known; no M2 PR/merge/deployment has occurred. Current delivery is local/uncommitted,
implemented and verified; owner acceptance of this completed M2 is next. Under the
standing clarification, that acceptance includes normal commit/push, exact-head
CI, guarded squash and release/sync without another approval loop. No deployment
or live calls follow. After integration, automatic selection/enforcement and other
packs/exports/pilot/client work remain separate queued tasks.

Recommended next task: review completed M2 source/evidence here, then integrate
accepted work. Exact next action: owner accepts or states delivery findings; record
that decision, close any actual issue and complete the normal validated PR/squash.
Recommend GPT-6 Sol high for integrity-sensitive review/integration; continue this
conversation for acceptance, with a fresh conversation useful after integration.
Advice only: no observed model switch or availability claim. Completion protocol
and final exact-trace handoff receipts live in the runtime delivery record.


## Owner M2 delivery acceptance and integration approval — 2026-11-14

The owner replied **“accepted, squash merge”** after the completed M2 delivery
summary (961 passing tests,186 passing evals and the local uncommitted state).
This accepts the verified M2 delivery without revisions and explicitly authorises
normal task-branch commit/push, PR publication, exact-head validation and squash
integration. No separate integration confirmation is outstanding. CP/CD/revision0.2
acceptance remains intact; this is owner delivery acceptance, not independent
technical review or standards certification.

Release trace: `20261114-075748-428824`. All30 delivered file hashes and16 protected
originals were reconciled before this acceptance-only update. Reuse the existing
961-test/186-eval and actual wheel/CLI evidence; code/tests/fixtures/skill content
remain unchanged. Complete guarded squash and verify reviewed tree/sole parent,
clean synced main and release checks; record actual outcome in the append-only
handoff. Deployment, live model calls and later automatic selection/enforcement
or client/pilot work remain separate. Earlier delivery-pending/local-only states
are history, superseded by this scoped acceptance and later merge evidence.
