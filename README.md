# Credit Scoring AI

Team project for **Introduction to AI in Business**. We investigate how a
credit-scoring model can support a business decision and assess its results,
costs, and limitations. Statlog (German Credit Data) is the proposed dataset;
the team will confirm the plan at the kickoff. No models have been trained.

## First team meeting

Start with [the project plan and meeting agenda](PROJECT_PLAN.md) for Tuesday,
20 October 2026 (time/location TBD). The preparation includes a
[dataset guide](data/README.md) and a [seven-input demo sketch](demo/README.md).
No installation is required to read these files or join the discussion.

## Getting started

Questions about the project or your role? Upload `README.md`, `PROJECT_PLAN.md`,
and `presentation/outline.md` to your usual AI chat and ask it to explain them
in simple terms. Add other relevant files when needed. You do not need to
install anything for this; check its answers against the files and ask the team
if something is unclear.

If you want to try GitHub edits or use an AI assistant with the project, see the
[optional GitHub and AI tutorial](OPTIONAL_TUTORIAL.md). It is not a prerequisite
for contributing; you can also share your work with the team and ask for help.

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
| Technical implementation (data, modeling, demo) | Nicolai, proposed |
| Business and literature | TBD |
| Results interpretation and economics | Philipp, proposed |
| Risks and implementation recommendations | TBD |

Each presentation slide must name its actual responsible author(s) in the footer.
Record the presenter separately if different. Also document report-chapter
ownership and AI assistance. Proposed roles are detailed in the
[presentation plan](presentation/outline.md) and will be confirmed together.

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
