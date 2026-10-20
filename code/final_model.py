"""Refit the frozen decision on development data and assess the test set once.

Run this script explicitly, never as a notebook side effect. Existing final
outputs prevent reruns; notebooks and the demo read the saved artifacts.
"""

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import platform

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.linear_model import LogisticRegression

from evaluate import classification_metrics
from preprocessing import (
    FEATURE_COLUMNS, PROJECT_ROOT, SOURCE_SHA256, SPLIT_PATH,
    build_model_pipeline, load_partition,
)

RESULTS = PROJECT_ROOT / "results"
DECISION_PATH = RESULTS / "model_decision.json"
FINAL_FILES = ["selected_pipeline.joblib", "final_test_predictions.csv", "final_test.json"]


def load_decision(path=DECISION_PATH):
    """Check the frozen experiment identity before any final fitting or test use."""
    decision = json.loads(Path(path).read_text(encoding="utf-8"))
    if (decision["model"] != "logistic_regression"
            or decision["feature_columns"] != FEATURE_COLUMNS
            or decision["source_sha256"] != SOURCE_SHA256
            or decision["split_sha256"] != sha256(SPLIT_PATH.read_bytes()).hexdigest()
            or decision["threshold"] != 0.5
            or decision["scale_numeric"] is not True):
        raise ValueError("Frozen decision does not match the selected project experiment.")
    comparison = RESULTS / "model_comparison.json"
    if sha256(comparison.read_bytes()).hexdigest() != decision["comparison_sha256"]:
        raise ValueError("Validation comparison has changed since the decision was frozen.")
    for name, checksum in decision["training_code_sha256"].items():
        if sha256((PROJECT_ROOT / "code" / name).read_bytes()).hexdigest() != checksum:
            raise ValueError(f"Training code changed after model selection: {name}")
    return decision


def predict_risk(bundle, X):
    """Use the saved threshold explicitly; scores are not calibrated default risks."""
    pipeline = bundle["pipeline"]
    bad_column = list(pipeline.classes_).index(1)
    scores = pipeline.predict_proba(X)[:, bad_column]
    return pd.DataFrame({
        "predicted_bad_risk": (scores >= bundle["threshold"]).astype(int),
        "bad_risk_score": scores,
    }, index=X.index)


def run_final_assessment(output_dir=RESULTS, decision_path=DECISION_PATH):
    """Refuse existing artifacts before loading data, then run the frozen assessment.

    The guard prevents accidental reruns in the normal workflow; it is not an
    access-control mechanism. Never delete outputs to try a different model.
    """
    output = Path(output_dir)
    if any((output / name).exists() for name in FINAL_FILES):
        raise FileExistsError("Final outputs already exist. Read them; do not repeat test selection.")
    decision = load_decision(decision_path)
    X_dev, y_dev = load_partition()
    pipeline = build_model_pipeline(
        LogisticRegression(**decision["model_parameters"]),
        scale_numeric=decision["scale_numeric"],
    ).fit(X_dev, y_dev)
    bundle = {
        "pipeline": pipeline, "threshold": decision["threshold"],
        "feature_columns": FEATURE_COLUMNS,
        "decision_sha256": sha256(Path(decision_path).read_bytes()).hexdigest(),
        "training_cases": len(X_dev),
        "scikit_learn_version": sklearn.__version__,
    }
    # Only now open the reserved test partition; no decisions follow its scores.
    X_test, y_test = load_partition("test")
    predictions = predict_risk(bundle, X_test)
    scores = classification_metrics(y_test, predictions.predicted_bad_risk, predictions.bad_risk_score)
    # A prespecified always-good reference, not a second candidate selection.
    baseline = classification_metrics(y_test, np.zeros(len(y_test), dtype=int), np.zeros(len(y_test)))
    output.mkdir(parents=True, exist_ok=True)
    with (output / "selected_pipeline.joblib").open("xb") as stream:
        joblib.dump(bundle, stream)
    predictions.insert(0, "actual_bad_risk", y_test)
    predictions.to_csv(output / "final_test_predictions.csv", index=True, index_label="row_id", mode="x")
    report = {
        "assessed_at_utc": datetime.now(timezone.utc).isoformat(),
        "partition": "test", "training_partition": "development",
        "training_cases": len(X_dev), "test_cases": len(X_test),
        "model": decision["model"], "threshold": decision["threshold"],
        "threshold_tuned_on_test": False, "model_refitted_on_test": False,
        "decision_sha256": bundle["decision_sha256"],
        "pipeline_sha256": sha256((output / "selected_pipeline.joblib").read_bytes()).hexdigest(),
        "source_sha256": SOURCE_SHA256, "split_sha256": decision["split_sha256"],
        "assessment_code_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "versions": {"python": platform.python_version(), "numpy": np.__version__,
                     "pandas": pd.__version__, "scikit_learn": sklearn.__version__,
                     "joblib": joblib.__version__},
        "selected_model_metrics": scores, "always_good_reference_metrics": baseline,
        "cost_assumption": "5 per false approval, 1 per false rejection; not currency",
        "limitations": [
            "One historical random test split with only 60 bad-risk cases.",
            "No threshold or model changes should be made using these test results.",
            "Scores are not calibrated probabilities of future default.",
            "No demonstrated fairness, profitability, or suitability for real lending.",
        ],
    }
    with (output / "final_test.json").open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(report, indent=2, allow_nan=False) + "\n")
    return report


if __name__ == "__main__":
    print(json.dumps(run_final_assessment(), indent=2))
