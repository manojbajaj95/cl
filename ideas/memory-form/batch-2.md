# Memory-form proposer batch 2: layer-local lesson KV, prohibition lessons in text, an M2 note

Read before writing: ledger (PR #6), agent batches (PR #7), and the batch-1 verdicts. The verdict that killed M1 was that its prediction was linear algebra, so every kill line below tests a claim that a first-order expansion does not settle. Prior art checked via alphaXiv on 2026-11-24.

## Note for the M2 pilot (per-lesson attention-logit bias)
EASE-KV (2611.11299) already uses signed per-memory attention-logit biases over cached KV memories. It finds that learned allocation gains little over an evidence-guided reference, because binary correctness gives within-query reward contrast in only 53% of groups (74% with shaped reward). Hand-set recency bias recovers 19.5 of a 20.9-point temporal-conflict gap. So M2 is novel only if (a) the gradient on b_i is a dense log-prob gradient on logged actions, not outcome RL, and (b) the recurring-regime reversibility result holds. The pilot should add **EASE-KV evidence-guided allocation** and a **hand-set recency bias** as controls.

## N1. Layer-local lesson memory: store a lesson as KV visible only at the layers where its help lives
**Form.** A lesson cached as KV with a per-layer visibility mask m_ℓ ∈ {0,1}. Text is read at every layer and weights act at every layer; only KV memory can be exposed at some depths and hidden at others.
**Mechanism / claim.** A lesson helps the queries it targets through some layers, and it harms unrelated queries through other layers (The System Prompt Illusion finds persona and format prompts restructure intermediate layers while safety prompts barely move them). If help and harm are carried by different layers, masking the harm layers cuts off-target damage while keeping on-target gain. This is something a uniform down-weighting cannot do. It is not true by construction: if help and harm share layers, every mask scales both together, and the method reduces to M2's single scalar.
**Closest prior art.** The System Prompt Illusion (layer-selective effects of system prompts, analysis only); The Attentional White Bear Effect (head-level routing to prohibited concepts); DepthKV and layer-wise KV eviction (compression, not interference); EASE-KV (per-memory bias, not per-layer); Memory Attention (2609.28399). I found no use of per-layer visibility of a memory as a continual-learning interference control.
**Strongest control.** M2's global per-lesson logit bias tuned to give the **same on-target gain**. Layer-locality must win at matched help. Also: retrieval gating at equal recall, and a lesson rewritten to be narrower.
**Smallest falsifying test.** Qwen2.5-1.5B, 40 lessons from the existing tool-world, each with on-target and off-target probes. Pick masks greedily on a training split of probes (one forward pass per layer block) and evaluate on held-out probes. 3 seeds. **Kill** if, at ≥ 90% of full-visibility on-target gain, the layer mask does not cut off-target log-prob harm by ≥ 30% more than the matched global bias. Also kill if the chosen masks do not transfer to held-out probes (Spearman of per-layer help between splits < 0.5).

## N2. Prohibition lessons rebound in text memory as they accumulate, and the fix depends on memory form
**Form.** An agent's text memory fills with "don't do X" lessons over a long run (tool misuse, bad arguments). In text, a prohibition must mention X, and reading it routes attention to X. A logit-level or program constraint suppresses X without putting X in the context.
**Mechanism / claim.** Two predictions. (i) As text memory accumulates prohibition lessons, the per-lesson violation rate of *already-stored* prohibitions rises (an ironic-rebound interference between lessons), while the same lessons stored as decode-time constraints show no such rise. (ii) The rebound is predicted by how much attention the current state routes to the mentioned X tokens, which is an exact quantity available only because the memory is text.
**Closest prior art.** The Attentional White Bear Effect: prohibited concepts stay decodable and gain head-level routing under suppression instructions. It studies one instruction, not accumulation in agent memory. Pink-elephant / negation-following papers. Constrained decoding and guardrails (forms, not a CL result).
**Strongest control.** Rewrite each prohibition as a positive instruction in text ("use tool Y for Z"), at the same token budget. This cheap rewrite could tie the form switch outright. Also: a verifier with reject-and-resample at the same compute.
**Smallest falsifying test.** Synthetic tool world, 60 prohibition lessons added in 6 waves of 10. Measure the violation rate of wave-1 lessons after each wave, under text vs. positive-rewrite vs. logit-mask forms. Qwen2.5-1.5B, 3 seeds, 200 probes per wave. **Kill** if the wave-1 violation rate in text does not rise by ≥ 5 points from wave 1 to wave 6 (no rebound), or if the positive rewrite matches the logit mask within the CI.

## Killed at proposal (self-review)

| Idea | Why dropped |
|---|---|
| RoPE-distance aging: place older lessons at larger positional offsets | Reduces to a recency logit bias; EASE-KV hand-set recency already recovers most of the temporal-conflict gap |
| Dependency-conditioned KV encoding of lessons that refine earlier ones | EASE-KV (causal vs block-diagonal encoding), CacheBlend-style selective recompute, SemPIC |
| Pointer memory: weights learn when to recall a lesson id, text holds content | DSI++ (continual generative-retrieval forgetting), Adaptive Memory Index Evolution (2610.34977) |
| Per-rank decaying LoRA memory | Some Memories Must Fade (2611.25235): sparse k-hot LoRA ranks with per-rank decay plus a learned controller |
| Recurrent latent memory compiled across sessions | RPMem (2609.23466) |
| SSM-state memory written into slow decay modes | Mamba-CL (2411.15469), meta-learned Mamba CL (2412.00776), Naju (2607.21000) cover the retention/overwrite split |
