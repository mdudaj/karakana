# Scientific Decision Ranking

## Research Boundary

Karakana separates three quantities that must not be conflated:

1. **Verbalized probability**: model-produced metadata used to expose diverse candidate modes.
2. **Evidence relevance score**: an information-retrieval ranking signal.
3. **Decision weight**: a normalized share of an explicit multi-criteria score.

Only the first is formatted like a probability, and it is not considered calibrated without repeated outcomes and post-hoc evaluation.

## Evidence Base

[Zhang et al., Verbalized Sampling](https://arxiv.org/html/2510.01171v2) shows that distribution-level prompting improves response diversity across its evaluated tasks. Its simple reference-distribution result is explicitly described as proof-of-concept, and its limitations include inference cost and dependence on model capability. The paper does not validate software milestone probabilities.

[Wang et al., Calibrating Verbalized Probabilities for Large Language Models](https://arxiv.org/abs/2410.06707) reports overconfidence and calibration complications for verbalized probabilities on discriminative tasks. Calibration requires held-out observations; Karakana has no outcome dataset that would support such a claim.

[Robertson-style BM25](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/ppm.pdf) provides a transparent term-frequency, document-length, and inverse-document-frequency ranking basis. Karakana combines a BM25-style saturation score with query-term coverage. This ranks evidence; it does not estimate probability of relevance.

[Więckowski and Sałabun's MCDA sensitivity review](https://doi.org/10.1016/j.asoc.2023.110915) identifies sensitivity analysis as fundamental to assessing ranking robustness. Karakana therefore reports leave-one-criterion-out and single-weight perturbation scenarios.

## Deterministic Method

### Evidence Relevance

For a user note and a project-scoped evidence corpus:

1. Normalize tokens and remove a fixed stopword list.
2. Calculate BM25-style term contributions with `k1=1.2` and `b=0.75`.
3. Combine BM25 saturation (70%) with unique query-term coverage (30%).
4. For ingestion candidates, apply a field-focus gate: title relevance must be at least medium or full-content relevance must be high. This prevents incidental pipeline context in long documents from becoming an actionable finding.
5. Record the numeric score, matched terms, and threshold label.

Thresholds are explicit engineering policy: `high >= 0.55`, `medium >= 0.35`, `low >= 0.18`, otherwise `irrelevant`. They require future tuning against labeled Karakana evidence judgments.

### Candidate Selection

Candidates use a 0-5 ordinal scale and these criterion weights:

| Criterion | Weight |
|---|---:|
| Blocker priority | 0.25 |
| User alignment | 0.20 |
| Evidence strength | 0.15 |
| Readiness | 0.15 |
| Risk control | 0.10 |
| Reversibility | 0.10 |
| Cost efficiency | 0.05 |

The aggregate is a simple weighted sum. The displayed decision weight is the candidate score divided by the sum of candidate scores. It supports comparison but has no probabilistic interpretation.

### Robustness

Karakana tests 21 scenarios for seven criteria:

- remove each criterion once;
- reduce each criterion weight by 20%;
- increase each criterion weight by 20%;
- renormalize remaining weights in every scenario.

The artifact reports the baseline margin, winner counts, alternate winners, and critical criteria. A winner is called robust only if it remains first in every tested scenario.

## Remaining Scientific Limits

- Criterion weights and 0-5 scores encode policy judgments; transparency and sensitivity do not make them objective.
- BM25 thresholds are not yet validated against a labeled relevance set.
- Decision quality is not yet backtested against milestone outcomes.
- Verbalized probabilities should not be calibrated until Karakana has a sufficient repeated-outcome dataset and a pre-registered evaluation protocol.
