# Credit Scoring AI

Team project for **Introduction to AI in Business**.
**Question:** How well can a simple model classify credit risk using seven inputs?

## Start here — no installation needed

You can read the text, view/download figures and open the saved notebook outputs
**directly on GitHub**. You do not need to run Python or learn Git for your part.

| Read | What you get |
| --- | --- |
| **[Results and figures](results/README.md)** | The model results, errors, cost illustration and reusable graphics |
| **[Presentation outline](presentation/outline.md)** | Everyone's section, slide suggestions and demo sequence |
| [GenAI experiment](results/genai/README.md) | The prompt comparison, real answers and assessment |

For an AI explanation of the project, download this README and `results/README.md`
and upload them to your usual AI chat. Add the presentation outline for role
questions. Check its answers against the files. [GitHub/AI tutorial](OPTIONAL_TUTORIAL.md)
is optional; it is not required to contribute.

## What Nicolai implemented

1. Checked the original **UCI German Credit** dataset: 1,000 historical cases.
2. Used seven inputs: amount, duration, purpose, checking account, savings,
   employment duration and credit history. Amounts stay in historical **DM**, not EUR.
3. Reserved **200 test cases**; used **800 development cases** to compare an
   always-good baseline, logistic regression and random forest in five validation folds.
4. Selected logistic regression and threshold 0.5 **before the final test**.
   The test was assessed once; the model was not trained on test cases.
5. Built a seven-input Streamlit demo with optional AI explanations, and compared
   two GenAI prompts in a six-response pilot and a separate 30-response extension
   across three scenarios (one actual, two explicitly synthetic).

Nicolai confirmed human review of the expanded GenAI comparison on 24 October
2026. The assessment remains AI-assisted, not independent or blinded.

In plain English: **training** learns patterns, **validation** compares approaches,
and the separate **test** gives the final check. The ML model predicts the risk
class; generative AI explains results and model contributions, without deciding the class.

The selected model detected **46 of 60 bad risks**, but wrongly flagged
**40 of 140 good risks**. Accuracy is **73%**, balanced accuracy **74%**.
This is a working teaching example with substantial errors, not a lending system.
The results page explains these numbers and the 5:1 assumed error-cost illustration.

## Where each person continues

| Person | Area | Main material |
| --- | --- | --- |
| Jan | Business context and existing solutions | This page, presentation outline, own literature |
| Nicolai | Data, method, GenAI and demo | Saved notebooks, GenAI experiment, demo guide |
| Philipp | Results and economics | Results page and its linked figures |
| Zosia | Risks, limitations and conclusions | Results/limitations, demo data flow, own sources |

Write the report in the **shared Word document in Teams** and slides in the
[shared Canva presentation](https://canva.link/doeibex7vw4e04b). Use actual authorship
and record AI assistance. The [report map](report/report.md) identifies sections;
it is an export skeleton, not another draft to edit alongside Word.

## Remaining team checks

- Finish/review the shared report and slides; keep numbers and sources consistent.
- Rehearse the 24-minute presentation and 8-minute demo; confirm the lecturer's time slots.
- Check startup on a second computer and prepare fallback screenshots.
- Export the reviewed report as Markdown/PDF and follow the [submission checklist](submission/README.md).

Presentation date, final topic name and the shared Word link still need to be
recorded. Technical implementation is complete; report/slide readiness is a team check.

## Optional: run or inspect the implementation

To use the demo, see the **[demo guide](demo/README.md)**. It separates the
classifier, aggregate AI explanation and submitted-profile AI explanation.
Recorded GenAI examples work offline; live explanations need a local API key.

<details>
<summary>Technical setup, files and collaboration rules</summary>

Python **3.12.13**; install the pinned packages, not newer model-library versions.
From the project directory in PowerShell, create `.venv` once if absent:

```powershell
uv venv --python 3.12.13 --seed .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe demo/run.py
```

Use [uv's Python setup](https://docs.astral.sh/uv/guides/install-python/) if needed.
For an existing environment, skip creation. On macOS/Linux use `.venv/bin/python`;
only Windows has been verified. Requirements list eight direct dependencies and
pin resolved versions. Keep the local environment and API key out of Git.

- [Notebook 01](notebooks/01_exploration.ipynb): development-data exploration.
- [Notebook 02](notebooks/02_model_comparison.ipynb): validation and saved final-test results.
- [Dataset reference](data/README.md): source, category meanings, integrity and limitations.
- `code/`: loading/preprocessing, model comparison, metrics, frozen final assessment,
  OpenAI integration and exact profile contributions. `tests/` checks those boundaries.
- `results/`: evidence and saved pipeline; JSON/CSV files are optional for team reading.
- `prompts/`: actual prompt texts and chronological AI-use log.

Run checks with:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The fixed split, decision and final assessment are already recorded. Do not
refit/tune using test data or delete artifacts to repeat selection. The demo
loads the saved pipeline. Read saved results instead of rerunning the final test.

Work directly on `main` by default. Check status and remote updates first,
coordinate shared-file edits, preserve team changes and check before committing.
Commit/push completed steps; use a branch only if requested. Never force-push or
reset over another member's work. All project files are in English. Report chapters
and slide footers must reflect actual authorship and AI assistance.

</details>
