"""Exercise the real Streamlit form with fictional profiles, without fitting."""

from pathlib import Path
import sys
import unittest
from unittest.mock import patch

import joblib
import pandas as pd
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
from final_model import predict_risk  # noqa: E402


class DemoTests(unittest.TestCase):
    def test_form_and_fictional_predictions_reuse_saved_pipeline(self):
        bundle = joblib.load(ROOT / "results/selected_pipeline.joblib")
        app = AppTest.from_file(str(ROOT / "demo/app.py"), default_timeout=30)
        with (patch("sklearn.pipeline.Pipeline.fit", side_effect=AssertionError("Demo must not fit")),
              patch("final_model.load_partition", side_effect=AssertionError("Demo must not load partitions"))):
            app.run()
            self.assertEqual(len(app.exception), 0)
            self.assertEqual(len(app.number_input), 2)
            self.assertEqual(len(app.selectbox), 5)
            self.assertEqual(len(app.button), 1)
            self.assertFalse(any("Predicted class:" in element.value for element in app.info))
            self.assertEqual(app.number_input(key="credit_amount").min, 276)
            self.assertEqual(app.number_input(key="credit_amount").max, 15945)
            self.assertEqual(app.number_input(key="duration_months").max, 60)
            self.assertIn("Unknown / no savings account", app.selectbox(key="savings_status").options)
            self.assertNotIn("Vacation", app.selectbox(key="purpose").options)

            for amount, months, purpose, checking, savings, employment, history in [
                (3000, 12, "A42", "A12", "A62", "A74", "A32"),
                (9000, 48, "A40", "A11", "A61", "A72", "A33"),
                (3000, 12, "A42", "A14", "A65", "A74", "A32"),
            ]:
                app.number_input(key="credit_amount").set_value(amount)
                app.number_input(key="duration_months").set_value(months)
                values = dict(zip(bundle["feature_columns"],
                                  [amount, months, purpose, checking, savings, employment, history]))
                for key in ["purpose", "checking_status", "savings_status", "employment_duration", "credit_history"]:
                    app.selectbox(key=key).set_value(values[key])
                app.button[0].click().run()
                self.assertEqual(len(app.exception), 0)
                raw = pd.DataFrame([values], columns=bundle["feature_columns"])
                expected = int(predict_risk(bundle, raw).predicted_bad_risk.iloc[0])
                label = "Bad risk" if expected else "Good risk"
                self.assertTrue(any(element.value == f"Predicted class: {label}" for element in app.info))
                self.assertEqual(len(app.table), 1)
                self.assertEqual(len(app.table[0].value), 7)
            self.assertTrue(any("40 of 140 good risks" in item.value for item in app.markdown))


if __name__ == "__main__":
    unittest.main()
