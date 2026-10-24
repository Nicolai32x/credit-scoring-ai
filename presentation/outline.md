# Presentation outline

Use the [shared Canva presentation](https://canva.link/doeibex7vw4e04b).
Target **24 minutes of presentation plus an 8-minute demo**. The course ranges
are 20-25 and 5-10 minutes; confirm whether the demo has its own time slot.
Presentation date and final topic name still need to be recorded.

**Story:** Can seven inputs support a useful credit-risk classification, and
what do its errors prevent us from claiming?

## Sections and suggested slides

Everyone has about six minutes. Suggestions are flexible; develop your own
slides and the matching report section. Figures and numbers are already saved.

| Slide | Person | Topic | Material / point to explain | Minutes |
| --- | --- | --- | --- | --- |
| 1 | Jan | Business problem | Who needs support, and what decision is involved? | 2 |
| 2 | Jan | Existing approaches | Referenced comparison of rules, scorecards and ML | 2 |
| 3 | Jan | Project goal | Seven-input scope, success criteria and the two error types | 2 |
| 4 | Nicolai | Our dataset and seven inputs | 1,000 UCI historical cases, seven inputs, 70:30 labels, DM units | 1.25 |
| 5 | Nicolai | Training, validation and testing | 800 development / 200 test; five validation folds; freeze model and threshold before test | 1.5 |
| 6 | Nicolai | The models we compared | Always-Good baseline, logistic regression, random forest; select using balanced accuracy | 1.25 |
| 7 | Nicolai | Using and checking generative AI | Separate 30-response extension: 3 scenarios x 2 prompts x 5 repetitions. Denominators 10/15 vs 15/15; word limit 15/15 vs 12/15. Two scenarios synthetic; AI-assisted review, human sign-off pending | 2 |
| 8 | Philipp | Results | Validation comparison, then the selected model's separate test result: 74.0% balanced accuracy | 2 |
| 9 | Philipp | Prediction errors | 46/60 bad risks detected, 40/140 good risks wrongly flagged; 5:1 assumed costs | 2 |
| 10 | Philipp | Costs and benefits | Implementation effort, hosting/maintenance and review needs; explicit assumptions, no fabricated ROI | 2 |
| 11 | Zosia | Ethical, legal and social risks | Referenced risks, affected people and mitigations | 2 |
| 12 | Zosia | Lessons learned | Actual findings: leakage prevention, moderate performance, AI review, usability | 2 |
| 13 | Zosia | Conclusion and next steps | Bounded recommendation, evidence still missing, transition to demo | 2 |

## Material to use

- **Philipp:** [results and figure links](../results/README.md). Distinguish validation
  means from final test scores. The cost units are not euros or actual savings.
- **Nicolai:** saved [notebook 01](../notebooks/01_exploration.ipynb),
  [notebook 02](../notebooks/02_model_comparison.ipynb) and
  [GenAI summary/answers](../results/genai/README.md). The profile explanation is
  a separate demo feature, outside the pilot and expanded aggregate comparison.
- **Jan and Zosia:** use those same results as factual context, then add sources
  for your own business/literature and risk claims.

Name the actual responsible author(s) in each slide footer and cite the sources.
Presenter and author may differ; record contributions and AI assistance accurately.
The demo includes an API explanation, not an autonomous lending agent.

## Demo sequence: eight minutes

| Segment | Lead | Minutes |
| --- | --- | --- |
| Introduce a fictional profile and the seven inputs | Jan | 1 |
| Run contrasting examples and explain the model/AI distinction | Nicolai | 3 |
| Explain errors and change one input without claiming causality | Philipp | 1 |
| Show simple/structured recorded AI answers and one limitation/correction | Nicolai | 1 |
| Discuss an ambiguous case, limits and the need for review | Zosia | 2 |

Use the [demo guide](../demo/README.md). The actual app has three distinct parts:
ML prediction, optional AI explanation of the submitted fictional profile, and
AI explanation of the overall results. Only the profile button sends the fictional
form values to OpenAI. Calculated contribution directions work without an API key;
recorded aggregate answers also work offline. Prepare screenshots as a fallback.

## Before presenting

- Everyone can explain historical risk labels, training/validation/test separation,
  both error types and the limits of the model and AI explanations.
- Read the actual AI outputs; the assessment is AI-assisted, with human sign-off pending.
- Rehearse content, then time the full presentation and demo. Test a second computer.
- Use the same figures, numbers and APA references as the shared Word report.
- Complete [the submission checklist](../submission/README.md).

<details>
<summary>Course coverage check</summary>

| Requirement | Where |
| --- | --- |
| Business problem | 1 and 3 |
| AI method/technology | 2, 5, 6 and 7 |
| Data | 4 |
| Measurable results | 8 and 9 |
| Implementation costs | 10 |
| Ethical, legal and social risks | 11 |
| Good practices and insights | 7 and 12 |
| Prompt design, output and limitations | 7 and the demo |
| Responsible authorship | Every slide footer |

</details>
