"""Report safety checks without importing ML libraries or running models."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "smoke_local_model.py"


class SmokeReportTests(unittest.TestCase):
    def test_existing_report_is_not_overwritten_before_runtime_import(self):
        with tempfile.TemporaryDirectory(prefix="cot-report-test-") as directory:
            report = Path(directory) / "report.json"
            original = '{"artifact_kind":"test_sentinel"}\n'
            report.write_text(original, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--output", str(report)],
                capture_output=True, text=True, timeout=5,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("FileExistsError", result.stderr)
            self.assertEqual(report.read_text(encoding="utf-8"), original)

    def test_atomic_progress_preserves_assigned_and_failed_attempt(self):
        spec = importlib.util.spec_from_file_location("smoke_report_test", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory(prefix="cot-report-test-") as directory:
            module._OUTPUT = Path(directory) / "report.json"
            module._REPORT = {
                "artifact_kind": "test_fixture_not_model_observations",
                "status": "generating", "assigned_actor_attempts": 1,
                "samples": [{"attempt": 0, "status": "assigned"}],
            }
            module.save_progress()
            module._REPORT.update(status="failed", error_type="TestFailure")
            module.save_progress()
            saved = json.loads(module._OUTPUT.read_text(encoding="utf-8"))
            self.assertEqual(saved["assigned_actor_attempts"], 1)
            self.assertEqual(saved["samples"][0]["status"], "assigned")
            self.assertEqual(saved["status"], "failed")
            self.assertFalse(module._OUTPUT.with_name("report.json.tmp").exists())


if __name__ == "__main__":
    unittest.main()
