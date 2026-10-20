# Dataset guide: Statlog (German Credit Data)

Downloaded and checked on 16 October 2026; project status updated on 20 October.
Statlog is the selected teaching dataset. No preprocessing, splitting, or model
training has been done.

## Source, files, and license

Hofmann, H. (1994). *Statlog (German Credit Data)* [Dataset]. UCI Machine Learning
Repository. DOI: https://doi.org/10.24432/C5NC77

- [Official dataset page](https://archive.ics.uci.edu/dataset/144/statlog+german+credit+data)
- [Original data download](https://archive.ics.uci.edu/ml/machine-learning-databases/statlog/german/german.data)
- [Original dictionary download](https://archive.ics.uci.edu/ml/machine-learning-databases/statlog/german/german.doc)
- License listed by UCI: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
  Include attribution, the license link, and a statement of changes when sharing
  or adapting the data. See [LICENSE.md](LICENSE.md).

`german.data` and `german.doc` were downloaded unchanged on 16 October 2026.
They are explicitly allowed in Git because they are small, publicly licensed
files. Other datasets remain ignored. Include these originals and attribution
in the eventual submission package.

| File | Bytes | SHA-256 |
| --- | --- | --- |
| `german.data` | 79,793 | `b21f3d81db8071257d5ff1deaeba1fd4303b62712e6fcc9715c7a86202cb5871` |
| `german.doc` | 4,679 | `69b92cb551111bc37098698288849c96f0fd87ce81a2e54451ff39aa1e53fe49` |

Use the original mixed categorical/numeric `german.data`, not the separately
transformed `german.data-numeric`. It has no header and uses whitespace between
fields. Columns 1-20 are inputs; column 21 is the target. Later, load with
`pandas.read_csv`, `sep=r"\s+"`, and `header=None`, then assign column names.
Both `.data` and `.doc` are plain-text files; `german.doc` is not a Word document.

## Target and verified structural checks

Original labels: **1 = good credit risk; 2 = bad credit risk**. For later
evaluation, map these to **0 = good; 1 = bad**, so positive means bad risk.
These are historical risk labels, not a documented default-within-12-months
outcome. A model score is not automatically a validated future default probability.

The following checks examined the complete downloaded file without modeling
or exploring feature/target relationships. Predictive exploration will use
development data only, after reserving the test set.

| Check | Finding |
| --- | --- |
| Records and fields | 1,000 records, each with 20 inputs and one target |
| Input types | 7 numeric, 13 categorical, as described in `german.doc` |
| Classes | 700 good (70%), 300 bad (30%) |
| Blank rows / common missing tokens | 0 / 0; checked `?`, `NA`, `NaN`, `null`, `none` |
| Exact duplicate rows | 0 |
| Identical full inputs with conflicting targets | 0 |
| Repeated vectors across the seven proposed inputs | 0 |
| Unexpected categorical codes against dictionary | 0 |
| Duration | 4-72 months |
| Credit amount | 250-18,424; keep historical DM context explicit |

Some categories include unknown information despite the absence of empty cells.
For example, A65 combines unknown savings with no savings account. Do not
silently convert this to zero or discard these cases.

Always predicting good risk would give 70% accuracy and 0% bad-risk recall on
the whole file. This is a reference calculation, not a validated model result.

## Seven planned inputs

| Original column | English feature name | Form control |
| --- | --- | --- |
| 5 | `credit_amount` | Integer: amount in historical DM context |
| 2 | `duration_months` | Integer: months |
| 4 | `purpose` | Dropdown |
| 1 | `checking_status` | Dropdown |
| 6 | `savings_status` | Dropdown |
| 7 | `employment_duration` | Dropdown |
| 3 | `credit_history` | Dropdown |

Train the demo model using exactly these seven inputs. Display order differs
from file order. Do not train on 20 inputs and silently invent the remaining
13 values for the form. Predictive adequacy has not yet been established.

### Category guide for the form

Descriptions below paraphrase `german.doc`. Preserve combined meanings rather
than interpreting the source codes as ordered numeric risk scores.

| Input | Source codes and English meanings |
| --- | --- |
| Checking account | A11: below 0 DM; A12: 0 to below 200 DM; A13: at least 200 DM / salary assignments for at least one year; A14: no checking account |
| Savings/bonds | A61: below 100 DM; A62: 100 to below 500 DM; A63: 500 to below 1,000 DM; A64: at least 1,000 DM; A65: unknown / no savings account |
| Employment | A71: unemployed; A72: less than one year; A73: one to less than four years; A74: four to less than seven years; A75: at least seven years |
| Credit history | A30: no credits taken / all credits repaid duly; A31: all credits at this bank repaid duly; A32: existing credits repaid duly so far; A33: previous repayment delay; A34: critical account / other credits outside this bank |
| Purpose | A40: new car; A41: used car; A42: furniture/equipment; A43: radio/television; A44: domestic appliances; A45: repairs; A46: education; A48: retraining; A49: business; A410: other |

A47 (vacation) appears in the dictionary but not the data; omit it from the
first demo. A95 in the unused personal-status/sex column is also documented but
absent. Neither absence indicates a missing row.

All 20 original input columns, in order: checking account, duration, credit
history, purpose, amount, savings/bonds, employment duration, installment rate,
personal status/sex, other debtors/guarantors, residence duration, property,
age, other installment plans, housing, existing credits, job, dependants,
telephone, foreign-worker status. Consult `german.doc` for the unused columns.

## Limits to explain in the report

- The dataset was donated in 1994. The source does not establish a precise
  observation period or prediction horizon; donation date is not collection date.
- Retain the historical currency context. Relabeling amounts as EUR is misleading;
  conversion alone would not modernize the data.
- With 1,000 examples, performance and subgroup comparisons can be unstable.
  Some categories are rare: retraining, for example, has 9 records.
- The original data includes age, personal status/sex, and foreign-worker status.
  The planned seven-input model excludes them. Other features can still act as proxies;
  exclusion alone does not demonstrate fairness.
- No IDs or dates allow us to independently verify a split by applicant or time.
  A random test split does not demonstrate generalization to today's applicants.
- The source's illustrative error costs are 5 for bad risk predicted good, 1 for
  good risk predicted bad, and 0 for correct predictions. They are not actual
  monetary losses for a bank.

See [PROJECT_PLAN.md](../PROJECT_PLAN.md) for the proposed experiment.
