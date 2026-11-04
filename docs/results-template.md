# Local engineering result

Protocol 0.3.0 | Reviewed November 3, 2026

**Outcome: offline apparatus passed; model phase BLOCKED_HOST_RAM.**

## Completed

- Machine inventory established RTX 3060 12 GB VRAM, about 16 GB physical RAM, i7-12700, and ample sampled disk.
- Existing Torch CUDA/BF16 and a tiny tensor multiplication worked.
- An ignored isolated environment now imports Torch 2.6.0+cu118 and Transformers 4.57.1 with locally pinned model-loading packages.
- Twelve checker/parser unit tests passed, including wrong arithmetic versus forbidden actions, duplicate/invalid JSON, and reasoning-boundary fixture cases.
- Two report-safety tests passed: atomic failure bookkeeping and refusal to overwrite old reports. Total: 14 unit tests.
- A four-fixture selfcheck ran 20 checks and explicitly reported no inference or actions.

## Model resource gate

Latest report time: 2026-11-04T07:11:50.933053+00:00 (November 3 in America/Los_Angeles).

- Host RAM available after runtime initialization: 1,302,429,696 bytes.
- Required available host RAM: 3,221,225,472 bytes (3 GiB).
- Model loading attempted: false.
- Checkpoint acquisition started: false.
- Model inference performed: false.
- Actor attempts: zero.
- Published pretrained throughput, valid-action rate, memory peak, and monitor quality: **not measured**.

The earlier RAM snapshot was larger; live headroom changed. This block demonstrates the guard, not that model inference is impossible on a less-loaded machine. See [the audit](resource-audit.json).

## Still required before the engineering batch

A resource-qualified pretrained smoke, completion/benign-task screens, boundary-aligned activation capture, historical cached replay, a capped resumable batch writer, and the full live resource guard. No 32-attempt batch or statistical monitoring comparison has been run.

## Claim ledger

| Claim | Evidence | Status |
| --- | --- | --- |
| Offline checker/parser apparatus works on tested fixtures | 12 unit tests and executable selfcheck | Supported within fixtures |
| CUDA and BF16 are usable | Device query and tiny finite tensor operation | Supported |
| Small pretrained actor runs within limits | Guard stopped before acquisition/loading | Not established |
| CoT/activation complementarity | No model data or semantic comparator | Untested |
| Awareness suppression or circuit discovery | No relevant intervention study | Untested |

Preserve this failed readiness result. Do not replace unknown measurements with estimates or report fixture outputs as model observations.
