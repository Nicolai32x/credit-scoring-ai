# Credit Scoring AI

Team project for **Introduction to AI in Business**. We investigate how a
credit-scoring model can support a business decision and assess its results,
costs, and limitations. The dataset and models have not yet been selected.

## Getting started

Use Python 3.11 or later. Run these commands from the project directory in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m jupyterlab
```

Open the notebooks in numerical order. They currently contain outlines only.
Record the package versions in `requirements.txt` before starting shared experiments.

## Structure

| Directory | Purpose |
| --- | --- |
| `code/` | Shared Python functions for notebooks and the demo |
| `notebooks/` | Exploration, baseline, and model comparison with explanations |
| `data/` | Dataset and documentation of its source |
| `results/` | Generated metrics, models, and shared figures |
| `report/` | Report in Markdown and, later, PDF format |
| `presentation/` | Presentation outline and, later, slides |
| `prompts/` | Documentation of generative AI use |
| `demo/` | Practical demo and walkthrough |
| `submission/` | Checklist for the MS Teams submission package |

Notebooks explain the analysis. Place shared logic in `code/` so that the demo
uses the same preprocessing as training. The Python modules initially contain
only descriptions of their intended purpose.

## Collaboration

- Work on a separate branch for each task, e.g. `codex/project-structure`.
- Check `git status` before making changes and preserve existing team edits.
- Review changes together through pull requests; avoid force-pushes and
  destructive resets on shared branches.
- Assign one owner per notebook where possible to reduce merge conflicts.
- Do not commit credentials or personal credit data.
- Write project documentation, comments, and notebook explanations in English.

| Area | Owner |
| --- | --- |
| Data and exploration | TBD |
| Modeling and evaluation | TBD |
| Report and literature | TBD |
| Presentation and demo | TBD |

Each presentation slide must name its responsible author in the footer.
Also document ownership of report chapters.

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
