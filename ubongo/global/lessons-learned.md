# Lessons Learned

Preserve durable lessons from completed work, incidents, reviews, and evaluations. Prefer short, reviewable entries with dates and project context.

## 2026-07-07: Make Learned Constraints Executable

Context: TACATDP Power Apps Canvas source packaging repeatedly failed Studio import because fixes were based on plausible control-property assumptions rather than exact Source Code schema/import evidence for the active control versions.

Durable rule:

- Treat vendor docs, source schemas, runtime/import errors, and exported artifacts as the authority for implementation details.
- When a failure happens, update the relevant validator/eval/skill/doc before declaring the next package ready.
- A lesson is not durable until the next agent has explicit implementation instructions and a regression guard.

Applied pattern:

- Global behavior belongs in `ubongo/global/engineering-standards.md` and `KARAKANA.md`.
- Project-specific constraints belong in `ubongo/projects/<project>/`.
- Workflow guidance belongs in a skill.
- Repeated failure signatures belong in tests, evals, or validators.

## 2026-07-12: UX Work Must Define Behavior and Data Scope First

Context: TACATDP Monitoring Tool UX revisions initially focused on screens and controls before the expected data visibility and edit semantics were fully explicit. This caused repeated revisions around whether saved records were current-user-only or shared, whether a draft was real/restorable, and whether an Open action should create, view, or edit.

Durable rule:

- Before UX-impacting implementation, define behavior and data scope first: who can see which records, what source/limit/pagination is loaded, what fields are searchable, what each action mutates, and what empty/loading/error states mean.
- Do not infer data scope from the current screen, seed data, or a previous prototype. Document the scope in requirements/design artifacts before coding.
- Add validator or test guards for scope-sensitive behavior, especially filters, action labels, and create/edit flows.

## 2026-08-06: Prefer Observed Console Context Over Guessed Cloud Resource URLs

Context: TACATDP/Mshirika PAC verification initially treated a PAC device-code failure against a Dataverse org URL as evidence that the tenant account lacked access. A Maker Portal screenshot showed the same work/school tenant account already signed in to the target `PowerPagesDeveloper-*` environment, which is stronger evidence about the intended environment and principal.

Durable rule:

- When a cloud admin console is open and shows the target environment, extract exact tenant/account/environment identifiers from that console before diagnosing permission failure.
- For Power Platform/PAC, prefer the Maker Portal environment id from `make.powerapps.com/environments/<environment-id>/...` when PAC auth/list against a Dataverse org URL fails.
- Do not tell the user they lack access until the exact observed tenant account, environment id, and expected PAC command shape have been tried or proven unavailable.
- If a repository has a relevant admin/PAC skill, load it before giving access conclusions, not after the first failed command.
