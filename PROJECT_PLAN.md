# Team kickoff and project plan

Prepared for **Tuesday, 20 October 2026**. Meeting time and location: TBD.
This is a proposal for the team to discuss, not a record of a team decision.

## What we want to build

**Research question:** How well can a simple machine learning model classify
credit risk using a small set of applicant and loan characteristics?

Use Statlog (German Credit Data) as a historical teaching dataset. The planned
Streamlit demo will take seven inputs and display a predicted risk class.
It will illustrate the model, not make real lending decisions.

Read [the dataset guide](data/README.md) and [the demo sketch](demo/README.md).
Models, preprocessing, data splits, and the application have not been implemented.
The dataset review is preparation, not an evaluation of predictive performance.

## Proposed experiment

| Step | Plan |
| --- | --- |
| Inputs | Seven documented features, identical in training and the demo |
| Target | Original label 1 = good risk, 2 = bad risk; later map to 0 and 1 respectively |
| Test set | Reserve 20% (200 cases) once, stratified by target, with random seed 42 |
| Development set | Use the other 80% (800 cases) for training and validation |
| Validation | Five stratified, shuffled folds inside development data, seed 42 |
| Reference | A majority-class predictor to show whether ML adds value |
| Models | Logistic regression and random forest, with a small tuning budget |
| Selection | Provisional primary metric: balanced accuracy; also examine bad-risk recall and error costs |
| Final assessment | Freeze model, features, preprocessing, and threshold; then evaluate once on the test set |

In each validation round, approximately 640 cases train the model and 160
validate it. Refit the chosen pipeline on all 800 development cases before
the final test. These are planned sizes; no split has been created yet.

Keep preprocessing inside each training fold: encode categories, scale numeric
inputs for logistic regression, and fit any learned transformations without
using validation/test cases. Do not tune features or settings based on test
results. If identical applicant records are found, keep them in the same split.
Different people can share the seven selected values; do not remove such cases
just because their reduced feature vectors match.

Report accuracy, balanced accuracy, bad-risk precision/recall/F1, ROC-AUC, and a
confusion matrix, with validation mean and variation. Explain false approvals
(bad risk predicted good) and false rejections (good risk predicted bad).
As an additional business illustration, use the dataset's 5:1 error-cost matrix
as a historical assumption, not actual monetary losses. No minimum performance
is promised. A weak model is still a valid finding if evaluated honestly.

Source for validation and preprocessing:
[scikit-learn cross-validation guide](https://scikit-learn.org/stable/modules/cross_validation.html).

## Delivery stages after the meeting

1. **Understand the data:** agree on the feature definitions, document limitations,
   pin package versions, and create the untouched test split before exploratory
   modeling. Explore the development data in notebook 01.
2. **Compare models:** implement preprocessing and shared functions in `code/`;
   compare the reference and two models in notebook 02 using validation only.
3. **Evaluate and demonstrate:** freeze the chosen approach, run the final test,
   and connect the same saved pipeline to the seven-field Streamlit form.
4. **Explain the outcome:** finish the Markdown/PDF report, slides, GenAI log,
   and demo rehearsal. Use the [submission checklist](submission/README.md).

Dates and owners are to be agreed by the team. Prefer a small complete analysis
over adding more algorithms or application features.

## First meeting agenda (about 45 minutes)

| Topic | Minutes | Outcome |
| --- | --- | --- |
| Course requirements and project question | 5 | Shared understanding of the deliverables |
| Dataset and seven proposed inputs | 10 | Confirm the scope and discuss limitations |
| Training, validation, test, and demo | 10 | Agree on the experiment and output wording |
| GitHub access and setup needs | 10 | Everyone can access the files; identify who needs help |
| Responsibilities and next milestone | 10 | Owners, dates, and next meeting recorded |

Before the meeting, create a GitHub account if needed, accept the repository
invitation, and read this page. No software installation is needed for the
discussion. Nicolai and Philipp have experience with similar projects and can
help with setup. Nicolai is proposed as technical lead and Philipp for results
and economics; confirm roles and review responsibilities together.

## Decisions to make together

- Confirm Statlog and the seven-input scope, including historical DM units.
- Confirm the split, metrics, models, and the primary model-selection metric.
- Confirm Streamlit as the demo tool; keep output to a risk class initially.
- Assign owners and a reviewer/buddy for each area below.
- Check the presentation date, topic approval, and any additional course rules.
- Agree on the first milestone date and next meeting time.

| Area | Suggested first task | Owner / reviewer | Due |
| --- | --- | --- | --- |
| Technical implementation | Data preparation, experiments, reproducible evaluation, and demo | Nicolai (proposed) / reviewer TBD | TBD |
| Business and literature | Define the decision, existing solutions, references, and success criteria | TBD | TBD |
| Results and economics | Review outputs, interpret errors, and estimate costs with explicit assumptions | Philipp (proposed) / reviewer TBD | TBD |
| Risks and implementation | Research risks, propose mitigations, and review demo scenarios/usability | TBD | TBD |

These areas can overlap; each person should understand the overall analysis.
See the [presentation plan](presentation/outline.md) for proposed speaking
sections and concrete contributions. One technical lead is compatible with
substantial non-coding contributions. Assign credit based on actual work,
record AI assistance, and distinguish content authors from presenters.
The proposed first milestone is a reproducible development-data exploration
and a baseline validation result, with the test data still unused.

## How we work

Use English in project files. Work on task branches and review changes before
merging. Coordinate notebook ownership and avoid editing the same notebook at
the same time. Never overwrite another member's work to resolve a conflict.
Record relevant AI prompts, outputs, corrections, and limitations in
[`prompts/log.md`](prompts/log.md). Everyone must be able to explain their work.
