"""Check the expanded comparison without calling a paid API."""

from hashlib import sha256
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
import genai_comparison as comparison


class ExpandedComparisonTests(unittest.TestCase):
    def test_recorded_assessment_matches_all_attempts_and_objective_counts(self):
        folder = comparison.OUTPUT
        if not (folder / "assessment.json").exists():
            self.skipTest("Expanded comparison not yet recorded.")
        protocol = json.loads((folder / "protocol.json").read_text())
        assessment = json.loads((folder / "assessment.json").read_text(encoding="utf-8"))
        records = [json.loads(line) for line in
                   (folder / "attempts.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertEqual(len(records), protocol["planned_requests"])
        self.assertEqual(len(assessment["results"]), len(records))
        self.assertEqual(assessment["protocol_sha256"], sha256((folder / "protocol.json").read_bytes()).hexdigest())
        self.assertEqual(assessment["attempts_sha256"], sha256((folder / "attempts.jsonl").read_bytes()).hexdigest())
        self.assertEqual(protocol["source_fingerprints"], comparison.fingerprints())
        for trial, record, review in zip(protocol["order"], records, assessment["results"]):
            for key, value in trial.items():
                self.assertEqual(record[key], value)
                self.assertEqual(review[key], value)
            self.assertEqual(record["prompt"], protocol["prompts"][trial["scenario"]][trial["variant"]])
            self.assertEqual(record["status"], "completed")
            words = len(record["output_text"].split())
            self.assertEqual(review["word_count"], words)
            self.assertEqual(review["criteria"]["word_limit"]["pass"], 120 <= words <= 180)
        for summary in assessment["summary"]:
            group = [row for row in assessment["results"] if row["variant"] == summary["variant"]
                     and (summary["scenario"] == "all" or row["scenario"] == summary["scenario"])]
            self.assertEqual(summary["responses"], len(group))
            for criterion, count in summary["passes"].items():
                self.assertEqual(count, sum(row["criteria"][criterion]["pass"] for row in group))

    def test_synthetic_arithmetic_and_labels_do_not_change_actual_results(self):
        contexts = comparison.scenarios()
        self.assertEqual(contexts["actual_results"]["test_metrics"]["true_bad"], 46)
        low = contexts["high_accuracy_low_detection"]
        self.assertIn("SYNTHETIC", low["evidence_type"])
        self.assertEqual(low["test_metrics"]["accuracy"], .9)
        self.assertEqual(low["test_metrics"]["bad_recall"], .2)
        self.assertEqual(low["test_metrics"]["cost_per_case"], .42)
        high = contexts["high_detection_many_false_flags"]
        self.assertEqual(high["test_metrics"]["bad_recall"], .9)
        self.assertEqual(high["test_metrics"]["false_rejections"], 55)
        self.assertNotIn("roc_auc", high["test_metrics"])
        with self.assertRaises(ValueError):
            comparison.count_metrics(1, 0, 0, 0)

    def test_protocol_is_balanced_reproducible_and_cannot_be_overwritten(self):
        with tempfile.TemporaryDirectory() as folder:
            first = comparison.prepare(Path(folder) / "first")
            second = comparison.prepare(Path(folder) / "second")
            self.assertEqual(first["order"], second["order"])
            self.assertEqual(len(first["order"]), 30)
            for name in first["contexts"]:
                for variant in ["simple", "structured"]:
                    trials = [trial for trial in first["order"]
                              if trial["scenario"] == name and trial["variant"] == variant]
                    self.assertEqual(sorted(t["repetition"] for t in trials), [1, 2, 3, 4, 5])
            with self.assertRaises(FileExistsError):
                comparison.prepare(Path(folder) / "first")

    def test_plan_cannot_run_if_source_files_change(self):
        with tempfile.TemporaryDirectory() as folder:
            comparison.prepare(folder)
            with patch.object(comparison, "fingerprints", return_value={}):
                with self.assertRaises(ValueError):
                    comparison.run(folder)
            self.assertFalse((Path(folder) / "attempts.jsonl").exists())

    def test_all_trials_use_their_planned_context_and_reruns_are_blocked(self):
        with tempfile.TemporaryDirectory() as folder:
            protocol = comparison.prepare(folder)
            with (patch("genai.get_api_key", return_value="synthetic-test-key"),
                  patch("genai.generate_explanation", side_effect=lambda *a, **k:
                        {"status": "completed", "output_text": "Offline fixture only."}) as generate):
                comparison.run(folder)
                self.assertEqual(generate.call_count, 30)
                for trial, call in zip(protocol["order"], generate.call_args_list):
                    self.assertEqual(call.args[0], trial["variant"])
                    self.assertEqual(call.kwargs["context"], protocol["contexts"][trial["scenario"]])
                with self.assertRaises(FileExistsError):
                    comparison.run(folder)

    def test_failure_is_retained_without_secrets_or_retry(self):
        with tempfile.TemporaryDirectory() as folder:
            comparison.prepare(folder)
            with (patch("genai.get_api_key", return_value="synthetic-test-key"),
                  patch("genai.generate_explanation", side_effect=RuntimeError("secret-provider-body")) as generate):
                comparison.run(folder)
                generate.assert_called_once()
            text = (Path(folder) / "attempts.jsonl").read_text()
            self.assertIn("RuntimeError", text)
            self.assertNotIn("secret-provider-body", text)
            self.assertNotIn("synthetic-test-key", text)


if __name__ == "__main__":
    unittest.main()
