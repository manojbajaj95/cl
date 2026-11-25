# Memory-form proposer batch 1: KV-slot plasticity, graded salience for text lessons, an E1 arm

Angle: the form agent memory takes (text, KV cache, weights, programs, latent states, hybrids) and mechanisms that exist only because of that form. I read the ledger (PR #6) and agent batches 1-11 (PR #7) first. Prior art checked via alphaXiv on 2026-11-24.

## M1. Attention-gated plasticity: a trainable KV memory forgets in proportion to the attention it gets off-target
**Form.** A fixed set of trainable KV slots (a continually updated cartridge / prefix) read by a frozen model, versus LoRA with the same parameter count.
**Mechanism (only in KV form).** A gradient into a KV slot reaches the output only through attention, so a write changes the model's behaviour on any query q by an amount scaled by a(q), the attention mass q puts on that slot. LoRA has no such gate: its ΔW acts on every input. Prediction: per-query drift on old tasks after a write is ≈ proportional to a(q) · ‖Δv‖, so (i) forgetting in KV memory is predictable from one forward pass (read a(q) on old probes), and (ii) a per-slot logit bias b (one scalar per slot, set at write time) is a stability dial: lowering b for off-target keys cuts forgetting with no regulariser or replay.
**Closest prior art.** Cartridges (2506.06266), Cartridges at Scale (2606.04557), Cartridges++ (2609.35621) train KV caches for static corpora, not sequential writes. Sparse memory finetuning (2510.15103, 2605.03229) gets low forgetting from sparse slot selection, not attention gating. LoRA vs N-gram drift (2610.14921) and Delta N-gram (2610.31125) compare other memory forms. I found no claim that KV-slot forgetting is set by off-target attention mass, and no use of a slot bias as a stability knob.
**Strongest control.** Sparse memory finetuning at equal trainable parameters and equal write steps (it already gates writes, by TF-IDF slot choice). Also LoRA, and the same KV memory without the bias dial.
**Smallest falsifying test.** Qwen2.5-0.5B frozen, 64 trainable KV slots per layer, a stream of 20 synthetic fact documents written one at a time by self-study loss; old-fact probes after each write. 3 seeds. **Kill** if the Spearman between a(q)·‖Δv‖ and per-probe old-fact log-prob drop is < 0.5, or if the KV memory (with the dial) is not on a better retention-vs-acquisition Pareto front than sparse memory finetuning beyond the seed CI.

## M2. Graded, reversible forgetting for in-context lessons: learn one attention-logit bias per lesson from outcomes
**Form.** Text lessons in context. Today a lesson is either in context or deleted; weights have no per-memory handle at all.
**Mechanism (only because the lesson is read by attention).** Add a scalar b_i to the attention logits of every token of lesson i (all heads, all layers). b_i is differentiable: one backward pass on N scalars from the task loss of a logged episode gives ∂loss/∂b_i exactly. So the agent learns each lesson's salience online from outcomes, instead of an LLM deciding to keep or delete it. Under recurring drift (a lesson goes stale and later becomes valid again), a down-weighted lesson comes back in a few gradient steps, while a deleted one must be rediscovered. Prediction: graded salience beats binary curation on streams with recurring regimes and on partially valid lessons, and ties it on streams with permanent change.
**Closest prior art.** Mechanistic Attention Guidance for Agent Memory Refinement (2607.17621) reads attention as a diagnostic to rewrite text; it learns no salience. Prompt highlighting / attention steering (PASTA; 2603.01281; 2603.10705) up-weights spans a user names. Learned memory curation (2609.37930, 2610.26453, 2606.21144) learns keep/delete policies in text. Activation-steering memories (2610.14958, 2606.29824) are a different form. I found no outcome-trained per-lesson attention bias for agent memory.
**Strongest control.** Binary subset selection driven by the same feedback at the same compute: leave-one-out log-likelihood credit per lesson with a threshold, re-inclusion allowed. Also an ACE-style helpful/harmful counter per lesson, and an "outdated?" text tag.
**Smallest falsifying test.** Qwen2.5-0.5B (CPU), synthetic tool world with 3 regimes that recur (A, B, A, C, B ...), 30 lessons in context, 600 episodes, 3 seeds. **Kill** if learned b does not beat the binary-selection control by ≥ 5 points of success on returns to a previous regime (beyond the seed CI), or if it loses > 2 points on first-visit regimes.

## M3. (Arm for E1) Query variance of a lesson's in-context effect predicts how much consolidating it into weights forgets
**Form.** Hybrid text → weights. A lesson in context acts through a query-dependent implicit update (its effect δh(q) on the residual stream depends on how the query attends to it). A weight update is query-independent. Consolidating a lesson whose effect points in different directions for different queries forces one ΔW to cover them all, so it must over-apply off-target.
**Mechanism.** Gating index G = 1 − ‖E_q δh(q)‖² / E_q ‖δh(q)‖² over on- and off-target probes at one mid layer. High G: the context gates the lesson strongly, and consolidation will forget or under-apply. Low G: consolidation is lossless. This also gives a form-routing rule: consolidate low-G lessons into LoRA, keep high-G ones in text or a key-gated memory layer.
**Closest prior art.** E1 (passed, gated on B3) predicts consolidation from the lesson's ΔW share in the LoRA span; G is about direction variance across queries, which a span share does not see. Implicit in-context updates: 2507.16003. Context-induced degradation after distillation (2606.11627).
**Strongest control.** E1's own controls: in-context effect size, first-step distillation loss, the projected distillation gradient, plus the plain off-target in-context KL (magnitude without direction).
**Smallest falsifying test.** Run inside E1 on its 200 lessons. **Kill** if G does not add ≥ 0.1 Spearman over E1's score and the off-target KL for predicting off-target drift after consolidation.

## Killed at proposal (self-review)

| Idea | Why dropped |
|---|---|
| Fossil KV: pre-update KV caches restore skills the update forgot | KV-cache patching (2610.41480) already shows base KV in the fine-tuned model removes fine-tuned behaviour; cross-update reuse studied in 2611.14051 |
| Double counting: keeping a lesson in context after consolidating it over-applies it | Context-induced degradation after on-policy distillation (2606.11627) |
| Lessons misread after weight updates; lesson signatures to rewrite them | Memory portability (2609.05339), memory canonicalization (2610.05124) |
| Stale-vs-fresh KV divergence as a per-lesson reading-drift detector | Functional cache divergence (2611.14051); keeping the old checkpoint is the cheap exact control |
| Memory rebase: re-derive lessons written while a bad lesson was in context | Dependency-guided rollback repair (2608.10502), dependency-aware revision (2611.02912), AfterDeleteBench (2610.31366) |
| Steering-vector / function-vector lesson memory | 2610.14958, 2606.29824 |
| Cross-episode latent token memory | MemGen (2509.24704), 2605.21951, ElasticMem (2605.30690) |
| Re-project stale keys after a weight update | KV-Lingo (2609.32610), PatchKV (2609.39329), CacheLink (2610.15509) |
| Fine-tune, extract template-position KV, revert weights | Same hypothesis space as prefix tuning; ties per-task LoRA swap (save/restore pattern) |
| Collision-coded reads for hashed N-gram memory | Delta N-gram (2610.31125): interference comes from one n-gram shared by many contexts, not hash collisions; a larger table does not help |
| Program memory with past episodes as regression tests | Skill-V (2610.11781), DoppelVet (2611.29306); exact by construction |
| Test-time-training fast weights as agent memory | Crowded: 2610.36794, 2610.23942, 2610.05303 |
| Ski-rental timing for context → weights consolidation | A scheduling result (cf. killed delay-compensated gating); 2611.10982 covers the cost tradeoff |
