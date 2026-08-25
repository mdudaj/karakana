# User Preferences

Capture durable user preferences for workflow, communication, tooling, project priorities, and review style. Do not store secrets or transient notes here.

## Delivery Workflow

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
