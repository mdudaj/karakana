from karakana.safety.patch import detect_patch_blocking_signals, detect_patch_high_risk_signals, validate_patch_apply


def test_patch_safety_blocks_env_and_secret():
    diff = "diff --git a/.env b/.env\n+++ b/.env\n@@\n+client_secret=abc\n"

    signals = detect_patch_blocking_signals(diff, [".env"])

    assert "env_exposure" in signals
    assert "secret" in signals


def test_patch_safety_detects_high_risk():
    diff = "diff --git a/billing/payment.py b/billing/payment.py\n+++ b/billing/payment.py\n@@\n+payment = True\n"

    assert "payment_or_billing" in detect_patch_high_risk_signals(diff, ["billing/payment.py"])


def test_dry_run_apply_does_not_require_high_risk_override():
    assert validate_patch_apply(False, "high", "feature", write=False) == []
