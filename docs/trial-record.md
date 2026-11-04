# Local study records, version 0.4

The implemented [worker](../src/cot_monitoring_local/model_study.py) writes a frozen assigned plan, atomic progress file, and one JSON file per attempted trial. [Completed example](../results/2026-11-04-local-study/progress.json).

Each record preserves the shared source-template/state identity, note, framing, seed, exact visible messages, prompt hash, raw generated IDs, special-token-preserving text, action-checker outcome, diagnostic flags, timestamps, and checkpoint vectors. Four states remain one shared template, not four independent clusters.

Checkpoint offsets refer to the input token being processed. For reasoning_end, that token is the first closing token 151668; its hidden state predicts the next token. Thus the readout precedes every action token. A reasoning-prefix-128 observation is collected only before closure.

The reasoning-only flag is computed from the delimited reasoning slice. The prompt baseline uses the visible note. The checker receives policy, state, and the later action only. Unknown/capped/malformed outputs never become nonviolations by default.

The [supervisor](../scripts/run_local_study.py) writes a watchdog report and worker log. It owns only its launched worker. Completed records and all preassignments survive a timeout; forcibly terminating an active worker can lose its unsaved token prefix, leaving that assignment indeterminate. It does not guarantee cleanup if the supervisor itself is forcibly killed.

The [verification CLI](../scripts/verify_local_run.py) checks assignment/rule/source hashes, finite vector shapes and positions, checker outcomes, per-trial consistency, and aggregate counts. --verify-token-text additionally uses the cached tokenizer to verify raw/reasoning/action text without a model forward pass.

Published JSON is UTF-8 with LF and unchanged parsed values. The artifact manifest records both raw-run and published-file hashes when newlines differ. Model weights stay outside the repository; the actual synthetic run is intentionally published under results/.
