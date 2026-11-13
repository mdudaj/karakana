# Engineering documentation conventions and templates

Research and implementation proposal, 13 November 2026. Research trace: `20261113-110352-78004f`. This records research and a proposed direction; it does not activate new skills, change client documents, or authorise implementation.

Current continuation: the owner accepted the requirements and design directions
and selected CT01–CT08 implementation. That slice is locally implemented and
verified; [delivery results](#convention-and-templates-delivery-results) distinguish
it from integration and sample acceptance. The [bounded implementation plan](#bounded-convention-and-templates-plan)
and original research remain below with their authority/history preserved.

## Recommendation

Support each engineering documentation skill with a versioned content template, examples and executable checks. Reuse the five existing engineering skills. Add one shared `engineering-documentation-conventions` coordinator for common language rules and document selection. Keep presentation templates separate from content rules.

The intended result is consistent, relevant engineering documentation: purpose, technical content and evidence appropriate to the document. Meeting chronology and document approval arrangements belong in their own records when needed. Actual product approval workflows, audit requirements and operational authority remain valid engineering content.

Templates can make structure and checks deterministic. They cannot establish that a technical claim is true or a document is useful without evidence and substantive review.

## Research basis

The [Agent Skills specification](https://agentskills.io/specification) supports instructions with references, scripts and assets. Its [authoring guidance](https://agentskills.io/skill-creation/best-practices#templates-for-output-format) recommends concrete output templates and validation loops. This supports linking a skill to an explicit template instead of relying on general prose instructions.

[arc42](https://arc42.org/overview/) separates architecture concerns and supports tailoring. Its [download variants](https://arc42.org/download/) distinguish templates with authoring help from clean versions. Use that separation for guidance versus issued content; do not force every architecture section into every artifact. No third-party template was copied. Redistribution of an arc42 adaptation would require review of its [licence](https://arc42.org/license/).

[Diataxis](https://diataxis.fr/) distinguishes instructions, reference and explanation by reader need. [NASA's requirement checklist](https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/) supports concise, unambiguous and verifiable requirements; its [verification matrix guidance](https://www.nasa.gov/reference/appendix-d-requirements-verification-matrix/) connects requirements to verification. These inform our local convention rather than impose their organisational processes.

The public [ISO/IEC/IEEE 15289 abstract](https://www.iso.org/standard/74909.html) supports purposeful document types. The full standard was not reviewed; this proposal makes no standards-conformance claim. [JSON Schema annotations](https://json-schema.org/understanding-json-schema/reference/annotations) do not themselves validate content. Actual assertions are needed. [Vale's scoped checks](https://docs.vale.sh/topics/styles) are a useful diagnostic model; Vale need not become a mandatory dependency.

## Current implementation and confirmed gaps

| Area | Evidence | Implication |
| --- | --- | --- |
| Catalogue | Five engineering skills exist and are experimental, optional entries in `skillpacks/karakana.yml`. | Extend these skills rather than create competing versions. |
| Template | `TEMPLATE.md` is an extensive internal artifact/review library. | It is not a concise client template for each document type. Retain its existing uses. |
| Selection | `karakana/cli.py` defaults to the first required skill; `karakana/agents/planner.py` loads one selected skill and asks for a generic implementation plan. | Documentation needs explicit type/profile selection at task time. Optional catalogue membership is insufficient. |
| Source contract | `karakana/tools/engineering_artifacts.py` checks structure, references and records. Its projections include internal status/control material. | Add an explicit client projection; retain real internal authority records. |
| Protocol | `karakana/protocols/checks.py` normally checks artifact presence. | An attached file alone does not prove content conformance. |
| Evals | `karakana/evals/runner.py` can judge prompt-file text; existing engineering requirement cases label themselves instruction coverage. | Keep these tests, but add generated-artifact fixtures and integration checks. |
| Hooks | `.codex/hooks/karakana_session_start.sh` loads a handoff and can exit successfully after reporting a missing CLI. | Session loading does not enforce document selection or final checks. Do not equate hook completion with validation. |

Isolated temporary-repository probes confirmed:

- A requirements protocol accepted an attached file containing only meeting-arrangement prose. The result explicitly covered artifact presence.
- A structurally valid requirement row containing meeting-arrangement prose produced one parsed record and no validation issues.
- The identical source with CRLF instead of LF produced zero requirement records and no issues. Structured requirements were treated as narrative. This is a parser defect, not evidence that Windows is unsuitable for authoring.
- The generated skill index matches source; the five optional skills do not automatically replace the default `delivery-artifact-gate` selection.

The probes did not change skills, source code or client artifacts. Focused pytest execution could not start because pytest is absent from the inspected Python environment. Direct probes ran successfully; no regression-suite result is claimed.

## Content template catalogue

| Document | Owning skill | Minimum content |
| --- | --- | --- |
| Requirements specification | engineering-requirements | Purpose and scope; system context; functional requirements; measurable quality requirements; interfaces and constraints; acceptance/verification references; declared unresolved parameters. |
| System design | engineering-design-records | Context and boundaries; solution structure; data and interfaces; key runtime flows; deployment; security; quality decisions and trade-offs. Tailor sections to the system. |
| Implementation plan | engineering-delivery-planning | Delivered scope; dependencies; sequenced work; responsibilities; acceptance evidence; rollout and recovery references. |
| Release notes | engineering-release-documentation | Product and version/date table; delivered capabilities; relevant compatibility/deployment information. Distinguish initial release from changes to a previous release. |
| User guide | engineering-release-documentation | Role-based journeys; prerequisites; numbered actions within procedures; expected results; useful recovery guidance. |
| UAT pack | engineering-requirements with engineering-workbooks | Journey and requirement coverage; setup/data; actors; actions; expected results; actual results and findings fields. Include setup, approvals, collection, monitoring and reporting where delivered. |
| Deployment/recovery runbook | engineering-release-documentation with engineering-delivery-planning | Preconditions; ordered commands/actions; stop conditions; verification; recovery limits and steps. Preserve actual operating authority. |

Each template pack should contain a purpose/audience definition, clean source outline, separate authoring help, statement patterns, synthetic good/bad examples, machine-checkable profile, presentation mapping, and evaluation fixtures. Short patterns may be inline in the skill; substantial templates belong in its assets. Avoid a universal template that inserts irrelevant sections.

For example, a requirement pattern is: `The system shall [observable behaviour] when [condition], verified by [test or inspection reference].` A valid alternative may be needed for a constraint; do not force every sentence into this pattern. `We will arrange a meeting to agree the requirements` is authoring activity, not a system requirement. A requirement that the application records independent approval is valid product behaviour.

Client language should be direct and neutral. Show document revision, applicable product release and date where relevant. Do not automatically print `Draft for review`, reviewer nominations, repeated approval disclaimers or meeting history. Do not invent dates, thresholds, approvals or successful test results. Unresolved facts must be explicit and bounded. Unnumbered document headings are acceptable; numbered procedural actions remain useful.

## Source and enforcement design

Extend the existing artifact contract and native JSON bindings rather than create another editable master. Resolve document type, audience, purpose, scope, authoritative sources, template/profile versions and output format before drafting. Explicit task instructions govern permitted choices, followed by project conventions and harness defaults; no profile overrides safety or grants authority.

Preserve existing exports under their legacy profile. Add an explicit client-engineering projection that omits internal control fields from issued content without deleting the underlying records. Support existing narrative sources through an explicit adapter, not silent conversion. Normalise line endings and fail on unparsed required structured sections.

Use one conditional documentation gate in the existing lifecycle, proportional to the task. Resolve the selected skill and template at task start. Validate actual artifact output after drafting and again before export/completion. Bind results to source/profile hashes and checker versions; a self-authored `passed` statement is insufficient. Keep visual export verification separate from content verification.

Hard failures should cover required sections/fields, unsupported profile versions, unresolved references, unfilled issued-template instructions, missing required record counts, source/hash mismatch and unsupported claims of executed verification. Scoped diagnostics should identify likely authoring narration, vague requirements and repeated boilerplate for substantive review. Avoid blanket bans on words such as approval, owner or status.

Managed CLI gates can refuse a compliant-completion claim when checks are missing. Hooks and prompts cannot guarantee that every external agent or unmanaged tool follows the workflow. No automatic model calls, source mutation or external publication should be introduced by checking.

## Implementation slices and acceptance

| Slice | Inspect/change targets | Acceptance |
| --- | --- | --- |
| Template review | Existing catalogue/template library and proposed document outlines; representative requirements/design samples where missing | Present concise structure, language, required/optional sections and validation recommendations; review the templates with the owner before implementation. |
| Convention and templates | Existing five `skills/engineering-*/SKILL.md`, `docs/engineering-artifacts.md`, new shared coordinator and owning-skill assets | One clear document-to-template map; requirements/design examples; authoring help excluded from issued output; local convention and source choices recorded. |
| Parser and checks | `karakana/tools/engineering_artifacts.py` and focused artifact tests | LF/CRLF equivalence; required structured sections cannot silently parse as zero records; good/bad output fixtures; existing native bindings and legacy exports retained. |
| Selection and gates | `karakana/cli.py`, `karakana/agents/planner.py`, skillpack resolver and protocol checks | Documentation type selects the correct resources; explicit selections honoured; unrelated tasks retain current selection; completion recomputes source-bound checks. |
| Remaining templates and exports | Owning-skill assets; workbook/document export profiles | Release, user guide, UAT and runbook coverage; neutral client metadata; content checks independent of chosen renderer; rendered Word/PDF/workbook checks appropriate to the format. |
| Pilot and integration | Artifact fixtures, routing/protocol integration tests, skill evals | Repeatable decisions; negative cases rejected; source changes invalidate checks; focused then required full regression gates pass; one compact delivery record and reviewed PR. |

Important fixtures: product approval requirements allowed; meeting prose misplaced under requirements flagged; meeting minutes allowed as their own artifact; unknown thresholds declared rather than invented; actual pass claims require run evidence; acceptance criteria are not mistaken for completed tests; internal ADR status retained; client draft boilerplate omitted; changed hashes invalidate validation; checks perform no external writes. Retain instruction-coverage evals with their limited claim. A real model authoring pilot needs explicit opt-in for live calls.

The smaller alternative is templates alone: quick to add but unable to prevent wrong selection or false completion. A universal document generator is the opposite alternative: broader migration risk and unnecessary replacement of existing tools. Prefer focused templates plus existing-lifecycle enforcement.

## Continuation

Research is complete. Next, review the existing templates and proposed outlines, preparing representative requirements/design samples where needed. Present concise recommendations and review the templates with the owner before implementation. Then proceed through the convention/templates slice, parser/checks and task-time enforcement. Do not revise the Jovina bundle during these slices. After the harness changes are verified and integrated, perform a new bounded client review, produce the update plan, then apply authorised revisions.

Portable continuation branch: `feat/documentation-conventions-templates-20261113`. The research was integrated through PR #33, and the portable loading correction through PR #34. Windows runtime traces and handoffs under `.karakana/` are intentionally excluded from Git. Use the tracked continuation note as current task context and follow repository instructions to establish the local handoff. No server connection is needed for this work.

The user's initial approval on 13 November covered committing and syncing this research branch. The subsequent request extends this to updating `main` through the pull request and preparing the next branch for continuation. This publication does not itself activate skills or revise client documents. The portable [Ubuntu handoff](UBUNTU-HANDOFF-2026-11-13.md) records the current scope and exact next action. Reuse the research rather than repeat it. Recommended route: GPT-6 Sol with medium reasoning for the convention and design work, high for consequential protocol-gate changes; this is a recommendation, not an observed model switch. A fresh conversation on Ubuntu is appropriate.

<a id="bounded-convention-and-templates-plan"></a>
## Bounded convention-and-templates plan

Planning trace: `20261113-165952-4fa887`. Inspected baseline: `798b3c2` on
`feat/documentation-conventions-templates-20261113`, tracking its origin branch
with zero divergence. This task consolidates accepted choices into a plan.
Implementation, publication and integration are separate actions.

### Accepted decisions and authority

| Review event | Decision carried forward | Scope of agreement |
| --- | --- | --- |
| Requirements: “accepted for now” | Tailored requirements outline, direct language, stable IDs, linked criteria and verification; optional sections selected for need | Requirements direction accepted for the current round |
| Standards: “accepted, next task” | Short Standards and references section; exact editions and explanation of use; distinguish actual mandatory obligations from guidance | Requirements review completed, including the standards addition |
| Design: “okay, i meant accepted in this round” | Tailored design outline, useful source-maintained diagrams and linked ADRs for consequential choices | Design direction accepted for the current round; clarification stopped premature drafting |
| Task brief followed by “execute action” | Reconcile these decisions with the existing convention/templates slice and produce its bounded implementation plan | Planning authorised; skills, templates and enforcement implementation are not part of this task |
| Following the completed plan: “execute” | Implement CT01–CT08 on the continuation branch, including verification | Local convention/templates, skills, optional profiles, tests and evals authorised; later parser/selection/enforcement/client work and remote publication remain separate |
| Following verified local delivery: “pr squash merge” | Commit and publish this slice through a PR, validate it and squash merge into `main` | Source integration authorised; deployment, live model calls and later implementation slices remain separate |

The runtime review histories under `.karakana/reviews/20261113-requirements-template-review/`
and `.karakana/reviews/20261113-design-template-review/` retain the detailed
discussion locally. This tracked record carries the decisions needed on another
machine; those ignored histories are supporting evidence, not required imports.
Later revisions must record what changed and which accepted choice they supersede.

### Outcome and acceptance

The first implementation slice will make the accepted requirements/design
structures usable through the existing engineering skills. It will provide one
shared convention, a document-to-resource map, two clean narrative templates,
separate authoring guides and two worked synthetic examples. The other three
engineering skills will reference the shared convention while retaining their
existing document-specific guidance and examples.

| ID | Observable acceptance for that slice |
| --- | --- |
| CT01 | Each of the five existing engineering skills links the shared convention; the coordinator maps supported document types to the owning skill and relevant resources. Requirements and design have the new packs; other types retain their current guides. |
| CT02 | Requirements template covers metadata, standards/references, purpose/scope, context/users, functional requirements, quality/constraints, linked acceptance/verification and unresolved facts where present. Interfaces/data, stories, glossary, transition needs and detailed traceability are conditional. |
| CT03 | Design template covers metadata/references, purpose and requirement links, context/concerns/boundaries, solution structure, runtime/failure behavior, data/interfaces, security/quality, deployment/operations, decisions and verification/risks. Small changes may link existing applicable views. UX, migration and detailed contracts/views are included when affected. |
| CT04 | Guides explain selection, tailoring, requirement/decision patterns, conditional content and revision handling. Issued examples contain completed technical content; template prompts and reviewer/meeting arrangements stay in guidance. Blank templates use consistent substitution fields, with authoring instructions held separately. |
| CT05 | Requirements reference ISO/IEC/IEEE 29148:2018; design references ISO/IEC/IEEE 42010:2022. Both use ISO/IEC 25010:2023 and ISO/IEC/IEEE 15289:2019 as relevant supporting references. NASA is supplementary writing guidance; arc42/C4 are practical design guidance. Editions and application are explicit, with tailored/informed-by wording and no unsupported conformity claim. |
| CT06 | Examples are visibly synthetic, share consistent IDs/terms and include meaningful normal, failure and permission boundaries. Unknown measures remain unresolved. Defined criteria, proposed decisions, planned checks and executed observations remain distinct. Product approval/audit requirements remain legitimate content. |
| CT07 | Existing source authority, IDs, exact-table exports, blank workbook/library and historical example baselines remain intact. Narrative assets are not presented as supported structured-export inputs. The coordinator remains experimental and optional; unrelated tasks retain existing defaults. |
| CT08 | Resource links resolve; skill metadata/index/profile discovery checks and deterministic instruction evals pass; existing example/export regressions remain green. Manual review checks the actual two examples against CT02–CT06. Automated structure checks do not certify usefulness, factual truth or conformance. |

### Resources and files

Paths in this table are planned; new resources are not delivered by this plan.

| Target | Planned change |
| --- | --- |
| `skills/engineering-documentation-conventions/SKILL.md` | New shared coordinator: document type, audience, purpose, scope, sources, output format, applicable references, language and tailoring. Use valid required metadata and standard sections; experimental/public/bundled, documentation category. Preserve existing approval and execution boundaries. |
| `skills/engineering-documentation-conventions/references/document-map.md` | Versioned selection map for requirements, design, implementation plans, release notes, guides, UAT and runbooks; identify available packs versus existing guidance and later work. |
| `skills/engineering-requirements/assets/requirements-template.md` | Clean requirements outline with substitution fields and accepted required/conditional content. |
| `skills/engineering-requirements/references/requirements-template-guide.md` | Authoring guidance, good/bad statement patterns, quality measures, criteria/source links, standards wording and completion checklist. |
| `skills/engineering-requirements/assets/requirements-example.md` | Complete synthetic example of the accepted outline; distinguish expectations from actual verification. |
| `skills/engineering-design-records/assets/system-design-template.md` | Clean design outline with requirement links and tailored views. |
| `skills/engineering-design-records/references/system-design-template-guide.md` | Authoring guidance, diagram purpose/source conventions, scenario/contract checks, standards wording and ADR linking; reuse existing `references/adr.md`. |
| `skills/engineering-design-records/assets/system-design-example.md` | Synthetic design for the same scenario/IDs as the new requirements example, including rationale and explicit evidence gaps. |
| Existing five `skills/engineering-*/SKILL.md` | Add common-convention links; requirements/design also link their new assets and guides. Update changed instruction versions appropriately. Preserve the existing workflow, authority and example-export guidance. |
| `docs/engineering-artifacts.md` | Add the convention/resource map and an explicit narrative-versus-structured-source boundary. Retain the legacy source/export contract. |
| `skills/README.md` | Regenerate with `karakana skill index --write`; retain experimental status. |
| `skillpacks/karakana.yml`, `skillpacks/lims.yml`, `skillpacks/ent-meal.yml` | Add the coordinator as optional alongside the five existing engineering skills; retain all required-skill ordering, project memory and approval settings. These are harness profiles, not application-repository edits. |
| New coordinator evals; existing requirements/design eval directories | Add deterministic cases for task-type preservation, tailoring, applicable standards, unresolved facts and the distinction between criteria and actual results. Label instruction coverage accurately. |
| `tests/test_engineering_documentation_skills.py`, `tests/test_engineering_skill_discovery.py` | Extend existing loader/resource/discovery coverage for the coordinator and new packs. Preserve temporary-repository isolation and existing example/export tests; add only meaningful compatibility and source-integrity checks. |
| This record and append-only runtime handoff | Record exact slice results, changes to accepted decisions, verification limits and the next action. |

Clean examples are placed under `assets/` because the current
`test_authored_examples_are_valid_alone_and_combined` collects every Markdown
file under the existing skills' `examples/` directories as a structured P02
source. Preserve those examples as working export fixtures. This placement avoids
implying that a new narrative shape satisfies the legacy exact-table parser.

### Delivery steps and dependencies

1. Start the implementation task on the continuation branch after it is selected.
   Read this plan, `AGENTS.md`, `KARAKANA.md`, `docs/engineering-process.md`,
   `docs/engineering-artifacts.md`, `skills/write-karakana-skill/SKILL.md`, the
   five owning skills and their relevant references. Reuse the completed research
   and accepted decisions; inspect only changed/new uncertainties.
2. Use the existing `skill-update` protocol for the slice. Attach this record as
   the compact scope/requirements/design/acceptance/plan evidence where its content
   satisfies each required kind. Supply any remaining protocol-specific evidence
   and review the pre-implementation check before changing skills/resources.
3. Add the coordinator and map, then the requirements pack and matching design
   pack. Keep blank outlines, authoring help and complete examples separate.
   Reuse the accepted synthetic programme-access scenario without asserting that
   it specifies or verifies any actual application. Retain unconfirmed policy
   parameters and proposed verification clearly.
4. Add focused compatibility/discovery checks and instruction evals as the skills
   are wired. Update the shared contract, optional profile entries and generated
   index. Follow existing `SkillLoader`/`SkillValidator` behavior; links in a skill
   do not recursively load referenced skills or resources.
5. Run the focused gates below, review the actual assets and then run the required
   full regression/eval gates once the slice is stable. Verify the tracked diff
   stays within this file map and the legacy examples/blank assets remain unchanged.
6. Finish one compact delivery update and a trace-bound handoff. Deliver through
   a reviewable PR under the repository's existing authority rules. Record local
   completion, publication, squash integration and acceptance separately; this
   planning request grants no new GitHub-write or release authority.

### Verification plan

Commands below are planned implementation checks, not results of this planning task.

| Check | Command / observation and expected result |
| --- | --- |
| Resource and discovery integration | `.venv/bin/pytest -q tests/test_engineering_documentation_skills.py tests/test_engineering_skill_discovery.py tests/test_skill_index.py tests/test_skill_validator.py` — new resources resolve, coordinator stays optional, explicit project/skill isolation and unrelated defaults remain correct. |
| Legacy content/export compatibility | `.venv/bin/pytest -q tests/test_engineering_artifacts.py tests/test_engineering_artifact_pilots.py` — supported tables, native bindings, immutable exports and feedback behavior retain their existing results. |
| Skill and profile validation | `.venv/bin/karakana skill validate-all` and `.venv/bin/karakana skillpack validate-all` — no new errors or warnings; investigate existing warnings separately. |
| Focused deterministic evals | `.venv/bin/karakana eval run --skill engineering-documentation-conventions`, then the requirements/design skill cases — discoverable cases pass with instruction-coverage limits explicit. |
| Stable final regression | `.venv/bin/pytest -q` and `.venv/bin/karakana eval run` — required local regression/eval gates pass; no live provider calls. |
| Human content review | Inspect both worked examples against CT02–CT06, including consistency across requirement IDs, design decisions, negative scenarios and proposed checks. Check authoring help stays out of completed examples. State this as substantive self-review, not independent acceptance. |
| Diff and continuation | `git diff --check`, scoped diff review, completion protocol check and `handoff doctor` — clean patch and complete referenced continuation; protocol checks establish evidence presence/structure only. |

Test-generated runtime stores and outputs belong in `tmp_path`/`isolated_repo`,
never the checkout's `.karakana`. No new tests are needed for this planning-only
Markdown edit. Its own verification is source/path reconciliation, link and diff
review and the planning protocol closeout.

### Limits, alternatives and recovery

The first slice supplies reusable guidance and assets. It does not implement
document-type routing, recursive resource loading, machine content profiles,
parser repairs, new export projections, protocol enforcement, visual rendering,
model authoring pilots or client/Jovina revisions. Those retain the later slices
in the original plan. New content patterns do not silently change the existing
canonical metadata or export schema; narrative adoption/export needs an explicit
supported path in the later adapter work.

The selected method extends existing skills. A templates-only alternative has a
smaller footprint but leaves common language and selection guidance duplicated.
A universal generator or full mandatory architecture outline has broader scope
and migration/tailoring cost. The shared coordinator plus two focused packs fits
the accepted direction while keeping automated selection/enforcement separate.

Risks to check are misplaced assumptions of automatic activation, accidental
legacy-parser compatibility claims, invented policy/metrics, and copied
third-party template text. Use original local content and link authoritative
references. Recovery for an implemented slice is a reviewed revert of its scoped
resource/skill/profile changes, preserving runtime history and all pre-existing
example/workbook baselines. No database migration or runtime rollback is applicable.

### Readiness and exact next action

Planning is complete when this accepted-decision record, resource map, ordered
steps, acceptance and verification plan have been reviewed against current source.
The current request authorises that plan, not its execution. The owner controls
selection of the next implementation slice; no requirements/design re-review is
needed unless a material change arises.

Next recommended task: implement the bounded convention-and-templates slice
defined here when selected. First implementation action: verify the current
branch/source, load the skill-authoring instructions, start `skill-update`, attach
the prerequisites and review its pre-implementation gate. Recommended model:
GPT-6 Sol with medium reasoning; continue this conversation while context remains
useful. This recommendation does not switch or verify the active model.

Planning verification: branch and origin were aligned at `798b3c2` before this
edit. Both local links/anchors, the eight acceptance IDs and the named existing
test, skill and profile paths were checked; `git diff --check` passed and the
pytest runner is available. The full patch was self-reviewed. No tests/evals were
run and no skills, templates, profiles or application files were changed by this
planning task. Protocol/handoff receipts remain append-only runtime evidence.

### Implementation continuation adjustment

The owner selected implementation with “execute” after the planning summary.
Completion inspection also found that the tracked portable note and wrapper still
described the original pre-implementation template review. Their continuation text
and wrapper labels are refreshed with this slice so a later machine does not
reopen completed work. The wrapper retains the same refresh/load calls and full
brief handling; no loader, routing or execution behavior is added. Its existing
temporary-repository tests and Bash syntax check join the verification scope.

<a id="convention-and-templates-delivery-results"></a>
## Convention-and-templates delivery results

Implementation trace: `20261113-171059-f4a7e6`. The owner's “execute” selected
the bounded plan. Work remains on `feat/documentation-conventions-templates-20261113`
from `798b3c2`, including the preceding local planning edit. The results below are
the local verification checkpoint before publication. The owner subsequently
authorised PR publication and squash integration; exact integration receipts
belong to the associated GitHub PR and final append-only handoff. No deployment
or live model call is included.

| Delivered surface | Result |
| --- | --- |
| Shared convention and map | New experimental `engineering-documentation-conventions`, with one type/resource map, common language, standards/reference and authority rules; all five existing engineering skills link it. |
| Requirements pack | Clean template, separate authoring guide and complete narrative example under the owning skill. Six stable requirement IDs link to six criteria; unknown quality measures remain explicit. |
| Design pack | Matching clean template, guide and narrative example with editable Mermaid source, responsibilities, failure/revocation scenarios, proposed decision rationale and complete requirement/criterion references. |
| Discovery | Coordinator is optional in Karakana, LIMS and ent-meal harness profiles. Required-skill ordering, project memory and approval settings are retained; generated index is current. |
| Compatibility and continuation | Existing parser/structured examples/blank library and workbook retained. Source contract explains narrative/export limits. Portable note and wrapper labels carry current continuation instead of reopening pre-implementation review. |

| Verification | Observed result |
| --- | --- |
| Pre-implementation artifact gate | Passed `20261113-171142-protocol-check-db6849`; presence only. |
| Focused baseline | 48 tests passed; 179/179 deterministic evals passed before skill changes. |
| Focused updated discovery/resources | 57 passed in 3.66s. First run found three instances of one new-skill heading mismatch with existing prompt tests; corrected to the catalogue heading convention, then passed. |
| Legacy artifact/export/pilot checks | 66 passed in 2.89s. |
| Portable wrapper | Four temporary-repository tests passed; `bash -n` passed. Only continuation labels/text changed, not refresh/load behavior. |
| Actual portable load | Real local refresh/load showed the complete current note and locally implemented state; the obsolete pre-implementation milestone was absent. This is a continuation check, not source integration. |
| Skill and profile validation | All skills and ten skillpacks passed with no warnings in these commands. The repository's required metadata schema governs; the generic skill-creator validator's restricted frontmatter keys do not accept Karakana's required metadata. |
| Focused instruction evals | Coordinator 2/2, requirements 5/5, design 5/5 passed. |
| Full stable regression | 766 passed in 21.69s. |
| Full deterministic evals | 183/183 passed; zero warnings. Report `20261113-172000-eval-f1549c`. No live authoring/model-behavior result is inferred. |
| Preservation and diff | Fourteen legacy source/example/blank-asset files matched `HEAD` byte-for-byte; `git diff --check` passed. |

CT01–CT08 self-review: type/resource links and optional discovery are exercised
through actual isolated planner calls. The two completed examples were read
against the accepted content: matching terms and IDs, normal/denied/pending/revoked
states, dependency failure, current entitlements, proposed decision alternatives,
source authority and unresolved performance/identity/deployment facts are explicit.
Templates have substitution fields; worked examples contain completed content
and no unfilled fields or authoring logistics. Product approval state remains
legitimate technical content. Standards are identified by edition and use with
tailored guidance limits. This is substantive self-review, not independent reader
acceptance, a real application security test or standards-conformity assessment.

No parser fixes, recursive loading, task routing, machine content profiles,
new client export projection or completion enforcement were added. No Word/PDF/
workbook rendering or real product implementation is claimed by the narrative
examples. Their intended use and legacy-export boundary are explicit in the
guides, map, common convention and source contract.

Remaining: review the delivered sample content and source patch, then authorised
PR publication/integration before starting the next implementation milestone.
Later parser/checks, task-time selection/enforcement, remaining packs/exports and
the Jovina review retain the original sequence and authority. Recommended next
task is source/sample review of CT01–CT08; GPT-6 Sol medium, with a fresh
conversation useful at this completed local-delivery boundary.
