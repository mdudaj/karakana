---
status: decision_required
question: How should accepted CP01-CP10 and CD01-CD12 be delivered as bounded useful milestones, including the missing explicit-reference mapping shape?
evidence:
  - source: docs/skills/engineering-artifact-catalogue/CONTENT-PROFILE-REQUIREMENTS-2026-11-13.md
    finding: CP01-CP10 and the initial requirements/system-design scope are accepted; implementation is a separate task.
  - source: docs/skills/engineering-artifact-catalogue/CONTENT-PROFILE-DESIGN-2026-11-13.md
    finding: CD01-CD12 is accepted and permits sizing-based delivery splits. It promises explicit source-cell/target mapping but its exhaustive context shape has no edge field.
  - source: pyproject.toml
    finding: No content extra or packaged content-profile resources exist. Dev installation is the existing CI dependency path; no workflow change is needed.
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
  state: pending
  evidence: Owner selected and accepted verified M1, then clarified "squash merge, thats approved means" on 2026-11-14. M1 task-branch commit/push, PR publication and validated squash integration are authorised without another confirmation. M2/context0.2, deployment and live model calls remain separate.
pending_decisions:
  - owner: Project owner
    question: Accept the proposed context0.2 links array for M2 explicit-reference mappings, or retain unsupported reporting for that syntax?
    next_action: Review the small proposed shape and alternatives below; record agreement before M2 implementation. This decision does not block M1.
next_action: Complete the authorised M1 PR and validated squash integration, then release-check/sync and refresh the handoff. M2 amendment agreement remains separate.
---

# Content-profile checker implementation plan

Revision 0.1, 2026-11-14. Planning trace: `20261114-050550-9e5288`.
Baseline verified after `git fetch origin`: local HEAD and `origin/main` both
`fc93fbcf6b3d7f79fcffa6406c2bfc983b6f3654`. Current branch:
`research/engineering-content-profile-requirements-20261113`. The accepted
requirements and design are local uncommitted documents; preserve them.

Current execution: **M1 is locally implemented, verified and owner-accepted**; see the delivery
results at the end. Earlier plan-only wording is retained as history.

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
