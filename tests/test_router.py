from karakana.router import select_model


def test_select_model_for_planning():
    assert select_model("planning") == "gpt-5-mini"


def test_select_model_for_code_implementation():
    assert select_model("code_implementation") == "codex-gpt-5.5"


def test_select_model_defaults_to_gpt_5_mini():
    assert select_model("unknown") == "gpt-5-mini"
