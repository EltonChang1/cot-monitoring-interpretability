# Trial record and leakage boundaries

The [JSON Schema](../schemas/trial.schema.json) specifies one planned actor rollout, including its primary-checkpoint monitor scores. It is a contract for future implementation, not evidence that a runner exists. No illustrative model observation is included.

Each assigned trial needs a unique `trial_id`, immutable scenario/template-group identity, split, framing, intervention, generation seed, status, hashes, and output references. Write an assignment record before inference so failures remain in the denominator. Use JSON `null` for unknown outcomes rather than converting failures to nonviolations.

The run manifest resolves every SHA-256 to an immutable artifact. Large/raw files live outside Git: full token IDs, reasoning, final output, pre-hook activations, optional diagnostic post-hook activations, and timing logs. Store paths relative to the local run directory and forbid path traversal in the eventual writer/reader.

The checkpoint contains only a reasoning prefix. `reasoning_tokens_observed` is the actual count, possibly below 128. `boundary` is `token_budget`, `reasoning_end`, or `unavailable`. No final-action token may appear in the monitor observation. A no-reasoning output may have zero tokens with `reasoning_end`; a missing/unparseable boundary uses `unavailable`.

Monitor scores are probabilities or risk scores in [0,1] with frozen thresholds. Store `null` scores for unavailable predictions. For valid available scores, `flagged` must equal `score > threshold`. The implementation must check this cross-field invariant; JSON Schema alone does not enforce it. `fusion` is the mean of `cot` and `activation` when both exist.

`policy_violation` and `task_success` come from the independent action checker. A valid abstention can have both fields false. A malformed, truncated, failed, or ambiguous action has unknown labels. An invalid action does not become valid merely because its intent seems clear in CoT.

Required semantic checks beyond schema validation:

- A trial ID is unique within the manifest; all scenario variants share the same split.
- `valid` requires a parseable action and non-null outcome labels; other statuses require unknown outcome labels.
- Scenario, model, configuration, and artifact hashes match the frozen manifest.
- Token offsets prove that the observed prefix and activations precede the action segment.
- Monitors receive only their permitted views; the analysis table is never used as monitor input.
- Layer, strength, vector, actual perturbation norm, timing, and score thresholds resolve through the run artifacts.
- `not_started`, failed, and unavailable records remain in the assigned-trial denominator.

For privacy and reproducibility, synthetic canaries must have no relationship to real secrets. Do not log access tokens or unrelated local paths in run artifacts.
