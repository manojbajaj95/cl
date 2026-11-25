# Shared route budgets: count what new-task SGD closes, replay while a joint route still works

**Status:** Ideas only; no training, pilot, or GPU work. **Parent:** [Self-depleting teaching supply](self-depleting-supply.md) ([PR #220](https://github.com/manojbajaj95/cl/pull/220)). **Review seeds:** [Flood triage, row 332](https://github.com/manojbajaj95/cl/blob/358fd8c800e452935da7472b2aece542309d400a/reviews/flood-triage.md#L332), score-3 cards **#03** (certify lost routes, not lost units) and **#19** (replay before the last joint route closes). **Read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/358fd8c800e452935da7472b2aece542309d400a/reviews/idea-ledger.md).

## What would count as new?

Separate **which truthful presentations can still jointly teach two old obligations** from **whether the learner still performs its old tasks**. An old read can pass after the last joint route is gone; many example strings can share a single exhaustible route. The bet is that a small, checkable certificate can distinguish these cases before the replay decision, not that a new plasticity score ranks examples better.

**Nearest comparisons.** [Operator counting](https://ojs.aaai.org/index.php/ICAPS/article/view/13581), matching, and reachability already supply the combinatorics; [interval bound propagation](https://arxiv.org/abs/1810.12715) supplies one tool for checking margins. [ReDo](https://arxiv.org/abs/2302.12902) measures dormancy and recycles units; [Dohare et al.](https://arxiv.org/abs/2306.13812) study continual loss of plasticity. [MIR](https://arxiv.org/abs/1908.04742) retrieves examples threatened by the imminent update; [Learn the Time to Learn](https://arxiv.org/abs/2209.08660) learns a replay schedule; [Dark Experience Replay](https://arxiv.org/abs/2004.07211) is a strong equal-budget replay control. None of these comparisons establishes priority. The ledger already killed the generic replay-deadline option (PR #113: smooth value decay, timing policies effectively tied) and Gramian reserve selection. A scheduling gain with an imposed cliff, an old-loss forecast, or a rank/dormancy proxy is not a resurrection of either idea.

## Contract and two paper fixtures

Freeze the truthful example pool, presentation atom, optimizer (including slots), admissible B minibatches, order and repeat rules, horizon, information available at each decision, and free transcript. Let `z_A,z_C` count distinct discharges for two specified families of old obligations; old-task retention is independently measured on ordinary held-out A/C tasks and worst slices, at prescribed floors at every live prefix. Compare policies at the same new-task B utility target, replay count, and presentation budget; report verification work, bytes, failed checks, and fallback. A replay record is truthful even when it no longer has a usable route.

**Upper graph and charging.** Fix route identities before seeing the B stream. An upper graph covers **every** lawful joint presentation in the reachable envelope, not only sampled successful ones. It can include latent routes (activation and expiry tracked separately), so lawful activation need not add an upper edge. Give the graph capacity tokens: every sequence of joint presentations must consume distinct covered tokens, not distinct example strings or paths. One sufficient proof assigns each joint transition a token it permanently removes and shows all other transitions preserve or shrink the available token set. More generally, use a nonnegative graph-derived cap `S` and verify `Δ(z_A+z_C+S) ≤ cost` on all reachable edges: free B increments neither discharge and only deletes upper edges, a joint paid step consumes at least one unit of cap, and a paid non-joint step may not increase the cap without an explicit price. From a zero-progress snapshot this gives `max(d_A,d_C,d_A+d_C−S_0)` presentations for demand `(d_A,d_C)`, assuming each presentation discharges at most one obligation per family. A genuine unrepresented route, a token reused for two spends, or an unpriced refill invalidates the associated bound; revert to the separately proved per-family bound. Do not silently rename a reopened route. An upper cap falling does not certify that the exact optimum rose; compare with an exact small-game oracle.

**Deadline and readiness are different proofs.** Upper exclusion can certify that a route is impossible after a time; upper presence cannot certify that it works before then. To prescribe replay, require a separate, executable continuation witnessing readiness and a joint spend on the **same** route within the replay window and all A/C floors. If the B suffix is unknown, distinguish a witnessed schedule from a policy with a lawful witness for every permitted suffix using only information available online. If replay creates new capacity, account for it separately before claiming that an earlier no-refill deadline applies.

**F1 — equal units and witnesses, different budgets.** Two abstract learners each have two capacity-one receivers, two truthful joint examples, and demand (2,2). In X both examples can spend only receiver 1; in Y one spends receiver 1 and the other spends receiver 2. Singles cost one and do not affect receivers. All stipulated ordinary A/C reads pass; receiver availability models joint teaching, not old accuracy. The caps are 1 and 2, and exact costs 3 and 2. Delete receiver 1's routes and costs become 4 and 3. Copying an example adds a witness, not a receiver. As a negative, a free B step reconnecting receiver 1 in X after the deletion makes the old bound 4 wrong (cost 3).

**F2 — latest safe replay is earlier than the last live route.** On a scalar shared coordinate, ordinary B SGD uses loss `(x−1)²/2`, step size 1/2, and `x_0=0`. At ticks 0 through 3, `x=(0,1/2,3/4,7/8)`. In this hybrid paper game one unspent joint token is live only at `x≤3/4`. A truthful old replay presented at tick `r` opens its gate exactly at tick `r+1`, for that tick only; replay and the joint spend do not move `x`. An ordinary A probe has smooth loss `x²/2) and a floor equivalent to loss ≤ 1/2, so it passes throughout; C's ordinary reads are held fixed. With one replay and one joint presentation, legal replay ticks are 0 and 1: tick 2 still has a live route but its opener is too late, and tick 3 has the largest observed old loss. A gate that opens immediately would also admit tick 2. The route threshold and gate lag are assumptions, not discoveries about learning. The useful follow-up must derive a similar decision from a learner's actual finite updates and withstand a smooth no-cliff control.

## Idea cards

**P** = candidate primitive (an object or operation other methods could use); **I** = improvement or diagnostic, not a standalone pilot. The seed restatements are marked explicitly. All first tests are proposed paper or small CPU tests, not results.

### Prove what is gone and what charges a spend

#### 01. Keep a deletion-only upper route graph (P; parent #03)
- **Mechanism:** Give each truthful example-to-joint-obligation route a fixed identity; use finite-step margin witnesses to remove edges and prove no admissible ordinary B minibatch can add one. Charge each joint spend against the cap.
- **Novelty vs nearest prior art:** ReDo counts dormant units and #220's scalar cap counts supply; graph certification would bound what differently wired but equally dormant learners can jointly teach.
- **Cheapest first test:** Start from F1, then derive a deletion in a two-feature gated learner under ordinary B SGD. Match dormancy, effective rank, and old margins; compare scalar supply and recomputed reachability. Offer one legal reopening.
- **Old-task retention check:** Check both normal old tasks after each B update and after all joint spends, including in the reopening negative.

#### 02. Certify the cut, not the number of paths (P)
- **Mechanism:** Export an upper-graph cut whose arcs carry independently verified spend capacities; even disjoint-looking examples crossing one consumable receiver get one bill.
- **Novelty vs nearest prior art:** Max-flow/min-cut and operator counting are established; the candidate is a cut over verified finite-SGD teaching transitions, not a path-count heuristic.
- **Cheapest first test:** Duplicate F1's witness strings and add one physically independent receiver. Compare count, static min-cut without burn verification, and exact reachability; plant a reusable arc that a cut incorrectly bills once.
- **Old-task retention check:** Test held-out old inputs using the cut and bypass receivers before and after the last charged use.

#### 03. Attach a proof of absence to an edge (P)
- **Mechanism:** Store a compact exclusion witness (a sign interval and forward-invariance proof for the closed side); reuse it through a held-out B suffix instead of testing the example at every step.
- **Novelty vs nearest prior art:** Interval verification certifies properties over sets; here the transferable object is impossibility of a particular future spend under optimizer dynamics.
- **Cheapest first test:** In a two-ReLU model compare an interval witness with exact recomputation and cached point checks. Hold out a lawful crossing minibatch; a verifier must refuse its envelope.
- **Old-task retention check:** Probe paraphrases and low-margin normal A/C reads on both sides of the removed gate.

#### 04. Price uncertain edges without deleting them (P)
- **Mechanism:** Keep ambiguous edges in the upper graph but require a witnessed route for action. Ask which single paid diagnostic can resolve uncertainty on a binding cut, charging its actual effect if the diagnostic trains the learner.
- **Novelty vs nearest prior art:** Active verification picks queries and operator counting supplies bounds; the candidate is a proof economy with opposite soundness rules for exclusion and replay.
- **Cheapest first test:** Create two hidden momentum states with the same visible weights, one permitting a joint use. Compare cut-directed inspection with random inspection, full-state access, and no query at equal cost.
- **Old-task retention check:** Test A/C after every diagnostic and spend in both hidden states; reject a diagnostic that makes a previously lawful old read fail.

#### 05. Certify joint budgets for subsets, not a single global quota (P)
- **Mechanism:** Export caps for fixed subsets of obligations; a scarce receiver used by one pair cannot also pay for another pair. Enforce all subset constraints in one relaxation.
- **Novelty vs nearest prior art:** Hall cuts and cost partitioning already do this combinatorially; the candidate is a portable obligation-subset budget derived from shared learner features rather than counts of stored examples.
- **Cheapest first test:** Give three obligation types a common receiver and a spare exclusive to one pair. Compare a total cap, separate pairwise caps, and the exact optimum; change which pair is requested after certification.
- **Old-task retention check:** Audit all three old tasks, including the family excluded from the actual spend.

#### 06. Compile an ordered replay route into one burnable certificate (P)
- **Mechanism:** Represent a lawful short word of truthful examples as a route, with a prefix proof and a single token for the terminal joint discharge; preparing the word is charged but cannot discharge it twice.
- **Novelty vs nearest prior art:** Macro operators and #220 #16 cover sequences; the extension is a budget-preserving compilation across multiple alternative words sharing one terminal token.
- **Cheapest first test:** Enumerate two overlapping two-item words; compare a flat route graph and exact sequencing. Insert a B step that invalidates only one prefix and an accumulation control.
- **Old-task retention check:** Check A/C after each prefix, not just at the macro boundary.

#### 07. Split a false shared cut by optimizer state (P)
- **Mechanism:** Refine only proof cells where one set of observed weights conflates two different burn capacities; certify the hidden slot range from the lawful history, not a reset.
- **Novelty vs nearest prior art:** Counterexample-guided abstraction refinement is standard; the candidate is slot-aware accounting that tightens a teaching lower bound without exporting complete checkpoints.
- **Cheapest first test:** On one momentum coordinate, make equal-weight histories disagree on whether a second spend is lawful. Compare exact checkpoints, weight-only cells, and learned thresholds; hold out a third history.
- **Old-task retention check:** Match A/C starting margins and verify both through the distinguishing second presentation.

#### 08. Distinguish deletion from representation relabeling (P)
- **Mechanism:** Use a fixed token identity defined by observable teaching transitions; permit a path lift across unit permutations only if it preserves spends and cannot map two successive burns to one identity.
- **Novelty vs nearest prior art:** Neuron alignment and graph quotients already remove symmetries; the extra contract preserves resource consumption, not just predictions or apparent edge count.
- **Cheapest first test:** Apply a known two-unit permutation as a representation check, then an actual B update that loses a path. Compare raw unit IDs, assignment-based alignment, and exact costs; ensure the quotient does not hide a true refill.
- **Old-task retention check:** Verify both normal old tasks after the relabeling and after the genuine B step.

#### 09. Track monotonicity under whole minibatches, not per-item gradients (I)
- **Mechanism:** Check finite optimizer transitions for allowed batch compositions, distinguishing serial updates from a single accumulated update and including admissible clipping and LR changes.
- **Novelty vs nearest prior art:** #220 already asks for minibatch closure; this is an adversarial validity audit, not a scheduling or gradient-order claim.
- **Cheapest first test:** Enumerate a two-example B pool where both singleton steps pass but a lawful batch or slot state reopens an edge; compare exact finite updates with first-order screening.
- **Old-task retention check:** Check A/C after serial, accumulated, and clipped transitions at matched B utility.

#### 10. Compose local route certificates across shared layers (P)
- **Mechanism:** Give each layer proof obligations for emitting and consuming route tokens; link only with a compatibility witness, so an upper edge cannot disappear locally and be recreated by an untracked downstream bypass.
- **Novelty vs nearest prior art:** Assume–guarantee verification is mature; the candidate is a composable accounting interface for truthful learner updates with a shared burn identity.
- **Cheapest first test:** Compare two serial gates and a skip connection against whole-network interval verification and exact reachability. Add a downstream-only activation that defeats naive intersection.
- **Old-task retention check:** Test old inputs reliant on each gate and on the bypass after every B step.

#### 11. Give soft effects a conservative weighted route budget (P)
- **Mechanism:** Freeze a target for measurable old teaching progress; bound the total possible extra joint progress by nonnegative weights on verified exhaustible resources, rather than thresholding one gradient norm into “alive.”
- **Novelty vs nearest prior art:** Potential heuristics and #220 already weight progress; the extra test is whether route-local weights still prove a useful global bound in a smooth learner with no binary gate.
- **Cheapest first test:** Use a smooth two-feature regression game with partial discharges; compare a scalar potential, thresholded route counting, and an exact finite-horizon solver. Reject any bound that works only after imposing a cliff.
- **Old-task retention check:** Check held-out A/C continuous loss and worst slice throughout, independently of the progress used to fit the weights.

### Turn a route certificate into a replay decision

#### 12. Replay before closure, not at peak loss (P; parent #19)
- **Mechanism:** Intersect a certified drain deadline with the truthful opener's readiness window, and choose a slot with an actual lawful joint continuation.
- **Novelty vs nearest prior art:** MIR addresses threatened items and learned replay scheduling addresses when to replay; the candidate is a checkable loss-independent feasibility window for a particular shared spend. The ledger's failed generic deadline remains a negative control.
- **Cheapest first test:** Extend F2 to matched-loss B streams with different route calendars. Compare fixed/spaced, loss-triggered, MIR plus scheduling, fitted recency, #220's combined potential, and exact planning at equal replay count. Include coincident closure and loss peaks.
- **Old-task retention check:** Test A/C at every slot and after the spend, matching starting margins and B utility so early replay is not simply acting on a stronger model.

#### 13. Require the opener and the deadline to name the same route (P)
- **Mechanism:** Attach an executable continuation to an opener; do not combine readiness for route X with the later closure deadline for route Y.
- **Novelty vs nearest prior art:** Planning already binds actions to preconditions; the CL candidate is a same-route proof joining two separately measured replay effects.
- **Cheapest first test:** Give two old examples identical immediate loss and readiness scalar, but opposite route identities. Compare a pooled calendar, the parent's potential, and exact scheduling with identity shuffling.
- **Old-task retention check:** Audit old tasks immediately after both truthful openers and at the purported joint use, including the non-served old slice.

#### 14. Reserve a failover slot across unknown B suffixes (P)
- **Mechanism:** Issue a contingent replay policy with a verified common first action or a branch keyed only to information visible before the deadline, and refuse if each valid continuation requires advance knowledge of the suffix.
- **Novelty vs nearest prior art:** Robust scheduling and policy trees are known; the proposed object is an online certificate that retention and a shared teaching spend can both be achieved without hindsight.
- **Cheapest first test:** Branch a two-step B stream into suffixes with opposite draining routes. Compare clairvoyant search, exact online planning, and a fixed schedule; move the branch observation past the last safe slot as a negative.
- **Old-task retention check:** Require A/C floors on both suffixes, including the wait branch and any paid fallback.

#### 15. Match two expiring openers to two non-reusable routes (P)
- **Mechanism:** Couple interval feasibility to shared capacity so two replay records cannot both reserve the same bottleneck; certify an assignment of opener, route, and spend tick.
- **Novelty vs nearest prior art:** Interval matching and deadline scheduling are not new; the candidate is a schedule witness with state-dependent route consumption validated on actual learner prefixes.
- **Cheapest first test:** Give two old items overlapping expiry windows but only one common receiver; add a later alternative route for one. Compare earliest-deadline-first, generic scheduling plus MIR, and exact search; add a spend that invalidates a nominal assignment.
- **Old-task retention check:** Check A/C after each opener and spend, especially the task whose replay is postponed.

#### 16. Publish a missed-window witness instead of retrying replay (P)
- **Mechanism:** Once every relevant route is excluded, certify that spending additional old presentations on openers cannot produce the joint discharge under the declared no-refill law; switch to singles or stop making a joint claim.
- **Novelty vs nearest prior art:** Dead-end detection exists in planning; the CL object is a negative guarantee about truthful replay while its independent old-task utility may still be positive.
- **Cheapest first test:** Present one old item after closure that still helps A alone. Compare loss-based retries, generic dead-end search, and a planted paid reset that must invalidate the refusal's premise.
- **Old-task retention check:** Measure A/C through fallback and report any real standalone value of the skipped replay.

#### 17. Choose replay from progress-indexed, not wall-clock, closure (P)
- **Mechanism:** Certify a route's safe window in a verified cumulative B progress coordinate; map it to presentation slots under the actual admissible B update rates.
- **Novelty vs nearest prior art:** LR-area decay and the parent's dose bounds already replace clock time; the extension requires a verified link to a route-specific deadline and opener lag, not a fitted scalar clock.
- **Cheapest first test:** Compare two curricula with equal B loss and unequal directional drift, plus a pair where the proposed coordinate should transfer. Compare wall time, LR area, and exact reachability; count coordinate verification work.
- **Old-task retention check:** Check normal old behavior at matched B utility and through the intervening high-drift updates.

#### 18. Commit one replay before learning which old obligation becomes urgent (P)
- **Mechanism:** A truthful opener reserves one route that can serve either of two later permissible joint demands, but the certificate counts only one eventual spend across those alternatives.
- **Novelty vs nearest prior art:** Row 327's PRS1 already shares an opening across unknown finishes; the narrower bet is that a deletion certificate can verify the remaining common option under ordinary B without a full contingent plan.
- **Cheapest first test:** Compare preopening, separate bookings, no reservation, and exact online planning on two possible suffix demands; include a demand that becomes revealed after its route has closed.
- **Old-task retention check:** Evaluate all old tasks before revelation and after either finish, not just the old task that turns out to need replay.

#### 19. Use a paid refill only when the old route budget is exhausted (P)
- **Mechanism:** Offer a separately billed truthful action that restores capacity, and attach a certificate of how much it can add. Never use the earlier no-refill cap on the augmented game without rechecking the edge inequality.
- **Novelty vs nearest prior art:** ReDo replenishes units and #220 already distinguishes opening from creating supply; the candidate is comparing a certified local refill price with the cost of switching to singles, not calling recovery new plasticity.
- **Cheapest first test:** In F1 compare one genuine reconnecting action, a latent opener, and ordinary singles against exact search. Bundle refill with an existing discharge as the negative; edge accounting must reject the old price if it becomes unsound.
- **Old-task retention check:** Verify normal A/C after refill, throughout the added uses, and at the matched B endpoint.

#### 20. Attribute two replay effects without billing twice (P)
- **Mechanism:** Use paired continuations to ask whether a truthful old atom improves held-out retention and independently preserves access to a route; a ledger entry records both effects but only one presentation cost.
- **Novelty vs nearest prior art:** #220's dual-effect opener is the baseline; the increment is causal attribution to a distinct route when another same-loss item protects reads but spends or misses that option.
- **Cheapest first test:** Cross two truthful records with a disabled versus enabled downstream receiver; compare dual-credit proof, MIR plus an equally useful non-opener, and an arm where the two effects reduce to one margin.
- **Old-task retention check:** Evaluate independent normal A/C probes, including the old slice absent from the replay buffer.

### Try to kill the mechanism

#### 21. Match complete old-loss traces, not just the peak (I)
- **Mechanism:** Construct B streams with the same old loss trace and matched initial margins and dormancy but different joint reachability and replay utility; separately construct a smooth stream without a meaningful closure.
- **Novelty vs nearest prior art:** This is a stronger negative-control design for the ledger's PR #113 result, not a new timing method.
- **Cheapest first test:** Search a tiny shared-feature learner for paired traces without imposing a route cliff. Compare the strongest loss/recency schedule, parent potential, and exact search; if replay utility is smooth and timing ties, keep the null.
- **Old-task retention check:** Use separate held-out old tasks and slices to match old behavior; trace matching on the replay record is insufficient.

#### 22. Audit the joint certificate against the best stack (I)
- **Mechanism:** Cross route-altering B vs route-neutral B, truthful opener vs equally retaining non-opener, and shared vs independent capacity. Give the baseline the best scalar supply check plus generic replay scheduler.
- **Novelty vs nearest prior art:** This is the ledger's merge gate. Only an advantage from interacting route identity, verified deletion and readiness survives; checking all three with a larger budget does not count.
- **Cheapest first test:** Enumerate a blinded set of small games and compare equal-budget stack, graph recomputation, and offline/online oracles. Reject any false bound; report tightening, verified nontrivial windows, and all computation, including refusals.
- **Old-task retention check:** Compare full A/C retention trajectories at the same B target, including fallback paths and rare old slices.

## Ranked deeper questions

1. **Can ordinary B SGD certify a useful deletion-only graph in a shared-feature learner without modifying B?** Start with #01–#03 and #09: verify finite transitions over held-out lawful minibatches, actively try to reopen a route, and demand an exact teaching-cost separation at matched dormancy and old margins. If monotonicity holds only in a tiny manually gated corner, do not generalize the theorem.
2. **Is there an actionable window when old performance gives no timing signal?** Use #12/#13/#21. Find paired matched-loss streams with different feasibility windows and a truthful readiness witness on the right route. Beat the stacked controls without a manufactured cliff or concede the earlier deadline null.
3. **Can the abstract graph charge shared routes tightly without simulating the whole teaching game?** Use #02/#05/#06/#10. Count proof work, memory, and failed certificates against full recomputation and exact planning. Reject a cheap abstraction if it double-spends or never improves the scalar bound.
4. **Which timings are certified online when the B suffix and demand are unknown?** Use #14/#15/#18/#22. Separate an anytime safe witness from hindsight-only feasibility; charge for reservations and fallback, and test a case where no online policy can match hindsight.

**Verdict:** Keep both seeds conditional. A deletion-only upper graph counts shared teaching only if its capacities cannot be double-spent or refilled for free; an earlier replay slot needs its own on-route readiness witness, not merely a nonzero upper bound. The first decision is whether those proofs are nonvacuous in a small learner with plain B SGD, independent old-task reads, and no imposed cliff.
