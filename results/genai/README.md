# Generative AI experiment

**Question:** Can generative AI explain credit-scoring results clearly without unsupported claims?

We asked the same model to explain the same aggregate results with two different
prompts, three times each. The simple prompt asked for an explanation for a bank
manager. The structured prompt explicitly requested error types, denominators
and limits. Both received the same facts and a 120-180-word target.

## What happened

| | Simple prompt | Structured prompt |
| --- | --- | --- |
| Completed responses | 3 | 3 |
| Correct numerical values | All 3 | All 3 |
| Both error types explained | All 3 | All 3 |
| Includes the 60 bad / 140 good case denominators | None | All 3 |
| Meets the word target | All 3 | 2 of 3; one had 193 words |
| Mean rubric score / 8 | 7.00 | 7.67 |

The structured prompt supplied more complete numerical context in this example.
It did not fix fabricated numbers: neither version invented any. Six answers to
one input do not establish statistical significance or general prompt superiority.

The assessment is **AI-assisted, not independent or blinded; human sign-off is
still pending**. Its four criteria were fixed before generation, each worth 0-2:
numerical accuracy/completeness, clarity/length, explanation of both errors, and
avoidance of specified unsupported claims. A high score does not certify every
phrase: simple answers used approval/rejection language, one called the model a
"useful screening tool", and another generalized error priorities beyond our
historical cost assumption. Keep the raw answers unchanged when correcting wording.

## What to read or show

- [All six real answers](outputs.md): readable directly on GitHub.
- [Assessment with scores, evidence and cautions](run_02/assessment.json): optional detail.
- In Streamlit, open **Recorded experiment: simple vs structured prompt**. It shows
  the first completed answer per version, with a model name and timestamp. This
  works without an API key or network access; examples were not chosen by score.
- [Demo guide](../../demo/README.md): live aggregate and individual-profile explanations.
  Profile explanations are a later extension, outside this six-answer comparison.

<details>
<summary>Optional: exact protocol, execution history and technical evidence</summary>

Model: `gpt-5.4-mini-2026-03-17`, OpenAI Responses API, temperature 0.7,
reasoning effort none, maximum 800 output tokens, no tools or automatic retries.
Requests were independent and alternated simple/structured for three repetitions.
Only aggregate facts were sent in this experiment, not applicant inputs.

- [Full protocol and exact prompts](run_02/protocol.json), written before generation.
- [All raw responses, timestamps, IDs and usage](run_02/attempts.jsonl).
- [Full scoring rubric](run_02/protocol.json) and [assessment](run_02/assessment.json).
- [Run index used by the demo](selected_run.json).
- [Initial setup protocol](protocol.json) and [authentication failure](attempts.jsonl).
  That failure was retained; after the key was corrected all six requests completed.
  No successful answers were discarded.
- [First profile integration example](profile_example.json) and
  [refined profile example](profile_example_refined.json). The first contained
  technical labels/raw values and a counting slip; the refined prompt requests
  friendly labels, an explicit reference and only 2-3 features. These additional
  checks are not part of the original experiment or its score/cost total.

Recorded experiment usage: 3,213 input and 1,454 output tokens. Estimated standard
cost: $0.00895 using the published rates checked on 20 October 2026, not an account
billing statement. [Official model/pricing reference](https://developers.openai.com/api/docs/models/gpt-5.4-mini).
The API requests use `store=False`; this is not a claim of zero provider retention.

The protocol and attempts are preserved as evidence. Do not rerun the experiment
just for the presentation. Ordinary automated tests use synthetic replies.
For a separately justified new run, the technical command is:

```powershell
.\.venv\Scripts\python.exe -u code/genai.py --output-dir results/genai/new_run
```

Use a new folder and keep earlier attempts; never include credentials in prompts
or Git. API setup belongs in the [demo guide](../../demo/README.md).

</details>

<details>
<summary>Optional: chapter 3 reference text to copy into the shared Word report</summary>

This is copy-ready reference material, not a second working report. Edit the
shared Word document in Teams. Read the real answers and assessment before
adopting the text; human review has not been recorded as complete.

### 3. Generative AI experiment

We investigated whether generative AI could explain our credit-scoring results
clearly without making unsupported claims. The task was to explain the overall
evaluation to a bank manager without a machine-learning background. We did not
ask the AI to make credit decisions or explain why an individual applicant
received a particular prediction.

The experiment used the OpenAI Responses API with the fixed model snapshot
GPT-5.4 mini, dated 17 March 2026 (OpenAI, n.d.-a, n.d.-b). We compared two
prompts. The simple version asked: "Explain these credit-scoring results to a
bank manager." The structured version additionally requested both error types,
the relevant class denominators and a distinction between accuracy and bad-risk
detection. It also instructed the model not to invent individual causes, treat
scores as calibrated default probabilities, describe assumed costs as actual
savings, or recommend lending decisions or deployment.

Both prompts received the same aggregate results, including 46 of 60 bad risks
detected and 40 of 140 good risks incorrectly flagged. They also received the
same audience instruction and a target length of 120-180 words. We generated
three responses per prompt in alternating order, using temperature 0.7,
reasoning effort none and a maximum of 800 output tokens. Every request was
independent. No applicant inputs or personal data were sent to the API. An
initial authentication failure was retained in the log; the six completed
responses came from the subsequent run after the local key was corrected.

Before generation, we defined four criteria, each worth up to two points:
numerical accuracy and completeness, clarity, explanation of both error types,
and avoidance of specified unsupported claims. Numerical completeness required
the relevant denominators, not just the numbers of detected or incorrectly
flagged cases. Clarity included the word target. The assessment was AI-assisted,
with evidence excerpts recorded for each score; it was not an independent or
blinded human evaluation. Team review of the answers and assessment is still
required before final submission.

The simple prompt scored 7 out of 8 in all three responses. The structured
prompt scored 8, 7 and 8, giving a mean of 7.67. All six responses used correct
numerical values and explained both error types. The difference in numerical
scores arose because the simple responses omitted the class denominators of
60 bad risks and 140 good risks. The structured responses included those
denominators, making the scale of each error easier to judge. However, one
structured response contained 193 words and exceeded the requested length.

The qualitative review also found wording that the numerical scores did not
fully capture. Simple responses described cases as approved or declined,
although our application only predicts risk classes. One described the model
as a "useful screening tool", suggesting more practical usefulness than the
experiment establishes. These observations show that a short scoring rubric
does not replace reading the actual output. Original responses remain
unchanged in the experiment log, separate from any wording adopted in the report.

We integrated the structured prompt into the Streamlit demonstration as an
optional explanation of the aggregate results. It does not alter the saved
classifier, decision threshold or individual prediction. Recorded real responses
from both prompts are also available in the app, allowing the experiment to be
shown without a live API connection.

Separately, we added an optional explanation of the last submitted fictional
profile. This feature calculates contributions from the saved logistic-regression
coefficients relative to mean transformed development inputs and supplies them
to the language model. It does not ask the language model to infer reasons from
the class label alone. After an explicit button click, the seven fictional
inputs, predicted class and contributions are sent to OpenAI. These explanations
describe the fitted model's calculation, not causal effects or future default
probabilities. This extension was not part of the six-response prompt comparison.

For this input, the structured prompt produced more complete numerical context,
but did not guarantee compliance with every instruction. The experiment contains
only six outputs for one results summary, and the prompts differ in several
instructions. It therefore provides an illustrative comparison rather than
evidence of statistical significance or general reliability.

### References for this section

OpenAI. (n.d.-a). *Create a model response*. https://developers.openai.com/api/reference/python/resources/responses/methods/create

OpenAI. (n.d.-b). *GPT-5.4 mini*. https://developers.openai.com/api/docs/models/gpt-5.4-mini

</details>
