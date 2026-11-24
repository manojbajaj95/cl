# Self-replenishing capacity

**Status:** Ideas only; no experiments, code, or GPU. **Parent:** [Accommodation games](accommodation-games.md) ([PR #167](https://github.com/manojbajaj95/cl/pull/167)), cards 06 and 09. **Review seed:** [Flood triage row 266](https://github.com/manojbajaj95/cl/blob/2d4ed8254dbc15802fb65dbf9c34332f36569d06/reviews/flood-triage.md#L266) kept two directions at 3: a costed re-buffer that restores dormant thresholds without changing outputs and a certified frontier that leaves different directions open to later editors. Grading follows the [idea ledger](https://github.com/manojbajaj95/cl/blob/2d4ed8254dbc15802fb65dbf9c34332f36569d06/reviews/idea-ledger.md). The ledger closed Gramian and forecast-based write selection: in the [retention-matched rerun](https://github.com/manojbajaj95/cl/pull/21), the spread fell to 0.09 absolute MSE points and missed the gate. This node does not revive a next-task-gain score. It asks whether a concrete intervention restores an independently verifiable opportunity to make useful edits at the same retention.

**Is a learner that regenerates its own plasticity reserve a new object for continual learning?** Not simply because it recycles neurons, lands in an invariant set, or exposes a Pareto set. [Continual backprop](https://arxiv.org/abs/2306.13812) and [ReDo](https://arxiv.org/abs/2302.12902) already recycle units; [shrink-and-perturb](https://arxiv.org/abs/1910.08475) counters warm-start degradation; [Net2Net](https://arxiv.org/abs/1511.05641) transports a function to new parameters; [HJ reachability](https://arxiv.org/abs/1709.07523) and [control barrier functions](https://arxiv.org/abs/1903.11199) cover the safety object. The conditional CL candidate is a **reusable renewal operation**: a learner pays to move capacity within a fixed host, certifies unchanged installed outputs during renewal, and hands a later blind editor a choice of versions that make different certified continuations possible. If ordinary function-preserving reparameterization plus the same-action invariant planner and verifier matches useful admission and total cost, call it an improvement, not a new primitive.

## What gets renewed?

Let a host state include weights, optimizer slots if used, protection obligations, and the metadata needed to tell which reserve is free. A protected task has an acquisition-anchored floor on a declared domain (including ordinary inputs and rare slices). A re-buffer moves reserve between hidden slots or merges redundant carriers to free a slot. It must prove equality of installed outputs on those domains **across the re-buffer itself**, not just keep aggregate accuracy flat; foreign edits may change outputs subject to their own utility and retention checks. Define a directional reserve by the set of *useful* frozen payloads that can be served safely from a state with the declared moves and budget. It is not the number of inactive units, a norm, or a Gramian. Freeze the payloads, utility tests, and their addressing semantics before training B or publishing a frontier. Count only payloads that improve their declared objective against a no-write control, not idles, refusals, or edits undone by repair.

For a fixed future task contract, let `S` contain the acquisition floors and physical resource limits. The reusable round contract is:

```text
Pre(X) = { s ∈ S : ∀ e ∈ T(s), ∃ a ∈ M(s,e) :
                   a(e(s)) ∈ X, e's utility survives, and all costs fit }
Win_∞  = greatest fixed point of Pre
```

`T` comes from an external, precommitted workload, not a host-selected subset; if a request cannot be handled, that is a failure of the advertised universal contract. `M` includes the re-buffer and is identical across comparable guards, repairs, and planners. In the finite toy, iterate from `S` to a fixed point or check a nonempty inductive subset `I ⊆ Pre(I)`. Train B for B utility with an entry objective for that set and certify the resulting host independently. Six rounds are a useful smoke test, not evidence of infinity. A per-round budget allows ongoing payment; a lifetime budget must be in the state and cannot fund a positive-cost renewal forever. Atomic staging checks every published state; live operation checks any edit or renewal intermediate that serves traffic. No claim for arbitrary growing, incompatible obligations at fixed capacity.

A frontier stores certified descendants of one host version, not concurrent serving copies. Each entry records its exact protected scope, directional continuation, cost, and any proof dependencies. An editor discloses a type or presents a frozen payload; the host selects and verifies one compatible branch before committing. Charge peak bytes (including staged deltas and proofs), verifier calls, and selection and reconstruction cost. Dominance is scope- and horizon-dependent: a superset of one-step offers need not dominate for repeated edits. Stale descendants cannot be selected without revalidation or an explicit transport proof.

### Two paper checks before any pilot

1. **A reversible transfer can renew a useful transition, but only under explicit assumptions.** Let a rare old slice read `1 − ReLU(−q)`, with floor 1, and let `p` be a donor threshold on a hidden slot with zero outgoing weights to the protected heads. Fix `q+p=1`; the starting split is `(1/2,1/2)`. In this toy transition abstraction, a frozen payload moves `1/4` from `q` to `p` as a collateral update and does useful work on a separate readout. Without replenishment the first two edits leave outputs intact but the third violates the floor. A fixed cost-1 re-buffer transfers `1/4` back immediately after each edit; both thresholds are nonnegative, the old output remains 1, and the re-buffer does not touch the useful readout. The original split is inductive **if** the useful readout stays inside its own finite, recurrent contract and the per-round budget pays 1. This is a threshold-geometry witness, not proof that arbitrary new labels can be accumulated indefinitely or that a learned policy beats an exact solver. In an implementation the donor must be checked against every protected readout, and the useful readout must be audited rather than assumed.
2. **Equal-output descendants can leave disjoint room.** Two old slices read `1 − ReLU(−q_u)` and `1 − ReLU(−q_v)`, both with floor 1. With `q_u+q_v=1/2`, descendants `(1/2,0)` and `(0,1/2)` agree on both slices and may share the same useful B head. Frozen payload `u` debits `q_u` by `1/2`; `v` debits `q_v` by `1/2`. If no transfer can serve between disclosure and the debit (e.g. a live floor and fixed response deadline), each descendant takes just one direction and the balanced split takes neither. A pre-certified two-state frontier can select after disclosure and before the write. Remove the deadline or give the planner costless pre-write switching and the separation may vanish. Compare storing both deltas to reconstructing both on demand under the same timing, not to a control forbidden to switch.

## Idea cards

### Regenerate, rather than take reserve from another task

#### 01. Re-buffer a dormant threshold out of an unused donor
- **Mechanism:** Shift a quarter-grid bias allowance from a certified unused hidden slot to a gate eroded by a frozen editor; verify output equality across the shift and train B to leave both the donor and the gate inside an inductive region.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [ReDo](https://arxiv.org/abs/2302.12902) recycles dormant units and [Net2Net](https://arxiv.org/abs/1511.05641) preserves functions across transformations. Here the deliverable is a priced output-preserving transfer that restores service to a named future edit family on the same-width host.
- **Cheapest first test:** Extend Paper Check 1 to a four-unit ReLU host with six frozen, utility-tested requests. Compare ordinary B training plus the same re-buffer, `Win_2`-trained B, periodic replay, and frozen expansion under matched capacity and compute; enumerate the toy fixed point separately.
- **Old-task retention check:** Check A/C, B, and all still-protected installations on ordinary and rare domains after each edit, plus equality on those domains before and after each transfer.

#### 02. Distill two live carriers into one and use the freed slot
- **Mechanism:** Train B so two redundant carriers compute exactly the same function on the declared domain. Sum their outgoing weights into one, zero the other, then allocate its threshold to a different edit direction.
- **Novelty vs nearest prior art — IMPROVEMENT:** This is an inverse [Net2Net](https://arxiv.org/abs/1511.05641) split followed by [PackNet](https://arxiv.org/abs/1711.05769)-style reuse. Test whether deliberate duplicate formation gives a useful, certifiable reclamation schedule rather than claiming the merge as new.
- **Cheapest first test:** Use a two-carrier ReLU pair and a held-out task that needs one slot. Compare exact merge, prune-and-retrain, and hard reservation on equal width, including a near-duplicate that must not merge.
- **Old-task retention check:** Prove equality on A/C/B across the merge and verify those tasks again after the freed slot is reused, including an input where the near-duplicate differs.

#### 03. Renew a pair of cancelling units into two different opening directions
- **Mechanism:** Find two hidden functions with equal activations and opposite outgoing coefficients on protected inputs. Remove their cancellation pair atomically and reposition their gates for two independent future edits.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [Orthogonal Gradient Descent](https://arxiv.org/abs/1910.07104) protects first-order behavior and Net2Net gives exact transformations. The proposed gain is reclaiming directional room from *jointly* null finite moves when neither carrier can be recycled independently.
- **Cheapest first test:** Enumerate a three-unit ReLU host with a cancelling pair; compare pair-aware recycling, unit-utility recycling, and exact joint [APRNN](https://arxiv.org/abs/2304.03496) with the same move budget.
- **Old-task retention check:** Verify A/C and B including gate crossings, reject either solo removal, and test equality after joint renewal followed by each frozen edit's retention check.

#### 04. Renew without paying permanent donor debt
- **Mechanism:** Keep a paired ledger of reserve debits and outstanding obligations. Require a closed return cycle that restores the donor too, not just the recipient; discharged temporary debt may never be hidden in a cache or an unprotected head.
- **Novelty vs nearest prior art — IMPROVEMENT:** [HJ reachability](https://arxiv.org/abs/1709.07523) already allows augmented resource states. This is an audit of whether recycling buys recurrence rather than consuming a second finite reservoir.
- **Cheapest first test:** Compare a counterexample with irreversible donor loss to the reversible transfer in Paper Check 1. Check cycle coverage for every externally fixed request type, not just one easy cycle.
- **Old-task retention check:** Verify A/C/B and live installations through both cycles or until honest rejection; check that no task, floor, or donor liability is removed to close the loop.

#### 05. Learn invariant entry while B still has freedom to choose
- **Mechanism:** Give B an induction-violation counterexample curriculum: when a candidate is unsafe for a frozen editor and no paid re-buffer works, train on that failure and recheck entry into a separately certified set.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [InterContiNet](https://arxiv.org/abs/2206.07996) learns within weight intervals and [control barrier functions](https://arxiv.org/abs/1903.11199) enforce invariant sets. The CL test is whether learning ordinary B constructs renewable entry states that online planning cannot cheaply recover from equally useful B fits.
- **Cheapest first test:** Find two equal-output B optima on a quarter-grid ReLU host; train with and without counterexamples, then apply the same exact fixed-point planner and `M` to both on held-out payload banks.
- **Old-task retention check:** Require the same A/C and B floors at entry and after every admitted continuation; keep training counterexamples separate from withheld normal and rare inputs.

#### 06. Test fixed-width renewal against growth from preallocated slots
- **Mechanism:** Attempt repeated merge-and-reuse when only `n` carriers can be live; let the control reserve the same `n` positions for frozen per-task modules instead of adding width at test time.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Progressive Neural Networks](https://arxiv.org/abs/1606.04671) prevent interference by expansion and PackNet by staged packing. This compares recycling against a strong preallocated baseline, not free growth against fixed width.
- **Cheapest first test:** Cycle through three compatible edit types on a four-unit host; compare renewal, frozen expansion capped at four active-or-reserved units, and PackNet-style allocation with equal peak bytes and work.
- **Old-task retention check:** Report every protected task at every acquisition checkpoint, even once expansion fills all slots; do not count an overwritten task as retained.

#### 07. Make gain invariant to the parameter ruler
- **Mechanism:** Bind each payload to a canonical slot/address convention or transport it before freezing across positive ReLU rescalings. Count restored external task utility, not raw bias distance.
- **Novelty vs nearest prior art — IMPROVEMENT:** Function-preserving transformations such as [Net2Net](https://arxiv.org/abs/1511.05641) already change the parameter ruler; this audit distinguishes true service to an external editor from unit changes.
- **Cheapest first test:** Duplicate a host with two exact scales and matched transported calibrated payloads; compare threshold magnitude, normalized edit distance, and certified useful admission under the same cost units.
- **Old-task retention check:** Prove equal A/C/B outputs after rescaling, then verify those outputs or their acquisition floors as appropriate after each transported payload.

#### 08. Re-buffer optimizer slots as well as weights
- **Mechanism:** Pair a weight-preserving gate transfer with a declared transform or reset of the donor's momentum and second moments; a reactivated unit must not inherit a delayed write that spends the apparent reserve.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Optimizer resetting](https://arxiv.org/abs/2306.17833) already attacks stale state. The useful distinction is whether transporting only the renewal's state dependencies beats resetting everything at equal work and retention.
- **Cheapest first test:** Compare transfer-only, transfer plus full reset, and a slot-local transform on a tiny momentum learner with two frozen follow-up gradient operators.
- **Old-task retention check:** Test A/C and B immediately after transfer and after each of two deterministic optimizer steps, checking rare slices even when the first post-transfer prediction agrees.

### Keep different directions open

#### 09. Publish two certified descendants, not one best buffer score
- **Mechanism:** After a first write, keep two sparse state deltas with equal immediate outputs but complementary safe next payloads. A later editor selects a compatible certified descendant with its frozen payload before atomic commit.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [IBCL](https://arxiv.org/abs/2305.14782) gives model trade-offs over tasks and [mergeable writes (PR #156)](https://github.com/manojbajaj95/cl/pull/156) gives alternatives at write time. This is a frontier at **matched present utility**, over independently editable future directions after a committed edit.
- **Cheapest first test:** Use Paper Check 2 with a check deadline. Compare one myopic state, one minimax-volume state, write-time substitutes, and exact two-step planning on the same moves, disclosure, peak bytes, and checks.
- **Old-task retention check:** Certify A/C/B and the first installation on every stored descendant before offering it; independently audit the selected descendant after the blind write.

#### 10. Keep a common base and certify cheap branching deltas
- **Mechanism:** Factor certified descendants into a shared serving base plus sparse gate deltas; one shared proof discharges unchanged slices and a branch proof covers edited slices.
- **Novelty vs nearest prior art — IMPROVEMENT:** Shared bases and compositional checks such as [Pacti](https://arxiv.org/abs/2303.17751) are known; the question is whether a proof factorization fits more useful alternatives into a given byte and verification budget.
- **Cheapest first test:** Compare a full snapshot frontier, sparse branch deltas with fresh checks, and shared-check deltas for four independent gate slices, including peak reconstruction storage.
- **Old-task retention check:** Compare proof decisions against exact checks on A/C/B and earlier installations for every reconstructed branch; give no credit for a delta stale relative to its base.

#### 11. Dominate only if you can simulate the other branch's continuations
- **Mechanism:** Drop branch X in favor of Y only if each externally useful request from X has a no-dearer response from Y whose successor again dominates, with equal protection and scope.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Alternating simulation is known in control and [contract reasoning](https://arxiv.org/abs/2303.17751); the CL candidate is reducing stored descendants without losing blind edit sequences that one-step set inclusion would silently prune.
- **Cheapest first test:** Construct two finite residual graphs where Y has a larger first menu but cannot renew after u and X can. Compare one-step pruning, depth-two pruning, and exact simulation under equal bytes.
- **Old-task retention check:** Exhaustively verify A/C/B and previous installations along all retained game edges; countercheck a pruned branch's accepted sequences against its alleged simulator.

#### 12. Quote a frontier before seeing payload coordinates
- **Mechanism:** Let the editor disclose one coarse direction type, get a branch commitment, then reveal its frozen payload. Certify the entire type on the selected branch to avoid a promise that works only after inspecting the actual edit.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Pacti](https://arxiv.org/abs/2303.17751) already supports assumption/guarantee interfaces. This measures the privacy and usefulness cost of type-only routing over ordinary payload-conditioned planning.
- **Cheapest first test:** Freeze two types with four payloads each and compare one-bit type routing, no disclosure, and full payload disclosure on equal frontier bytes.
- **Old-task retention check:** Check each payload in each offered type on A/C/B and installed edits, including the worst boundary case, before publishing any type-wide promise.

#### 13. Sell one safe edit separately from repeated access
- **Mechanism:** Publish a one-use offer for a direction that consumes its last buffer, and a repeatable offer only if the next state returns to a checked invariant set. Spend the offers through host-versioned commits.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [HJ reachability](https://arxiv.org/abs/1709.07523) already separates finite and invariant horizons. The proposed interface lets independent editors distinguish a one-off admission from service they can safely request again without running reachability themselves.
- **Cheapest first test:** Present two equal-margin branches with identical next menus, one with a return edge and one without; compare against scalar margins, one-step residual contracts, and exact planner queries.
- **Old-task retention check:** Verify A/C/B across every offered use and all inductive return edges; attempt an extra call on the exhausted branch and require refusal without state change.

#### 14. Reserve compatible options for two independent clients
- **Mechanism:** Record branch incompatibilities when two editors receive simultaneous offers, and expose a pair only if one priced sequence or a common branch can honor both. No independent redemption of contradictory promises.
- **Novelty vs nearest prior art — IMPROVEMENT:** This is relational composition in [Pacti](https://arxiv.org/abs/2303.17751) and the existing write alternatives in [PR #156](https://github.com/manojbajaj95/cl/pull/156); the new test is explicit double-booking of renewable reserve.
- **Cheapest first test:** Give two editors overlapping and disjoint claims on the two gates of Paper Check 2; compare independent quotes, serialized planning, and a pair certificate under equal deadlines.
- **Old-task retention check:** Check A/C/B and the first installed editor in both possible redemption orders; test rollback of the staged second edit if joint certification fails.

#### 15. Carry a frontier through a new retention commitment
- **Mechanism:** Once a blind editor becomes an old task, show which dormant-slot assumptions its new head invalidates. Keep only branches whose renewal certificates still hold, or rebuild only affected proofs.
- **Novelty vs nearest prior art — IMPROVEMENT:** Incremental [architecture-preserving repair](https://arxiv.org/abs/2304.03496) and contract composition are strong controls; tracking a frontier through growing obligations is not automatic certificate reuse.
- **Cheapest first test:** Add one editor whose readout observes a previously spare donor, and one that does not. Compare dependency-keyed invalidation with fresh proof search after both.
- **Old-task retention check:** Check A/C/B and the new retained task on every reused branch, especially where its new head observes donor movement invisible to A/C.

### Find the limits before claiming a primitive

#### 16. Learn from recurring writes without hiding irreversible task growth
- **Mechanism:** Split the workload into genuinely recurrent compatible requests and monotone accumulations of independent labels. Require an invariant proof for the first regime and a checked exhaustion boundary for the second.
- **Novelty vs nearest prior art — IMPROVEMENT:** [PackNet](https://arxiv.org/abs/1711.05769) already exposes finite model capacity; [control barrier functions](https://arxiv.org/abs/1903.11199) do not imply a nonempty invariant set. This prevents an infinite-horizon claim based on quiet forgetting or no-op edits.
- **Cheapest first test:** Fix a finite-precision host and compare recurring utility-tested revision requests on a declared mutable head with an equal-length stream of random binary labels on newly protected independent inputs. Include a packed-label ceiling and count protected obligations.
- **Old-task retention check:** Audit A/C/B and every immutable label; in the revision regime, check the currently installed revision plus the immutable tasks and state explicitly which requests supersede earlier ones.

#### 17. Make the renewal schedule pay for bursts
- **Mechanism:** Model a reserve move as requiring one tick of work and stage requests with bounded arrival bursts. Certify viable joint states of thresholds and workload backlog, rather than proving recurrence with free time between every edit.
- **Novelty vs nearest prior art — IMPROVEMENT:** Resource-augmented [HJ reachability](https://arxiv.org/abs/1709.07523) is the same formal object. Whether proactive gate renewal admits more useful edits before a real deadline is an operational check.
- **Cheapest first test:** Enumerate two arrival patterns with equal total demand but different burst size; compare always-renew, renew-on-debit, and the exact budgeted strategy, all with the same idle slots and deadline.
- **Old-task retention check:** Verify A/C/B and retained edits at each served tick, including when backlog peaks; late requests and unsafe transient states are failures, not free continuations.

#### 18. Separate accidental headroom from a causal regeneration effect
- **Mechanism:** Pair the same post-edit state with a real transfer, a same-cost sham transfer that cannot change either named threshold, and a no-transfer arm. Evaluate identical blind useful payloads without ranking states by a reserve score.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Optimization readiness](https://arxiv.org/abs/2605.09044) is a predictor and the ledger's prior reserve line was killed. This is an intervention control for exact finite admission, not a claim to forecast average next-task gain.
- **Cheapest first test:** Enumerate four paired states on the quarter grid, compare admitted edits and absolute new-task gains, and stop if no real-vs-sham difference survives utility and retention matching.
- **Old-task retention check:** Require identical pre-payload A/C/B outputs in the paired arms and check acquisition floors for all earlier tasks after each payload they admit.

#### 19. Refuse a transfer that is exact on probes but wrong in between
- **Mechanism:** Use a piecewise-linear check over the protected domain to find narrow activation slivers missed by equality probes; require a certificate or abstain.
- **Novelty vs nearest prior art — IMPROVEMENT:** [APRNN](https://arxiv.org/abs/2304.03496) already does provable network repair. This is a falsification test for treating “dormant on examples” as an exact renewal precondition.
- **Cheapest first test:** Plant one triangular ReLU feature between probe points and compare probes, interval abstraction, and exact rational cell enumeration at known cost.
- **Old-task retention check:** Verify the continuum slice as well as ordinary A/C/B inputs, and check that the feature's withheld peak causes renewal refusal rather than silent output drift.

#### 20. Allow the ordinary planner to compile it away
- **Mechanism:** Hand generic fixed-point search the same trained states, move menu, payload interface, disclosed types, and exact verifier. Also try a baseline with established heuristics or [control minimization](https://arxiv.org/abs/2602.04542) to enter a favorable region; bill every offline and online operation.
- **Novelty vs nearest prior art — IMPROVEMENT:** [HJ reachability](https://arxiv.org/abs/1709.07523), [Pacti](https://arxiv.org/abs/2303.17751), and architecture-preserving repair are the compile-away hypothesis, not weaker straw men.
- **Cheapest first test:** Use the same four-unit host to compare renewal and frontier alone, both together, and exact generic synthesis with matched caching. Amortize cost over a sweep of blind requests and report the break-even if any.
- **Old-task retention check:** Run one independent floor and output-equality oracle across arms on A/C/B and every installed obligation; a tie at equal guarantees and cost demotes the proposed primitive.

#### 21. Price the storage lower bound for directions
- **Mechanism:** Create states where `n` independent gate conditions encode an arbitrary binary vector and an editor can ask about any one direction. A standalone exact offer with no host access must distinguish all `2^n` cases; test whether structure yields compression before claiming a compact frontier.
- **Novelty vs nearest prior art — IMPROVEMENT:** This is an indexing bound on exact answers, not a new certification technique; structured contracts such as [Pacti](https://arxiv.org/abs/2303.17751) are the alternative to a table.
- **Cheapest first test:** Enumerate up to six gates and compare bit-packed exact offers, factored offers on structured banks, and bounded host queries. Charge false refusals, bytes, and verification calls separately.
- **Old-task retention check:** For every direction admitted by a compressed offer, check A/C/B and the acquired gate-specific tasks; compressed summaries may abstain, never accept an unsafe direction.

#### 22. Take the frontier away and see what the trained host learned
- **Mechanism:** After B training, retain either only live weights, weights plus a single preferred descendant, or the full frontier. Compare blind edits under the same reconstruction time to see whether B learned renewable geometry or the host is just paying for branching.
- **Novelty vs nearest prior art — IMPROVEMENT:** [IBCL](https://arxiv.org/abs/2305.14782) supports model alternatives, and [Net2Net](https://arxiv.org/abs/1511.05641) supports transport; this is an ablation separating the value of retained alternatives from the value of the state itself.
- **Cheapest first test:** Cross invariant-entry vs ordinary B training with one vs two stored descendants and exact fresh reconstruction. Use the same frozen u/v request traces and match total peak bytes.
- **Old-task retention check:** Start all arms at identical acquisition floors for A/C/B and the first installation; independently verify the selected branches and every revival step at which the host serves.

## Ranked deeper questions

1. **Can a learner enter a nontrivial, paid renewal invariant at fixed width?** Start with cards 01, 04, and 05: show more useful blind edits than `Win_2`, replay, and capped expansion at equal retention, plus a checked inductive subset on the finite host. If generic invariant synthesis on ordinary B fits already gives the same service at the same total cost, do not claim a learned primitive.
2. **Is keeping an equal-output frontier better than keeping one state and planning when an editor arrives?** Start with cards 09–11 and 22. Match deadline, disclosures, memory, moves, and checks against myopic and minimax-volume choices, write-time substitutes, and exact two-step planning. Look for a gain that persists when later editors can choose between *renewable* directions, not just one-use offers.
3. **Which demand and retention contracts make renewal impossible?** Use cards 13, 15–17, and 21 to separate per-round payment from lifetime debt, recurrent requests from growing obligations, and real nontrivial invariants from narrowed edit banks. Publish the first infeasible request sequence rather than average away lost old tasks.
4. **Is the gain really regeneration rather than reset, reparameterization, or better verification?** Run the matched sham, rescaling, cancellation, and compile-away comparisons (cards 03, 07, and 18–20), with ReDo, continual backprop, shrink-and-perturb, and function-preserving reuse as controls. A first-order score or a six-round streak is not a substitute for a checked return and useful blind-edit gain at equal retention.
