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

The template alone is not an experiment. The completed explanation experiment
is documented in the 20 October entry below and `results/genai/README.md`.

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

## 2026-10-20: First development-only model comparison

- Requested by: Nicolai, continuing after the preprocessing step. This is an
  English task summary, not a verbatim prompt transcript.
- Tool: AI coding assistant; model/version not recorded here.
- Work: implemented shared comparison and metric functions; extended notebook 02
  with majority baseline, logistic regression and random forest. Fixed settings
  were documented before inspecting results: balanced weights for both ML models,
  logistic C=1, forest 300 trees/minimum leaf size 5, score threshold 0.5.
- Evaluation: same five stratified development folds for every model; fresh
  pipelines fit on 640 training cases and predict 160 validation cases. Every
  development case has one out-of-fold prediction per model. No parameter search,
  threshold tuning, test evaluation or final fitted-pipeline export was performed.
- Outputs: fold metrics, mean/sample-standard-deviation summary, out-of-fold
  predictions, JSON provenance, two figures and executed notebook explanations.
- Findings: logistic regression leads narrowly on mean balanced accuracy (0.709
  versus forest 0.702), while forest has slightly higher mean ROC-AUC. The
  baseline's 70% accuracy hides zero bad-risk recall. Both ML models falsely
  reject many good risks; no reliable superiority or bank-profit claim is made.
- Checks: 20 tests cover source/split integrity, preprocessing, error-cost
  direction and validation coverage/isolation using invented fixtures. Notebook
  execution and figures were checked. Final decision and human review are pending.

## 2026-10-20: Frozen model, final assessment and saved pipeline

- Requested by: Nicolai, continuing after the model comparison. This is an
  English summary, not a verbatim prompt transcript.
- Tool: AI coding assistant; model/version not recorded here.
- Decision: retain logistic regression with balanced class weights, C=1 and the
  original score threshold 0.5. It leads narrowly on validation balanced accuracy
  and illustrative costs and is simpler than the forest. No further parameter
  or threshold search was conducted. False rejections remain an accepted
  limitation of this teaching example, not an operational banking policy.
- Sequence: recorded `model_decision.json` and committed/pushed it as `d29c258`
  before opening the test partition for prediction. Then fitted the complete
  chosen pipeline on 800 development cases and assessed 200 test cases once.
  The comparison's source files and outputs were preserved.
- Outputs: saved pipeline/threshold bundle, final prediction CSV, test report
  with provenance, and a confusion figure. Notebook 02's final section only
  reads these outputs; it does not rerun final training or test prediction.
- Findings: test accuracy 0.730, balanced accuracy 0.740 and bad-risk recall
  46/60 (0.767), with 14 false approvals and 40 false rejections. Illustrative
  cost 110 units versus 300 for the always-good reference; not currency/profit.
- Checks: 23 tests passed, including explicit threshold use and refusal of
  repeated final assessment before any data loading. The saved artifact and
  report are checked against the frozen decision. No model or threshold changes
  are made after seeing the test results. Human review and Streamlit work remain.

## 2026-10-20: Seven-input Streamlit demo

- Requested by: Nicolai, continuing after discussing the moderate model results.
  This is an English summary, not a verbatim prompt transcript.
- Tool: AI coding assistant; model/version not recorded here.
- Work: connected an English Streamlit form to the saved development-trained
  pipeline and explicit frozen threshold. Two numeric inputs retain historical
  DM/month units and development-data ranges; five dropdowns preserve the source
  category meanings and offer only categories learned by the saved encoder.
- Output: a predicted risk class, an expandable submitted-input summary, and a
  reliability explanation showing 46/60 bad risks detected and 40/140 good risks
  falsely flagged. No default-probability percentage or lending approval is shown.
- Dependencies: added Streamlit and pinned its dependencies. Existing model and
  analysis package versions are retained; Pillow changed from 13.0.0 to 12.3.0
  for Streamlit compatibility. Original requirements remain available in Git.
- Checks: 24 tests passed, including the real form with three fictional profiles,
  comparison with the saved helper, and guards prohibiting fitting or partition
  loading during the app check. Local startup/health and package compatibility
  were verified; frozen model/data/test outputs remain unchanged.
- Limits: no external AI API or generative AI experiment is implemented here.
  Frozen model, threshold and final assessment are unchanged. Team rehearsal,
  second-machine testing and human review remain pending.

## 2026-10-20: OpenAI result-explanation experiment

- Requested by: Nicolai, approving the two-prompt experiment and Streamlit
  integration. This is a task summary; exact experimental prompts are preserved
  separately from the conversational instructions.
- Generation model: `gpt-5.4-mini-2026-03-17`, OpenAI Responses API, SDK 3.35.1.
  Evaluation and implementation: AI coding assistant, with human review pending.
- Protocol: simple versus structured prompt, three independent responses each,
  paired alternating order, same aggregate results and audience/word instruction;
  temperature 0.7, reasoning none, maximum 800 output tokens, no tools/retries.
  Prompt files: `explanation_simple.txt` and `explanation_structured.txt`. Full
  supplied prompts/settings and the rubric were written before generation.
- Execution history: first attempt failed authentication because the management
  identifier was used rather than the secret key. The failure and its protocol
  remain in `results/genai/`. After the user replaced the local key, all six
  requests in `results/genai/run_02/` completed. No successful answers were dropped.
- Outputs: `results/genai/outputs.md` contains all six unedited answers; raw
  response IDs, timestamps, usage and report checksum are in `attempts.jsonl`.
  The assessment stores scores, evidence excerpts and qualitative cautions.
- Findings: all responses used correct numbers and described both error types.
  Simple responses omitted the 60/140 class denominators; structured responses
  included them. One structured response exceeded 180 words (193 words).
  Mean rubric scores: 7.00/8 versus 7.67/8. Differences are descriptive, not
  statistically significant evidence or proof of general superiority.
- Corrections and limits: simple responses use approval/rejection language
  despite the app predicting only classes. Broad phrases about usefulness and
  error priorities also need caution. The fixed rubric does not capture every
  framing problem. Raw outputs remain unedited. Assessment is AI-assisted,
  neither independent nor blinded; Nicolai's review is still pending.
- Integration: optional live structured-prompt explanation of aggregate results,
  plus clearly labeled recorded examples from the first completed repetition
  of each variant. No applicant inputs are sent. The ML pipeline/test is unchanged.
- Usage: 3,213 input and 1,454 output tokens; estimated standard cost $0.00895
  at the published rates checked on 20 October 2026, not an account billing total.
- Report: draft chapter 3 with APA-style references is in `prompts/experiment.md`
  for transfer to the shared Word document. No competing final report was created.
- Security: key remains local in the ignored secrets file and is never written
  to prompts, responses or Git. Provider error bodies are not logged or displayed.
- Verification: all 31 tests passed, including offline recorded examples,
  explicit live-call behavior and persistence of the original ML result during
  AI interaction. Raw outputs, rubric evidence, usage and source checksums were
  checked. No additional paid calls were made by automated tests.

## 2026-10-20: Explanation of the submitted fictional profile

- Requested by: Nicolai, asking for an explanation of the current input/result.
- Work: added a separate profile explanation button. It uses the last submitted
  form snapshot and the frozen pipeline's actual coefficient contributions,
  centered on mean transformed development inputs. Seven grouped contributions
  plus the reference exactly reconstruct the decision score. No model fitting,
  threshold changes or new test predictions were performed.
- Data flow: the app explicitly states that this optional button sends the
  fictional inputs, class, descriptions and contributions to OpenAI. The existing
  aggregate explanation still sends no applicant inputs. Do not use real personal
  data. Profile explanations clear when a new prediction is submitted.
- Verification: contribution reconstruction, coefficient signs, reference checks,
  request context and submitted-snapshot behavior were checked offline. Two real
  API integration checks used the existing fictional scenario A. The first used
  technical names/raw values and said two minor features while listing three;
  the refined prompt requests friendly labels, 2-3 features and no raw logits.
  Both raw responses remain in `results/genai/`, outside the original experiment.
- Limits: these are relative contributions to a model logit, not causal effects,
  calibrated default probabilities or lending recommendations. The reference is
  an average transformed vector, not a real or typical applicant. A successful
  example does not prove every future explanation will follow instructions.
- Report: the chapter-3 draft in `prompts/experiment.md` includes a separate
  extension paragraph; existing Word text saying the app never sends profile
  inputs needs qualification for this optional feature.
- Checks: all 36 tests passed. The local server is healthy, both fictional
  integration outputs were checked against the supplied contribution directions,
  and the frozen model, final test and original experiment remain unchanged.

## 2026-10-20: Fix stale Streamlit explanation imports

- Trigger: Nicolai reported that the profile explanation was unavailable, while
  the aggregate explanation worked. Browser inspection confirmed a stale imported
  `genai` module: the running process lacked the updated context-aware function
  and could not import a newly added error helper despite its presence on disk.
- Fix: restarted the owned local server and added `demo/run.py`. The launcher
  places the shared `code/` folder on `PYTHONPATH` before Streamlit starts so its
  imported modules are watched. Startup instructions now use this launcher.
- Errors: added fixed, actionable messages for stale code, authentication,
  permission, request limits, billing limits, timeouts and connection failures.
  Logs include only exception class names; provider bodies and keys remain hidden.
- Verification: 38 tests passed, including launcher-path and safe-message
  regressions. Restored the fictional browser profile and verified a successful
  live profile explanation in the actual running app. This troubleshooting call
  is not part of the completed six-response experiment. The original model,
  threshold and evaluation were not changed.

## 2026-10-20: Simplify the team handover

- Requested by: Nicolai, asking to review, update and remove unnecessary material
  so teammates can understand the technical work without navigating many files.
- Work: made the root README the single project overview and reading route;
  put final test results/errors/cost assumptions first in `results/README.md`;
  simplified the presentation outline, demo instructions and report section map.
  Technical details are optional expandable sections. All files remain English.
- Removed: redundant `PROJECT_PLAN.md`, duplicate `prompts/experiment.md` and the
  unused figure-folder marker. Current roles, next steps and course requirements
  were consolidated into the existing overview, outline and submission checklist.
  The unique chapter-3 reference draft was preserved in an expandable section of
  `results/genai/README.md`; the shared Word document remains the working report.
- Evidence: original data, fixed split, executable code/tests, saved model,
  metrics/predictions, notebook outputs, exact prompts, raw API attempts and
  assessments remain at their original paths. Historical entries in this log
  retain earlier filenames as a record, not as current navigation instructions.
- Remaining: GenAI human sign-off, second-machine testing, shared report/slides,
  rehearsal and final exports still require team checks. No review or completion
  by another team member was inferred.
- Verification: all local Markdown links/detail blocks checked; 49 implementation
  and evidence files confirmed unchanged, including the exact prompt texts.
  All 38 tests passed without paid API calls. The first test import hit a local
  OpenBLAS memory-allocation error; the successful run limited BLAS/OMP threads
  to one for that process, without changing packages or model settings.

## 2026-10-24: Expand the aggregate GenAI prompt comparison

- Requested by: Nicolai, approving 30 new responses after discussing the limits
  of the six-response pilot while preparing his presentation slides.
- Design: unchanged simple/structured prompts, three scenarios and five
  repetitions per cell. One scenario uses the saved actual test summary; two use
  explicitly synthetic confusion counts. No ML fit, threshold change or new test
  evaluation. The pilot and all earlier evidence remain unchanged and separate.
- Pre-registration: `run_03/protocol.json` and the tested runner were committed as
  `e4dec48` before the first request. The protocol fixes contexts, criteria,
  source fingerprints and shuffled pair order. All 30 requests completed; no
  retries, discarded answers or replacements. Only aggregate facts were sent.
- Assessment: deterministic length checks and AI-assisted reading of every raw
  output; not independent or blinded. Human sign-off remains pending. Explicit
  class totals and linked counts in different sentences qualify as complete.
  No numerical error was identified in either prompt. Complete counts/denominators:
  simple 10/15, structured 15/15. Both errors: 15/15 each. Clear unsupported-claim
  flags: 5 simple, 0 structured, with borderline cases documented. Word target:
  simple 15/15, structured 12/15. No composite score or significance claim.
- Cautions: prompt compliance is part of the rubric; five repetitions do not
  create five independent task scenarios. Invented examples are not credit-model
  results. Both variants sometimes imply approval/rejection; some structured
  answers echo historical wording for synthetic cases. All raw text is retained.
- Usage: 15,915 input and 6,845 output tokens; estimated standard cost $0.04274,
  not an account billing statement. API credentials stay local and ignored.
- Handover: updated existing overview, result summary, optional chapter 3 draft,
  report map and the approved four-slide Nicolai section. Streamlit now offers
  actual/synthetic recorded scenarios, defaults to actual results and displays
  the first completed answer per cell rather than choosing by score.
- Checks: offline tests cover synthetic arithmetic, balanced/frozen protocol,
  exact context routing, failure retention, overwrite protection and saved
  assessment provenance/summary counts; Streamlit checks both actual and
  synthetic recorded answers without API calls.
  All 44 offline tests passed. Final checks found no broken local documentation
  links or credential patterns in the new evidence; protected ML artifacts,
  datasets, exact prompts and original pilot records were confirmed unchanged.
