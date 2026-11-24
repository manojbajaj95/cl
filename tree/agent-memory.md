# Node: agent memory — why lessons, skills and retrieval don't compound

Parent question: why agent memory (lessons, skills, retrieval) fails to give lasting, compounding improvement without degradation.

## Root cause in one line

**A memory item has no denotation.** Its effect on behaviour is not a property of the item. A frozen reader re-derives it at every read, by imitation, against its priors and against everything else in the store. So items cannot add up (no superposition), their value cannot be measured (no identifiability), consolidation cannot be checked (no invariant to preserve), and stale items keep acting with the weight of their repetition (no scope). Compounding needs a memory whose items are operators with a fixed, composable, checkable effect. Weight-space programming gives weights that property. Agent memory has nothing like it.

## Evidence

### Quick CPU probe (this PR, `tree/probes/`)

Setup: arbitrary key → queue rules (no prior can supply them), Qwen2.5-0.5B-Instruct, 4 seeds × 6 probe items (table below), replicated on 1.5B. Each probed item's own correct rule is always in the store. Every other rule is also correct and about a different key. So the store never conflicts; it only grows.

| Rules in store k | Accuracy (chance 17%) | Target margin (logits) | Same rule alone |
|---|---|---|---|
| 0 (no memory) | — | −2.98 | — |
| 1 | 100% | +4.19 | +4.19 |
| 4 | 83% | +1.32 | +4.19 |
| 16 | 50% | +0.12 | +4.19 |
| 48 | 54% | +0.05 | +4.19 |

- A correct rule loses about 99% of its effect (+4.19 → +0.05 logits) when 47 other correct, unrelated rules sit beside it. The store's value is not the sum of its items' values: adding items erases old ones, even though nothing conflicts.
- Revision under repeated experience (old rule repeated r times, then one explicit "UPDATE (latest, overrides earlier rules)" at the end): P(new) falls from 0.38 to 0.30 and P(old) rises from 0.35 to 0.41 as r goes from 1 to 8. More experience makes updates weaker. This is the dose-response that Experience Rot reports (below), reproduced with a 0.5B reader on arbitrary rules.
- Caveat: a keyed top-1 lookup would trivially fix this task (as in N1). The point is not that recall needs retrieval; it is that whatever reaches the reader together has no additive semantics, and abstraction, consolidation and multi-item composition all need several items read together.
- Replication, Qwen2.5-1.5B-Instruct (3 seeds): the same direction, weaker. Target margin goes +8.37 (alone) → +7.13 / +4.91 / +3.09 at k = 4 / 16 / 48 (63% of the effect gone at k = 48), and accuracy drops from 100% to 83%. Under the revision test P(old) rises from 0.02 to 0.17 and P(new) falls from 0.97 to 0.81 as r goes from 1 to 8. Scale reduces the erasure but does not remove it; both curves are still falling at the largest k and r tested.

### Papers (alphaXiv, 2026)

| Failure | Evidence | What it shows about the root cause |
|---|---|---|
| Low gain | Anchor [2611.10382](https://arxiv.org/abs/2611.10382): replaying source decisions with and without a candidate memory, "most candidates barely shift the probed distribution". In-house PR #31: a directive shifts the named action by ~0.6–1.0 logit; A3: an entropy-matched temperature reproduces ~95% of lesson effects | Items are read as weak nudges against priors (margin competition, [2604.23750](https://arxiv.org/abs/2604.23750)) |
| Imitation, not evaluation | [2610.11152](https://arxiv.org/abs/2610.11152): flipping, randomizing or removing rewards in in-context RL leaves the improvement curve almost unchanged; shuffled or corrupted trajectories work as well as real ones | The reader does not use the content that would let improvement compound (outcomes, credit) |
| Copying stale experience | Experience Rot [2611.20922](https://arxiv.org/abs/2611.20922): after a silent tool change, experienced agents fail on most tasks where novices succeed; they copy the old call even when the definition shows the change; the failure grows with experience and appears in every memory form tested. Stale skills cost >10 pp ([2611.22525](https://arxiv.org/abs/2611.22525)) | Items carry no validity scope; their weight comes from repetition |
| Consolidation drifts | [2605.12978](https://arxiv.org/abs/2605.12978): consolidated memory utility rises, then falls below no-memory; GPT-5.4 consolidating from ground-truth solutions fails 54% of ARC problems it solved without memory; an episodic-only control stays competitive | The rewriter has no invariant to preserve |
| Values unidentifiable | [2611.03289](https://arxiv.org/abs/2611.03289): top-k retrieval leaves every memory value undetermined however many episodes are logged (0 of 55 configurations determined any value) | Credit, pruning and curation run blind |
| Noise and order | [2608.18066](https://arxiv.org/abs/2608.18066): self-improving loops raise run variance in 71% of cases; shuffled task order gives −4.5% instead of +1.5% | Updates do not commute; the default curriculum was carrying the result |
| No transfer | [2610.22984](https://arxiv.org/abs/2610.22984): failure-derived memory repairs seen failures but rarely helps unseen tasks. ContinualSkillBench [2608.03874](https://arxiv.org/abs/2608.03874): keeping raw context and feedback ≈ maintaining a skill library | Abstraction adds little over storing raw episodes |

Already tried in this repo and dead (ledger, PR #6): per-lesson attention-logit salience (M2), layer-local KV masks (N1), offline IS ranking of lessons (G1), obsolescence predictor (Q2), interference prediction from implicit ΔW (B3), double dosing (M3). All of them tried to fix one symptom (salience, routing, valuation) on top of the same reader. None changed what an item means.

Nearby fixes that keep the root cause: compile text into adapters (Doc-to-LoRA [2602.15902](https://arxiv.org/abs/2602.15902), LatentSkill [2606.06087](https://arxiv.org/abs/2606.06087), CLAM [2611.20759](https://arxiv.org/abs/2611.20759)), task operators ([2610.01054](https://arxiv.org/abs/2610.01054)), and parallel context-of-experts decoding ([2601.08670](https://arxiv.org/abs/2601.08670)). They change where the item lives. None specifies what the item must do, so the four properties (gain, superposition, identifiability, scope) are still unguaranteed. Task-vector composition is input-conditioned and non-additive ([2608.09490](https://arxiv.org/abs/2608.09490)).

## What compounding would require

1. **Gain**: an item can move behaviour by as much as its evidence warrants, not by a fixed ~1 logit.
2. **Superposition**: the effect of a set of items is a known function (ideally a sum) of each item's effect.
3. **Identifiability**: each item's effect can be measured, so credit and pruning are possible.
4. **Scope**: each item says where it applies, and it stops acting outside that region or after evidence against it.

Current memories have none of the four. The ideas below each try to build one or more of them in as primitives.

## Ideas (raw, unfiltered)

Each: mechanism · why new · cheapest first test · likely tie (for the reviewer).

1. **Memory ISA: train the reader to execute memory with a contract.** Fine-tune a reader on synthetic stores so that an item `IF c THEN shift(a, w)` moves log-odds of `a` by exactly `w` when `c` holds, and by 0 otherwise, independent of the other items. Memory becomes a programming language with fixed semantics, and the model becomes its interpreter. · New: prior work trains instruction following; nothing trains calibrated, additive, weighted execution of a store. · Test: LoRA on 0.5B with synthetic weighted rules; on held-out rule families measure slope of realized vs specified `w` and additivity at k = 48 (the probe above is the before picture). · Tie: plain SFT on rule following at equal data.
2. **Denotational memory (product of single-item experts).** Read each item alone, take its logit delta against the no-memory reader, and combine deltas explicitly: `logits = base + Σ g_i·Δ_i(x)`. Superposition holds by construction, and the per-item delta is the item's measured meaning. · New: parallel-context decoding mixes documents; this uses per-item deltas as an algebra with a learned gain per item. · Test: the probe at k = 48: summed solo deltas vs concatenated context. · Tie: top-1 keyed retrieval on keyed tasks; needs a task where several items must combine.
3. **Memory fingerprints.** Store each item with its behavioural fingerprint: its delta vector on a fixed probe panel. Consolidation must produce text whose fingerprint equals the sum of the merged items' fingerprints, so it becomes a verifiable compression instead of a rewrite. Duplicates are items with equal fingerprints. · New: consolidation today has no invariant (2605.12978). · Test: consolidate 20 lessons with and without a fingerprint-matching loop; measure the regression rate of 2605.12978 type. · Tie: keeping raw episodes (their own control).
4. **Evidence-weighted gain (memory as Bayes factors).** An item's shift equals its log-likelihood ratio from the evidence that wrote it; it grows with confirmations and shrinks with refutations. This fixes "a lesson seen once acts like one seen 100 times" and the repetition-dose effect the probe shows. · New: text memory is blind to evidence count. · Test: inject explicit shifts sized by counts on the G1 router vs text lessons that state counts. · Tie: Thompson sampling on top of the LM.
5. **Scope-centred memory (anti-spill).** Subtract each item's average effect on out-of-scope probes from its effect, so it acts only where it applies (per-item contextual calibration). · New: calibration is per-prompt today, not per-item in a store. · Test: the probe with unrelated queries; spillover before and after. · Tie: hard retrieval gating.
6. **Commutative memory (sufficient-statistic store).** The writer may only append atomic, typed observations. Lessons are re-derived on read by a deterministic function of the multiset, so the result is order-invariant by construction and consolidation cannot drift. · New: removes the order effect of 2608.18066 at the source. · Test: shuffled-order variance on a small ALFWorld-like stream, multiset vs ACE-style rewriting. · Tie: episodic-only memory.
7. **Falsifiable memory.** Every item carries a cheap test prediction ("calling X with Y returns a field Z"). Before an item acts, its prediction is checked with one probe action; a failed check zeroes its gain and flags rewrite. Fixes Experience Rot by construction. · New: selective maintenance (2611.22525) replays checks after failures; this makes the check part of the item's semantics at every read. · Test: the silent-tool-change setting of 2611.20922 with a 1.5B reader. · Tie: always re-reading the tool schema.
8. **Reader-response surrogate as a memory compiler.** Train a small model to predict the reader's delta for (item text, query). The writer optimizes item text against that differentiable surrogate, so it writes text that has the intended effect. · New: writers today never see the effect of what they write. · Test: compile 20 target behaviours on the G1 router; hit rate vs an LLM writer told the target. · Tie: prompt optimization with real reader calls.
9. **Forward-only memory writes (A/B rollouts, Manoj's ask).** Keep a soft-prompt or KV memory and update it with antithetic evolution strategies from paired A/B rollouts during deployment; no backprop. The memory is a vector, but its update rule is a learning rule, so gains can compound. · New: ES fine-tuning exists (2509.24372); ES as the online write rule for persistent agent memory, with the store as the search space, does not. · Test: 0.5B, 64-dim soft prompt, 200 episodes on the router; vs text lessons at equal rollouts. · Tie: ES on LoRA.
10. **Big model chooses where to write (Manoj's ask).** A large surgeon model sees the small model's attribution on a failure and picks the substrate (context line, KV slot, logit bias, LoRA row, code) and location for the fix. Memory becomes routed by mechanism, not by format. · New: writers choose content, never placement. · Test: on 30 failures, surgeon-chosen placement vs always-context vs always-LoRA, effect per byte. · Tie: try all substrates and keep the best.
11. **Memory interest rate as the objective.** Optimize memory writes for the derivative of future learning speed (how much each write shortens learning of the next task family), not for current success. · New: writes today are scored by the current task. · Test: score lesson sets by time-to-solve on a later family; does the ranking differ from current-task utility? · Tie: current-task utility.
12. **Holographic bound memory.** Bind each item to its key by circular convolution in a residual-stream subspace and superpose all items into one fixed vector; read by unbinding with the query key. Capacity scales with dimension, and superposition is exact up to crosstalk. · New: function vectors superpose tasks, not keyed facts. · Test: arbitrary key→queue at k = 48 on 0.5B, injected at one layer. · Tie: KV retrieval.
13. **Model-swap-invariant memory.** Store memory as target fingerprints (idea 3), not text. On a model upgrade, recompile text or adapters until the new reader reproduces the fingerprints, so memory survives model swaps. · New: portability today is measured, not enforced. · Test: 20 lessons, 0.5B → 1.5B; fingerprint-recompiled vs copied text. · Tie: re-run the writer on the new model.
14. **Memory as a prior on exploration.** Since the reader imitates, store where the agent has not been, or where its predictions failed, so that memory pushes verification and exploration instead of copying. · New: memory is always used for exploitation. · Test: silent-change setting; novelty-memory agent vs experience agent. · Tie: an explicit "verify first" instruction.
15. **Truth-maintenance lessons.** Every derived lesson cites the items it came from; refuting a base item retracts descendants automatically. Degradation by stale abstraction becomes impossible. · New-ish: dependency graphs exist for facts (2611.19859); not for derived procedural lessons. · Test: plant one wrong base lesson; measure the spread of derived errors with and without retraction. · Tie: periodic full rebuild.
16. **Additivity-regularized consolidation into weights.** Distill items into adapters with a loss that forces the adapter of a set to equal the sum of single-item adapters on probe activations. Weight-space memory with superposition as a trained property. · New: Doc-to-LoRA/LatentSkill compose only "when aligned". · Test: 20 items; compare additivity error and accuracy against plain context distillation. · Tie: separate adapters per item plus routing.
17. **Arbitration-circuit gain knob.** Locate the circuit that arbitrates context against prior (2609.25602) and expose its gate as an input, so each memory item can be read with a specified trust level. · New: steering directions for conflicts exist (2610.20067); a per-item, input-level trust channel does not. · Test: patch the gate per item on the probe; does margin at k = 48 recover? · Tie: global steering.
18. **Counterfactual episodes instead of lessons.** Store paired episodes (what happened, what would have happened with the other action), generated by a world model or real rollbacks. The reader learns from contrasts, which imitation can't flatten. · New-ish: COUNTERMEM (2609.31874) is close; check before work. · Test: contrast pairs vs single episodes on the router. · Tie: CAD-style contrast (C1 kill).
19. **Memory that edits the evaluator, not the actor.** Write lessons only into a verifier or critic; the actor improves by search against it. Verifiers compose (AND of checks) while actor nudges do not. · New: memory always targets the actor. · Test: 20 lessons as verifier checks + best-of-8 vs as actor context. · Tie: best-of-8 with lessons in context.
20. **Episodic-control rerank.** Nonparametric Q estimates from stored (state, action, outcome) entries rerank the LM's actions: the gain grows with evidence and is additive across entries. · New: REMEMBERER-type work exists; check. · Test: router with 500 logs. · Tie: success-minus-failure log-likelihood control (G1).

## Deeper sub-questions, ranked by chance of a new primitive

1. **Can a reader be trained to give memory items fixed, additive, calibrated semantics (a memory ISA)?** If yes, memory becomes a programming language for a model, the closest agent-side analog of weight-space programming. Ideas 1, 2, 16, 17.
2. **What exactly erases a correct item's effect as the store grows, and can it be removed?** Attention dilution, position, or a learned deference policy. The probe shows the effect falls 99% (0.5B) and 63% (1.5B) at k = 48 with no conflict; finding the mechanism decides whether ideas 2, 12 and 17 can work. Ideas 2, 5, 12, 17.
3. **Can behavioural fingerprints serve as memory's identity, making consolidation, transfer and pruning verifiable?** Ideas 3, 13, 16.
4. **Can memory updates be made commutative and evidence-weighted without losing abstraction?** This would remove order sensitivity and the repetition-dose effect. Ideas 4, 6, 15.
5. **Can forward-only search write memory directly in activation or weight space, with a large model choosing where?** Manoj's two asks. Ideas 9, 10.

## Reproduce

`python tree/probes/memory_accumulation_probe.py Qwen/Qwen2.5-0.5B-Instruct 4` (CPU, ~3 min; needs torch and transformers). Raw results are in `tree/probes/results_*.json`.
