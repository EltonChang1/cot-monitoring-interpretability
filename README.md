# CoT Monitoring & Interpretability

A research-design repository for testing whether internal activations add useful warning information beyond a semantic chain-of-thought monitor, and how frozen monitors behave under framing perturbations.

**Status: protocol 0.2.0; design only. No model experiments or empirical results.** Inference, simulators, activation hooks, monitor training, and analysis still need implementation.

## Research audit and revised plan

The [harsh critique of v0.1](docs/critique-v0.1.md) found a same-layer activation-readout error, unequal monitor information, an inadequate lexical comparator, conflated error labels, and unsupported evaluation-awareness interpretations. Version 0.2 replaces those comparisons.

- [Experiment protocol](docs/experiment.md): staged questions, task definitions, observation timing, interventions, and execution gates.
- [Statistical analysis](docs/statistical-analysis.md): paired estimand, grouped cross-fitting, conservative calibration, precision forecasts, and missingness bounds.
- [Research references](docs/references.md): primary papers and research reports through November 3, 2026.
- [Pilot configuration](configs/pilot.json): machine-readable counts, selection rules, and unresolved artifact pins.
- [Semantic monitor specification](prompts/semantic-monitor.md): complete context, untrusted reasoning, and label-likelihood scoring.
- [Trial record contract](docs/trial-record.md) and [JSON Schema](schemas/trial.schema.json): future data and validation boundaries.
- [Ledger scenario](examples/ledger-scenario.json), [evidence-coverage scenario](examples/evidence-coverage-scenario.json), and [results template](docs/results-template.md).

## Proposed study

Stage A compares a frozen semantic CoT monitor with semantic-plus-activation fusion on **the same 1,440 held-out unsteered trajectories across 120 outer blueprint groups**. Both receive matched public context. The primary checkpoint is complete reasoning before any final-action token.

Stage B is a gated secondary robustness study with **4,800 additional rollouts**, using a downstream activation readout, identical-token clean replays, opposite-direction steering, and concrete semantic/random controls. Its arm names do not establish removal of mental awareness.

The maximum phased ceiling is **12,940 actor rollouts**, including discovery and preflight. Calibration and development gates can stop the study before testing. A public-benchmark anchor has its own future budget; this bespoke design is not a completed benchmark replication.

All proposed actions are inert JSON checked against explicit synthetic authorization policies. Task mistakes, policy-boundary crossings, and intent are different claims. Model traces and activations must come from the locally instrumented open-weight model.

No weights are downloaded and no paid compute is started by creating this repository. Model revisions and run artifacts remain unpinned, so the protocol is not preregistration-ready. No software/content license has been selected.

## Validate the design artifacts

Run `python scripts/validate_plan.py` with Python and the `jsonschema` package installed. The [validator](scripts/validate_plan.py) checks document targets, schema behavior, allocations, and calibration calculations. It does not run models, implement the simulator, or validate the scientific hypotheses.

Created and research-audited November 3, 2026.
