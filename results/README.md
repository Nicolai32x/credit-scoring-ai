# Results — what the team needs

**Use this page for the report and presentation.** Everything is saved and can be
read on GitHub without running code. The final model is logistic regression.
The dataset is historical; Good/Bad risk are dataset labels, not credit decisions
or calibrated probabilities of future default.

## 1. Final test: the main result

The model was fitted on 800 development cases, after selecting it through
validation. Model settings and threshold 0.5 were fixed **before** testing on
200 separate cases. The test was evaluated once; the forest was not subsequently
tested to choose a different winner.

| Measure | Selected model | Always predict Good risk |
| --- | --- | --- |
| Accuracy: all correct classifications | **73.0%** | 70.0% |
| Balanced accuracy: average recall of both classes | **74.0%** | 50.0% |
| Bad-risk recall: bad cases detected | **46/60 = 76.7%** | 0/60 = 0% |
| Bad-risk precision: flagged cases actually labeled bad | **46/86 = 53.5%** | Not applicable: no cases flagged |
| Bad-risk F1 | 0.630 | 0.000 |
| ROC-AUC | 0.810 | 0.500 |

The stored metric implementation reports zero precision/F1 when there are no
bad predictions. The plain-language interpretation of baseline precision is
"not applicable", rather than evidence from any flagged cases.

### The errors matter more than the headline

| Actual label | Predicted Good | Predicted Bad |
| --- | --- | --- |
| 140 Good risks | 100 correct | **40 false rejections** |
| 60 Bad risks | **14 false approvals** | 46 correct |

Here, "approval" and "rejection" name hypothetical error types. The app does
not make lending decisions. It detects most bad cases, but wrongly flags
**40/140 good cases (28.6%)**. Only about half its Bad predictions are correct.
A similar accuracy to the baseline therefore hides a very different error tradeoff.

[Download the final test confusion matrix](figures/final_test_confusion_matrix.png).

### Cost illustration for Philipp

The source assigns **5 units per false approval**, **1 per false rejection**,
and zero for a correct prediction:

- Selected model: `5 x 14 + 40 = 110` units, or **0.55 per case**.
- Always-Good reference: `5 x 60 + 0 = 300` units, or **1.50 per case**.

This comparison uses assumed historical cost units, **not euros, actual bank
losses, demonstrated savings or profit**. Operating costs/benefits need separate
assumptions and sources.

## 2. Why logistic regression?

These are **validation means on the 800 development cases**, not final test scores.
All models used the same five folds, each with 640 training and 160 validation
cases. Preprocessing was learned in the training fold only.

| Candidate | Accuracy | Balanced accuracy | Bad-risk recall | ROC-AUC |
| --- | --- | --- | --- | --- |
| Always-Good baseline | 70.0% | 50.0% | 0.0% | 0.500 |
| Logistic regression | 70.8% | **70.9%** | **71.3%** | 0.766 |
| Random forest | 70.3% | 70.2% | 70.0% | **0.778** |

Logistic regression led narrowly on the primary balanced-accuracy metric and
illustrative cost, and is simpler. The forest ranked cases slightly better by
ROC-AUC. The small differences do not establish reliable superiority.
There was no parameter or threshold search. The model and 0.5 threshold stayed
unchanged after the test result; no further tuning uses that test set.

[Validation comparison figure](figures/cv_model_comparison.png) shows fold means
and standard deviations. Those deviations are **not confidence intervals**.
[Validation confusion matrices](figures/cv_confusion_matrices.png) pool the
out-of-fold predictions and must not be labeled as test results.

## 3. GenAI and the demo

After a six-response pilot, Nicolai ran a separate comparison: three scenarios,
two unchanged prompts and five repetitions, giving **30 new responses**.
Only one scenario uses actual project results; two use clearly labelled invented
counts to test different error trade-offs. They are not new ML test results.
The AI-assisted review found complete class denominators/counts in 10/15 simple
and 15/15 structured responses. Neither version had an identified numerical
error; both explained both errors in all responses. Five simple responses were
flagged for clear overreach under the rubric. All simple responses met the word
limit, compared with 12/15 structured responses. This small, non-independent
comparison does not prove general superiority. **Human review is still pending.**

Read [the GenAI summary and actual answers](genai/README.md) for Nicolai's section.
The [demo guide](../demo/README.md) explains the three separate features:
ML risk prediction, AI explanation of overall results, and optional explanation
of a submitted fictional profile using calculated model contributions.

## 4. Limits to keep in the story

- Only 1,000 historical records, including 200 test cases and 60 bad-risk test cases.
  One test case changes bad-risk recall by about 1.7 percentage points.
- Higher test scores than validation means do not establish an improvement.
- Historical labels have no documented future-default prediction horizon;
  amounts remain in DM. The sample does not establish performance today.
- Seven inputs simplify the form; their optimality was not systematically tested.
- Some categories are rare or combine meanings, such as unknown/no savings.
- Excluding demographic inputs does not demonstrate fairness; proxies can remain.
- AI explanations can sound convincing while using imprecise wording. Model
  contributions describe a fitted calculation relative to a reference, not causes.

A fair conclusion is: **a working teaching demo that detects bad risks, with a
substantial false-rejection tradeoff and insufficient evidence for real lending.**

## Figures to reuse

| For | Figure |
| --- | --- |
| Philipp: validation comparison | [Model comparison](figures/cv_model_comparison.png) |
| Philipp: final errors | [Test confusion matrix](figures/final_test_confusion_matrix.png) |
| Optional validation detail | [Out-of-fold confusion matrices](figures/cv_confusion_matrices.png) |
| Nicolai: class imbalance | [Development class balance](figures/development_class_balance.png) |
| Optional data exploration | [Amounts/duration](figures/development_numeric_distributions.png), [accounts](figures/development_account_categories.png), [background categories](figures/development_background_categories.png) |

Use these existing figures and distinguish development, validation and test.
Attribute the dataset to Hofmann (1994), UCI Statlog (German Credit Data).
Dataset source, license and category meanings: [dataset guide](../data/README.md).

<details>
<summary>Optional: detailed metrics, data exploration and reproducibility evidence</summary>

- [Full validation summary](metrics.csv): all seven metrics, fold means and sample standard deviations.
- [Per-fold metrics](cv_fold_metrics.csv) and [out-of-fold predictions](cv_predictions.csv).
- [Comparison provenance](model_comparison.json): settings, hashes and pooled metrics.
- [Frozen decision](model_decision.json), committed as `d29c258` before test access.
- [Final test report](final_test.json) and [saved test predictions](final_test_predictions.csv).
- [Development summary](development_summary.json): 560 Good/240 Bad; no missing
  inputs, duplicate seven-input profiles or unknown codes. Median amount 2,317 DM;
  median duration 18 months. Sparse groups are descriptive, not validated rules.
- [Notebook 01](../notebooks/01_exploration.ipynb) and [notebook 02](../notebooks/02_model_comparison.ipynb)
  retain executed tables, figures and explanations.
- `selected_pipeline.joblib` is the saved development-trained pipeline and threshold;
  `explanation_reference.json` holds the development-only reference for profile contributions.

Fold averages and pooled predictions are different summaries, especially for
ROC-AUC and precision/F1. The artifacts label them separately. Keep original
files and decisions intact; read the saved final assessment rather than rerunning
it. Technical setup and checks are in the root README's optional section.

</details>
