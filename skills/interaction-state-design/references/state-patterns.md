# Interaction State Patterns

Use this reference when planning or auditing non-happy UI states.

## State taxonomy

| State | Meaning | Typical pattern | Recovery |
| --- | --- | --- | --- |
| Initial | User has not started interaction | Neutral form/list/dashboard | Start primary action |
| Loading | Data/action is in progress | Skeleton, spinner, progress bar | Wait, cancel if safe |
| Partial loading | One section/control is loading | Local progress/skeleton | Keep rest usable |
| Empty | No records exist in context | Contextual empty state | Start/create/import if allowed |
| Filtered-empty | Records may exist but filters hide them | Empty state plus active chips | Clear filters |
| No results | Search query matched nothing | Search no-results state | Edit/clear search |
| Validation error | Submitted input failed checks | Field errors + optional summary | Correct and resubmit |
| System error | Operation failed unexpectedly | Error panel/message | Retry, report, support |
| Permission denied | User cannot access/action | Permission state | Request access or switch role/context |
| Disabled | Action unavailable now | Disabled control with reason | Satisfy prerequisite |
| Readonly | Data visible but not editable | Readonly field/surface | Explain owner/source |
| Blocked | Workflow cannot proceed | Blocking banner/row state | Open prerequisite |
| Stale | Data may no longer be current | Timestamp + refresh warning | Refresh/reload |
| Offline | Network unavailable | Persistent indicator/local error | Continue offline-safe work |
| Conflict | Data changed during edit | Conflict message/diff | Reload, merge, retry |
| Success | Operation completed | Inline confirmation/snackbar | Continue next task |
| Queued | Operation accepted, not done | Queued status/progress | Track status |

## Scope rules

Place state feedback at the smallest accurate scope.

| Scope | Examples | Placement |
| --- | --- | --- |
| Control | field validation, autocomplete loading | field/helper/error area |
| Row | row action saving, row blocked | row trailing/status cell |
| Section | table loading, chart unavailable | section body/header |
| Page | permission denied, page data failed | below page header |
| Shell/global | offline, session, global integration issue | shell/banner/notification |

Avoid page-level blocking when only a small part of the interface is affected.

## Copy formula

Use this order:

```text
What happened.
Why it matters.
What the user can do next.
```

Examples:

- `No tasks match these filters. Clear filters or change your search.`
- `Storage movement is blocked because this box has no active positions. Open
  storage setup to finish configuration.`
- `This record changed since you opened it. Refresh before submitting to avoid
  overwriting newer work.`

Avoid blame. Avoid implementation details. Avoid unsupported actions.

## Material-compatible pattern mapping

- **Progress indicator**: ongoing loading, saving, import, upload, background
  job. Use determinate progress when the system knows progress.
- **Skeleton**: initial content loading when layout is predictable.
- **Banner/alert panel**: persistent page or section issue requiring attention.
- **Inline field error**: validation or control-specific failure.
- **Snackbar/toast**: transient confirmation or low-risk undo, not persistent
  blocking error.
- **Chips**: active filters, removable selections, compact status controls.
- **Dialog**: decision that must interrupt the task, especially destructive or
  confirmation-sensitive operations.
- **Empty state**: absence of content; not the same as system failure.

## Operational system rules

For laboratory, healthcare, research, finance, or regulated operations:

- never hide critical safety/quality states;
- distinguish queued from completed;
- distinguish recorded-at from occurred-at when state timing matters;
- show actor/context when wrong-object action is plausible;
- preserve entered values after validation failures;
- make manual fallback visible when automation fails;
- log/audit recovery actions where required by the domain.

## Verification checklist

- At least one test or browser check covers non-happy state behavior.
- Filtered-empty and no-results are separate when both can occur.
- Loading does not erase context needed for safe decisions.
- Permission-denied copy avoids restricted details.
- Disabled action has a discoverable reason when the user expects access.
- Success copy accurately matches completed vs queued work.
- Status/error changes are accessible.
