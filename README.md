# CoT Monitoring & Interpretability

Latest requested execution: [completed 16-trial rerun](results/2026-11-04-requested-run-02/README.md), with its [RAM-interrupted first attempt](results/2026-11-04-requested-run-01/README.md) preserved separately.

**The default local study is executable and has been run.** Protocol 0.4 uses a pinned Qwen3-0.6B model on the available RTX 3060; it studies shortcut-pressure behavior and a fixed CoT warning diagnostic on a small synthetic ledger panel.

The November 4 run completed all **16 assigned trials in about 7 minutes**. It saved 13 pre-action activation readouts. Eight actions were valid, successful, and nonviolating; five completed outputs were malformed, and three hit the token cap. These eight unknown labels make the behavioral and monitoring conclusions inconclusive. They are preserved, not repaired or discarded.

## Run the study

From this repository in the prepared local environment:

    .venv\Scripts\python.exe scripts/run_local_study.py --output-dir runs/NEW-RUN --states 4 --max-new-tokens 512 --wall-seconds 1200

The output path must be new. The pinned checkpoint is now cached locally, so the default is offline. The parent supervises only its own worker, with a hard 20-minute limit while the supervisor remains alive. Live RAM/VRAM checks still apply; current workload can change.

Verify an output without generating more model data:

    .venv\Scripts\python.exe scripts/verify_local_run.py --run-dir runs/NEW-RUN --verify-token-text

## Inspect the actual work

- [Protocol](docs/experiment.md) and [configuration](configs/pilot.json).
- [Measured results](docs/results-template.md).
- [Published observations, tokens, and activation vectors](results/2026-11-04-local-study/progress.json).
- [Small result summary](results/2026-11-04-local-study/summary.json), [verification](results/2026-11-04-local-study/verification.json), and [frozen assignments](results/2026-11-04-local-study/assigned-plan.json).
- [Local setup](docs/local-setup.md), [record contract](docs/trial-record.md), and [resource history](docs/resource-audit.json).
- [Research references](docs/references.md) and [earlier resource critique](docs/resource-critique-v0.2.md).

## Checks and scope

    python -m unittest discover -s tests -v
    python scripts/validate_plan.py

All 27 unit tests pass, including token-boundary alignment, strict checking, missing-label counts, atomic reports, and watchdog timeout/interrupt tests using dummy processes.

This study has one shared toy template, no learned monitor or fusion, and no population inference, awareness-suppression result, or circuit claim. The [larger v0.2 design](docs/full-study-v0.2.md) remains deferred; running this small study does not qualify its 8B comparator or compute budget.

All proposals are inert synthetic JSON. Model weights and environments stay outside Git; published observations contain only constructed tasks. No paid compute was used. No project software/content license has been selected.
