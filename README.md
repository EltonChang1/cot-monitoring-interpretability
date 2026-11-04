# CoT Monitoring & Interpretability

A resource-audited project for a small local CoT/activation instrumentation pilot, with a larger research design kept as a deferred reference.

**Default: protocol 0.3.0, local engineering. Current model status: BLOCKED_HOST_RAM.**
The offline checker/parser and report-safety apparatus pass 14 unit tests. No model checkpoint has been downloaded and no pretrained inference or monitoring result exists.

## What the machine can support

The workstation has an RTX 3060 with 12 GB VRAM and about 16 GB system RAM. CUDA/BF16 work. The earlier 8B BF16 monitor exceeds this GPU's capacity before runtime overhead. The latest small-model smoke was stopped by its guard with about 1.30 GB RAM available, below its 3 GiB requirement.

An isolated ignored environment now has a working model-loading runtime. Rechecking live headroom and passing a real model smoke remain necessary; GPU fit alone is not a readiness claim.

- [Current local protocol](docs/experiment.md) and [configuration](configs/pilot.json).
- [Harsh resource critique](docs/resource-critique-v0.2.md) and [machine/readiness audit](docs/resource-audit.json).
- [Current engineering result](docs/results-template.md).
- [Local environment and smoke instructions](docs/local-setup.md).
- [Local record contract](docs/trial-record.md).
- [Primary research references](docs/references.md).
- [Earlier scientific critique](docs/critique-v0.1.md).

## Run the parts that work now

From the repository root:

    python -m unittest discover -s tests -v
    python scripts/validate_plan.py

The validator requires jsonschema. The offline fixture CLI uses only the standard library:

    $env:PYTHONPATH = 'src'
    python -m cot_monitoring_local --count 4

These are fixture/design checks, not model observations.

The [bounded smoke runner](scripts/smoke_local_model.py) uses the isolated runtime and refuses execution without live memory headroom:

    .venv\Scripts\python.exe scripts/smoke_local_model.py --output runs/local-resource-smoke/report.json

That command is offline by default and requires a new report path. Explicit acquisition requires --allow-download. The candidate pinned 0.6B checkpoint file is about 1.50 GB; cache/setup have a separate checked budget. Time limits are cooperative in the smoke. Do not lower guards to make a run pass. See the protocol for setup, missing batch implementation, and claims.

## Local budget and deferred study

The local ceiling is 48 actor attempts at 512 generated tokens each: **24,576 generated tokens**, including smoke and repairs. It has no learned monitor, fusion training, 5% FPR claim, or awareness/circuit conclusion. Eight numeric states share one template.

The [full v0.2 study](docs/full-study-v0.2.md), [full configuration](configs/full-study-v0.2.json), and [statistical analysis](docs/statistical-analysis.md) retain the 12,940-rollout reference design. Its 8B judge, dataset, instrumentation, and compute budget remain deferred. Quantization or a smaller judge would need a new validation, not a silent substitution.

All proposed actions are inert synthetic JSON. No real credentials, external recipients, tools, or paid compute are used. No software/content license has been selected.
