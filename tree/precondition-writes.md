# Precondition-carrying writes

**Status:** Ideas only; no experiments, probe code, or GPU. **Parent:** [Mergeable writes with certificates](mergeable-writes.md), [PR #156](https://github.com/manojbajaj95/cl/pull/156), cards 02 and 10. **Review seed:** [Flood triage row 250](https://github.com/manojbajaj95/cl/blob/a23652eb741c8198a672880caeccf111a4222c2a/reviews/flood-triage.md#L250), two score-3 ideas: return prerequisites over particular choices (“apply B's choice before A's” when B makes room for A); attach a proved range of starting states to a stale write so it can be rebased by checking membership and new obligations rather than retraining.

**Are writes with explicit preconditions a new object for continual learning?** Not as a formal object: a guarded transition with a proof is a Hoare contract, and producing or protecting prerequisites is already part of planning. The CL candidate is narrower: a learned write whose certified starting-state envelope travels with it, can be consumed or deliberately established by independent learners, and remains useful after either the base or the set of protected tasks changes. If generic planning over the same effects plus ordinary rebase and incremental verification ties, this is an application, not a new CL primitive.

## What would a pending write carry?

- **A specified transition and an entry envelope.** For a named choice w, let T_w be its deployed transition, including any runtime state that matters (routing, optimizer state if used, arithmetic). The contract names a deployment domain W and acquisition-anchored old obligations Oᵥ at version v. The exact entry set consists of starts in W where Oᵥ already holds and where T_w is defined, keeps every obligation at each served prefix, and meets the stated new-task floor N_w at the advertised acquisition point. Export a checkable sufficient subset P_w of that set, not necessarily a ball or even connected. A start outside P_w is unsupported, not necessarily unsafe. A region of safe **starts for a particular write** is not the [finite safe regions node](finite-safe-regions.md)'s region of safe checkpoints: for a single atomic write and an old safe region S, the old-only entry set is S ∩ T_w⁻¹(S) where T_w is defined.
- **An effect and its threats.** On a specified starting domain, a merge can prove that B's named choice establishes P_A, then that no admitted intervening choice destroys it (or require an atomic check at A). “B before A” may be a sufficient route, not a necessary order; proving necessity means ruling out every admitted trace with A but without B before it, under a stated menu and start domain. Use alternatives, guards and exclusions when a static graph lies. An atomic shadow-build proof authorizes the endpoint, not service from its hidden intermediates.
- **A checked rebase, not a new fit.** If the deployment semantics match and a returning write still has the same T_w, prove that the live state is in P_w and that every currently required obligation not covered by the proof also holds through the write. Recheck or reserve the live snapshot through publication; a concurrent update can invalidate membership. If the proof covered only an older contract, do not use it to drop the intervening learner's acquisitions or to block explicitly authorized revisions of retired tasks. If a reparameterization or new edit changes T_w, prove the correspondence or treat it as a new write. Registration and inference reference points are part of the contract; a successful write does not silently reset old baselines.

**Paper checks.** Let old A win iff x > 0 and let old C be independent. From x = 1, choice a subtracts 2 from x, choice b adds 2, and choice c adds 3. Each also sets its own independent skill flag, which by stipulation meets its toy new-task floor. Choice a's exact old-A entry condition is x > 2 (up to the host bounds); b then a serves A at both prefixes, a then b does not. The same a can instead follow c or be used solo from x = 3; b is not a universal prerequisite. From x = 5, two distinct copies of the debit can run, but not three: a spent guard is not a reusable permission. A stale a can be accepted from x = 3 by checking its guard, not from x = 1 even though current A still passes. If a newly learned D now wins iff x > 2, x = 3 passes the old envelope but the post-a state x = 1 flips D. Alternatively, if a's new skill flag only works when an unchanged feature key equals 1, a proof for that version of a must also check the key; passing A/C is not successful acquisition.

## Closest work and common CPU oracle

[Hoare logic](https://web.stanford.edu/class/cs357/hoare69.pdf), [predicate transformers](https://doi.org/10.1145/322077.322088), [proof-carrying code](https://www.usenix.org/legacy/publications/library/proceedings/osdi96/full_papers/necula/html/), and [UCPOP](https://homes.cs.washington.edu/~weld/papers/ucpop-kr92.pdf) already give contracts, weakest preconditions, independently checkable proofs, and causal links with threats. [Context-based operational transformation](https://dl.acm.org/doi/10.1145/1180875.1180918) already reasons about the context in which an operation applies and adapts it to a changed context; a membership-only fast path here keeps the transition fixed. [CRDTs](https://arxiv.org/abs/1805.06358) and [invariant confluence](https://arxiv.org/abs/1402.2237) make convergence and coordination the right distributed baselines, not evidence for retention.

[Git-Theta](https://arxiv.org/abs/2306.04529) provides model change tracking and merge machinery. [Task arithmetic](https://arxiv.org/abs/2212.04089) and [fine-tuning transfer](https://arxiv.org/abs/2503.20110) already apply deltas outside the context where they were trained; neither transferring a delta nor avoiding retraining is by itself the claim. [MEMIT](https://arxiv.org/abs/2210.07229) and [AlphaEdit](https://arxiv.org/abs/2410.02355) are editor controls: locally refit or project an edit against the live base. [GPM](https://arxiv.org/abs/2103.09762) protects old activation subspaces, [InterContiNet](https://arxiv.org/abs/2206.07996) constrains weight intervals, and [APRNN](https://arxiv.org/abs/2304.03496) repairs networks under specs. [Certified Continual Learning](https://arxiv.org/abs/2407.06697) reuses verification across retraining; [CABA](https://arxiv.org/abs/2610.40740) already gives conditional off-anchor and sequential retention bounds for an endpoint gate. The [finite-safe-regions](finite-safe-regions.md) and [mergeable-writes](mergeable-writes.md) baselines get the same verifier and menus. The [idea ledger](https://github.com/manojbajaj95/cl/blob/a23652eb741c8198a672880caeccf111a4222c2a/reviews/idea-ledger.md) kills read-pinning without downstream checks, free-form lesson preconditions repaired by prompting, and forecasts mistaken for safety. None is a certificate here; a nonzero order-sensitivity signal is not required even when only one order is safe.

Start with rational finite-state and small ReLU worlds. Enumerate live starts, choices, serving prefixes, changed obligations and delayed returns; use exact transition/decision checks as truth. A and C are old tasks (include rare A and an unrelated C); D is acquired while a writer is away. Check exact agreement against acquisition and report ground-truth accuracy on A/C/D separately, with held-out examples as diagnostics, not certified claims. Unless explicitly shadowed, **every** served prefix must pass; score attained new-task floors separately and register accepted acquisitions. Start with finite declared domains, and only claim regional guarantees with a proof over the entire declared region. State the tie rule and test its boundaries.

The stacked control is the same frozen menus and training data access with Git-Theta-style tracking, ordinary causal-link scheduling with verification of served prefixes, and incremental verification on live rebase; add APRNN-style joint repair or warm-started editor refitting at equal total work where feasible. Include the exact entry-set/trace oracle as a ceiling, not as a scalable baseline. Charge proof search, failed attempts, membership checks, retained and transmitted bytes, waiting, and retraining over the stream; give each side the same late writers and new-task floors. Report zero false admits as a requirement, coverage of truly safe rebases, old-task service, admitted new-task utility and amortized cost. Count abstentions and misses, not just precision on a few easy accepts.

## Idea cards

### Orders that can survive new choices

#### 01. Derive the weakest usable starting condition
- **Mechanism:** Pull the retained decisions and new floor back through the actual write. Compile exact entry sets where possible; elsewhere export proved inner approximations with explicit abstention.
- **Novelty vs nearest prior art — IMPROVEMENT:** This is weakest-precondition computation plus finite-safe-regions. The gain to measure is how much a write-specific preimage buys over holding a whole common tolerance box.
- **Cheapest first test:** Enumerate a rational one-mutable-layer ReLU grid whose safe entry set has two pieces; compare equal-byte polyhedral, box and checkpoint-only exports against exact per-base verification.
- **Old-task retention check:** Check rare A and C at all admitted start/end pairs and every served prefix; test the unsafe gap, faces and tie points.

#### 02. Separate must-order from a sufficient schedule
- **Mechanism:** Return a witness that B enables A on a named start domain, and optionally a separate exclusion proof for traces where A runs without B first. A late writer can retract the must-order claim without discarding the enabling witness.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** UCPOP already supplies causal links, and PR #156 names choice-level prerequisites. The candidate is an updatable proof interface that separates the two claims when independent menus arrive.
- **Cheapest first test:** Hide a third choice that makes room for A and reveal it after merge; compare updating the two proofs to an incremental causal-link solver given the same effects. Include a cyclic dead end with no enabled first step.
- **Old-task retention check:** Check A/C over all admitted traces before and after revelation, and show an early failing prefix for any order actually ruled out as unsafe.

#### 03. Let several effects jointly establish one guard
- **Mechanism:** For a particular A choice, export alternatives such as “B and C together, or E alone,” guarded by the live starting slack. Bind each clause to its joint effect, not each provider's solo validity.
- **Novelty vs nearest prior art — IMPROVEMENT:** Partial-order planning and [disjunctive protection](https://github.com/manojbajaj95/cl/pull/155) already offer disjunctions; here the clauses govern production of a pending write's precondition, not alternative carriers of current service.
- **Cheapest first test:** Sweep starts for a threshold requiring two small deposits or one large deposit. Compare choice clauses to flat DAGs and a planner with numeric guards and the same verification budget.
- **Old-task retention check:** Enumerate each clause and partial clause on A/C; include a weak substitute that meets its own task but does not provide enough slack.

#### 04. Attach an expiry event, not a timestamp
- **Mechanism:** Return a causal link plus exactly the certified class of intervening writes that cannot destroy it. Require a new live check after a possible threat, even if the provider was executed recently.
- **Novelty vs nearest prior art — IMPROVEMENT:** Threat handling is standard in causal-link planning. Test whether model-derived effect summaries make it cheaper than checking all intervening prefixes, not whether time predicts forgetting.
- **Cheapest first test:** Interleave one supplier with many harmless writes and one write that consumes its headroom without breaking today's old service; compare version expiry, planner threat checks and exact readmission.
- **Old-task retention check:** Check A/C throughout the valid queue and prove the threatened A application is blocked before its first bad served prefix.

#### 05. Spend a guard once, split it only by proof
- **Mechanism:** A supplier can authorize a bounded bundle of future debits. Split the bundle across learners only when the composed worst-case consumption, including shared rivals, keeps each promised guard true until its use.
- **Novelty vs nearest prior art — IMPROVEMENT:** Escrow and invariant confluence already budget decrements; [stored slack](https://github.com/manojbajaj95/cl/pull/151) already prices margin. The case worth testing is nonlinear behavioral headroom with an honest joint bill.
- **Cheapest first test:** Give two consumers overlapping claims on two margins; compare behavioral splitting to scalar escrow, per-margin escrow and per-commit serial checks. Include a cross term that invalidates a split that looked additive.
- **Old-task retention check:** Check every authorized debit order on A/C, rejecting duplicate spending and concurrent acquisition of the same last unit of headroom.

#### 06. Learn to make room for a future write
- **Mechanism:** Accept a local B choice only if it meets B's floor and demonstrably establishes more of the *declared* pending write guards than a matched B choice. Test transfer to independent writes withheld during B training, never promising their admission without proof.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** GPM protects past features, [future edit cost](future-edit-cost.md) prices revisions, and PR #156 trains menus for compatibility. The proposed action deliberately produces a certified state predicate another learner has published, not a generic plasticity score.
- **Cheapest first test:** Train small B readouts on identical data with ordinary B loss, matched margin bonus and pending-guard objectives; delay A's payload and reveal a held-out second consumer after B commits.
- **Old-task retention check:** Match reference A/C accuracy and margins before intervention; audit A/C after B and after all served consumer prefixes, plus B after its registration.

### Rebase without touching the writer's data

#### 07. Give one proof a long and a short route
- **Mechanism:** Export a cheap sufficient gate for typical starts and a more expensive verifier for a larger certified region, both tied to identical deployed semantics and new-task floor.
- **Novelty vs nearest prior art — IMPROVEMENT:** Cascaded verification and CABA-style gates are prior art. The question is whether a fixed pending write amortizes gates over late bases, not whether loose gates can accept quickly.
- **Cheapest first test:** Replay sparse and bursty delay traces; sweep cheap gate size and compare to warm starts, cached endpoint proofs and incremental verification with the same stopping rule.
- **Old-task retention check:** Verify A/C/D on every accepted served prefix and compare both fast and slow paths to the exact oracle at the same boundaries.

#### 08. Rebase against the obligations added during absence
- **Mechanism:** Index the envelope by its covered contract clauses and accepted versions. On return, check membership once, then prove only new or changed clauses with the live references; do not waive old clauses that are still active.
- **Novelty vs nearest prior art — IMPROVEMENT:** This is the parent's card 10 with an explicit delta-of-obligations control. Certified Continual Learning makes ordinary incremental reuse the baseline.
- **Cheapest first test:** Delay one write past three commits: one harmless, one leaving its envelope while remaining functional, and one registering D inside the envelope. Compare stale gates, live incremental rebase, and fresh refit.
- **Old-task retention check:** Separate out-of-envelope abstention from an in-envelope D failure; check A/C and D across all prefixes admitted after D registers.

#### 09. Make applicability and usefulness separate checks
- **Mechanism:** Prove two entry regions for the same write: one for retention and one for the target floor. Their intersection is the fast path; the separate failure reasons tell a returning writer whether to revisit its editor or seek more room.
- **Novelty vs nearest prior art — IMPROVEMENT:** APRNN and [DUET](https://arxiv.org/abs/2611.29269) already target old and new behavior together. The proposed gain is cheaper diagnosis and repair selection after staleness.
- **Cheapest first test:** Let an intervening write change a feature key used only by the new task, then separately move an old rival. Compare blind task-vector transfer, ordinary verification with split diagnostics and warm-started refits.
- **Old-task retention check:** Check A/C/D after each trial in shadow and after each published prefix; a safe but useless write must never count as acquisition.

#### 10. Version the task being edited, not just the base
- **Mechanism:** Bind a delayed edit to the target revision it intends to install and to the revision that authorizes it. An admitted weight envelope says nothing about whether that revision is still current.
- **Novelty vs nearest prior art — IMPROVEMENT:** Compare-and-swap and MEMIT cover conditional publication and edits respectively; the CL question is whether explicit target versions prevent safe-looking resurrection of superseded facts.
- **Cheapest first test:** Queue v2, then admit v3 from another learner; make the stale v2 still pass checks on unrelated old tasks. Compare base versioning, target-version checks and ordinary refit on current labels.
- **Old-task retention check:** Check unchanged A/C/D and the currently authorized fact plus its dependent skill; do not score agreement with an explicitly retired answer as retention.

#### 11. Certify an adaptive edit script, not just a delta
- **Mechanism:** Attach guarded branches to a bounded deterministic write program. It can choose a different pre-proved operation at a shifted base without local optimization; reject when none of its entry predicates hold.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Operational transformation already adapts operations, and PR #156 already has a menu. The narrower candidate is a portable dispatch rule with a common acquisition guarantee and live behavior guards, versus a menu routed by a generic planner.
- **Cheapest first test:** Compare static transfer, equal-byte menus with a gate, and a small guarded script on two ReLU start cells with different feature keys. Include one start where no branch works.
- **Old-task retention check:** Exhaustively check the dispatched branch and its intermediate states on A/C/D, including branch overlaps and explicit no-branch abstention.

#### 12. Keep the check true until the write publishes
- **Mechanism:** Tie proof membership, covered contract versions and publish to one serialized snapshot, or prove every permitted concurrent transition safe until an atomic recheck.
- **Novelty vs nearest prior art — IMPROVEMENT:** This is optimistic concurrency control against behavioral predicates, not a new transaction algorithm. The potential savings are fewer false conflicts than exact snapshot locks.
- **Cheapest first test:** Enumerate check/commit interleavings with unrelated drift, a guard-destroying update and concurrent registration of D; compare snapshot retries, ordinary serial checks and verified tolerance of benign drift.
- **Old-task retention check:** Audit A/C/D in actual publication order; include the race in which both writers pass isolated checks but the second would fail on the committed base.

#### 13. Rebase the optimizer continuation, too
- **Mechanism:** When the proposed write includes a future momentum or adaptive step, extend its start envelope to optimizer state, or explicitly terminate the proof at weight publication.
- **Novelty vs nearest prior art — IMPROVEMENT:** Ordinary checkpointing carries optimizer state; [disjunctive protection](https://github.com/manojbajaj95/cl/pull/155) already considers optimizer-state leases. This tests whether a weight-only envelope is a false portability claim.
- **Cheapest first test:** Prepare two identical weights with opposite momentum; compare full-state guards, resetting state and a verifier of the same bounded continuation. Charge progress lost by reset.
- **Old-task retention check:** Check A/C/D for each served continuation step, not just the identical initial weights or the final model.

### Change what can be checked without old data

#### 14. Make the guard smaller without pinning activations
- **Mechanism:** Prove that a compact statistic suffices for a particular edit's retention and utility predicates over admitted drift, including its downstream consumers and rivals. Fall back to the full guard when that implication cannot be proved.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** GPM and AlphaEdit already keep compact old-read information. The ledger's read-pinning failed precisely when consumers moved; the candidate is a sufficient statistic for a *write transition*, not a frozen activation.
- **Cheapest first test:** Use paired base states with identical insertion activations but different downstream gains. Compare equal-byte activation summaries, composed producer–consumer guards and exact checks.
- **Old-task retention check:** Require the guard to reject the wrong-gain twin if it breaks A/C, with D included when it depends on the changed consumer.

#### 15. Acquire a missing guard fact rather than retrain
- **Mechanism:** When deciding membership requires an unknown state predicate, choose the cheapest certified diagnostic that settles it, or abstain. A diagnostic can disclose a Boolean proof fact rather than raw historical examples.
- **Novelty vs nearest prior art — IMPROVEMENT:** Adaptive testing and the parent's multi-custodian contracts already make selective queries natural. This is a measured communication or verification saving, not a privacy guarantee.
- **Cheapest first test:** Split an exact linear guard across three custodians and assign different check costs; compare byte-matched direct audit, fixed order, and adaptive check selection with a timeout arm.
- **Old-task retention check:** Independently audit all panels on A/C/D; a timeout or an unproved off-panel conclusion may not authorize a write.

#### 16. Keep the choice alive by negotiating its entry condition
- **Mechanism:** Return a witness of a violated live guard and a sufficient condition for a distinct preparatory transition. Let another writer satisfy that condition if it can meet its task, without changing the stale payload.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Causal-link planning already asks how to establish an open precondition; APRNN already repairs against a spec. The candidate operation is a bilateral repair interface between learners who cannot exchange old examples or retrain the payload.
- **Cheapest first test:** Give two writers private objectives and a shared behavioral guard, then hide the supplier until after rejection. Compare normal counterexample exchange, joint repair with disclosed inputs as a ceiling, and a live repair request using the same permitted information.
- **Old-task retention check:** Check A/C/D after any preparatory write and after the payload; include a preparer whose endpoint helps the guard but whose served path forgets A.

#### 17. Transfer a guard through a change of coordinates, not through wishful equivalence
- **Mechanism:** Check a map that preserves the deployed transition and its certified domain, including old observations and the target floor. Pull the guard back along that map and recompute any unproved remainder.
- **Novelty vs nearest prior art — IMPROVEMENT:** PR #152/#156 already require proof transport, and fine-tuning transfer already moves deltas between model versions. This is a fast-path boundary for stale entry predicates, not a new transport theorem.
- **Cheapest first test:** Compare exact permutation, same-span basis change moving the certified box, and downstream consumer drift against full incremental rebase. Include both a valid transported write and a false same-span transfer.
- **Old-task retention check:** Check A/C/D on every transported accepted start and every served prefix in the new chart; challenge points whose images fall outside the original certified domain.

#### 18. Exploit identical entry rules without conflating tasks
- **Mechanism:** Share verification of a common guard across many stale writes only where their individual retention and utility claims all follow. Keep per-write effects and version requirements separate so a later coordinate change or task addition can split the group.
- **Novelty vs nearest prior art — IMPROVEMENT:** Proof caching and subexpression reuse are routine, and PR #156 already reuses unaffected premises. Test reuse across independently trained payloads rather than across repeated checks of one checkpoint.
- **Cheapest first test:** Create fifty readout edits sharing two genuinely common thresholds and one deceptive near-match; compare hash-based caches, batched direct verification and shared implication proofs at the same memory.
- **Old-task retention check:** Recheck A/C/D on every payload passing the shared gate, especially the near-match at an exact boundary and the group after a version split.

### Ways to falsify the object

#### 19. Separate order-sensitive retention from noncommuting learning
- **Mechanism:** Build a factorial oracle crossing commuting versus noncommuting transitions with invariant versus order-sensitive served prefixes. Ask whether a compiled behavioral order adds anything beyond actual per-prefix checks.
- **Novelty vs nearest prior art — IMPROVEMENT:** The [Lie bracket order predictor](https://arxiv.org/abs/2611.20087) studies optimization order; the ledger already killed weaker forecasts. This is a separation test, not another surrogate: commuting additions can share a final state yet have a bad prefix.
- **Cheapest first test:** Enumerate tiny additive and state-dependent update pairs with matched endpoints where possible; compare bracket or endpoint ranking, a causal-link planner and cached per-prefix checks.
- **Old-task retention check:** Check A/C/D separately on both orders and distinguish failures of served prefixes from endpoint failures or changes in final new-task utility.

#### 20. Find the bits needed to answer later admissions
- **Mechanism:** Withhold the late query when compiling; to derive a lower bound, construct histories whose retained model and public pending menu are identical but whose protected input domains differ and induce different safe admission answers. Count all retained side information and any later queries.
- **Novelty vs nearest prior art — IMPROVEMENT:** The parent's trace-separation card and reviewer’s future-language equivalence already cover distinguishability. Here the assay prices information specifically for delayed admission; it does not claim a separation between identical full states.
- **Cheapest first test:** Start a linear table with identical correct outputs on k input pairs. In each history only one input per pair is protected, and each query write flips just the first input of one pair, giving 2ᵏ admission vectors across histories. Test whether guard compression wins on a matched correlated family against an equal-byte history and incremental verifier.
- **Old-task retention check:** For every distinguishable pair, exhibit the pending write and the specific A/C/D decision it would flip on one history; current service alone must not distinguish the pair in the assay.

#### 21. Measure where delay makes the proof worthless
- **Mechanism:** Vary delay length, base drift and contract turnover independently. Measure the payback time of envelope compilation; record which misses are due to conservative geometry, new obligations, or loss of the target effect.
- **Novelty vs nearest prior art — IMPROVEMENT:** The parent prices cumulative verification and ordinary checkpointing prices staleness. This is a break-even test, not a replay-deadline forecast.
- **Cheapest first test:** Run an enumerable stream with independently varied drift/delay and a held-out arrival process; compare cold/warm verification, unconditional transfer, warm refit and guard reuse at equal utility floors.
- **Old-task retention check:** Audit worst-prefix A/C/D, including rare cases in churn-heavy streams; a fast scheme that rejects almost everything or postpones learning cannot claim a win.

#### 22. Fail closed when the deployed model is not the proof model
- **Mechanism:** Bind envelope membership to the transition implementation and arithmetic; allow verified slack for possible rounding or abstain when the running model cannot justify the comparison.
- **Novelty vs nearest prior art — IMPROVEMENT:** Numerical verification and both parent nodes already demand this. The extra test is the stale-write race at changed precision, not a new soundness technique.
- **Cheapest first test:** Find rational entry points exactly at or just inside a guard and replay them after a simulated precision change and tie-rule patch. Compare strict implementation binding, bounded rechecking and full fresh verification.
- **Old-task retention check:** Compare every accepted prefix in deployed arithmetic against A/C/D acquisition references and the declared tie rule; flag precision-induced false admission separately.

## Ranked deeper questions

1. **Can a delayed, independently trained write be admitted, or be made admissible by another writer, for less than ordinary rebase plus incremental verification?** Run 02 → 08 → 16 with withheld late providers and acquisitions. Require zero false admits and a gain in total verified new-task utility or amortized work at matched bytes and old service. Give the stacked planner/rebase control the same payloads and effects. A tie makes the proposed object an application of contracts.
2. **What is the smallest usable behavioral interface between a supplier, a consumer and the learners in between?** Run 03/04/14 as coupling goes from sparse to dense. Can checked summaries establish and protect more live guards than ordinary numeric planning at the same check cost? Include erasers that keep today's old outputs unchanged.
3. **Can training learn to leave room for an independently invented write, rather than memorizing the requested guards?** In 06/11, match B progress and margins, hold out whole consumer families, and compare strong margin, GPM and menu baselines with identical verification. Measure verifiable admission and subsequent utility, not a readiness proxy.
4. **What must an envelope forget as its world changes?** Use 08/10/20/21 to separate obsolete task revisions, expanding commitments, and changes to the write or verifier. Find the drift and contract-churn regimes where retained proof state saves less than an equal-budget log, incremental checks or refitting.
