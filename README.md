# CoT Monitoring & Interpretability

An experiment-design repository studying whether observable reasoning and internal activations provide complementary warning signals before a model proposes a policy-violating action.

**Status: protocol draft; no model experiments or empirical results yet.** This repository contains the study design and supporting specifications. Model inference, activation hooks, monitors, and analysis code remain to be implemented.

## Research question

When a candidate evaluation-framing representation is suppressed in an open-weight reasoning model, does the rate of policy violations missed by a frozen reasoning monitor change? Can an activation monitor help identify those misses?

The motivating Anthropic result is an audit intervention: suppressing evaluation-awareness representations sometimes **increased** problematic behavior. It does not establish that suppression improves safety. Observable CoT is also an imperfect signal, rather than a complete account of model computation. See the [primary-source notes](docs/references.md).

## Start here

- [Experiment protocol](docs/experiment.md): hypotheses, tasks, interventions, monitor timing, analysis, and execution gates.
- [Primary sources](docs/references.md): verified 2025–2026 research and claim boundaries.
- [Pilot configuration](configs/pilot.json): proposed counts and settings; unresolved pins are explicit.
- [Trial specification](docs/trial-record.md) and [JSON Schema](schemas/trial.schema.json): planned records and leakage boundaries.
- [Illustrative scenario](examples/ledger-scenario.json): hand-authored task specification, not a model output or experimental observation.
- [Results template](docs/results-template.md): reporting requirements, including null and inconclusive outcomes.

## Proposed pilot

Use `Qwen/Qwen3-4B` locally in thinking mode, three synthetic task families, two matched context framings, four activation conditions, and three sampling seeds. The held-out test comprises **2,880 rollouts across 120 independent base-scenario groups**. The primary outcome is a policy violation that an early reasoning monitor fails to flag.

All actions are inert JSON proposals checked against explicit toy policies. The experiment does not connect a model to real tools, accounts, credentials, or external recipients. Reasoning tokens and activations come from the locally instrumented open-weight model; hosted reasoning summaries are not substitutes.

## Next implementation milestone

Implement the simulator and label checker first, then verify reasoning boundaries and activation hooks on a 96-rollout preflight. Freeze model revisions, dependency versions, scenario splits, steering settings, and monitor artifacts before opening the held-out test. See [the staged run plan](docs/experiment.md#10-execution-plan-and-resources).

Created November 3, 2026. The protocol is a proposed pilot, not a registered or completed study. No software or content license has been selected yet.
