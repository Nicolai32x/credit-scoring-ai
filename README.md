# Credit Risk Prediction with Machine Learning

A university project for **Introduction to AI in Business and Management**.

**Research question:** How well can a simple machine learning model classify credit risk using seven applicant and loan characteristics?

The project combines a comparison of classification models, a Streamlit demonstration and a generative AI explanation experiment. It uses the historical UCI German Credit dataset and is a teaching prototype, not a lending system.

## Report and presentation

| Document | Content |
| --- | --- |
| **[Report (PDF)](report/report.pdf)** · [Markdown](report/report.md) | Complete analysis, results, business implications, limitations and references |
| **[Presentation (PDF)](presentation/credit_risk_prediction.pdf)** | Final 19-slide presentation |
| [Results](results/README.md) | Model comparison, final test results and figures |
| [Generative AI experiment](results/genai/README.md) | Prompt comparison, recorded responses and assessment |

These documents and the saved notebook outputs can be read directly on GitHub without installing software.

## Main findings

The dataset contains 1,000 historical cases. Seven inputs describe the loan and selected financial characteristics; amounts remain in historical Deutsche Mark (DM).

We compared an Always-Good baseline, logistic regression and random forest using five-fold cross-validation on 800 development cases. Logistic regression and a threshold of 0.5 were selected before a single final evaluation on 200 held-out cases.

| Final test measure | Logistic regression |
| --- | --- |
| Accuracy | 73.0% |
| Balanced accuracy | 74.0% |
| Bad risks detected | 46 of 60 (76.7%) |
| Good risks incorrectly flagged | 40 of 140 (28.6%) |
| Bad-risk precision | 53.5% |
| ROC-AUC | 0.810 |

The model detects bad risks that the majority baseline misses, but produces substantial false alarms. The results do not establish fairness, current lending suitability or calibrated probabilities of future default.

A separate GenAI experiment compared two prompts across three scenarios and five repetitions per prompt, producing 30 responses. One scenario uses actual model results; two use synthetic counts. Structured instructions improved completeness in this sample, but did not guarantee word-limit compliance. The assessment was AI-assisted and subsequently reviewed by Nicolai Hönnige; it was not independent or blinded.

## Run the demo

Use **Python 3.12.13** and the pinned dependencies. From the repository root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe demo/run.py
```

Open [http://127.0.0.1:8501/](http://127.0.0.1:8501/). Stop the server with Ctrl+C.
On macOS/Linux, use `.venv/bin/python` instead of `.\.venv\Scripts\python.exe`; the project has been verified on Windows.

The saved model, calculated contributions and recorded GenAI examples work without an API key. Optional live AI explanations require an OpenAI API key and incur API charges. See the **[demo guide](demo/README.md)** for configuration, fictional examples and data flow.

## Repository contents

| Folder | Content |
| --- | --- |
| [report/](report/report.md) | Final report in Markdown and PDF, with its figures |
| [presentation/](presentation/README.md) | Final presentation and content overview |
| [demo/](demo/README.md) | Streamlit app, startup and usage guide |
| [notebooks/](notebooks/01_exploration.ipynb) | Executed data exploration and [model evaluation](notebooks/02_model_comparison.ipynb) |
| [code/](code/preprocessing.py) | Data loading, preprocessing, training, evaluation and AI integration |
| [data/](data/README.md) | Original dataset, dictionary, attribution and fixed split |
| [results/](results/README.md) | Saved metrics, figures, model and experiment evidence |
| [prompts/](prompts/README.md) | Exact explanation prompts and AI-use documentation |
| [tests/](tests/test_demo.py) | Automated checks for data, evaluation, demo and AI integration |

## Verification and reproducibility

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m pip check
```

Tests use simulated API responses and do not require paid API calls. The notebooks retain executed results. The demo loads the saved development-trained pipeline without retraining. The fixed split, model decision and final evaluation are retained with provenance; the reserved test data were not used for model selection. Experimental protocols and raw responses are preserved as evidence, including their original historical review status.

## Team and AI use

**Jan Jurczyk:** business context and literature. **Nicolai Hönnige:** data, technical implementation and GenAI. **Philipp Pehlemann:** results and business value. **Zofia Wiśniewska:** risks and conclusions.

Generative AI supported coding, debugging, documentation and drafting/editing of report and presentation material. The team reviewed and adapted that material and remains responsible for the submitted work. The OpenAI API provides explanations; it does not determine the classifier's predictions. See [AI use and prompts](prompts/README.md).

**Presentation date:** 3 November 2026. Dataset attribution and reuse terms are in [data/LICENSE.md](data/LICENSE.md).
