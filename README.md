# Credit Scoring AI

Team project for **Introduction to AI in Business**. We investigate how a
credit-scoring model can support a business decision and assess its results,
costs, and limitations. We will use Statlog (German Credit Data) and a small
Streamlit demo with seven inputs.

## Current status and project documents

The original dataset, its structural review, project plan, and presentation
outline are ready. Python and package versions are recorded. The named data
loader and fixed 800/200 development/test split are implemented and checked;
notebook 01 now includes development-only exploration, tables, four figures and
interpretation. Reusable encoding/scaling pipelines are implemented and demonstrated
on one training/validation fold in notebook 02. That notebook also compares a
majority baseline, logistic regression and random forest in five development-only
validation folds. Logistic regression and threshold 0.5 were frozen before a
one-time test assessment. The final pipeline and test results are saved;
the local seven-input Streamlit demo is implemented.
The report is written in Word in Teams, and a Canva presentation template is ready.

Start with [the project plan](PROJECT_PLAN.md), [dataset guide](data/README.md),
[presentation outline](presentation/outline.md), and [demo sketch](demo/README.md).
No installation is required to read these files or contribute to the written work.

## Getting started

Questions about the project or your role? Upload `README.md`, `PROJECT_PLAN.md`,
and `presentation/outline.md` to your usual AI chat and ask it to explain them
in simple terms. Add other relevant files when needed. You do not need to
install anything for this; check its answers against the files and ask the team
if something is unclear.

If you want to try GitHub edits or use an AI assistant with the project, see the
[optional GitHub and AI tutorial](OPTIONAL_TUTORIAL.md). It is not a prerequisite
for contributing; you can also share your work with the team and ask for help.

### Technical setup for running Python later

The development environment uses **Python 3.12.13**, recorded in `.python-version`.
Use [uv](https://docs.astral.sh/uv/guides/install-python/) to find or install that
version and create the environment. Create `.venv` only once; for an existing
environment, skip the first command. From the project directory in PowerShell:

```powershell
uv venv --python 3.12.13 --seed .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m jupyterlab
```

On macOS/Linux, use `.venv/bin/python` instead of `.\.venv\Scripts\python.exe`.
You do not need to activate the environment when using its Python path directly.
In VS Code, select this `.venv` environment as the interpreter and notebook kernel.
Open the notebooks in numerical order. Notebook 01 can run end to end to load
and explore development data and export the descriptive figures and summary.
Its executed outputs are saved for reading on GitHub. Notebook 02 explains and
demonstrates preprocessing in sections 1-2 and runs the model comparison in
sections 3-5, including validation metrics, error costs and figures. Section 6
reads the saved final test assessment without fitting or rerunning the test.

`requirements.in` lists the seven direct dependencies; `requirements.txt` pins the
resolved dependencies with platform markers. Install from `requirements.txt`
for repeatable setup. The environment itself stays local and is ignored by Git.
Only Windows has been verified locally; other platforms still need a setup check.
When deliberately updating packages, regenerate the pins and rerun the checks:

```powershell
uv pip compile requirements.in --python-version 3.12.13 --universal --no-annotate --output-file requirements.txt
```

To start the demo with the saved model, run from the project directory:

```powershell
.\.venv\Scripts\python.exe -m streamlit run demo/app.py --server.address 127.0.0.1 --browser.gatherUsageStats false
```

Read [the demo guide](demo/README.md) for the walkthrough and fictional profiles.
The app uses the frozen pipeline; it does not train or rerun the test assessment.

### Load data and verify the fixed split

From the project directory in PowerShell:

```powershell
.\.venv\Scripts\python.exe code/preprocessing.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

`data/split.json` is versioned and fixes row membership. The first command
validates and reuses it; it only creates a split when the file is absent.
Do not delete it to try alternative partitions. Notebook 01 calls
`load_partition()` with its development-only default. Test access is explicit
and reserved for final evaluation. See [the dataset guide](data/README.md).

Descriptive findings, validation metrics and final test results are kept distinct
in [`results/README.md`](results/README.md), together with reusable figures.

## Structure

| Directory | Purpose |
| --- | --- |
| `code/` | Shared Python functions for notebooks and the demo |
| `notebooks/` | Exploration, baseline, and model comparison with explanations |
| `tests/` | Source integrity, split isolation, and preprocessing checks |
| `data/` | Dataset and documentation of its source |
| `results/` | Generated metrics, models, and shared figures |
| `report/` | Writing workflow and Markdown skeleton for the final export |
| `presentation/` | Outline and link to the shared Canva presentation |
| `prompts/` | Documentation of generative AI use |
| `demo/` | Practical demo and walkthrough |
| `submission/` | Checklist for the MS Teams submission package |

Notebooks explain the analysis. Place shared logic in `code/` so that the demo
uses the same preprocessing as training. Loading and pipeline factories live in
`code/preprocessing.py`, the development comparison in `code/train.py`, and
metric/error-cost calculations in `code/evaluate.py`. Running `code/train.py`
regenerates validation CSV/JSON outputs; run notebook 02 for figures as well.
Neither comparison path evaluates the test set or saves a final fitted model.
The separate `code/final_model.py` assessment has already been run once; read
`results/final_test.json` or notebook 02 section 6 instead of repeating it.
`results/selected_pipeline.joblib` contains the complete development-trained
pipeline and explicit threshold used by the demo. Load only the trusted
project artifact, using the pinned environment; joblib files can execute code
when loaded. The assessment script refuses to overwrite existing final outputs.

## Collaboration

- Work directly on `main` by default, including technical changes. Check
  `git status` and update from the remote before starting with a clean working
  tree. Coordinate edits to shared files.
- Review changes locally and run the relevant checks before committing and
  pushing. Nicolai can inspect the local changes; if he asks to review first,
  wait for that review before publishing. Use a separate branch only when
  explicitly requested.
- Preserve existing team edits. If updates or conflicts are unclear, ask for
  help; never force-push or use a destructive reset to overwrite shared work.
- After each completed and checked work step, commit and push directly to `main`.
- Assign one owner per notebook where possible to reduce merge conflicts.
- Do not commit credentials or personal credit data.
- Write project documentation, comments, and notebook explanations in English.

| Area | Owner |
| --- | --- |
| Technical implementation (data, modeling, demo) | Nicolai |
| Business and literature | Jan |
| Results interpretation and economics | Philipp |
| Risks and implementation recommendations | Zosia |

Each presentation slide must name its actual responsible author(s) in the footer.
Record the presenter separately if different. Also document report-chapter
ownership and AI assistance. Roles and speaking sections are detailed in the
[presentation plan](presentation/outline.md).

## Writing the report

Use the shared Word document in Teams as the working version;
each person writes their sections and adds sources. Its Teams link still needs
to be recorded. Word files are kept in Teams rather than this repository.
Do not maintain a separate competing draft in `report/report.md`.
After the team review, Nicolai coordinates the Markdown and PDF exports.
See [the report skeleton and responsibilities](report/report.md).

## Course requirements

The team project includes the report (20 points), presentation (20), demo (10),
and an individual end-of-semester test (20). The separate case study accounts
for the remaining 30% of the final grade and is outside this credit-scoring project.

- Report as `.md` and PDF: business problem, existing solutions with references,
  a generative AI experiment, and empirical analysis covering goals, assumptions,
  results, and interpretation.
- Presentation: 20-25 minutes; business problem, method, data, results,
  implementation costs, ethical/legal/social risks, and lessons learned.
- Demo: 5-10 minutes; explain functionality, prompt/agent design, output, and limitations.
- Upload all project files to MS Teams by the presentation day in a folder named
  `YYYYMMDD_Topic`. According to the Grading Regulations, late submission costs
  50% of the points.

Presentation date and final topic name: **TBD**.
Full submission checklist: `submission/README.md`.
