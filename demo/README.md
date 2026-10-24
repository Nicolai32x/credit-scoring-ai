# Demo guide

Use fictional profiles. The demo illustrates a historical model; it does not
approve loans, predict a calibrated default probability or establish real lending suitability.

## What the audience sees

1. Enter seven values and click **Predict risk class**. Amount is historical DM,
   duration is months; the other five fields use English category descriptions.
2. **Explain this result with AI** explains the last submitted profile using actual
   model contributions. It does not explain unsent form edits. A new prediction
   clears the old profile explanation.
3. **Calculated model contributions** shows directions without an API call. They
   are relative to average transformed development inputs, not real-world causes
   or percentage changes. The reference is not a real or typical applicant.
4. **How reliable is this example?** shows the actual error tradeoff: 46/60 bad
   risks detected and 40/140 good risks wrongly flagged.
5. **AI explanation of our results** explains the aggregate evaluation. Its
   recorded simple/structured examples work without internet or an API key.
   The expanded comparison offers actual project results and two clearly marked
   synthetic explanation tests. Those invented counts are not new model results.

The ML classifier and generative AI are separate. No button retrains the model
or changes the frozen threshold. AI responses must still be checked.

## Fictional examples

These have no known correct outcome. Use the live class rather than promising
what the model will say. Category meanings: [dataset reference](../data/README.md).

| Scenario | Amount (DM) | Months | Purpose | Checking | Savings | Employment | Credit history |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A | 3,000 | 12 | A42: furniture | A12 | A62 | A74 | A32 |
| B | 9,000 | 48 | A40: new car | A11 | A61 | A72 | A33 |
| C | 3,000 | 12 | A42: furniture | A14 | A65 | A74 | A32 |

Change one input to discuss model sensitivity, not causality. The form limits
amount to 276-15,945 DM and duration to 4-60 months, following development data.
These are demo guardrails; allowed combinations can still be poorly represented.

For the group walkthrough, use [the eight-minute sequence](../presentation/outline.md).
A second-computer check and team rehearsal are still needed. Keep screenshots
as a fallback; the recorded aggregate AI responses are already available offline.

## Start locally

Reading results on GitHub needs no setup. To run the app, use Python 3.12.13 and
an existing project `.venv` (initial setup is in the root README). In PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe demo/run.py
```

Open the terminal's local URL, normally http://127.0.0.1:8501. Leave the terminal
open; stop with Ctrl+C. On macOS/Linux use `.venv/bin/python`; only Windows is verified.
The launcher watches the shared code folder. After code changes, use Streamlit's
Rerun prompt; if starting with a direct `streamlit run` command, restart the server
when imported modules change. Browser refresh alone can leave old modules loaded.

## Live AI: key and data flow

Risk predictions, model-contribution directions and recorded aggregate examples
need no API key. For live explanations, configure `OPENAI_API_KEY` in the local
environment or ignored `.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "your-secret-key"
```

Never commit or share the key. Each live click incurs API usage charges.

| Button | What is sent to OpenAI |
| --- | --- |
| Explain this result with AI | Last submitted fictional inputs, predicted class, English descriptions and computed model contributions |
| Generate AI explanation | Only the aggregate evaluation facts; no applicant inputs |

The app discloses the profile data flow before the button. Use fictional inputs
only. Requests do not run automatically on ordinary widget reruns. On failure,
the app distinguishes key/access, limits, connection and timeout issues; model
predictions remain available. Raw provider errors and keys are not displayed.

<details>
<summary>Optional: how the profile explanation is grounded</summary>

The saved logistic-regression pipeline is fitted on 800 development cases and
uses threshold 0.5. Center each transformed profile input on the development-data
mean, multiply by the fitted coefficient, and group one-hot columns back into
seven inputs. Those contributions plus the reference score exactly reconstruct
the model's decision score. The app never loads training data or refits anything.
The reference is stored in `results/explanation_reference.json` and tied to the
saved model checksum. These are associations in the model, not causal effects.

The first [profile integration output](../results/genai/profile_example.json)
used technical labels/raw values and said two smaller features while listing
three. The [refined output](../results/genai/profile_example_refined.json) used
friendlier labels and correctly described the supplied major directions. Both
remain unedited. They are outside the [aggregate prompt comparisons](../results/genai/README.md)
and do not prove every future profile explanation will follow instructions.

</details>
