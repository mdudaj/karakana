from karakana.codex.reviewer import review_patch_text


def test_patch_review_safe_docs_diff_passes():
    diff = "diff --git a/README.md b/README.md\n+++ b/README.md\n@@\n+hello\n"

    review = review_patch_text(diff, "patch")

    assert review.status == "passed"
    assert review.risk_level == "low"


def test_patch_review_blocks_env_secret():
    diff = "diff --git a/.env b/.env\n+++ b/.env\n@@\n+client_secret=abc\n"

    review = review_patch_text(diff, "patch")

    assert review.blocked
    assert review.risk_level == "critical"


def test_patch_review_flags_payment_and_missing_tests():
    diff = "diff --git a/billing/payment.py b/billing/payment.py\n+++ b/billing/payment.py\n@@\n+def callback(): pass\n"

    review = review_patch_text(diff, "patch")

    assert review.risk_level == "high"
    assert any(f.finding_type == "payment_or_billing" for f in review.findings)
    assert any(f.finding_type == "missing_tests" for f in review.findings)


def test_patch_review_flags_viewflow_state():
    diff = "diff --git a/workflows/flow.py b/workflows/flow.py\n+++ b/workflows/flow.py\n@@\n+# Viewflow process state transition\n"

    review = review_patch_text(diff, "patch")

    assert any(f.finding_type == "viewflow_process_state" for f in review.findings)
