# Demo sketch

Proposal for the team meeting; no Streamlit app or scoring model has been built.
The existing `app.py` remains a placeholder. After agreement, the technical lead
will connect a saved preprocessing/model pipeline to a small Streamlit form.

## Planned interface

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

Use the exact mappings in [the dataset guide](../data/README.md). All seven
features must match the trained model. No hidden guesses for other features.
Keep category meanings faithful to the dictionary, including combined unknown
categories. Keep DM labels explicit. Initially show a class, not an unsupported
percentage probability of future default.

Numeric inputs should stay within the observed teaching-data ranges: amount
250-18,424 and duration 4-72 months. Staying within those ranges does not ensure
that a combination is well represented. Other inputs use observed categories.

## Fictional scenarios to try after implementation

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
screenshots or example outputs. Add final installation/startup instructions
when the actual demo exists; do not install Streamlit just for this planning step.

To run the current placeholder from the project directory:

```powershell
.\.venv\Scripts\python.exe demo/app.py
```
