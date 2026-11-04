"""Exercise process ownership/timeouts with tiny dummy workers, never ML."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load_watchdog():
    spec = importlib.util.spec_from_file_location("watchdog_test", ROOT / "scripts/run_local_study.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def dummy_launcher(module, snippet, children):
    def launch(command, **kwargs):
        child = subprocess.Popen([sys.executable, "-u", "-c", snippet], **kwargs)
        children.append(child)
        return child
    module.subprocess = SimpleNamespace(
        Popen=launch, PIPE=subprocess.PIPE, STDOUT=subprocess.STDOUT,
        TimeoutExpired=subprocess.TimeoutExpired,
        CREATE_NO_WINDOW=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )


class StudyWatchdogTests(unittest.TestCase):
    def test_completed_owned_dummy_worker_is_recorded(self):
        module, children = load_watchdog(), []
        dummy_launcher(module, "print('dummy-completed', flush=True)", children)
        with tempfile.TemporaryDirectory(prefix="cot-watchdog-") as directory:
            output = Path(directory) / "new-run"
            with patch.object(sys, "argv", ["runner", "--output-dir", str(output)]), contextlib.redirect_stdout(io.StringIO()):
                code = module.main()
            report = json.loads(output.with_name(output.name + ".watchdog.json").read_text())
            self.assertEqual(code, 0)
            self.assertEqual(report["status"], "completed")
            self.assertEqual(report["child_exit_code"], 0)
            self.assertFalse(report["terminated_owned_child"])
            self.assertIsNotNone(children[0].poll())

    def test_timeout_terminates_only_the_owned_dummy_and_keeps_report(self):
        module, children = load_watchdog(), []
        dummy_launcher(module, "import time; time.sleep(30)", children)
        ticks = iter([0.0, 31.0, 32.0])
        module.time = SimpleNamespace(monotonic=lambda: next(ticks), sleep=time.sleep)
        with tempfile.TemporaryDirectory(prefix="cot-watchdog-") as directory:
            output = Path(directory) / "new-run"
            with patch.object(sys, "argv", ["runner", "--output-dir", str(output), "--wall-seconds", "30"]), contextlib.redirect_stdout(io.StringIO()):
                code = module.main()
            report = json.loads(output.with_name(output.name + ".watchdog.json").read_text())
            self.assertEqual(code, 124)
            self.assertEqual(report["status"], "hard_timeout")
            self.assertTrue(report["terminated_owned_child"])
            self.assertEqual(report["child_pid"], children[0].pid)
            self.assertIsNotNone(children[0].poll())

    def test_interrupt_cleans_up_owned_dummy(self):
        module, children = load_watchdog(), []
        dummy_launcher(module, "import time; time.sleep(30)", children)
        calls = [0]
        def interrupted_clock():
            calls[0] += 1
            if calls[0] == 2:
                raise KeyboardInterrupt()
            return float(calls[0])
        module.time = SimpleNamespace(monotonic=interrupted_clock, sleep=time.sleep)
        with tempfile.TemporaryDirectory(prefix="cot-watchdog-") as directory:
            output = Path(directory) / "new-run"
            with patch.object(sys, "argv", ["runner", "--output-dir", str(output)]), contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(KeyboardInterrupt):
                    module.main()
            report = json.loads(output.with_name(output.name + ".watchdog.json").read_text())
            self.assertEqual(report["status"], "parent_interrupted")
            self.assertTrue(report["terminated_owned_child"])
            self.assertIsNotNone(children[0].poll())

    def test_existing_output_is_refused_before_worker_launch(self):
        module = load_watchdog()
        with tempfile.TemporaryDirectory(prefix="cot-watchdog-") as directory:
            with patch.object(sys, "argv", ["runner", "--output-dir", directory]), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as caught:
                    module.main()
            self.assertEqual(caught.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
