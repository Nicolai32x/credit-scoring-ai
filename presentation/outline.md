# Final presentation plan

Updated on 20 October 2026. This is the course-presentation plan, not the
kickoff agenda. The shared Canva template is available; final content and model
test results are still pending. Preliminary development-only model results are
available in `results/README.md`; label them as validation results when drafting
slides. The course requires a 20-25 minute
presentation and a 5-10 minute practical demo; this plan budgets 24 + 8 minutes.
Confirm with the lecturer whether the demo has a separate time slot.

Use the [shared Canva presentation](https://canva.link/doeibex7blblalaa) for slide
designs. It is a starting point, not a prescribed layout for each person's part.

## Story and roles

Question: How well can a simple model classify credit risk with seven inputs?
Explain the business decision, show how it is evaluated, then demonstrate the
limits alongside the practical result.

Technical implementation can have one lead. Speaking time does not measure
coding effort. Other roles own substantive analysis, evidence, and written
material, rather than only reading slides prepared by the technical lead.
Actual authorship and AI assistance must be recorded accurately.

| Role | Owner | Substantive responsibility | Speaking time |
| --- | --- | --- | --- |
| B: Business and literature | Jan | Business scenario, existing solutions, sources, success criteria | 6 minutes |
| T: Technical lead | Nicolai | Data preparation, experiments, evaluation pipeline, app; explain technical choices and GenAI use | 6 minutes |
| E: Results and economics | Philipp | Check results with technical lead, interpret errors, estimate costs and benefits with explicit assumptions | 6 minutes |
| R: Risks and conclusions | Zosia | Research risks and mitigations, discuss limitations, lessons learned and next steps | 6 minutes |

Each person also writes the matching report sections. The slide suggestions
below are flexible: develop your own explanations and visuals within your area,
while covering the course criteria. Conclusions depend on the actual results.

## Presentation overview

| Part | Slides / topics | Presenter | Time |
| --- | --- | --- | --- |
| Business Context & Project Goal | 1-3: business problem, existing solutions, research question and success criteria | Jan | 6 minutes |
| Data & Technical Approach | 4-6: dataset and seven inputs, models and evaluation, AI assistance and verification | Nicolai | 6 minutes |
| Results & Business Value | 7-9: model comparison, prediction errors, implementation costs and benefits | Philipp | 6 minutes |
| Risks & Conclusions | 10-12: ethical/legal/social risks, lessons learned, conclusions and next steps | Zosia | 6 minutes |
| Practical Demo | Seven inputs, example scenarios, prediction interpretation and limitations | Everyone; technical lead: Nicolai | 8 minutes |

Total target: 24-minute presentation plus 8-minute demo. Check actual timings
during rehearsal and confirm the time slots with the lecturer.

## Slide-by-slide outline (24 minutes)

| Slide | Content and question to answer | Evidence or visual to prepare later | Presenter | Minutes |
| --- | --- | --- | --- | --- |
| 1 | Business problem: what decision needs support and who is affected? | One illustrative lending scenario, with no invented performance claims | B | 2 |
| 2 | Existing solutions: how do rules, scorecards, and ML address the problem? | Referenced comparison; explain why a simple ML approach is worth testing | B | 2 |
| 3 | Project goal: what does success mean and what is outside scope? | Research question, seven-input scope, false-approval versus false-rejection tradeoff | B | 2 |
| 4 | Data: what are the labels and seven inputs? | UCI attribution, sample size, class balance, DM units, historical-data caveat | T | 2 |
| 5 | Method: how do we compare models fairly? | Diagram: test holdout, cross-validation, baseline, logistic regression, random forest | T | 2 |
| 6 | GenAI and reproducibility: what did AI help with and how did we check it? | One actual prompt, output excerpt, correction, and reproducible pipeline explanation | T | 2 |
| 7 | Measurable results: what did each model achieve? | Validation comparison and final held-out test result for the selected approach; values remain TBD | E | 2 |
| 8 | Error interpretation: which mistakes matter to the business? | Confusion matrix and bad-risk recall; historical 5:1 cost example, clearly labeled | E | 2 |
| 9 | Costs and benefits: what would this take to operate? | Team effort, hosting/maintenance assumptions, data and review needs; no fabricated ROI | E | 2 |
| 10 | Ethical, legal, and social risks: who could be harmed and how do we mitigate it? | Referenced discussion or visual covering all three areas | R | 2 |
| 11 | Good practices and lessons learned: what worked and what did not? | Actual findings on leakage prevention, evaluation, AI review, usability, and limitations | R | 2 |
| 12 | Implementation recommendation: what would we do next? | Bounded conclusion, remaining evidence needs, human-review concept, handoff to demo | R | 2 |
| **Total** | | | | **24** |

Do not select models or rewrite conclusions to make the story look successful.
A negative or mixed result is acceptable when explained and evaluated honestly.
Keep detailed code, full feature mappings, and extra metrics in backup material.

## Coverage of the course criteria

| Required presentation topic | Where it is covered |
| --- | --- |
| Business problem | Slides 1 and 3 |
| AI method or technology | Slides 2, 5, and 6 |
| Data used | Slide 4 |
| Measurable results | Slides 7 and 8 |
| Implementation costs | Slide 9 |
| Ethical, legal, and social risks | Slide 10, with limitations reinforced on slides 4 and 12 |
| Good practices and insights | Slides 6 and 11 |
| Practical demo and prompt/agent design, output, limitations | Slide 6 and the separate demo below |
| Responsible author on each slide | Author footer on every slide, including backups |

Each slide footer must name the actual content author(s). Track the presenter
separately when that person differs from the author. Cite data, literature,
figures, and legal claims where used. Record report-chapter authors as well.
AI-assisted material requires human review and a corresponding prompt-log entry.
The deck should not claim an agent exists if the team only used coding assistance.

## Separate practical demo (8 minutes)

| Segment | Lead | Minutes |
| --- | --- | --- |
| Introduce a fictional applicant and explain the seven inputs | B | 1 |
| Run the form with two contrasting scenarios | T | 3 |
| Interpret the output and change one input without claiming causality | E | 1 |
| Explain the actual prompt design, output, and human corrections | T | 1 |
| Show a boundary/ambiguous scenario and explain limitations | R | 2 |
| **Total** | | **8** |

Use the [demo sketch](../demo/README.md). Prepare screenshots or recorded example
outputs as a fallback after implementation. Do not invent predictions now.

## Minimum preparation for every presenter

Each person should be able to explain, in plain English:

- The target is a historical risk label, not a guaranteed future default.
- Training learns patterns, validation chooses settings, and the untouched test
  set provides a final assessment on held-out examples.
- What the confusion matrix says about costly mistakes.
- Why historical data, small samples, and proxy variables limit the conclusions.
- Their actual contribution and how they checked any AI-assisted material.

Rehearse once for content and once with a timer. Ask each other questions as
individuals, matching the lecturer's Q&A approach. Nobody needs to learn the
entire codebase, but nobody should present claims they cannot explain.

## Report and submission alignment

Use the same research question, dataset, metrics, and figures in report and
slides. Draft the report in one shared Word document in Teams, then export the
reviewed version to Markdown and PDF. Follow the
[report outline and workflow](../report/report.md); keep Word files in Teams
and do not write competing drafts in both formats.
Include existing solutions
with references, the GenAI experiment, and empirical goals, assumptions,
results, and interpretation. Check [the submission checklist](../submission/README.md)
before the presentation-day MS Teams upload into `YYYYMMDD_Topic`.
