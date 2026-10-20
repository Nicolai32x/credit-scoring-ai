"""Regression checks for shared-module reloading and safe error messages."""

import os
from pathlib import Path
import runpy
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
from genai import explanation_error_message  # noqa: E402


class DemoStartupTests(unittest.TestCase):
    def test_launcher_puts_shared_code_on_pythonpath_before_streamlit_starts(self):
        namespace = runpy.run_path(str(ROOT / "demo/run.py"), run_name="test_launcher")
        with (patch("subprocess.call", return_value=0) as call,
              patch.dict(os.environ, {"PYTHONPATH": "existing-module-directory"}),
              patch.object(sys, "argv", ["demo/run.py"])):
            self.assertEqual(namespace["main"](), 0)
        args, kwargs = call.call_args
        self.assertEqual(kwargs["cwd"], ROOT)
        paths = kwargs["env"]["PYTHONPATH"].split(os.pathsep)
        self.assertEqual(paths[0], str(ROOT / "code"))
        self.assertIn("existing-module-directory", paths)
        self.assertEqual(args[0][:4], [sys.executable, "-m", "streamlit", "run"])
        self.assertIn("127.0.0.1", args[0])

    def test_error_messages_are_actionable_without_provider_body_or_key(self):
        stale = TypeError("generate_explanation() got an unexpected keyword argument 'context'")
        self.assertIn("Restart", explanation_error_message(stale))
        for name, code, phrase in [
            ("AuthenticationError", None, "rejected"),
            ("RateLimitError", "insufficient_quota", "billing"),
            ("RateLimitError", "rate_limit_exceeded", "Wait"),
            ("APITimeoutError", None, "timed out"),
            ("APIConnectionError", None, "connect"),
        ]:
            error = type(name, (Exception,), {})("private body sk-synthetic-secret")
            error.code = code
            message = explanation_error_message(error)
            self.assertIn(phrase, message)
            self.assertNotIn("sk-synthetic-secret", message)
            self.assertNotIn("private body", message)


if __name__ == "__main__":
    unittest.main()
