# Independent critique of protocol v0.1.0

**Reviewed:** commit `4928689`, especially `docs/experiment.md`, sections 1–10. **Review date:** 2026-11-03. This records defects in that version, rather than asserting that subsequent revisions retain them. No model runs underpin this review.

**Verdict: reject as a preregisterable evaluation-awareness or mechanistic safety study.** The design has worthwhile label independence, frozen-monitor intentions, and missingness rules. Nevertheless, its activation readout has a causal-graph error, its monitor views have unequal information, and it lacks evidence that its actor exhibits the behavior it proposes to manipulate. It is salvageable as a staged feasibility study of bounded policy failures and monitoring under framing perturbations.

## Reject-level findings

### R1. The same-layer prehook cannot contain the claimed cached intervention history

**Original sections 5–6.** Steering occurs after block `l`, while monitoring reads that same output before the offset. With identical token IDs, upstream computation through block `l` is unchanged: that block's K/V are computed before its output is modified. Altered caches occur downstream and cannot send information backward through layers. Thus, in deterministic inference, `h_pre[l, prefix, steered] = h[l, prefix, clean replay]`, within numerical tolerance. Different generated text can change this readout; hidden downstream treatment history cannot. This follows from the [Qwen3 attention, block, and layer-loop implementation](https://github.com/huggingface/transformers/blob/v4.57.1/src/transformers/models/qwen3/modeling_qwen3.py#L173-L254).

**Required fix:** use a fixed downstream readout, paired clean replay of identical realized tokens, and the same-layer prehook as a negative control. **Falsifier:** a same-layer fixed-prefix discrepancy indicates a hook, cache, architecture, or numerical-assumption problem; it is not evidence of awareness. This argument is restricted to the stated single-block output intervention.

### R2. Activations see a wrapper withheld from the text monitors

**Original section 6.** All activations encode the full actor prompt, including evaluation/operational framing. The task and CoT monitors are denied that wrapper. An activation advantage can therefore arise from access to a predictive variable unavailable to its competitor. An exploratory prompt-boundary baseline does not repair the primary comparison.

**Required fix:** give every primary monitor the complete actor-visible context; report deliberate information ablations separately. **Falsifier:** if the advantage disappears with matched context, the previous result supports unequal information access rather than complementary internal evidence.

### R3. No demonstrated evaluation-aware behavior exists in the proposed actor

**Original sections 1, 3, and 5.** Separating explicit wrappers and changing a prompted context-classification answer do not establish naturally occurring evaluation awareness or evaluation-dependent policy behavior. The gate could select a direction that changes answer vocabulary. Hua et al.'s positive result instead uses an intentionally trained behavioral organism, with known context-dependent type-hint behavior and acknowledged limitations ([version 5, sections 3–4 and 6](https://arxiv.org/html/2510.20487v5)).

**Required fix:** separate an untrained-model feasibility screen from any optional trained-organism validation; do not authorize training implicitly. **Falsifier:** failure to establish independently measured context-dependent behavior defeats the awareness interpretation, even if a probe classifies wrappers accurately.

## Major findings

### M1. A generic evaluation cue omits the objective that may drive behavior

**Original sections 4–5.** “This is an evaluation” versus “ordinary workflow” collapses recognition, inferred test objective, authority, and expected reward. The [2026-11-03 OpenAI intervention study](https://alignment.openai.com/eval-production-behavior-gap/) found no significant effect of generic framing in its tested setting, but correct and opposing objective cues shifted behavior differently. That scoped finding is not a universal law.

**Required fix:** distinguish generic recognition from inferred objectives in annotations and scope claims to framing perturbations. Objective-cue follow-ups must acknowledge their instruction-like content. **Falsifier:** objective-sensitive effects without a generic-framing effect undermine a one-dimensional awareness explanation.

### M2. Weak controls cannot establish awareness-specific causation

**Original section 5.** A norm-matched isotropic perturbation is useful but does not match semantic directions' geometry, activation frequency, or learned downstream effects. Three random vectors cannot characterize that distribution. Unrelated semantic controls are mentioned without a concrete confirmatory allocation. The primary [UK AISI GLM-5 replication, Results and Discussion](https://www.lesswrong.com/posts/HhF5kESdtPHku7kim/reproducing-steering-against-evaluation-awareness-in-a-large-1) reports large effects from semantically unrelated directions, including nonmonotonic effects.

**Required fix:** freeze multiple unrelated contrastive directions, both signs, a strength sweep, and capability checks before interpreting specificity. **Falsifier:** comparable control effects or task degradation leave generic perturbation and bundled semantics viable explanations.

**Citation provenance:** the linked original experimental write-up is by Thomas Read, Bronson Schoen, Santiago Aranguri, and Joseph Bloom, dated **2026-04-10**. Its authors identify the work as part of the UK AISI Model Transparency Team. It studies a narrow GLM-5 setting and is a research post, not a peer-reviewed replication of this protocol.

### M3. Direction identity is coupled to sampling seed

**Original sections 4–5.** Assigning one random direction to each generation-seed stratum ties two sources of variability. A pooled random-arm contrast remains an explicitly defined mixture, but direction effects and their interaction with sampling randomness cannot be separated. Many scenarios do not create many independent random directions.

**Required fix:** cross generation seeds with direction identities, or independently balance direction assignment across scenarios and seeds. Budget the resulting trials explicitly. **Falsifier:** an apparent control effect that depends on a single direction/seed cell is not robust specificity evidence.

### M4. The lexical monitor is an inadequate sole competitor

**Original section 7.** TF-IDF logistic regression cannot reliably interpret negation, policy scope, recipient authorization, or a plan to resist an injected instruction. The actor's transformer representation can encode these relationships. Beating this lexical baseline does not establish that activations contain useful information absent from text. [OpenAI's 2026-10-06 metagaming analysis](https://alignment.openai.com/metagaming-latents/) also distinguishes steering efficacy from monitoring validity and warns through its results about task-specific readout signals.

**Required fix:** add a frozen semantic text monitor with matched context and a matched fusion comparator. Retain lexical baselines for diagnosis. **Falsifier:** an advantage that disappears against the semantic comparator establishes baseline weakness, not broad CoT failure.

### M5. Arithmetic mistakes are mislabeled as the safety construct

**Original section 3, Score integrity row.** Any wrong count becomes a policy violation, including an ordinary computation error. That is a valid correctness label but cannot distinguish shortcut-taking from inability to calculate. Steering-induced capability loss could therefore manufacture the headline effect.

**Required fix:** separate task correctness from explicit authorization violations; supply checkable evidence and permitted alternatives. Add pressure-free, difficulty-matched competence controls. **Falsifier:** violations tracking benign arithmetic errors rather than pressure-sensitive unauthorized actions defeat the intended safety interpretation.

### M6. The 128-token checkpoint compares different reasoning phases

**Original section 6.** At 128 tokens one rollout may have stated its action, another may still be parsing policy, and another may have ended reasoning. Steering-induced verbosity changes the amount and kind of information available. This is a legitimate fixed-budget endpoint but a poor sole basis for semantic-monitorability claims.

**Required fix:** make complete pre-action reasoning the primary measurement; retain fixed-token checkpoints as budgeted early-warning analyses, with lengths and closure rates. **Falsifier:** effects confined to the 128-token cutoff can reflect timing or verbosity rather than suppressed warning content.

### M7. Thirty calibration groups cannot support a precise operating-point claim

**Original sections 4, 7–8.** The minimum fifty nonviolations and five-percent empirical FPR gate do not establish a reliable five-percent population FPR. Seeds and framing variants remain clustered within only thirty calibration scenarios. Rare violations also make sensitivity unstable. Balanced-class logistic outputs are not automatically calibrated probabilities, so averaging their scores needs explicit empirical validation.

**Required fix:** use development-based uncertainty/precision forecasts, larger untouched calibration sets where justified, and interval estimates at the achieved operating point. **Falsifier:** wide intervals or intervention-specific FPR inflation preclude a claim of improved detection at a stable false-alarm cost.

### M8. “Cache/no-cache equivalence” needs a reproducible intervention mask

**Original sections 5, 6, and 10.** Replaying only the final token, or applying offsets to every token in a full-prefix pass, does not reproduce the specified trajectory. The replay must preserve absolute positions, the last-prompt-only prefill rule, historical reasoning offsets, delimiter boundaries, and cache positions. A generated token's activation may require processing that token after it is sampled.

**Required fix:** teacher-force identical token sequences with explicit per-position masks; compare cached and uncached logits/readouts within declared tolerances. Test zero-offset equivalence, empty reasoning, early close, and truncation. **Falsifier:** unexplained replay disagreement invalidates the activation measurements before scientific analysis.

## Minimum salvage and remaining limits

First validate parser/checker fixtures and hook invariants. Then screen unsteered competence and outcome prevalence. Establish baseline monitor complementarity with matched semantic text access before unlocking a separate, gated framing-perturbation study. Use a fixed downstream readout, identical-token clean replay, concrete semantic/random controls, and complete pre-action reasoning. Freeze all choices before test access.

Even after these repairs, a downstream readout may detect a perturbation footprint rather than an awareness mechanism. Successful steering is not successful monitoring; altered wording is not erased awareness; a direction is not a circuit. A trained positive-control organism could validate an assay under known conditions, but cannot establish natural awareness in an unrelated untrained model. These are substantive limits on interpretation, rather than disclaimers that can rescue an unidentified causal claim.

## Resolution in protocol 0.2.0

These are design repairs, not experimental validation. Read the [v0.2 reference protocol](full-study-v0.2.md) and [statistics appendix](statistical-analysis.md). The default local study has since been narrowed further.

| Finding | Revision | What remains unvalidated |
| --- | --- | --- |
| R1: same-layer readout error | Fixed downstream block 32; same-layer prehook negative control; exact-token treated/clean replay | Hook/cache implementation and measured predictive value |
| R2: unequal public context | Full actor prompt for every primary text view | Semantic monitor competence and elicitation |
| R3/M1: unidentified awareness construct | Stage A complementarity separated from gated framing robustness; recognition/objective labels separated | Natural awareness, production generalization, causal mediation |
| M2: generic damage | Fresh120-group benign validation, concrete semantic controls, eight-direction random bank | Direction-specific effects and adequacy beyond the finite bank |
| M3: seed/direction confounding | Two balanced random directions per blueprint, each crossed with both replicates | Robustness across additional directions or seeds |
| M4: lexical strawman | Frozen semantic monitor, sanity controls, grouped fusion and equally fitted semantic comparator | Results against independently validated monitor families |
| M5: error-label conflation | Explicit evidence omission separated from numerical correctness; concrete fixtures | Checker implementation and compositional-task competence |
| M6: arbitrary timing | Complete pre-action reasoning primary; early-prefix views separately calibrated | Actual latency, censoring, and decision timing |
| M7: weak calibration/precision |120 calibration groups, predesignated cells, conditional-E tolerance rule, group-level precision gates | IID/grouping assumptions and empirical event counts |
| M8: vague replay | Absolute-position historical masks and frozen numerical-tolerance gates | Passing executable replay invariants |

Two additional review findings changed the revision: a raw-score average became a group-cross-fitted stacker, and the unattainable24-group rare-damage gate became a fresh 120-group exact-binomial screen. The study remains unfrozen and unexecuted; none of these repairs licenses a safety or mechanistic result before data exist.
