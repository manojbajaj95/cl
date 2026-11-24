# Proposer batch 3: make the charge channel useful, edit-capacity physics, agent memory languages

Same format as batches [1](batch-1.md) and [2](batch-2.md). I dropped one candidate because the area is crowded: compiling agent text memory into weights by hindsight self-distillation, already covered by [ASCENT (2610.05303)](https://arxiv.org/abs/2610.05303), [experience internalization (2606.04703)](https://arxiv.org/abs/2606.04703) and [context-distillation knowledge updates (2602.16093)](https://arxiv.org/abs/2602.16093).

## 13. Noether-keyed skills: turn the unerasable channel into a working restore path

**The objection to batch 1 #1 that this answers.** A conserved payload does not affect the function, so on its own it restores nothing. The fix: a *frozen, stop-gradient reader* `R(Q(θ))` maps the conserved charges `Q` to a key, the key selects a frozen adapter or skill program from a side bank, and the forward pass adds it. Training never back-propagates through `Q`, so the gradient keeps the symmetry and the charges stay conserved. A model can then lose a skill behaviourally to someone else's SGD and still carry an intact pointer to its restoration, which no hand-off file or metadata field guarantees.

**Pilot.** (1) Reuse `pilots/noether_memory.py` and add a 64-bit key with a Hamming-ECC code over 256 units. Measure decoded-key error under SGD, momentum and AdamW. (2) Two-skill MLP with a frozen adapter bank. After fine-tuning on unrelated data, compare restored skill accuracy using keys decoded from charges vs. keys stored in a non-conserved weight statistic. (3) Measure how much the adapter must be re-fit to the drifted features: a pointer to a stale adapter may be useless, which would kill the "restore" claim and leave only provenance. **Kill** if restored accuracy after drift is no better than re-fitting a fresh head on the same few-shot data.

## 14. A Hopfield-style capacity law for sequential model edits

**Claim.** Sequential rank-1 key→value edits in a transformer MLP (ROME/MEMIT family) behave like writes into a linear associative memory. Collapse should then appear at a critical edit count `N* ≈ c · d_ff / κ`, where κ is set by the effective rank / spectral spread of the edit keys' covariance. That predicts a phase transition, not gradual decay, plus a constant measurable before editing. It would turn "editing eventually collapses" ([2402.09656](https://arxiv.org/abs/2402.09656)) into a law with a predicted N*.

**Pilot.** GPT-2-small and Pythia-160M/410M, MEMIT on CounterFact-style synthetic facts with controlled key correlation (paraphrase-tied vs. random subjects). Sweep d_ff (layer choice) and key correlation, and fit N* against the predicted ratio. **Kill** if N* is not within 2× of prediction across ≥3 model sizes, or if the degradation curve has no sharp knee.

**Closest.** Collapse and long-horizon editing work ([2602.02543](https://arxiv.org/abs/2602.02543), [2502.01636](https://arxiv.org/abs/2502.01636), [WISE 2405.14768](https://arxiv.org/abs/2405.14768)) fixes or postpones collapse empirically. None predicts N* from key statistics.

## 15. Emergent memory languages for agents

**Claim.** Under a hard memory-token budget, an agent that iteratively refines its own **private shorthand** (abbreviations, symbols, implicit structure it alone decodes) stores more usable experience per token than natural-language summaries or structured notes. The twist that makes it a continual-learning question: the shorthand is a contract between writer and reader that may break when the reading model is upgraded. Measure how much private compression costs in portability, and whether a "translate-before-upgrade" step pays for it.

**Pilot.** Qwen2.5-1.5B (CPU GGUF) on a stream of 300 rule/fact episodes with a 512-token memory. Arms: NL summary, JSON notes, and self-refined shorthand (the agent rewrites memory to maximize its own future answer accuracy on a held-out dev stream). Then swap the reader to Qwen2.5-3B or Llama-3.2-3B with and without a translation pass. **Kill** if shorthand does not beat the best NL arm by ≥5 points at equal tokens on held-out episodes.

**Closest.** [MemSkill (2602.02474)](https://arxiv.org/abs/2602.02474), [A-MEM (2502.12110)](https://arxiv.org/abs/2502.12110) and gist/prompt-compression work learn *what* to store in human-readable or soft-token form. The emergent-communication literature studies agent-to-agent codes, not a code an agent uses with its future self, nor robustness to swapping the reader.

## 16. Forecast forgetting from the update alone

**Claim.** A small learned model can predict, from a cheap sketch of a candidate update (random projection of the parameter delta, per-layer norms, alignment with stored skill-gradient sketches), each tracked skill's accuracy change *before the update is applied or evaluated*. If it generalizes to unseen update types (new datasets, LoRA vs. full, different learning rates), continual learners get an almost-free gate: reject, shrink or route updates predicted to cause forgetting, and evaluate only the uncertain ones.

**Pilot.** SmolLM-135M: run 400 short fine-tunes on varied public subsets and record each delta's sketch and its effect on a 20-skill probe suite. Train the predictor on 300 and test on 100 drawn from held-out data sources. Compare against a first-order Taylor baseline (`g_skill · Δθ`), a Fisher-weighted norm, and evaluation on 5% of the probe set (the PR #2 audit style). **Kill** if the predictor's rank correlation with true deltas on held-out sources does not beat the Taylor baseline by ≥0.15.

**Closest.** The verifier-measured audit in PR #2 measures retention by evaluation. Data-attribution/TRAK-style methods predict per-example influence on a *fixed* model, not per-skill effects of arbitrary updates across update types.

## 17. Iterated learning as a regulariser for agent lessons

**Claim.** Pass an agent's lesson pool through a chain of generations. Each fresh agent learns only from the previous generation's lessons under a length bottleneck, then acts and rewrites. Cultural-evolution theory predicts that lessons drift toward compressible, general rules: better transfer to new task variants and fewer brittle episode-specific notes, at the price of accumulated shared bias. That gives a training-free generalization pressure for agent memories, plus a measurable bias-amplification failure mode.

**Pilot.** Qwen2.5-1.5B agent on rule-induction tasks with held-out variants. Compare 1, 3 and 10 generations at a fixed lesson budget against a single-generation summary at the same budget. Track transfer accuracy and lesson generality (fraction of lessons that mention specific episodes), and seed a false rule to measure bias amplification. **Kill** if 10 generations do not beat one-shot summarization on held-out variants by ≥5 points, or if bias amplification dominates in every run.

**Closest.** Iterated-learning bias amplification in LLMs (Ren et al. 2024) studies preferences, not task-solving memories. The lesson-pool epidemic project (in progress) studies spread across agents within one generation, not a generational bottleneck. Check the overlap with that team before running.

## Proposer ranking across batches

1. **Batch 1 #1 + batch 3 #13 (Noether memory → keyed restore).** It has a CPU result, a conservation-law science claim and a clear failure mode to test next: whether a stale adapter is useless after drift.
2. **Batch 2 #9 (metamemory)** and **#11 (testing effect).** Single small LM, clean either way.
3. **Batch 3 #14 (edit capacity law).** A sharp, theory-predicted phase transition if it holds.
4. **Batch 3 #16 (forecast forgetting).** The most practical; it complements PR #2.
