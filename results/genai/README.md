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

## What to read or show

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

## Human review

Nicolai confirmed in chat that he completed the review on 24 October 2026.
No corrections were reported; the original AI-assisted scores and responses are
unchanged. This confirmation concerns the expanded comparison, not an independent
or blinded evaluation or a second review by another team member.

For other readers, useful checks include the five flagged simple answers
(4, 12, 19, 21, 29), borderline statements in 10 and 27, length failures
(1, 7, 25), and approval/rejection wording in both variants. The frozen protocol
retains its original prospective pending-review wording as an audit record.

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
limit. The AI-assisted /8 means were 7.00 and 7.67. Human sign-off remains pending.

- [Pilot answers](outputs.md), [protocol](run_02/protocol.json),
  [raw records](run_02/attempts.jsonl), [assessment](run_02/assessment.json).
- [Initial authentication failure](attempts.jsonl) and [setup protocol](protocol.json)
  remain as a record; no successful answer was discarded.
- [First profile example](profile_example.json) and
  [refined profile example](profile_example_refined.json) are separate integration
  checks, not part of either comparison. The first had technical names/raw values
  and a counting slip; the refined prompt asks for friendly labels and 2-3 features.

Ordinary automated tests use fake replies, not paid API calls. Do not regenerate
responses for the presentation. The extension runner refuses to overwrite attempts
and validates the frozen protocol's source fingerprints. A future separately
justified run needs a new output folder and a new prepared protocol:

```powershell
.\.venv\Scripts\python.exe code/genai_comparison.py prepare --output-dir results/genai/new_run
.\.venv\Scripts\python.exe code/genai_comparison.py run --output-dir results/genai/new_run
.\.venv\Scripts\python.exe code/genai_comparison.py export --output-dir results/genai/new_run
```

[Evaluation design reference](https://developers.openai.com/api/docs/guides/evaluation-best-practices).

</details>

<details>
<summary>Optional: updated chapter 3 reference text for the shared Word report</summary>

This is reference text to adapt in the shared Word document, not another working
draft. Nicolai confirmed human review of the expanded comparison on 24 October
2026; no corrections were reported. Other authors should check the material
before adopting it.

### 3. Generative AI experiment

We investigated whether generative AI could explain credit-scoring results to a
bank manager without a machine-learning background. The task concerned an
aggregate evaluation, not individual lending decisions. We used the OpenAI
Responses API with the fixed GPT-5.4 mini snapshot dated 17 March 2026
(OpenAI, n.d.-a, n.d.-c).

We compared a simple prompt asking for an explanation with a structured version
requesting both error types, class denominators and a distinction between accuracy
and bad-risk detection. The structured version also warned against invented
causes, calibrated-default claims, treating illustrative costs as actual savings,
and recommending lending decisions or deployment. Both received identical facts
within each scenario and the same 120-180-word instruction.

The first six-response pilot used our actual results only. After inspecting that
pilot, we designed a separate extension with three scenarios and five responses
per prompt per scenario, giving 30 new responses. One scenario used the saved
project test results: 46 of 60 bad risks detected and 40 of 140 good risks wrongly
flagged. Two explicitly synthetic scenarios tested different trade-offs. One had
90% accuracy but detected only 4 of 20 bad risks; the other detected 90 of 100 bad
risks but wrongly flagged 55 of 100 good risks. These invented counts were used
to test explanations; they are not additional results of our credit model.

The extension kept the original prompts and settings: temperature 0.7, reasoning
effort none, maximum 800 output tokens, no tools and no automatic retries.
Scenario/repetition blocks and prompt order within each pair were shuffled using
a fixed order seed. This did not seed the language model's generation. The full
protocol, inputs and criteria were committed before generation, and all 30
requests completed. No successful response was replaced or discarded. Only
aggregate facts were sent, not applicant records. The original pilot remains
separate and is not pooled into the new comparison.

Before generation, we defined five pass/fail checks: numerical accuracy, complete
class denominators and relevant counts, explanation of both error types, bounded
claims, and the word limit. Length was checked automatically; the other criteria
were assessed by an AI-assisted reading against the supplied facts, with
numerical excerpts and reasons recorded. Class totals and corresponding counts
could occur in separate clearly linked sentences. There was no composite score.
The assessment was not blinded or independent. Nicolai Hönnige subsequently
confirmed human review of the 30 answers and assessment on 24 October 2026;
no corrections were reported.

In the extension, no numerical error was identified in either prompt's 15
responses, and both error types were explained throughout. The simple prompt
provided complete denominators and counts in 10 of 15 responses, compared with
15 of 15 for the structured prompt. Five simple responses were flagged for clear
claims beyond the evidence, such as practical screening usefulness or a general
claim about the costliest lending mistake. No clear failure of that criterion
was identified in the structured responses, although both variants sometimes
used approval/rejection language for classification. Borderline judgements and
synthetic-versus-historical wording remain documented as cautions. The simple
prompt met the word target in all 15 responses; the structured prompt met it in
12, with three responses containing 183, 192 and 183 words.

The result supports a limited observation: explicit instructions made the
requested numerical context more consistent in these scenarios, but did not
guarantee compliance with every constraint. The structured prompt explicitly
requests content used in the scoring criteria, so this partly measures prompt
compliance rather than overall writing quality. The extension was designed after
seeing the pilot, includes only three selected scenarios and one model, and
contains repeated answers rather than 30 independent tasks. It cannot establish
general reliability or statistical superiority. Automated checks should be
combined with human judgement (OpenAI, n.d.-b).

The Streamlit demo provides recorded responses for all three scenarios without
a live connection, with synthetic examples clearly labelled. Its live aggregate
explanation uses the actual project results. Separately, an optional explanation
of a submitted fictional profile uses calculated logistic-regression contributions
relative to mean transformed development inputs. After an explicit click, those
seven fictional inputs, the predicted class and contributions are sent to OpenAI.
This describes the fitted calculation, not causal effects or future default
probabilities. It is outside both prompt comparisons and does not alter the
classifier or its threshold.

### References for this section

OpenAI. (n.d.-a). *Create a model response*. https://developers.openai.com/api/reference/python/resources/responses/methods/create

OpenAI. (n.d.-b). *Evaluation best practices*. https://developers.openai.com/api/docs/guides/evaluation-best-practices

OpenAI. (n.d.-c). *GPT-5.4 mini*. https://developers.openai.com/api/docs/models/gpt-5.4-mini

</details>
