"""Shared engineering guidance and artifact stage selection; no execution."""

CHECK_STAGES = {"pre-implementation", "completion"}
DELIVERY_OUTPUTS = {
    "change_summary", "verification_summary", "screenshot_or_render_evidence", "handoff",
}


def artifacts_for_stage(required: list[str], stage: str) -> tuple[list[str], list[str]]:
    if stage not in CHECK_STAGES:
        raise ValueError(f"Unknown protocol check stage: {stage}")
    unique = list(dict.fromkeys(required))
    deferred = [kind for kind in unique if stage == "pre-implementation" and kind in DELIVERY_OUTPUTS]
    return [kind for kind in unique if kind not in deferred], deferred


def render_engineering_process() -> str:
    """Keep primary agent entrypoints aligned without duplicating skill bodies."""
    return """## Engineering Process

Follow the tailored lifecycle in docs/engineering-process.md when available.
- Orient: verify project, branch, handoff, request type, scope, risk and authority.
  Analysis/review requests do not authorize implementation or external writes.
- Define: state outcome, non-goals and observable acceptance criteria; link current requirements.
- Research/design: reuse verified current evidence; research only unresolved questions.
  Close research with chosen requirements and observable acceptance, design/method
  rationale, and governing artifact updates or reuse. Record consequential trade-offs,
  UX/accessibility, security, data and operational effects. Mark ready only when
  choices, artifacts and authority are settled; otherwise name the owner, exact
  decision/evidence gap and next action. Do not leave vague proposed choices.
- Plan: name files, bounded steps, regression checks, approvals and applicable rollback.
  Before non-trivial implementation run protocol check --trace <id> --stage pre-implementation.
- Implement: small reviewable task-branch changes; reproduce bugs and add regression tests
  where feasible. Extend established abstractions. Replan when scope or evidence changes.
- Verify/validate: focused tests then the required broader gate; check actual user outcomes.
  Record commands, results, revision/environment, skipped checks and residual risk.
- Review: inspect the diff and acceptance evidence; resolve P0/P1 findings.
  Self-review is not independent review; required checks must pass before claiming completion.
- Release only when authorized: verify target, release, recovery and post-deploy behavior.
  Implemented, verified, merged, deployed and accepted are distinct states.
- Handoff: record remaining work, next exact action/model/conversation; protect repeated
  failures with tests/evals. Attach the handoff then run protocol check --trace <id> --stage completion.
  After two failed diagnostic attempts, stop speculation and replan.
For subsequent implementation, use one active milestone, one branch and one coherent PR.
Size work for roughly half to one day of implementation, then verification/review.
Finish the squash merge and release checks before starting the next milestone.
Record implemented, verified, merged, deployed and accepted separately, with evidence.
Collect clarifications in the shared workbook while configurable implementation continues.
Unresolved decisions hold only affected behavior or activation; use reversible defaults
within existing authority. Workbook comments do not authorize external actions.
Keep project boundaries intact; a cross-repository request completes each milestone
sequentially. These are delivery instructions, not an automatic merge/deploy controller.
Tailor to risk: small mechanical work needs a concise record, not a new PRD/ADR.
One artifact may cover several concerns only when its content genuinely covers them.
Artifact checks establish file presence; research closeouts also check required
structure and local references. Neither proves correctness, passing tests or approval.
Do not report unrun checks as passed, or treat a pre-implementation pass as completion.
"""
