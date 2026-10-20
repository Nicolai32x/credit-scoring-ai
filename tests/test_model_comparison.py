"""Check error-cost direction and out-of-fold isolation with invented cases."""

from pathlib import Path
import sys
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import StratifiedKFold

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
from evaluate import classification_metrics  # noqa: E402
from preprocessing import NUMERIC_FEATURES, build_model_pipeline  # noqa: E402
from train import compare_models, summarize_folds  # noqa: E402


class ModelComparisonTests(unittest.TestCase):
    def test_bad_risk_is_positive_and_false_approval_costs_five(self):
        scores = classification_metrics(
            [0, 0, 0, 1, 1, 1], [0, 0, 1, 0, 0, 1], [.1, .2, .8, .3, .4, .9],
        )
        self.assertEqual(scores["false_approvals"], 2)
        self.assertEqual(scores["false_rejections"], 1)
        self.assertAlmostEqual(scores["cost_per_case"], 11 / 6)
        self.assertAlmostEqual(scores["bad_recall"], 1 / 3)
        self.assertAlmostEqual(scores["bad_precision"], .5)
        self.assertAlmostEqual(scores["balanced_accuracy"], .5)
        self.assertAlmostEqual(scores["roc_auc"], 7 / 9)

    def test_all_good_baseline_does_not_hide_zero_bad_recall(self):
        scores = classification_metrics([0, 0, 1], [0, 0, 0], [0, 0, 0])
        self.assertEqual(scores["bad_recall"], 0)
        self.assertEqual(scores["bad_precision"], 0)
        self.assertEqual(scores["bad_f1"], 0)
        self.assertEqual(scores["balanced_accuracy"], .5)
        self.assertEqual(scores["roc_auc"], .5)
        self.assertAlmostEqual(scores["cost_per_case"], 5 / 3)

    def test_invalid_labels_or_scores_are_rejected(self):
        for truth, predicted, probability in [
            ([1, 2], [0, 1], [.1, .8]), ([0, 1], [0, 2], [.1, .8]),
            ([0, 1], [0, 1], [.1, np.nan]), ([0, 1], [0, 1], [.1, 1.2]),
            ([0, 1], [0], [.1, .8]),
        ]:
            with self.subTest(truth=truth, probability=probability):
                with self.assertRaises(ValueError):
                    classification_metrics(truth, predicted, probability)

    def test_same_folds_full_coverage_and_no_validation_fit(self):
        X = pd.DataFrame({
            "credit_amount": np.arange(30) ** 2 + 100,
            "duration_months": np.arange(30) + 5,
            "purpose": ["A40", "A41", "A42"] * 10,
            "checking_status": ["A11"] * 30, "savings_status": ["A65"] * 30,
            "employment_duration": ["A72"] * 30, "credit_history": ["A32"] * 30,
        }, index=pd.Index(np.arange(100, 130), name="row_id"))
        y = pd.Series([0, 0, 1] * 10, index=X.index)
        models = {name: build_model_pipeline(DummyClassifier(strategy=strategy))
                  for name, strategy in [("majority", "most_frequent"), ("prior", "prior")]}
        fitted_pipelines = []

        def capture_clone(template):
            fresh = clone(template)
            fitted_pipelines.append(fresh)
            return fresh

        with patch("train.clone", side_effect=capture_clone):
            metrics, predictions = compare_models(X, y, models=models)
        folds = list(StratifiedKFold(n_splits=5, shuffle=True, random_state=42).split(X, y))
        self.assertEqual(len(metrics), 10)
        for model_number, name in enumerate(models):
            rows = predictions[predictions.model == name]
            self.assertEqual(set(rows.row_id), set(X.index))
            self.assertTrue(rows.row_id.is_unique)
            self.assertTrue((rows.predicted_bad_risk == 0).all())
            for fold, (training, validation) in enumerate(folds, start=1):
                self.assertEqual(set(rows[rows.fold == fold].row_id), set(X.index[validation]))
                fitted = fitted_pipelines[model_number * 5 + fold - 1]
                scaler = fitted.named_steps["preprocessing"].named_transformers_["numeric"]
                np.testing.assert_allclose(scaler.mean_, X.iloc[training][NUMERIC_FEATURES].mean())
                self.assertEqual(int(scaler.n_samples_seen_), len(training))
            self.assertFalse(hasattr(models[name].named_steps["model"], "classes_"))
        summary = summarize_folds(metrics)
        np.testing.assert_allclose(summary.balanced_accuracy_mean, .5)
        np.testing.assert_allclose(summary.bad_recall_mean, 0)


if __name__ == "__main__":
    unittest.main()
