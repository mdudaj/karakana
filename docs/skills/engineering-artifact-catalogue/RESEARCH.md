# Engineering artifact catalogue: research and proposed update

Status: **Local delivery for review**. Research completed 2026-09-26.
P01–P03 are implemented locally; discovery/enablement, pilots, integration and
stable promotion remain pending.

The user requested comprehensive research before an update plan, covering
engineering documentation artifacts. Following the format correction, Markdown
is the primary authoring and version-controlled format; accompanying Excel
workbooks provide sharing and review views tailored to each audience.
The scope includes requirements, stories, acceptance, ADRs, design, roadmaps,
milestones, implementation plans and releases, with their supporting evidence.
It applies across Karakana projects. No LIMS first-release documents or live
operational changes are part of this slice.

## Deliverables and reading order

For reuse, start with the [generic Markdown template](TEMPLATE.md) and its
accompanying [blank Excel template](engineering-artifacts-template.xlsx).
They contain generic artifact fields, empty data rows and audience guidance,
with no project names or project-specific features. Populate only instantiated
copies. Five experimental skills now exist in the repository; personal
installation and project skillpack enablement are not part of P03.
[P02](P02.md) supplies the separately invoked local audience export workflow.

P01 is now delivered locally for review: the
[content/source and export contract](../../engineering-artifacts.md),
[ADR](../../adr/0005-markdown-engineering-artifact-contract.md),
[native-engine mapping and delivery record](P01.md), and complete synthetic
[tiny](examples/tiny.md), [feature](examples/feature.md),
[ADR/design](examples/design.md) and [roadmap/release](examples/release.md) examples.
Template version 0.2 adds stable source anchors, per-artifact source authority/hash,
a persisted legacy-string binding table and a multiple-file source manifest.
The user accepted the generic Markdown/Excel template direction; detailed adapter
choices were subsequently authorized for P02 implementation.

P02 is delivered locally: Markdown validation, read-only native adapters, binding
proposals, five audience export profiles and three-way feedback reports. Its
[usage and verification record](P02.md) separates local test evidence from
independent review, project pilots and integration.

[P03 delivery/source register](P03.md) records five original experimental skills:
[requirements](../../../skills/engineering-requirements/SKILL.md),
[design records](../../../skills/engineering-design-records/SKILL.md),
[delivery planning](../../../skills/engineering-delivery-planning/SKILL.md),
[release documentation](../../../skills/engineering-release-documentation/SKILL.md)
and [workbooks](../../../skills/engineering-workbooks/SKILL.md), with fourteen
conditional guides, four neutral worked examples and nineteen coverage evals.
They are available through the repository loader/CLI; generated discovery and
project enablement remain P04.

This narrative and the [detailed Markdown plan](PLAN.md) are the canonical
research and proposal. The detailed plan contains all evidence, requirements,
decisions and implementation records, including the audience profiles.

The accompanying [Excel research and update plan](research-and-update-plan.xlsx)
is a derived view for the research-review audience: 15 sheets, 226 record rows,
38 external primary/maintainer references and five inspected local/upstream
evidence entries. Start with `02 Findings`,
`05 Skill Plan`, `09 Delivery Plan` and `10 Decisions`. Review fields are marked
with both text labels and yellow fill; no decision is pre-populated as approved.
This research workbook is evidence and planning, **not the reusable template**.
Its project names and repository paths identify inspected research sources;
those names and features are excluded from the separate generic assets.

The [JSON snapshot](research-and-update-plan.json) is a generated rendering
intermediate, carrying the same detailed records and the source hash. Edit
Markdown first. Archive annotated workbooks and compare feedback by source ID
and revision; review proposed changes into Markdown, then generate a new export.
Workbook feedback cannot automatically update source content or approvals.
The [renderer](render_workbook.py) reads `PLAN.md` directly and can derive both
outputs. It reproduces this complete research-review pack; audience projection
for instantiated engineering artifacts is implemented by the separate P02 tool.
It refuses to overwrite files.

## Research method and limitations

Inspected the accepted [engineering process](../../engineering-process.md),
global engineering memory, current skills, requirement schemas and artifact
checks. Inspected ent-meal upstream at
`90d32e220f798858918c1e2177e5b34ad3a0f401`, including its baseline conventions,
roadmap framework, methodology, Excel generator and generated five-sheet pack.
The checkout matched the fetched upstream revision and was not changed.

The external survey covers standards, requirements quality, agile/XP practices,
architecture documentation, acceptance testing, security, release communication,
documentation audiences, skill packaging, community implementations and Excel
integrity/usability. Sources were read from publishers, originators and maintainers;
marketplace listings and reposts were not used as authorities.

Only public publisher summaries of paid standards were inspected. The result is
a tailored engineering proposal, not a clause-by-clause standards assessment or
certification. Each canonical source row states its edition/revision, inspection
date, finding and adoption limit. These are inspected references, not a claim
that every possible documentation method has been exhausted. Recheck evolving
standards and community implementations before implementation.

Community code was pinned through public repository commit metadata:

| Repository | Inspected revision | Reuse boundary |
| --- | --- | --- |
| Anthropic skills | `33375500bcea98d610eb30ce10ac4e59b89c390d` | Document skills are source-available; the inspected XLSX license is proprietary. No import or adaptation proposed. |
| Matt Pocock skills | `c55ee46073ed923f86ce59a5eb3b6d895095d1b7` | MIT; use selected concepts with attribution if text is reused. |
| Superpowers | `8ca22dba9a94f28898bbce59f2537ff4d87c747d` | MIT; retain useful planning content without importing orchestration. |

The public [Anthropic repository explanation](https://github.com/anthropics/skills/blob/33375500bcea98d610eb30ce10ac4e59b89c390d/README.md)
distinguishes open example skills from its source-available document skills.
Folder-specific licensing for `doc-coauthoring` was not resolved; no copying is
proposed. The Excel design below is original and based on inspected project
evidence and official Microsoft/openpyxl guidance. No upstream skill was invoked
as instructions, installed or bundled in this package.

## Findings that shape the proposal

### Documentation content and standards

[29148:2018](https://standards.ieee.org/ieee/29148/6937/) provides requirements
engineering context. [15289:2019](https://www.iso.org/standard/74909.html) supplies
the lifecycle information-item perspective and supports combining records; its
public summary does not prescribe Excel. [12207:2026](https://www.iso.org/standard/90219.html)
is the inspected lifecycle edition. The older mappings in 15289 are not assumed
to have been updated to that edition. Our artifact profiles and field choices
are local design decisions.

Use the [NASA requirement-writing checklist](https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/)
for clarity and verifiability, and [IIBA's public classification and traceability
guidance](https://www.iiba.org/knowledgehub/the-business-analysis-standard/4-implementing-business-analysis/4-4-understanding-requirements-and-designs/)
for the distinction between needs and solution descriptions. Business, stakeholder,
solution and transition are the high-level classes; data, workflow and reporting
can be local tags or subtypes. A measurable requirement must have a source,
acceptance condition and verification approach; an agent must not invent a
performance threshold or stakeholder priority to fill a cell.

Two standards need careful version labels. The inspected
[25010:2023](https://www.iso.org/standard/78176.html) product-quality model has nine
characteristics; ent-meal's unversioned eight-category summary should not become
the global current-edition model. [IEEE 1016:2009](https://standards.ieee.org/ieee/1016/4502/)
is inactive-reserved and can be identified only as historical design-description
guidance. Full normative details would require separately obtained texts.

### Agile requirements, stories and planning

The [Agile Manifesto](https://agilemanifesto.org/) values documentation while
giving working software and adaptation greater weight. The
[Scrum Guide](https://scrumguides.org/scrum-guide.html) uses Product/Sprint Goals
and a Definition of Done, but does not prescribe our workbook, user-story syntax,
story points or a Definition of Ready. We can use these as local practices
without representing them as Scrum obligations.

[INVEST](https://xp123.com/invest-in-good-stories-and-smart-tasks/) and
[Card, Conversation, Confirmation](https://ronjeffries.com/xprog/articles/expcardconversationconfirmation/)
support useful small stories with discussion and acceptance examples. Keep
requirements and stories linked rather than turning each constraint into an
artificial user story. [Gherkin](https://cucumber.io/docs/gherkin/reference/)
can express observable examples; writing one in Excel is not executing a test.

Use outcome-based roadmap records informed by the
[GO roadmap discussion](https://www.romanpichler.com/blog/goal-oriented-agile-product-roadmap),
with horizon, dependencies, confidence and success measures. Keep broad product
direction separate from implementation tasks and from agreed release commitments.
[DORA's small-batch guidance](https://dora.dev/capabilities/working-in-small-batches/)
supports independently useful slices and feedback. Document counts and estimated
dates are not evidence of delivered value.

### ADRs, design and audience

[Nygard's ADR guidance](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
and [MADR](https://adr.github.io/madr/) support concise decision records with
context, alternatives, rationale, consequences and retained supersession history.
Author complete ADRs in Markdown, preserving reasoning and history. A shared
workbook can include a decision register, concise rationale/consequence summaries
and source links; it must identify excerpts and point to the complete ADR.

[42010:2022](https://www.iso.org/standard/74393.html),
[arc42](https://arc42.org/overview/) and the [C4 model](https://c4model.com/) inform
audience-specific views. Select the relevant context, runtime, component,
deployment and quality concerns; do not require every possible view for each
task. Diagrams and authoritative API/schema sources keep repository locations
and revision links. Markdown design records hold the narrative and useful text
descriptions; audience workbook summaries link the complete records and views.
[Diataxis](https://diataxis.fr/) helps distinguish user-learning/task/reference
needs from design rationale and delivery records.

### Acceptance, security and release truth

[ISTQB's acceptance-testing guidance](https://istqb.org/certifications/certified-tester-acceptance-testing/)
supports collaboration on acceptance conditions and tests. Record a case separately
from its run: actual result, revision, environment, timestamp, executor and
evidence. Preserve Not run, Blocked, Skipped, Fail and Pass as distinct facts.
Business acceptance requires its own real reviewer decision.

[NIST SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final) and
[OWASP SAMM](https://owaspsamm.org/model/) inform security considerations across
design, verification and operation. The inspected
[SSDF 1.2 revision](https://csrc.nist.gov/pubs/sp/800/218/r1/ipd) remains an initial
public draft; track it separately from final guidance.
[Google engineering review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
informs substantive review beyond formatting. Self-review is still not independent
review, and structural validation is still not approval.

[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) informs human-readable
versioned changes. [SemVer](https://semver.org/) is suitable only where a project
declares the public compatibility contract it versions. A release pack should
link delivered scope, candidate revision, limitations, migration, recovery,
monitoring, user guidance and actual review evidence. Draft, locally verified,
merged, published, deployed and accepted remain separate states. A planned
feature must not appear as a delivered release note.

### Skills and format tooling

The [Agent Skills specification](https://agentskills.io/specification) supports
concise metadata and conditional resources. Karakana's extra metadata and
validation requirements still apply. The local `skill-creator` and
`write-karakana-skill` guidance also favors focused scope, progressive disclosure
and observable behavioral checks.

The inspected [Matt Pocock collection](https://github.com/mattpocock/skills/tree/c55ee46073ed923f86ce59a5eb3b6d895095d1b7)
now uses `to-spec` and `to-tickets`, so the earlier local `to-prd`/`to-issues`
inventory is historical. Their synthesis and dependency ideas are useful, but
tracker publication and extensive-story defaults must not become our behavior.
[Superpowers writing-plans](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/writing-plans/SKILL.md)
provides useful file/interface/check detail. Its execution and delegation framework
is not needed here. Community workflow assumptions are reviewed evidence, not
authority to change our process.

## Ent-meal reuse and improvements

Retain its explicit baseline status, review guide, requirement/capability IDs,
source fields, filters, freeze panes, comments and sign-off roles. Generalize
the conventions and release-output checklist; retain project-specific terminology,
ownership and release proposals within ent-meal.

The inspected workbook has five sheets, 69 requirement records, 29 capability
records, no named Excel Tables and no formulas. Its `Traceability` sheet maps
workbook sheets to source documents. The global proposal adds typed item-level
links through requirements, stories, decisions/design, criteria, tests and release
scope. Source mappings remain useful but do not substitute for that chain.

The generator's `_priority_from_requirement` assigns candidate P1/P2 values from
ID prefixes; `_priority_from_status` falls back to P2 for unrecognized status.
The new contract preserves proposed and agreed priority separately and keeps
unknown priority unconfirmed. Its generated acceptance bases are draft review
aids; they must not become proof of implementation or tests. These findings are
research evidence for a new shared workflow, not fixes applied to ent-meal.

## Proposed catalogue architecture

| Proposed skill | Owns | Reuses |
| --- | --- | --- |
| `engineering-requirements` | Requirements, stories, acceptance and traceability authoring/revision | Elicitation, existing requirements schemas/store/readiness, plan grill |
| `engineering-design-records` | ADRs and relevant architecture/design descriptions | System design, domain/UX skills, architecture protocol |
| `engineering-delivery-planning` | Roadmap, milestones and bounded implementation plans | Next-milestone selection, existing issue drafts and lifecycle |
| `engineering-release-documentation` | Release plans/assurance, notes and adoption/handover | Project release checks/runbooks, release protocol, handoffs |
| `engineering-workbooks` | Derived audience Excel exports, integrity/freshness checks and feedback reporting | Markdown from the selected authoring skill and narrow deterministic tools |

P03 implements these focused skills in the shared repository catalogue. It adds
no framework and does not automatically load five skills for every task.
Overlap was checked against current skills; the new workflows author selected
artifacts rather than replacing elicitation, reasoning or direction selection.
`delivery-artifact-gate` remains the prerequisite/review
guide; `requirements-elicitation` resolves ambiguity; `next-milestone-decision`
chooses direction. Authoring skills record the selected outcome.

The existing `karakana/requirements` engine already stores structured PRDs,
stories, issue drafts and readiness results. Preserve its IDs, states and source
provenance through an adapter. Acceptance strings currently lack individual IDs:
the adapter design must assign/persist stable criterion identities without using
row order as identity or silently breaking existing consumers.

All four authoring workflows produce Markdown with stable artifact IDs, sources,
status, review evidence and version history. Existing structured requirement
records, machine schemas and source diagrams retain authority for their explicitly
identified content; Markdown links those sources rather than duplicating editable
machine definitions. Define that mapping and identity ownership during P01.
Global skills and template assets must contain generic conventions, not a
particular project's name, capabilities or release scope. Keep upstream evidence
in research records and project data in instantiated artifacts; do not distribute
an upstream project's populated workbook as the global template.

Excel profiles contain only applicable tables. Every export identifies project,
artifact/export identity, audience/profile version, generation date, source
Markdown paths/sections/IDs/revisions/hashes, baseline, requested action and
omissions, with links to complete sources. The plan details 24 proposed export
table contracts. Typed link rows express many-to-many
relationships by qualified IDs; baseline/version resolution must be defined in
P01. Full ADR/design narratives stay in Markdown.

Audience profiles in `14 Audience Profiles` select useful views:

| Audience | Sharing focus |
| --- | --- |
| Business/product | Needs, scope, stories, acceptance, outcome roadmap and user-facing release changes |
| Engineering | Constraints, ADR summaries, design/contract links, implementation tasks and technical changes |
| QA/UAT | Acceptance, cases, actual runs, candidate/environment, defects and review evidence |
| Operations/release | Readiness, rollout/recovery, migration, monitoring, support and runbook links |
| Executive/sponsor | Outcomes, milestones, confidence, material risks and decisions needed |

Relevant blockers, limitations, uncertainty and trace IDs survive every applicable
projection. Each workbook declares omitted detail and links the full baseline.
An audience summary must not turn a forecast into a commitment or hide a release
blocker. The current research workbook is the complete research-review profile;
it demonstrates the proposal. P02 separately implements five generic local
profiles; real project pilots remain pending.

Markdown is the canonical documentation source. Workbook review collects proposed
feedback against a specific source version. Archive it, report changed IDs and
conflicts, compare source freshness, and review changes into current Markdown
before regenerating a new export. Never synchronize two editable masters or
import workbook agreement as source approval. Source changes preserve history
and reconsider earlier approvals.

## Excel quality and verification contract

Use simple named tables, meaningful worksheet names and headers, useful wrap/
row heights, source links, frozen identity columns and text statuses.
[Microsoft's accessibility guidance](https://support.microsoft.com/en-us/accessibility/excel/accessibility-best-practices-with-excel-spreadsheets)
supports avoiding merged data cells and checking accessible presentation. The
proposed workbook also needs actual review in its supported target application;
styling alone cannot establish accessibility.

The deterministic tool should check uniqueness, link endpoints, provenance,
allowed values, applicable required fields, table ranges, source freshness and
review evidence. [openpyxl validation](https://openpyxl.readthedocs.io/en/stable/validation.html)
does not enforce entered values. Dropdowns assist humans; they cannot provide
integrity or authorization. [openpyxl](https://openpyxl.readthedocs.io/en/stable/simple_formulae.html)
does not evaluate formulas. Use calculation only where necessary; then recalculate
and compare results against known expectations, not just the absence of errors.

Preserve reviewer cells, unsupported content and existing formula sources when
editing supported workbooks. Define feature compatibility before using a library
to save a complex workbook. Block stale overwrites, capture changed IDs/cells,
and produce a feedback report against the source version. A stale export remains
historical evidence, with feedback reviewed against current Markdown; it cannot
overwrite the current source. Treat untrusted formula-like
strings as literal text and keep examples synthetic and secret-free.

The current protocol checker accepts readable nonempty files. It does not inspect
Excel sheets or evaluate content. Attach canonical Markdown and relevant source
evidence for required artifacts. Accompanying workbook views must map to the
same source version and actual reviewed content; attaching the same path repeatedly
is not proof. Keep a validation/review report alongside the export. Do not introduce a second lifecycle/approval
state machine or silently change existing protocol behavior in this update.

## Ordered implementation proposal

The detailed Markdown plan contains inspected/proposed paths, dependency edges, exit
evidence and requirement mappings for six slices:

1. **P01 — Agree Markdown content and export contracts.** Map current engine
   identities and authority to Markdown, persist stable criterion IDs and define
   links/history. Specify audience mappings, source manifests, freshness and
   feedback reconciliation. Review complete synthetic examples and a tiny task.
2. **P02 — Build narrow export and feedback tooling.** Validate Markdown and
   generate audience Excel views with source provenance. Report feedback,
   stale sources and conflicts; preserve annotated exports. Define supported
   workbook features and optional dependencies before changing code.
3. **P03 — Author focused skills.** Original instructions, conditional references,
   complete synthetic examples and meaningful behavior evals; start experimental.
4. **P04 — Update discovery.** Generate the catalogue index and add concise shared
   guidance and selected optional skillpack entries. Preserve permissions and
   avoid loading unrelated documentation workflows.
5. **P05 — Pilot and inspect actual output.** Synthetic Markdown feature, design/ADR
   and roadmap/release packs with audience exports; office round trips,
   source freshness, feedback reconciliation, render/accessibility
   review and recorded limitations. Real LIMS drafting is a later requested task.
6. **P06 — Review and integrate.** Follow the appropriate skill/code protocols,
   resolve blocking findings, run required tests/evals and review the final change.
   Publish/merge only under explicit session authorization; promotion needs evidence.

During implementation, inspect `karakana/requirements/{schemas,store,readiness}.py`,
`karakana/protocols/checks.py`, relevant protocols, the accepted lifecycle and
`skills/{loader,validator,index}.py`. Follow `write-karakana-skill` and the artifact
gate. Future tool behavior needs functional tests using isolated temporary
repositories/workbooks. Existing skill/index/eval commands should be reused:
`karakana skill validate-all`, `karakana skillpack validate-all`,
`karakana memory validate --project karakana`, `karakana skill index --write`
and focused `karakana eval run --skill <skill-name>` before the broader required
gate. These are implementation checks, not commands claimed to have run here.

Twenty update requirements map to 29 planned verification scenarios. They cover
the earlier inquiry-to-drafting mistake, request boundaries, project isolation,
IDs/links, measurable acceptance, decision history, forecast truth, release truth,
Markdown authority, audience projections, stale/conflicting feedback, human edits,
unrelated-file false assurance, licensing, formula correctness,
literal text and controlled promotion. They are **planned**, not passing results.

No delivery dates, assigned people or estimates are invented. The proposed
defaults in `10 Decisions` are concrete but unapproved. The implementation review
must settle status vocabulary, existing-engine compatibility and supported Excel
versions/features. Rollback of a later implementation would use a reviewed revert
without deleting project workbooks or runtime history; preserve schema compatibility
and archive superseded artifacts.

## Current verification and continuation

This slice changes only the research package on task branch
`docs/engineering-artifact-catalogue-research`. There are no skill, catalogue,
global memory, protocol, requirement-engine, dependency or LIMS changes.
The workbook is formula-free. The renderer, Markdown/JSON/XLSX record parity, IDs and
planned reference mappings are checked locally; rendered evidence and the exact
outcomes/limitations are recorded in the task verification artifact and append-only
handoff. No application behavior tests are needed for these documentation records.

To reproduce into a new file using the repository environment with openpyxl:

```bash
.venv/bin/python docs/skills/engineering-artifact-catalogue/render_workbook.py \
  --output /tmp/engineering-artifact-research-review.xlsx \
  --snapshot-output /tmp/engineering-artifact-research-review.json
```

To reproduce the separate generic blank template:

```bash
.venv/bin/python docs/skills/engineering-artifact-catalogue/render_workbook.py \
  --source docs/skills/engineering-artifact-catalogue/TEMPLATE.md \
  --output /tmp/engineering-artifacts-template.xlsx
```

The JSON metadata and workbook document properties record the `PLAN.md` source
SHA-256, research-review audience and UTC generation time. This is provenance
for the detailed export, not proof of freshness or approval; compare the hash
with the current source before relying on the workbook.

Remaining work: discovery/optional enablement, project pilots and reviewed
integration. Recommended next task: **P04**, following P01–P03 contracts, source
mapping, tool/skill usage, fixtures and verification instructions. Native source
IDs remain unchanged; exporting must not regenerate engine stories/issues or
rewrite source/approval state. Reuse the inspected evidence and research only
unresolved implementation/application compatibility questions.
