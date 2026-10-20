"""Exercise preprocessing boundaries with synthetic data, not held-out cases."""

from io import BytesIO
from pathlib import Path
import sys
import unittest

import joblib
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.exceptions import NotFittedError
from sklearn.model_selection import StratifiedKFold, cross_validate

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
from preprocessing import (  # noqa: E402
    FEATURE_COLUMNS, NUMERIC_FEATURES,
    build_model_pipeline, build_preprocessor,
)


def synthetic_inputs():
    """Small invented fixture; no claim about actual applicant risk."""
    return pd.DataFrame({
        "credit_amount": [100, 200, 300, 400],
        "duration_months": [6, 12, 18, 24],
        "purpose": ["A40", "A41", "A40", "A41"],
        "checking_status": ["A11", "A12", "A11", "A12"],
        "savings_status": ["A61", "A65", "A61", "A65"],
        "employment_duration": ["A72", "A73", "A72", "A73"],
        "credit_history": ["A32", "A33", "A32", "A33"],
    })[FEATURE_COLUMNS]


class PreprocessingTests(unittest.TestCase):
    def test_factory_is_unfitted_and_returns_independent_instances(self):
        first, second = build_preprocessor(), build_preprocessor()
        with self.assertRaises(NotFittedError):
            first.transform(synthetic_inputs())
        first.fit(synthetic_inputs())
        with self.assertRaises(NotFittedError):
            second.transform(synthetic_inputs())

    def test_scaling_and_nominal_one_hot_blocks(self):
        X = synthetic_inputs()
        transformer = build_preprocessor()
        transformed = transformer.fit_transform(X)
        np.testing.assert_allclose(transformed[:, :2].mean(axis=0), 0, atol=1e-12)
        np.testing.assert_allclose(transformed[:, :2].std(axis=0), 1, atol=1e-12)
        encoded = transformed[:, 2:]
        self.assertTrue(set(np.unique(encoded)) <= {0, 1})
        np.testing.assert_array_equal(encoded.sum(axis=1), np.full(4, 5))
        names = transformer.get_feature_names_out().tolist()
        self.assertIn("categorical__savings_status_A65", names)

    def test_validation_does_not_refit_or_learn_unseen_category(self):
        transformer = build_preprocessor().fit(synthetic_inputs())
        scaler = transformer.named_transformers_["numeric"]
        encoder = transformer.named_transformers_["categorical"]
        original_mean = scaler.mean_.copy()
        original_categories = [values.copy() for values in encoder.categories_]
        validation = synthetic_inputs().iloc[[0]].copy()
        validation["credit_amount"] = 10000
        validation["purpose"] = "A48"  # valid source category absent from this training fixture
        transformed = transformer.transform(validation)
        self.assertEqual(transformed.shape[1], len(transformer.get_feature_names_out()))
        purpose_columns = [i for i, name in enumerate(transformer.get_feature_names_out())
                           if name.startswith("categorical__purpose_")]
        self.assertEqual(transformed[0, purpose_columns].sum(), 0)
        self.assertGreater(transformed[0, 0], 10)
        np.testing.assert_array_equal(scaler.mean_, original_mean)
        for actual, before in zip(encoder.categories_, original_categories):
            np.testing.assert_array_equal(actual, before)

    def test_tree_variant_keeps_numeric_values_unscaled(self):
        X = synthetic_inputs()
        values = build_preprocessor(scale_numeric=False).fit_transform(X)
        np.testing.assert_array_equal(values[:, :2], X[NUMERIC_FEATURES].to_numpy())

    def test_extra_target_and_row_id_are_not_model_inputs(self):
        X = synthetic_inputs()
        transformer = build_preprocessor()
        expected = transformer.fit_transform(X)
        expanded = X.assign(bad_risk=[0, 1, 0, 1], row_id=[10, 11, 12, 13])
        actual = build_preprocessor().fit_transform(expanded)
        np.testing.assert_array_equal(actual, expected)
        reordered = X[list(reversed(FEATURE_COLUMNS))]
        np.testing.assert_array_equal(transformer.transform(reordered), expected)

    def test_missing_required_feature_is_rejected(self):
        transformer = build_preprocessor().fit(synthetic_inputs())
        with self.assertRaises(ValueError):
            transformer.transform(synthetic_inputs().drop(columns="purpose"))

    def test_cross_validation_learns_scaler_from_each_training_fold(self):
        X = synthetic_inputs()
        X.loc[3, "credit_amount"] = 1000  # avoid coincidentally equal fold/global means
        y = np.array([0, 1, 0, 1])
        folds = list(StratifiedKFold(n_splits=2, shuffle=True, random_state=42).split(X, y))
        original_model = DummyClassifier(strategy="most_frequent")
        pipeline = build_model_pipeline(original_model)
        result = cross_validate(
            pipeline, X, y, cv=folds, return_estimator=True, scoring="balanced_accuracy",
        )
        for fitted, (training, validation) in zip(result["estimator"], folds):
            scaler = fitted.named_steps["preprocessing"].named_transformers_["numeric"]
            np.testing.assert_allclose(scaler.mean_, X.iloc[training][NUMERIC_FEATURES].mean())
            self.assertEqual(int(scaler.n_samples_seen_), len(training))
            self.assertNotEqual(float(scaler.mean_[0]), float(X["credit_amount"].mean()))
        self.assertFalse(hasattr(original_model, "classes_"))
        self.assertFalse(hasattr(pipeline.named_steps["preprocessing"], "transformers_"))

    def test_fitted_preprocessor_survives_serialization(self):
        transformer = build_preprocessor().fit(synthetic_inputs())
        buffer = BytesIO()
        joblib.dump(transformer, buffer)
        buffer.seek(0)
        restored = joblib.load(buffer)
        np.testing.assert_array_equal(
            restored.transform(synthetic_inputs()), transformer.transform(synthetic_inputs()),
        )


if __name__ == "__main__":
    unittest.main()
