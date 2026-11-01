# AI use and explanation prompts

Generative AI supported coding, debugging, project documentation, and drafting and editing of report and presentation material. The team reviewed and adapted AI-generated material and remains responsible for the submitted work. Model metrics were calculated by the Python evaluation pipeline rather than supplied by a language model.

## Exact application prompts

| Prompt | Purpose |
| --- | --- |
| [Simple explanation](explanation_simple.txt) | Explain aggregate evaluation results to a bank manager |
| [Structured explanation](explanation_structured.txt) | Explain the same results with explicit numerical context and limits |
| [Profile explanation](explanation_profile.txt) | Explain a fictional profile using calculated contributions from the saved classifier |

The first two prompts were compared in a six-response pilot and a separate 30-response experiment. The full request contexts, settings, unedited responses and assessments are available in the [experiment documentation](../results/genai/README.md). Protocols preserve the instructions recorded before generation. Historical review statements in those records describe their status at that time; the expanded comparison was subsequently reviewed by Nicolai Hönnige on 24 October 2026.

The profile explanation is a separate application feature, outside the prompt comparison. It describes the fitted model's calculation, not real-world causes or validated default probabilities, and does not change its prediction. The [demo guide](../demo/README.md) explains which fictional inputs are sent after an explicit button click.

## Review and limitations

The expanded experiment used automatic word counts and an AI-assisted reading against supplied facts, followed by Nicolai's review of all 30 responses and their assessment. The evaluation was not independent or blinded. Numerical correctness in this small sample does not establish general reliability. Detailed limitations and examples of unsupported wording are retained alongside the [recorded results](../results/genai/run_03/assessment.json).

The repository records the exact prompts and outputs of the documented API experiments. Development assistance is disclosed here and in the report; it is not presented as a complete verbatim transcript of every development conversation.
