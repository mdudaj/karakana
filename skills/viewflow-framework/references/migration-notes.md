# Viewflow Migration Notes

Changing existing workflows can affect active processes.

## Risks

- Active processes may already exist.
- State names may change.
- Task ownership may break.
- URLs or templates may change.
- Permissions may regress.
- Business data migrations may be needed.
- Process data migrations may be needed.
- Dashboards may show stale or unreachable tasks.

## Review Guidance

- Identify whether active processes exist before changing flow state.
- Avoid renaming states or tasks without migration planning.
- Check whether old processes can still complete.
- Add compatibility tests for active or historical process states when possible.
- Document manual recovery only when explicitly approved.
