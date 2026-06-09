from karakana.safety.model_calls import failed_model_checks, validate_model_call


def test_live_flag_required():
    checks = validate_model_call(False, True, True, "Hello", "model")

    assert any(check.name == "explicit_live_flag_present" for check in failed_model_checks(checks))


def test_secret_assignment_rejected():
    checks = validate_model_call(True, True, True, "client_secret=abc", "model")

    assert any(check.name == "prompt_redacted" for check in failed_model_checks(checks))


def test_safety_text_about_secrets_allowed():
    checks = validate_model_call(True, True, True, "Do not touch secrets.", "model")

    assert not failed_model_checks(checks)
