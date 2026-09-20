# HCD UI/UX Review Threshold

Use this scorecard after rendered review for non-trivial UI/UX work.

## Severity gates

| Severity | Meaning | Delivery rule |
|---|---|---|
| P0 | User cannot complete the core task, data/audit meaning is misleading, or a critical accessibility/permission/workflow risk exists. | Must fix before delivery. |
| P1 | Primary hierarchy, action scope, control behavior, accessibility, or system consistency is materially confusing or error-prone. | Must fix before delivery unless explicitly deferred by the user. |
| P2 | Important polish, density, copy, responsive, or secondary-state issue that slows work but does not block the core task. | May deliver with follow-up if recorded. |
| P3 | Minor visual refinement or optional enhancement. | Record only if useful. |

## Scorecard

Score each area from 0 to 3.

| Area | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| User job fit | Core job is unclear. | Job is implied but not prioritized. | Main job is clear. | Main job and next action are immediately clear. |
| Information hierarchy | Everything competes. | Some hierarchy exists but controls/details dominate. | Primary content is distinguishable. | Attention, work, context, and details appear in task order. |
| Simplicity and cognitive load | Excessive content/actions. | Some non-essential content competes. | Mostly focused. | Minimal, progressive, and easy to scan. |
| Material semantics | Components used incorrectly or inconsistently. | Components mostly visual. | Components match common roles. | Components are semantically correct and consistent. |
| Design-system alignment | Page-local styling dominates. | Some reusable styles used. | Mostly reusable tokens/components. | Fully aligned with shared tokens/components/patterns. |
| Accessibility | Critical label/focus/contrast/keyboard issues. | Multiple likely WCAG issues. | No obvious blocker; minor risk remains. | Labels, focus, contrast, targets, states, and semantics are sound. |
| Interaction states | Non-happy states missing. | Only empty or error state exists. | Key states covered. | Loading, empty, filtered-empty, error, disabled, stale, success, and permission states are covered or explicitly not applicable. |
| UX writing | Jargon, implementation copy, or unclear actions. | Mixed wording and unclear helper text. | Clear enough. | Concise, task-oriented, domain-appropriate, and consistent. |
| Data scanability | Dense data is hard to compare. | Rows/cards lack anchors or labels. | Scannable with some friction. | Strong anchors, columns/labels, status, filters, and actions. |
| Verification evidence | No rendered evidence. | Code/tests only for visual behavior. | Browser/manual evidence exists. | Browser evidence, tests, and accessibility checks cover the critical path. |

## Pass threshold

A UI/UX delivery may be reported as complete only when:

- there are no unresolved P0 findings;
- there are no unresolved P1 findings unless the user explicitly defers them;
- Accessibility scores at least 2;
- Design-system alignment scores at least 2;
- User job fit scores at least 2;
- total score is at least 24 out of 30.

If any gate fails, perform a refinement pass before final delivery. If a
refinement pass cannot be completed, report the failing gates, the blocker, and
the exact next action.

## Review output

Use this compact output during post-delivery critique:

```markdown
Score: NN/30
Gate: pass/fail

P0:
P1:
P2:
P3:

Refinements applied:
Remaining follow-ups:
```
