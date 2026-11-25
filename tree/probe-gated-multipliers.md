# Probe-gated step multipliers and momentum-safe retirement

**Status:** Ideas only; no learner runs, pilots, or GPU work. **Parent:** [Private step multipliers](private-step-multipliers.md) ([PR #277](https://github.com/manojbajaj95/cl/pull/277)). **Review seeds:** the two score-3 ideas in [the #277 flood-triage row](https://github.com/manojbajaj95/cl/blob/5f855dd90e44e8868569acb34265713a5fec7a4a/reviews/flood-triage.md#L395): #04 uses one probe in the direction where a scale shift and coordinate interference disagree most; #06 compares two terminal momentum weightings before retiring gains.

**Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/5f855dd90e44e8868569acb34265713a5fec7a4a/reviews/idea-ledger.md). No gauge or effective-rate claim by itself; no forgetting guarantee from a first-order score; no win from exactness relative to a conveniently redefined reference. A joint proposal must beat the best gate plus the best retirement rule stacked at equal cost. **P** marks a candidate reusable operation; **I** marks an improvement or a falsifier, not a reviewer verdict.

## What would be new?

- [Atkinson and Fedorov's model-discrimination design](https://doi.org/10.1093/biomet/62.1.57) already asks where rival models disagree. [AdaHessian](https://arxiv.org/abs/2006.00719) already buys directional curvature information; [Adam-mini](https://arxiv.org/abs/2406.16793), [AdamPM](https://arxiv.org/abs/2610.24598), [Adafactor](https://arxiv.org/abs/1804.04235), and [LAMB](https://arxiv.org/abs/1904.00962) already pool, factor or rescale updates. The candidate is a one-measurement **decision about whether to open a temporary optimizer degree of freedom**, including refusal when opposite decisions still fit the measurement. Neither a nicer probe nor a faster scalar rate alone would establish it.
- Warmdown reduces step amplitude; bumpless transfer matches outputs at a switch; [Guarded Compression of Adam Optimizer State](https://arxiv.org/abs/2611.00589) guards the first restored update under shared gradients. The target here is **retirement of relative gains** with explicit accounting for the lost momentum mode, including later masks, feedback, and old-task margins. Matching the visible first update, or exactly folding into a weighted continuation while calling it uniform retirement, does not meet that target.

## Contract and two paper fixtures

Freeze the legal probe menu, one scalar observation per window, serving precision and response error bounds, byte and gradient budgets, allowed update words U, horizon H, and A/C retention and B/P utility floors before the window. A probe has no persistent weight or slot effects; any work or state needed to construct the direction counts. A direction can be a legal directional derivative or a readout response of a scratch trial on a legal batch; it is not a free query to private Adam. Declare a forward map from each explanation to that observation, based on information the memory-saving arm actually keeps. If no available measurement depends on the disputed feature, refuse. Private moments, exhaustive probes and an oracle history may label offline controls, not issue a live gain.

Let the compatible worlds after observing y be those whose predicted response intervals contain y. A nonunit gain is eligible only if the compatible set is nonempty and one predeclared action meets the gain and exit constraints in **every** compatible world. Being unable to resolve two labels is harmless if they justify the same action; an alias with conflicting safe actions is not. Charge setup, probing, refused windows, extra serving width and all retained evidence. Compare at matched bytes, work and deadlines: always-on multipliers, random/past-RMS probes, Adam-mini/AdamPM with tuned block gains or LAMB, private v as a costed comparator, abrupt uniform gains, warmdown, moment reset, frozen ratios, and #264#06's cooling tail. On the same accepted windows report (i) actual tied-wide to narrow fold error, (ii) retired to uninterrupted frozen-gain trajectory error from the same checkpoint, including transition offset, and (iii) actual held-out A and C margins and B/P progress. A hard case must still run old service if gain or retirement is refused.

**F1 — Separation depends on the available observation, not just the hypotheses.** In a paper response model, suppose two worlds share the same stored pooled summaries and have directional response vectors S = (2, 2), X = (2, 1/2). The responses here are specified by the fixture, not read from a private v; the testable assumption is that an admissible query reports q·S or q·X with at most 1/8 error. With q in {e₁, e₂}, e₂ maximizes separation (3/2 vs 0). Its intervals are [15/8, 17/8] and [3/8, 5/8], so it separates; e₁ aliases. An equal-cost uniform random choice separates on only half its choices. Add X′ = (2, 2, 1/2) against S′ = (2, 2, 2) but restrict the probe menu to {e₁, e₂}: every observed interval aliases. If the third coordinate matters later, even a clean response cannot grant the scalar. This is a check on the decision geometry, not evidence that real gradients expose the two worlds.

**F2 — Matching total gain does not match inherited momentum.** Take two frozen twins with common g = 1, m₁ = 1, m₂ = −1, β₁ = 1/2, shared v = 1, ε = 0, uncorrected moments and base rate η = 1. The denominator stays 1 for any β₂ in [0, 1). Frozen gains (2, 1) and uniform gains (3/2, 3/2) both sum to 3, so the fresh-gradient coefficients match. After t ≥ 1 steps the weighted moment sums are 3 − 2·2⁻ᵗ and 3 − 3·2⁻ᵗ. Uniform minus frozen in signed parameter displacement is +1/2 on step 1, +1/4 on step 2, and +3/4 cumulatively. If both references apply a common rate taper λₜ, each per-step gap becomes λₜ·2⁻ᵗ; the gap to an *untapered* frozen reference must separately include the rate change. A weighted-moment transport can preserve the frozen reference under the parent's twin assumptions, but it is not the uniform-weighted terminal state. This fixture uses a prescribed trace; it gives no closed-loop or retention guarantee.

## Idea cards

### A. Make the one probe decide something (#277#04)

#### 01. One direction to admit the gain (P; review seed)
- **Mechanism:** Pick the legal direction with the largest disagreement between registered scale and shape explanations, normalized for the probe's error bound. Issue a bounded scalar only on an unambiguous scale response and otherwise keep pooled Adam at unit gain.
- **Novelty vs nearest prior art:** Atkinson–Fedorov already picks discriminating queries; this uses the result to grant a temporary gain under a shared-v memory contract, not to select a better fitting model.
- **Cheapest first test:** Enumerate the two F1 directions, then replace the response oracle with one actual directional read on two tiny quadratic streams. Compare equal-cost random direction, past RMS, always-on gains, Adam-mini/AdamPM and private v; include an aliased pair.
- **Old-task retention check:** Hold out A on the common direction and C on the disputed one; score both after scale approvals, shape refusals and an intentionally forced false approval.

#### 02. Choose by conflicting actions, not class labels (P)
- **Mechanism:** Search for the probe whose worst response bin leaves the widest common safe-gain interval with a feasible exit. Shape and scale worlds may share a bin if the same gain works on their declared continuation.
- **Novelty vs nearest prior art:** Decision-theoretic experiment design already values an action over a label; the proposed artifact is a gain-and-exit interval shared by unresolved optimizer histories.
- **Cheapest first test:** Build four finite quadratic cases where the probe that perfectly identifies a nuisance axis leaves no common useful action. Compare class separation, best fixed gain and full information.
- **Old-task retention check:** Put A and C on different active constraints; score the worst member of each accepted bin plus the fallback, not just the most likely world.

#### 03. Probe a residual after removing unknown scale (P)
- **Mechanism:** Use a public pooled-update template u. Select a legal q with q·u = 0 so that any scalar fit of u predicts zero, then maximize the smallest observable response from harmful residuals. Null feasibility is a prerequisite, not evidence from a pass.
- **Novelty vs nearest prior art:** Invariant contrasts and [OGD](https://arxiv.org/abs/1910.07104) use orthogonality; here the null is in the measurement, not a projection of the training update.
- **Cheapest first test:** Sweep three 2-D templates with an unknown scale and a signed transverse mismatch. Compare a scale-fitted axis, random q and a norm ratio; include a harmful residual annihilated by every legal q.
- **Old-task retention check:** A reads the scale-aligned feature; C reads the transverse feature. Ensure every unresolved harmful case refuses or takes a common safe action, and test both after B learning.

#### 04. Choose for surviving integer bins (P)
- **Mechanism:** Optimize for separation *after* the actual rounding and clipping of the probe report. If a bin mixes worlds requiring different gains, publish a narrower common gain or none, even when the exact response would identify the world.
- **Novelty vs nearest prior art:** Quantized sensing already optimizes binned discrimination; the bins here control a timed optimizer-state allocation and cannot subsidize it with unbilled precision.
- **Cheapest first test:** Enumerate two fixed-point formats and legal direction amplitudes, with one clipped high-disagreement direction. Compare float-first selection then quantization, a wider paid report and a random fixed-point probe.
- **Old-task retention check:** Make rounding cross a safety boundary for A but not C in one world, reverse this in another, and score the executed fallback on both.

#### 05. Ask one directional read on the unapplied write (P)
- **Mechanism:** Compute the pooled-step proposal from the due batch, but take the one extra directional derivative along a preselected contrast at the scratch candidate, where the two explanations predict different residuals. The real write starts at the untouched state.
- **Novelty vs nearest prior art:** AdaHessian and line search obtain local directional information; this read chooses whether *any* scalar write in a bounded family is credible rather than optimizing the line length. The residual model must be independently checked.
- **Cheapest first test:** Use two quadratics with identical initial gradients and differing cross-curvature. Compare one directional read before vs after the scratch displacement, an equal-cost one-step line search, and a pair identical at both legal read points.
- **Old-task retention check:** Hide A in a high-curvature direction and C at a tight margin; evaluate after the real write and confirm the scratch probe did not advance either weights or clocks.

#### 06. Buy an observable using useful work (P)
- **Mechanism:** When an immediate probe aliases, choose among already-due, independently useful B/P records to reach a point where one later probe separates. Select the record before observing the probe; decline if the move itself requires the gain being diagnosed.
- **Novelty vs nearest prior art:** Active identification with control already excites a system; the constraint here is that the excitation earn its keep as normal learning and must be safe under every pre-probe alias.
- **Cheapest first test:** Two masked CPU quadratics, with either of two due records unlocking a different coordinate. Compare the best passive one-probe gate, a dedicated excitation step and a useful record that opens no distinguishing coordinate.
- **Old-task retention check:** Serve A and C between the ordinary record and the probe, as well as after gain admission; a temporary violation cannot be repaid at commit.

#### 07. One contrast for an allocation, not one gain per shard (P)
- **Mechanism:** If the byte cap funds only one compensated shard, use a cross-shard read that rejects incompatible *allocations*. Grant at most one action common to all worlds in the response bin, including choosing neither.
- **Novelty vs nearest prior art:** AdamPM pools state and #277#03 redistributes gains on a fixed simplex; the candidate is a single observation deciding who may use a scarce gain without certifying every shard's full shape.
- **Cheapest first test:** Enumerate four two-shard scale/shape worlds with identical per-shard norms. Compare a contrast, a single local probe, a paid two-probe oracle, and a world where swapping shards aliases two opposite allocations.
- **Old-task retention check:** Associate A and C with different shards and score false allocation and no-allocation paths separately at matched B/P progress.

#### 08. Demand a refusal witness for an unreachable separator (I)
- **Mechanism:** Produce two admissible histories with disjoint safe-gain sets and equal responses for every legal query. Use this as a falsifier for tightening the same probe rule; widen the menu or keep the pooled fallback.
- **Novelty vs nearest prior art:** Standard observability impossibility, applied to the admissible one-probe interface rather than claiming an impossibility for Adam or all measurements.
- **Cheapest first test:** Enumerate a 3-D F1 extension with the third coordinate unprobeable but trainable later; then make that coordinate publicly probeable and check that the witness disappears.
- **Old-task retention check:** Track A on the visible coordinates and C on the hidden one; show forced admission fails on at least one compatible history and check both on the real fallback.

### B. Retire the relative gain, not just its visible step (#277#06)

#### 09. Two terminal weightings, one exit decision (P; review seed)
- **Mechanism:** Before deleting relative gains, compare the frozen-gain weighting and uniform weighting of the live m over the registered suffix. Permit retirement after a common taper only if the transition and post-exit gaps fit the allowance; otherwise keep frozen ratios or refuse the refund.
- **Novelty vs nearest prior art:** Warmdown changes overall rate; #264#06 cools v. Neither by itself bounds the m mode lost when the relative gains become uniform.
- **Cheapest first test:** Extend F2 with a zero-gradient and a nonzero-gradient branch; compare abrupt uniform gains, LR warmdown, reset, frozen ratios and #264#06 at equal time and storage. Include a discarded mode a short taper cannot cover.
- **Old-task retention check:** Put A and C on opposite sides of narrow decision margins and check both throughout taper, at fold, and after both branches run.

#### 10. Test the first mask that can see the dropped mode (P)
- **Mechanism:** Hold the exit while a registered delayed mask can expose a difference invisible to current reads. Release it only if that first exposure, and the remaining suffix, are bounded for all legal words.
- **Novelty vs nearest prior art:** One-step guarded compression protects the current gradient domain; this certifies an exit against delayed visibility, not only small instantaneous output error.
- **Cheapest first test:** Project the first F2-like mismatch onto a dormant coordinate, then let one of two allowed masks activate it at step 2. Compare first-step matching, a fixed wait and full finite branch enumeration.
- **Old-task retention check:** A observes the current mask and C the delayed coordinate; measure both across the switch and verify refusal preserves service if the mask arrives early.

#### 11. Separate the stale mode from the fresh-gradient coefficient (P)
- **Mechanism:** Fix gain sum across a retirement so common fresh gradients have the same coefficient. Bound or extinguish only the stale signed contrast; if a legal gradient is unequal across shards, charge its new forcing term rather than claiming decay.
- **Novelty vs nearest prior art:** LAMB and warmdown scale the whole step, and weighted transport preserves frozen ratios. The candidate is a retirement bound that distinguishes lost memory from accidentally changing gain on fresh gradients.
- **Cheapest first test:** Enumerate a two-twin F2 extension with a common trace and a shard-specific impulse at step 2. Compare a matched-sum taper, a matched-step-norm taper and a full difference oracle.
- **Old-task retention check:** Give A a margin on accumulated displacement and C a margin on the impulse direction; both must hold when the forced term is included.

#### 12. A useful installment to pay down the contrast (P)
- **Mechanism:** Before uniform retirement, choose a due record whose native shard gradients reduce the signed contrast while advancing B/P. No direct write to m; accept only if the updated state passes the same exit test as the passive tail.
- **Novelty vs nearest prior art:** [GradMatch](https://arxiv.org/abs/2103.00123) selects subsets to match a target gradient; #277's cooling uses a lawful tail. Here a particular future-state mode, not total gradient match, can decide which due record to spend.
- **Cheapest first test:** With grad pairs (1, 1), (−1, 1) and a reversed control at equal B utility, compare a passive taper, GradMatch plus taper, and a direct slot edit as an oracle.
- **Old-task retention check:** Put A near a margin on the first shard and C near one on their sum; check the installment itself, not just the smaller contrast it leaves.

#### 13. Retire a group only if unequal clocks cannot unmask it (P)
- **Mechanism:** Certify the difference using bias-corrected moments and actual per-shard clock/mask transitions. Treat raw weighted–uniform cancellation as provisional if later decays or clocks can give the terms different weights.
- **Novelty vs nearest prior art:** Adam bias correction is standard; the candidate is an exit test on when a cancellation is preserved by lawful clock transitions, not a new correction rule.
- **Cheapest first test:** Three shards with zero raw contrast, then pause one clock under a legal mask and resume. Compare aligned-clock approximation, resetting clocks and keeping private gains; enumerate early and late resumes.
- **Old-task retention check:** A reads the aggregate before resume; C reads the resumed feature. Evaluate both through every allowed order, including the reset baseline.

#### 14. Price the position offset separately from momentum (P)
- **Mechanism:** Track an upper bound on output displacement already accumulated during taper plus a bound on the remaining update gap. Never release width solely because the momentum contrast shrank below tolerance.
- **Novelty vs nearest prior art:** #277#10 already anchors a re-tied-v tail; this applies its distinction to signed gain-driven displacement and asks when a useful native continuation can reduce, rather than compound, the existing offset.
- **Cheapest first test:** Use F2 and add a reversal with two legal gains. Compare bounds with and without the offset, a naive contrast threshold, and a control where the reversal only increases the offset.
- **Old-task retention check:** A is near a margin already spent during taper and C is sensitive to the reversal; report the worst trajectory margins as well as final recovery.

#### 15. Stage retirement by continuation visibility (P)
- **Mechanism:** Where several shard groups share a budget, discard only groups whose gain contrasts are harmless on the current legal suffix; bill any retained ratios until their own check passes. A later mask outside that suffix must not inherit the receipt.
- **Novelty vs nearest prior art:** Tiered state allocation retains high-value slots; this tiers gain lifetimes by future read/write obligations, not parameter magnitude or present activity.
- **Cheapest first test:** Give two groups opposite early/late relevance with room for one retained group. Compare all-at-once exit, magnitude-ranked storage, and equal-byte quantized gains plus a warmdown.
- **Old-task retention check:** A depends on the early group and C on the late one; test an adversarial legal ordering and an out-of-contract ordering that the receipt must deny.

#### 16. Propagate the gap on each trajectory's own gradients (I)
- **Mechanism:** For a tiny closed-loop host, enumerate legal suffixes twice from the exit cut, recomputing gradients at each branch's own weights. Use failures of the common-trace estimate to identify when a cheap feedback bound is necessary.
- **Novelty vs nearest prior art:** #277 already requires a feedback check, and guarded Adam compression holds gradients fixed. This is a falsification benchmark for extending a gain-exit bound to closed loop, not a new certificate by itself.
- **Cheapest first test:** Use one contracting and one expanding scalar quadratic continuation; compare F2-style trace arithmetic, a coupled analytic bound and exact enumeration at H = 3.
- **Old-task retention check:** Measure A and C on both branches after every step. Count a small trace gap with actual old-task loss as a missed failure, even if the endpoint looks safe.

### C. Make the opening probe pay for the exit

#### 17. Choose the probe for both admission and retirement (P)
- **Mechanism:** Among legal probes, prefer one that separates worlds whose gain would be useful during the window but whose feasible exits differ. Grant only a gain and exit plan that work together across the bin; don't spend a second exit probe.
- **Novelty vs nearest prior art:** #277#17 hands gains to a cooling tail, and discriminating design separates models. The proposed interaction is one observation removing an alias shared by the two decisions, versus independently optimized gate and retirement.
- **Cheapest first test:** Three quadratic worlds: safe scale, unsafe shape, and useful scale with an unretirable mode. Compare stacked gate plus best exit rule at one probe total, and a paid two-probe oracle. Include a set with no jointly decisive direction.
- **Old-task retention check:** Make A expose false openings and C expose false exits. Evaluate both after refusal, during the gained interval and at every suffix cut.

#### 18. Pick the gain that avoids creating the mode it must retire (P)
- **Mechanism:** Use each response bin to select gains with an upper bound on the projected *future* stale contrast, not just on current shape residual. Accept a smaller gain if it still hits B/P and permits a uniform exit.
- **Novelty vs nearest prior art:** #277#03 fixes total gain and #277#06 audits the resulting momentum. The candidate is to choose within a bin for downstream uniform-retirement feasibility rather than waiting to audit the damage.
- **Cheapest first test:** Enumerate a gain grid on a state-dependent two-shard quadratic where two rates have equal B progress but create different terminal gradients and m contrasts. Compare max-safe gain plus best taper, fixed budgeted gains, and an example where all useful gains leave a bad contrast.
- **Old-task retention check:** A is scored at the high-gain interior step and C after fold; require both floors at matched B/P and width deadline.

#### 19. Bind release to the disturbance that invalidates the probe (P)
- **Mechanism:** Attach a validity condition to the gain tied to publicly visible mask and routing events. If an event can turn a scale bin into a shape bin, run the registered safe exit *before* taking the event, or refuse; do not quietly renew the stale probe.
- **Novelty vs nearest prior art:** #277#14 conditions cooling on mask changes; here the same event ends the authority to use the multiplier and may require spending exit slack before the next legal write.
- **Cheapest first test:** Three-step stream with one announced and one unannounced mask reveal. Compare a fixed gain timeout plus best taper, per-event re-probing charged in full, and a disturbance that cannot be safely preceded by retirement.
- **Old-task retention check:** Serve A on the old route and C on the new route at the boundary; declined branches must still serve both under the fallback.

#### 20. Spend saved state bytes on a paid exit option (P)
- **Mechanism:** If one response bin needs a short-lived contrast to permit a later safe decision, prepay its storage or refuse admission. Compare the resulting byte-time to keeping private v until commit; do not count a retained contrast as retired.
- **Novelty vs nearest prior art:** #277#18 escrows cooling memory and guarded compression retains difficult coordinates. Here the initial probe chooses a specific reversible exit option and its bounded liability, not just a smaller state code.
- **Cheapest first test:** Enumerate bins on a three-coordinate fixture with cap for one stored contrast. Compare low-bit m plus warmdown, a best fixed reserve plus the probe, and a bin needing two independent contrasts.
- **Old-task retention check:** A and C depend on different contrasts; exercise early retirement, the paid delayed retirement, and cap-triggered refusal without dropping old-task updates.

#### 21. Share a probe only for a joint retirement decision (P)
- **Mechanism:** When two windows overlap, allow one ordinary diagnostic response to authorize the *pair* of gain schedules only if every compatible world can pay both exit gaps from the shared reader margin. Do not issue independent permissions whose guarantees can be added twice.
- **Novelty vs nearest prior art:** [Useful-batch-checks #273](https://github.com/manojbajaj95/cl/pull/273) already proposes joint claims from one check. The possible extension is selecting paired optimizer schedules whose signed cumulative retirement displacements are provably coupled; the shared check itself is inherited.
- **Cheapest first test:** Two windows with either opposite or reinforcing stale effects on the same output. Compare the #273-style joint check with independent best tapers, separate probes at equal total work, and an order that destroys a claimed cancellation.
- **Old-task retention check:** A reads the coupled output and C reads each window's effect separately; neither mutual cancellation nor acceptable endpoint loss excuses an intermediate regression.

#### 22. An exit-aware lower bound on what one probe can buy (I)
- **Mechanism:** Search for two histories with the same observable responses and the same useful opening gain, but with disjoint sets of useful, safe exit plans under the deadline. This witnesses a limit even for a perfect scale/shape gate.
- **Novelty vs nearest prior art:** #277#16 rules out a short cooling tail; standard identifiability rules out classification. The yardstick here is a common *window-and-exit policy*, not whether each hidden history has a private solution.
- **Cheapest first test:** Enumerate short discrete moment histories with a shared opening read but one needing a positive and one a negative tail action. Compare one-probe policies at equal work, an extra-look oracle and a wider retained state; drop the witness if a common fallback still hits B/P on time.
- **Old-task retention check:** Give A and C opposite signed margins so each wrong exit violates a different floor. Check both throughout the no-gain fallback to distinguish a safe refusal from a service failure.

## Ranked deeper questions

1. **Can one paid, legal read certify a useful gain *and* a feasible uniform exit without private v?** (01–05, 17, 22) Start by finding a reachable alias that survives a good scale/shape probe but disagrees on the safe exit. Beat the separately tuned gate-plus-retirement stack at equal cost on useful on-time exits; if the legal probe menu cannot resolve the conflict, quantify the no-gain fallback rather than claiming a win.
2. **What is the smallest sound retirement check once gradients respond to the switch?** (09–14, 16) Begin with a finite CPU closed-loop enumeration and delayed-mask counterexample. Compare one-step matching, warmdown, reset, frozen ratios and a re-shared v tail. Separate clock/mask forcing, accumulated output drift and fresh-gradient feedback.
3. **Can useful work create the needed evidence or pay off the exit mode without adding a private state array?** (06, 12, 18–20) Compare against the best due-batch selector plus a separate probe or taper at equal work. Require an interaction on a stream where no single free opener or passive taper hits deadline, B/P utility and both old-task floors.
4. **Can many shards share evidence without sharing the same safety margin twice?** (07, 15, 21) Find a signed coupling that survives legal order changes and protects both aggregate and local readers. If a single reinforcing branch breaks it, retain state or refuse rather than pooling the guarantees.
