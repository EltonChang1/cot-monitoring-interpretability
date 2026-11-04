# Local engineering record contract

Protocol 0.3.0. The full-study record specification is [archived separately](full-study-trial-record-v0.2.md); its v0.2 schema is not the local smoke-report schema.

Every local attempt needs a unique attempt ID, source-template and state identities, note/wrapper, pinned model/runtime, input/output token counts, outcome availability, elapsed time, memory, and raw-artifact hashes. Retain failed and repaired attempts. All eight states share the existing ledger source template; do not relabel them as independent clusters.

The resource guard report is a separate artifact: it records whether acquisition/loading/inference began and the live memory that prevented execution. A blocked guard is zero actor attempts and is not a valid/safe model outcome.

The four-attempt model smoke report has artifact_kind=local_model_resource_smoke_not_monitor_evaluation. It records generation-wide finite-hook diagnostics and uncached prompt forwards, not a boundary-aligned monitoring dataset. No model observations exist while its status is blocked_host_ram.

Before the 32-attempt batch, implement a distinct JSONL writer with:
- Preassignment and cumulative attempt/token/time/storage accounting.
- Token-ID reasoning boundary and pre-action observation offsets.
- Strict action checking with unknown labels for invalid output.
- Separate validity, task success, computation correctness, and boundary crossing.
- Selected-layer finite-state artifacts, masks, and cached/uncached replay results.
- Hashes of raw tokens/text, model revision, config, prompts, checker, and runtime.
- Atomic progress saves and honest failure statuses.

The existing text parser validates fixture strings; it does not prove model-token alignment. The existing smoke hook can observe action-token states, so those states must never be presented as pre-action evidence. Do not fabricate a baseline dataset from fixture selfchecks, guard reports, or future batch schema examples.

Store model caches outside the source tree and runs under ignored local directories. Publish only a deliberately summarized resource report without credentials or unrelated personal data.
