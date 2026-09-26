# Engineering artifact catalogue: detailed research and update plan

Status: Draft for review
Package version: 0.2
Research date: 2026-09-26
Export audience: research-review

This Markdown document is the canonical source for the detailed records below.
Read [RESEARCH.md](RESEARCH.md) for rationale and source limitations. The accompanying
JSON snapshot and Excel workbook are generated views. Workbook feedback is proposed
input for reviewed Markdown changes; it is never another editable master.

The width comments are presentation hints only. Keep stable IDs when editing records.
All verification scenarios and implementation slices below are planned, not executed.

## 00 Read Me

Purpose: Research and proposed update only; no catalogue or runtime changes are implemented.

<!-- workbook-widths: [27, 60, 76] -->

| Item | Value | Review guidance |
| --- | --- | --- |
| Package | Global engineering artifact catalogue research and update plan | Start with Findings, Skill Plan and Delivery Plan. |
| Version | 0.2 / Draft for review | Research conclusions and implementation proposal; no approval implied. |
| Research date | 2026-09-26 | Recheck changing standards and upstream versions before implementation. |
| Authority | User authorized research followed by planning | Implementation, installation, remote publishing and deployment are separate stages. |
| Format | Markdown is the primary authoring and version-controlled format | RESEARCH.md and PLAN.md are canonical for this package. XLSX and JSON are derived sharing/rendering outputs. |
| Scope | ADR, requirements, design, stories, roadmap, plan, releases and supporting evidence | General across Karakana projects; no LIMS release commitments are drafted here. |
| Recommendation | Four focused authoring skills plus one Excel format skill | Reuse elicitation, milestone choice, artifact gate, requirements engine and handoffs. |
| Review cells | Review Decision and Reviewer Comments columns on Skills, Requirements and Decisions | Yellow cells are editable; text labels also indicate purpose. |
| Review example | Requires revision / Keep forecast and commitment as distinct fields | Example guidance only; no stakeholder approval recorded. |
| Review decisions | Not reviewed; Agree with proposal; Requires revision; Needs decision | Agreeing with a proposal is not authorization to deploy or proof of tests. |
| Sources | 38 external primary/maintainer sources plus 5 local/upstream evidence entries | Public standards abstracts only; not a compliance audit. |
| Source boundary | Pinned community code reviewed as research only | No third-party skill is installed or copied into the catalogue. |
| Preserve edits | Workbook review is proposed feedback, not another master | Archive the annotated workbook, compare by stable ID, review proposed changes into Markdown and regenerate a new export. Never silently import agreement or overwrite comments. |
| Current formulas | None in this research workbook | It is a record pack. Future calculated models must verify recalculation and meaning. |
| Next action | Review proposed schema, skill split and ordered slices | Then implement the accepted first slice using skill-update protocol. |
| Known limitations | Paid normative standards not read; Excel desktop accessibility test remains pending | LibreOffice rendering and structural checks are evidence, not Excel certification. |
| Audience | Research-review: complete evidence and proposed catalogue update | Other audience profiles are defined in 14 Audience Profiles for later implementation; this helper renders this review package only. |
| Canonical sources | RESEARCH.md (rationale) and PLAN.md (all detailed records) | Edit Markdown first. The renderer derives the JSON snapshot and workbook directly from PLAN.md. |
| Export provenance | Source path/hash, audience and generated UTC time are in workbook document properties and JSON metadata | Compare the source SHA-256 with the current PLAN.md bytes to detect staleness. Do not treat an export as current without checking its source. |

## 01 Sources

Purpose: Primary source register; conclusions are paraphrased and local adoption is explicitly tailored.

<!-- workbook-widths: [13, 32, 29, 42, 17, 64, 67, 48] -->

| Source ID | Title | Authority type | Version or revision | Reviewed date | Evidence finding | Adoption limit | Reference |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | ISO/IEC/IEEE 29148 | Standard | 2018; public publisher abstract | 2026-09-26 | Requirements engineering includes requirements-related processes and information content. | Abstract only; no clause-level compliance claim. | https://standards.ieee.org/ieee/29148/6937/ |
| S02 | ISO/IEC/IEEE 42010 | Standard | 2022; public abstract | 2026-09-26 | Architecture descriptions address stakeholders, concerns and viewpoints. | Public summary only; local template is tailored. | https://www.iso.org/standard/74393.html |
| S03 | ISO/IEC/IEEE 12207 | Standard | 2026; public abstract | 2026-09-26 | Software lifecycle processes provide lifecycle context for delivery. | Public summary only; do not assume 15289:2019 mappings already cover this edition. | https://www.iso.org/standard/90219.html |
| S04 | ISO/IEC/IEEE 15289 | Standard | 2019; confirmed 2025; revision under development | 2026-09-26 | Defines purposes/content of lifecycle information items; combining items is supported. | Public abstract only; does not prescribe Excel as a delivery medium. | https://www.iso.org/standard/74909.html |
| S05 | ISO/IEC 25010 | Standard | 2023; edition 2 | 2026-09-26 | Product quality model now has nine characteristics. | Do not repeat the older eight-category model as the current edition; public abstract only. | https://www.iso.org/standard/78176.html |
| S06 | IEEE 1016 | Historical standard | 2009; inactive-reserved since 2020 | 2026-09-26 | Software design descriptions communicate design information to stakeholders. | Historical guidance; must not label it an active standard. | https://standards.ieee.org/ieee/1016/4502/ |
| S07 | NASA requirements checklist | Public engineering guidance | Systems Engineering Handbook Appendix C | 2026-09-26 | Requirements should be unambiguous, uniquely identified and verifiable. | Use the writing/checking technique; do not import NASA project governance. | https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/ |
| S08 | IIBA requirements and designs | Business analysis guidance | Business Analysis Standard, public section 4.4 | 2026-09-26 | Business, stakeholder, solution and transition types; bidirectional traceability. | Local data/workflow/reporting categories are subtypes or tags, not new BABOK classes. | https://www.iiba.org/knowledgehub/the-business-analysis-standard/4-implementing-business-analysis/4-4-understanding-requirements-and-designs/ |
| S09 | Agile Manifesto | Agile primary source | 2001 | 2026-09-26 | Documentation has value; working software and adaptation receive greater emphasis. | No inference that documentation is unnecessary or that all artifacts must precede all coding. | https://agilemanifesto.org/ |
| S10 | Scrum Guide | Agile primary source | November 2020 | 2026-09-26 | Product/Sprint Goals and Definition of Done provide commitments for empirical delivery. | Stories, story points, Definition of Ready and this workbook are local practices, not Scrum requirements. | https://scrumguides.org/scrum-guide.html |
| S11 | INVEST / SMART | Community originator | Bill Wake, 2003 | 2026-09-26 | Useful story-quality and task-quality heuristics; valuable vertical slicing. | Heuristics; estimates are not mandatory story points or promises. | https://xp123.com/invest-in-good-stories-and-smart-tasks/ |
| S12 | Card, Conversation, Confirmation | Community originator | Ron Jeffries, 2001 | 2026-09-26 | Story cards are supported by conversation and confirmation through acceptance examples. | A spreadsheet row alone is not a complete understanding or a test result. | https://ronjeffries.com/xprog/articles/expcardconversationconfirmation/ |
| S13 | Gherkin reference | Official implementation guidance | Current reference reviewed | 2026-09-26 | Given/When/Then express context, event and observable outcome. | Use examples without requiring Cucumber installation; prose in Excel is not an executed test. | https://cucumber.io/docs/gherkin/reference/ |
| S14 | GO Product Roadmap | Community originator | Updated 2026-01-12 | 2026-09-26 | Connect roadmap outcomes to time horizons, broad capabilities and success measures. | Original local structure; do not copy the CC BY-SA template or promise forecast dates. | https://www.romanpichler.com/blog/goal-oriented-agile-product-roadmap |
| S15 | Nygard ADR | Community originator | 2011 | 2026-09-26 | Small records preserve decision context, status and consequences; retain superseded decisions. | Author ADRs as repository Markdown; workbook summaries link the complete record. | https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions |
| S16 | MADR | Maintainer implementation | Maintainer site reviewed | 2026-09-26 | Decision drivers, options and consequences support transparent architectural choices. | Use concise local fields; check license/version before copying any template. | https://adr.github.io/madr/ |
| S17 | arc42 | Maintainer implementation | Current overview reviewed | 2026-09-26 | Tailorable architecture views cover context, runtime, deployment, quality and decisions. | Use a relevant subset; do not require twelve sections for every change or copy licensed text. | https://arc42.org/overview/ |
| S18 | C4 | Community originator | Creator site reviewed | 2026-09-26 | Hierarchical architecture views support communication at different levels of detail. | Choose diagrams for audience; maintain source files and accessible descriptions outside cell-sized summaries. | https://c4model.com/ |
| S19 | ISTQB acceptance testing | Testing body public guidance | CT-AcT public overview and 2019 syllabus | 2026-09-26 | Collaborative acceptance criteria/test design includes business and quality requirements. | Training guidance; no certification claim; test result needs actual execution evidence. | https://istqb.org/certifications/certified-tester-acceptance-testing/ |
| S20 | NIST SSDF | Public security framework | SP 800-218, version 1.1, final 2022 | 2026-09-26 | Integrate security requirements, design and release provenance into the lifecycle. | Use final guidance as research basis; spreadsheet records do not establish security compliance. | https://csrc.nist.gov/pubs/sp/800/218/final |
| S21 | NIST SSDF update status | Public draft | Version 1.2, initial public draft, 2025-12-17 | 2026-09-26 | A newer SSDF revision is explicitly still a public draft on the inspected page. | Track separately from the final 1.1 reference; recheck on implementation. | https://csrc.nist.gov/pubs/sp/800/218/r1/ipd |
| S22 | OWASP SAMM | Maintainer security model | v2 model | 2026-09-26 | Security spans governance, design, implementation, verification and operations. | Risk-tailored considerations; do not make every assessment a full security audit. | https://owaspsamm.org/model/ |
| S23 | DORA small batches | Primary research programme | Current capability guidance | 2026-09-26 | Small independently useful batches shorten feedback cycles. | Do not substitute document counts or checklist completion for delivery outcomes. | https://dora.dev/capabilities/working-in-small-batches/ |
| S24 | Google engineering review | Maintainer practice | Current published practice | 2026-09-26 | Review design, behavior, complexity, tests and documentation. | Agent self-review remains distinct from independent review. | https://google.github.io/eng-practices/review/reviewer/looking-for.html |
| S25 | Keep a Changelog | Maintainer convention | 1.1.0 | 2026-09-26 | Curate human-readable release changes by version and category. | Commit logs alone are insufficient; user-facing notes still require audience/context. | https://keepachangelog.com/en/1.1.0/ |
| S26 | Semantic Versioning | Maintainer specification | 2.0.0 | 2026-09-26 | Version changes describe compatibility relative to a declared public API. | Adopt only if the project defines that contract; do not force SemVer onto every product. | https://semver.org/ |
| S27 | Diataxis | Maintainer documentation framework | Current framework overview | 2026-09-26 | Separate learning, task, reference and explanatory documentation needs. | Engineering records need their own semantics; do not treat an ADR as a user tutorial. | https://diataxis.fr/ |
| S28 | Agent Skills specification | Maintainer open format | Current specification reviewed | 2026-09-26 | Metadata, instructions and optional resources enable progressive disclosure. | Karakana adds required metadata; import syntax is not automatically compatible. | https://agentskills.io/specification |
| S29 | Anthropic example/document skills | Maintainer skills implementation | 33375500bcea98d610eb30ce10ac4e59b89c390d | 2026-09-26 | Examples distinguish domain workflow skills from document-format skills. | Repository states document skills are source-available; xlsx is proprietary. Do not import or adapt those files. | https://github.com/anthropics/skills/tree/33375500bcea98d610eb30ce10ac4e59b89c390d |
| S30 | Anthropic doc-coauthoring | Maintainer skills implementation | Pinned as S29 | 2026-09-26 | Context, revision and reader testing are explicit documentation concerns. | Folder-specific license was not resolved; no copying. Do not inherit repeated permission questions or automatic delegation. | https://github.com/anthropics/skills/blob/33375500bcea98d610eb30ce10ac4e59b89c390d/skills/doc-coauthoring/SKILL.md |
| S31 | Matt Pocock engineering skills | Community maintainer implementation | c55ee46073ed923f86ce59a5eb3b6d895095d1b7; MIT | 2026-09-26 | to-spec, to-tickets and writing-for-agents provide spec, slice-dependency and disclosure examples. | Synthesis/publishing and setup assumptions need adaptation; current names differ from older to-prd/to-issues review. | https://github.com/mattpocock/skills/tree/c55ee46073ed923f86ce59a5eb3b6d895095d1b7 |
| S32 | Superpowers planning skills | Community maintainer implementation | 8ca22dba9a94f28898bbce59f2537ff4d87c747d; MIT | 2026-09-26 | Plans name files, constraints, interfaces, tasks and checks for another engineer. | Borrow bounded plan content, not mandatory subagent execution or a second orchestration framework. | https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/writing-plans/SKILL.md |
| S33 | Microsoft accessible Excel | Official product guidance | Current Microsoft support guidance | 2026-09-26 | Use simple named tables, clear headers, meaningful sheet/link names and accessible presentation. | Run actual accessibility review; styling alone does not prove accessibility. | https://support.microsoft.com/en-us/accessibility/excel/accessibility-best-practices-with-excel-spreadsheets |
| S34 | Microsoft Excel tables | Official product guidance | Current support guidance | 2026-09-26 | Named tables and structured references support readable workbook structure. | IDs, not physical row positions, define engineering relationships. | https://support.microsoft.com/en-us/excel/using-structured-references-with-excel-tables |
| S35 | openpyxl formulae | Official library documentation | Stable documentation reviewed | 2026-09-26 | openpyxl stores formulas but does not evaluate them. | If formulas are used, recalculate with a compatible engine and verify expected results. | https://openpyxl.readthedocs.io/en/stable/simple_formulae.html |
| S36 | openpyxl validation | Official library documentation | Stable documentation reviewed | 2026-09-26 | Data validation metadata is not enforced by the Python library. | Validate values after human edits; dropdowns are assistance, not integrity/security guarantees. | https://openpyxl.readthedocs.io/en/stable/validation.html |
| S37 | openpyxl tables | Official library documentation | Stable documentation reviewed | 2026-09-26 | Table names must be unique; table headers need text values. | Validate table/print ranges after row additions and application round trips. | https://openpyxl.readthedocs.io/en/stable/worksheet_tables.html |
| S38 | WCAG | W3C recommendation | WCAG 2.2 | 2026-09-26 | Provides a reference for applicable web accessibility requirements. | For application UX artifacts; Microsoft guidance governs workbook-specific presentation checks. | https://www.w3.org/TR/WCAG22/ |
| L01 | Karakana engineering process | Local accepted process | 5e4cb9fdf137900180d76a1304f194021580b825 | 2026-09-26 | Risk-tailored lifecycle, authority boundaries and separate presence/substantive review. | This proposal complements it; it does not replace or weaken its gates. | docs/engineering-process.md |
| L02 | Karakana skills and requirements engine | Local inspected code | 5e4cb9fdf137900180d76a1304f194021580b825 | 2026-09-26 | Structured PRDs/stories/readiness and skill validation already exist. | Extend existing sources and IDs; avoid a parallel PRD generator or approval state machine. | karakana/requirements/schemas.py |
| L03 | Ent-meal engineering baseline | Upstream inspected project | 90d32e220f798858918c1e2177e5b34ad3a0f401; draft | 2026-09-26 | Provides requirement convention, prioritization framework and per-release output checklist. | Reuse generic guidance only; project terminology, candidate phases and owner roles are not global commitments. | https://github.com/mdudaj/ent-meal/tree/90d32e220f798858918c1e2177e5b34ad3a0f401/docs/requirements/baseline |
| L04 | Ent-meal Excel generator | Upstream inspected code | 90d32e220f798858918c1e2177e5b34ad3a0f401 | 2026-09-26 | Five-sheet review pack uses IDs, dropdowns, filters, freeze panes and sign-off. | No named Excel Tables; sheet-level source trace; inferred priorities and generic acceptance basis need strengthening. | https://github.com/mdudaj/ent-meal/blob/90d32e220f798858918c1e2177e5b34ad3a0f401/scripts/render_baseline_confirmation_excel.py |
| L05 | Karakana artifact checker | Local inspected code | 5e4cb9fdf137900180d76a1304f194021580b825 | 2026-09-26 | Readable nonempty file evidence satisfies current presence checks. | Attaching one workbook under multiple kinds does not prove that each artifact has substantive content. | karakana/protocols/checks.py |

## 02 Findings

Purpose: Research synthesis; proposed local policies are design decisions, not verbatim standard requirements.

<!-- workbook-widths: [13, 48, 25, 66, 72] -->

| Finding ID | Finding | Evidence IDs | Proposed application | Verification or caveat |
| --- | --- | --- | --- | --- |
| F01 | Maintain decision-useful information across the lifecycle | S01; S03; S04; L01 | One artifact catalogue maps content to lifecycle stage and risk. | Reuse or combine records for small tasks; not every sheet is mandatory. |
| F02 | Requirements and user stories serve different purposes | S07; S08; S11; S12 | Requirements describe testable needs/constraints; stories describe useful slices. | Link both; avoid forcing technical constraints into artificial user stories. |
| F03 | Readiness and completion evidence have different meanings | S10; S19; L01; L05 | Separate acceptance criteria, execution results, readiness checks and approval records. | A populated cell or passing file gate never means a test or review passed. |
| F04 | ADRs explain consequential decisions | S15; S16 | Capture drivers, options, rationale and positive/negative consequences. | Retain and link superseded records; do not silently rewrite an accepted decision. |
| F05 | Design needs audience-specific views | S02; S17; S18 | Use context, boundary, interface, runtime and deployment views when relevant. | Keep diagrams/source contracts linked and describe them in text. |
| F06 | Agile planning changes with evidence | S09; S10; S14; S23 | Outcome-based roadmap; coarse horizons; small implementation slices. | Forecast, agreed release scope and actual delivery are separate fields. |
| F07 | Release notes and release authorization are distinct | S25; S26; S20; L01 | Versioned audience-facing notes link scope, tests, limitations and operations. | Version scheme requires a project contract; release drafting never publishes. |
| F08 | Use focused skills with conditional references | S28; S31; S32; L02 | Four Markdown authoring skills and an audience-specific Excel export/review skill. | Descriptions must distinguish catalogue inquiry, research, planning, drafting and execution. |
| F09 | Deterministic workbook integrity belongs in tooling | S34; S35; S36; S37 | Validate IDs, references, enums, provenance, table ranges and workbook structure. | Heuristics flag questionable prose; human review judges meaning and adequacy. |
| F10 | Markdown authority and review evidence must survive audience sharing | S36; L04 | Versioned Markdown records are canonical; workbook comments produce reviewed change proposals against source IDs and revisions. | Preserve annotated exports; flag stale source versions and conflicting feedback. No automatic Markdown writes or approval import. |
| F11 | Draft standards and inactive standards need explicit labels | S05; S06; S21 | Version the standards register and record review dates/status. | 25010:2023 is current inspected model; 1016:2009 historical; SSDF 1.2 draft. |
| F12 | Ent-meal is a reusable source, not an installable skill | L03; L04 | Borrow review pack organization, source fields and per-release outputs. | Do not import CRDB roles, terminology, priorities or proposed release phases. |
| F13 | Workbook usability is part of artifact quality | S33; S37 | Named tables, clear headers, freeze panes, wrap, navigation and no merged data cells. | Check rendered examples and assistive accessibility; color alone does not carry status. |
| F14 | Community skills require permission and license adaptation | S29; S30; S31; S32 | Write original Karakana guidance; record inspirations and pinned provenance. | No proprietary document-skill import; no automatic tracker publication or delegation. |
| F15 | Global guidance must preserve project provenance | L01; L02; L03 | Require project ID, artifact ID, revision and explicitly scoped links. | Cross-project lessons may be reused; project records are never silently mixed. |

## 03 Ent Meal Reuse

Purpose: Evidence at ent-meal origin/main 90d32e2; recommendations do not change ent-meal.

<!-- workbook-widths: [13, 45, 51, 75, 23] -->

| Reuse ID | Inspected surface | Retain | Enhance for global use | Evidence IDs |
| --- | --- | --- | --- | --- |
| EM01 | 00 documentation convention | Testable statements, attributes, source and traceability intent | Version sources and distinguish BABOK classes from local tags. | L03; S01; S08 |
| EM02 | 04 roadmap framework | Business/data/dependency/UAT prioritization criteria | Record outcomes, confidence, priority decision owner and commitment evidence. | L03; S14 |
| EM03 | 05 methodology | Incremental delivery, ready/done, per-release outputs | Add immutable revision/environment, evidence links and separate release/deployment/acceptance state. | L03; L01 |
| EM04 | Generated XLSX | Cover/sign-off, review instructions, stable IDs, comments, filters and dropdowns | Use named Excel Tables; active profile selects relevant sheets; avoid merged cells. | L04; S33; S37 |
| EM05 | Traceability sheet | Source document pointers | Add typed item-level links: need -> requirement -> story -> design/ADR -> test -> release. | L04; S08 |
| EM06 | _priority_from_requirement / _priority_from_status | Candidate priority can assist discussion | Do not default to P1/P2 from prefix or unknown status; store proposal separately from agreed priority. | L04 |
| EM07 | _derived_acceptance_basis | Business-level acceptance review is useful | Add criterion IDs, observable thresholds, verification method and real evidence; label generated basis as draft. | L04; S07; S19 |
| EM08 | Generation/editing lifecycle | Deterministic generation and version snapshots | Archive annotated exports; compare feedback by source ID/revision; review changes into Markdown before regeneration. | L04; S36 |
| EM09 | Project scope | Explicit baseline/review status | Generic examples only; no TACATDP/CRDB releases copied into another project. | L03; L01 |

## 04 Artifact Catalogue

Purpose: Proposed artifact content contract; minimum content is tailored by task and risk.

<!-- workbook-widths: [13, 35, 39, 78, 31, 69, 25] -->

| Artifact ID | Artifact type | When needed | Minimum content | Accountability | Quality review | Evidence IDs |
| --- | --- | --- | --- | --- | --- | --- |
| ART01 | Product brief / PRD | New product or meaningful capability | Problem; users; outcomes; scope/non-goals; assumptions; success measures; linked requirements | Product/request owner + author | Evidence-backed problem and explicit non-goals; distinguish hypotheses. | L01; L02; S08 |
| ART02 | Requirements baseline | Feature/change definition | Stable ID; class/tags; statement; rationale; source; actor; priority proposal/agreement; acceptance IDs | Requirements owner | Atomic, clear, feasible, traceable and verifiable; quality constraints measurable. | S01; S07; S08 |
| ART03 | User stories / backlog items | User-visible slices | Actor; goal; benefit; requirement links; conversation notes; acceptance IDs; dependencies; estimate basis | Product owner + delivery team | Useful small slices; do not claim INVEST forces independence without dependencies. | S11; S12; S10 |
| ART04 | Acceptance criteria | Every meaningful delivery | Criterion ID; linked need/story; context/event/outcome or rule; threshold; verification method | Business owner + tester | Observable pass/fail boundary; distinguish examples from executable tests. | S07; S13; S19 |
| ART05 | ADR / decision record | Consequential architecture or hard-to-reverse choice | Context; drivers; options; decision; rationale; consequences; status; owner; replacement link | Decision authority + architect | Compare plausible alternatives; proposed/accepted distinct; retain decision history. | S15; S16 |
| ART06 | Architecture / design description | Affected components/contracts/views | Stakeholders/concerns; scope; views; interfaces; data/state; scenarios; constraints; tradeoffs; diagrams | Design owner | Cover applicable quality/security/UX/operations; inspect implementation evidence. | S02; S17; S18 |
| ART07 | UX / interaction specification | User experience change | User tasks; behavior; look/feel; states; content; responsive/a11y; shared component refs; acceptance | UX/product + engineering | Reuse active design system and existing UX skills; linked render evidence. | L01; S38 |
| ART08 | API / data / schema contract | Persisted or exchanged data boundary | Versioned source schema; semantics; examples; validation; compatibility; migration; owner | Contract owner | Use authoritative machine-readable schema; Markdown describes and links it, with optional workbook summaries. | L01; S17 |
| ART09 | Roadmap | Product direction across releases | Outcome; audience; horizon; confidence; dependencies; broad capabilities; metric; review trigger | Product owner | Forecast separated from commitment; no invented stakeholder dates or priorities. | S14; S09 |
| ART10 | Milestone / delivery plan | Multi-step bounded work | Goal; ordered slices; dependencies; owner; estimate basis; checkpoints; acceptance and risks | Delivery lead | Small demonstrable units; explicit blockers and review points. | S23; S10 |
| ART11 | Implementation plan | Accepted change before code | Inspect-first files; source revision; tasks/files/interfaces; checks; approvals; applicable rollback | Implementation lead | Another engineer can act; avoid writing speculative code or repeating satisfied research. | S32; L01 |
| ART12 | Release plan / assurance | Preparing release for real use | Release scope/version; candidate revision; target; evidence; blockers; rollout; recovery; monitoring/support; approvals | Release operator + product owner | Conditional readiness; unresolved blocker cannot become green via a count. | S20; S19; L01 |
| ART13 | Release notes / changelog | User-facing release communication | Version/date; audience; delivered changes; fixed issues; compatibility; migration; limitations; support links | Release author + reviewer | Evidence-based changes; planned features not listed as delivered; no raw commit dump. | S25; S26 |
| ART14 | Test / UAT plan and results | Applicable verification and acceptance | Case ID; linked criteria; preconditions; steps; expected; actual; revision/environment; result; evidence | Tester/UAT reviewer | Not run distinct from pass; human acceptance distinct from automated checks. | S19; S13 |
| ART15 | Risk / assumption / dependency register | Material uncertainty or exposure | Type; impact; likelihood or rationale; owner; mitigation; trigger; decision deadline; status; evidence | Named risk/decision owner | Do not manufacture numerical confidence or ownership. | S22; L01 |
| ART16 | Change / baseline history | Revision to agreed artifact | Change ID; old/new baseline; reason; impact; affected IDs; reviewer; approval/evidence; supersedes | Artifact owner | Approved records retained; changed text does not silently inherit old approval. | S08; S15; L01 |
| ART17 | User guidance / operational handover | Adoption, support or first use | Audience; tasks; access/setup; limitations; support; recovery/operations links; owner; verified revision | Product/support owner | Task guidance useful without implementation jargon; link authoritative runbooks. | S27; L01 |
| ART18 | Delivery / review / handoff record | End of bounded task | State; changed refs; verification; risks; unresolved work; next action/model; continuation evidence | Author + actual reviewer | Report implemented/verified/merged/deployed/accepted separately. | L01; L05 |

## 05 Skill Plan

Purpose: Names and boundaries are proposed; no new skills have been created.

<!-- workbook-widths: [13, 34, 64, 62, 61, 24, 64] -->

| Skill ID | Proposed skill | Output boundary | Existing capability to reuse | Resources proposed | Review Decision | Reviewer Comments |
| --- | --- | --- | --- | --- | --- | --- |
| SK01 | engineering-requirements | Evidence-backed requirements, stories, acceptance and traceability authoring/revision in Markdown, with stable source IDs and revision history | requirements-elicitation; karakana/requirements; grill-with-docs | references/requirements.md; stories-and-acceptance.md; traceability.md; evals | Not reviewed | Unresolved terms remain explicit; no second PRD/issue generator. |
| SK02 | engineering-design-records | ADR and architecture/design description authoring/review in Markdown, with stable source IDs and revision history | system-design-thinking; domain/UX skills; architecture-decision protocol | references/adr.md; design-views.md; contracts-and-quality.md; evals | Not reviewed | Use a proposed decision until actual authority accepts it. |
| SK03 | engineering-delivery-planning | Roadmap, milestone and bounded implementation plan in Markdown, with stable source IDs and revision history | next-milestone-decision; existing requirements/issues drafts; engineering process | references/roadmap.md; milestones.md; implementation-plan.md; evals | Not reviewed | Recommendation skill chooses what next; this skill records the chosen direction. |
| SK04 | engineering-release-documentation | Release plan/assurance, notes and adoption/handover pack in Markdown, with stable source IDs and revision history | release-change protocol; release checks; karakana-handoff; project runbooks | references/release-plan.md; release-notes.md; adoption-and-handover.md; evals | Not reviewed | Drafting is distinct from publishing, deploying and approving operational use. |
| SK05 | engineering-workbooks | Derived audience Excel exports, integrity/freshness checks and feedback comparison against Markdown | Existing requirements schema; new narrow deterministic tools; openpyxl | references/workbook-contract.md; audience-profiles.md; assets/export templates; tool adapter; evals | Not reviewed | Sharing/review only. Source content stays in Markdown; existing machine schemas and diagrams retain their explicitly linked authority. |

## 06 Workbook Contract

Purpose: Derived export table contracts selected per audience; canonical narrative and records remain in Markdown. Not every table belongs in every export.

<!-- workbook-widths: [13, 31, 35, 87, 35, 76] -->

| Schema ID | Sheet or table | Row identity | Essential fields beyond shared metadata | Applicability | Integrity rule |
| --- | --- | --- | --- | --- | --- |
| WB01 | Control | Workbook_ID | Project_ID; export ID; audience/profile version; generation time; source Markdown paths/IDs/revisions/hashes; schema/doc version; baseline; purpose; omitted content and full-source links | All profiles | Manifest identifies a derived sharing view. Source changes mark the export stale; never infer approval from generation. |
| WB02 | Artifact Register | Artifact_ID | Type; status; owner; canonical Markdown path/section; current baseline/revision; supersedes; applicability rationale | All profiles | Resolve each artifact to its canonical Markdown record; link authoritative machine schema/diagram sources separately. |
| WB03 | Sources | Source_ID | URI/path; publisher; source revision/date; inspected date; claim scope; limitation | All profiles | Claims reference inspected sources; inaccessible evidence marked unavailable. |
| WB04 | Requirements | Requirement_ID | Class; tags; statement; rationale; actor; source; proposed priority; agreed priority; decision evidence | Requirements profile | No inferred agreement from prefix or blank priority; one testable need per row. |
| WB05 | Stories | Story_ID | Actor; goal; benefit; conversation note; scope; dependency; estimate/basis | Requirements profile | Story is a slice, not a duplicate of every requirement. |
| WB06 | Acceptance | Criterion_ID | Context; event; expected outcome; measurable condition; method; owner | Requirements and relevant profiles | Criterion references need/story; test outcomes stored separately. |
| WB07 | ADRs | ADR_ID | Title; decision state; drivers; options; decision; rationale; consequences; decision owner; superseded_by | Design profile | No ID reuse; accepted decisions need actual evidence and history. |
| WB08 | ADR Summaries and Source Links | ADR_ID + section + sequence | Decision summary; rationale/consequence summary; canonical ADR path/section/revision; optional narrative extract | Design/engineering audience when useful | Complete ADR reasoning and history stay in Markdown; mark excerpts and link the full record. |
| WB09 | Design Views | Design_ID + View_ID | Concern; viewpoint; scope; element/interface; scenario; quality constraint; source diagram link/description | Design profile | Linked schemas/diagrams keep their repository authority and revision. |
| WB10 | UX and Contracts | Design_Element_ID | Behavior; states; copy; a11y; shared tokens/components; schema/API URI and version; examples | When UX/data/interface affected | Use existing UX/contract skills; no workbook-only machine schema. |
| WB11 | Roadmap | Outcome_ID | Audience; outcome; measure; horizon; confidence; proposal status; dependency; review trigger | Planning profile | No requirement-level feature list in strategic roadmap; dates remain forecasts unless agreed. |
| WB12 | Milestones | Milestone_ID | Goal; output; owner; checkpoint; acceptance; estimate basis; forecast/agreement evidence | Planning profile | Milestone acceptance and an estimate are distinct. |
| WB13 | Implementation Tasks | Task_ID | Inspect refs/revision; files; interface; steps; check command and expected result; owner; dependencies; approvals; rollback | Execution planning profile | Task instructions satisfy existing process; no execution side effects. |
| WB14 | Release Plan | Release_ID | Scope baseline; version scheme; candidate revision; target; gates; rollout; recovery; support; owner | Release profile | Release planned/published, deployment and user acceptance have separate facts. |
| WB15 | Release Notes | Note_ID | Release ID; category; audience; description; affected behavior; compatibility; migration; known limit; source evidence | Release profile | Planned scope is not a delivered note. |
| WB16 | Test Cases | Test_ID | Preconditions; steps; expected; verification method; test source; owner | Acceptance/verification profiles | Case definition is not execution. |
| WB17 | Test Runs | Run_ID | Test ID; actual result; status; revision; environment; executed date; executor; evidence ID | When verification performed | Not run/blocked/skipped/fail/pass are distinct; no synthetic pass. |
| WB18 | Risks and Decisions | Risk_ID or Question_ID | Type; uncertainty; impact; mitigation; trigger; owner; decision need; due horizon; evidence | When material uncertainty exists | Unconfirmed owner/date/threshold remains explicitly unconfirmed. |
| WB19 | Links | Link_ID | From_Project; From_Type; From_ID; Relation; To_Project; To_Type; To_ID; rationale | Every profile with multiple artifact types | One typed relationship per row; many-to-many; no reliance on row numbers or comma lists. |
| WB20 | Evidence | Evidence_ID | Artifact/test/review ref; URI/path; revision; environment; observed result; time; limitation; content hash when local | All profiles | Evidence points to a scoped observation; a path alone is not truth. |
| WB21 | Reviews and Approvals | Review_ID | Source artifact version; reviewer role/identity; feedback kind; proposed decision; timestamp; evidence; reconciliation status | Review or acceptance stage | Feedback is proposed input. Canonical review/approval evidence changes only after explicit review in the existing process; stale exports cannot update current approvals. |
| WB22 | Change History | Change_ID | Source change ID; artifact ID; old/new revision; reason; impact; reviewer; evidence; feedback/export reference | Revisions to baselined material | Derive history from versioned source; archive exports. Do not carry approval onto changed content. |
| WB23 | Guidance and Handover | Guide_ID | Audience; task; steps; support/runbook refs; limitation; owner; tested revision | Adoption/release profile | Link existing project runbooks; no invented live operational assurances. |
| WB24 | Vocabulary | Vocabulary_ID + value | Allowed classes; status values; relations; definitions; applicability labels | When schema-defined fields are used | Visible explanations; dropdowns assist entry, validator checks actual values. |

## 07 Update Requirements

Purpose: Proposed observable acceptance for the future catalogue update.

<!-- workbook-widths: [16, 39, 83, 23, 26, 24, 43] -->

| Requirement ID | Need | Acceptance condition | Basis IDs | Planned verification IDs | Review Decision | Reviewer Comments |
| --- | --- | --- | --- | --- | --- | --- |
| REQ01 | Preserve request type and permissions | Catalogue inquiry/research/plan does not draft product artifacts or publish anything. | L01; F08 | EV01; EV02; EV03 | Not reviewed |  |
| REQ02 | Global scope with project isolation | Shared guidance loads across projects; records require project/revision and intentional cross-project links. | F15 | EV04 | Not reviewed |  |
| REQ03 | Stable identities and typed traceability | IDs survive sorting/reordering; every relationship resolves to the declared project/type/version. | F02; F09 | EV05; EV06 | Not reviewed |  |
| REQ04 | Verifiable requirements and stories | Applicable acceptance includes observable behavior/thresholds and links actual evidence when available. | F02; F03 | EV07; EV08 | Not reviewed |  |
| REQ05 | ADRs preserve options and history | Records cover significant decisions and keep superseded versions with evidence of acceptance. | F04 | EV09 | Not reviewed |  |
| REQ06 | Design describes relevant views | Design links quality/security/UX/data/operations and authoritative diagrams or contracts. | F05 | EV10 | Not reviewed |  |
| REQ07 | Forecasts stay distinct from commitments | Roadmaps show outcomes, horizon, confidence and agreement evidence without manufacturing dates/priorities. | F06; EM06 | EV11 | Not reviewed |  |
| REQ08 | Release records distinguish states | Release plan, notes, publication, deployment and acceptance remain separate and evidence-backed. | F07 | EV12; EV13 | Not reviewed |  |
| REQ09 | Markdown primary; Excel accompanies each relevant audience | Author/version engineering artifacts in Markdown. Export selected audience tables with source paths/IDs/revisions/hashes, audience/profile, generated date, omissions and full-source links. JSON is a derived rendering snapshot. | User correction; F10; F13 | EV14; EV28; EV29 | Not reviewed |  |
| REQ10 | Preserve feedback without competing editable masters | Archive annotated exports; compare feedback by stable source ID/version, flag stale/conflicting input, and review changes into Markdown before regenerating. No automatic source or approval updates. | F10 | EV15; EV16; EV29 | Not reviewed |  |
| REQ11 | Validate structural integrity | Reject duplicate IDs, broken links, missing provenance, invalid enums and claimed approval without evidence. | F09 | EV05; EV06; EV17 | Not reviewed |  |
| REQ12 | Separate structure from semantic review | Validation reports factual integrity; substantive review judges adequacy; neither grants external authority. | F03; L05 | EV18 | Not reviewed |  |
| REQ13 | Proportional profiles | Tiny fixes and research use compact existing records; meaningful features/releases select applicable artifacts. | F01 | EV19; EV28 | Not reviewed |  |
| REQ14 | Reuse existing harness capabilities | Existing requirements IDs/store/readiness, protocols, skills/index/evals/handoffs remain authoritative. | L02; F08 | EV20 | Not reviewed |  |
| REQ15 | Portable skills and explicit licensing | Valid Karakana metadata; conditional references; original text; license checks before reuse. | F14; S28 | EV21; EV22 | Not reviewed |  |
| REQ16 | Readable and accessible workbooks | Text statuses, named tables, no merged data cells, useful widths/heights, navigation and review instructions. | F13 | EV14; EV23 | Not reviewed |  |
| REQ17 | Calculation correctness when used | No external-workbook dependencies by default; formulas recalculated and checked against expected outcomes. | S35; F09 | EV24 | Not reviewed |  |
| REQ18 | Safe literal text | Untrusted leading formula-like text is preserved as literal; project records contain no secrets/real example PII. | L01; F09 | EV25 | Not reviewed |  |
| REQ19 | Controlled catalogue rollout | Experimental first; focused skillpack enablement and evidence-driven pilot before stable promotion. | L01; F08 | EV26 | Not reviewed |  |
| REQ20 | Versioned standards register | Source edition/status/review dates and limitations are recorded; no certification claims. | F11 | EV27 | Not reviewed |  |

## 08 Verification Plan

Purpose: These are planned behavioral scenarios for implementation; none are represented as already passed.

<!-- workbook-widths: [17, 31, 66, 84, 26] -->

| Verification ID | Scenario | Input or trigger | Expected observable behavior | Requirement IDs |
| --- | --- | --- | --- | --- |
| EV01 | Skill inquiry | Ask whether roadmap skills exist. | Answer catalogue question; create no roadmap or release draft. | REQ01 |
| EV02 | Research/plan only | Request this research and update plan. | Create evidence and plan; no skill installation or runtime changes. | REQ01 |
| EV03 | Remote boundary | Ask for local release notes only. | Create reviewed local artifact without tracker, push, publish or deploy. | REQ01 |
| EV04 | Project boundary | Combine records with identical short IDs from two projects. | Qualified IDs keep them separate; cross-project link needs explicit intent. | REQ02 |
| EV05 | Identity integrity | Duplicate an artifact ID and sort its rows. | Duplicate rejected; valid relations survive row sorting. | REQ03; REQ11 |
| EV06 | Reference integrity | Delete a linked requirement or provide an unknown relation. | Report broken endpoint/relation with sheet and stable ID. | REQ03; REQ11 |
| EV07 | Requirement quality | Provide vague speed/security claims without thresholds. | Flag missing measurable acceptance and source; do not invent numbers. | REQ04 |
| EV08 | Evidence distinction | Fill acceptance text but mark test Not run. | Keep result Not run; do not describe acceptance as verified. | REQ04 |
| EV09 | Decision history | Change a previously accepted ADR. | Create revised/superseding record; retain original and reconsider approval. | REQ05 |
| EV10 | Design scope | Specify a workflow/API change with runtime and data effects. | Cover applicable concerns and link existing authoritative contracts/views. | REQ06 |
| EV11 | Priority/forecast | Unprioritized requirements with FR prefixes and a requested presentation date. | Candidate priority and forecast remain proposals; no assumed release commitment. | REQ07 |
| EV12 | Release truth | PR merged but deployment and UAT unknown. | Notes distinguish implementation, publication, deployed state and acceptance. | REQ08 |
| EV13 | Operational blocker | Release gate has missing restore evidence. | Preserve blocker and required action; documentation completeness does not override it. | REQ08 |
| EV14 | Markdown source and audience workbook | Author one meaningful feature/release record in Markdown, then request an audience export. | Markdown contains the complete canonical record; Excel carries relevant navigable tables, stable source IDs/links, profile/version and freshness metadata. | REQ09; REQ16 |
| EV15 | Workbook feedback reconciliation | Reviewer comments and proposes a changed priority/decision in an audience workbook. | Report proposals by source ID/version; preserve original feedback; apply only reviewed changes to Markdown. Workbook agreement never imports source approval. | REQ10 |
| EV16 | Workbook round trip | Edit/reopen XLSX through target office application. | Source locators, headers, IDs, links, formulas and review cells preserved or differences reported; original annotated workbook remains archived. | REQ10 |
| EV17 | Invalid approval | Type Accepted without approver/timestamp/evidence for a governed decision. | Report insufficient acceptance evidence; no authorization inferred. | REQ11 |
| EV18 | Gate limitation | Attach unrelated nonempty workbook under several artifact kinds. | Presence may pass; substantive review detects absent content and refuses completion claim. | REQ12 |
| EV19 | Tiny task | Fix a typo or perform a read-only inventory. | Reuse compact record; do not force all workbook sheets or an ADR. | REQ13 |
| EV20 | Existing engine adapter | Reference existing PRD/story identities through Markdown and export them to Excel. | Preserve engine identities/source metadata through the adapter, identify authoritative machine fields and avoid a competing PRD or workbook master. | REQ14 |
| EV21 | Skill discovery | Validate focused descriptions and conditional references. | Correct workflow selected; unrelated academic/image/product tasks do not trigger it. | REQ15 |
| EV22 | License boundary | Propose importing proprietary xlsx skill. | Reject bundled copying; original tools use official library/product guidance. | REQ15 |
| EV23 | Human readability | Review long ADR sections and a wide requirements table. | Useful wrapping/row heights, clear labels, table navigation and accessibility review. | REQ16 |
| EV24 | Formula correctness | Add counts/coverage formulas and modify source rows. | Recalculate; compare cached outputs to expected values; errors/stale caches reported. | REQ17 |
| EV25 | Literal text/security | Include example text starting =, +, -, @ and a sensitive-value candidate. | Treat untrusted text as text; legitimate formulas use explicit formula fields; secrets excluded. | REQ18 |
| EV26 | Pilot/promotion | Run synthetic cross-project feature/design/release scenarios. | Record observed results and gaps; no stable promotion solely from passing schema checks. | REQ19 |
| EV27 | Standards freshness | Supply IEEE 1016 as active and SSDF 1.2 as final. | Correct statuses and record public-summary limits; no compliance certification. | REQ20 |
| EV28 | Audience projection | Export the same baseline for product, engineering, QA/UAT, operations and executive audiences. | Each profile selects useful fields/views and declares omissions/full-source links; relevant blockers, limitations, uncertainty and trace IDs survive every applicable projection. | REQ09; REQ13 |
| EV29 | Stale source or conflicting feedback | Change Markdown after export; return two conflicting annotated exports. | Compare source revisions/hashes, report staleness/conflicts, preserve both inputs and require review against current source before changes. No silent import or overwrite. | REQ09; REQ10 |

## 09 Delivery Plan

Purpose: Ordered proposal; estimates and owners remain to be assigned rather than invented.

<!-- workbook-widths: [13, 43, 22, 78, 100, 87, 39] -->

| Slice ID | Outcome | Depends on | Files to inspect or change | Implementation instructions | Exit evidence | Requirement IDs |
| --- | --- | --- | --- | --- | --- | --- |
| P01 | Agree Markdown content contract, source authority and export adapter | Research/plan review | karakana/requirements/schemas.py; store.py; readiness.py; protocols/checks.py; docs/engineering-process.md; proposed docs/engineering-artifacts.md | Map existing PRD/story identities and machine-field authority to canonical Markdown records; define stable criterion IDs, source sections, typed relations and review history. Specify audience selection, export manifest/freshness and feedback reconciliation. Keep machine schemas/diagrams authoritative for their own content. Record consequential adapter decisions before code. | Reviewed Markdown contract and complete tiny/feature/design/release examples; five audience mappings, source-to-field mapping and conflict/freshness rules. | REQ02; REQ03; REQ04; REQ09; REQ10; REQ13; REQ14; REQ20 |
| P02 | Markdown-to-Excel export and feedback reporting | P01 | Proposed karakana/tools/engineering_artifacts.py; tests/test_engineering_artifacts_workbooks.py; chosen optional dependency group in pyproject.toml | Implement narrow Markdown read/validate, audience export and feedback-diff helpers. Validate source version/hash and stable IDs; flag stale/conflicting feedback; preserve annotated outputs and unsupported workbook content. Source changes require explicit review; no automatic approval import, remote actions or two-way master synchronization. Scope supported features and optional dependency. | Functional fixtures prove source/export parity, audience omissions and blocker visibility, traceability, literal text, freshness, conflicting feedback, no-overwrite and office round trips. | REQ03; REQ09; REQ10; REQ11; REQ12; REQ16; REQ17; REQ18 |
| P03 | Focused authoring skills and original references | P01; P02 | Proposed skills/engineering-requirements/; engineering-design-records/; engineering-delivery-planning/; engineering-release-documentation/; engineering-workbooks/ | Write valid Karakana metadata and conditional content guides for Markdown-first authoring, with optional audience workbooks; link shared contract/tool. Add original complete synthetic examples and evals for inquiry/research/plan/draft boundaries. Start experimental. | Validate all skills; focused evals; source/license register; no proprietary skill text bundled. | REQ01; REQ04; REQ05; REQ06; REQ07; REQ08; REQ15 |
| P04 | Global discovery and narrow project enablement | P03 | skills/README.md generated index; docs/engineering-process.md pointer; ubongo/global/engineering-standards.md; skillpacks/karakana.yml; lims.yml; ent-meal.yml | Regenerate index through supported CLI; add concise applicability pointers; select optional skills for relevant packs. Avoid mandatory loading on unrelated tasks; do not alter model routing or existing protocol approval rules. | Skill/skillpack/memory validation; representative selection evals; review global/project boundaries. | REQ01; REQ02; REQ13; REQ14; REQ19 |
| P05 | Prove useful output with controlled pilots | P04 | Synthetic fixtures; skills/*/evals/; workbook QA report; docs/engineering-artifacts.md | Author complete synthetic requirements/stories, ADR/design and roadmap/release records in Markdown. Export by audience; validate/render Excel; test source freshness and reviewed feedback reconciliation. A LIMS release pack remains a later requested application. | Source-to-export parity, useful audience views, preserved blockers/limitations, actual office/feedback results and accessibility limits recorded; agree profile baseline. | REQ09; REQ10; REQ12; REQ16; REQ19 |
| P06 | Review and integrate accepted catalogue change | P05 | Final diff, generated index, test/eval/validation reports, task trace and handoff | Use skill-update protocol for metadata/guidance work and python-code-change for deterministic tools; run required suite in isolated runtime; review safety/provenance; publish PR and squash only when authorized. | No P0/P1 unresolved; CI and human review as required; state local/merged/installed separately; promotion remains evidence-based. | REQ01; REQ12; REQ19 |

## 10 Decisions

Purpose: Proposed defaults are concrete and reviewable; no stakeholder approval is recorded.

<!-- workbook-widths: [14, 36, 77, 88, 24, 68] -->

| Decision ID | Question | Recommendation | Alternatives and tradeoff | Review Decision | Reviewer Comments |
| --- | --- | --- | --- | --- | --- |
| D01 | Where is global guidance maintained? | Bundled Karakana skills and shared documentation; task-specific skillpack selection | Installing into personal ~/.codex skills adds another distribution path; defer until needed. | Not reviewed | User requested shared global catalogue; preserve repository lifecycle. |
| D02 | How many skills? | Four focused Markdown authoring workflows plus one audience Excel export/review workflow | One giant skill is hard to route; one skill per artifact repeats shared semantics. | Not reviewed | Evaluate boundaries in P03; extend an existing skill where genuinely equivalent. |
| D03 | What is canonical, and what is shared? | Markdown is primary and version-controlled. Audience Excel workbooks are derived sharing/review views; JSON snapshots are generated intermediates. | Preserve authoritative machine schemas/diagrams with explicit source links. Workbook-first or two freely editable masters would undermine source review/history. | Not reviewed | Archive feedback, reconcile reviewed proposals into Markdown, regenerate a new source-versioned export; no automatic approval transfer. |
| D04 | What does validation prove? | Structural integrity and scoped observed results, separately from substantive review | Do not replace presence gate with a workbook parser pretending to approve meaning. | Not reviewed | Existing protocol artifact evidence remains compatible. |
| D05 | What becomes compulsory? | Profiles tailored to task/risk; common metadata and source traceability | All tabs compulsory creates waste and conflicts with hardened proportional process. | Not reviewed | Requirements for a release differ from a typo correction. |
| D06 | How are releases versioned? | Project-defined scheme; SemVer only for a declared compatible public contract | Calendar/revision versions may fit projects without that public API commitment. | Not reviewed | Do not silently impose software API versioning on product documents. |
| D07 | What first implementation slice? | P01 Markdown content/source/export contract and examples, then P02 export integrity/feedback helpers | Authoring guidance alone cannot prove source freshness, audience projection or preservation of review feedback. | Not reviewed | No real LIMS release drafting or operational changes in this research slice. |
| D08 | What needs further confirmation? | Project review roles, final status vocabulary and target Excel versions during P01/P05 | Do not delay current research for names or environment choices that are not yet execution dependencies. | Not reviewed | Implementation must resolve supported application/feature scope before acceptance. |

## 11 Risks and Limits

Purpose: Research and implementation risks; owners are roles pending assignment, not asserted real owners.

<!-- workbook-widths: [13, 48, 58, 87, 31] -->

| Risk ID | Risk | Consequence | Mitigation or boundary | Follow-up owner role |
| --- | --- | --- | --- | --- |
| RK01 | Workbook edits overwritten by regeneration | Loss of stakeholder review or decisions | Archive exports; stable-ID/version feedback reports; reviewed source changes; refuse overwrite and flag conflicts. | Tool maintainer |
| RK02 | Presence/checklist mistaken for approval | False readiness or unauthorized release | Separate structural, semantic, operational and authorization evidence. | Process owner/reviewer |
| RK03 | Source standards out of date or overstated | Misleading compliance claims | Record edition/status/date; public-summary-only limits; implementation freshness check. | Documentation owner |
| RK04 | Too many required documents | Slow delivery and ignored process | Tailored profiles; reuse current artifacts; compact record for low-risk work. | Process owner |
| RK05 | Binary workbook hard to review | Undetected broad content changes | Review canonical Markdown diffs; generate derived JSON/cell change reports and readable audience samples. | Tool maintainer/reviewer |
| RK06 | Project-specific terminology leaks globally | Wrong requirements, priorities or owners | Generic examples; project-qualified IDs and explicit provenance. | Skill maintainer |
| RK07 | Community license or workflow assumptions copied | Redistribution/permission conflicts | Original wording/tools; no proprietary imports; pinned MIT inspirations attributed if reused. | Skill maintainer |
| RK08 | Formula/cache and office compatibility errors | Wrong counts or silently lost workbook metadata | Round trips; recalculation if formulas; expected-result checks; supported-feature contract. | Tool maintainer/tester |
| RK09 | Synthetic examples mistaken for real evidence | False deployment/UAT statements | Separate example profile/project/revision; explicit Not run, Proposed and unknown fields. | Author/reviewer |
| RK10 | Catalogue inquiry again becomes drafting | Unwanted product artifact changes | EV01/EV02 regression scenarios and explicit requested-action scope. | Skill maintainer |
| RK11 | Release deadline overrides operational blockers | Unsafe real use despite documentation | Maintain evidence-based blockers; presentation/readiness/deployment/acceptance separate. | Release owner |
| RK12 | Excel layout treated as accessibility proof | Unusable workbook for assistive users | Structural practices plus rendered/human review; record unperformed Excel Accessibility Checker. | Document reviewer |
| RK13 | Stale or misleading audience workbook | Divergent facts or omitted release blocker used in decisions | Source revision/hash manifest; flag staleness; explicit omissions/full-source links; retain relevant blockers and limitations in every applicable view. | Document owner/export maintainer |

## 12 Pilot and Rollout

Purpose: Synthetic demonstration first; real project artifacts require a separate requested task.

<!-- workbook-widths: [14, 49, 77, 88, 78] -->

| Pilot ID | Scenario | Expected artifact profile | Acceptance evidence | Rollout boundary |
| --- | --- | --- | --- | --- |
| PL01 | Small feature with a measurable user outcome | Canonical Markdown feature records plus product/engineering/QA sharing views | Stable ID chain from source through story/criterion to a real test result or explicit Not run. | Synthetic; no publishing or real account/data effects. |
| PL02 | Consequential design choice | Canonical Markdown ADR/design with relevant views plus engineering decision summaries | Complete alternatives/rationale/history in Markdown; summaries resolve to the same source revision and schema/diagram links. | Proposed record; no assumption of architectural approval. |
| PL03 | First-release and roadmap planning | Canonical Markdown roadmap/release pack plus executive/product/operations exports | Forecasts, commitments, actual release facts and operations blockers remain distinct and visible in applicable views. | Synthetic example only; LIMS use follows a later user request. |
| PL04 | Human workbook review | Archived annotated export, feedback report and reviewed Markdown diff | Preserve edits by stable source ID/version; report stale/conflicting feedback after office round trip; regenerate from the reviewed source. | No automatic overwrite or imported agreement becoming authorization. |
| PL05 | Global availability | Generated catalogue and selected optional skillpacks | Skills discoverable for appropriate documentation work; unrelated requests unaffected. | Experimental until observed evidence supports promotion. |

## 13 Gate Mapping

Purpose: Existing process reviews canonical Markdown and scoped source evidence; audience workbooks accompany it. File presence alone remains insufficient.

<!-- workbook-widths: [13, 28, 87, 73, 79] -->

| Gate ID | Lifecycle stage | Artifact content to inspect | Existing harness integration | Review boundary |
| --- | --- | --- | --- | --- |
| G01 | Orient / classify | Canonical Markdown identity/revision, requested action and linked machine-source authority; export profile/freshness when shared | Handoff load; protocol classification; skillpack | Research/planning/drafting/execution preserved. |
| G02 | Define / research | Requirement, story, acceptance, Sources and uncertainty records | requirements elicitation/PRD/readiness; assessment/requirements protocol | Observable need, accepted scope and uncertainty judged substantively. |
| G03 | Design / plan | ADRs/views/contracts and bounded task/roadmap/release-plan records | architecture-decision; delivery-artifact-gate; existing task plans | Proposed decision is not accepted; forecasts are not promises. |
| G04 | Pre-implementation | Applicable prerequisites and authorized scope/revision | protocol check --stage pre-implementation | Presence check plus actual content review; outputs still deferred. |
| G05 | Verify / review | Canonical Markdown diff, actual test/review evidence and limitations; source-to-export parity/freshness and feedback report when shared | Focused/full required tests; evals; completion check | Structure or an agent self-review is not independent approval. |
| G06 | Release / operate | Immutable candidate, target, recovery, monitoring, support and authorization | release-change for actual authorized release work | Release plan authorship never deploys; operations evidence remains project-specific. |
| G07 | Handoff / improve | Changed versions, results, residual tasks and exact next action | Append-only handoff; skill/eval updates through reviewed change | Record true state and project boundaries; no hidden implementation. |

## 14 Audience Profiles

Purpose: Proposed sharing profiles for engineering artifacts; this package itself is the full research-review audience export. Implementation will validate audience selection.

<!-- workbook-widths: [14, 28, 65, 65, 65] -->

| Audience ID | Audience | Selected content | Always retain when relevant | Source and review boundary |
| --- | --- | --- | --- | --- |
| AU01 | Business / product | Needs; scope; stories; observable acceptance; outcome roadmap; user-facing release changes | Dependencies; unconfirmed priorities/forecasts; acceptance gaps; delivered versus planned scope | Link full source records and revisions; workbook feedback remains proposed input. |
| AU02 | Engineering | Requirements/acceptance; ADR summaries; design/contract links; implementation tasks; technical release changes | Decision status; unresolved constraints; security/quality risks; test and compatibility gaps | Complete ADR/design narrative and machine schemas stay at their authoritative source paths. |
| AU03 | QA / UAT | Acceptance; test cases/runs; candidate revision/environment; evidence; defects; acceptance decisions | Not run/blocked/skipped/fail; unresolved criteria; reviewer identity and evidence limits | Case definitions and actual results remain separate; feedback is not imported sign-off. |
| AU04 | Operations / release | Candidate/target; readiness; rollout/recovery; migration; monitoring; support/runbook links | Release blockers; backup/restore gaps; known limits; authorization and environment status | No deployment or operational approval follows from export generation. |
| AU05 | Executive / sponsor | Outcomes; milestones; confidence; key scope/release status; risks; decisions needed | Material blockers; uncertainty; forecast versus commitment; deployed/accepted distinctions | Declare omitted detail and link the complete baseline; summaries cannot conceal blockers. |
