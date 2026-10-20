# Actual OpenAI responses

Six completed responses from the first completed run after correcting the API key. These are unedited outputs. The earlier authentication failure remains in `attempts.jsonl`.

Exact full prompts and settings: `run_02/protocol.json`. Raw response records: `run_02/attempts.jsonl`. AI-assisted assessment: `run_02/assessment.json`; human sign-off pending.

## Simple prompt - repetition 1 (attempt 1)

Model: `gpt-5.4-mini-2026-03-17`. Generated: 2026-10-20T13:25:20.127463+00:00.

This model is a **credit-risk screening tool**, not an approval decision by itself. On the test set of 200 cases, it correctly identified **100 good borrowers** and **46 bad borrowers**. It made **14 false approvals** (risky applicants marked as good) and **40 false rejections** (good applicants marked as bad).

For lending, the most important error is usually a **false approval**, because that can lead to losses. Here, the model caught about **77% of bad cases**. Its **bad-risk precision is 53%**, meaning a little over half of the applicants it flags as bad really are bad. Overall, its performance is better than a simple rule that approves everyone: the reference approach would miss all bad cases and has a higher estimated cost.

The estimated **cost per case is 0.55**, versus **1.5** for the always-approve approach, so this model appears materially better on this historical dataset.

Important caveat: these are **historical teaching data**, not current lending data. The scores are **not calibrated probabilities**, and we have **no evidence here about fairness or present-day regulatory suitability**.

## Structured prompt - repetition 1 (attempt 2)

Model: `gpt-5.4-mini-2026-03-17`. Generated: 2026-10-20T13:25:22.670671+00:00.

This is a **historical teaching example**, not proof of how the model would perform in today’s lending process.

On the 200 test cases, there were **60 actual bad risks** and **140 actual good risks**. The model detected **46 of the 60 bad risks**, so it **missed 14 bad risks**. It also flagged **40 of the 140 good risks as bad**, so those were **incorrectly rejected good risks**.

So, the model is better at **finding bad risks** than a simple “always good” baseline, which would catch **0 of 60 bad risks**. Its **bad-risk recall** is **76.7%**, meaning it found about three-quarters of the bad cases. But **accuracy** is a different measure: the model got **73%** of all test cases right overall. Accuracy alone does not show how well it finds bad risks.

The reported cost is **0.55 illustrative cost units per case**, compared with **1.5** for the always-good baseline. This suggests better historical performance under that cost rule, but it does **not** prove future savings, profitability, or suitability for deployment.

## Simple prompt - repetition 2 (attempt 3)

Model: `gpt-5.4-mini-2026-03-17`. Generated: 2026-10-20T13:25:24.810957+00:00.

This model is a **credit-screening tool**, not a final lending decision maker. On the test set of 200 cases, it correctly identified **100 good borrowers** and **46 bad borrowers**. It made **14 false approvals** (bad applicants marked as good) and **40 false rejections** (good applicants marked as bad).

Compared with an “always approve” approach, the model is much better at spotting risky applicants. Its **bad-recall of 76.7%** means it catches about three-quarters of bad cases, while the reference catches none. Its **ROC AUC of 0.81** suggests good overall separation between good and bad risks.

However, the model is still conservative: it rejects some good customers. The **accuracy of 73%** is useful, but the more important point for lending is the trade-off between missed bad loans and lost good business.

The reported **cost per case fell from 1.5 to 0.55**, which is a strong improvement under the stated assumptions. Still, this is a historical teaching dataset, so it should not be used as proof of current lending suitability or fairness.

## Structured prompt - repetition 2 (attempt 4)

Model: `gpt-5.4-mini-2026-03-17`. Generated: 2026-10-20T13:25:27.593748+00:00.

This is a **historical teaching example**, not proof of how the model would perform today or in live lending. The test set had **60 actual bad risks** and **140 actual good risks**.

The model correctly identified **46 of the 60 bad risks**, so it **missed 14 bad risks**. It also correctly kept **100 of the 140 good risks**. However, it **incorrectly flagged 40 good risks as bad**.

So the model’s **accuracy was 73%**, meaning it got 73 out of 100 cases right overall. But accuracy alone can be misleading here, because the model’s main job is to spot bad risks. On that measure, it detected **76.7% of the actual bad risks**. That is different from accuracy.

Compared with an “always good” reference rule, this model does better at identifying bad risks, but it still makes both kinds of mistakes. Any cost figures are only **illustrative cost units**: the model’s average cost was **0.55 per case**, versus **1.5** for the reference rule.

What the evidence supports: the model has some ability to separate bad from good cases in this dataset. What it does not support: calibrated default probabilities, causal explanations, or present-day lending decisions.

## Simple prompt - repetition 3 (attempt 5)

Model: `gpt-5.4-mini-2026-03-17`. Generated: 2026-10-20T13:25:29.513705+00:00.

This model is a **useful screening tool**, not a final lending decision rule. On the test set of 200 cases, it correctly identified **100 good customers** and **46 bad customers**. It made **14 false approvals** (bad applicants accepted) and **40 false rejections** (good applicants declined).

Compared with an “always approve” approach, the model is much better at spotting risky applicants. It raises the ability to detect bad cases from **0% to 76.7%**, and overall discrimination is stronger, with a **ROC AUC of 0.81**. That means it separates good and bad risks fairly well.

The trade-off is that it still rejects some good applicants. Under the stated cost assumption, the model’s average cost is **0.55 per case**, versus **1.5** for always approving everyone.

Important caveat: this is a **historical teaching dataset**, and the scores are **not calibrated probabilities**. It has **not been tested for fairness or current lending use**.

## Structured prompt - repetition 3 (attempt 6)

Model: `gpt-5.4-mini-2026-03-17`. Generated: 2026-10-20T13:25:32.023929+00:00.

This is a **historical teaching example**, not proof about today’s borrowers. The model was tested on 200 cases and correctly classified **73%** overall. But overall accuracy alone does not show how well it finds bad risks.

Out of **60 actual bad risks**, it detected **46** and missed **14**. So its **bad-risk recall** was about **76.7%**. Out of **140 actual good risks**, it incorrectly flagged **40** as bad and correctly accepted **100**. So the **good-risk false rejection rate** was **40/140 = 28.6%**.

In plain terms: it catches many bad risks, but it also wrongly turns away a noticeable number of good risks. That trade-off is separate from accuracy. A model can look fairly accurate overall while still missing some bad cases or wrongly flagging good ones.

The score is **not a calibrated probability of default**. The evidence here supports only performance on this historical dataset, with **illustrative cost units** showing the model did better than an “always good” baseline on that data. It does **not** prove fairness, present-day usefulness, or lending suitability.
