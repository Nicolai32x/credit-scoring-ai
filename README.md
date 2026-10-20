# Credit Scoring AI

Team project for **Introduction to AI in Business**. We investigate how a
credit-scoring model can support a business decision and assess its results,
costs, and limitations. We will use Statlog (German Credit Data) and a small
Streamlit demo with seven inputs.

## Current status and project documents

The original dataset, its structural review, project plan, and presentation
outline are ready. A local Python environment is set up and the package
versions are recorded. The report is written in Word in Teams, and a Canva
presentation template has been prepared. No preprocessing pipeline, data splits, trained models,
evaluation results, or working Streamlit application exist yet.

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
Open the notebooks in numerical order. They currently contain outlines only.

`requirements.in` lists the six direct dependencies; `requirements.txt` pins the
resolved dependencies with platform markers. Install from `requirements.txt`
for repeatable setup. The environment itself stays local and is ignored by Git.
Only Windows has been verified locally; other platforms still need a setup check.
When deliberately updating packages, regenerate the pins and rerun the checks:

```powershell
uv pip compile requirements.in --python-version 3.12.13 --universal --no-annotate --output-file requirements.txt
```

Streamlit is planned and is not installed by the current requirements; add it
when implementing the demo. The setup above does not create a working model.

## Structure

| Directory | Purpose |
| --- | --- |
| `code/` | Shared Python functions for notebooks and the demo |
| `notebooks/` | Exploration, baseline, and model comparison with explanations |
| `data/` | Dataset and documentation of its source |
| `results/` | Generated metrics, models, and shared figures |
| `report/` | Writing workflow and Markdown skeleton for the final export |
| `presentation/` | Outline and link to the shared Canva presentation |
| `prompts/` | Documentation of generative AI use |
| `demo/` | Practical demo and walkthrough |
| `submission/` | Checklist for the MS Teams submission package |

Notebooks explain the analysis. Place shared logic in `code/` so that the demo
uses the same preprocessing as training. The Python modules initially contain
only descriptions of their intended purpose.

## Collaboration

- Small, easy-to-review documentation changes can go directly to `main`.
  Check `git status` and pull the latest `main` before starting with a clean
  working tree. Coordinate edits to shared files and review the diff before committing.
- Use a task branch for code, data processing, models, dependencies, or larger
  or uncertain changes, including broad AI-generated edits. Review and validate
  them before merging; use a pull request when team review is useful.
- Preserve existing team edits. If updates or conflicts are unclear, ask for
  help; never force-push or use a destructive reset to overwrite shared work.
- After each completed and checked work step, commit and push the checkpoint
  to its current branch. Pushing a task branch does not merge it into `main`.
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
