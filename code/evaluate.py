"""Metrics for binary historical risk labels; no data loading or fitting."""

import numpy as np
from sklearn.metrics import (
    accuracy_score, balanced_accuracy_score, confusion_matrix,
    f1_score, precision_score, recall_score, roc_auc_score,
)

METRICS = [
    "accuracy", "balanced_accuracy", "bad_precision", "bad_recall", "bad_f1",
    "roc_auc", "cost_per_case",
]


def classification_metrics(y_true, y_pred, bad_probability):
    """Treat bad risk (1) as positive; cost = (5 * false negatives + FP) / n.

    Cost units are the source's illustrative assumption, not currency. Both
    true classes must be present for balanced accuracy and ROC-AUC to be useful.
    Undefined precision/F1 (no bad predictions) is reported as zero.
    """
    truth = np.asarray(y_true)
    predicted = np.asarray(y_pred)
    probability = np.asarray(bad_probability)
    if truth.ndim != 1 or predicted.shape != truth.shape or probability.shape != truth.shape:
        raise ValueError("Labels and probabilities must be matching one-dimensional arrays.")
    if set(np.unique(truth)) != {0, 1} or not set(np.unique(predicted)) <= {0, 1}:
        raise ValueError("True labels must contain both 0 and 1; predictions must be binary.")
    if not np.isfinite(probability).all() or ((probability < 0) | (probability > 1)).any():
        raise ValueError("Bad-risk scores must be finite values between zero and one.")
    tn, fp, fn, tp = confusion_matrix(truth, predicted, labels=[0, 1]).ravel()
    return {
        "accuracy": float(accuracy_score(truth, predicted)),
        "balanced_accuracy": float(balanced_accuracy_score(truth, predicted)),
        "bad_precision": float(precision_score(truth, predicted, zero_division=0)),
        "bad_recall": float(recall_score(truth, predicted)),
        "bad_f1": float(f1_score(truth, predicted, zero_division=0)),
        "roc_auc": float(roc_auc_score(truth, probability)),
        "cost_per_case": float((5 * fn + fp) / len(truth)),
        "true_good": int(tn), "false_rejections": int(fp),
        "false_approvals": int(fn), "true_bad": int(tp),
    }
