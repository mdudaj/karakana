# Engineering documentation conventions and templates

Research and implementation proposal, 13 November 2026. Research trace: `20261113-110352-78004f`. This records research and a proposed direction; it does not activate new skills, change client documents, or authorise implementation.

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
