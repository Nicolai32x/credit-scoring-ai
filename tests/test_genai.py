"""Offline checks with synthetic API replies; never spend API credits in tests."""

import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock, patch

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
import genai  # noqa: E402


class GenAITests(unittest.TestCase):
    def test_request_contains_aggregate_facts_and_fixed_settings_only(self):
        client = MagicMock()
        client.responses.create.return_value = SimpleNamespace(
            usage=None, model=genai.MODEL, id="synthetic-test-id", status="completed",
            output_text="Synthetic offline test response, not an experiment result.",
        )
        result = genai.generate_explanation(client=client)
        kwargs = client.responses.create.call_args.kwargs
        self.assertFalse(kwargs["store"])
        self.assertEqual(kwargs["max_output_tokens"], 800)
        self.assertEqual(kwargs["model"], genai.MODEL)
        self.assertEqual(kwargs["reasoning"], {"effort": "none"})
        self.assertEqual(result["status"], "completed")
        self.assertIn('"false_rejections": 40', kwargs["input"])
        self.assertNotIn('"credit_amount"', kwargs["input"])
        self.assertNotIn("OPENAI_API_KEY", kwargs["input"])
        self.assertNotIn("tools", kwargs)

    def test_six_attempts_are_recorded_and_rerun_is_blocked(self):
        fake = {"status": "completed", "output_text": "Synthetic fixture only."}
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "experiment"
            with (patch("genai.get_api_key", return_value="synthetic-key"),
                  patch("genai.generate_explanation", return_value=fake.copy()) as generate):
                genai.run_experiment(output)
                self.assertEqual(generate.call_count, 6)
                self.assertEqual([call.args[0] for call in generate.call_args_list],
                                 ["simple", "structured"] * 3)
                rows = [json.loads(line) for line in (output / "attempts.jsonl").read_text().splitlines()]
                self.assertEqual([row["attempt"] for row in rows], list(range(1, 7)))
                with self.assertRaises(FileExistsError):
                    genai.run_experiment(output)
                self.assertEqual(generate.call_count, 6)

    def test_failure_is_logged_without_provider_body_and_stops_calls(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "experiment"
            with (patch("genai.get_api_key", return_value="synthetic-key"),
                  patch("genai.generate_explanation", side_effect=RuntimeError("private-provider-body")) as generate):
                genai.run_experiment(output)
                self.assertEqual(generate.call_count, 1)
            log = (output / "attempts.jsonl").read_text()
            self.assertIn("RuntimeError", log)
            self.assertNotIn("private-provider-body", log)
            self.assertNotIn("synthetic-key", log)

    def test_no_key_does_not_create_experiment_outputs(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "experiment"
            with patch("genai.get_api_key", return_value=""):
                with self.assertRaises(ValueError):
                    genai.run_experiment(output)
            self.assertFalse(output.exists())

    def test_live_button_is_explicit_and_ml_result_survives_ai_rerun(self):
        reply = {"status": "completed", "output_text": "Synthetic UI test explanation."}
        with (patch("genai.get_api_key", return_value="synthetic-key"),
              patch("genai.generate_explanation", return_value=reply) as generate):
            app = AppTest.from_file(str(ROOT / "demo/app.py"), default_timeout=30).run()
            generate.assert_not_called()
            app.button(key="predict_class").click().run()
            generate.assert_not_called()
            prediction_before = [item.value for item in app.info if item.value.startswith("Predicted class:")]
            app.button(key="generate_explanation").click().run()
            self.assertEqual(len(app.exception), 0)
            generate.assert_called_once()
            self.assertEqual(prediction_before, [item.value for item in app.info
                                                if item.value.startswith("Predicted class:")])
            self.assertTrue(any(item.value == reply["output_text"] for item in app.markdown))
            generate.side_effect = RuntimeError("Do not display this provider error")
            app.button(key="generate_explanation").click().run()
            self.assertEqual(len(app.exception), 0)
            self.assertTrue(any("unavailable" in item.value for item in app.warning))
            self.assertFalse(any("Do not display" in item.value for item in app.markdown))


if __name__ == "__main__":
    unittest.main()
