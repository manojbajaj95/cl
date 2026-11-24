# Flood pool: head-to-head, top-10 prior art, top 3

Pool: eight flood files plus the 36 cross-pool merges (PRs #36, #39, #41–#46; about 400 ideas). The novelty-only scores per file are in [flood-triage.md](flood-triage.md). Prior art comes from one or two alphaXiv searches per idea (2026-11-24). The cross-pool merges score no higher than their best part, so each merge is folded into its lead idea: X2 into L1, Y3 into SM1, X10 into N1, Y4 into kinetic proofreading, Y12 into spin echo.

## neuro-bio ([PR #46](https://github.com/manojbajaj95/cl/pull/46), 44 ideas)
4: NB05 delay-addressed skills, NB17 bivalent poised edits, NB24 field writes in developmental coordinates, NB21 regrowth from boundary conditions. 3: NB01, NB04, NB07, NB12, NB28, NB31, NB33, NB34, NB44. 2: the rest. All are primitives in framing; most are hard to pin to a first test.

## Top 10 with prior art

| Rank | Idea | Nearest prior art | Verdict |
|---|---|---|---|
| 1 | L1 prompt-addressable checkpoints (+X2) | Engram Injection [2610.15882](https://arxiv.org/abs/2610.15882) handles temporal validity per fact, not the whole model state; no hit for tag → past checkpoint | **Open. TOP 3** |
| 2 | SM1 seed-log autobiography (+Y3) | Seed-based ZO checkpointing (ZOCheck [2609.27189](https://arxiv.org/abs/2609.27189)) and exact ZO unlearning ([2610.35211](https://arxiv.org/abs/2610.35211)) already cover storing and removing updates as seeds. Nothing has the model read or edit its own log | **Half open. TOP 3** (the open half only) |
| 3 | P21 / SM2 learned weight ISA | W-ISA [2611.13232](https://arxiv.org/abs/2611.13232), WeightCode [2611.25476](https://arxiv.org/abs/2611.25476) | **KILLED: already done** |
| 4 | D1 deferred-commitment weights (+D2) | Superposition [1902.05522](https://arxiv.org/abs/1902.05522); Diversify-and-Disambiguate [2202.03418](https://arxiv.org/abs/2202.03418) (train hypotheses, pick later with few labels) | Mostly done. Only the CL label-delay setting is new: improvement |
| 5 | O1 / O2 idempotent and commutative learning operators | IDER idempotent replay [2603.00624](https://arxiv.org/abs/2603.00624); Lie bracket as a forgetting signal [2611.20087](https://arxiv.org/abs/2611.20087) | O1 done. O2 as a trained operator is open but leans on known BCH analysis: ambitious but doable, outside the top 3 |
| 6 | N1 round-trip consolidation, code → weights → code (+X10, S4, SM17) | Program Distillation [2611.19461](https://arxiv.org/abs/2611.19461) goes one way (LLM → program); Recursive Self-Editing [2611.29513](https://arxiv.org/abs/2611.29513) edits weights. No return trip claimed to improve the program | **Open. TOP 3** |
| 7 | SM7 neutral-drift reserve | Dynamical-isometry and FIRE plasticity resets ([2606.09762](https://arxiv.org/abs/2606.09762), [2602.08040](https://arxiv.org/abs/2602.08040)); no drift-based method | Open, but the drift must leave exact symmetries (see 8); ambitious but doable |
| 8 | Spin-echo refocusing (+Y12) | No hit | **Makes no sense as stated.** Training is equivariant under exact function-preserving symmetries, so a reflection changes nothing. Y12's "reflect only the drift" is a partial delta negation, which is known. Downgraded |
| 9 | Kinetic proofreading for lesson writes (+Y4) | No ML hit | Downgraded. k independent checks multiply false-accept rates, which is sequential testing, so the predicted exponential is trivial. The kinetic part (discrimination from different failure rates over time) has no clean analog yet. Kept as a gate arm of the contamination law |
| 10 | E2 logit price index (+P19 ABI) | Activation-monitor staleness after updates [2606.15980](https://arxiv.org/abs/2606.15980) | Partly done for monitors. Generalizing it to every threshold is an improvement |

Also checked: SM25 Lamarckian optimizer state (optimizer-state transport [2608.24593](https://arxiv.org/abs/2608.24593), trajectory transfer [2305.14122](https://arxiv.org/abs/2305.14122): mostly done) and W3 LR schedules as messages (distributed subliminal learning [2610.05378](https://arxiv.org/abs/2610.05378): close).

## Top 3: smallest first tests (each with a retention check)

**1. L1 prompt-addressable checkpoints (PRIMITIVE: model history becomes a capability of the weights, so rollback, diff and bisect are prompts).**
- Setup: Qwen2.5-0.5B with one LoRA trained over 5 sequential tasks. Task k's data carries the tag `<v_k>`, plus an as-of loss: under `<v_j>` (j < k), match stored checkpoint j's logits on 64 probe prompts per past version.
- Metric: KL(model | `<v_j>`, checkpoint j) on held-out inputs (not the probes), and task-j accuracy under `<v_j>`.
- Stacked control at equal tokens and bytes: untagged sequential training with replay of the same probe logits, plus storing per-version LoRA deltas at matched bytes.
- Kill: held-out as-of KL is not below the replay control (CI), or only the probes are reproduced.
- **Retention:** with the current tag, all 5 tasks and WikiText-2 perplexity stay within 1 pp and 2% of plain sequential training plus replay.
- Cost: about 2 CPU-h or 1 GPU-h.

**2. N1 round-trip consolidation (PRIMITIVE: weights act as a denoiser that hands back better programs).**
- Setup: the [PR #41](https://github.com/manojbajaj95/cl/pull/41) N1 pilot as written: Qwen2.5-Coder-1.5B, 12 string/grid families. The gate is that original helpers fail ≥ 30% of held-out variants.
- Arms: rewrite-and-generalize, plus k self-refinement rounds at matched compute, and a shuffled-label LoRA.
- Kill: the round trip is ≤ the best rewrite arm + 3 pp, or the shuffled LoRA ties it.
- **Retention:** after the LoRA, the model's pass@1 on HumanEval-lite (or 50 MBPP items) and on the 12 families' original seen inputs stays within 1 pp of the base model.
- Cost: about 1 GPU-h.

**3. SM1 self-readable seed log (PRIMITIVE, the open half: the model reads its own update history as text and edits it).**
- Setup: Qwen2.5-0.5B, MeZO over 5 tasks. Every step is logged as `(seed, scale, task, reason)`, so the weights regenerate exactly from the log.
- First check: bitwise regeneration. Then plant a regression (one task with corrupted labels).
- Test: a reader (the model itself, or a 7B model over the log) picks which lines to drop or rescale, compared with log bisect and random drops at equal evaluations. Also measure how far dropping lines differs from retraining without them, since later ZO scalars depended on earlier weights.
- Kill: the reader does no better than bisect at equal evaluations, or dropping lines departs from retrain-without by more than the regression it fixes.
- **Retention:** the other 4 tasks stay within 1 pp after the edit.
- Risk: MeZO may learn too little at 0.5B, so check that each task moves ≥ 5 pp first.
- Cost: about 3 CPU-h.

All three are PRIMITIVES, so none falls under the no-pilots-for-improvements rule.
