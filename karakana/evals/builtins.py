"""Built-in eval case metadata."""

from __future__ import annotations

BUILTIN_EVAL_PATHS = [
    "evals/safety/no-secret-leak.yml",
    "evals/safety/no-production-deploy.yml",
    "evals/safety/no-direct-main-push.yml",
    "evals/github/comment-opt-in.yml",
    "evals/github/pr-creation-safety.yml",
    "skills/invenio-framework/evals/custom-field-loader.yml",
    "skills/invenio-framework/evals/oauth-invalid-client.yml",
    "skills/gepg-billing/evals/payment-callback-idempotency.yml",
    "skills/karakana-self-improvement/evals/proposal-requires-review.yml",
]
