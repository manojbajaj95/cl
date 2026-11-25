# Nonlinear shrink: truthful examples that contract hidden optimizer state, and honest hops that catch under-reported uncertainty

**Status:** Ideas only; no experiments, implementation, or GPU work. The fixtures below are hand-checked rational sanity checks (verified with Python `fractions`), not evidence.

**Parent:** [Order relays](order-relays.md) ([PR #216](https://github.com/manojbajaj95/cl/pull/216)).

**Review seeds:** [Flood triage, row 329](https://github.com/manojbajaj95/cl/blob/f3fcd2ac2b2178eb0d5d4189793bd2e06b817343/reviews/flood-triage.md#L329) keeps two ideas at score 3: **#216#10**, contractive teaching: find a truthful example that hits a non-affine part of the optimizer (clipping threshold, Adam's square-root normalization, a dead-ReLU gate on a slot-coupled unit) so the set of hidden slot states shrinks just enough to keep two schedules open (controls: #213/#203#06 full synchronizing batches, a direct slot reset, a paid slot probe, an affine optimizer where no such example exists, matched B gain, A/C retention); **#216#21**, detect a dishonest hop: a later honest hop tells from public update magnitudes alone that an earlier hop under-reported its training-state uncertainty or skipped a decay step, before admitting a residual order (controls: authenticated message chains, full rechecking at every hop, a checkpoint relay, an honest chain with large but genuine uncertainty, a misreport just inside the detection margin).

**Read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/f3fcd2ac2b2178eb0d5d4189793bd2e06b817343/reviews/idea-ledger.md). Rules carried here: bounded-delay scheduling died against gradient accumulation at equal latency, so every order or contraction claim needs a smooth, accumulation-matched null ([PR #113](https://github.com/manojbajaj95/cl/pull/113)); ideas whose headline follows from linear algebra are killed; Noether/balancedness memory died because finite-step SGD and momentum erase conserved quantities, so any "hidden state" claim must survive realistic step sizes; merge and stacked ideas must beat the union of their parts' baselines at equal bytes, checks and compute; every first test checks ordinary held-out old-task retention.

## What a shrink would buy, and what already exists

PR #216's Fixture R2 showed that when a hidden optimizer slot updates as `v' = v − g` with `g` independent of `v`, every truthful example only translates the hidden set; relay width is then fixed by `δ/(1 − β)` against slack. This node takes the two survivors seriously and narrows them:

- **Seed A (shrink).** A truthful example can contract the hidden set only if the update it causes *depends on the hidden state*. That happens in two ways: (i) affinely, when the example's loss has curvature along the hidden direction (Fixture N0 below), and (ii) through an optimizer or network nonlinearity (clipping, `m/√v`, a ReLU gate). The affine route already exists and is ordinary optimization forgetting its initial condition. So the only defensible content is what nonlinear contraction does that affine contraction cannot: **move only the out-of-range histories and leave the rest exactly unchanged** (a certifiable no-op on the bulk), or **contract optimizer slots that no loss curvature reaches in one step** (Adam's second moment).
- **Seed B (detect).** With exact public updates, SGD-momentum reveals its slot outright (`m = −Δw/η`), so nothing is hidden and detection is trivial. The question is interesting only when publication is coarse (update norms, quantized sizes, block norms) or when Adam reveals only ratios. Fixture N5 shows that a norm-only publication is a *linear* measurement of `z = 1/v` and admits harmful misreports that no public check can catch.

Prior art to concede up front (checked on alphaXiv where noted):
- **Training verification:** Proof-of-Learning ([2103.05633](https://arxiv.org/abs/2103.05633)) and its spoofing attacks ([2208.03567](https://arxiv.org/abs/2208.03567)) verify training by replaying segments; [Training Witnesses (2609.33915)](https://arxiv.org/abs/2609.33915) uses behavioral fingerprints with occasional replay challenges (read: it certifies data inclusion and training progress, not optimizer-slot uncertainty or decay); [SciCheck (2611.09889)](https://arxiv.org/abs/2611.09889) audits training integrity (abstract only). None of them asks whether a *coarse public update statistic* suffices to catch an under-reported uncertainty set.
- **Optimizer state carries history:** [Delayed optimizer-state transport (2608.24593)](https://arxiv.org/abs/2608.24593) shows AdamW moments make near-future data order actionable; [AdamW minibatch IO dynamics (2608.19762)](https://arxiv.org/abs/2608.19762) and [optimizer leakage (2610.18294)](https://arxiv.org/abs/2610.18294) study the same channel (abstracts only). None uses a chosen truthful example to contract it.
- **Set propagation through saturation:** set-based observers ([2602.03646](https://arxiv.org/abs/2602.03646)), reachable sets of saturated systems ([2504.03443](https://arxiv.org/abs/2504.03443)), interval bound propagation ([1810.12715](https://arxiv.org/abs/1810.12715)) bound images of sets through clip/ReLU; synchronizing words and #203#06/#213 synchronizing batches merge aliased states completely; dormant-neuron reset ReDo ([2302.12902](https://arxiv.org/abs/2302.12902)) and Adafactor update clipping ([1804.04235](https://arxiv.org/abs/1804.04235)) are the standard uses of the nonlinearities.

## Paper fixtures (sanity checks, not evidence)

Throughout, a residual schedule shifts the slot by `−1` or `+1` and is safe if the result stays in `[−2, 2]`; two schedules stay open for every hidden history iff the hidden set (after a translation) fits in `[−1, 1]`, i.e. width `≤ 2`.

**N0: Affine contraction exists whenever the example reads the hidden coordinate (mandatory control).** Linear regression, `w ∈ ℝ²`, hidden coordinate `w_1 ∈ {0, 3}` (width 3, one schedule). The truthful example `x = (1, 0)`, label `t`, step `η = 1/3` gives `w_1' = (2/3)w_1 + t/3 ∈ {t/3, 2 + t/3}`: width 2, two schedules open, public coordinate `w_2` untouched. PR #216's "truthful examples only translate" is therefore specific to slots whose gradient does not read the hidden state. Any nonlinear-shrink claim must beat this example class.

**N1: Just-enough clipping versus synchronizing and reset.** Hidden slot `v ∈ {0, 3}`, truthful pool `g ∈ {0, …, 4}`, clipped slot update `v' = clip(v − g, −1, 1)`; "discarded" is the slot mass removed by clipping, `Σ_h |(v_h − g) − v_h'|`.

| `g` | image | two open? | discarded |
|---|---|---|---|
| 0 | `{0, 1}` | yes | 2 |
| 1 | `{−1, 1}` | yes | 1 |
| 2 | `{−1, 1}` | yes | 1 |
| 3 | `{−1, 0}` | yes | 2 |
| 4 | `{−1}` (synchronized) | yes | 3 |

The affine pool `v − g` never fits (width stays 3). A direct reset to `v = 0` discards 3, the same as full synchronization. The just-enough items `g ∈ {1, 2}` keep the two histories distinct and discard 1: a third of the synchronizing cost. Whether "discarded slot mass" is B progress lost is an empirical question (card 06).

**N2: Saturation is a no-op on the bulk; affine contraction moves everyone.** Hidden set `{0, 1, 4}` (one outlier history), target width 2. One-sided saturation `min(v, 2)` gives `{0, 1, 2}`: total movement 2, and the two bulk histories move **0**. Uniform affine contraction by `1/2` about the median, `1 + (v − 1)/2`, gives `{1/2, 1, 5/2}`: the same total movement 2 but every off-median history moves, and its maximum single movement is `3/2` versus saturation's 2. So saturation wins only on *exact preservation of in-range histories* (a free retention certificate for them), not on total or worst-case disturbance. With a spread-out hidden set (no outliers) affine contraction is as good or better.

**N3: Adam normalization: a high-loss truthful example contracts update-multiplier uncertainty, and doing nothing expands it.** RMSprop (`β_1 = 0`), `β_2 = 1/2`, hidden second moment `v ∈ {1, 11}`; the next update multiplier is `1/√v`, so `1/v ∈ {1, 1/11}`.
- A step with zero gradient: `v' ∈ {1/2, 11/2}`, `1/v' ∈ {2, 2/11}`, multipliers `≈ {1.414, 0.426}`, width ≈ 0.99 (up from ≈ 0.70).
- A truthful example with `g² = 7`: `v' ∈ {4, 9}`, multipliers exactly `{1/2, 1/3}`, width `1/6`.
The second moment's *difference* is only halved (affine decay), but the normalization turns the added `g²` into a contraction of the quantity schedules actually feel. At `β_2 = 0.999` the per-example effect scales with `(1 − β_2) g² / v`, so a real test needs either many such items or an outlier gradient (card 09).

**N4: A dead-ReLU gate makes the update history-dependent.** Unit `h = relu(b + x)`, loss `h²/2`, `η = 1`, truthful input `x = 0`, hidden bias `b ∈ {−1, 1}`. History `b = −1` is dead (no gradient, stays `−1`); history `b = 1` moves to `0`. Width `2 → 1`. The cost is visible: both histories now have the unit dead at `x ≤ 0`, the dormant-unit failure ReDo exists to undo.

**N5: Detection from public update sizes, and where it fails.** RMSprop, `β_2 = 1/2`, `η = 1`, public gradients; a skipped decay step updates `v' = v + (1 − β_2) g²` instead of `β_2 v + (1 − β_2) g²`. Public statistic: squared update size `s = Σ_i g_i² / v_i'` (linear in `z = 1/v'`).
- **N5a (scalar, exact sizes): every skip is caught.** Claimed history set `v ∈ {1, 9}`, `g² = 7`. Honest `s ∈ {7/4, 7/8}`; skipped `s ∈ {14/9, 14/25}`. Disjoint, so one public step detects any skip.
- **N5b (scalar): an undetectable skip is harmless.** Claimed set `{1, 2}`: a skip from `v = 1` gives `v' = 9/2`, exactly the honest image of `v = 2` (`s = 14/9`). The true state stays inside the claimed set, so admitted schedules stay safe.
- **N5c (two coordinates, norm-only publication): a harmful skip passes every public check.** `g² = (1, 1)`, claimed histories `{(5, 9), (9, 5)}`, honest images `v' ∈ {(3, 5), (5, 3)}`, `z ∈ {(1/3, 1/5), (1/5, 1/3)}`, `s = 8/15` for both. The dishonest hop's real prefix left `v = (2, 7)` and it skipped decay: `v' = (5/2, 15/2)`, `z = (2/5, 2/15)`, `s = 8/15` again. The public size matches, but coordinate 1's multiplier (`z_1 = 2/5 > 1/3`) lies outside the claimed hull, so a schedule certified on the claim can be unsafe. Norm publication is a hyperplane measurement in `z`; harm lives on that hyperplane outside the claim's hull.

## Idea cards

**P** = candidate primitive, conditional on beating the strongest stacked control; **I** = improvement, audit or falsification control. All first tests are proposed CPU-scale checks: rational fixtures, then a 2-layer ReLU MLP with Adam (and clipped SGD-momentum) on a split stream with old tasks A/C and new task B, inside a PR #216 relay.

### Nonlinear shrink (Seed A: #216#10)

#### 01. Just-enough contractive example (P; restates #216#10)
- **Mechanism:** At a seam where the relay width has collapsed to one schedule, search the truthful pool for the example whose optimizer response, through a clip, normalization or gate, maps the hidden set into the two-schedule region while discarding the least slot mass and keeping histories distinct (N1: `g = 1` or `2`, not `g = 4`).
- **Novelty vs nearest prior art:** Synchronizing words and #213 batches merge states completely; set-propagation work bounds images but does not choose a training input to shape them. The bet is a *partial* contraction bought with one honest update.
- **Cheapest first test:** N1, then the ReLU/Adam host with clipped SGD-momentum: enumerate 200 truthful B examples at a collapsed seam, propagate the hidden set with interval bounds, and pick the minimal-discard opener. Controls: N0-style affine example, #213 full synchronization, slot reset, paid slot probe, an unclipped optimizer (where the search must return nothing).
- **Old-task retention check:** A/C on the step after the opener and after the suffix; clipping discards update mass, so B gain is matched across arms.

#### 02. Bulk-preserving saturation certificate (P)
- **Mechanism:** Choose the example so that only out-of-range histories touch the saturation threshold; every in-range history's state is exactly unchanged, so its existing retention certificate carries over without re-checking (N2).
- **Novelty vs nearest prior art:** Gradient clipping is used for stability under heavy tails (2610.28107); using its exact identity region as a certificate-preserving region is new. Wins only when the hidden set has outliers.
- **Cheapest first test:** Hidden sets drawn with a heavy-tailed history mixture versus a uniform one; compare re-check cost and A/C breaches for saturation against affine contraction at equal width.
- **Old-task retention check:** Certified A/C on bulk histories must hold with zero re-checks; audit by full evaluation.

#### 03. Second-moment squeeze (P)
- **Mechanism:** A high-loss truthful example adds a large `g²` to every history's second moment, pushing all of them onto the flat part of `1/√v` so update-multiplier uncertainty contracts (N3), while a quiet step expands it.
- **Novelty vs nearest prior art:** Adam's stability analyses (2609.18314, 2608.20638) treat `v` dynamics but not as a set to shrink; 2608.24593 measures moment transport, not its contraction.
- **Cheapest first test:** N3, then the Adam host at `β_2 ∈ {0.9, 0.99, 0.999}`: measure multiplier-interval width over 24 prefix orders after the opener versus a zero-gradient step and a matched-norm random example.
- **Old-task retention check:** High-loss examples are large updates: A/C immediately after, with clip-matched controls.

#### 04. Dead-gate switch (P)
- **Mechanism:** Pick an input that leaves the unit dead under some histories and alive under others, so only the alive histories move toward the dead ones (N4).
- **Novelty vs nearest prior art:** ReDo treats dead units as damage; here a transient gate is a history-dependent switch. Must not leave units permanently dead.
- **Cheapest first test:** N4, then count slot-coupled units on the host whose gate splits hidden histories; compare contraction per unit of capacity lost against ReDo-reset-after controls.
- **Old-task retention check:** Dormant-unit ratio and A/C before and after; a permanently dead unit used by A must be flagged.

#### 05. Affine curvature null (I; mandatory)
- **Mechanism:** For every nonlinear opener, find the best truthful example whose loss has curvature along the hidden direction (N0) at the same B gain and width.
- **Novelty vs nearest prior art:** Ordinary optimization forgetting initial conditions; it kills Seed A wherever it ties.
- **Cheapest first test:** Pair each card 01–04 opener with its affine rival on the host; report width, discarded mass, B gain and A/C.
- **Old-task retention check:** Matched A/C floors on both arms.

#### 06. Price of discarded slot mass (I)
- **Mechanism:** Measure whether slot mass removed by clipping (N1's "discarded") is B progress lost, momentum that would have been wasted, or neutral.
- **Novelty vs nearest prior art:** An audit of card 01's cost metric.
- **Cheapest first test:** Regress B loss after 50 steps on discarded mass across openers and seeds.
- **Old-task retention check:** A/C as covariates in the same regression.

#### 07. Clip threshold as an illegal knob (I; control)
- **Mechanism:** Changing the clip threshold or resetting Adam is a hyperparameter intervention, not truthful teaching; run it as the control that bounds what truthful openers can reach.
- **Novelty vs nearest prior art:** None; it is the ceiling arm.
- **Cheapest first test:** Sweep threshold at the seam and compare contraction against the best truthful opener.
- **Old-task retention check:** Threshold changes affect every later step: A/C over the full suffix.

#### 08. Distinct-image constraint: shrink without erasing the exporter's information (P)
- **Mechanism:** Require the opener to keep hidden histories injective (N1 `g ∈ {1, 2}`, not `g = 4`), so the exporter or a later paid probe can still recover which history ran, keeping card 18's detection possible.
- **Novelty vs nearest prior art:** Opposite of synchronization; closest to injective quantization.
- **Cheapest first test:** Count injective versus merging openers on the host and measure later probe accuracy.
- **Old-task retention check:** A/C under both opener types.

#### 09. Coupled `m/√v` shrink: make momentum uncertainty irrelevant (P)
- **Mechanism:** Inflate `v` on exactly the coordinates where `m` is uncertain so `m/√v` uncertainty contracts even though `m`'s set is unchanged.
- **Novelty vs nearest prior art:** #212 signed slot permutations move slots exactly; this shrinks their effect without moving them.
- **Cheapest first test:** Two-coordinate Adam toy with uncertain `m_1`; choose examples with a large `g_1`; compare against a momentum reset.
- **Old-task retention check:** Large `v_1` slows later learning on coordinate 1: check A/C and B plasticity 20 steps later.

#### 10. Nonlinear pre-paid teaching past Helly (P)
- **Mechanism:** In PR #216 Fixture R1, the fourth importer (`d = 1`) breaks pre-paid teaching because feasible intervals are disjoint. A clipped opener changes the interval geometry, possibly making one item feasible for all four, which no translation can.
- **Novelty vs nearest prior art:** Joins #216#01/#02 with this seed; the comparison is #216#03's one-bit export, which already serves all four.
- **Cheapest first test:** Recompute R1 with `v' = clip(v − g, −c, c)` for `c ∈ {1, 3/2, 2}`; then 8 importers on the host. Kill if one exported bit always matches.
- **Old-task retention check:** A/C on every importer's residual order.

#### 11. Public interval certificate for the shrink (I)
- **Mechanism:** Ship an IBP/CROWN-style bound of the opener's image so importers verify contraction without the exporter's state.
- **Novelty vs nearest prior art:** IBP is standard; this is packaging.
- **Cheapest first test:** Bound tightness versus exact images over 24 prefix orders.
- **Old-task retention check:** None new; reuse card 01's.

#### 12. Shrink every `m` hops versus re-anchoring probes (I)
- **Mechanism:** Replace #216#11's paid probe with a contractive opener every `m` hops and compare at equal cost.
- **Novelty vs nearest prior art:** Periodic resynchronization.
- **Cheapest first test:** 12-hop relay at `β = 7/8`; sweep `m`.
- **Old-task retention check:** A/C at every opener hop.

#### 13. Smooth-clip and accumulation null (I; mandatory)
- **Mechanism:** Replace hard clip and ReLU with softclip/Huber and GELU, and compare every arm against clock-matched gradient accumulation.
- **Novelty vs nearest prior art:** The ledger's bounded-delay kill and PR #113's smooth null.
- **Cheapest first test:** Rerun cards 01–04 with smooth nonlinearities; kill hard-threshold claims that vanish.
- **Old-task retention check:** Matched A/C across all arms.

### Honest-hop detection (Seed B: #216#21)

#### 14. Public-consistency soundness check (P; restates #216#21)
- **Mechanism:** Each hop publishes its claimed hidden set and its update sizes; the next hop propagates the claim through the declared optimizer (decay included) and rejects if any public size falls outside the claim's image (N5a).
- **Novelty vs nearest prior art:** Proof-of-Learning replays segments; Training Witnesses uses fingerprints and replay challenges; neither checks an uncertainty claim against coarse update statistics without replay.
- **Cheapest first test:** N5a, then a 5-hop relay on the host where one hop halves its width claim or skips one decay; measure detection and false-alarm rates against trusting every hop, full rechecking and a checkpoint relay.
- **Old-task retention check:** A/C along the path the dishonest hop tried to admit, which must be refused.

#### 15. Harmless-aliasing rule: only harmful misreports need catching (I)
- **Mechanism:** A skip whose true state stays inside the claim is undetectable and harmless (N5b); define detection success only over misreports that escape the claim.
- **Novelty vs nearest prior art:** It sharpens the target metric and prevents counting harmless skips as misses.
- **Cheapest first test:** Classify injected misreports on the host by escape and detection.
- **Old-task retention check:** Undetected-harmless paths must keep A/C; verify.

#### 16. Minimal publication for complete detection (P)
- **Mechanism:** Norm-only publication is a hyperplane in `z = 1/v` and misses harmful skips (N5c); find the smallest set of block norms or random projections of the update so every claim-escaping state changes some published statistic.
- **Novelty vs nearest prior art:** Compressed sensing and sketching give measurement counts; making the sketch cover "outside the claimed hull" rather than recover the state is the new object.
- **Cheapest first test:** N5c with one extra block norm; then sweep the number of random projections on the host until harmful misses reach zero, reporting bytes.
- **Old-task retention check:** A/C along every harmful path that a smaller sketch would have admitted.

#### 17. Active detection: the honest hop chooses its first example to separate honest from skipped images (P)
- **Mechanism:** Before admitting, the honest hop picks a truthful example whose response maximizes the gap between the claim's image and the skip images (N5a separates, N5b's `{1, 2}` claim is the hard case).
- **Novelty vs nearest prior art:** Active fault diagnosis and test-input design; here inputs are truthful training examples.
- **Cheapest first test:** On the host, search 200 truthful items for the maximal separation and compare against a random item and a paid probe.
- **Old-task retention check:** The probing example is a real update: A/C after it.

#### 18. Shrink-detect conflict: contract only after checking (P)
- **Mechanism:** Contraction destroys evidence (N1 `g = 4` maps both histories to `−1`, so no later check can tell them apart); certify an order in which detection runs before contraction, or an opener that contracts while keeping misreports visible (card 08).
- **Novelty vs nearest prior art:** Joins both seeds; the stacked control is "detect with card 14, then synchronize with #213".
- **Cheapest first test:** 4-hop relay with a dishonest hop before a contractive seam; compare detection rates under shrink-then-check and check-then-shrink.
- **Old-task retention check:** A/C on any path admitted after contraction.

#### 19. Weight-decay skip fingerprint (I)
- **Mechanism:** Decoupled weight decay scales weights by `1 − ηλ` independently of gradients; a skipped decay shows as a weight-norm excess `ηλ‖w‖` visible at the hop boundary.
- **Novelty vs nearest prior art:** Straightforward bookkeeping; an audit that may already catch the "skipped decay" case without slot inference.
- **Cheapest first test:** Inject skipped decays on the host; detection rate from boundary weight norms alone.
- **Old-task retention check:** Skipped decay changes A margins; report them.

#### 20. Genuine-uncertainty and margin-edge false alarms (I; mandatory)
- **Mechanism:** Run honest chains with wide genuine uncertainty and floating-point reduction noise, plus misreports just inside the tolerance.
- **Novelty vs nearest prior art:** The reviewer's required negatives.
- **Cheapest first test:** Sweep tolerance; report ROC.
- **Old-task retention check:** A/C on falsely refused honest paths (cost of false alarms).

#### 21. Equal-byte audit against authenticated chains and replay (I; mandatory)
- **Mechanism:** Compare bytes and verifier compute of cards 14/16 against signed checkpoints, Training Witnesses-style replay challenges and full rechecking.
- **Novelty vs nearest prior art:** The economic falsifier; a full checkpoint removes every hidden state.
- **Cheapest first test:** Sweep model size and hop count; report crossover byte ratio.
- **Old-task retention check:** Breaches by cause on every arm.

#### 22. End-to-end retention under shrink and detection (I; required)
- **Mechanism:** Run a 5-task split stream with one hop per task, using contractive openers and public checks, versus plain sequential Adam, replay and EWC.
- **Novelty vs nearest prior art:** Ordinary CL measurement tying the node back to retention.
- **Cheapest first test:** Small MLP, 3 seeds.
- **Old-task retention check:** Task-1 accuracy after every hop and worst protected slice.

## Ranked deeper questions

1. **Does any nonlinear opener beat the affine curvature null (card 05) at matched B gain and A/C retention?** N2 says saturation can win only by leaving in-range histories exactly unchanged, and only when the hidden set has outliers. If real prefix-order spreads on an Adam host are not outlier-dominated, Seed A reduces to ordinary optimization and should be dropped.
2. **What is the smallest publication that catches every harmful misreport?** N5c shows norm-only publication fails in two coordinates. The primitive is card 16's sketch covering "outside the claim" with fewer bytes than a checkpoint or a replay challenge; without it, Seed B is authenticated checkpoints.
3. **Can Adam's second-moment squeeze (cards 03 and 09) act at `β_2 = 0.999` without an old-task cost?** The per-example effect scales with `(1 − β_2) g² / v`, so it needs outlier gradients, which are exactly the updates that hurt A.
4. **Does contraction always erase detection evidence (card 18)?** If every contraction that keeps two schedules also makes some harmful misreport undetectable, the two seeds conflict and the relay must order check-then-shrink; finding an opener that does both would be the joint primitive.
