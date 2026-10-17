# User Preferences

Capture durable user preferences for workflow, communication, tooling, project priorities, and review style. Do not store secrets or transient notes here.

## Delivery Workflow

- When work requires review, include a self-contained review brief in both the
  user-facing completion and handoff: proposed changes/defaults, rationale,
  meaningful alternatives, verification/limitations, exact decision and next
  action. Routine decision review should not require opening linked files;
  retain links for optional detail. Technical review still requires inspecting
  relevant code and evidence. Keep the brief concise and proportional to scope.
- Across Karakana and every managed project, bring a preferred evidence-backed
  proposal before asking the user or a third party for a decision or waiting for
  input. Explain why it fits current project conventions, assumptions and effects;
  offer meaningful alternatives with trade-offs when available. If only one path
  is feasible, explain why. Missing site facts require a conditional proposal and
  bounded verification, not invented facts or unsupported claims of best practice.
- Present material choices for agreement, then record the agreed decision in the
  governing artifacts. Incorporate user revisions, preserve decision history and
  recheck affected implementation, verification and authority. Identify what can
  proceed now, what is held, the owner and exact confirmation needed. Continue
  independent authorized work; reuse existing agreements and routine delegated
  authority without adding approval loops. Silence is not agreement, and a
  proposed setting does not authorize live activation or external actions.
- Subsequent implementation follows the global mergeable milestone policy in
  `ubongo/global/engineering-standards.md`: one active milestone, one branch and
  one coherent PR; roughly half to one day of implementation followed by
  verification/review; finish squash merge and release checks before the next.
  Record implemented, verified, merged, deployed and accepted separately.
  Collect clarifications in the shared workbook while configurable implementation
  continues; do not hold unrelated work for those answers.
- Once the user agrees to a plan or slice, deliver the reviewable slice end to
  end without asking for additional permission in the middle of the same slice,
  unless a hard safety boundary appears: secrets, destructive actions,
  production deployment, protected-branch writes, external writes/messages, or
  a material scope change beyond the agreed plan.
- For LIMS work, Docker-backed local preview operations are part of agreed
  delivery verification once the user approves a slice. Treat Docker-backed
  `./scripts/local_preview.sh` check, migrate, test, and browser-test commands
  as in-scope technical verification, not as a separate product permission
  question. If the sandbox blocks Docker socket access, request the technical
  escalation directly and continue.
