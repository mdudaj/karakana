# Ubuntu continuation: engineering documentation

Project: Karakana. Date: 13 November 2026.

## Current task

Deliver engineering documentation skills supported by purposeful content templates, examples and checks. The motivation is concise technical documentation rather than authoring history or repeated review arrangements. Keep genuine product approval requirements, audit behaviour and operating authority.

Research and the implementation proposal are complete in [DRAFTING-CONVENTIONS-2026-11-13.md](DRAFTING-CONVENTIONS-2026-11-13.md). Reuse that evidence; do not restart broad research. The owner requested committing/syncing the research, a loadable handoff, updating `main`, then switching to the next task branch to continue. Integration is through draft PR [#33](https://github.com/mdudaj/karakana/pull/33), to be squash-merged after documentation checks. Verify its actual merged state and local source before proceeding; this note is not a merge receipt.

No skills, application code, client documents or server settings have changed in this slice. No server connection is required. Runtime traces and handoffs under `.karakana/` are ignored; they do not transfer through Git. This tracked note provides the portable continuation context.

## Next bounded slice

Branch: `feat/documentation-conventions-templates-20261113`.

Start the convention/templates slice using the proposal and existing lifecycle. Resolve the concrete profile and file layout in a compact task brief, then implement the shared convention and initial requirements/design templates, examples and relevant eval coverage. Present any new material decision before dependent changes; do not reopen settled research or seek permission again for routine in-scope work. Run the slice's own pre-implementation gate before editing skills or code.

Acceptance: one clear document-to-template mapping; instructions and examples distinguish product requirements from authoring activity; authoring help stays out of issued documents; templates name required and optional sections; internal authority records remain intact; no universal template forces irrelevant sections. Keep legacy exports and native JSON authority. Validate skills and run relevant deterministic evals/tests, then the required broader gate. Use one reviewable branch/PR.

Later slices address CRLF parsing, artifact-output checks, selection/protocol enforcement, remaining templates, exports and pilot validation. After those changes are verified and integrated, perform the new Jovina bundle review and produce its bounded update plan before revisions. Do not edit that bundle during this first harness slice.

## Inspect first

1. `AGENTS.md`, `KARAKANA.md`, `docs/engineering-process.md`, `docs/cost-aware-continuation.md`.
2. `ubongo/projects/karakana/overview.md`, `ubongo/projects/karakana/open-issues.md`; verify the existing KDX-09 state independently. This handoff does not mark it complete.
3. The linked research proposal, `docs/engineering-artifacts.md`, `docs/skills/engineering-artifact-catalogue/TEMPLATE.md`.
4. `skills/karakana-self-improvement/SKILL.md`, `skills/delivery-artifact-gate/SKILL.md`, the five existing `engineering-*` skills and `skillpacks/karakana.yml`.
5. Inspect parser, planner, resolver and protocol source only as needed for the bounded slice; file targets are in the proposal.

Existing five skills are optional/experimental. The current default selects `delivery-artifact-gate`; merely listing an optional skill does not load it. Checks largely establish structure/presence. Synthetic probes accepted off-purpose meeting prose as a requirement and showed CRLF input silently parsed as zero requirement records. These findings are not fixed yet. Details and authoritative research links are in the proposal.

Verification completed on Windows: direct probes in temporary repositories, research-closeout structure/local-reference checks, document whitespace and 14 local source references. Pytest was unavailable; no regression pass is claimed. Recheck tooling on Ubuntu rather than assume it exists. No live model calls are authorised by validation commands. Recommended model: GPT-6 Sol medium for the convention/design slice; high for later consequential protocol gates. Verify actual model availability; no automatic switch is implied.

## Update the Ubuntu checkout

From the Karakana repository root, with local work saved and a clean working tree:

```bash
git fetch origin
git switch main
git pull --ff-only origin main
git switch feat/documentation-conventions-templates-20261113
```

The continuation branch is to be published from updated `main`. If it is not present after fetching, stop and inspect the remote branches and PR #33 state; do not reset or discard local work. Do not continue from the old research branch after a squash merge.

Read this note and the proposal, then load current context using the block below. It checks CLI availability, appends a local runtime handoff, and loads it. It does not install packages, edit source, call a model or connect to the app server. Historical Windows trace IDs are evidence references, not portable local validation results.

```bash
(
set -euo pipefail
note=docs/skills/engineering-artifact-catalogue/UBUNTU-HANDOFF-2026-11-13.md
research=docs/skills/engineering-artifact-catalogue/DRAFTING-CONVENTIONS-2026-11-13.md
test -f KARAKANA.md
test -f "$note"
test -f "$research"
if command -v karakana >/dev/null 2>&1; then
    cli=(karakana)
elif [ -x .venv/bin/karakana ]; then
    cli=(.venv/bin/karakana)
else
    echo 'STOP: Karakana CLI unavailable; inspect docs/installation.md before setup.' >&2
    exit 1
fi
"${cli[@]}" handoff refresh \
    --project karakana --skillpack karakana \
    --purpose 'Resume documentation convention/templates work on Ubuntu' \
    --current-milestone 'First convention/templates slice; research reusable' \
    --from-note "$(cat "$note")" \
    --next-task 'Deliver the first bounded documentation convention and initial templates slice' \
    --next-task-brief 'Read the portable handoff and proposal; inspect existing skills; define the concrete first slice and its acceptance; run its pre-implementation gate; implement and verify only that slice.' \
    --reuse-stage "research=$research" --reuse-reviewed \
    --no-recover-artifacts
"${cli[@]}" handoff load --project karakana --skillpack karakana
)
```

An older local protocol check displayed during refresh does not validate this new task. Start and bind the next slice's own protocol trace. Preserve all prior runtime history. End the slice with a trace-bound append-only handoff and distinguish implemented, verified, merged, deployed and accepted states.
