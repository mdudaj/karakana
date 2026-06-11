from karakana.ingestion.classifier import classify_content


def test_classifies_memory_skill_eval_prompt_safety_behavior():
    assert classify_content("architecture decision and project convention", project="demo").category == "ubongo_memory"
    assert classify_content("repeated workflow checklist verification step", project="demo").category == "skill_update"
    assert classify_content("regression repeated failure missing test", project="demo").category == "eval_update"
    assert classify_content("missing section weak prompt wrong model route", project="demo").category == "prompt_update"
    assert classify_content("secret exposure destructive command bypass review", project="demo").category == "safety_update"
    assert classify_content("preferred style copy-ready markdown", project="demo").category == "behavior_update"
