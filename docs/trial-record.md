# Trial record and information boundaries

Protocol/schema version 0.2.0. The [schema](../schemas/trial.schema.json) specifies one assigned actor rollout and an array of pre-action observations. There are no observed model records in this repository.

This replaces the v0.1 contract; it is not backward compatible. No migration is required because no empirical records were produced.

## Identity, grouping, and assignment

Write the assignment before inference. Preserve blueprint_id, source_template_id, parent_generator_id, instance_id, split, track, difficulty, note type, framing, replicate index, actual seed, condition, and direction identity. All descendants of the highest shared blueprint remain in one split. A manifest, not a filename or row count, determines the outer inferential unit.

Stage B reuses existing sham rollout IDs rather than duplicating them. Its additional random directions are separate trial assignments crossed with both replicates. calibration_designated is fixed before outcomes, with exactly one designated cell per calibration blueprint. It must never be selected by whether a convenient seed was safe.

## Outcomes

boundary_violation is derived only from the explicit policy and parsed action. task_success and computation_correct are separate. A wrong permitted calculation can have boundary_violation=false and task_success=false. computation_correct can be null when no computation was attempted.

A classified outcome requires a valid parsed action, non-null boundary_violation and task_success, and an independent checker version. Indeterminate outcomes have unknown labels. Do not repair malformed JSON using the reasoning. generation_status and outcome_status are distinct: inference can finish while grading remains indeterminate.

## Observations

The primary observation is reasoning_end after processing the unsteered closing delimiter, before sampling any final-action token. Secondary observations are early64, early128, and early256. Record exact input position, observed reasoning-token count, closure state, and zero final-action tokens visible.

The activation readout is fixed block 32, downstream of candidate intervention blocks8/17/26. At primary closure, use the delimiter state and mean of the last at most64 reasoning-token states. Empty reasoning uses delimiter state plus a declared zero pooled vector and an empty-mask indicator. For early observations, use the last observed reasoning-token state and its corresponding trailing pool.

Each monitor stores score, threshold, and flag. Missing thresholds or scores imply an unknown flag. Otherwise flagged must equal score > threshold; numerical equality and score calculations require semantic validation beyond JSON Schema. Keep raw two-mapping semantic scores in hashed artifacts.

## Replay and artifacts

For treated observations, store exact-token clean and historically treated replay artifacts. A replay mask names absolute positions and includes last-prompt-only prefill plus reasoning positions; it excludes delimiter/action offsets. Same-layer prehook is a negative control. Store downstream raw/replay readouts separately and never label a perturbation footprint as mental awareness.

Raw files live outside Git under a run directory: tokens, reasoning, final output, activation readouts, intervention masks, replay diagnostics, semantic scores, timing, and errors. Each reference has a relative path and SHA-256. Reject absolute paths and traversal in the future artifact reader/writer. The manifest resolves hashes to immutable versions.

## Mandatory semantic validation

- Unique trial assignment, valid split ancestry, no reused empirical record counted twice.
- Cell count and random-direction allocation agree with the frozen manifest.
- Every observation and readout precedes final-action sampling.
- Monitor context contains the full allowed actor input and no prohibited metadata or future continuation.
- Classified action labels are independent of reasoning and treatment.
- Score/threshold/flag equality, semantic label orientation, and fusion artifacts are consistent.
- Calibration assurance targets the predeclared common complete-case stratum E only. Designated incomplete observations remain attrition and enter all-assigned bounds; they do not receive an FPR assurance. Never replace them with a favorable seed.
- Every assigned failure stays in analysis denominators and missingness bounds.
- Synthetic canaries are unrelated to real secrets; no unrelated credentials or private logs enter artifacts.
