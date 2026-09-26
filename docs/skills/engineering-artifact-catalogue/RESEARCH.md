# Engineering artifact catalogue: research and proposed update

Status: **Draft for review**. Research completed 2026-09-26. This package plans
the catalogue update; it does not implement, install or promote skills.

The user requested comprehensive research before an update plan, covering
engineering documentation artifacts and using Excel as the current format.
The scope includes requirements, stories, acceptance, ADRs, design, roadmaps,
milestones, implementation plans and releases, with their supporting evidence.
It applies across Karakana projects. No LIMS first-release documents or live
operational changes are part of this slice.

## Deliverables and reading order

The [Excel research and update plan](research-and-update-plan.xlsx) is the human
review pack: 14 sheets, 215 record rows, 38 external primary/maintainer references
and five inspected local/upstream evidence entries. Start with `02 Findings`,
`05 Skill Plan`, `09 Delivery Plan` and `10 Decisions`. Review fields are marked
with both text labels and yellow fill; no decision is pre-populated as approved.

The [JSON snapshot](research-and-update-plan.json) carries the same records for
version-control review. It is not an independent editable authority. Reconcile
workbook review edits before updating the snapshot or rendering another version.
The [renderer](render_workbook.py) exists only to reproduce this research pack;
it is not the proposed reusable workbook tool. It refuses to overwrite files.

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
certification. Each workbook source row states its edition/revision, inspection
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
Our Excel adaptation should use a decision register plus ordered narrative rows,
so important reasoning is neither truncated nor buried in a huge cell.

[42010:2022](https://www.iso.org/standard/74393.html),
[arc42](https://arc42.org/overview/) and the [C4 model](https://c4model.com/) inform
audience-specific views. Select the relevant context, runtime, component,
deployment and quality concerns; do not require every possible view for each
task. Diagrams and authoritative API/schema sources keep repository locations
and revision links, with useful text descriptions in the workbook.
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
| `engineering-workbooks` | Excel creation/editing, integrity checks and review snapshots | Selected authoring skill and narrow deterministic tools |

This is a proposal to add capability to the shared Karakana catalogue, not to
install another framework or automatically load five skills for every task.
Reassess overlap during implementation: extend an existing skill if it actually
owns the same workflow. `delivery-artifact-gate` remains the prerequisite/review
guide; `requirements-elicitation` resolves ambiguity; `next-milestone-decision`
chooses direction. Authoring skills record the selected outcome.

The existing `karakana/requirements` engine already stores structured PRDs,
stories, issue drafts and readiness results. Preserve its IDs, states and source
provenance through an adapter. Acceptance strings currently lack individual IDs:
the adapter design must assign/persist stable criterion identities without using
row order as identity or silently breaking existing consumers.

Excel profiles should contain only the applicable tables. Shared metadata
includes project, artifact/workbook identity, schema version, document version,
baseline, source revision, requested action, owner/reviewer and dates. The workbook
details 24 proposed table contracts. Typed link rows express many-to-many
relationships by qualified IDs; baseline/version resolution must be defined in
P01. Narrative ADR/design sections can use multiple ordered rows.

The workbook is the current review medium. Existing machine schemas, source
diagrams and accepted repository ADRs may remain authoritative sources referenced
from it. Register that authority per artifact; never create two freely editable
masters. Editing a baseline must preserve history and reconsider earlier approvals.

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
and reconcile edits into a lossless review snapshot. Treat untrusted formula-like
strings as literal text and keep examples synthetic and secret-free.

The current protocol checker accepts readable nonempty files. It does not inspect
Excel sheets or evaluate content. A workbook may support several artifact kinds
only if the actual mapped content exists and has been substantively reviewed;
attaching the same path repeatedly is not proof. Keep a local validation/review
report alongside the workbook. Do not introduce a second lifecycle/approval
state machine or silently change existing protocol behavior in this update.

## Ordered implementation proposal

The workbook contains exact inspected/proposed paths, dependency edges, exit
evidence and requirement mappings for six slices:

1. **P01 — Agree schema and adapter.** Map current requirement/story identities,
   statuses and source provenance; define artifact profiles, links and authority.
   Review complete synthetic examples, including a tiny-task profile.
2. **P02 — Build narrow Excel tooling.** Add scoped read/write/validate/snapshot
   helpers with stale-overwrite and reviewer-preservation checks. Define supported
   workbook features and an appropriate optional dependency before changing code.
3. **P03 — Author focused skills.** Original instructions, conditional references,
   complete synthetic examples and meaningful behavior evals; start experimental.
4. **P04 — Update discovery.** Generate the catalogue index and add concise shared
   guidance and selected optional skillpack entries. Preserve permissions and
   avoid loading unrelated documentation workflows.
5. **P05 — Pilot and inspect actual output.** Synthetic feature, design/ADR and
   roadmap/release packs; office round trips, human comments, render/accessibility
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

Twenty update requirements map to 27 planned verification scenarios. They cover
the earlier inquiry-to-drafting mistake, request boundaries, project isolation,
IDs/links, measurable acceptance, decision history, forecast truth, release truth,
human edits, unrelated-file false assurance, licensing, formula correctness,
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
The workbook is formula-free. The renderer, JSON/XLSX record parity, IDs and
planned reference mappings are checked locally; rendered evidence and the exact
outcomes/limitations are recorded in the task verification artifact and append-only
handoff. No application behavior tests are needed for these documentation records.

To reproduce into a new file using the repository environment with openpyxl:

```bash
.venv/bin/python docs/skills/engineering-artifact-catalogue/render_workbook.py \
  --output /tmp/engineering-artifact-research-review.xlsx
```

Remaining work: review this proposal, then implement the accepted content/schema
and adapter slice before workbook tooling and skill authoring. Recommended next
task: **P01**, using the source register and inspected revisions as reusable
research; investigate only unresolved compatibility and status decisions.
