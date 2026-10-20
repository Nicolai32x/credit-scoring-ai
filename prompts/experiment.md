# Generative AI experiment: explaining aggregate credit-risk results

## Question and design

Can generative AI explain credit-scoring results clearly without unsupported
claims? Compare a simple prompt with a structured prompt that asks explicitly
for error tradeoffs and limits. Both receive the same aggregate final-test
summary, audience instruction and 120-180-word target. No individual applicant
inputs, raw rows, API credentials or personal data are included.

Use `gpt-5.4-mini-2026-03-17` through the OpenAI Responses API. Each request is
independent, with reasoning effort `none`, temperature 0.7, a maximum of 800
output tokens, no tools and no automatic retries. Run three repetitions of each
prompt in paired order: simple, structured, simple, structured, simple, structured.
Model settings and facts stay fixed. Save every actual response, including
incomplete outputs and failed attempts; do not select only favorable answers.

The protocol and exact full prompts are written before the first request in
`results/genai/protocol.json`. Actual outputs, response IDs, timestamps, model
IDs, usage and source-report checksum go into `results/genai/attempts.jsonl`.
The SDK does not request server-side response storage (`store=False`); outputs
are deliberately saved locally for the experiment. This is not a claim of
zero provider retention.

## Assessment fixed before generation

Each answer receives 0, 1 or 2 points on each criterion:

| Criterion | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Numerical accuracy | Incorrect number or denominator | No numeric error, but key counts omitted | Correct 46/60 detected and 40/140 falsely flagged; no numeric errors |
| Clarity | Hard to follow | Understandable, but jargon unexplained or outside 120-180 words | Clear for a nontechnical reader and within the word target |
| Balanced errors | Neither error type explained | One error type explained | Both bad predicted good and good predicted bad explained |
| Unsupported claims | Invented causes, default probabilities, actual savings/profit or deployment recommendation | None of those, but historical scope or need for caution omitted | No unsupported claims and historical/teaching limits clearly stated |

Record a brief rationale with evidence from each output. Review is AI-assisted,
not an independent or blinded human evaluation; human sign-off must be stated
separately. An answer can fail despite sounding fluent. Keep unedited raw outputs
separate from any corrected text used in the report or presentation.

Six responses to one fixed input provide an illustrative comparison only. The
structured prompt changes multiple instructions, so differences cannot be
attributed to a single instruction. Do not claim statistical significance or
general reliability, and report no improvement if the outputs do not show one.

## Local setup and execution

The API key goes in the ignored `.streamlit/secrets.toml` file:

```toml
OPENAI_API_KEY = "your-local-key"
```

Alternatively set the `OPENAI_API_KEY` environment variable. Never add a key to
Git or a prompt. The code uses the official OpenAI API endpoint explicitly.

From the project directory in PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -u code/genai.py
```

The command makes at most six requests and refuses to overwrite an existing
attempt log. Check availability and credit in the provider account. Do not
delete failed attempts to make the experiment look better; document any repair
or additional run separately, using `--output-dir results/genai/run_02` for a
second run. `results/genai/selected_run.json` identifies the completed run used
for the demo; earlier failed setup attempts remain visible in the original log.
Ordinary automated tests use synthetic replies
and make no paid API calls.

## Streamlit use

The aggregate live button uses the structured prompt and only the fixed aggregate results.
It is separate from the applicant prediction and does not change model settings,
the threshold or test metrics. Repeated UI reruns do not automatically call the
API. Live answers are labeled as generated and need checking.

The recorded-example panel reads the first completed response per variant from
the experiment log and labels it with its timestamp and model. All attempts
remain available for inspection. It works without an API key or network access.
Saved examples are actual API responses, never invented substitutes.

A later **Explain this result with AI** feature explains the last submitted
fictional profile using calculated logistic-regression contributions. It sends
the profile, class and contributions after a visible disclosure and is outside
the six-answer experiment. Two actual integration outputs and a prompt refinement
are documented in the demo guide; the original experiment and ML model are unchanged.

## Official implementation references

- OpenAI. (n.d.). *GPT-5.4 mini*. https://developers.openai.com/api/docs/models/gpt-5.4-mini
- OpenAI. (n.d.). *Create a model response*. https://developers.openai.com/api/reference/python/resources/responses/methods/create

## Execution and results

The experiment is complete. The first setup attempt failed authentication and
is retained in the original log. After correction, all six requests in `run_02`
completed. No successful outputs were discarded. See the
[result overview](../results/genai/README.md), [all actual answers](../results/genai/outputs.md)
and [AI-assisted assessment](../results/genai/run_02/assessment.json).
Human review remains pending; do not describe this as an independent human study.

## Report chapter 3 - draft for the shared Word document

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
