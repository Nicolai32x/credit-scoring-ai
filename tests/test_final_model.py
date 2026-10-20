"""Synthetic final-assessment checks; never evaluate the project's test partition."""

import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
from final_model import load_decision, predict_risk, run_final_assessment  # noqa: E402


class FixedScorePipeline:
    # Deliberately reversed class order checks selection of the bad-class column.
    classes_ = np.array([1, 0])

    def predict_proba(self, X):
        return np.array([[.49, .51], [.5, .5], [.8, .2]])


class FinalModelTests(unittest.TestCase):
    def test_saved_threshold_and_positive_class_order(self):
        X = pd.DataFrame({"invented_input": [1, 2, 3]}, index=[20, 30, 40])
        output = predict_risk({"pipeline": FixedScorePipeline(), "threshold": .5}, X)
        self.assertEqual(output.predicted_bad_risk.tolist(), [0, 1, 1])
        self.assertEqual(output.index.tolist(), [20, 30, 40])
        alternative = predict_risk({"pipeline": FixedScorePipeline(), "threshold": .7}, X)
        self.assertEqual(alternative.predicted_bad_risk.tolist(), [0, 0, 1])

    def test_existing_final_output_stops_before_loading_any_data(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder)
            (output / "final_test.json").write_text("{}")
            with patch("final_model.load_partition") as loader:
                with self.assertRaises(FileExistsError):
                    run_final_assessment(output_dir=output)
                loader.assert_not_called()

    def test_modified_decision_is_rejected_before_test_access(self):
        from final_model import DECISION_PATH
        decision = json.loads(DECISION_PATH.read_text(encoding="utf-8"))
        decision["threshold"] = .1
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "decision.json"
            path.write_text(json.dumps(decision), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_decision(path)


if __name__ == "__main__":
    unittest.main()
