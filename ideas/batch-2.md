# Proposer batch 2: erasure vs. scrambling, metamemory, and data-only protection

Same format as [batch 1](batch-1.md). Search source: Hugging Face papers API, 2026-11-24.

## 7. Programmable half-life: knowledge that expires on schedule

**Claim.** Batch 1's Noether channel is the infinitely durable extreme of a dial. If the forgetting rate of a write is set by its overlap with the gradient-noise covariance of whatever training follows, a writer can choose a half-life. Store facts in directions that generic future training erodes fast (session data, embargoed or licensed content, time-boxed user preferences), or in directions it leaves alone. That would give self-expiring knowledge with no unlearning step. The predictor to test: a generalized eigenproblem between the write task's Fisher and the expected future-stream Fisher.

**Sanity attempt (inconclusive; the setup was flawed).** In a 2-layer MLP I wrote task A into W1 subspaces (top/bottom eigenspaces of B's gradient second moment, generalized A/B eigenvectors, random), then resumed training on B. All variants forgot A within 500 steps. That was because A and B shared a frozen 4-way head with conflicting labels, so no subspace could hold both. A valid pilot needs non-conflicting outputs (separate heads or held-out tokens). It is recorded as untested, not negative.

**Pilot.** GPT-2-small or SmolLM-135M. Write 200 synthetic facts with gradients projected onto candidate subspaces at matched write accuracy, continue generic pretraining on a held-out web slice, and fit retention half-lives. **Kill** if the predicted vs. measured half-life rank correlation is < 0.6, or if the subspace choice moves the half-life by less than 3× at matched write accuracy and collateral loss.

**Closest.** Knowledge-entropy and "how new data permeates" work ([2504.09522](https://arxiv.org/abs/2504.09522)) measures spread, not a designable decay. Unlearning work removes knowledge after the fact.

## 8. Forgetting is scrambling: a Landauer budget for continual learning

**Claim.** With exactly reversible training dynamics (fixed-point SGD+momentum à la Maclaurin et al. 2015), no information about past tasks is ever erased, only scrambled. Ordinary training erases a measurable number of bits per step (momentum decay, rounding, weight decay). The hypothesis: savings (relearning speed) and probe-recoverability of a forgotten task scale with bits *not* erased since it was learned. Forgetting gets a thermodynamic accounting, and "scramble but don't erase" becomes a design principle, which is distinct from replay or regularization.

**Pilot.** MLP on 5-task streams. Interpolate from reversible (β → 1, exact integer arithmetic, bits of momentum decay stored in a side tape) to standard SGD, and count erased bits per step. Measure old-task linear-probe accuracy, relearning steps to 90%, and mask-only recovery. **Kill** if savings show no monotone dependence on erased bits at matched new-task accuracy, or if reversible training simply forgets behaviourally more without being more recoverable.

**Closest.** Maclaurin et al. 2015 (reversible learning, for hyperparameter gradients). Unlearning-reversibility work ([2505.16831](https://arxiv.org/abs/2505.16831)) shows unlearned knowledge returns, but has no erasure accounting.

## 9. Metamemory: does the model know what it just forgot?

**Claim.** After an update, a model's own confidence (verbalized, or the internal "I know this" probe direction) on old items drops in proportion to its actual accuracy drop. If that metamemory is calibrated, it gives free, unlabeled targeting for replay: replay only what the model *feels* it lost. If it is not calibrated (confident but wrong after forgetting), that is itself a safety finding: continual updates create confident confabulation.

**Pilot.** Qwen2.5-0.5B on 1k synthetic biographies, then fine-tune on unrelated data. Before and after, record per-item accuracy, P(True)/verbal confidence and a linear "known" probe trained only pre-update. Report AUROC of the confidence drop for predicting forgotten items. Then compare targeted replay vs. random replay at equal tokens. **Kill** if AUROC < 0.65 for all three signals.

**Closest.** Calibration work ("Language models (mostly) know what they know", 2022) is static. Forgetting-prediction work uses external statistics (loss, example forgetting events [1812.05159](https://arxiv.org/abs/1812.05159)), not the model's self-report.

## 10. Counter-gradient data: protect skills when you only control the data

**Claim.** With closed fine-tuning APIs or someone else's training pipeline you control only the dataset. Gradient-matching (the mechanism behind data poisoning) can craft a few benign synthetic examples whose combined gradient cancels the component of the new-task update that hurts protected skills. That gives GEM/OGD-style projection in **data space**, enforced through a black-box optimizer.

**Pilot.** A local stand-in for the API: SmolLM-135M with fixed AdamW. Craft 1–5% extra examples by optimizing soft-then-discretized text (or images for a CIFAR version) to match the negative projected interference gradient. Compare with equal-size real replay, dataset-condensed replay and no protection, on retention and new-task accuracy. **Kill** if crafted examples beat equal-size real replay by < 20% of the retention gap, or if the effect disappears when the API's learning rate or shuffling changes.

**Closest.** Witches' Brew gradient-matching poisoning (Geiping et al. 2020) and dataset condensation for replay buffers. Neither aims to cancel a specific update's interference under an unknown optimizer.

## 11. The testing effect for language models

**Claim.** Humans retain more from retrieval practice than from re-reading. The LM analogue: replaying old knowledge as *self-generated question → own answer, kept only if verified* retains more per token than replaying the source text. Spacing each item's practice for when predicted retention falls to about 0.8 adds more. The hypothesized mechanism: generation trains the retrieval pathway (question → fact) that is actually queried, rather than the storage pathway.

**Pilot.** SmolLM-360M / Qwen2.5-0.5B on synthetic biographies (Physics-of-LMs style), with a stream of unrelated fine-tuning. At equal replay tokens, compare raw-text replay, teacher-written QA replay, self-generated verified QA replay, and spaced vs. uniform schedules. **Kill** if self-QA ≤ raw replay at equal tokens on held-out paraphrased queries.

**Closest.** [Knowledge acquisition with auxiliary views (2609.04180)](https://arxiv.org/abs/2609.04180) and QA augmentation papers improve *acquisition*. I found no retention-under-stream comparison of self-generated retrieval practice against re-reading.

## 12. Forgotten skills survive as subnetworks: residual skill bits

**Claim.** After task A is behaviourally forgotten, a binary mask over the *current* weights (no weight change) recovers A using far fewer mask bits than the same search needs on a random network of the same shape. The gap in bits (the "residual skill bits") is a new forgetting metric that separates erased from hidden skills. Its sign predicts whether replay or plain reactivation is needed.

**Pilot.** Supermask search (edge-popup) on MLP/ResNet-8 after Split-CIFAR streams. Report bits-to-recover vs. matched random-weight and never-trained controls, and correlate with relearning savings. **Kill** if the gap is < 10% of the random-net bits.

**Closest.** Supermasks in Superposition (Wortsman et al. 2020) uses masks to *store* tasks. [Hidden not Deleted (2609.27593)](https://arxiv.org/abs/2609.27593) shows suppression, not a bit-count metric.

## Proposer ranking

9 (metamemory) and 11 (testing effect) are the cheapest to make a clean paper from: each fits a single small LM, and a negative result is still informative. 10 is the most practically useful. 8 is the most "new physics" bet and pairs with batch 1 #1. 7 needs a corrected pilot before anyone believes it.
