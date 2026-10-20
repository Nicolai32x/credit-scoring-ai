"""Check exact local model contributions and submitted-profile UI behavior."""

import copy
import json
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock, patch

import joblib
import numpy as np
import pandas as pd
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
from explain import profile_context  # noqa: E402
from final_model import predict_risk  # noqa: E402
from genai import generate_explanation, request_text  # noqa: E402


class ProfileExplanationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = joblib.load(ROOT / "results/selected_pipeline.joblib")
        cls.reference = json.loads((ROOT / "results/explanation_reference.json").read_text())

    def profile(self, amount=3000):
        return pd.DataFrame([[amount, 12, "A42", "A12", "A62", "A74", "A32"]],
                            columns=self.bundle["feature_columns"])

    def test_contributions_reconstruct_saved_model_and_class_for_fictional_profiles(self):
        with patch("sklearn.pipeline.Pipeline.fit", side_effect=AssertionError("No refitting")):
            for amount in [276, 3000, 9000, 15945]:
                inputs = self.profile(amount)
                context = profile_context(self.bundle, inputs, self.reference)
                expected = float(self.bundle["pipeline"].decision_function(inputs)[0])
                reconstructed = context["reference_logit"] + sum(
                    item["contribution_logit_units"] for item in context["contributions"])
                self.assertAlmostEqual(reconstructed, expected, places=10)
                label = "Bad risk" if int(predict_risk(self.bundle, inputs).predicted_bad_risk.iloc[0]) else "Good risk"
                self.assertEqual(context["predicted_class"], label)
                self.assertEqual({item["feature"] for item in context["contributions"]},
                                 set(self.bundle["feature_columns"]))
                self.assertEqual(len(context["contributions"]), 7)

    def test_amount_direction_matches_centered_coefficient_math(self):
        inputs = self.profile(9000)
        context = profile_context(self.bundle, inputs, self.reference)
        pipeline = self.bundle["pipeline"]
        prep = pipeline.named_steps["preprocessing"]
        index = list(prep.get_feature_names_out()).index("numeric__credit_amount")
        expected = ((prep.transform(inputs)[0, index]
                    - self.reference["mean_transformed_development_inputs"][index])
                    * pipeline.named_steps["model"].coef_[0, index])
        actual = next(row for row in context["contributions"] if row["feature"] == "credit_amount")
        self.assertAlmostEqual(actual["contribution_logit_units"], expected)
        self.assertEqual(actual["direction"], "toward Bad risk" if expected > 0 else "toward Good risk")

    def test_mismatched_reference_or_unknown_category_is_rejected(self):
        reference = copy.deepcopy(self.reference)
        reference["pipeline_sha256"] = "wrong"
        with self.assertRaises(ValueError):
            profile_context(self.bundle, self.profile(), reference)
        inputs = self.profile()
        inputs.loc[0, "purpose"] = "A47"
        with self.assertRaises(ValueError):
            profile_context(self.bundle, inputs, self.reference)

    def test_profile_request_requires_explicit_context_and_uses_it(self):
        with self.assertRaises(ValueError):
            request_text("profile")
        context = profile_context(self.bundle, self.profile(9000), self.reference)
        client = MagicMock()
        client.responses.create.return_value = SimpleNamespace(
            usage=None, model="synthetic", id="synthetic", status="completed", output_text="Test fixture.")
        generate_explanation("profile", context=context, client=client)
        prompt = client.responses.create.call_args.kwargs["input"]
        self.assertIn('"credit_amount": 9000', prompt)
        self.assertIn('"contribution_logit_units"', prompt)
        self.assertIn('"predicted_class"', prompt)
        self.assertNotIn('"test_metrics"', prompt)

    def test_ui_sends_last_submitted_snapshot_and_clears_stale_explanation(self):
        reply = {"status": "completed", "output_text": "Synthetic profile explanation."}
        with (patch("genai.get_api_key", return_value="synthetic-key"),
              patch("genai.generate_explanation", return_value=reply) as generate):
            app = AppTest.from_file(str(ROOT / "demo/app.py"), default_timeout=30).run()
            app.button(key="predict_class").click().run()
            generate.assert_not_called()
            app.number_input(key="credit_amount").set_value(9000)
            app.button(key="explain_profile").click().run()
            self.assertEqual(len(app.exception), 0)
            self.assertEqual(generate.call_args.args[0], "profile")
            self.assertEqual(generate.call_args.kwargs["context"]["submitted_profile"]["credit_amount"], 3000)
            self.assertIn("english_input_descriptions", generate.call_args.kwargs["context"])
            self.assertTrue(any(item.value == reply["output_text"] for item in app.markdown))
            # Submit a new form batch after the separate explanation-button rerun.
            app.number_input(key="credit_amount").set_value(9000)
            app.button(key="predict_class").click().run()
            self.assertFalse(any(item.value == reply["output_text"] for item in app.markdown))
            self.assertEqual(len(app.exception), 0)
            app.button(key="explain_profile").click().run()
            self.assertEqual(generate.call_args.kwargs["context"]["submitted_profile"]["credit_amount"], 9000)


if __name__ == "__main__":
    unittest.main()
