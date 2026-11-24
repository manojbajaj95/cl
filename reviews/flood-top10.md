# Expanded-pool top 10 (supersedes the round-1 list below)

Pool: about 1,960 ideas (round 1: about 400 across PRs #36, #39, #41–#46; round 2: about 1,560 across PRs #47–#94). Ranked head to head on novelty only. Every entry is a PRIMITIVE and AMBITIOUS BUT DOABLE. Prior-art check: alphaXiv quota was exhausted, so these use arXiv full-text search and abstracts. "None found" is weaker evidence than a full alphaXiv read and should be re-checked before writing.

| # | Idea (source) | Nearest prior art | Verdict |
|---|---|---|---|
| 1 | Waterbed law for forgetting (CD2, PR #74): a Bode-style sensitivity integral; cutting forgetting at some timescales must raise it at others | None found (Bode/forgetting, conservation-law/forgetting searches) | Open |
| 2 | Nerode quotient of edits (PR #91 #1/#2, + PR #92 #8; rediscovered in PRs #95, #96, #98; developed in [PR #104](https://github.com/manojbajaj95/cl/pull/104)): two edits are equal iff every later edit acts the same on both; learned with L\* | None found as a CL object; edit-effect clustering (PR #63) uses immediate effects only. The machinery is prior: observability closure / minimal realization, predictive state representations, bisimulation | Open; PR #104 shows function-identical states (uv with (u,v) = (1,1) vs (2,½)) diverge after one gradient step, so the quotient cannot be read off current outputs |
| 3 | Write-skew between lessons (SD3, PR #58, + PR #88 #8, PR #92 #9, inversions 21, M2): each update is safe alone, the set breaks an invariant | Merging spectral regularization (2611.17728) is pairwise; PR #89's probe motivates it: 47 correct, unrelated rules remove about 58% (0.5B) / 56% (1.5B) of one rule's uplift over an empty store, revised by [PR #103](https://github.com/manojbajaj95/cl/pull/103) from 99% / 63% of solo margin. That is set-level load, not yet a three-way effect: no singleton or pair was checked at a fixed tolerance | Open; motivating result, not yet evidence of write-skew |
| 4 | Rate–drift law for stored memories ([PR #105](https://github.com/manojbajaj95/cl/pull/105), + round-10 W8/W10): a compressed edit, lesson or index is decoded with the current model as side information, so its install-time saving is a loan that later training calls in. Zero-error bound: χ(G_0 ∪ … ∪ G_H) over the training trajectory; durable compression = information about training's invariants; "keep f(x)" constraints are incompressible under drift | Read in full: the math is classical, as side information at many decoders and side information that may be absent (Heegard–Berger; Timo et al. [0901.1705](https://arxiv.org/abs/0901.1705)) and uncertain side-information delay ([1109.1293](https://arxiv.org/abs/1109.1293)). The ML instance of the loan is backfilling under model updates (BCT [2003.11942](https://arxiv.org/abs/2003.11942), L2R [2308.11512](https://arxiv.org/abs/2308.11512)), which repairs it by training rather than pricing it. Semantic communication with drifting knowledge bases ([2301.03133](https://arxiv.org/abs/2301.03133)) syncs parameters. Edit survival is measured but not priced: edits decay under later fine-tuning ([2511.05852](https://arxiv.org/abs/2511.05852)), and behaviour recovers without reversing the weight edit ([2608.24988](https://arxiv.org/abs/2608.24988)). Replay-necessity results bound the learner's memory, not a description's validity: perfect memory ([2006.05188](https://arxiv.org/abs/2006.05188)), Ω(k) memory ([2204.10830](https://arxiv.org/abs/2204.10830)). No R(Δ) for a learner decoding its own memories found | **Open, novelty provisional:** the theorem is classical, so the claim rests on the CL object and a measured R(Δ) on a real model. Probe reproduced (toy table receiver). Risk: it is the decoder-side counterpart of #6 dirty-paper writes |
| 5 | Relearning as the read head (inversions 03, PR #72): a memory that is readable only through relearning speed | Relearning attacks on unlearning (2506.01318, 2502.05374, 2605.11685) show the phenomenon; none use it as a designed channel | Open as a channel |
| 6 | Dirty-paper coding of a new task against known old weights (PR #56) | Learned DPC exists for communication only (2507.17427) | Open for weights; risk from #4: precoding against the old weights borrows the same loan, so the gain may decay as training continues |
| 7 | Gauge-orbit metadata (PR #53, + PR #69 #10, PR #67 #12): tags in function-preserving unit permutations | Neuron-permutation attacks and re-alignment for watermarks (2312.14182, 2112.14108) | Open as CL provenance; risk: the canonical order drifts with training |
| 8 | N1 round-trip consolidation (PR #41) | Program Distillation 2611.19461 is one-way | Open; test paused (PR #55) |
| 9 | Executable weight header with a consistency loss (PR #53, PR #69 #1, PR #91 #12) | Meta Models 2610.37001 and TuneAhead 2606.17660 predict training externally | Open for an in-weights, self-consistent header |
| 10 | SM1 self-readable seed log, the open half (PR #43) | ZOCheck 2609.27189, exact ZO unlearning 2610.35211 cover storage and undo | Open half only; test paused (PR #54) |

Revised after [PR #105](https://github.com/manojbajaj95/cl/pull/105): the rate–drift law enters at #4, old #4–#7 move to #5–#8, and re-derivability memory (old #8) drops to the next tier. Triage rows written before this revision use the old numbers.

Next: re-derivability memory (LP39, PR #59; partly covered by Beyond Gain 2610.32322), WOM codes (PR #56), question barcodes (PR #50 #3 + PR #86), edge-addressable weights (B6), P19 ABI. Falsified: L1.

## Smallest first tests (each with a retention check)

1. **Waterbed law.** Two-layer linear teacher–student, CPU. Drive the task mixture sinusoidally at 12 frequencies and measure forgetting gain |S(ω)| for plain SGD, EWC, replay, and two LRs, at matched final accuracy. **Kill:** ∫log|S(ω)|dω varies > 20% across methods (no invariant). **Retention:** old-task accuracy is the measured quantity; also report it at the end of the stream. About 1 CPU-h.
2. **Nerode quotient.** Evaluator check first ([PR #104](https://github.com/manojbajaj95/cl/pull/104)): reproduce the exact affine closure oracle (a visible register, an unreadable tail, edits that expose the tail). Then a small transformer on modular arithmetic, with output- and margin-matched histories as the hard rival; 200 random rank-1 edits, each followed by 50 continuation edits. Count classes against tolerance. Check [PR #108](https://github.com/manojbajaj95/cl/pull/108)'s prediction: classes merge only at singular steps (weight decay to zero, dead units), never under invertible updates. **Kill:** class count grows linearly with edits, or classes predict post-continuation outcome no better than immediate-effect clustering. **Retention:** classes must predict old-task accuracy after continuation. About 2 CPU-h.
3. **Write-skew.** Qwen2.5-0.5B, 30 lesson triples B,C,D over a fixed old rule A (in context first, as PR #89; LoRA only after the context result). Evaluate all 8 subsets with matched placeholders in unused slots ([PR #103](https://github.com/manojbajaj95/cl/pull/103) protocol). A strict witness keeps A above a pre-registered floor for every proper subset and drops it for BCD; also measure the interaction contrast m(BCD) − Σpairs + Σsingles − m(∅) on fixed-rival margins. **Kill:** the contrast is < 10% of pairwise effects, or matched disjoint filler triples and a count-only curve fitted on other stores explain it. **Retention:** old-task probes per triple. About 2 CPU-h.
4. **Rate–drift law.** Gate: reproduce PR #105's table receiver (done). Then a small MLP on modular arithmetic: install 200 rank-1 edits from descriptions decoded against the current model, continue training on unrelated tasks for H = 0…32 steps, and measure the bits needed to keep each edit decodable. Fit R(Δ) against drift measured as functional distance, and against drift projected on the directions that separate intents (round 11 RD1); the law should prefer the second. **Prediction:** the description grows to the full-intent rate under free drift, and stays at the invariant limit when a probe set is held fixed by replay. **Control:** explicit post-edit targets and stored raw anchors at equal bits. **Kill:** R does not track drift (rank correlation < 0.5), or the invariant limit misses by more than 0.5 bits. **Retention:** old-task accuracy after H steps, which the law should predict from the description's decode error. Score separately ([PR #106](https://github.com/manojbajaj95/cl/pull/106)): the description still decodes, the edit meets its obligation without reapplication, old tasks hold. Exact linear check first: a write in U⊥ survives when all future inputs lie in U, and fails under weight decay or one input outside U. About 2 CPU-h.
5. **Relearning read head.** Write N facts, then mask recall to chance; read by k-step relearning speed. **Control:** shuffled-label relearning at matched steps. **Kill:** savings ≤ control or capacity below direct storage. **Retention:** normal tasks and perplexity within 1 pp / 2%. About 1 GPU-h on 0.5B.
6. **Dirty-paper writes.** Small MLP; precode the new-task update against known old weights versus GPM/OWM projection at equal update norm. **Kill:** no gain over GPM. **Retention:** old-task accuracy is the primary metric. About 1 CPU-h.
7. **Gauge-orbit tags.** Encode 64 bits in MLP unit permutations of 0.5B relative to a canonical sort; fine-tune on 5 tasks; decode. **Kill:** bit error > 10% after 1 task. **Retention:** outputs bitwise equal before fine-tuning; task scores unchanged. About 1 CPU-h.
8. **N1.** As written in the round-1 section (PR #55). **Retention:** MBPP and seen inputs within 1 pp.
9. **Weight header.** 0.5B LoRA with a per-block header trained to predict Δloss on probes for proposed writes, under a consistency loss. **Control:** an external TabPFN meta-model with equal parameters. **Kill:** the header doesn't beat the external predictor or goes stale after 3 tasks. **Retention:** base tasks within 1 pp with the header on.
10. **SM1.** As written in the round-1 section (PR #54). **Retention:** the other 4 tasks within 1 pp.

---

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
