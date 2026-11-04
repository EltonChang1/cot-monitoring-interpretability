# Local setup and executable study

The small model now loads and the 16-trial study has [completed](results-template.md). The previous RAM block is preserved in [resource history](resource-audit.json); it is no longer the current run status.

## Prepared environment

The ignored .venv reuses the existing system Torch 2.6.0+cu118. Model-loading additions are pinned in [requirements-local.txt](../requirements-local.txt). Transformers 4.57.1, the tokenizer, BF16 CUDA generation, and checkpoint hooks have now executed successfully. Direct dependency pins are not a claim of a fully hermetic environment.

On this host, only if .venv is absent:

    uv venv .venv --system-site-packages --python C:\Users\trena\AppData\Local\Programs\Python\Python312\python.exe
    uv pip install --python .venv\Scripts\python.exe -r requirements-local.txt

A different host must independently establish a compatible Torch/CUDA environment. No API credit, cloud GPU, or paid compute is assumed.

## Run and verify

From the repository root, choose a new run name:

    .venv\Scripts\python.exe scripts/run_local_study.py --output-dir runs/NEW-RUN --states 4 --max-new-tokens 512 --wall-seconds 1200
    .venv\Scripts\python.exe scripts/verify_local_run.py --run-dir runs/NEW-RUN --verify-token-text

The default is offline. The pinned checkpoint is cached under the user's .cache/cot-monitoring-interpretability directory, outside the source tree. For a fresh cache, first use scripts/smoke_local_model.py with --allow-download and a new --output path; that setup path checks the separate disk/cache budget. Remote model code is disabled and safetensors is required. The default study's resource qualification covers cached execution, not an unmeasured fresh download inside the worker.

The direct worker is also executable with PYTHONPATH=src, but use the supervisor for a process-level wall-clock bound. The worker's own per-token deadline and resource checks are cooperative. The supervisor limits its owned child while the supervisor remains alive; external forced termination of the supervisor is outside that guarantee.

The four-attempt smoke CLI remains available for separate hardware checks. It is not the study entrypoint. It has cooperative timing and cannot replace the supervisor's hard process timeout.

## Resource behavior

The worker requires at least 3 GiB free host RAM after imports and 4 GiB free VRAM before loading. During generation it checks host/VRAM reserves, allocation, time, and artifact use. These checks are not OS reservations. If current desktop load fails a gate, the run stops and its assignments remain; do not lower guards or close unrelated applications automatically.

The checkpoint file is about 1.50 GB, with additional tokenizer/cache/setup use. Cache duplication on Windows is possible. Do not assume a rounded model name is a storage measurement. The 8B BF16 comparator remains deferred.

## Offline checks

    python -m unittest discover -s tests -v
    python scripts/validate_plan.py

These checks use no model weights or GPU inference. The watchdog tests launch only short dummy child processes. The artifact verifier can also check the published run in results/2026-11-04-local-study; tokenizer verification requires the prepared environment/cache.

No training, learned monitor, semantic judge, intervention direction search, or historical intervention replay is part of this study.
