"""Fixed-configuration development-only comparison; no final test or model export."""

from hashlib import sha256
import json
import platform

import numpy as np
import pandas as pd
import sklearn
from sklearn.base import clone
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold

from evaluate import METRICS, classification_metrics
from preprocessing import (
    FEATURE_COLUMNS, PROJECT_ROOT, RANDOM_SEED, SOURCE_SHA256, SPLIT_PATH,
    build_model_pipeline, load_partition,
)

THRESHOLD = 0.5


def candidate_pipelines():
    """Prespecified first comparison, without tuning or threshold search.

    Balanced weights address class imbalance without resampling. The forest's
    minimum leaf size of five limits very small leaves in this small dataset.
    Neither weighting nor these settings are claimed to be optimal.
    """
    return {
        "majority_baseline": build_model_pipeline(DummyClassifier(strategy="most_frequent")),
        "logistic_regression": build_model_pipeline(LogisticRegression(
            C=1.0, solver="lbfgs", max_iter=2000,
            class_weight="balanced", random_state=RANDOM_SEED,
        )),
        "random_forest": build_model_pipeline(RandomForestClassifier(
            n_estimators=300, min_samples_leaf=5, class_weight="balanced",
            random_state=RANDOM_SEED, n_jobs=1,
        ), scale_numeric=False),
    }


def compare_models(X, y, *, models=None, n_splits=5):
    """Return fold metrics and out-of-fold predictions on supplied development data.

    Each row is validation once per model. Every fit starts with a fresh complete
    pipeline, and all models use identical fold membership. No fit on all rows
    or final model selection occurs here. Optional models support small checks.
    """
    if not X.index.equals(y.index) or not X.index.is_unique:
        raise ValueError("Inputs and target need matching, unique row indices.")
    if set(y.unique()) != {0, 1} or y.value_counts().min() < n_splits:
        raise ValueError("Both classes need at least n_splits development examples.")
    candidates = candidate_pipelines() if models is None else models
    folds = list(StratifiedKFold(
        n_splits=n_splits, shuffle=True, random_state=RANDOM_SEED,
    ).split(X, y))
    fold_records, prediction_frames = [], []
    for name, template in candidates.items():
        for fold, (training, validation) in enumerate(folds, start=1):
            fitted = clone(template).fit(X.iloc[training], y.iloc[training])
            bad_column = list(fitted.classes_).index(1)
            probability = fitted.predict_proba(X.iloc[validation])[:, bad_column]
            predicted = (probability >= THRESHOLD).astype(int)
            scores = classification_metrics(y.iloc[validation], predicted, probability)
            fold_records.append({
                "model": name, "fold": fold, "training_cases": len(training),
                "validation_cases": len(validation), **scores,
            })
            prediction_frames.append(pd.DataFrame({
                "model": name, "fold": fold, "row_id": X.index[validation],
                "actual_bad_risk": y.iloc[validation].to_numpy(),
                "predicted_bad_risk": predicted, "bad_risk_score": probability,
            }))
    return pd.DataFrame(fold_records), pd.concat(prediction_frames, ignore_index=True)


def summarize_folds(fold_metrics):
    """Mean and sample standard deviation across folds, not confidence intervals."""
    grouped = fold_metrics.groupby("model", sort=False)[METRICS].agg(["mean", "std"])
    grouped.columns = [f"{metric}_{statistic}" for metric, statistic in grouped.columns]
    return grouped.reset_index()


def save_comparison(fold_metrics, predictions, output_dir=None):
    """Export reproducible validation outputs from the fixed project experiment."""
    output = PROJECT_ROOT / "results" if output_dir is None else output_dir
    output.mkdir(parents=True, exist_ok=True)
    summary = summarize_folds(fold_metrics)
    fold_metrics.to_csv(output / "cv_fold_metrics.csv", index=False)
    predictions.to_csv(output / "cv_predictions.csv", index=False)
    summary.to_csv(output / "metrics.csv", index=False)
    pooled = {}
    for name, rows in predictions.groupby("model", sort=False):
        pooled[name] = classification_metrics(
            rows.actual_bad_risk, rows.predicted_bad_risk, rows.bad_risk_score,
        )
    provenance = {
        "partition": "development", "cases": 800, "test_evaluated": False,
        "validation": {"n_splits": 5, "shuffle": True, "random_state": RANDOM_SEED},
        "threshold": THRESHOLD, "threshold_tuned": False, "parameter_search": False,
        "primary_metric": "balanced_accuracy", "feature_columns": FEATURE_COLUMNS,
        "cost_assumption": "(5 * false approvals + false rejections) / number of cases; not currency",
        "source_sha256": SOURCE_SHA256,
        "split_sha256": sha256(SPLIT_PATH.read_bytes()).hexdigest(),
        "code_sha256": {name: sha256((PROJECT_ROOT / "code" / name).read_bytes()).hexdigest()
                        for name in ["preprocessing.py", "train.py", "evaluate.py"]},
        "versions": {"python": platform.python_version(), "numpy": np.__version__,
                     "pandas": pd.__version__, "scikit_learn": sklearn.__version__},
        "candidate_parameters": {
            name: pipeline.named_steps["model"].get_params(deep=False)
            for name, pipeline in candidate_pipelines().items()
        },
        "fold_summary": summary.to_dict(orient="records"),
        "pooled_out_of_fold_metrics": pooled,
        "limitations": [
            "Same validation folds compare candidates; selection estimates can be optimistic.",
            "Fold standard deviations are not independent-sample confidence intervals.",
            "Raw model scores are not calibrated probabilities of future default.",
            "No final model, threshold, or test assessment has been frozen.",
        ],
    }
    (output / "model_comparison.json").write_text(
        json.dumps(provenance, indent=2, allow_nan=False) + "\n", encoding="utf-8",
    )
    return summary


if __name__ == "__main__":
    X_development, y_development = load_partition()
    metrics, predictions = compare_models(X_development, y_development)
    print(save_comparison(metrics, predictions).to_string(index=False))
    print("Development-only comparison saved. No test evaluation or final model export.")
