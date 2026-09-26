# Adaptive UX verification catalogue update

## Scope and requirements
Update existing governance and browser-QA skills from observed responsive review
failures. Agents need to distinguish clipping from a genuinely fitting layout,
check identity-text readability, diagnose computed icon styles, and select correct
disclosure semantics. Do not introduce a new design system, global palette,
LIMS-specific card counts, permissions, or live model execution.

## Architecture and implementation
`design-system-governance` 0.1.1 routes adaptive work to a focused component
contract reference. `design-qa-playwright` 0.1.1 extends its existing QA reference
with control/ancestor checks, glyph geometry, text-width checks and keyboard
recovery. The skills protocol index links this task-oriented combination.
No skillpack changes are required: both skills are already listed for LIMS and
Karakana. No standalone duplicate skill is added.

Inspect those two SKILL.md files, their references, the project UI contract and
current browser harness before implementation. Use the W3C sources in the
reference for behavioral requirements; retain project/framework visual identity.

## Acceptance and verification
- All skill manifests validate.
- Focused deterministic evals pass: governance 1/1, browser QA 2/2.
- Two new reference-contract evals protect discovery of the diagnosis and
  verification checks. These are text-contract checks, not simulations of agent
  judgment or independent accessibility certification.
- Full catalogue eval: 144/145 passed. Existing `material-record-list` fails
  because its forbidden `color alone` pattern matches the safety instruction
  `Do not rely on color alone`. Unrelated to these changes; not silently waived.
- No live model call, credential change, source-code generation automation or
  production deployment is part of this slice.

## Evidence, readiness and follow-up
Research and browser implementation evidence remain in the LIMS project:
`docs/planning/ADAPTIVE_SHELL_TASKS.md`, its new regression tests and ignored
`.scratch/browser-runs/adaptive-tasks*.png` captures. This catalogue change has no
rendered UI of its own; LIMS is the concrete exercise, not a cross-project rule.
Accessibility expectations explicitly distinguish browser evidence from full
conformance. No migration or ADR is needed for these additive references.

Delivery is a reviewable task-branch change. Rollback is reverting the skill
reference/version additions. Next: review the catalogue diff and correct the
separate material-record-list eval false positive in its own bounded task.
