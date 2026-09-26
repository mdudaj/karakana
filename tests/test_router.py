from karakana.router import select_model


def test_select_model_for_planning():
    assert select_model("planning") == "gpt-6-sol"


def test_select_model_for_deep_planning():
    assert select_model("implementation_planning") == "gpt-6-sol"


def test_select_model_for_code_implementation():
    assert select_model("code_implementation") == "gpt-6-luna"


def test_select_model_defaults_to_gpt_5_mini():
    assert select_model("unknown") == "mock-model"
