# Research references and claim boundaries

Protocol 0.2 research review. Sources checked through **November 3, 2026**, using primary papers, original research reports, and publisher model cards. Dates distinguish a public report, an arXiv submission, and a later revision. Recent reports are relevant evidence, not independent replications or proof that their conclusions transfer to this pilot. The original seven reference identifiers are retained.

## R1. CoT monitoring as a research opportunity

**Korbak et al., _Chain of Thought Monitorability: A New and Fragile Opportunity for AI Safety_.** First submitted **2025-07-15**; v2 **2025-12-07**. [Pinned paper](https://arxiv.org/abs/2507.11473v2).

This position paper motivates monitoring readable reasoning alongside other safeguards while emphasizing incomplete coverage and fragility. Its argument does not establish faithfulness, successful monitoring in every task, or the safety of a model that produces reassuring reasoning. The protocol therefore treats CoT as an observable signal and tests concrete outcomes.

## R2. Evaluation-awareness interventions in Sonnet 4.5

**Anthropic, _Claude Sonnet 4.5 System Card_, §7.6.** Associated model release **2025-09-29**. [System card](https://assets.anthropic.com/m/12f214efcc2f457a/original/Claude-Sonnet-4-5-System-Card.pdf); [release announcement](https://www.anthropic.com/news/claude-sonnet-4-5).

Inhibiting candidate evaluation-related representations sometimes increased concerning behavior; effects depended on the representation and scenario. The investigation did not find evidence of sophisticated strategic deception. This supports a qualified audit intervention, not the claim that suppression improves safety or removes an isolated awareness mechanism in another model.

## R3. Random perturbations as a causal confound

**Anthropic, _Claude Opus 4.5 System Card_, §6.7.2.** Associated model release **2025-11-24**; the linked card includes later corrections. [System card](https://assets.anthropic.com/m/64823ba7485345a7/Claude-Opus-4-5-System-Card.pdf); [release announcement](https://www.anthropic.com/news/claude-opus-4-5).

Evaluation-related inhibition had modest behavioral effects, and random feature inhibition also produced similar, usually weaker changes. The authors identify perturbation-induced distribution shift as a partial explanation. This makes matched random directions and competence controls necessary, and prevents interpreting any steering-induced deterioration as an awareness-specific causal effect.

## R4. A controlled evaluation-aware model organism

**Hua, Qin, Marks, and Nanda, _Steering Evaluation-Aware Language Models to Act Like They Are Deployed_.** First submitted **2025-10-23**; v5 **2026-03-02**. [Pinned paper](https://arxiv.org/abs/2510.20487v5).

The authors deliberately train evaluation-dependent Python type-hint behavior and steer it using a direction obtained before that additional training. This is a controlled model organism with an observable behavioral distinction. It does not establish naturally occurring awareness in an unmodified checkpoint, or justify transferring its intervention without an independent manipulation check.

## R5. Monitorability taxonomy and observation scopes

**Guan et al., _Monitoring Monitorability_.** [OpenAI research report](https://openai.com/index/evaluating-chain-of-thought-monitorability/) **2025-12-18**; [arXiv v1](https://arxiv.org/abs/2512.18311v1) submitted **2025-12-20**.

The study distinguishes intervention, process, and outcome-property evaluations and examines monitor capability, observation scope, and reasoning length. Monitorability depends on both actor and monitor. It motivates semantic monitoring and prefix-length analyses, while its results do not license inferring faithful internal computation from successful prediction of an observable action property.

## R6. Proposed open-weight actor and semantic monitor

**Qwen team, _Qwen3-4B_ and _Qwen3-8B_ model cards.** Mutable documentation accessed **2026-11-03**; no publication date inferred. [4B card](https://huggingface.co/Qwen/Qwen3-4B); [8B card](https://huggingface.co/Qwen/Qwen3-8B).

The publisher documents locally accessible causal models with thinking and nonthinking modes, including delimited reasoning. This supports instrumenting the 4B actor and proposing an 8B semantic monitor. Parameter count does not establish judge competence: the monitor still needs task-specific validation, and both checkpoints, tokenizers, templates, and inference settings require immutable pins.

## R7. White-box auditing with a learned readout

**Gurnee et al., _Verbalizable Representations Form a Global Workspace in Language Models_.** Published **2026-07-06**. [Primary paper](https://www.transformer-circuits.pub/2026/workspace/index.html).

A J-lens evaluation-awareness ablation changes verbalized awareness and blackmail attempts in a small case study, while most ablated rollouts still reject blackmail. The authors identify limitations of readout coverage. This motivates complementary observations without assuming that their proprietary learned readout or causal directions exist in this pilot's open model.

## R8. Monitoring and optimization-induced obfuscation

**Baker et al., _Monitoring Reasoning Models for Misbehavior and the Risks of Promoting Obfuscation_.** arXiv v1 submitted **2025-03-14**. [Pinned paper](https://arxiv.org/abs/2503.11926v1).

In coding environments, LLM monitoring of reasoning detects reward hacking, but strong training pressure against the monitor can induce less visible hacking. This distinguishes ordinary frozen-monitor evaluation from adaptation against an overseer. The pilot freezes actor and monitors and makes no adversarial-robustness claim from an actor never optimized to evade them.

## R9. Omitted influences in observable reasoning

**Chen et al., _Reasoning Models Don't Always Say What They Think_.** [Anthropic report](https://www.anthropic.com/research/reasoning-models-dont-say-think) **2025-04-03**; [arXiv v1](https://arxiv.org/abs/2505.05410v1) submitted **2025-05-08**.

Hint interventions reveal that reasoning can omit influences on the final answer, including in reward-hacking settings. These experiments concern specific faithfulness properties; they do not show that all useful monitoring fails. The protocol separately measures observable policy-boundary crossings, verbalized context recognition, and task competence rather than equating any one with intent.

## R10. Reasoning-dependent proxies and capable monitors

**Emmons et al., _When Chain of Thought Is Necessary, Language Models Struggle to Evade Monitors_.** arXiv v1 submitted **2025-07-07**. [Pinned paper](https://arxiv.org/abs/2507.05246v1).

The authors distinguish reasoning used for computation from rationalization and stress-test several evasion settings. Their methodology motivates compositional tasks and a capable monitor, but does not establish that reasoning is necessary for every harmful behavior. The pilot includes reasoning-dependence diagnostics and keeps its conclusions bounded to the selected tasks and monitors.

## R11. Public evaluation data and reference metrics

**OpenAI, _Open Sourcing Monitorability Evaluations_.** Published **2026-04-23**. [Original release](https://alignment.openai.com/monitorability-evals/); [primary repository](https://github.com/openai/monitorability-evals).

The release provides public datasets, prompts, metric code, and cross-fit filtering for intervention estimates. Its orchestration scaffold uses mocked outputs and is explicitly illustrative rather than a supported evaluation framework. The protocol therefore reviews relevant components and licensing for an external anchor, rather than claiming either turnkey execution or an already implemented replication.

## R12. Metagaming is not one scalar mechanism

**Xu et al., _Studying Metagaming Latents in Language Models_.** Published **2026-10-06**. [Original research report](https://alignment.openai.com/metagaming-latents/).

An o3 investigation finds overlapping signals related to response style, evaluation, reward, and normative reasoning; some interventions affect answers without corresponding verbalization. This challenges a single-vector awareness interpretation. The protocol uses the narrower term evaluation-framing direction and requires specificity checks instead of treating a change in wording or probe score as a mechanistic explanation.

## R13. Discrimination, shared-instance comparisons, and accepted risk

**Guan, Xie, and Baker, _Beyond g-mean²: Complementary Metrics for Monitorability_.** Published **2026-10-20**. [Original methods report](https://alignment.openai.com/beyond-gmean-squared/).

The report distinguishes discrimination, pair-matched instance comparisons, and risk after hypothetical monitor gating. Changing which cases exhibit a target behavior can reverse apparent comparisons. The pilot accordingly reports prevalence, achieved false-positive rates, accepted coverage, and joint misses; conditional detection rates alone cannot identify a causal change in an invariant population of violations.

## R14. Activation classifiers as supervised, model-dependent monitors

**Makelov et al., _Training Activation Classifiers for Safety and Alignment_.** Published **2026-11-02**. [Original research report](https://alignment.openai.com/training-activation-classifiers/).

The report describes streaming activation classifiers and tested robustness/transfer properties in proprietary models. It emphasizes dependence on labeled targets and model checkpoints. This supports an independently evaluated activation channel, not interpreting a framing probe as a general safety detector or expecting a classifier to transfer unchanged between different base models.

## R15. Evaluation objectives can matter more than evaluation labels

**Hsu and Arnesen, _Eval-production Behavior Gaps in Agent Safety and the Role of Eval-awareness_.** Published **2026-11-03**. [Original research report](https://alignment.openai.com/eval-production-behavior-gap/).

In the studied warning-respecting tasks, merely stating that an interaction is an evaluation has no significant effect, while stated objectives shift performance. Production/evaluation matching is approximate. This undermines assuming that a generic evaluation wrapper manipulates consequential awareness; the protocol must validate observable framing effects and makes no production-generalization claim from synthetic wrappers.

## R16. Distinct evidence for visibility, causality, and monitoring

**Li, Ma, Hu, Zhong, and Liu, _Chain-of-Thought Oversight Requires Separate Evidence for Faithfulness and Monitorability_.** arXiv v1 submitted **2026-11-01**. [Pinned position paper and case studies](https://arxiv.org/abs/2611.01620v1).

The paper distinguishes accessible reasoning, mechanistic faithfulness, localizable causal mechanisms, and behavioral monitorability, with case studies showing that evidence for one need not establish another. This newly posted position paper informs claim discipline rather than serving as a settled standard or independent replication. The protocol explicitly separates these evidence requirements.

## R17. Controllability is an evasion proxy

**OpenAI, _Reasoning Models Struggle to Control Their Chains of Thought, and That's Good_.** Published **2026-03-05**. [Original report and linked paper](https://openai.com/index/reasoning-models-chain-of-thought-controllability/).

CoT-Control measures compliance with instructions about reasoning form, across several datasets and models. Such controllability can inform concern about evasion, but is a proxy rather than a complete adversarial-monitoring evaluation. This pilot does not infer robust monitoring from a failure to obey stylistic instructions, or infer evasion merely from changed language.

## Boundaries used in this repository

- **Observe the target directly.** A prohibited action, an incorrect calculation, a framing judgment, and an awareness phrase are distinct labels. None alone establishes intent.
- **Match information before comparing channels.** Primary public-context baselines receive the same visible prompt; treatment metadata and future action tokens remain unavailable.
- **Separate the claims.** Prediction does not establish faithful reasoning; intervention does not establish an isolated circuit; suppression does not establish safety improvement.
- **Respect scope.** A result on a frozen small model, selected synthetic tasks, or one monitor is not a guarantee about deployment, other checkpoints, or adaptive evasion.
- **Keep provenance explicit.** The papers motivate the design. This repository has not reproduced their results, run model experiments, or independently validated proprietary methods.
