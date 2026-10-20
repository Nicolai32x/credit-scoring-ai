# Generative AI log

Create an entry for each relevant generative AI experiment, including attempts
that did not produce the desired result. Do not include personal data or
credentials in prompts.

## Entry template

- Date and responsible author:
- Tool and model/version, where known:
- Purpose and context:
- Prompt (exact wording):

```text
Enter the actual prompt used here.
```

- Output (relevant excerpt or file reference):
- Your own review and corrections:
- Content adopted and its use in the project:
- Limitations, errors, and lessons learned:

This template is not yet a documented generative AI experiment.

## 2026-10-16: Kickoff preparation and presentation planning

- Requested by: Nicolai. Human review of the generated files: pending.
- Tool: AI coding assistant. Model/version: not recorded in this log.
- Request summary (English paraphrase, not a verbatim prompt): prepare the
  proposed Statlog dataset, document checks and the ML approach, sketch the
  demo, prepare the first meeting, and plan a course-aligned presentation with
  Nicolai leading technical implementation.
- Output: `PROJECT_PLAN.md`, dataset documentation, unchanged UCI source files,
  a demo sketch, and an expanded presentation outline; linked documentation
  updated. No model training or application implementation.
- Checks performed: downloaded data examined for structure, labels, duplicate
  records, missing tokens, ranges, and category codes; provenance and license
  checked against UCI. These checks do not establish predictive performance.
- Corrections and limitations: preserved historical currency and ambiguous
  category meanings; no invented predictions, probability claims, or completed
  team contributions. Technical ownership and presenter assignments remain
  proposals. Review methods, sources, and timing at the kickoff.
- Later action: retain the original conversation if an exact prompt transcript
  is needed; log actual coding experiments separately with their exact prompts,
  outputs, human review, and corrections.

## 2026-10-20: Repository consistency review

- Requested by: Nicolai. Request summary (English paraphrase): review the entire
  repository and update it to reflect the current project arrangements.
- Tool: AI coding assistant; model/version not recorded in this log.
- Changes: synchronized Jan, Nicolai, Philipp and Zosia's roles; recorded the
  shared Word writing workflow and Canva template; corrected outdated dataset
  and implementation-status descriptions. The Word template was prepared and
  simplified earlier following Nicolai's feedback; it is not a completed report.
  At Nicolai's request, Word files are kept in Teams and the local template was
  removed from the repository workspace before publication.
- Scope: documentation and placeholder descriptions only. Original data stays
  unchanged; no preprocessing, training, test split or Streamlit implementation.
- Checks: data integrity, document links, notebook structure, Python syntax and
  agreement between the role and workflow descriptions.
- Pending: team review of these updates, the actual shared Word link, dates and
  eventual empirical results. Preserve the conversation for exact user prompts;
  this entry is a summary, not a verbatim transcript.

## 2026-10-20: Python environment setup

- Requested by: Nicolai, approving step 1 of the technical work. Request summary
  (English paraphrase): prepare the Python environment before working with data.
- Tool: AI coding assistant; model/version not recorded in this log.
- Work: reused the existing uv-managed Python 3.12.13 installation, created the
  local `.venv`, and resolved the six direct dependencies from `requirements.in`
  into pinned `requirements.txt` entries with platform markers. Python version
  recorded in `.python-version`; setup instructions updated.
- Checks: imported the analysis libraries, rendered a small in-memory figure,
  validated the empty notebook templates, and checked package compatibility.
  A temporary Jupyter kernel executed a simple calculation using the project
  interpreter. No dataset was loaded or split and no model was fitted.
- Limitation: the environment has been exercised on Windows only. Package pins
  contain platform markers, but macOS/Linux setup still needs verification.
- Human review of this setup is pending. This entry summarizes the work rather
  than reproducing the exact user prompts.

## 2026-10-20: Named data loading and fixed holdout

- Requested by: Nicolai, continuing the agreed work one step at a time. This
  entry is an English summary, not a verbatim prompt transcript.
- Tool: AI coding assistant; model/version not recorded here.
- Output: shared loader with English column names, seven selected inputs, and
  `bad_risk` mapping (original 1 to 0, original 2 to 1). `data/split.json`
  reserves 800 development rows and 200 test rows using seed 42 and stratification.
- Safeguards: source checksum verified; row IDs are source positions, not model
  inputs; existing manifests are validated and never overwritten by the loader.
  The notebook defaults to development data. Explicit test access is reserved
  for final evaluation and is not a technical access restriction.
- Verification: tests cover label/feature mapping, split isolation and balance,
  reproducibility, source changes, and invalid manifests. Notebook loading is
  checked from both supported working directories.
- Limits: no feature encoding/scaling, predictive exploration, cross-validation,
  model fitting or performance evaluation in this step. Test class counts are
  used only to verify stratification. Human review of these changes is pending.

## 2026-10-20: Development data exploration

- Requested by: Nicolai, approving the next notebook-analysis step. This is an
  English task summary, not a verbatim prompt transcript.
- Tool: AI coding assistant; model/version not recorded here.
- Work: extended notebook 01 with feature explanations, quality checks, class
  balance, numeric distributions, category counts, and descriptive label shares
  with group sizes. Exported four figures and a JSON summary with provenance.
- Existing local changes: Nicolai had executed the original loading cell without
  changing its source. Its code was preserved and rerun with the full notebook.
- Checks: all cells executed, figures inspected, descriptive summary checked
  against development-only calculations, original source/split kept unchanged.
- Interpretation: sparse groups and combined source meanings require caution;
  no rows or inputs were removed and no causal, fairness, or performance claims
  are inferred. Demo range guidance now uses development-data support.
- Limits: no model fitting, feature transformation, or test-set exploration.
  Human review of the new explanations and figures is pending.

## 2026-10-20: Fold-specific preprocessing

- Requested by: Nicolai, continuing after review of the exploratory notebook.
  This entry is an English summary, not a verbatim prompt transcript.
- Tool: AI coding assistant; model/version not recorded here.
- Work: added fresh preprocessing and model-pipeline factories. Five categorical
  inputs use one-hot encoding; two numeric inputs are standardized for logistic
  regression and left unscaled for random forest. Source category A65 is kept.
  Unseen categories produce a zero block and need explanation in the future demo.
- Notebook 02: fit preprocessing on 640 training cases from the first development
  fold, then transform 160 validation cases without refitting. Later sections
  remain placeholders. This example is not reused as a globally fitted transform.
- Checks: synthetic fixtures verify training-only statistics, stable handling of
  unseen categories, feature selection, serialization, and per-fold fitting.
  A dummy classifier is fitted only to invented test fixtures to check pipeline
  behavior; no credit-risk classifier is trained on the project dataset.
- Limits: no predictive performance, model selection, or test-partition analysis.
  Original source files, split membership, and exploratory outputs are unchanged.
  Human review of the new notebook explanations is pending.
