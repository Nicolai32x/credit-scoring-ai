# Project plan

Updated on **20 October 2026** with the agreed roles and writing workflow.
The kickoff agenda is retained below for reference; no meeting outcomes or
deadlines have been recorded. The Python environment, named data loader and
fixed development/test split are ready. Development-only exploration is complete
in notebook 01. Preprocessing factories and a single-fold demonstration are ready
in notebook 02, along with the first fixed-configuration five-fold model
comparison. Logistic regression with threshold 0.5 was frozen, refitted on the
800 development cases, and assessed once on the 200 test cases. The saved
pipeline is ready and connected to the local seven-input Streamlit app. Team
rehearsal and a second-machine check are still pending.

## What we want to build

**Research question:** How well can a simple machine learning model classify
credit risk using a small set of applicant and loan characteristics?

Use Statlog (German Credit Data) as a historical teaching dataset. The planned
Streamlit demo will take seven inputs and display a predicted risk class.
It will illustrate the model, not make real lending decisions.

Read [the dataset guide](data/README.md) and [the demo sketch](demo/README.md).
Data loading, target mapping and the fixed split are implemented. Feature
encoding/scaling and a first model comparison are implemented. Descriptive
statistics, plots and validation metrics use development data only. A separate
final test assessment is complete and the Streamlit demo is implemented locally.

## Planned experiment

| Step | Plan |
| --- | --- |
| Inputs | Seven documented features, identical in training and the demo |
| Target | Implemented: original label 1 maps to 0 (good); 2 maps to 1 (bad) |
| Test set | Reserved: 20% (200 cases), stratified by target, seed 42; membership in `data/split.json` |
| Development set | Reserved: 80% (800 cases) for training and validation |
| Validation | Five stratified, shuffled folds inside development data, seed 42 |
| Reference | A majority-class predictor to show whether ML adds value |
| Models | Logistic regression and random forest, with a small tuning budget |
| Selection | Provisional primary metric: balanced accuracy; also examine bad-risk recall and error costs |
| Final assessment | Freeze model, features, preprocessing, and threshold; then evaluate once on the test set |

In each validation round, approximately 640 cases train the model and 160
validate it. Refit the chosen pipeline on all 800 development cases before
the final test. The 800/200 allocation is fixed. Notebook 02 demonstrates
preprocessing on the first development fold and then compares all three
candidates across all five folds using fresh pipelines.

The first comparison fixes class weighting to `balanced` for both ML models,
logistic regression C=1 and a forest with 300 trees and minimum leaf size 5.
The score threshold is 0.5; no parameter or threshold search has been performed.
Logistic regression leads provisionally on balanced accuracy (0.709 versus
0.702 for the forest), but the small difference does not establish superiority.
See [validation results and limitations](results/README.md). Review this simple
comparison informed the frozen decision: retain logistic regression and the
original threshold 0.5 without further tuning. The decision was committed before
the one-time test assessment. No model or threshold changes follow test results.

Final test: accuracy 0.730, balanced accuracy 0.740, bad-risk recall 0.767 and
ROC-AUC 0.810. The model detects 46/60 bad risks but falsely flags 40/140 good
risks. This is a historical teaching result, not lending approval. The saved
pipeline remains fitted on development cases only and will be reused by the demo.

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

1. **Understand the data:** review the feature definitions and limitations,
   use the recorded package versions, and create the untouched test split before exploratory
   modeling. Explore the development data in notebook 01.
2. **Compare models:** implement preprocessing and shared functions in `code/`;
   compare the reference and two models in notebook 02 using validation only.
3. **Evaluate and demonstrate:** freeze the chosen approach, run the final test,
   and connect the same saved pipeline to the seven-field Streamlit form.
4. **Explain the outcome:** write the report in one shared Word document in
   Teams, complete the Canva slides, GenAI log, and demo rehearsal. After team
   review, export the report to Markdown and PDF. Use the
   [submission checklist](submission/README.md).

Roles are assigned below; task dates and reviewers still need agreement.
Prefer a small complete analysis
over adding more algorithms or application features.

## Kickoff agenda for 20 October 2026 (about 45 minutes)

| Topic | Minutes | Outcome |
| --- | --- | --- |
| Course requirements and project question | 5 | Shared understanding of the deliverables |
| Dataset and seven proposed inputs | 10 | Confirm the scope and discuss limitations |
| Training, validation, test, and demo | 10 | Agree on the experiment and output wording |
| GitHub access and setup needs | 10 | Everyone can access the files; identify who needs help |
| Responsibilities and next milestone | 10 | Owners, dates, and next meeting recorded |

Read this page before the discussion. GitHub and AI setup is optional; use the
[optional tutorial](OPTIONAL_TUTORIAL.md) if interested. Nicolai leads the
technical implementation. The shared Word document supports contributions
without requiring local development tools.

## Items still to agree or record

- Review the planned experiment and primary model-selection metric before implementation.
- Record the shared Word document link and choose reviewers for each area.
- Confirm presentation/demo time slots with the lecturer.
- Check the presentation date, topic approval, and any additional course rules.
- Agree on the first milestone date and next meeting time.

| Area | Suggested first task | Owner / reviewer | Due |
| --- | --- | --- | --- |
| Technical implementation | Data preparation, experiments, reproducible evaluation, and demo | Nicolai / reviewer TBD | TBD |
| Business and literature | Define the decision, existing solutions, references, and success criteria | Jan / reviewer TBD | TBD |
| Results and economics | Review outputs, interpret errors, and estimate costs with explicit assumptions | Philipp / reviewer TBD | TBD |
| Risks and implementation | Research risks, propose mitigations, and review demo scenarios/usability | Zosia / reviewer TBD | TBD |

These areas can overlap; each person should understand the overall analysis.
See the [presentation plan](presentation/outline.md) for proposed speaking
sections and contributions. The report headings and slide suggestions can be
adapted within each person's area while covering the course criteria.
One technical lead is compatible with
substantial non-coding contributions. Assign credit based on actual work,
record AI assistance, and distinguish content authors from presenters.
The proposed first milestone is a reproducible development-data exploration
and a baseline validation result, with the test data still unused.

## How we work

Write the report together in one shared Word document in Teams. Keep the Word
file there; the repository contains the workflow and final export skeleton.
Add references alongside claims and use comments for discussion. This is the
working version until the final team review; `report/report.md` is the export
skeleton, not a parallel draft. Nicolai coordinates the final Markdown/PDF
versions. Share the Word link with the team once the document is uploaded.

Use English in project files. Work directly on `main` by default for both
documentation and technical work. Start from the latest shared version, preserve
existing edits, and review and check changes locally before committing and
pushing each completed step. If Nicolai requests a local review first, wait for
it before publishing. Create a separate branch only when explicitly requested.
Coordinate notebook ownership and avoid editing the same notebook at the same
time. Never overwrite another member's work to resolve a conflict.
Record relevant AI prompts, outputs, corrections, and limitations in
[`prompts/log.md`](prompts/log.md). Everyone must be able to explain their work.
