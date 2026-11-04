"""Run the local study worker with a hard, process-level wall-clock limit."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
import time

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--states", type=int, default=4, choices=range(1,9))
    parser.add_argument("--max-new-tokens", type=int, default=512)
    parser.add_argument("--wall-seconds", type=int, default=1200)
    parser.add_argument("--allow-download", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.max_new_tokens <= 512:
        parser.error("max-new-tokens must be in 1..512")
    if not 30 <= args.wall_seconds <= 1800:
        parser.error("wall-seconds must be in 30..1800")
    output = Path(args.output_dir).resolve()
    if output.exists():
        parser.error("output-dir must be new; previous observations are never overwritten")
    output.parent.mkdir(parents=True, exist_ok=True)
    ledger = output.with_name(output.name + ".watchdog.json")
    log_path = output.with_name(output.name + ".worker.log")
    if ledger.exists() or log_path.exists():
        parser.error("watchdog/log path already exists; choose a new run name")
    command = [
        sys.executable, "-u", "-m", "cot_monitoring_local.model_study",
        "--output-dir", str(output), "--states", str(args.states),
        "--max-trials", str(args.states * 4),
        "--max-new-tokens", str(args.max_new_tokens),
        "--wall-seconds", str(args.wall_seconds),
    ]
    if args.allow_download:
        command.append("--allow-download")
    report = {
        "artifact_kind": "local_study_process_watchdog",
        "status": "starting", "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "hard_wall_seconds": args.wall_seconds, "requested_trials": args.states*4,
        "max_generated_tokens": args.states*4*args.max_new_tokens,
        "child_exit_code": None, "terminated_owned_child": False,
    }
    def save():
        temporary = ledger.with_name(ledger.name + ".tmp")
        temporary.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
        temporary.replace(ledger)
    with ledger.open("x",encoding="utf-8") as f:
        f.write(json.dumps(report,indent=2)+"\n")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT/"src")
    env["PYTHONUNBUFFERED"] = "1"
    start = time.monotonic()
    with log_path.open("x",encoding="utf-8") as log:
        child = subprocess.Popen(
            command, cwd=ROOT, env=env, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace",
            creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0),
        )
        reader = None
        try:
            report.update(status="running", child_pid=child.pid)
            save()
            def drain():
                for line in child.stdout:
                    log.write(line)
                    log.flush()
                    print(line,end="",flush=True)
            reader = threading.Thread(target=drain,daemon=True)
            reader.start()
            while child.poll() is None:
                if time.monotonic()-start > args.wall_seconds:
                    report.update(status="hard_timeout",terminated_owned_child=True)
                    child.terminate()
                    try:
                        child.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        child.kill()
                        child.wait()
                    break
                time.sleep(0.1)
        except BaseException:
            report.update(status="parent_interrupted",terminated_owned_child=True)
            if child.poll() is None:
                child.terminate()
                try:
                    child.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    child.kill()
                    child.wait()
            raise
        finally:
            if reader is not None:
                reader.join(timeout=5)
            report["elapsed_seconds"] = time.monotonic()-start
            report["child_exit_code"] = child.poll()
            if report["status"] == "running":
                report["status"] = "completed" if child.returncode==0 else "child_failed"
            report["ended_at_utc"] = datetime.now(timezone.utc).isoformat()
            save()
    print(json.dumps(report),flush=True)
    return 0 if report["status"]=="completed" else 124 if report["status"]=="hard_timeout" else (child.returncode or 1)

if __name__=="__main__":
    raise SystemExit(main())
