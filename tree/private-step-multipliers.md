# Private step multipliers and certified cooling tails

**Status:** Ideas only; no pilots, training runs, or GPU work. **Parent:** [Tied split moments](tied-split-moments.md) ([PR #264](https://github.com/manojbajaj95/cl/pull/264)). **Review seeds:** [Flood triage row 380](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md#L380) scores two ideas 3: #02 gives each shard a private scalar step multiplier under one shared second moment; #06 keeps private moments during divergence, then switches to shared moments for a short cooling suffix before a commit with a certified bounded gap.

**Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md). A fold made exact by changing the reference is not evidence of useful learning. A combined proposal must beat the stacked baselines at equal bytes and information. Every first test below protects both old tasks A and C, not just a fit to the new task. **P** denotes a candidate reusable primitive; **I** denotes a candidate improvement or falsifier. These are proposal labels, not reviewer verdicts.

## What would be new?

- [AdamPM](https://arxiv.org/abs/2610.24598) pools moment entries along rows or columns to save memory; [Adam-mini](https://arxiv.org/abs/2406.16793) assigns second-moment scales by block; [Adafactor](https://arxiv.org/abs/1804.04235) reconstructs preconditioner shape from factored statistics. [LAMB](https://arxiv.org/abs/1904.00962) already puts a layer-wise trust ratio on an adaptive update. Scalar rescaling, pooling and factoring are not novelty claims. The candidate operation is **temporary optimizer freedom with a predeclared return to a narrow continuation**.
- [Second-Moment Memory in Coordinatewise Adam](https://arxiv.org/abs/2608.15824) shows that lingering large squared gradients can suppress Adam's progress. The parent's F1 gives a concrete cross-shard analogue: a 100× gradient-scale mismatch produces a 70.71× slowdown on the quiet shard under steady mean-square pooling. The open question is whether a lawful scalar policy recovers useful progress without borrowing a private denominator in disguise.
- [Guarded Compression of Adam Optimizer State](https://arxiv.org/abs/2611.00589) certifies the first restored Adam update over a shared gradient domain. The tail proposal instead decides when to **stop carrying private state and release width**, against a private continuation over a declared horizon with an unchanged new-task and old-task contract. Post-hoc minimal sufficient state ([parent of the parent, #239#02 discussion](minimal-fold-state.md#what-would-be-new)) is the strongest offline comparator. This is an abstract-level prior-art screen, not a priority claim.

## Contract and two algebraic checks

Fix the host, peak bytes (including multipliers, shadows and evidence), narrow budget, feature domain D, allowed update words U, horizon H, optimizer arithmetic, A/C floors, B/P utility floors and gap tolerance before opening a window. Use matched samples, width-steps and clocks; charge probe gradients, failed attempts and refusal delays. Report A and C individually through the wide window, transition, commit and H follow-up steps, B/P progress at matched effort, and refusal rate separately from quality of accepted folds. If the check fails, refuse the refund and keep the last lawful model. Report exactness in real arithmetic separately from implementation rounding.

**S — Scalars can fix a scale mismatch, not a shape mismatch.** For frozen twin features, private first moments and one shared v, let the shard rates be η·cᵢ, with cᵢ positive. In the quiet shard of F1, a fixed 70.71× multiplier cancels the steady denominator ratio when ε = 0; this is algebra, not a progress result. On a vector, one scalar can exactly reproduce the private-v update only if the shared/private denominator ratios agree on all active first-moment coordinates. A two-coordinate shard with required ratios (2, 1/2) cannot do it. Do not estimate a scalar from the private per-coordinate v in a claimed memory-saving arm; that is an oracle.

For an exact tied fold, freeze the cᵢ for all post-commit steps, give twins identical future gradients and masks, and keep their bias-correction clocks aligned. With C = Σcᵢ, transport the read-out by sum, the first moment by Σ(cᵢmᵢ)/C, the shared v unchanged and the narrow rate as η·C. This follows by linearity of the first-moment recurrence; a common predeclared multiplier on all cᵢ can instead be absorbed into η. If the wide reference switches back to unit multipliers at commit, use the ordinary mean and k·η against **that** reference; also audit the transition against continuing the old multipliers. If the relative multipliers can change after folding, one weighted first moment generally loses information. Feature motion, unequal masks, shard-dependent decay and clock differences each need their own closure proof.

**T — Re-tying is exact against a tied twin, not against the private twin.** At entry to the suffix, project private vᵢ to their mean v̄, retain the private first moments, and switch the actual shards to a shared v. For a cheap **common-trace diagnostic** with equal rates and aligned clocks, run the private shadow on the same prescribed shard gradients. When those gradients are identical across shards during the suffix and continuation, the raw discrepancy obeys |vᵢ−v̄| after L+j steps = β₂^(L+j)·|vᵢ−v̄| at tail entry. Bias-correct the discrepancy by 1−β₂^t. For ε > 0, the reciprocal-denominator error on each step is bounded by √|v̂ᵢ−v̂̄|/ε²; tighter intervals are possible when denominators have a certified lower bound. Multiply by η·|m̂ᵢ|, sum over shards and steps, and scale by sup on D of |h| for one frozen feature h. In the simplest fixture with identical read-outs at tail entry, the bound sums **from tail entry**, not just after commit. If the gradients differ across shards, add the EMA of the square-gradient mismatch to the discrepancy recurrence; if trajectories generate their own gradients, certify gradient feedback as well (e.g., finite enumeration or a Lipschitz error recurrence on declared D and U). Without that extra check, the trace bound is not a closed-loop refund certificate.

Report three gaps separately: actual tied-wide to narrow (potentially zero), narrow to **always-private** from the same pre-tail checkpoint (target ≤ τ through H, including the accumulated parameter offset), and actual A/C floor margins. Shared state equality or exponentially decaying v discrepancy alone cannot certify the second or third gap.

**A limit on what the tail buys:** On a fixed common gradient trace, mean projection commutes with the EMA, so re-tying L steps early and mean-transporting at the same commit step yield the same terminal raw v. Any advantage over that control must come from the path, different paid storage, or closed-loop gradient changes, not a closer terminal denominator. For a negative control, set v = (4, 0), m = (1, 0), and use all-zero gradients with ε > 0 and 0 < β₁, β₂ < 1. The active shard always steps farther under mean tying than under private v, so its read-out offset has one sign and is already nonzero after the first step. No longer tail can certify an arbitrarily small parameter gap in this example.

**Baseline stack.** For S: tied from birth without scalars (#251#03), tuned fixed parameter-group rates or LAMB-style trust ratios on pooled Adam-mini/AdamPM, private v (both oracle and charged), v-reset at fold, and the non-scalar shape case above. For T: tied from birth, private v with a hard reset at fold, mean transport with L = 0, #239#02 post-hoc state selection, an intentionally too-short suffix that the certificate must refuse, and a permanent split. For hybrids, stack the best scalar control with the best transport/reset control and the same retention audit, data, bytes and time. Report absolute and incremental gains, not just a win over default Adam.

## Idea cards

### A. What one scalar can buy (#264#02)

#### 01. Fold-locked gain ratios (P)
- **Mechanism:** Give each shard one bounded gain inferred from a few RMS observations; freeze the ratios before commit and define the narrow continuation by the weighted-moment map in S.
- **Novelty vs nearest prior art:** AdamPM plus fixed group rates reproduces the window; only the optimizer-state transport and a predeclared retirement of those rate degrees of freedom could add value.
- **Cheapest first test:** On two 1-D quadratics sweep gradient ratios from 1 to 100; compare time to B/P targets and the first three folded updates with the baseline stack.
- **Old-task retention check:** Give A and C separate frozen holdouts with asymmetric margins, and check both at the last wide, first narrow and third narrow steps.

#### 02. Shape-refusal witness (P)
- **Mechanism:** Before opening a window, give a lower bound on any scalar policy's best local step fit using two non-overlapping admissible gain intervals.
- **Novelty vs nearest prior art:** Adafactor tries to recover shape; this is a witness that scalarizing a proposed shard cannot meet both coordinate tolerances, irrespective of tuning.
- **Cheapest first test:** Enumerate gains on the (2, 1/2) case in S and on a positive control (2, 2); compare with paid factored and private denominators.
- **Old-task retention check:** Put A and C on opposing coordinate margins; verify a false scalar admission causes a visible regression and refusal preserves the checkpoint.

#### 03. Gain gauge with a safety budget (P)
- **Mechanism:** Redistribute gains subject to Σcᵢ = k so the folded rate stays fixed; solve jointly for useful private steps and slack on protected outputs.
- **Novelty vs nearest prior art:** LAMB clips or scales individual layers; a fixed total gain makes compensation a scarce allocation with a predictable narrow rate.
- **Cheapest first test:** Enumerate a two-shard gain simplex under several scale mismatches. Compare with clipped LAMB and independently tuned gains at matched total step norm.
- **Old-task retention check:** Give A and C differently signed responses to a transferred unit of gain and require both to stay above their floors even when B improves.

#### 04. A probe that chooses who gets the gain (P)
- **Mechanism:** Spend one extra probe on a direction with maximal disagreement between a common scale shift and coordinate-specific interference; only the former can justify scalar compensation.
- **Novelty vs nearest prior art:** Adafactor observes row/column statistics; the candidate is a decision probe for whether a cheap scalar path should be opened at all.
- **Cheapest first test:** Create diagonal worlds with the same pooled RMS but different direction mismatch; compare the probe with a random gradient and a past-RMS rule, at one extra gradient each.
- **Old-task retention check:** Reserve unseen A and C slices in both worlds; measure damage from false approvals and the opportunity cost of false refusals without using those slices to fit gains.

#### 05. Shock quarantine without a second v (I)
- **Mechanism:** Detect when one shard dominates a pooled squared-gradient update. Temporarily increase the quiet shard's gain up to a cap, and retire the gain when its held-out progress recovers.
- **Novelty vs nearest prior art:** The second-moment memory paper explains suppression, and capped adaptive rates are established; the improvement would be recovery from a partner's shock without retaining a private moment array.
- **Cheapest first test:** Inject one shock then reverse the quiet gradient. Compare recovery with clipping plus a trust ratio and with resetting pooled v, not just uncorrected pooling.
- **Old-task retention check:** Measure peak A and C damage during the shock and after reversal; a gain that amplifies stale momentum enough to cross either floor loses.

#### 06. Gain retirement without a hidden momentum jump (P)
- **Mechanism:** Test the two candidate terminal weightings of m before retiring relative gains. Use a common taper only when it meets a predeclared transition-gap allowance; otherwise keep the frozen ratios in the reference or refuse.
- **Novelty vs nearest prior art:** Learning-rate warmdown is standard; the retirement criterion is whether changing the ratios discards a continuation mode invisible to the unweighted mean.
- **Cheapest first test:** Use m = (1, −1) and c = (2, 1) before a zero-gradient step, then sweep common and relative tapers against abrupt unit gains and fixed ratios.
- **Old-task retention check:** Put A near a zero-step decision margin and C near the opposite margin; test both before and after gain retirement, not just after folding.

#### 07. Low-rank gain shapes with a paid exit (P)
- **Mechanism:** Predeclare a small bank of feature groups that may gain separate scalars during the window; return to one scalar only where those components can be retired within a certified gap.
- **Novelty vs nearest prior art:** Adafactor and Adam-mini already encode low-dimensional shapes; the new operation would retire temporary rank under a narrow-state contract rather than keep a factored optimizer indefinitely.
- **Cheapest first test:** On a four-coordinate diagonal toy, sweep one through four groups and compare with byte-matched Adafactor plus hard reset. Hold out a second coordinate partition.
- **Old-task retention check:** Place A and C on different groups, including the least useful group for B, and require both to survive the rank collapse.

#### 08. Gain offers before the other shard is known (P)
- **Mechanism:** Each learner publishes a bounded gain interval and an old-task slack estimate from solo probes. Negotiate a shared v only when those offers admit a jointly feasible total gain.
- **Novelty vs nearest prior art:** Adam-mini partitions known weights; the candidate operation is a composable offer for a later blind partner, not a better block heuristic.
- **Cheapest first test:** Enumerate pairs from three 1-D learner types, with one incompatible pair. Compare against independent tuning plus a pooled-v admission check of the same information cost.
- **Old-task retention check:** Audit held-out A and C after pairing, including unadvertised but admissible partner orders; log both misses and refusals.

### B. What a short tail can actually certify (#264#06)

#### 09. Earliest safe re-tie receipt (P)
- **Mechanism:** Start the suffix at a predeclared trigger; release width at the first step where the charged H-step private-reference gap and A/C floors both pass, rather than after a prescribed L.
- **Novelty vs nearest prior art:** One-step guarded compression accepts or escapes a codec; this receipt selects a safe release time for a live private-to-shared transition.
- **Cheapest first test:** Enumerate all suffixes in a two-shard scalar toy with gradients drawn from a small alphabet. Compare with best fixed L, L = 0, and the intentionally too-short control.
- **Old-task retention check:** Track worst A and worst C across all accepted words, including a case that meets the optimizer bound but misses a task floor.

#### 10. Offset-aware anchor at tail entry (P)
- **Mechanism:** Choose a shared v and, only if the host contract permits it, a bounded read-out correction by minimizing the *running* gap to the private twin; carry no per-shard offset after fold.
- **Novelty vs nearest prior art:** Mean transport and one-step guarded compression fit a state; this anchor accounts for displacement incurred during cooling rather than only denominator agreement at commit.
- **Cheapest first test:** On a prescribed sign-flipping gradient word, compare minimax anchoring, mean plus a matched correction, and untouched mean. Verify the result on unseen words and count correction bytes and probes.
- **Old-task retention check:** Score A and C immediately before and after the anchor, then at every suffix step, to catch an apparently good final gap bought by temporary damage.

#### 11. Coupled rather than independent interval bounds (P)
- **Mechanism:** Bound the difference recurrence for two trajectories under the *same update word*, branching on the gradient or activation cells where the coupling stops being useful.
- **Novelty vs nearest prior art:** Guarded Compression exploits the shared gradient in one step; this extends the idea to different internally generated gradients over a finite word.
- **Cheapest first test:** Enumerate two-step closed-loop quadratic updates with exact interval endpoints. Compare certificate tightness and cost with two separate trajectory envelopes and direct enumeration.
- **Old-task retention check:** Add one A and one C margin near cell boundaries; every certified box must retain both when enumerated, not only the box center.

#### 12. Two clocks, one refund (P)
- **Mechanism:** Normalize differently aged private EMA histories to a shared clock at tail entry and explicitly bound the subsequent bias-correction discrepancy; prefer refusal to silently dropping the ages.
- **Novelty vs nearest prior art:** Adam bias correction compensates an optimizer's own age; the candidate is a transport rule across shard ages under one terminal clock.
- **Cheapest first test:** Initialize twins at ages 1 and 20 with the same raw v, enumerate warmup-length words, and test effective-v transport versus mean, reset and a paid extra clock.
- **Old-task retention check:** Report A and C just after re-tying, especially in the early steps where age normalization changes them most.

#### 13. Separate cooling memory from deployment memory (I)
- **Mechanism:** Use a lower β₂ for both the actual tied run and a matched scheduled-private reference during the suffix; restore deployment β₂ at commit and separately audit against ordinary always-private Adam.
- **Novelty vs nearest prior art:** Shortening the Adam memory horizon is suggested by second-moment slowdown; only a measurable reduction in safe refund time over abrupt reset or scheduled-private Adam would count.
- **Cheapest first test:** Sweep tail β₂ on a scalar pulse-plus-noise fixture, matching width-steps. Reject schedules that look safe only against the scheduled reference.
- **Old-task retention check:** Check A and C at both hyperparameter boundaries and on a noisy old-task revisit to expose variance bought by faster cooling.

#### 14. Cooling through rare mask changes (P)
- **Mechanism:** Admit only U schedules whose equal-twin-mask segments are long enough for contraction; account for each allowed asymmetric mask event as a new source term and prove the narrow map still implements U or refuse.
- **Novelty vs nearest prior art:** #239#02 tests minimal continuation state for a specified U; this schedules the move into a refundable U while retaining explicit counterexamples for unsupported mask words.
- **Cheapest first test:** Enumerate one skipped-shard update at every position in a four-step word, with compensation by a paid extra slot as a control.
- **Old-task retention check:** Set A to depend on a normally frozen channel and C on an always-trainable channel; audit both on every admitted mask word.

#### 15. A certificate that spends old-task margin (P)
- **Mechanism:** Turn a closed-loop output-gap bound into a per-task margin budget with separate A and C slack. Tight margins can veto commit even when the global tolerance passes.
- **Novelty vs nearest prior art:** Metric thresholds and one-step guards are standard; the candidate is a reusable receipt linking an optimizer-state release bound to each protected task's independent floor.
- **Cheapest first test:** In a tiny classifier, give A/C equal average margins but unequal lower tails; compare admissions against a norm-only tolerance and direct held-out accuracy.
- **Old-task retention check:** Check full A and C predictions over the enumerated admissible words, including one near-boundary class in each, and count any false certificate.

#### 16. Impossibility of a useful short tail (P)
- **Mechanism:** Construct two private reference states with equal candidate narrow statistics but provably separated by more than 2τ under one permitted word, forcing refusal for at least one of the two states.
- **Novelty vs nearest prior art:** #239#02 gives exact minimal-state lower bounds; this is an approximate, tail-length-dependent obstruction at an operational tolerance.
- **Cheapest first test:** Search two scalar v histories on a rational grid for opposite read-out offsets and a shared-gradient continuation. Compare the lower bound on L with the earliest feasible L from 09.
- **Old-task retention check:** Choose A and C witnesses sensitive to opposite continuations and verify the violating state would affect old-task behavior rather than merely a hidden slot.

### C. Joining the two seeds without moving the goalposts

#### 17. Gain-to-tail handoff (P)
- **Mechanism:** Run private v only while scalar failure is certified; at tail entry translate the private update into bounded gains under shared v, then freeze ratios or pay for their retirement.
- **Novelty vs nearest prior art:** AdamPM with a trust ratio can already implement the end phase. The possible interaction is less tail-entry damage at the same certified width-release time than scalar-only or cooling-only arms.
- **Cheapest first test:** Use a two-phase quadratic stream with coordinate mismatch early and scale mismatch late. Compare the full 2×2 scalar × tail factorial and the baseline stack.
- **Old-task retention check:** Check both protected tasks at first divergence, first tied step, commit and every follow-up; reject a hybrid that only hides an early A or C loss at commit.

#### 18. A controller with a byte-time escrow (P)
- **Mechanism:** Reserve capacity for either private v or a scalar-paid cooling suffix at split birth. Spend it only when the certified release forecast improves at matched pending-writer wait.
- **Novelty vs nearest prior art:** The parent's shared byte pool prices a terminal footprint; this candidate prices how long optional optimizer state stays live, with the third writer able to rely on release deadlines.
- **Cheapest first test:** Simulate two split windows and one waiting writer with fixed deadlines. Compare against best fixed tail plus an independent terminal pool with the same peak bytes and byte-steps.
- **Old-task retention check:** Score A and C before the waiting writer starts, just after it writes and after the next fold; a speedup that borrows slack from a later old task loses.

#### 19. A chain of refunds that propagates slack (P)
- **Mechanism:** Feed each accepted gap through a declared stability bound to the next fold, keeping a cumulative allowance rather than resetting τ after every commit.
- **Novelty vs nearest prior art:** The parent's chained budget receipts track slots, not how a private-to-shared approximation changes later trajectories and consumes a sequence-level error allowance.
- **Cheapest first test:** Enumerate three split–cool–fold cycles on one frozen feature with one expansive regime; compare summed local gaps, propagated gaps and recertification from the original reference.
- **Old-task retention check:** Hold A and C fixed across all cycles; fail if either floor is crossed by a sequence that would have passed three local checks.

#### 20. Certified selective reset by coordinate (I)
- **Mechanism:** At tail entry, reset v only where the projected future gap is smaller than mean transport, otherwise keep the tied mean. Evaluate both against the same untouched private reference.
- **Novelty vs nearest prior art:** Bulk v resets and per-coordinate compression guards already exist; the improvement must be a shorter certified tail at the same bytes versus guarded mean/low-bit transport plus hard reset.
- **Cheapest first test:** Sweep a four-coordinate fixture with a recent shock on only one coordinate and disjoint sign patterns; compare all reset subsets with the one-step and H-step chooser.
- **Old-task retention check:** Put A on the shocked coordinate and C on an untouched one; report transient deficits as well as H-step metrics.

#### 21. Refund under a withheld partner reversal (P)
- **Mechanism:** Publish a gain-and-tail contract over a small class of future task reversals; search for the word with the largest gap to the private reference and keep the counterexample with every refusal.
- **Novelty vs nearest prior art:** Matched-state adaptation differences show why reversals can matter; the candidate is an adversarial refund receipt portable to a partner who did not disclose the realized reversal.
- **Cheapest first test:** Hide the reversal time and one gradient sign during fitting, then enumerate their admissible combinations. Compare with a random holdout and an oracle tuned to the realized word.
- **Old-task retention check:** Include revisits to both A and C inside the reversal words and score their first-at-return behavior before any relearning.

#### 22. Separate private-update matching from useful learning (I)
- **Mechanism:** Compare scalar and tail policies on two matched streams: one where private Adam learns the right direction and one where its normalized step is a nuisance. Gate on B/P utility as well as numerical fidelity.
- **Novelty vs nearest prior art:** The parent's variance-tax fixture measures a slowdown; this falsifier asks when removing that slowdown or imitating the private twin is a bad objective even with a valid fold.
- **Cheapest first test:** On two small supervised regressions, flip the correlation of one high-variance gradient component while preserving its RMS. Compare with plain tying, reset and the stacked baseline.
- **Old-task retention check:** Evaluate matched A and C holdouts on both streams; report any gain in new-task fit achieved only by reproducing a private-reference regression.

## Ranked deeper questions

1. **When does re-tying buy an earlier lawful width refund than a reset?** (09–11, 13, 16) Start with one finite, closed-loop CPU fixture and compare exact worst-word gaps against the analytic envelope. The decisive result is a real interval of L for which reset fails and a short tail passes, with A/C and B/P floors met. No credit for contracting v while leaving a large read-out offset.
2. **Is one scalar enough in the regimes that actually incur the variance tax?** (01–05, 07) Map scalar feasibility against B/P progress as scale and shape mismatches vary independently. A useful boundary must beat tuned pooled Adam plus group gains or trust ratios on decisions at equal bytes, not merely reproduce the parent's 1-D arithmetic.
3. **Is the scalar–tail handoff an interaction or two interchangeable tricks?** (06, 12, 17, 20) Compare the factorial against the stacked baseline at equal peak bytes and width-steps. Look for cases where gains specifically keep tail-entry drift small enough to accept commits neither constituent wins alone.
4. **Can another writer rely on the refund without knowing the private history?** (08, 14–15, 18–19, 21) Test whether portable gain offers and horizon-aware slack receipts admit more useful on-time commits than local recertification without hiding cumulative A/C regressions or assuming an unseen partner obeys the advertised U.
