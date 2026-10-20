# Generative AI experiment results

Question: **Can generative AI explain credit-scoring results clearly without
unsupported claims?**

We compared a simple and a structured prompt on the same aggregate test-result
summary, with three independent requests per prompt. Model:
`gpt-5.4-mini-2026-03-17`; temperature 0.7, reasoning effort none, maximum 800
output tokens. All six returned completed responses. The experiment does not
change the credit-risk model, threshold or test results.

## Read these files

- [Actual answers in readable form](outputs.md): all six unedited responses.
- [Experiment design and report text](../../prompts/experiment.md): question,
  exact rubric, setup and a draft for report chapter 3.
- [Full protocol](run_02/protocol.json): full prompts, shared facts and settings.
- [Raw responses](run_02/attempts.jsonl): timestamps, response IDs, usage and outputs.
- [Assessment with evidence](run_02/assessment.json): criterion scores, excerpts,
  rationale and limitations. **AI-assisted; human sign-off pending.**

## Assessment

The criteria were fixed before generation, each scored 0-2: numerical accuracy
and inclusion of the two class denominators, clarity and the 120-180-word target,
explanation of both error types, and avoidance of the specified unsupported claims.
Scores are descriptive judgments, not a validated measurement instrument.

| Attempt | Prompt | Words | Numerical accuracy | Clarity | Both errors | Unsupported claims | Total / 8 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Simple | 173 | 1 | 2 | 2 | 2 | 7 |
| 2 | Structured | 169 | 2 | 2 | 2 | 2 | 8 |
| 3 | Simple | 169 | 1 | 2 | 2 | 2 | 7 |
| 4 | Structured | 193 | 2 | 1 | 2 | 2 | 7 |
| 5 | Simple | 148 | 1 | 2 | 2 | 2 | 7 |
| 6 | Structured | 171 | 2 | 2 | 2 | 2 | 8 |

Mean score: **7.00/8 simple**, **7.67/8 structured**.

All six answers used correct numerical values and explained both kinds of
error. The simple answers omitted the class denominators of 60 bad and 140
good risks, while the structured answers included them. This difference is
about completeness, not invented or incorrect numbers. One structured answer
exceeded the word target with 193 words.

The fixed unsupported-claims criterion gives every answer 2 points: none makes
an explicit deployment recommendation, claims actual monetary savings or
calibrated default probability, or invents causal feature effects, and all
include historical/cautionary limits. That score does not certify every phrase:

- Simple attempt 1 says false approvals are usually the most important lending
  error. That is broader than our supplied historical cost assumption supports.
- Simple attempt 5 calls the model a "useful screening tool", which suggests
  more practical usefulness than this experiment establishes.
- The simple answers use approval/rejection or accepted/declined language.
  Our application only predicts classes; it does not make lending decisions.

These are additional qualitative cautions, not retrospective changes to the
scoring rules. If adopting any text, correct that framing and keep the original
answers unchanged. The exercise also shows a limitation of a small scoring rubric.

## What we can conclude

For this input, the structured prompt made the numerical context more explicit,
but did not eliminate all instruction failures. It did not correct fabricated
statistics: there were none in either group. Six responses to one results
summary do not establish general superiority, statistical significance, or
reliability for real lending. The rubric and scoring were AI-assisted and not
independent or blinded. Nicolai still needs to read the answers and assessment
and record any corrections before final submission.

## Execution history and cost

The first setup attempt was rejected with `AuthenticationError` because the
local credential was not the secret API key. [Its protocol](protocol.json) and
[failure record](attempts.jsonl) are preserved. No further requests were sent
until the user replaced the key. The completed experiment is in `run_02/`;
no successful answers were discarded. [The run index](selected_run.json) points
the Streamlit demo to that completed run.

Later profile-explanation integration checks are kept separately as
`profile_example.json` and `profile_example_refined.json`. They use fictional
scenario A and are not part of the six-response comparison or its cost total.
The original output is preserved alongside the refined prompt's output; see
the demo guide for the wording problems and changes. These are not scored as
additional evidence of general prompt superiority.

Recorded usage: **3,213 input tokens**, **1,454 output tokens**, no cached input
or reasoning tokens. Estimated standard API cost: **$0.00895**, using the
published GPT-5.4 mini rates checked on 20 October 2026. This is an estimate,
not a billing statement; see the [official model pricing](https://developers.openai.com/api/docs/models/gpt-5.4-mini).

## Demonstration

Open Streamlit and scroll to **AI explanation of our results**. This aggregate button
uses the structured prompt and sends only aggregate evaluation facts. It never
sends the applicant inputs. Each click is a separate paid request and its answer
must be checked; later live responses are not part of the six-answer comparison.

For a presentation without API access, expand **Recorded experiment: simple vs
structured prompt**. It shows the first completed response per variant, clearly
labeled as recorded. That choice is fixed, not based on which answer looks best.
