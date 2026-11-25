# Seam leaks: check what fragments pass forward and train a park before it is needed

**Status:** Ideas only; no pilot, code, or GPU work. **Parent:** [Glued fragments](glued-fragments.md) ([PR #224](https://github.com/manojbajaj95/cl/pull/224)), cards 07 and 17. **Review seeds:** The [#224 flood-triage row][triage] advances seam non-interference and a pre-trained maintenance-mode park in its score-3 column. **Ledger read first:** [Idea ledger][ledger].

## What must a blind seam preserve?

Fix a public transcript, the set `H` of all compatible reachable histories, the legal edit language `L`, and a service horizon. A seam is the boundary between two fragments, including the state the first leaves live for the second: weights, norm statistics, clip thresholds, optimizer slots, active gates, counters, or other state in scope. Blindness is about the **actual edit actions**, not just choosing the same named fragment. At the same public input and coupled public seed, the composed editor must issue the same effective updates, schedule, and externally visible edit-side effects in every history. Comparing only declared calls would miss a history-dependent scale; requiring equality of all latent state would reject harmless differences. A history-varying read is harmless only if its entire in-scope effect is invariant, including later uses of residual state. Comparing distributions under unrelated seeds does not establish this property. Offline paired worlds are for certification, not live observations; a live history probe is a licensed split, not a blind seam.

A park is a fixed public value on an active coordinate, chosen before future B edits are disclosed. Train the old host to keep serving ordinary A and independent rare-old C both normally and with that coordinate parked. Certify the entire park–edit–clear path, not just the trained park point; the clear target is public and no per-history copy or restore is allowed. Floors apply separately to each obligation in each compatible history; historical averaging is not certification. Freeze the scope of histories, edit family, capacity and continuation before evaluation. If scope coverage is only empirical, call it a test, not a universal guarantee. Keep refusals in the denominator.

**Prior-art floor.** [Information-flow typing][flow] and [hyperproperties][hyper] already express two-run non-interference; [Pacti][pacti] composes contracts, and [conformant planning][conformant] already solves blind planning on belief states. A producer–reader manifest alone is not a new primitive. [Once-for-All][ofa] already trains one model for multiple deployment settings, [Net2Net][net2net] preserves function under network transformations, and [GEM][gem] protects previous tasks by constraining updates. Training at a fixed setting alone is not a new primitive either. The bets here are a reusable **certificate of what a downstream editor can do with seam state**, and an active fixed-width host trained to provide **blind safe progress on unseen edits**, not just to produce good predictions when parked.

**Common test rules.** `P` marks a conditional primitive candidate; `I` marks an improvement or diagnostic, including direct implementations of the review seeds. In every proposed test check A and rare C at every served tick, at B commit, and under a held-out continuation, alongside achieved B utility and refusal rate. Compare the simplest tying control on each card and the applicable strongest lawful stack: whole-program relational blindness (#211#05), exact finite conformant planning, and clamping/reset for seams; dual-mode old-task training plus edit-time park synthesis (#211#08) or [neutral reroutes][neutral] for parks. Match normal A/C performance and realized B gain or report the frontier, not raw success at unmatched quality. Charge old training, offline world construction, proof search and checking, persistent bytes, spare width, pauses and observations. No control gets the deleted history for free. The ledger's failed read-pinning test warns that stable intermediates need not protect old tasks; its return-point adapter verdict rules out hiding a save/restore stack in a park.

## Two exact paper fixtures

### 1. A clip leak that even endpoint equality misses

Let `h ∈ {−1,+1}` be a hidden old-history tag; the live scalar norm summary `n=(3+h)/4` is reachable from old training. Initially public `x=3/4` and shared threshold `τ=3/4`. Fragment F writes `τ ← n` without exposing `n` to the editor; fragment G sets `x ← min(1,τ)` on a public unit proposal. The final fragment sets `x ← 3/4` (B's target) and may leave `τ` dead for the remaining declared horizon. A is always 1; old C's score is `1−|x−(3+h)/4|` with floor `2/3`.

| History | After F: `τ` | After G: `x` | C after F, G, final | Final `x` |
|---|---:|---:|---|---:|
| −1 | 1/2 | 1/2 | 3/4, 1, 3/4 | 3/4 |
| +1 | 1 | 1 | 3/4, 1, 3/4 | 3/4 |

Every floor passes; F issues the same normalization operation but leaves different latent thresholds. G consumes the difference as an effective edit action. A checker treating all shared inputs as public within each isolated invocation can miss it; an end-to-end check comparing actual edit traces will not. **Blind positive control:** F sets `τ ← 3/4`; G now acts identically, and all C scores are 3/4. **Blind-but-unsafe control:** keep F and lower G's public proposal to 1/2. Both G calls now write 1/2, but C for `h=+1` dips to 1/2. **Blind-and-safe varying-state control:** keep F, have G write `x ← 1/2 + min(1/4,τ/2)` (3/4 in both histories), and prove that no later reader observes `τ`. This masks a varying input; a blanket ban on tainted reads would wrongly reject it.

### 2. Old training opens a maintenance path at matched normal service

Let `h ∈ {−1,+1}` index old obligations. A fixed-width host has a public design coefficient `a` frozen at deployment, gate `s∈[0,1]`, and edit bits `w,u∈{0,1}`. Start at `(s,w,u)=(1,0,0)`. One coordinate may change per tick, with no simultaneous writes. The old floors are `A_h,C_h ≥ 3/4`, where

- `A_h = 1 − (1−s)(3/4−a−h/8)`;
- `C_h = 1 − (1−s)(3/4−a+h/8) − h·s·(w−u)`.

Compare an unprepared old-training endpoint `a=1/2` to a park-constrained endpoint `a=3/4`; both score exactly 1 on A and C at start for both histories. The fixture assumes those endpoints are achievable by old training; it does not show that an optimizer will find them cheaply. At the first bit flip, `|w−u|=1`. The exact worst C over histories is `1−(1−s)(3/4−a+1/8)−s` with `w` first and `1−(1−s)(3/4−a)−|(1−s)/8−s|` with `u` first. For the unprepared host the latter peaks at `7/9` when `s=1/9`, but worst A and C on entry to that state are only `2/3`. In fact A requires `s≥1/3`, where worst C at the first flip is at most `7/12` with `u` first and at most `5/12` with `w` first. Neither order works. **Edit-time tying control:** relax both floors to `2/3`; setting `s=1/9` and flipping `u` first then works without old training. A solver testing only the `w`-first order would miss this tie.

In the prepared host, set `s ← 0; w ← 1; u ← 1; s ← 1`. At every parked tick the worst A and C are `7/8`; they are 1 on clearing, and B's target `(1,1,1)` is met. There is no history read or restore. **Out-of-scope negative:** require `(1,1,0)` instead; some C is 0 at that commit for any `a`. A trained park does not make an incompatible target safe.

## Idea cards

### Find, close, or price a seam leak

#### 01. Check the producer and the consumer together (I; #224#07)
- **Mechanism:** Give each fragment a manifest covering writes and their dependencies, downstream read sites, and all effective action sinks, including scaling. On paired reachable seam states, follow an upstream difference to a downstream action rather than treating the shared input as public by default.
- **Novelty vs nearest prior art:** A direct application of [information-flow typing][flow] and #211#05 to extracted fragments; the control has to analyze the same state, not a deliberately weaker list of calls.
- **Cheapest first test:** Use fixture 1's leak, clamped positive and masked-reader positive; compare whole-program self-composition and isolated per-fragment typing on the same manifests and proof budget.
- **Old-task retention check:** Check both histories' A/C traces under every arm, then append a reader that reopens the masked channel. A retained but leaky script must still fail blindness.

#### 02. Export a certificate indexed by the next consumers (P)
- **Mechanism:** Certify a history-varying seam as equivalent for a named family of downstream editors, not for all readers. Export the equivalence relation and horizon with the fragment; adding a reader requires a proof that its action respects the relation, or invalidates the certificate.
- **Novelty vs nearest prior art:** [Pacti][pacti] composes contracts and [hyperproperties][hyper] already model the proof; the candidate object is a portable, consumer-indexed license to reuse a variant seam across independently assembled edit scripts.
- **Cheapest first test:** Exhaust a three-value threshold domain and three clip readers with overlapping saturation regions; compare memoized whole-script self-composition and static per-seam clamping at equal proof bytes and work.
- **Old-task retention check:** Add a late larger proposal that reads outside saturation. Retain A/C on the original scripts and require expiry before the new reader can use the seam.

#### 03. Find the smallest public overwrite that closes all live paths (I)
- **Mechanism:** Trace backward from varying action sinks, then synthesize the cheapest public overwrite or substitution that cuts every live producer–reader path while satisfying A/C/B. A candidate cut must still pass relational verification.
- **Novelty vs nearest prior art:** Information-flow repair and program slicing are the nearest template; this is an optimization for edit quality, not a replacement for them.
- **Cheapest first test:** Plant parallel norm and gate paths with a shared derived scale. Compare minimum cut plus exact checking against exhaustive single-buffer resets and an all-buffer reset with matched stall allowance.
- **Old-task retention check:** Give C a dependency on a counter unrelated to the leak; bulk reset must not get credit for preventing the leak if it drops C after one update.

#### 04. Close a channel by shaping the producer rather than resetting state (P)
- **Mechanism:** Before deletion, replace a fragment's norm-write recipe with one that maps all histories to the same downstream scale while preserving the producer's other old-task effects. Reuse that recipe after deletion without branching or storing a per-history recipe.
- **Novelty vs nearest prior art:** [GEM][gem] constrains weight updates and #224#07 rejects a bad seam; the candidate operation changes the producer to free a previously unusable reader, without erasing all slot state.
- **Cheapest first test:** Enumerate two-bit norm estimators and two downstream scales; pit a shared transformed producer against a public reader clamp and full slot reset. Count feasible B moves, not just norm equality.
- **Old-task retention check:** Give A a dependence on the preserved component and C a delayed dependence on the slot update. If public clamping preserves both at matched B gain it ties.

#### 05. Detect a leak that exists only in a joint read (I)
- **Mechanism:** Hold public seeds fixed and propagate pairs of reachable state tuples rather than independent per-buffer summaries. A comparer may see equal marginals for two gates across private histories while their parity determines which edit is emitted.
- **Novelty vs nearest prior art:** Joint information flow and [hyperproperties][hyper] already account for this; the idea is a test fixture for manifest-induced false negatives.
- **Cheapest first test:** Let the first gate be a public random bit and the second be equal to it in one history and its complement in the other; the reader consults gate equality. Compare paired-history checking to explicit full-state self-composition and univariate distribution tests.
- **Old-task retention check:** Make C fail only on the joint gate action in one history; evaluate it per seed and history, never on marginal activation rates.

#### 06. Demand a reachable leak witness, not a synthetic state swap (I)
- **Mechanism:** Attach a replayable pair of old prefixes to each counterexample, with the same public transcript and seed but a divergent edit action. Screen spurious alarms from independently swapping slots that are constrained jointly by the optimizer.
- **Novelty vs nearest prior art:** Concretization in counterexample-guided abstraction and [conformant planning][conformant] already reason about reachable states; this targets false refusals in the seam monitor.
- **Cheapest first test:** Enumerate two-step momentum histories where some combinations of `m` and `v` cannot occur; compare a paired-prefix witness to exact reachability and naive slot swaps.
- **Old-task retention check:** Include a reachable sign-crossing C regression as well as the impossible swap; reject the first without reducing coverage on the second.

#### 07. Make clocks and random draws part of the seam contract (I)
- **Mechanism:** Require equal published commit ticks and equivalent public random-draw consumption, not just equal updates. A gate that skips a draw or delays a fragment can otherwise make an identical subsequent call use different randomness or run against a different arrival.
- **Novelty vs nearest prior art:** Timing and probabilistic non-interference are established; this is an audited action alphabet for fragment editors.
- **Cheapest first test:** Exhaust two seeds and two equal-output fragments with conditional draw consumption. Compare counter-addressed public draws plus fixed ticks to padding only and to whole-program trace checking.
- **Old-task retention check:** Place a rare C query between the two ticks and use a seed-sensitive continuation after commit; padding cannot count as free service.

#### 08. Separate dormant history state from an expired blindness proof (P)
- **Mechanism:** Permit a varying inactive slot to remain without a backup if its reader set is proven unreachable through a public expiry event. At expiry, statically block activation until there is a fresh proof or a fixed public write; do not choose the write based on the slot.
- **Novelty vs nearest prior art:** [Pacti][pacti] contracts and liveness analysis already express dead state. The candidate operation is a reusable seam lease that allows useful live edits today without silently granting future consumers access.
- **Cheapest first test:** Run a gate that can be reopened by two distinct public events, one outside the proof. Compare a lease to zero-on-park, irrevocable scrubbing, and exact horizon-wide model checking.
- **Old-task retention check:** Give C legitimate service through a separate read during the lease and an unsafe late edit reader; retain C then refuse or reseal before opening the new reader.

#### 09. Refute blind repair with two histories that need disjoint actions (P)
- **Mechanism:** For a feasible prefix and fixed legal action alphabet, prove that every public next action violates an obligation in at least one history or makes B unreachable within budget. Emit a time-bounded obstruction and allow an explicitly priced split as a separate option.
- **Novelty vs nearest prior art:** [Conformant planning][conformant] and the parent's seam cores already refute plans. A portable obstruction at a shared seam could inform whether to redesign the writer, park, or spend observation, but only if it transfers across scripts.
- **Cheapest first test:** Use fixture 1 with a tighter independent C slice that arrives at G's tick on a fixed public schedule and requires `1−|x−(3+h)/4|≥7/8`. The required x intervals are disjoint. Compare reusable pair cores to exact finite belief-state planning and generic UNSAT cores.
- **Old-task retention check:** Check the scheduled slice when it is served and the original A/C obligations throughout. Charge both the hypothetical split and its return-to-service schedule.

#### 10. Preserve safe physical variation while equalizing the edit (I)
- **Mechanism:** Split the seam interface into service-only state and action-producing state. Keep history-dependent normalization in ordinary predictions if it never affects edit actions; provide the editor a public scale and prove that service scores do not feed it back through scheduling or gating.
- **Novelty vs nearest prior art:** [Batch normalization][bn] already separates normalization modes and information-flow partitioning is known. The useful diagnostic is distinguishing damage from resetting service state from genuine editor blindness.
- **Cheapest first test:** Use a two-stream affine model with distinct means and one shared edit magnitude. Compare split interfaces against per-layer frozen public statistics and shared BN with no edit-time reads.
- **Old-task retention check:** Check rare C under its own statistics at every tick, then plant a feedback edge from service confidence to the clip threshold and require rejection.

### Train a fixed park that actually supports later edits

#### 11. Buy a universal park during old-task training (I; #224#17)
- **Mechanism:** Fix `s_park` before seeing B and minimize old-task loss subject to separate worst-history floors in normal and parked modes. Freeze the host and the public clear rule before drawing future edits.
- **Novelty vs nearest prior art:** Direct seed; [Once-for-All][ofa] trains multi-setting subnetworks and #211#08 searches for a park at edit time. The experiment asks whether the future blind edit option pays for old training rather than assuming this is new.
- **Cheapest first test:** Check fixture 2, then propose a tiny piecewise-linear CPU host with old stream order randomized and B edit families held out. Compare paired-mode training with ordinary and width-matched randomly dropped-coordinate training, both allowed exact edit-time park search.
- **Old-task retention check:** Score independent A and worst rare C on normal/parked modes, all edit ticks and after clear; report training cost and any loss on old tasks even if B becomes easier.

#### 12. Train the park's safe edit region, not only its endpoint (P)
- **Mechanism:** During old training certify a largest fixed-width tube of lawful writes with `s=s_park`, independent of future target identities. Treat its verified shape as a reusable edit-capability interface, and only accept paths inside it with a separately certified clear.
- **Novelty vs nearest prior art:** [Robust optimization][robust] bounds adversarial perturbations and #224#13 certifies survival under concurrent continuation; a park-specific tube would buy safe **useful** write paths with entry and exit attached, not just margins.
- **Cheapest first test:** Learn a 2-D rectangle in a tiny bilinear host; compare to dual-mode adversarial training under the same perturbation budget plus exact edit-time search. Hold out B directions, including one outside the tube.
- **Old-task retention check:** Check A/C on all tube corners and along actual paths, using exact bounds where available, and on the clear and first continuation tick. A safe park with no B progress is a failure.

#### 13. Teach a public edit lattice whose steps remain connected (P)
- **Mechanism:** Train along legal neighbor transitions in parked mode so the certified safe region is connected from the current host to multiple exits through atomic writes. Reward the number of reachable exit classes, not the count of individually safe parked points.
- **Novelty vs nearest prior art:** [Conformant planning][conformant] searches a fixed state graph; dual-mode training targets predictions. The candidate is shaping the lawful edit graph offline so later blind plans have more reachability at fixed width.
- **Cheapest first test:** In a 3-bit host with two safe islands, shape one edge without adding a coordinate. Match old floors and number of safe vertices against pointwise robust training plus exact search.
- **Old-task retention check:** Inspect A/C on every intermediate bit flip and distinct exit, then test a novel C constraint at the new bridge; an unverified bridge must be unavailable.

#### 14. Reserve parked slack for rare old tasks rather than the mean (I)
- **Mechanism:** Allocate the old-training park penalty across named old slices using per-slice dual penalties; maximize the weakest parked margin subject to normal-service and edit-capability constraints.
- **Novelty vs nearest prior art:** Group-robust optimization already does worst-group training; this is a cost allocation improvement for parked service, not a new retention rule.
- **Cheapest first test:** Use two frequent old slices and a rare slice with an opposite response to `s`. Compare a group-balanced replay budget and ordinary worst-group training applied in both modes.
- **Old-task retention check:** Hold back a shifted rare C slice, check its worst margin along the edit and continuation, and count lower normal-mode quality as cost rather than balancing it away.

#### 15. Train the same park through every reachable old update order (P)
- **Mechanism:** Choose a small public invariant for the parked host and train an old-task update rule that maps each member of a bounded belief class back into it. Future B editors retain the same fixed park license after old-task arrivals without observing their order.
- **Novelty vs nearest prior art:** [GEM][gem] constrains each update and #224#21 transports drift certificates; the candidate is a learned *renewable* shared parking interface preserved by allowed old-task transitions.
- **Cheapest first test:** Exhaust two old update types over three arrivals; compare invariant-preserving training against dual-mode rehearsal plus fresh park certification after each arrival at equal total work.
- **Old-task retention check:** Measure A/C after each arrival and every subsequent prescribed B phase. Hold out a longer order and distinguish failure of extrapolation from failure within the certified horizon.

#### 16. Pre-train a park whose clear map has no old-state input (P)
- **Mechanism:** Constrain old training so clearing is a single public function of the declared B target and control schedule. Train the normal and parked dynamics to converge to valid clear states without storing the pre-park gate, momentum, or a history-specific restore recipe.
- **Novelty vs nearest prior art:** [Net2Net][net2net] preserves a function during transformations and #224#14 already forbids escrow leaks. The candidate capability is training a family of public clears that covers held-out B targets absent any history-specific inverse.
- **Cheapest first test:** Enumerate a 2-slot host with two old slot signs and three B targets; compare fixed clear, dual-mode training plus edit-time public clear synthesis, and same-byte save/restore as a separately labeled non-blind reference.
- **Old-task retention check:** Verify independent A/C after both clear and the next two optimizer steps. Reject a parked host that needs the saved sign to retain C.

#### 17. Learn to park a coordinate that still matters in normal mode (I)
- **Mechanism:** Require a minimum contribution from the active coordinate in normal service on an independently designed intervention, while learning a fixed park with enough margin. Exclude the degenerate solution where training makes the coordinate permanently inert.
- **Novelty vs nearest prior art:** [Once-for-All][ofa] and ablation-based specialization already train across subnet choices. The added value is a falsification control for the maintenance-mode claim.
- **Cheapest first test:** Compare matching-width hosts with an active trained gate, a dead gate, and a fixed always-parked gate; make normal-mode A need the gate to exceed a specified performance target above its hard floor.
- **Old-task retention check:** Compare per-mode A/C, and charge lost normal surplus as well as any hard-floor failure. Demand comparable B gain, not just a park certificate.

#### 18. Pre-train one park value across independently trained hosts (P)
- **Mechanism:** Freeze a shared public gate convention before independently training multiple old hosts. Export the same park/write/clear interface and verify the common write region across hosts; the later editor sees neither which old stream ran nor a per-host park token.
- **Novelty vs nearest prior art:** Multi-setting training [Once-for-All][ofa] targets one shared model, while [neutral reroutes][neutral] protect changes within a host. The candidate object is a blind maintenance interface portable across independently trained histories at unchanged width.
- **Cheapest first test:** Train or solve three small old hosts with different orderings and leave the fourth out; compare per-host offline park synthesis with a shared constant and with independently trained dual-mode baselines under the same train budget.
- **Old-task retention check:** Include a fourth host with a C direction rotated out of the common write region; reject it or shrink coverage, and check A/C from entry through clear on every claimed host.

### Combine the two seeds without counting either part twice

#### 19. Train a park that cuts a known producer–consumer dependency (P)
- **Mechanism:** Shape a live gate so its fixed park value removes the coefficient on a history-varying seam input in every relevant reader, while A/C still use the main host. The post-clear proof must show that residual differences cannot re-enter the edit.
- **Novelty vs nearest prior art:** #224#19 puts a park between incompatible fragments and [information-flow typing][flow] detects dependence. The candidate is designing one state that buys both legal gluing and live service before either exact B target or reader instance is known.
- **Cheapest first test:** Let G's public scale have a term `s·(τ−3/4)` and use fixture 2's old floors. Compare against the **stack** of dual-mode training, public clamping and an edit-time park solver at matched width and B gain.
- **Old-task retention check:** Add a rare C slice that needs some residual gate coupling and a delayed reader after clear. Reject if eliminating the leak sacrifices that slice or merely delays the leak.

#### 20. Certify reusable blind seams across service interruptions (P)
- **Mechanism:** Synthesize one park contract valid after any legally scheduled ordinary A/C service event within a bounded edit window. Live service may move the norm summary; a trained parked reader must remain invariant without inspecting the service event's private outcome.
- **Novelty vs nearest prior art:** #224#09 permits safe interruption and #224#13 covers concurrent continuations. This candidate combines that guarantee with blindness under **paired** schedules, not merely retention along each schedule.
- **Cheapest first test:** Enumerate two service insertions either side of F and a single continuation update. Compare against a matched stack of a public norm freeze, compositional trace checking and a stall, charging service latency.
- **Old-task retention check:** Invoke A/C during interruptions and after resumption. Plant a C failure caused by freezing adaptation and a separate leaky resume that retains C.

#### 21. Learn a portfolio of public parks without letting park choice split histories (P)
- **Mechanism:** Prepare two public park settings of the same active coordinate for disjoint public B edit regions. Select only from the public B specification and prove the selector, live path and clear safe across the same `H`; no confidence-triggered private dispatch.
- **Novelty vs nearest prior art:** [Once-for-All][ofa] is already a portfolio of deployment settings; exact conformant planning already chooses universal actions. The candidate is a trained menu of live maintenance regions whose selection creates new blind write capability without adding a route per history.
- **Cheapest first test:** Use a scalar gate with two coefficient zeros affecting two B directions, and a family requiring both zero simultaneously as a refusal case. Match against a single trained park plus exact edit-time synthesis and a licensed split under equal resources.
- **Old-task retention check:** Test both switch paths, the ambiguous public B case and a rare C slice specific to one setting; do not average away unsupported regions.

#### 22. Map where the cheaper intervention ties (I)
- **Mechanism:** Cross presence of seam leakage, sensitivity of A/C to clamping, and scarcity of park margin. Compare certification alone, public repair alone, park training alone, and their joint design, keeping impossibility and uncovered edits in the result.
- **Novelty vs nearest prior art:** A falsification map, not a primitive. It extends #224#22 to include leakage and amortization instead of rewarding a stack for winning only against its individual parts.
- **Cheapest first test:** Exhaust the fixture variants, then account for training cost amortized over 1, 4 and 16 held-out B requests. Compare the best stack of public clamp/reset, dual-mode training and exact conformant planning at each budget.
- **Old-task retention check:** Require identical per-tick A/C constraints and matched B utility before computing savings; record blind-but-unsafe, safe-but-leaky and no-legal-reply cells separately.

## Ranked deeper questions

1. **Can a consumer-indexed seam certificate beat whole-program checking without changing what counts as blind?** Start with #02 and the masked, leaky and delayed-reader variants of fixture 1. Require identical accept/refuse outcomes to exact paired trace checking within scope, then test certificate reuse across new fragment assemblies. If cache-aware whole-program checking ties after invalidation cost, keep manifests as engineering, not a new primitive.
2. **Does old training buy a larger safe edit region, or simply move old-task margin into a convenient coordinate?** Compare #12/#13 to margin-matched dual-mode training plus exact edit-time synthesis. Use withheld legal B targets, both bit orders in fixture 2, matched normal A/C, and a negative target that cannot be cleared. Count blind progress per total cost, including refusing requests.
3. **Can one trained park both close a real channel and keep live service better than the best stacked control?** On #19/#20 compare against public clamping plus dual-mode training plus edit-time planning. Check paired action traces under service interruptions and after clear; if retention requires reusing the hidden seam value, the result is not a blind park.
4. **When should the editor stop trying to glue and pay for a split?** On #08/#09/#22, separate an airtight reachable obstruction from an incomplete proof, then compare refusal, a public repair, and a priced licensed observation. Record the smallest public change that makes a blind plan possible without pretending the observation was free.

[ledger]: https://github.com/manojbajaj95/cl/blob/386a2f189c0504915a7c884be43e5754d1d86be7/reviews/idea-ledger.md
[triage]: https://github.com/manojbajaj95/cl/blob/386a2f189c0504915a7c884be43e5754d1d86be7/reviews/flood-triage.md#L336
[flow]: https://doi.org/10.1109/JSAC.2002.806121
[hyper]: https://doi.org/10.3233/JCS-2009-0393
[pacti]: https://arxiv.org/abs/2303.17751
[conformant]: https://arxiv.org/abs/1401.3468
[ofa]: https://arxiv.org/abs/1908.09791
[net2net]: https://arxiv.org/abs/1511.05641
[gem]: https://arxiv.org/abs/1706.08840
[bn]: https://arxiv.org/abs/1502.03167
[robust]: https://arxiv.org/abs/1706.06083
[neutral]: https://github.com/manojbajaj95/cl/pull/183
