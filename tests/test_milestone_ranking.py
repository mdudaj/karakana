from karakana.milestones.ranking import bm25_relevance, focused_candidate_relevance, rank_candidates


def test_bm25_relevance_distinguishes_specific_intake_evidence():
    query = "Provide TIE links and run curriculum source retrieval actions from an intake management page"
    corpus = [
        "Add TIE curriculum source links and retrieval actions to curriculum intake management",
        "Configure WhatsApp evaluator reminder delivery",
        "Automated curriculum review from uploaded file",
    ]

    specific = bm25_relevance(query, corpus[0], corpus)
    unrelated = bm25_relevance(query, corpus[1], corpus)
    broad = bm25_relevance(query, corpus[2], corpus)

    assert specific.score > broad.score > unrelated.score
    assert specific.label in {"medium", "high"}
    assert unrelated.label == "irrelevant"


def test_mcda_sensitivity_detects_robust_winner():
    names = [
        "blocker_priority", "user_alignment", "evidence_strength", "readiness",
        "risk_control", "reversibility", "cost_efficiency",
    ]
    candidates = [
        {
            "title": "Evidence-led slice", "category": "implementation", "rationale": "Best fit",
            "risks": "Bounded", "cost": "Medium", "reversibility": "High",
            "criterion_scores": dict.fromkeys(names, 5),
        },
        {
            "title": "Documentation only", "category": "documentation", "rationale": "Cheap",
            "risks": "Low", "cost": "Low", "reversibility": "High",
            "criterion_scores": dict.fromkeys(names, 2),
        },
    ]

    ranked, sensitivity = rank_candidates(candidates)

    assert ranked[0].title == "Evidence-led slice"
    assert sensitivity.robust is True
    assert sensitivity.alternate_winners == []
    assert sensitivity.scenarios_tested == 21


def test_focus_gate_rejects_incidental_pipeline_context():
    query = "Add TIE source links and retrieval actions to curriculum intake management"
    titles = ["Automated curriculum review", "Curriculum intake management actions"]
    contents = [
        "Automated topic review happens after source snapshot and deterministic curriculum intake.",
        "Let staff add TIE source links and run retrieval actions from curriculum intake management.",
    ]
    corpus = [f"{title} {content}" for title, content in zip(titles, contents)]

    incidental = focused_candidate_relevance(
        bm25_relevance(query, titles[0], titles),
        bm25_relevance(query, corpus[0], corpus),
    )
    focused = focused_candidate_relevance(
        bm25_relevance(query, titles[1], titles),
        bm25_relevance(query, corpus[1], corpus),
    )

    assert incidental is False
    assert focused is True
