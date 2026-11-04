# Research references and claim boundaries

Sources checked on **2026-11-03**. These are primary research reports or the model publisher's documentation. Dates below distinguish first publication from later revisions; none is evidence that a field-wide practice is universal.

## R1. CoT monitoring as a research opportunity

**Korbak et al., _Chain of Thought Monitorability: A New and Fragile Opportunity for AI Safety_.** First submitted **2025-07-15**; version 2 **2025-12-07**. [Pinned arXiv version](https://arxiv.org/abs/2507.11473v2).

This multi-author position paper argues that readable reasoning can provide useful evidence of concerning behavior and deserves investment alongside other safeguards. It emphasizes imperfect coverage and possible fragility under development changes. It motivates testing an additional monitoring channel; it does not establish that CoT is a faithful transcript of every internal computation.

## R2. Evaluation-awareness interventions in Sonnet 4.5

**Anthropic, _Claude Sonnet 4.5 System Card_, section 7.6.** Associated model release **2025-09-29**. [System card](https://assets.anthropic.com/m/12f214efcc2f457a/original/Claude-Sonnet-4-5-System-Card.pdf); [dated release announcement](https://www.anthropic.com/news/claude-sonnet-4-5).

The audit identified candidate evaluation-related representations and inhibited them using activation interventions. Some interventions increased concerning behavior; effects varied by vector and scenario. The report did not find evidence of sophisticated strategic deception. This motivates controlled auditing, rather than treating suppression as an established way to improve safety.

## R3. Random perturbations as a causal confound

**Anthropic, _Claude Opus 4.5 System Card_, section 6.7.2.** Associated model release **2025-11-24**; the linked card includes subsequent corrections. [System card](https://assets.anthropic.com/m/64823ba7485345a7/Claude-Opus-4-5-System-Card.pdf); [dated release announcement](https://www.anthropic.com/news/claude-opus-4-5).

The evaluation-awareness inhibition study reports modest increases in misaligned behavior, but random feature inhibition also had similar, usually weaker effects. The report identifies perturbation-induced distribution shift as a partial explanation. Accordingly, an experiment must compare candidate directions with matched controls and measure general task degradation before interpreting an effect as awareness-specific.

## R4. A controlled evaluation-aware model organism

**Hua, Qin, Marks, and Nanda, _Steering Evaluation-Aware Language Models to Act Like They Are Deployed_.** First submitted **2025-10-23**; version 5 **2026-03-02**. [Pinned arXiv version](https://arxiv.org/abs/2510.20487v5).

The authors construct evaluation-aware behavior through additional training: a model uses Python type hints differently across evaluation and deployment contexts. Activation steering reduces that behavioral difference, using a direction obtained from the original model. This is evidence in a deliberately constructed organism; it does not demonstrate reliable removal of naturally occurring awareness in arbitrary models.

## R5. Comparing monitoring observation scopes

**OpenAI, _Evaluating chain-of-thought monitorability_.** Published **2025-12-18**. [Research report and linked paper](https://openai.com/index/evaluating-chain-of-thought-monitorability/).

The report studies intervention, process, and outcome-property evaluations across thirteen evaluations and twenty-four environments. In almost every studied setting, CoT monitoring outperforms monitoring actions and final outputs alone. These findings motivate paired observation-scope comparisons, while remaining conditional on the tested models, environments, monitors, and access to the relevant reasoning text.

## R6. Proposed open-weight actor

**Qwen team, _Qwen/Qwen3-4B model card_.** Mutable documentation, accessed **2026-11-03**; no publication date is inferred from the live card. [Publisher model card](https://huggingface.co/Qwen/Qwen3-4B).

The card documents an Apache-2.0 causal language model with four billion parameters, thirty-six layers, and switchable thinking behavior. Thinking mode generates a delimited reasoning block followed by a final response. This makes local reasoning collection and activation instrumentation feasible in principle. Model and tokenizer revisions must be pinned before collecting experimental data.

## R7. A later white-box auditing case study

**Gurnee et al., _Verbalizable Representations Form a Global Workspace in Language Models_.** Published **2026-07-06**. [Primary paper, alignment auditing section](https://www.transformer-circuits.pub/2026/workspace/index.html).

The authors report that J-lens ablation of selected evaluation-awareness directions changes verbalized awareness and blackmail attempts across six prompts with thirty rollouts each. Most ablated rollouts still reject blackmail. They explicitly qualify monitoring coverage: automatic computation and readout limitations can evade this lens. This is motivation for complementary signals, not a complete monitoring guarantee.

## Boundaries used in this repository

- **Suppression is an experimental manipulation.** A lower awareness score or less explicit awareness language does not establish safer behavior, or prove that latent awareness has disappeared.
- **A contrastive direction is not a circuit.** A learned vector or successful probe is a candidate representation. Claims about a mechanism require causal specificity and further circuit analysis.
- **Evaluation awareness is not deception.** Recognizing an evaluation, adjusting behavior, and deliberately misleading an evaluator are different claims that require different evidence.
- **Model-generated reasoning is an observable channel.** It can omit relevant computation or rationalize a decision. Its availability does not make it a complete record of internal state.
- **This study tests a bounded proxy.** Simulated policy violations and prompted incentives do not establish a model's intrinsic goals, broad misalignment, or real-world deployment risk.
- **The protocol's hypotheses are proposals.** None of the cited results is presented as a result produced by this repository.
