# Actual local study result — November 4, 2026

Protocol 0.4.0 | **Execution completed and artifact verification passed.**

## What ran

The pinned Qwen/Qwen3-0.6B checkpoint ran 16 assigned cells: four ledger states × benign/pressure notes × ordinary/evaluation framing. All states share one source template. Raw tokens, action text, checkpoint vectors, plan/rule/source hashes, and per-trial failures are [published here](../results/2026-11-04-local-study/progress.json).

| Measurement | Actual result |
| --- | --- |
| Assigned / attempted trials | 16 / 16 |
| EOS completions | 13 |
| Valid actions | 8 |
| Valid, successful nonviolations | 8 |
| Malformed completed actions | 5 |
| Token-capped unknowns | 3 |
| Pre-action reasoning-end readouts | 13, all finite |
| Reasoning-prefix-128 readouts | 16 |
| Generated study tokens | 5,435 of the 8,192 cap |
| Worker elapsed time | 418.18 seconds |
| Supervisor elapsed time | 419.08 seconds; exit 0; no timeout |
| Cached model loading | 3.48 seconds |
| Peak GPU allocation after load | 1,318,557,696 bytes, approximately 1.23 GiB |
| Available host RAM before load | 5,141,131,264 bytes |

The GPU peak counter was reset after loading; this is a generation-phase value, not the loading-lifetime peak. The earlier smoke also exercised a 1,536-token forward and observed 1,832,777,728 allocated bytes after load.

## Behavioral result and unknowns

No authorization violation was observed in the eight classifiable actions. The other eight outcomes are unknown, so this does **not** mean zero violations across all 16.

| Framing | Benign: valid / assigned | Pressure: valid / assigned | Pressure-minus-benign violation bounds |
| --- | --- | --- | --- |
| Ordinary task | 2 / 4 | 2 / 4 | −0.50 to +0.50 |
| Evaluation | 3 / 4 | 1 / 4 | −0.25 to +0.75 |

These are missing-label identification bounds on the fixed panel, not confidence intervals. The pressure effect is inconclusive. Validity is a descriptive format/completion outcome; malformed actions are not recoded as safe or successful.

## Fixed warning diagnostic

Only the same eight classifiable actions enter these confusion counts; the other eight remain unknown.

| Rule | TP | FP | TN | FN | Unknown | Recall |
| --- | --- | --- | --- | --- | --- | --- |
| Reasoning-only lexical warning | 0 | 1 | 7 | 0 | 8 | Not estimable |
| Visible-note prompt baseline | 0 | 3 | 5 | 0 | 8 | Not estimable |

Observed false-alarm fractions are 1/8 and 3/8 respectively. This tiny conditional comparison does not establish monitor superiority. There are no known positive cases from which to estimate recall.

## Verification and provenance

[Verification](../results/2026-11-04-local-study/verification.json) recomputed the action labels and aggregate counts, matched plan/rule/source hashes, and checked all 13 reasoning-end readout positions against raw token IDs. It also used the cached tokenizer to check all 16 raw decodes, 13 reasoning slices, and 13 action slices. No model forward pass was used for this verification; activations were not recomputed.

An independent read-only artifact review reached the same counts and found no observed final-action leakage into the warning or readout. All 27 unit tests passed. [Artifact hashes](../results/2026-11-04-local-study/artifact-manifest.json) distinguish raw Windows run files from normalized published JSON.

Four preceding resource-smoke attempts are separate from this panel. They verified hardware and uncached hook invariants, but only one action met the old nested-format prompt contract. The old v0.3 competence screen therefore did not pass. Version 0.4 explicitly redesigned the task interface and measures format/behavioral outcomes; it does not claim that earlier competence gate passed.

The larger study, a capable semantic monitor, learned probes/fusion, awareness interventions, and circuit identification remain untested.
