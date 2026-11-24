# Leakage leases: spend proof slack without reopening the source

**Status:** Ideas only; no experiments, code, or GPU work. **Parent:** [Certificate entry ports](certificate-entry-ports.md) ([PR #171](https://github.com/manojbajaj95/cl/pull/171)), cards 2 and 4. **Review seed:** [Flood triage row 272](https://github.com/manojbajaj95/cl/blob/f236e3c105b840ad57c145494f36e3a17d7b492e/reviews/flood-triage.md#L272), two score-3 directions: drop a B-carrying coordinate from the proof while the witness ignores it and require a bound before it rejoins; lease each importer a certified budget for leakage over its remaining updates. **Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/f236e3c105b840ad57c145494f36e3a17d7b492e/reviews/idea-ledger.md). Related: [correction classes, PR #169](https://github.com/manojbajaj95/cl/pull/169) and [self-replenishing capacity, PR #170](https://github.com/manojbajaj95/cl/pull/170).

## Is a spendable, transferable proof budget a new object for continual learning?

**Not as a balance, filter, or transferable quota.** [Privacy odometers and filters](https://arxiv.org/abs/1605.08294), [fully adaptive composition](https://arxiv.org/abs/2203.05481), and [privacy budget scheduling](https://www.usenix.org/conference/osdi21/presentation/luo) already track, stop, or allocate cumulative expenditures across adaptive consumers. Their privacy guarantees do not carry over to training dynamics. [Pacti](https://arxiv.org/abs/2303.17751) can express a contract over a remaining balance; [funnel libraries](https://arxiv.org/abs/1601.04037) attach entry tests to preverified regions. In CL, [Certified CL](https://arxiv.org/abs/2407.06697) protects previously established properties during retraining and [CABA](https://arxiv.org/abs/2610.40740) gates candidate commits on a budget for worst-anchor behavioral change. A per-step bound on forgetting is not new either, and [first-order diagnostics can fail outside their validated region](https://arxiv.org/abs/2609.32818).

**Conditional candidate:** the right to spend certified headroom on variation in state that a retired-source replacement proof does not track, *and to pass the unused entitlement plus its inherited obligations to a different learner*. A receiver should be able to continue useful training and reintroduce an omitted coordinate using a local boundary proof, without the retired source or the predecessor's proof trace. The CL-specific claim is that forgetting proof state and transferring spendable headroom work better **together**: more useful blind continuations or less total evidence at the same scope and retention than verified substitution, dynamic abstraction and resource accounting composed conventionally. If that stack gets the same frontier, keep the engineering technique and drop the primitive claim.

### What is leased, spent, and handed off

- **Issue.** The publisher freezes the parent's versioned region, replacement buffer `W`, entry proof, legal transition grammar and horizon `H`. Extend it with the phase-specific projected state, the paired source/replacement relation, a proof of closure and an accounting rule binding charge units to protected outputs and prefix tolerances. An importer proves entry and applicability to the frozen package before receiving a lease. Include optimizer slots, RNG/sampler state, normalization and gates whenever they affect any claimed transition. The bound is on declared substitution discrepancy, not automatically a guarantee of normal task retention.
- **Spend.** In one conservative scalar instance, paired visible error `d_t` satisfies `d_{t+1} ≤ L_t d_t + c_t`, where `c_t ≥ 0` upper-bounds the additional hidden-to-visible discrepancy of the proposed legal update uniformly over its admitted hidden fiber. If `L_t ≤ 1` and `d_0 ≤ r`, every prefix with cumulative certified charge `≤ ε − r` has `d_t ≤ ε`. The publisher must also prove the required tube closure and output bound; an error inequality alone is not closure. If gains exceed one, use an all-prefix weighted bound over the remaining horizon or a certified envelope recurrence; raw charges no longer add safely. Filter **before** a commit (or check a speculative update that cannot become externally visible). An odometer reports liability already incurred; it cannot make an unsafe prefix acceptable.
- **Drop and rejoin.** When the witness stops reading a coordinate, dropping it does not freeze or erase it from either learner. Whole-fiber noninterference can give zero charge; indirect effects through legal updates must otherwise be bounded. Before any reintroduced coordinate can be read, verify a paired boundary relation that is strong enough for the next phase's closure, and charge any extra output discrepancy not already covered. The importer must derive the relation from the frozen package and local evidence, for example by comparing its boundary state against a preverified envelope for the counterfactual source arm. An oracle reading the retired arm is not a local check. Include a deliberately invalid return even though nominal charges fit. Boundary refusal happens before the read and counts against admissions. Neither a favorable sample nor a quiet prefix reestablishes the boundary.
- **Transfer.** Start with two independently authored importers in **one serial continuation** of the same retired-source obligation. Stage two inherits a checked interface state, current discrepancy envelope, outstanding rejoin conditions, remaining horizon and residual entitlement; the spent amount does not reset. Transfer debits the sender for the same scoped entitlement; reject a stale receipt, scope mismatch, or a transfer that strands a live boundary obligation. If units, tolerances, state context, or transition laws differ, require a proved conversion on the overlap or refuse. For *independent* copies, issue separate local bounds: two safe alternative worlds do not consume a conserved joint budget merely because they share a buffer. Splitting or joining matters only for a genuinely shared cap or a certified merge with a specified composition rule.

### Smallest witnesses, on paper

**Variable spend and a real handoff.** One visible error coordinate, one evolving B coordinate, legal charges `.10` or `.35` at steps 1–2, and a `.05` final reserve, with nonexpansive dynamics, zero initial error and cap `.50`. Use an exact scalar positive-coupling recurrence as a sanity check: either mixed order fits (final bound `.50`), both expensive steps do not, and the worst-case fixed allocation that accepts both mixed orders requires `.75`. Release only the first-stage suffix receipt to the second importer, whose continuation is selected independently. Check `.35 → .35` as a refusal, not as an average case. The arithmetic only distinguishes adaptive from fixed allocation; a Pacti contract with the same adaptive ledger should tie. Any primitive case must survive the next witness.

**Actual disappearance and return.** Enumerate a four-update quantized ReLU learner with a shared A/C path and a B-bearing unit. A delayed gate removes the unit from `W`'s read set for two steps; let it still affect B, with one grammar allowing optimizer-mediated weak coupling and a second giving true noninterference. The valid join requires a paired bound on the unit and any relevant slot before the gate admits it. Include a branch whose balance looks fine but whose return violates that relation, and an expansive suffix where the same sum of costs is unsafe. Enumerate both arms for exact ground truth; the published package and the import verifier cannot consult the live source after the cut. Compare one frozen package and handoff to a static union of coordinates, separate order-specific proofs and time-indexed IBP with boundary cost charged. An always-block-diagonal model is only a sanity check, not a useful win.

### Common controls and kill criteria

- **Free, rigid, erased:** Look for the free unshaped corridor with [linear mode connectivity](https://arxiv.org/abs/1912.05671) as a diagnostic, not a guarantee. Plot the freeze/[PackNet](https://arxiv.org/abs/1711.05769)/[GPM](https://arxiv.org/abs/2103.09762)/low-LR/lazy-width frontier, including a later task that needs a formerly shared coordinate. Preserve distinct, useful held-out B behavior where orders call for different outputs; include reset/erase controls. No credit for hiding a gauge, just delaying the same learning, or parking old tasks in uncharged copies.
- **Strongest control gets the same powers:** Compare worst-case static charge, full-state and per-order certificates, [IBP](https://arxiv.org/abs/1810.12715) with time-indexed bounds, Certified CL, and CABA with stated scope (anchor KL is not the substitution theorem). The stacked baseline gets [trajectory-matched buffers](https://arxiv.org/abs/2203.11932), the same checker and legal grammar, time-indexed abstraction with the same boundary proofs, and Pacti with the same adaptive scalar or structured accounting and handoff operations. Also compare matched-byte replay and save/restore, marking source-available arms. Run projection alone, leases alone, both and neither. Do not claim novelty over a fixed quota if the adaptive stack ties.
- **Count scope, cost and truth:** Freeze independent jobs, protected sets, tolerances and cutoff before seeing outcomes; include refusals and report exact missed-safe and admitted-unsafe jobs on the finite toys. Separate publisher/source cost, bytes (including boundary state and receipts), peak overlap, receipt transfer and verification, runtime filtering and fallback. Use original A/C tasks and independent held-out slices, worst prefix and slice, with pre-cut and acquisition references, including immediately before and after rejoin, after real source retirement, and after transfer. Match useful B progress and legal scope. For retention-order claims match example margins; require scope-valid bounds, not proxy calibration; if truth is sampled, check split-half reliability, and replicate surprise-mined effects over at least ten seeds. Kill if retention fails, convenience comes from narrowing jobs, or the equal-budget stack ties. **P** marks a conditional primitive; **I** marks an improvement or audit. All tests below are proposals for CPU or paper work.

## Idea cards

### Rent a smaller proof without freezing the learner

#### 1. Drop a coordinate and make it prove its return (P)
- **Mechanism:** Open an omission interval on a proof-relevant unit when the read gate closes; rejoin only after a local paired certificate checks the unit and any relevant optimizer slots against the next region.
- **Novelty vs nearest prior art:** Time-indexed IBP and funnel composition already do time-local reasoning. The candidate is an independently dischargeable rejoin obligation after carrying no proof trace for the unit.
- **Cheapest first test:** Exhaust the four-update delayed-gate toy against a static union, per-order proof and time-indexed IBP at equal boundary cost. Include a budget-valid, out-of-relation return.
- **Old-task retention check:** Score ordinary A/C one update before, at and after rejoin, and measure B content through the omitted phase; count refusals on the original denominator.

#### 2. Lease an importer the rest of the horizon (P)
- **Mechanism:** Authorize a blind importer to choose costly or cheap legal updates, spending from a source-free certificate for that particular continuation rather than proving every update against the full paired state.
- **Novelty vs nearest prior art:** Privacy filters already implement adaptive spending and CABA already budget-gates behavior. The liability here is hidden-to-visible substitution error under a frozen retired-source witness.
- **Cheapest first test:** Use the scalar mixed-order witness, compare worst-case, Certified CL, full-state enumeration and Pacti carrying the same scalar; count missed and unsound admissions.
- **Old-task retention check:** Put held-out A/C examples on both sides of the certified margin floor; score all prefixes on both orders, especially just before exhaustion and after the cut.

#### 3. Spend on a read path, not on a weight (I)
- **Mechanism:** Separate zero-cost omitted-coordinate changes from charged paths through global clipping, momentum or normalization by proving dependency cuts on the full transition.
- **Novelty vs nearest prior art:** Dependency slicing and OGD constrain or analyze influence. This is a soundness and cost improvement for omitted coordinates, not another primitive.
- **Cheapest first test:** Compare exact bounds to a weight-only mask on a two-slot momentum recurrence, then toggle joint clipping so the same hidden change creates an immediate visible effect.
- **Old-task retention check:** Measure A/C through the first indirect hit and its delayed peak; keep a coupled case in which the mask-only borrower fails.

#### 4. Prepay a future read (P)
- **Mechanism:** Buy a checkable reserve for a future coordinate return, before releasing the remaining balance to B updates. The reserve is coupled to the boundary relation, not permission to skip checking it.
- **Novelty vs nearest prior art:** Scheduled budgets reserve resources and robust funnels have fixed entrances. The proposed operation trades proof obligations between an omitted interval and its returning interface without widening the protected metric.
- **Cheapest first test:** Give a four-step grammar mandatory early or late re-entry chosen by a revealed batch. Compare fixed reserve, adaptive proved reserve and a ledger without reserve against exhaustive viability.
- **Old-task retention check:** Score A/C at both possible arrivals and the latest post-arrival prefix; record whether reserving the transition keeps both B jobs viable.

#### 5. Return a relation instead of a coordinate history (P)
- **Mechanism:** An importer proves agreement within a relational band at rejoin using a local summary of its updates; `W` need not know which hidden paths led there.
- **Novelty vs nearest prior art:** Relational abstract domains and parent entry ports already check relations. The candidate is a return receipt that can be replaced independently of the long-interval substitution proof.
- **Cheapest first test:** Compare one shared paired-difference interval, separate IBP boxes and exact path receipts when hidden values are far apart across jobs but close between arms within each job. Charge all summary bytes.
- **Old-task retention check:** At equal B outcomes score held-out A/C for opposite extremes of the shared band; add a pair whose same marginal bounds conceal too large a difference.

#### 6. Omit, then tighten only on demand (I)
- **Mechanism:** Start with a cheap coarse bound, ask for one stronger local constraint when admission would fail, and retain the refinement only for the phase that needs it.
- **Novelty vs nearest prior art:** Counterexample-guided abstraction refinement already tightens coarse domains. The improvement is avoiding paying for precision in phases where the learner does not need it.
- **Cheapest first test:** Give the delayed-gate toy one spurious and one real counterexample; compare one local refinement with eager full-state verification and interval-only refusal at equal checker effort.
- **Old-task retention check:** Score A/C for newly admitted prefixes and the first true counterexample; distinguish spurious refusal from actual loss of retention.

### Make the remaining budget survive a change of learner

#### 7. Pass the residual right, not a fresh tolerance (P)
- **Mechanism:** Bind a handoff receipt to the terminal interface state, discrepancy envelope, outstanding returns and residual balance. A second learner checks only that its law consumes that receipt soundly.
- **Novelty vs nearest prior art:** Pacti and privacy budget scheduling can express balances. The candidate is a source-free continuation of a nonlinear replacement obligation across independently constructed learners, at lower total cost than their composition.
- **Cheapest first test:** Publish before an independent second B grammar is revealed; compare pass-by-receipt, full recertification, nontransferable quotas and adaptive Pacti. Plant a stale receipt and an attempted reset.
- **Old-task retention check:** Measure A/C just before and after transfer and after the second learner's full suffix, with the retired source unavailable to both importers.

#### 8. Prove an exchange rate between leakage units (P)
- **Mechanism:** Convert a lease on paired representation drift into a lease on logit-margin drift only on a certified overlap, including already incurred discrepancy and remaining gains.
- **Novelty vs nearest prior art:** Lipschitz/IBP certificates already map perturbations, and Pacti translates interfaces. The new-operation claim is preservation of a usable residual right under a typed conversion without replaying predecessor updates.
- **Cheapest first test:** Use two linear readouts and a piecewise-linear gate; compare the local rate, global spectral rate and exact recertification. Include a receiver that exits the overlap on the next update.
- **Old-task retention check:** Margin-match protected A/C points and compare the worst slice at equal B progress, especially examples whose active readout differs across the overlap.

#### 9. Split rights only when branches will actually meet (P)
- **Mechanism:** Split spend between two learners whose updates must later be merged into one model, reserving a certified interaction term. For non-merging alternatives, issue independent local leases instead.
- **Novelty vs nearest prior art:** Privacy budget scheduling already allocates across callers; this tests whether learner-specific merge geometry permits composable residual rights rather than a fictitious global pool.
- **Cheapest first test:** Merge paired rank-one linear edits and then two edits sharing a ReLU gate. Compare independent jobs, static caps, linear accounting with a cross-term bound and full merged certification. Include the case where both edits pass alone but fail together.
- **Old-task retention check:** Score A/C on both branches and on the merged model immediately and after one further legal update; retain both B skills after merge.

#### 10. Keep conversion paths from manufacturing slack (I)
- **Mechanism:** Require an A→B→A cycle to preserve or tighten the carried liability only when justified by a state transition; merely changing lease units cannot increase the original spending power.
- **Novelty vs nearest prior art:** Contract refinement and resource accounting already reject inconsistent conversions. This is an audit of typed leases, not a primitive.
- **Cheapest first test:** Enumerate three scopes with overlapping readouts and one tempting inverse Lipschitz conversion in a saturated region; compare common-base accounting to pairwise rates.
- **Old-task retention check:** Score the original A/C tasks after a conversion cycle with and without a new B update; the control must expose false headroom without invoking an actual repair.

#### 11. Hand off the proof without handing off the hidden branch (P)
- **Mechanism:** Move the learner state needed for B and a small boundary statement, but not the trajectory of omitted coordinates or the publisher's proof history; bind the statement to the actual continuation state and package.
- **Novelty vs nearest prior art:** Modular verification and proof caching already avoid trace transfer. The candidate is minimal transition evidence after useful branch divergence, not a privacy guarantee.
- **Cheapest first test:** Enumerate multiple distinct B histories with the same admissible interface and compare bytes and checking work for state-bound receipts versus replaying predecessor proof traces. Try substituting a receipt from a different history with the same visible weights but bad slots.
- **Old-task retention check:** Compare A/C at handoff and after optimizer slots first matter, with matched independently measured B utility and memory.

#### 12. Route a refusal to a lease that can actually cover it (P)
- **Mechanism:** Expose the missing liability (boundary, horizon, or direction); a successor may choose another already-certified scope only if it can discharge that liability and carry the old one.
- **Novelty vs nearest prior art:** Funnel selection and [correction classes](https://github.com/manojbajaj95/cl/pull/169) select an interface or repair. This proposes transferring the accumulated liability without correcting or replaying the rejected edit.
- **Cheapest first test:** Two ports share `W` but protect different slices. Find one resumable refusal and one whose accumulated error blocks both ports; compare fallback rules with the exact admissible-scope graph.
- **Old-task retention check:** Keep all originally protected A/C slices in the check on the fallback, even if the receiving port would not protect one in isolation.

### Replace loose accounting with certificates that respect dynamics

#### 13. Keep a separate balance for every protected direction (P)
- **Mechanism:** Carry a vector or polytope of liabilities for a small set of readout directions; composition and transfer preserve its correlations rather than spending the largest component everywhere.
- **Novelty vs nearest prior art:** [Rényi DP](https://arxiv.org/abs/1702.07476) uses richer profiles than a single scalar, and relational verification tracks correlated directions. The candidate is transfer of a reusable liability profile keyed to old-task readouts.
- **Cheapest first test:** Two new streams charge different A/C directions in a two-dimensional linear learner; compare scalar, separate interval counters, a polytope receipt and full-state exact checks, including bytes.
- **Old-task retention check:** Score each A/C slice and their conjunction; reject a profile that improves macro-average while losing the slice hit by both directions.

#### 14. Reserve for amplification that has not happened yet (I)
- **Mechanism:** Charge a perturbation for its largest possible future amplification before any remaining prefix, not merely its impact at the current step or terminal time.
- **Novelty vs nearest prior art:** Robust funnel reachability and sensitivity propagation already multiply local gains. This is the correction to a naive scalar lease under expansive dynamics.
- **Cheapest first test:** Set suffix gains to `3` then `1/3`. Compare raw sum, final-only, prefix-envelope and exact enumeration with the same injected cost and output cap.
- **Old-task retention check:** Hold out ordinary examples that fail only at the middle prefix, and report failure even if the endpoint prediction recovers.

#### 15. Earn back headroom only after a proved repair (P)
- **Mechanism:** Replace outstanding liability with a smaller certified envelope after a contraction or reset of *error*, not a reset of useful B state. A separately issued monotone lease is not automatically refilled.
- **Novelty vs nearest prior art:** Robust invariance already permits contraction; [self-replenishing capacity](https://github.com/manojbajaj95/cl/pull/170) asks whether future editing room can be rebuilt. Here the operation reissues a retired-source guarantee on evidence of smaller paired discrepancy.
- **Cheapest first test:** Interleave one certified contractive step and one gate that only appears contractive in the publisher's data. Compare no refill, safe reissue, speculative refill and exact reachability.
- **Old-task retention check:** Require A/C floors throughout the repair, not just after, and confirm held-out B outputs survive the step that recovers headroom.

#### 16. Cancel leakage only in a signed relational proof (I)
- **Mechanism:** Offer certified cancellation across updates when their signs and dependency are coupled by the grammar. A favorable sign observed after one arm runs cannot justify credit.
- **Novelty vs nearest prior art:** Affine/relational propagation already tracks shared uncertainty symbols. This tests if the extra evidence beats triangle-inequality overcharging.
- **Cheapest first test:** Compare legal `+h, −h` with a second grammar that independently chooses the second sign. Enumerate intermediate as well as final error, and include the cost of carrying the shared symbol.
- **Old-task retention check:** Check A/C after the first change, even on a fully cancelling branch, and at the worst adversarial choice on the independent grammar.

#### 17. Buy an extension without buying a new teacher (P)
- **Mechanism:** Once the original horizon ends, extend only from a certified renewal region with a fresh suffix envelope and no unresolved omitted-coordinate return. Preserve the original reference for cumulative retention.
- **Novelty vs nearest prior art:** Invariant tails and funnel chains already support unbounded operation; the candidate is extension of a spendable substitution right after source retirement without silent re-anchoring.
- **Cheapest first test:** Repeat a two-phase affine grammar with and without a renewal invariant; compare chaining, horizon-specific recertification and a naive reset of the cap at every horizon.
- **Old-task retention check:** Score A/C against the original pre-cut reference across repeated phases; reject small per-renewal drift that accumulates beyond the declared floor.

#### 18. Lease stochastic continuations without mixing up error and risk (P)
- **Mechanism:** Keep a deterministic discrepancy cap on certified paths and a separately justified time-uniform bound on leaving that scope under adaptive batch selection. Never trade a unit of prediction error for a unit of failure probability.
- **Novelty vs nearest prior art:** Adaptive privacy odometers already separate probabilistic accounting from realized choices. The CL claim is source-free control of probabilistic scope with an enforceable return check, not a privacy guarantee.
- **Cheapest first test:** Enumerate a small stochastic gate tree with a rare rejoin failure; compare a conditional-risk bound, naive iid estimates and a deterministic filter under a schedule that adapts to past spend.
- **Old-task retention check:** Report ordinary A/C on both typical and rare rejoin paths, unconditional failure frequency and worst admitted prefix; do not drop out-of-scope jobs from utility accounting.

### Try to explain the result without the proposed primitive

#### 19. Teach lower leakage instead of demanding a larger cap (I)
- **Mechanism:** Select truthful training examples to lower the marginal price of B updates specifically near a guarded return, holding the old margin distribution and B progress fixed.
- **Novelty vs nearest prior art:** [HAL](https://arxiv.org/abs/2002.08165), GPM and trajectory matching already shape learning. This would improve the admission frontier, not establish a new budget object by itself.
- **Cheapest first test:** Exhaust size-two subsets of a small example pool; compare free corridor, the best verified-training stack and sparse isolation under the same checker and tuning budget.
- **Old-task retention check:** Margin-match A/C at entry, then score at rejoin and after source overwrite; add a later B task that needs the shared unit, to catch rigid isolation.

#### 20. Locate the obstruction to a compact lease (I)
- **Mechanism:** Seek pairs with identical visible state and receipts but incompatible legal returns, so no decision on that interface can be both safe and complete. Measure how many distinguishable return classes a useful interface needs.
- **Novelty vs nearest prior art:** Indistinguishability and partition refinement already give lower bounds. The audit pins down where proof omission buys nothing for future training.
- **Cheapest first test:** Use a hidden bit that selects the sign of a delayed old-task logit change; enumerate exact return classes, then grow the delayed state and compare the smallest honest receipt to tracking it directly.
- **Old-task retention check:** Construct matched-margin A/C examples harmed by the indistinguishable unsafe continuation, while the safe one preserves them at equal B progress.

#### 21. Find when checking the lease costs more than keeping the state (I)
- **Mechanism:** Price publication, receipts, peak copies, returns and failures across short and long leases. Compare cumulative spend on verification after many independent jobs, not just the smallest receipt.
- **Novelty vs nearest prior art:** Proof amortization and parent entry-port break-even analyses already price reuse. This isolates the incremental value and burden of spend and rejoin.
- **Cheapest first test:** Sweep omitted width, length, rejoin frequency and importer count on a finite grammar with exact checks; compare static union, full recertification, equal-byte replay and the stacked adaptive baseline.
- **Old-task retention check:** Only count a break-even point where A/C floors and useful B progress match across arms, including fallback at refused rejoin and after overwrite.

#### 22. Compile the whole lease into existing tools (I)
- **Mechanism:** Treat hidden state as a conventional time-indexed abstraction, use verified buffer substitution and implement allocation, precommit checks, rejoin and transfer as ordinary contracts with an augmented resource state.
- **Novelty vs nearest prior art:** Pacti plus IBP, verified training, MTT and adaptive accounting is the direct null. A tie rules out evidence for a new CL primitive, even if the artifact is convenient.
- **Cheapest first test:** Run the conceptual four-arm ablation on the two paper witnesses and then one blind handoff panel with identical grammar, verifier and source cutoff. Seek an interaction between omission and transfer not explained by either alone at matched costs.
- **Old-task retention check:** Require independent A/C and useful B behavior across every visible prefix and after a later learner spends residual rights; flag every unsound admission, not only terminal failures.

## Ranked deeper questions

1. **Can one blind learner spend another's residual right after the source is gone, without reopening the predecessor proof?** Freeze the package and try the serial handoff with dynamic omission and ordinary A/C floors (cards 1, 2, 7, 22). Compare the useful-admission frontier and total evidence with full recertification and the adaptive Pacti + IBP + verified-substitution stack. A tie ends the primitive claim; a fixed-quota win alone does not count.
2. **When is omitting a coordinate cheaper than tracking it once its return is priced?** Compare static-union and time-indexed proofs, optimizer paths, planted out-of-relation arrivals and the indistinguishability obstruction (cards 1, 3–6, 20). Require useful B differences and normal A/C retention before and after the read; report the first regime where the boundary receipt costs more than the omitted state.
3. **What must a successor inherit for spending to compose safely?** Start with a scalar under nonexpansion; try typed conversion and a truly coupled merge, then gains, cancellation and reissue (cards 8–10, 13–17). Seek the smallest bad prefix for each cheaper accountant. Separate liability already incurred from transferable entitlement; do not manufacture a shared cap for independent jobs.
4. **Where does leasing buy real plasticity rather than cheaper bookkeeping?** Hold scope, margins, source cutoff and retained A/C fixed; vary coupling and task order, map missed-safe versus unsafe admissions and check free, rigid and erased controls (cards 19–22). If useful admission does not grow and total evidence does not fall, keep only the negative result.
