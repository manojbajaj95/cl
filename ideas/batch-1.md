# Proposer batch 1: symmetry, conservation and time in weights

Each idea: claim, why it might be new, a pilot that can kill it in under a day, and the closest work found (Hugging Face papers search, 2026-11-24). Excludes everything in `docs/frontier-scan.md`, PR #1, PR #2, the lesson-pool epidemic threshold and stream change identification.

## 1. Noether memory: an information channel SGD cannot erase

**Claim.** Gradient flow on a ReLU (or any positively homogeneous) layer conserves each unit's balancedness `d_i = ||w_in,i||² − ||w_out,i||²`. A function-preserving rescaling can write an arbitrary vector into `d` without changing the model's outputs. Whatever is written survives any later training under SGD, with drift only O(η²) and from weight decay. Attention adds matrix-valued charges (`W_Qᵀ W_Q − W_Kᵀ W_K` per head under the GL(d_head) symmetry). So a model has a forgetting-proof channel of roughly one real per hidden unit plus d_head² per head.

**Why it might matter.** (a) Science: it splits forgetting into "erased" and "unerasable" parts, giving a conservation law of continual learning. (b) Use: a rescue kit or provenance record that travels inside released weights through somebody else's fine-tuning pipeline, which an external file cannot do. Candidate payloads: a key routing to a stored adapter, a seed for regenerating a skill, or a hash of the training data.

**CPU sanity check (done, `pilots/noether_memory.py`).** 2-layer MLP, H=256, trained on task A. Write ±amp per unit into `d`; the function changed by 1e-14. Then train 3 × 3000 steps on three new 5-way tasks. Task A accuracy drops 0.98 → 0.23 (chance 0.20).

| write amplitude (natural spread of d ≈ 0.3) | SGD bit accuracy | Adam bit accuracy | non-conserved control (‖W1‖² channel), SGD |
|---|---|---|---|
| 1.0 | 1.000 | 0.975 (corr) | – |
| 0.3 | 1.000 | 0.836 | 0.902 |
| 0.1 | 1.000 | 0.543 | 0.664 |
| 0.03 | 0.996 | 0.473 | 0.559 |

The SGD channel survives at one tenth of the natural spread, while the non-conserved control decays to chance. As theory predicts, Adam breaks conservation; only large writes survive it.

**Pilot to kill it.** (1) Measure bits/unit that survive SGD+momentum, Adam and AdamW at LLM-like learning rates on a 2-layer transformer; derive the Adam drift law. (2) Store a payload that *restores* the forgotten task (a 64-bit key indexing a frozen adapter, or the coefficients of a low-rank head in a fixed random basis). Measure recovery of A after B,C,D vs. the same bytes stored in a non-conserved place. (3) Qwen2.5-0.5B: write into the MLP balancedness, LoRA/full fine-tune on a public SFT set, decode. **Kill** if, under AdamW at standard settings, fewer than ~1 bit/unit survive one epoch of fine-tuning.

**Closest work.** [Noether's Learning Dynamics (2105.02716)](https://arxiv.org/abs/2105.02716) and Du et al. 2018 (balancedness conserved) describe the conservation law. Kunin et al. use it to control rich/lazy regimes. Weight watermarking ([2507.11137](https://arxiv.org/abs/2507.11137)) is not function-exact and is not argued from conservation. I found no use of conserved charges as continual memory.

## 2. Gauge preconditioning: control someone else's optimizer without touching it

**Claim.** The same symmetries let you choose, without changing the function, each unit's effective learning rate under any future SGD or Adam. Rescaling by c makes incoming relative updates scale like 1/c² (SGD) or 1/c (Adam), and outgoing ones the reverse. LayerNorm-preceded weights are fully scale-invariant, so their norm is a free stiffness knob. A "sleep" step that picks the gauge from Fisher importance can make naive downstream fine-tuning forget less of chosen skills. That is EWC compiled into the weights, enforced on optimizers that never heard of it.

**Pilot.** Small transformer on two synthetic tasks, then Qwen2.5-0.5B. Gauge-fix by per-unit Fisher, fine-tune on a new task with stock AdamW, and compare retention vs. new-task accuracy against no gauge, EWC and L2-SP. Also try the adversarial direction: make a safety behaviour stiff against harmful fine-tuning. **Kill** if the gain at matched new-task accuracy is <25% of EWC's gain, or vanishes when the fine-tuner rescales or uses a schedule-free optimizer.

**Closest.** TAR ([2408.00761](https://arxiv.org/abs/2408.00761)) meta-learns tamper resistance with no exact function preservation. Effective-LR-from-weight-norm work (van Laarhoven 2017, Hoffer 2018) explains the mechanism but not its use as CL protection.

## 3. Rational forgetting: the learner's forgetting exponent should match the world's

**Claim.** Anderson & Schooler showed human retention mirrors the environment's need-odds, which follow a power law in time since last use. For a capacity-bounded learner on a stream whose task recurrences follow a power law with exponent α, prequential loss should be minimized when the learner's retention curve has the same exponent. SGD-trained nets have their own forgetting exponents, set by learning rate, decay and replay schedule. An online estimator of α, plus a replay/decay schedule chosen to match it, should beat any fixed schedule across α.

**Pilot.** Linear and MLP learners on synthetic streams with α ∈ {0.5, 1, 2} and no-recurrence controls. Measure each schedule's forgetting exponent and plot excess prequential loss against the exponent mismatch. **Kill** if the loss-minimizing learner exponent does not track α monotonically across the three α.

**Closest.** [Catastrophic interference is mitigated in naturalistic power-law environments (2401.10393)](https://arxiv.org/abs/2401.10393) changes the environment, not a matched learner exponent. The Ebbinghaus/spaced-replay CL papers use fixed schedules.

## 4. Weights remember time: decode the training order of forgotten tasks

**Claim.** Once accuracy on early tasks is back at chance, the final weights still encode *when* each task was learned. The order of a 4-task stream is decodable from permutation-invariant weight statistics far above chance. That would be direct evidence that behavioral forgetting is not erasure, plus a forensic tool: was this model fine-tuned on X before Y?

**Pilot.** 1,000 small MLPs on random orders of 4 tasks (≈1 CPU-hour). Train a meta-classifier on permutation-invariant features (per-layer singular spectra, sorted unit statistics, alignment of each task's probe gradient with the weights) and report bits of order recovered vs. a behavioral-probe-only baseline. **Kill** if order accuracy beyond the last task is at chance, or the behavioral baseline matches it.

**Closest.** [Hidden not Deleted (2609.27593)](https://arxiv.org/abs/2609.27593) and [hidden-state leakage after unlearning (2609.36612)](https://arxiv.org/abs/2609.36612) show retained content, not recoverable chronology. Dataset inference gives membership, not order.

## 5. Forgetting as dynamical instability

**Claim.** Abrupt forgetting (as opposed to gradual drift) starts when new-task training pushes the old task's local curvature past 2/η, the edge of stability for the old minimum. That gives a predictive, learning-rate-dependent threshold and a one-number trigger for when to replay.

**Pilot.** Track the old-task Hessian top eigenvalue by power iteration during new-task training at 4 learning rates. **Kill** if the onset of the forgetting jump is not predicted within ±10% of steps in ≥3 of 4 learning rates, or if a plain gradient-alignment signal predicts it equally well.

**Closest.** [Mirzadeh et al. (2006.06958)](https://arxiv.org/abs/2006.06958) links wide minima to retention. The [stability gap (2205.13452)](https://arxiv.org/abs/2205.13452) describes transient drops. Neither gives a 2/η crossing criterion.

## 6. Agents: Fisher information for text memories

**Claim.** When an agent "learns" by rewriting a memory or system prompt, its forgetting is the deletion or paraphrase of sentences that past successes depended on. Estimating per-sentence importance by counterfactual ablation on a small replay set, then protecting high-importance sentences during rewrites, gives EWC for text. It should beat recency/decay heuristics at a fixed token budget.

**Pilot.** Qwen2.5-1.5B (CPU GGUF) agent on a stream of rule-following tasks whose rules recur. Compare rewrite-free append+retrieve, FadeMem-style decay and textual-Fisher protection at equal memory tokens. **Kill** if append+retrieve matches at equal tokens.

**Closest.** [FadeMem (2601.18642)](https://arxiv.org/abs/2601.18642) uses biologically inspired decay without counterfactual importance.

## Proposer ranking

1 and 2 first. They share one mechanism, have a CPU result already, and give both a conservation-law science claim and a concrete use (forgetting-proof payloads; optimizer-agnostic protection). 4 is the cheapest independent bet. 3, 5 and 6 are fallbacks.
