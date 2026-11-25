# Work–memory folds: price the slot, replay the batches that made it smaller

**Status:** Ideas only; no pilots, training runs, or GPU work. **Parent:** [Work-earned fold-backs](work-earned-folds.md) ([PR #259](https://github.com/manojbajaj95/cl/pull/259)). **Review seed:** [Flood triage, row 374](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md#L374), score-3 cards #12 (trade C batches for carried optimizer bytes at a preset price) and #20 (use those batches' own gradients as replayable evidence of the fold).

**Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md). State an actual discrete transition, not a gradient-flow invariant (Noether-memory kill). A tied save/restore or an equality built into a toy is not a result. Cheap audits must beat direct checks at equal resources, and the two seeds together must beat the stacked control. **P** means a candidate reusable operation; **I** means an improvement or falsifier. Neither means the novelty has been established.

## What would be new?

The question is whether required C work can pay down **both** the state the learner needs to carry and the evidence an independent verifier needs to check. The price curve and the receipt are the parent's proposals; the extension is to make **proof availability a condition of buying a point on the curve**, then look for a point neither standalone technique can buy.

- [Minimal sufficient fold state](https://github.com/manojbajaj95/cl/blob/devin/1795565523-minimal-fold-state/tree/minimal-fold-state.md) and exact lumpability already say which histories an exact decoder may merge. [Guarded Compression of Adam State](https://www.alphaxiv.org/abs/2611.00589) bounds update error at a fixed restore, and [proximity-regularized continual LoRA merging](https://www.alphaxiv.org/abs/2609.32332) makes a future merge easier. The proposed trade is to change the reachable optimizer states through required work so that **fewer distinctions are needed at zero update error**, not to tolerate more compression error.
- [Proof-of-Learning](https://arxiv.org/abs/2103.05633) already checks training with checkpoint replay, including selective checks. [Check-as-work](https://github.com/manojbajaj95/cl/blob/devin/1795565485-check-as-work/tree/check-as-work.md) already asks a useful batch to do checking. A shorter log is not new by itself: the claim here is that a fold-specific receipt reused from required updates proves the *erasure of distinctions*, including the ones later readers can expose, more cheaply than the best separate fold audit.

## Contract

- Before seeing results, pin host, split, encoder/decoder and fold family, arithmetic and RNG, eligible causal C scheduling policies, batch identity and order commitments, and what counts as one standardized batch. Use only required, truthfully labeled C examples. Compare allocations of the same total C work: `k` counts the required batches run wide before folding; any suffix must still be served and, if legal, can run narrow. If a suffix or another reader needs discarded state, include it in the post-fold update class U or refuse that cut. Fix U, domain, reader deadlines, and horizon (or require an inductive closure proof). Fix A retention floors, B retention and C utility floors at matched service milestones.
- For each k compute the smallest **worst-case serialized** carried optimizer payload M over the reachable admitted states at that cut: a lower bound from future-distinguishable classes and an upper bound from a fixed lawful narrow decoder. Include headers, padding, counters and any history-dependent information the learner can read (even in weights or remote logs); distinguish slot payload from actual resident allocation. With equal current outputs, distinct classes must be separated by some word in U within the declared horizon. An abstract partition is not a feasible point without a decoder and the same outputs and optimizer transitions through that horizon.
- Publish a single frontier of `(k, M, width released, worst A drift)` for exact, retention-feasible points, and label proof costs, refusals and any unproved lower bounds. Fix a price λ (bytes per pre-fold batch; e.g., 3/4 in the paper check) before seeing the traces. Among points meeting a fixed width target, deadline and proof budgets, minimize `M + λk`; break ties toward earlier cuts, then by predeclared policy order. Show the unfiltered diagnostics too; do not move λ or weaken U to rescue a result. Report peak bytes, width-steps, and a later writer that actually uses released capacity. Deny credit for merely deleting a field or moving it off-device.
- Make the receipt start from a trusted or independently verified commitment to the entering state, not a learner-chosen checkpoint. Bind the actual C records (or a verifiable immutable source), order, masks, seeds, precision and optimizer config. Publish the claimed gradient or a commitment to it, plus the echo after each required batch in the pre-fold prefix; bind the fold and the terminal state. The verifier recomputes each claimed transition from its inputs, checks the linked echo claims and the fold map, then separately checks a closure certificate for U. A signed gradient, hash or matching endpoint alone proves neither that the gradient came from the committed batch nor that future readers agree. If a member of the prefix is skipped without a verified summary of its effect, refuse.
- The prover reuses the real forward/backward work; the verifier still pays for replay. Itemize prover instrumentation and hashing, verifier work and latency, peak checkpoint memory, receipt bytes and lifetime, and any extra old-task evaluation. Keep offline evidence outside M only if the learner cannot read it, and count it separately under a fixed evidence budget. Check A/B/C at entry, at the cut, after the first sensitive reader, and over the declared continuation; a proof that wide and narrow forget equally is a failure.
- **Controls:** fixed-k MRS11; zero-work minimal slot ([PR #239](https://github.com/manojbajaj95/cl/pull/239)); slot reset; equal-byte low-rank/quantized optimizer state (report its exact error); a host whose slot never shrinks; full-run replay; a separate fold audit at equal compute; and a trusted, unverified fold as the cost floor only. The stacked control is the best causal C prefix plus lawful state compression/transport and an independent fold audit, with the same C data, width-steps, information, evidence budgets and guarantees. Also force a late reader to see an echo hidden by a skipped record.

## One exact paper check (not a learner result)

Use a two-slot transition model. At entry, `hᵢ = mᵢ ∈ {0,…,255}` independently for i=1,2; h is a private weight and m is its momentum. Required Cᵢ trains only slot i (the other clock is frozen) with loss `hᵢ²/4 + (w−1)²/2`. With unit step, momentum 1/2 on h and plain SGD on the shared w, `gᵢ = hᵢ/2`, `mᵢ′ = mᵢ/2 − gᵢ = 0`, `hᵢ′ = hᵢ + mᵢ′`, and `w′ = 1` from entry w=0. Each C record is used once; the order is C₁ then C₂. U here is an abstract finite reader/transition model, not a claim about Adam: a reader can expose either signed update contribution `mᵢ/2` before the corresponding remaining Cᵢ, only the remaining C records act on h, and after Cᵢ no continuation reads hᵢ. Thus the narrow map may reconstruct `hᵢ=mᵢ` when it needs to run an unserved Cᵢ and may discard hᵢ once that record is served.

| k | Distinguishable states at fixed visible w | Minimal payload M | A drift for probe w/8 | M + (3/4)k |
|---:|---:|---:|---:|---:|
| 0 | 65,536 | 2 bytes | 0 | 2 |
| 1 | 256 | 1 byte | 1/8 | 7/4 |
| 2 | 1 | 0 bytes | 1/8 | 3/2 |

The reader distinguishes each unsatisfied slot value; packing those values hits the counting bound for fixed-size payloads, with public cut and schema. For a paper-only A drift cap of 1/8, including after serving the remaining C records, the price picks k=2 if all three cuts meet the same abstract width target and evidence cap. With a one-wide-batch deadline k=1 wins instead. If a claimant omits C₂, entry `m₂=2` still contributes 1 to the next reader, even if w and the first echo agree. Replay can catch the omission; replay does not establish the reader theorem. There is no measured physical width gain here, and the public schema, known clocks and trusted starting state are doing work. On a host where every C transition is injective on the future-distinguishable classes, the same counting argument predicts **no payload savings** at any price.

## Idea cards

### 01. Buy a certified cut at a posted exchange rate (P; seed #12)
- **Mechanism:** Use the exact frontier and charge λ for every C batch run wide; a cut can spend less memory only if all remaining readers and C service still fit.
- **Novelty vs nearest prior art:** Restates #259 #12. Unlike fixed-state guarded compression, the optimizer gets a smaller admissible state space rather than an error allowance.
- **Cheapest first test:** Enumerate the paper frontier, then swap in injective C transitions; fixed-k MRS11, no-work minimal slot, equal-byte codec and reset should expose any bookkeeping-only gain.
- **Old-task retention check:** Gate the entire A trace and show worst drift at each candidate, not just the winning cut.

### 02. Make a state-erasure receipt out of the C prefix (P; seed #20)
- **Mechanism:** Link each actual gradient and resulting echo to the preceding committed state, then replay the prefix and validate the fold and closure relation.
- **Novelty vs nearest prior art:** Restates #259 #20; Proof-of-Learning already replays training. The target is an exact fold claim, not provenance for the full run.
- **Cheapest first test:** Omit C₂ in the paper check; compare full replay, independent audit, unverified fold and the late reader at equal claimed assurance where applicable.
- **Old-task retention check:** Evaluate A independently at replayed states, not by accepting a signed A score.

### 03. Give each price point a matching impossibility witness (P)
- **Mechanism:** Attach a lawful decoder above the point and an adversarial family of histories separated by U below it; bound both bytes and the minimum number of required records to get there.
- **Novelty vs nearest prior art:** #239's indistinguishability witness is static. This is a lower bound against every eligible causal policy up to a given cost, not just one bad codec.
- **Cheapest first test:** Enumerate two records and a branch in a four-state finite optimizer; certify or disprove “one record cannot erase one byte.”
- **Old-task retention check:** Do not use histories excluded by the precommitted A floors to inflate the bound.

### 04. Lock a price policy before the arrival order is known (I)
- **Mechanism:** Publish λ and an online stopping rule based on certified offers, then compare its choices with an offline exact envelope on withheld arrival orders.
- **Novelty vs nearest prior art:** An online stopping problem, not a new optimizer. Improvement requires a large reduction in wasted wide work over a fixed cut, not oracle scheduling.
- **Cheapest first test:** Enumerate three arrivals with the same multiset but different deadlines and report the gap to the oracle.
- **Old-task retention check:** Include A drift accumulated while an offer is delayed or refused.

### 05. Price only the byte that really leaves (I)
- **Mechanism:** Demand that the smaller quotient frees an allocatable slot or aligned block that a later writer consumes; charge any compaction copies.
- **Novelty vs nearest prior art:** Standard allocator accounting; useful only if it overturns a payload-based ranking.
- **Cheapest first test:** Compare 17→16 and 16→15 payload bytes under 16-byte allocation and issue an identical later write.
- **Old-task retention check:** Re-evaluate A after allocator reuse so stale aliases cannot masquerade as retained memory.

### 06. Keep slot side information out of the price loophole (P)
- **Mechanism:** Use a genuinely shared, fixed decoder and an explicit table of readable side channels; recompute the lower bound conditioned on public information and bill all state-dependent reads.
- **Novelty vs nearest prior art:** Conditional coding is classical. The proposed operation is an erasure certificate that becomes invalid if a proof log becomes optimizer-readable.
- **Cheapest first test:** Encode a lost bit in a schema choice, then in a public C record ID. Show the footprint bound changes only when the bit is freely common or paid for.
- **Old-task retention check:** Re-run A with receipt storage disconnected from the learner.

### 07. Spend A's available margin only where it buys a discrete deletion (P)
- **Mechanism:** Admit a causal C route only if an A-safe prefix crosses a provable class-collapse boundary before the deadline; refuse near-misses regardless of echo norm.
- **Novelty vs nearest prior art:** GEM constrains interference and #259 uses a retention-constrained fold. The additional decision is an all-or-nothing byte purchase backed by reader distinguishability.
- **Cheapest first test:** Compare two real quadratic C orders with matched terminal C utility and A headroom; one reduces an echo but preserves all classes.
- **Old-task retention check:** Match A margins before scheduling and check every prefix for transient breaches.

### 08. Make the same paid-for cut serve more than one future route (P)
- **Mechanism:** Compute a joint quotient across all declared possible successor routes and fold without a route tag only when that slot fits.
- **Novelty vs nearest prior art:** Classical multiple-input lumpability; unlike best-route pruning, the schedule must erase distinctions for the union of readers, not predict which reader will arrive.
- **Cheapest first test:** Two U branches read opposite slots; compare joint folding against a paid route tag plus two decoders.
- **Old-task retention check:** Test A under both branches, including the less likely continuation.

### 09. Use a first-revealing word to veto a misleading price drop (P)
- **Mechanism:** Search the exact future-reader graph for the shortest word separating states the new codec would merge and attach that word to rejected offers.
- **Novelty vs nearest prior art:** Partition refinement already provides distinguishing words. Here the counterexample changes the *priced cut* and may identify which C record is indispensable.
- **Cheapest first test:** A one-step-invisible slot exposed by a two-step clock switch; compare with first-update guarded compression.
- **Old-task retention check:** Include A immediately after the revealing word, not just after the first step.

### 10. Buy state for a known horizon without pretending it lasts forever (P)
- **Mechanism:** Bind a refund to a certified service horizon and a renewal state that does not rely on the discarded bytes; refuse extensions outside that declaration.
- **Novelty vs nearest prior art:** Finite-horizon lumpability and expiring leases are known. The candidate is a width buyback with a lawful expiry and independently priced renewal, not a hidden later restore.
- **Cheapest first test:** A clock makes a deleted slot readable at step three. Compare one two-step lease plus an admissible renewal with retaining the slot throughout.
- **Old-task retention check:** Evaluate A at expiry and after renewal; charge interruptions and refusals.

### 11. Prove the fold before a bad receipt can release capacity (P)
- **Mechanism:** Stage the fold but hold the width reservation until the independent verifier accepts; use an authenticated terminal token to commit the release.
- **Novelty vs nearest prior art:** Staged commit is old. Useful only if the live service can defer acceptance without a second full wide snapshot or missing the reader deadline.
- **Cheapest first test:** Deliver a syntactically valid receipt with an incorrect second echo after a writer requests the returned width. Compare eager release and a full shadow snapshot.
- **Old-task retention check:** Verify A remains on the last lawful state while the receipt is pending or rejected.

### 12. Bind a receipt to lawful minibatch reductions (P)
- **Mechanism:** Commit batch contents, reduction order and masks; verify the logged reduced gradient, not an alternative sequence of per-example optimizer steps.
- **Novelty vs nearest prior art:** Deterministic replay already logs execution details. The proposed fold receipt treats those details as part of the equivalence class and prices their real byte cost.
- **Cheapest first test:** Use one two-example batch with momentum and show that replaying its two gradients as two updates invalidates a claimed deletion.
- **Old-task retention check:** Compare A on the verified batch schedule against the per-example impostor.

### 13. Chain reusable segment receipts only over closed boundaries (P)
- **Mechanism:** Let two fold offers reuse a verified C segment only when its committed end equals the next committed start and all mutable state crossing the boundary is accounted for.
- **Novelty vs nearest prior art:** Checkpoint chaining is standard; the candidate is amortizing verification across rival offers without making any discarded slot readable again.
- **Cheapest first test:** Two offered cuts share the first two C records; inject a different optimizer counter at the join and require rejection.
- **Old-task retention check:** Preserve the worst A prefix across both segments, not their average.

### 14. Use seeds to remove receipt bytes, never to invent evidence (I)
- **Mechanism:** Replace gradient payloads with commitments and regenerate the immutable batches and stochastic masks from a bound manifest; report the full replay bill.
- **Novelty vs nearest prior art:** Seeded replay is standard. Improvement needs a large gain in the priced evidence budget without extra learner-side access or weaker assurance.
- **Cheapest first test:** Compare full gradient payload versus commitment plus reproducible replay on a masked two-coordinate model; mutate RNG on one record.
- **Old-task retention check:** Compare A across independently reconstructed traces before allowing the smaller receipt.

### 15. Let a segment summary earn a skipped replay only by proving equivalence (P)
- **Mechanism:** Replace a logged block with a checked exact composition on the admitted incoming set, including each possible intermediate reader effect. Treat an unsupported skipped batch as rejection.
- **Novelty vs nearest prior art:** Compositional verification is known; narrower claim is that the same truthful batches can both simplify the continuation quotient and admit a cheaper proof of their own composed effect.
- **Cheapest first test:** Compose two affine momentum maps; then add an intermediate clip decision only the first state can see and require a stronger summary or replay.
- **Old-task retention check:** Check A at internal reader boundaries even if the shortcut reproduces the final state.

### 16. Share work across candidate cuts without unsealing the evidence (P)
- **Mechanism:** Build multiple decoder certificates against one immutable replay stream; compute offers from the same verified states and charge any separate branch compute.
- **Novelty vs nearest prior art:** Shared prefixes in search are standard. Test whether evidence reuse changes which *exact* point fits the proof budget, beyond cached standalone audits.
- **Cheapest first test:** Three cuts share a prefix; compare against a cached independent auditor, not three redundant full replays.
- **Old-task retention check:** Apply the same A panel before selection at every cut and hold out a second panel to detect selection on noise.

### 17. Use a denial receipt when real work cannot buy a byte (P)
- **Mechanism:** Certify that each available C action maps the relevant reachable distinctions injectively and that U still separates their images; keep width or transport state without searching farther.
- **Novelty vs nearest prior art:** No-refund is already in minimal-fold-state; this is a reusable obstruction over a family of lawful work schedules, including equal-gradient decay that never reaches zero at exact arithmetic.
- **Cheapest first test:** Rational nonzero momentum decay, then finite-precision rounding; check the denial fails precisely when two distinct admissible values collide.
- **Old-task retention check:** Include an A-safe host with no savings so refusal cannot be attributed to A failure.

### 18. Show which clock erases a byte and which clock merely hides it (P)
- **Mechanism:** Treat the optimizer counter and the verification cut as part of U. Charge a clock slot if any later lawful clock change exposes different bias correction, even after equal moment values.
- **Novelty vs nearest prior art:** #259 includes counters in the echo; the extension is to partition by future clock transitions and ask if required C work can synchronize them cheaply enough to change the chosen cut.
- **Cheapest first test:** Enumerate two bias counters and a fixed nonzero moment, first with no counter reader, then with a permitted group restart.
- **Old-task retention check:** Check A after the restart and at matched C service, including the dormant slot arm.

### 19. Turn a bad fold into a small independently reproducible dispute (P)
- **Mechanism:** Once a linked prefix has been independently verified, produce the first bad transition or a U word the decoder fails on, so a challenger can specify which claim breaks.
- **Novelty vs nearest prior art:** Fraud proofs and Proof-of-Learning already localize bad updates. Here the disputed object can be a closed continuation class even when *all training steps are correct*.
- **Cheapest first test:** Make one receipt with a substituted gradient and one with correct gradients but an invalid codec; require different counterexamples.
- **Old-task retention check:** Attach the earliest independently observed A breach when the class mismatch affects A.

### 20. Limit receipts to declared readers without publishing raw gradients (P)
- **Mechanism:** Log commitments publicly and replay in an authorized audit boundary; give the learner no receipt lookup and account for access-control and verifier storage costs. Treat unauditable batch provenance as refusal.
- **Novelty vs nearest prior art:** Gated verifiable training is not new; the interaction is that moving state into a proof must not restore learner information or erase the apparent savings on the audit side.
- **Cheapest first test:** Use toy private C records and compare full-gradient publication with commitments plus authorized replay when a slot is inferable from the transcript.
- **Old-task retention check:** Verify unchanged A without raw-log access and do not disclose raw A probes in the public receipt.

### 21. Make the price decision pay for verifier congestion (P)
- **Mechanism:** Keep λ fixed but require the receipt to fit a predeclared verifier queue budget before a cut is eligible. Reserve and release verifier capacity along with the wide reservation.
- **Novelty vs nearest prior art:** Admission control is classical. The candidate is a coupled work/slot offer where a cheap decoder is unusable if receipt checking misses the first reader.
- **Cheapest first test:** Two learners offer a small late cut and a larger early cut; a single CPU verifier makes only one combination meet deadlines. Match against independent audit with the same reservation policy.
- **Old-task retention check:** Measure A during verification delay and under the other learner's admissible interleaving.

### 22. Try to kill the two-seed interaction with the full stack (I)
- **Mechanism:** Hold service, width-steps, retained information, A/B/C gates and proof assurance fixed; require the joint offer to buy a cut neither an exact compressor after causal C nor a cached separate audit can buy when stacked.
- **Novelty vs nearest prior art:** An audit, not a primitive. If the independent verifier can reuse exactly the same records at the same charged cost, the combined proposal is accounting around known parts.
- **Cheapest first test:** Enumerate a small momentum host with both a class-collapsing and an injective C route, a late reader, and a fixed proof cap; compare the selected offer and an actual later write.
- **Old-task retention check:** Report worst paired A drift over all service milestones, plus refusal counts; do not credit matching a forgetting wide reference.

## Ranked deeper questions

1. **Does any exact, retention-feasible price point beat the stacked control?** Start with 01, 03, 05 and 22. Require real reusable width and a nontrivial slot decrease under a preset λ. If an ordinary C prefix plus exact transport and a separate audit buys the same point, keep the curve as measurement, not as a new learning operation.
2. **Can batch-derived evidence establish deletion against late readers with less total work than a separate audit?** Use 02, 09, 15 and 19. Separate trace validity from closure validity; inject a skipped late echo and compare equivalent assurance, including replay and old-task checks.
3. **When is the lower envelope flat even with useful C work?** Use 03, 17 and 18. Classify when finite-step momentum or Adam forces distinguishable continuation classes to persist, and contrast exact-arithmetic persistence with lawful rounding collisions and clock changes.
4. **Does the gain survive accounting for proof storage and time?** Use 06, 13, 16 and 21. Move nothing into a free, readable log; check whether a reusable receipt admits an otherwise impossible cut without exceeding evidence or latency caps.

**Verdict:** Keep both score-3 seeds conditional. Posting a price makes the trade falsifiable; replaying C can authenticate the prefix but cannot replace a continuation certificate. The joint primitive earns its name only if the same truthful work buys a smaller lawful slot and cheaper evidence than the stacked control, before the first sensitive reader and without sacrificing A, B or C.
