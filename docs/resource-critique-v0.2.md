# Resource critique of protocol 0.2.0

**Reviewed:** the full-study design at commit `90b5e00`, with subsequent local engineering follow-through recorded below. **Date:** 2026-11-03. This review distinguishes the archived full study from the smaller local engineering pilot. It reports inventory, offline validation, and a failed readiness gate, not an inference benchmark. No model weights were downloaded or model inference executed.

**Verdict: reject v0.2 as the default experiment to run on this workstation. Current local model readiness: `BLOCKED_HOST_RAM`.** Its scientific safeguards improved, but its scope expanded beyond a measured local execution budget. The smaller engineering pilot has an implemented offline apparatus; its bounded model smoke check stopped at the host-memory guard. The full study is archived, and GPU capacity alone does not make the local pilot ready.

## 1. What is actually available

The initial read-only machine audit supplied these sampled facts. The later measurements below supersede its available-memory and installed-dependency snapshot for current readiness.

| Resource | Observed inventory | Consequence |
| --- | --- | --- |
| GPU | NVIDIA RTX 3060, 12,288 MiB VRAM; 10,697 MiB free at sampling | A useful local GPU exists; free memory is a snapshot, not a reservation |
| Host memory | 16,883,507,200 bytes total; 6,422,220,800 bytes available | Loading/offloading must respect current available RAM, not the nominal 16 GB machine class |
| CPU | Intel Core i7-12700, 12 cores / 20 threads | CPU fallback exists, with unmeasured model throughput |
| Disk | C: had 690,250,956,800 bytes free | Disk capacity is not the immediate blocker; cache duplication and trace retention still need accounting |
| Software | Windows 11; Python 3.12.6; Torch 2.6.0+cu118 | Existing Torch can use CUDA; BF16 support was verified |
| Missing model stack | Transformers, Accelerate, Safetensors, and Hugging Face Hub absent | The specified inference workflow is not installed |
| Model assets | No Hugging Face, Ollama, or LM Studio model caches found | A model download remains a separate prerequisite |
| External compute | Cloud configuration inventory empty | No provisioned external compute is established |

This establishes a GPU-backed route worth testing, not readiness to load a model. Available memory changed substantially during follow-through; other desktop applications share these resources.

## Follow-through and the actual current blocker

A repository-local, Git-ignored `.venv` was created using system site packages, retaining the existing Torch installation. Transformers **4.57.1**, Hugging Face Hub **0.36.0**, and NumPy **1.26.4** were installed in that environment. Torch 2.6.0+cu118 and Transformers import successfully together. This establishes runtime import compatibility only.

The offline simulator/checker/parser apparatus was implemented and **12 tests passed**. Those tests validate the implemented offline behavior, not model competence, activation-hook correctness on a loaded checkpoint, or research hypotheses.

The bounded Qwen3-0.6B smoke guard then failed **before checkpoint or tokenizer download**:

| Readiness measurement | Observed bytes |
| --- | ---: |
| Available host RAM before heavy runtime imports | 1,953,755,136 |
| Available host RAM after Torch/Transformers/CUDA imports | 1,349,906,432 |
| Process resident memory after imports | 634,273,792 |
| Required available-host-RAM gate | 3,221,225,472 (3 GiB) |

The initial 6,422,220,800-byte available-memory snapshot did not persist under current desktop load. These are successive system observations, not a controlled attribution of all memory changes to one process. No applications were closed, no model weights were downloaded, and no model inference ran.

**Required disposition:** preserve `BLOCKED_HOST_RAM` and the failed-gate record. Do not lower the memory threshold merely to pass, assume a small checkpoint's GPU fit resolves host loading needs, or report a successful model smoke test. Re-measure host and device headroom before any later attempt. If a different loading strategy or guard is proposed, justify and validate it as an explicit engineering change.

## 2. Reject-level resource findings

### R1. The 8B BF16 monitor fails a fully GPU-resident fit

The proposed monitor's roughly 16.4 GB of BF16 weights exceed the GPU's entire 12,884,377,600-byte CUDA-visible capacity, before caches, temporary tensors, and runtime allocations. Loading actor and monitor sequentially avoids simultaneous residency; it does not make the monitor itself fit. Partial CPU offload or quantization might make a different configuration possible, but neither has been implemented or validated here. Available host RAM was about 6.42 GB initially and only 1.35 GB in the later post-import measurement.

This does **not** establish that the 4B actor is impossible. Its roughly 8 GB of weights may fit within the sampled 11.22 GB free VRAM if loading and runtime overhead are controlled. That must be measured with the actual context, cache, dtype, and hooks. Treating the 4B actor and 8B monitor as equally infeasible would be an error.

**Required action:** remove the 8B comparator from the default local engineering track. Retain the full-study comparator as deferred. Quantized or smaller judges require a new competence audit and revised interpretation; they are not silent substitutions.

### R2. The ceiling is computationally large and incomplete

The v0.2 allocation is **8,140 core actor rollouts**, **12,940 maximum actor rollouts**, and **53,002,240 maximum generated actor tokens**. These numbers were recalculated with Python.

That ceiling excludes actor prompt processing, semantic-monitor prefill passes, both label mappings, optional early checkpoints, and masked/clean replays. An 8B judge producing one label can still process thousands of input tokens per score. Teacher-forcing two full prefixes per treated observation is also substantial work. Output-token counts alone do not estimate total compute.

**Required action:** give the local track its own small hard ceiling and measure warm loading, prompt processing, generation, and replay separately. Estimate runtime only from those measurements. A large disk and a CUDA-capable GPU do not establish an acceptable time budget.

### R3. The study's implementation and dataset costs were hidden

The reviewed v0.2 repository described simulators, boundary checking, hooks, replay, cross-fitting, calibration, and analysis before implementing an inference runner. An artifact validator cannot verify these absent components. The study also requires hundreds of independently sampled outer blueprints, not merely many renamed records, plus a human-authored monitor audit and checker truth tables.

**Required action:** make implemented, tested local components the next deliverable. New simulator/parser scaffolding should be described as such. Passing its tests is not successful model execution, a validated monitor, or an empirical safety result.

## 3. Major engineering findings

### M1. Full activation and logit retention can erase the memory advantage

The storage policy must specify which tensors survive a forward pass. Requesting every hidden state can retain all layers and positions when only a selected state and a short rolling mean are needed. Materializing full-sequence vocabulary logits is another avoidable peak: `6,144 Ã— 151,936 Ã— 4` bytes is approximately **3.73 GB** for one FP32 tensor.

Use targeted hooks, a bounded ring buffer, detached compact summaries, and final-position logits where supported by the pinned runtime. Measure actual peak allocated/reserved device memory and process RAM. Do not save full activation histories by default.

### M2. The smaller model is a new instrument, with different valid layers

The official [Qwen3-0.6B card](https://huggingface.co/Qwen/Qwen3-0.6B) and [Qwen3-1.7B card](https://huggingface.co/Qwen/Qwen3-1.7B) document thinking/nonthinking modes and 28 layers. Their [0.6B configuration](https://huggingface.co/Qwen/Qwen3-0.6B/blob/main/config.json) and [1.7B configuration](https://huggingface.co/Qwen/Qwen3-1.7B/blob/main/config.json) confirm that architecture. Block 32 does not exist in either model. The cards require Transformers 4.51.0 or later.

The [official 0.6B file metadata](https://huggingface.co/api/models/Qwen/Qwen3-0.6B?blobs=true) lists `model.safetensors` as **1,503,300,328 bytes**. That is a checkpoint-file size, not measured loaded VRAM. Use actual metadata rather than multiplying the rounded model name by bytes per parameter.

A 0.6B model can exercise token parsing and hooks without being competent at the proposed research tasks. Simplify the engineering fixture or stop on poor completion; do not reinterpret capability failures as concealed misalignment.

### M3. Quantized chat inference does not supply the proposed measurements automatically

[Qwen's llama.cpp guide](https://qwen.readthedocs.io/en/latest/run_locally/llama.cpp.html) describes CPU/GPU inference, GGUF quantization, and a separate C++ ecosystem. Its chat interface is not the PyTorch block-output hook interface used by this protocol. Changing runtime would require new instrumentation and replay validation.

[Current Transformers bitsandbytes documentation](https://huggingface.co/docs/transformers/en/quantization/bitsandbytes) lists Windows CPU and NVIDIA support. That makes quantization a possible future engineering route, not proof that a compatible implementation exists in the audited installation. The small, hookable Torch model is the simpler first instrument on the verified GPU.

## 4. Minimum local design

1. Preserve and extend the implemented inert ledger task, strict parser, independent checker, fixtures, and trial logging. The current **12 passing offline tests** are evidence for this apparatus only.
2. Use the prepared repository-local environment and preserve its dependency record. Before obtaining the Qwen3-0.6B checkpoint, pass the available-host-RAM and device-memory guards. This step is currently blocked; runtime imports have passed, model loading has not been attempted.
3. Once readiness passes, run at most **48 actor rollouts total: 4 smoke, 32 baseline, and 12 reserved repair rollouts**. At 512 generated tokens each, the ceiling is **24,576 generated tokens**. Repair capacity is a ceiling, not permission for unlimited prompt iteration. Fix input/context limits before collection; never force-close reasoning to obtain a convenient action.
4. Use fixed, valid instrumentation locations, for example block 8 intervention and block 20 downstream readout. Bound the number of additional teacher-forced replay checks explicitly. Verify zero-offset equivalence, same-layer fixed-prefix equality, downstream treatment differences, closing-delimiter timing, and state reset.
5. Record peak RAM/VRAM, loading time, throughput, valid completion, reasoning closure, and checker outcomes. Stop before expanding if the model cannot reliably complete the simple task or the runtime exceeds the local budget.

Manual or lexical trace annotations can help inspect these engineering records. They do not replace a capable semantic monitor. There should be no learned fusion comparison, formal five-percent FPR assurance, large direction search, or claim of suppressed awareness in this local track.

The completed outcome so far is an offline-tested apparatus, a working runtime import check, and an honestly blocked model-readiness check. A verified model measurement apparatus remains contingent on passing resource guards and executing its bounded tests. Activation complementarity, robust CoT oversight, evaluation-awareness mechanisms, and the archived full v0.2 research study remain deferred until supported by a measured implementation and an appropriate new design freeze.
