# Generative AI experiment

**Question:** How consistently do two prompts explain credit-scoring results,
both error types and the limits of the evidence?

## Expanded comparison: 30 new responses

We kept the same two prompts and model settings, but tested three scenarios with
five responses per prompt per scenario: **3 x 2 x 5 = 30 responses**.
The original six-response pilot is retained separately, not pooled into this result.

| Scenario | What the explanation needs to notice |
| --- | --- |
| **Actual project results** | 46/60 bad risks detected; 40/140 good risks falsely flagged |
| **Synthetic: high accuracy, low detection** | 90% accuracy, but only 4/20 bad risks detected; 4/180 good risks falsely flagged |
| **Synthetic: high detection, many false flags** | 90/100 bad risks detected, but 55/100 good risks falsely flagged |

The last two scenarios contain **invented aggregate counts**, not new results of
our credit model. No classifier was trained or tested for those scenarios.
The ML model, its final test results and its threshold remain unchanged.

### What happened

Counts below are out of **15 responses per prompt** in the expanded comparison.
The word-limit check is automatic; the other checks are an **AI-assisted reading
of all 30 answers, not independent or blinded human ratings**.

| Criterion passed | Simple prompt | Structured prompt |
| --- | --- | --- |
| No numerical error identified | 15/15 | 15/15 |
| Both class denominators and relevant counts explicit | 10/15 | 15/15 |
| Both error types explained | 15/15 | 15/15 |
| Scope stated and no clear unsupported claim identified | 10/15 | 15/15 |
| Within 120-180 words | 15/15 | 12/15 |

**Takeaway:** the structured prompt more consistently included complete numerical
context and avoided clear overreach under the stated rubric. It also exceeded
the word limit three times (183, 192 and 183 words). Neither prompt had an
identified numerical error in this sample; this does not establish an error-free model.

Explicit denominators can occur in a different sentence from their corresponding
counts; a literal "out of" phrase is not required. Percentages alone do not pass.
The structured prompt explicitly asks for these details, so this is partly a
compliance check, not a neutral test of overall writing quality.

Five simple responses were flagged for claims beyond the evidence, including
"useful for reducing credit losses", "more useful as a decision-support tool",
and "missing a bad borrower is usually the costliest mistake". These judgements
are qualitative: borderline cases and the exact interpretation are documented in
the assessment. Another reviewer could reasonably score some wording differently.
Both prompts also sometimes describe classification as actual approval/rejection;
that wording must not be adopted as a description of what our app does.

### Results by scenario

Each cell shows **simple / structured passes out of 5**.

| Scenario | Numerical accuracy | Complete denominators | Both errors | Bounded claims | Word limit |
| --- | --- | --- | --- | --- | --- |
| Actual results | 5 / 5 | 1 / 5 | 5 / 5 | 3 / 5 | 5 / 4 |
| Synthetic: high accuracy | 5 / 5 | 5 / 5 | 5 / 5 | 5 / 5 | 5 / 3 |
| Synthetic: high detection | 5 / 5 | 4 / 5 | 5 / 5 | 2 / 5 | 5 / 5 |

**Nicolai Hönnige confirmed human review of the 30 responses and their assessment
on 24 October 2026. No corrections were reported.** The assessment remains
AI-assisted, not independent or blinded. Human review does not remove its limits.
There are only three purposefully chosen scenarios and one model. Repetitions
are not independent real-world tasks. The extension was designed after looking
at the pilot; it is exploratory, not a confirmatory statistical study. Synthetic
examples vary in more than one respect, so differences cannot be attributed to
just one factor. Many structured answers call invented scenarios "historical";
most also explicitly say they are invented, but "synthetic" is the accurate term.

## Experiment records

- [All 30 answers](run_03/outputs.md): readable, unedited response text.
- [Assessment](run_03/assessment.json): every response, numerical excerpts,
  criterion decisions, cautions, exact word counts and recorded token usage.
- [Protocol](run_03/protocol.json): contexts, exact prompts, order and criteria,
  committed as `e4dec48` **before** the first API request.
- [Raw API records](run_03/attempts.jsonl): all 30 requests completed; none replaced.
- In Streamlit, open **Recorded experiment: simple vs structured prompt**.
  Actual project results are selected first. The two synthetic options carry a
  warning. Each option shows the first completed response for that prompt and
  scenario in recorded request order, not the best-scored response. This works offline.
- [Demo guide](../../demo/README.md): the aggregate and profile explanations are
  separate features. Profile explanations are outside this prompt comparison.

<details>
<summary>Optional: protocol, usage and original pilot</summary>

Both phases use `gpt-5.4-mini-2026-03-17`, temperature 0.7, reasoning effort none,
maximum 800 output tokens, no tools or automatic retries, and a 120-180-word
instruction. Requests are independent. The expansion shuffles scenario/repetition
blocks and prompt order within each pair using order seed 42. Generation itself
is not seeded. Criteria were fixed before generating the extension and are
reported separately without a composite score; the pilot's /8 scores are not
comparable to the extension's five pass/fail criteria.

Expanded usage: **15,915 input + 6,845 output tokens**, no cached input.
Estimated standard API cost: **$0.04274**, not an account billing statement.
It excludes the pilot and other app requests. Rates were checked on 24 October
2026: $0.75/million input and $4.50/million output tokens.
[Official model/pricing reference](https://developers.openai.com/api/docs/models/gpt-5.4-mini).
`store=False` is used; this is not a zero-provider-retention claim.

The initial pilot compared three answers per prompt on the actual project
results. All six had correct numbers and explained both error types; the simple
answers omitted class denominators. One structured answer exceeded the word
limit. The AI-assisted /8 means were 7.00 and 7.67. No separate human sign-off is recorded for the pilot.

- [Pilot answers](outputs.md), [protocol](run_02/protocol.json),
  [raw records](run_02/attempts.jsonl), [assessment](run_02/assessment.json).
- [Initial authentication failure](attempts.jsonl) and [setup protocol](protocol.json)
  remain as a record; no successful answer was discarded.
- [First profile example](profile_example.json) and
  [refined profile example](profile_example_refined.json) are separate integration
  checks, not part of either comparison. The first had technical names/raw values
  and a counting slip; the refined prompt asks for friendly labels and 2-3 features.

Automated tests use simulated replies and make no paid API calls. The experiment runner preserves existing records and validates the frozen protocol fingerprints.

[Evaluation design reference](https://developers.openai.com/api/docs/guides/evaluation-best-practices).

</details>

The full written analysis is in [Section 3 of the report](../../report/report.md#3-generative-ai-experiment).
