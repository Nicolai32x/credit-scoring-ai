"""Exact additive explanations for the frozen logistic-regression pipeline."""

from hashlib import sha256
from pathlib import Path

import numpy as np
from final_model import predict_risk

ROOT = Path(__file__).resolve().parents[1]


def profile_context(bundle, inputs, reference):
    """Explain one submitted profile relative to mean transformed development data.

    These are exact centered coefficient contributions to the model logit, not
    causal effects, calibrated probabilities, or a counterfactual applicant.
    No training data loading or fitting happens here.
    """
    if len(inputs) != 1 or list(inputs.columns) != bundle["feature_columns"]:
        raise ValueError("Explain exactly one profile with the seven trained inputs.")
    model_path = ROOT / "results" / "selected_pipeline.joblib"
    if sha256(model_path.read_bytes()).hexdigest() != reference["pipeline_sha256"]:
        raise ValueError("Explanation reference does not match the saved pipeline.")
    pipeline = bundle["pipeline"]
    preprocessing = pipeline.named_steps["preprocessing"]
    classifier = pipeline.named_steps["model"]
    if list(classifier.classes_) != [0, 1]:
        raise ValueError("Expected good (0) / bad (1) class order.")
    names = preprocessing.get_feature_names_out().tolist()
    if names != reference["transformed_feature_names"]:
        raise ValueError("Explanation reference has a different encoded feature order.")
    encoder = preprocessing.named_transformers_["categorical"]
    for feature, categories in zip(preprocessing.transformers_[1][2], encoder.categories_):
        if inputs.iloc[0][feature] not in categories:
            raise ValueError(f"Category for {feature} was not observed during model fitting.")
    transformed = preprocessing.transform(inputs)[0]
    mean = np.asarray(reference["mean_transformed_development_inputs"])
    contributions = (transformed - mean) * classifier.coef_[0]
    reference_logit = float(classifier.intercept_[0] + mean @ classifier.coef_[0])
    actual_logit = float(pipeline.decision_function(inputs)[0])
    np.testing.assert_allclose(reference_logit + contributions.sum(), actual_logit, atol=1e-10)
    grouped = []
    for feature in bundle["feature_columns"]:
        indices = [i for i, name in enumerate(names)
                   if name == f"numeric__{feature}" or name.startswith(f"categorical__{feature}_")]
        value = float(contributions[indices].sum())
        grouped.append({"feature": feature, "contribution_logit_units": value,
                        "direction": "toward Bad risk" if value > 1e-10 else
                                     "toward Good risk" if value < -1e-10 else "negligible"})
    threshold_logit = float(np.log(bundle["threshold"] / (1 - bundle["threshold"])))
    return {
        "submitted_profile": inputs.iloc[0].to_dict(),
        "predicted_class": "Bad risk" if int(predict_risk(bundle, inputs).predicted_bad_risk.iloc[0]) else "Good risk",
        "contribution_reference": "Mean transformed inputs of the 800 development cases; not a real or typical applicant.",
        "reference_logit": reference_logit,
        "threshold_logit": threshold_logit,
        "model_logit": actual_logit,
        "contributions": sorted(grouped, key=lambda item: abs(item["contribution_logit_units"]), reverse=True),
        "interpretation_limits": "Contributions explain this fixed model calculation relative to the stated development mean. They do not explain real-world causes, default probabilities or lending suitability. All seven contributions plus the reference determine the class; a single feature may push in the opposite direction.",
    }
