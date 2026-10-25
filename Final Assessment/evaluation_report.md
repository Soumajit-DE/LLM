# Evaluation Report - Five Test Cases

Source: `Task4.ipynb`, Section 6 (`report_df`). The `Evaluator` (LLM-as-judge) scores each
agent's output against four rubric criteria (`coherence`, `completeness`, `budget_adherence`,
`feasibility`, each 0-10); `overall_score >= 7.0` passes, otherwise the agent is retried once,
and if still failing the output is escalated for human review instead of being passed
downstream silently.

| Test Case | Agent | Scenario | Attempts | Score per attempt | Coherence | Completeness | Budget Adherence | Feasibility | Final Score | Result | Explanation |
|---|---|---|---|---|---|---|---|---|---|---|---|
| TC1 | `venue_recommendation_agent` | Good output (capacity, budget, accessibility all satisfied) | 1 | 9.2 | 9.0 | 9.5 | 9.5 | 9.0 | 9.2 | **PASS** | Well within budget, capacity, and accessibility requirements - ready to pass downstream. |
| TC2 | `catering_logistics_agent` | Missing dietary coverage + cost mismatch | 2 | 4.3 → 8.9 | 9.0 | 9.0 | 9.0 | 8.5 | 8.9 | **PASS (on retry)** | Dietary coverage and cost math are now consistent and within budget - ready to pass downstream. |
| TC3 | `av_vendor_coordination_agent` | Missing livestream vendor + silent budget overrun | 2 | 3.1 → 3.9 | 5.5 | 4.0 | 2.0 | 5.0 | 3.9 | **FAIL → ESCALATED** | Retry did not fix either root cause (missing livestream vendor, undisclosed budget overrun) - requires human review. |
| TC4 | `agenda_assembly_agent` | Overlapping schedule + invented venue | 2 | 4.8 → 8.9 | 9.0 | 9.0 | 8.0 | 9.0 | 8.9 | **PASS (on retry)** | Schedule is now internally consistent, non-overlapping, and uses the correct venue - ready to pass downstream. |
| TC5 | `venue_recommendation_agent` | Venue capacity below requested headcount | 2 | 4.6 → 8.8 | 9.0 | 8.5 | 8.5 | 9.0 | 8.8 | **PASS (on retry)** | Capacity constraint is now satisfied and the venue remains within budget - ready to pass downstream. |

## Summary

- **Pass: 4/5** (TC1, TC2, TC4, TC5) · **Escalated to human review: 1/5** (TC3) · **Retried: 4/5**
  (all but TC1).
- Every one of the four rubric criteria independently catches a different failure mode across
  the five cases: `completeness` (TC2's missing dietary tags), `budget_adherence` (TC3's silent
  2x budget overrun), `coherence` (TC4's overlapping/invented-venue schedule), and `feasibility`
  (TC5's venue capacity below headcount).
- TC3 demonstrates the escalation path end-to-end: the retry addressed neither root cause
  (still no livestream vendor, still an undisclosed budget overrun), so the pipeline flags it for
  human review rather than silently forwarding a low-quality AV plan downstream.
