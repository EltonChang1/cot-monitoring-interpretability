# Local setup and readiness

This is the 0.3 engineering profile, not the deferred full study. Current result: [host-RAM gate blocked model execution](results-template.md). Do not infer readiness from installed packages alone.

## Existing workspace

An ignored .venv was created with access to existing system packages so the already installed CUDA Torch did not need another large download. Model-loading additions are pinned in [requirements-local.txt](../requirements-local.txt). These direct pins are not a claim of a fully hermetic environment; observed Torch and hardware are recorded in the [audit](resource-audit.json).

Offline apparatus:

    python -m unittest discover -s tests -v
    python scripts/validate_plan.py
    $env:PYTHONPATH = 'src'
    python -m cot_monitoring_local --count 4

Runtime import check:

    .venv\Scripts\python.exe -c "import torch, transformers; print(torch.__version__, transformers.__version__)"

The smoke script checks current RAM after runtime initialization. Its 3 GiB requirement is higher than the latest observed headroom, so the current result is blocked. It also checks CUDA/BF16, free VRAM, and disk. No background retry or application shutdown is performed.

## Recreating the local environment

On this same host, only if .venv is absent:

    uv venv .venv --system-site-packages --python C:\Users\trena\AppData\Local\Programs\Python\Python312\python.exe

Install additions into that environment, not global Python:

    uv pip install --python .venv\Scripts\python.exe -r requirements-local.txt

A different host must separately verify its CUDA Torch installation; these commands do not install or validate a GPU driver. No cloud account, paid GPU, or API credit is assumed.

## Bounded model smoke

Offline is the default:

    .venv\Scripts\python.exe scripts/smoke_local_model.py --output runs/local-resource-smoke/report.json

Only when the resource gates pass, explicit --allow-download permits acquiring the one pinned public checkpoint. The published checkpoint file is 1,503,300,328 bytes; tokenizer metadata and cache duplication are additional. Cache location is under the user's home .cache/cot-monitoring-interpretability directory, outside the source tree. Remote model code is disabled and only safetensors weights are accepted.

The script is limited to four actor attempts, each at 512 new tokens, plus five forward-only smoke/stress calls. Setup/cache has a conservative preflight reservation and measured post-acquisition check, not an OS quota. Its 120-second timeout is cooperative between decode steps; there is no hard worker timeout for loading/prefill/forward calls. It does not implement the 32-attempt batch, its cumulative guard ledger, pre-action activation alignment, or historical cached replay. Those remain requirements before a batch. Do not represent this smoke as an experiment on monitoring accuracy.

Guard reports and raw traces go to ignored runs/. Choose a unique output path: the script refuses to overwrite an existing report. It atomically saves assignment/progress/failures and preserves raw token IDs and special-token text when generation occurs. Record a new summarized result only from actual observations. A blocked guard does not acquire a checkpoint, consume an actor generation attempt, or produce a safe model outcome.
