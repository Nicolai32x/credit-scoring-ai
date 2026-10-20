# Streamlit demo

The seven-input Streamlit app is implemented in `demo/app.py`. It loads the
complete saved pipeline from `results/selected_pipeline.joblib`: logistic regression,
development-trained preprocessing, and explicit score threshold 0.5. Model
decisions were frozen before final testing; see notebook 02 and the results guide.
The form displays English category descriptions, preserves historical DM units,
and returns a predicted class. It shows no percentage default probability.
Use `code/final_model.py`'s `predict_risk(bundle, inputs)` helper to apply the saved
threshold consistently. Do not call training or final assessment from the app.
The bundle contains the pipeline, threshold, seven feature names, training count,
decision checksum and scikit-learn version. Reuse it without fitting on test cases.

## Interface

```text
Credit Risk Demo - Historical Teaching Dataset

Credit amount (DM)          [integer]
Duration (months)          [integer]
Loan purpose               [dropdown]
Checking-account category  [dropdown]
Savings/bonds category     [dropdown]
Employment duration        [dropdown]
Credit history             [dropdown]

[Predict risk class]

Predicted class: [Good risk / Bad risk]
Historical dataset demonstration; not a lending recommendation.
```

The app uses the mappings in [the dataset guide](../data/README.md). It accepts
exactly the seven trained inputs and offers only categories supported by the
saved encoder. Combined meanings such as unknown / no savings account remain
visible. Submit the form again after changing inputs; the displayed result
belongs to the last submitted values, which can be expanded below it.

For the teaching demo, use the observed development-data ranges: amount
276-15,945 DM and duration 4-60 months. These are demonstration guardrails,
not general lending rules. Staying within them does not ensure a combination
is well represented. Other inputs use observed development categories.

## Fictional scenarios to try

These are invented discussion examples, not real people or labeled records.
They have no known correct outcome or promised prediction.

| Scenario | Amount (DM) | Months | Purpose | Checking | Savings | Employment | Credit history |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A | 3,000 | 12 | A42: furniture | A12 | A62 | A74 | A32 |
| B | 9,000 | 48 | A40: new car | A11 | A61 | A72 | A33 |
| C | 3,000 | 12 | A42: furniture | A14 | A65 | A74 | A32 |

A and B illustrate contrasting input profiles; do not assume what the model
will predict. C illustrates how the form represents no checking account and
unknown/no savings. A second run may change one input to discuss model behavior;
this is a sensitivity example, not evidence of cause and effect.

## Planned walkthrough

Use the eight-minute sequence and presenters in the
[presentation plan](../presentation/outline.md). It includes input explanation,
practical runs, output interpretation, an actual GenAI prompt/output example,
and limitations. Everyone should contribute material they can explain.

Before presenting, test startup on a second machine and prepare fallback
screenshots or example outputs. Automated checks exercise the form with the
three fictional profiles above and verify that no fitting or dataset loading
occurs. A second-machine check and team rehearsal are still pending.

## Start locally

From the project directory in PowerShell, with the existing `.venv`:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe demo/run.py
```

Open the local URL printed in the terminal (normally `http://127.0.0.1:8501`).
The launcher adds the shared `code/` directory to `PYTHONPATH` before Streamlit
starts, so its imported modules are watched and reloaded. If using the direct
`streamlit run` command instead, restart the server after shared-code changes;
refreshing the browser alone can leave old module signatures in memory.
Stop the server with `Ctrl+C`. On macOS/Linux, use `.venv/bin/python`; those
platforms have not yet been checked. Risk predictions and recorded explanation
examples need no API key or external service. Optional live explanations use
OpenAI; see below. Generative AI is separate from the saved risk classifier.

The reliability panel displays the final test tradeoff: 46/60 bad risks detected,
with 40/140 good risks incorrectly flagged. Use fictional profiles and explain
that these historical results do not establish suitability for real lending.

## Generative AI explanation and experiment

After **Predict risk class**, the result includes **Explain this result with AI**.
This button explains the last submitted fictional profile, not unsent form edits.
It sends the seven submitted values, class, English descriptions and calculated
feature contributions to OpenAI. The disclosure appears beside the button.
Use fictional profiles only. Submitting a new prediction clears its old explanation.

Contributions are computed locally from the saved logistic-regression coefficients.
Each transformed input is centered on the mean transformed inputs of the 800
development cases. Centered values times coefficients, grouped into seven inputs,
plus the reference score reconstruct the model's decision score. That reference
is not a real or typical applicant. Directions toward Bad/Good risk are relative
to it, not causal effects or probability changes. The reference is stored in
`results/explanation_reference.json`; the app never loads training data or fits
anything. **Calculated model contributions** also works without an API key.

Two real checks on fictional scenario A are retained in
`results/genai/profile_example.json` and `profile_example_refined.json`. The first
used technical labels and raw contributions and contained a counting slip
("Two smaller" followed by three features). The prompt was refined to use friendly
labels, 2-3 features, an explicit reference and no raw logits. The second matched
the supplied major contribution directions. These are integration examples,
not part of the six-answer experiment or proof of general explanation reliability.

Below the prediction, **AI explanation of our results** explains the overall
evaluation, not an individual applicant. The live button uses the structured
prompt from `prompts/explanation_structured.txt` and sends only aggregate
evaluation facts. It does not change the classifier, threshold or risk result.
An API error leaves the risk demo usable; requests are never triggered by
ordinary widget reruns.

For live explanations, add the local secret API key to the ignored file
`.streamlit/secrets.toml` as `OPENAI_API_KEY = "your-secret-key"`, or use the
environment variable of the same name. Do not use the key's management ID,
post it in a chat or commit it to Git. A live click incurs API usage charges.

For presentation without a key or network, expand **Recorded experiment: simple
vs structured prompt**. Switch between the first real completed response for
each variant, with the model and timestamp shown. This is a labeled recording,
not an invented answer or a new API call.

The [experiment overview](../results/genai/README.md) links all six actual answers,
their assessment and the draft text for report chapter 3. The structured prompt
included the two class denominators more consistently; one answer exceeded the
word target. Human review of the AI-assisted assessment remains pending.
