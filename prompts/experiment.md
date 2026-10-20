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
or additional run separately. Ordinary automated tests use synthetic replies
and make no paid API calls.

## Streamlit use

The live button uses the structured prompt and only the fixed aggregate results.
It is separate from the applicant prediction and does not change model settings,
the threshold or test metrics. Repeated UI reruns do not automatically call the
API. Live answers are labeled as generated and need checking.

The recorded-example panel reads the first completed response per variant from
the experiment log and labels it with its timestamp and model. All attempts
remain available for inspection. It works without an API key or network access.
Saved examples are actual API responses, never invented substitutes.

## Official implementation references

- OpenAI. (n.d.). *GPT-5.4 mini*. https://developers.openai.com/api/docs/models/gpt-5.4-mini
- OpenAI. (n.d.). *Create a model response*. https://developers.openai.com/api/reference/python/resources/responses/methods/create
