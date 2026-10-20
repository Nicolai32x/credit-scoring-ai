"""Seven-input teaching demo; inference only with the frozen saved pipeline."""

from hashlib import sha256
import json
from pathlib import Path
import sys

import joblib
import pandas as pd
import sklearn
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
from final_model import predict_risk  # noqa: E402
from preprocessing import CATEGORICAL_FEATURES, FEATURE_COLUMNS  # noqa: E402

CATEGORY_LABELS = {
    "purpose": {
        "A40": "New car", "A41": "Used car", "A42": "Furniture / equipment",
        "A43": "Radio / television", "A44": "Domestic appliances", "A45": "Repairs",
        "A46": "Education", "A48": "Retraining", "A49": "Business", "A410": "Other",
    },
    "checking_status": {
        "A11": "Below 0 DM", "A12": "0 to below 200 DM",
        "A13": "At least 200 DM / salary assignments for at least one year",
        "A14": "No checking account",
    },
    "savings_status": {
        "A61": "Below 100 DM", "A62": "100 to below 500 DM",
        "A63": "500 to below 1,000 DM", "A64": "At least 1,000 DM",
        "A65": "Unknown / no savings account",
    },
    "employment_duration": {
        "A71": "Unemployed", "A72": "Less than one year",
        "A73": "One to less than four years", "A74": "Four to less than seven years",
        "A75": "At least seven years",
    },
    "credit_history": {
        "A30": "No credits taken / all credits repaid duly",
        "A31": "All credits at this bank repaid duly",
        "A32": "Existing credits repaid duly so far",
        "A33": "Previous repayment delay",
        "A34": "Critical account / other credits outside this bank",
    },
}
FIELD_LABELS = {
    "purpose": "Loan purpose", "checking_status": "Checking-account category",
    "savings_status": "Savings / bonds", "employment_duration": "Employment duration",
    "credit_history": "Credit history",
}
DEFAULTS = {"purpose": "A42", "checking_status": "A12", "savings_status": "A62",
            "employment_duration": "A74", "credit_history": "A32"}


@st.cache_resource
def load_assets():
    """Load the trusted project artifact once; never train or open raw test data."""
    results = ROOT / "results"
    report = json.loads((results / "final_test.json").read_text(encoding="utf-8"))
    model_path = results / "selected_pipeline.joblib"
    if sha256(model_path.read_bytes()).hexdigest() != report["pipeline_sha256"]:
        raise ValueError("Saved model checksum does not match the final assessment.")
    if report["versions"]["scikit_learn"] != sklearn.__version__:
        raise ValueError("Use the project's pinned scikit-learn version to load the model.")
    bundle = joblib.load(model_path)
    if (bundle["feature_columns"] != FEATURE_COLUMNS or bundle["training_cases"] != 800
            or bundle["threshold"] != .5
            or bundle["decision_sha256"] != report["decision_sha256"]):
        raise ValueError("Saved model metadata does not match the frozen decision.")
    encoder = bundle["pipeline"].named_steps["preprocessing"].named_transformers_["categorical"]
    supported = dict(zip(CATEGORICAL_FEATURES, encoder.categories_))
    for feature, codes in supported.items():
        if not set(codes) <= set(CATEGORY_LABELS[feature]):
            raise ValueError(f"Missing source-category descriptions for {feature}.")
    return bundle, report, supported


def category_input(feature, supported):
    """Offer only categories learned by the saved development-trained encoder."""
    options = [code for code in CATEGORY_LABELS[feature] if code in supported[feature]]
    return st.selectbox(
        FIELD_LABELS[feature], options, index=options.index(DEFAULTS[feature]),
        format_func=lambda code: CATEGORY_LABELS[feature][code], key=feature,
    )


def main():
    st.set_page_config(page_title="Credit Risk Demo", page_icon="📊", layout="centered")
    st.title("Credit Risk Demo")
    st.caption("Introduction to AI in Business · Statlog German Credit Data")
    st.write("Try a fictional applicant and loan profile using seven inputs.")
    st.info("Historical teaching example. The prediction is not a lending recommendation.")
    try:
        bundle, report, supported = load_assets()
    except (OSError, ValueError, KeyError) as error:
        st.error("The saved model could not be loaded. Check the project files and install requirements.txt.")
        st.caption(str(error))
        st.stop()

    with st.form("credit_profile"):
        left, right = st.columns(2)
        with left:
            amount = st.number_input("Credit amount (historical DM)", min_value=276,
                                     max_value=15945, value=3000, step=100, key="credit_amount")
            purpose = category_input("purpose", supported)
            savings = category_input("savings_status", supported)
            history = category_input("credit_history", supported)
        with right:
            duration = st.number_input("Duration (months)", min_value=4,
                                       max_value=60, value=12, step=1, key="duration_months")
            checking = category_input("checking_status", supported)
            employment = category_input("employment_duration", supported)
        st.caption("DM is the historical currency, not EUR. Ranges follow development data; "
                   "an allowed combination may still be poorly represented.")
        submitted = st.form_submit_button("Predict risk class", type="primary")

    if submitted:
        values = {
            "credit_amount": amount, "duration_months": duration, "purpose": purpose,
            "checking_status": checking, "savings_status": savings,
            "employment_duration": employment, "credit_history": history,
        }
        inputs = pd.DataFrame([values], columns=bundle["feature_columns"])
        prediction = int(predict_risk(bundle, inputs).predicted_bad_risk.iloc[0])
        st.subheader("Result for the submitted example")
        st.info(f"Predicted class: {'Bad risk' if prediction else 'Good risk'}")
        st.caption("This is a model class, not a credit approval or a probability of default. "
                   "Submit again after changing inputs.")
        with st.expander("Submitted inputs"):
            readable = {"Credit amount (historical DM)": amount, "Duration (months)": duration}
            readable.update({FIELD_LABELS[name]: CATEGORY_LABELS[name][values[name]]
                             for name in CATEGORICAL_FEATURES})
            st.table(pd.DataFrame(readable.items(), columns=["Input", "Submitted value"]).astype(str))

    with st.expander("How reliable is this example?"):
        scores = report["selected_model_metrics"]
        st.write(f"On {report['test_cases']} held-out historical cases, the model detected "
                 f"{scores['true_bad']} of {scores['true_bad'] + scores['false_approvals']} bad risks. "
                 f"It also flagged {scores['false_rejections']} of "
                 f"{scores['true_good'] + scores['false_rejections']} good risks incorrectly.")
        st.write("About half the cases flagged bad were actually labeled bad. These results "
                 "do not establish suitability for real lending. The dataset is historical, "
                 "some categories are rare, and fairness has not been demonstrated.")
        st.write("The saved logistic-regression pipeline was trained on 800 development cases "
                 "with the same seven inputs. This app does not retrain it or change its threshold.")
    st.caption("Source: Hofmann (1994), UCI Statlog (German Credit Data), CC BY 4.0.")
    st.markdown("[Dataset and attribution](https://doi.org/10.24432/C5NC77)")


if __name__ == "__main__":
    main()
