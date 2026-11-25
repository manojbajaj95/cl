# Collective agents III: spend verification on decisions, not victories

**Status:** Ideas only; no implementation, learner runs, or GPU work. **Parent:** [Collective agents II](collective-agents-2.md) ([PR #314](https://github.com/manojbajaj95/cl/pull/314)). **Review seeds:** [Flood triage, lines 430–433](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md#L430-L433) on [PR #6](https://github.com/manojbajaj95/cl/pull/6), with #314 on line 432: score-3 [#01, renew only what the event told apart](collective-agents-2.md#01-renew-only-the-claims-separated-by-the-event), and [#09, renew on an observation nobody could have scripted](collective-agents-2.md#09-renew-on-an-observation-nobody-could-have-scripted). No card earned a 4. Item leases and echo subtraction are inherited controls, not new seeds; the reviewer already identifies the latter with control-variate/PPI++ rectification.

**Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md). No popularity voting, independently authored copies treated as truth, bagged writers, forecasts standing in for fresh outcomes, or historical replay A/B without prospective support. **P** means a candidate reusable operation or evidence object; **I** means a test or improvement, not a new primitive.

## What would have to be new?

The novelty bet is not that evidence should separate hypotheses, or that a draw made after commitment is harder to script. It is that a fleet can retain more skills by granting **authority to take a particular action for a particular old caller** on less evidence than it takes to renew a skill or resolve its mechanisms globally. That authority may depend on what can still be tested after deployment and on which other authorities are used with it. A success can distinguish two wrong models; a random draw can be authentic while its observed outcome is selected. Neither alone authorizes learning.

## Literature check

Checked the linked abstracts and the indicated sections for candidate selection, evidence validity, and sharing. The comparisons below are narrow novelty hypotheses, not priority claims.

- **Diagnosis and sensing:** [Reiter, *A Theory of Diagnosis from First Principles*](https://cs.ru.nl/~peterl/teaching/KeR/Theorist/reiteraij87.pdf) derives diagnoses from conflicts and discusses discriminatory measurements; [Controlled Sensing](https://doi.org/10.1109/TAC.2013.2261188) optimizes the choice of observation for hypothesis testing; [Adaptive Submodularity](https://arxiv.org/abs/1003.3967) gives conditions under which adaptive greedy selection is competitive. Generic hypothesis discrimination or greedy probe selection is not new.
- **Fleet curation and expiry:** [SkillClaw §2.3](https://arxiv.org/html/2604.08377v2#S2.SS3) compares candidate and incumbent on the actual toolchain before synchronization; [Zep §5](https://arxiv.org/html/2611.01386#S5) cites supporting events at the claim level and patches only supported fields. [MultiEvoSkill §3, Def. 3.2](https://arxiv.org/html/2610.34260v1) ties evidence-backed issues and preservation records to graph versions. [MASkills §4.2](https://arxiv.org/html/2609.02094) already assigns credit per invocation with a centralized counterfactual language critic. End-to-end fresh trials, claim-level provenance, graph-scoped preservation, credit assignment, and ordinary [Gray–Cheriton leases](https://doi.org/10.1145/74850.74870) are controls, not proposed inventions.
- **Disclosure and sequential validity:** [NIST's beacon procedure](https://csrc.nist.gov/Projects/interoperable-randomness-beacons/apps) already commits to a deterministic procedure before future public randomness. [Confidence sequences](https://arxiv.org/abs/1810.08240) handle repeated looks under stated conditions; [selective inference](https://arxiv.org/abs/1410.2597) conditions on selection; [the reusable holdout](https://doi.org/10.1126/science.aaa9375) limits what adaptive users learn from holdout queries; [SHANGRLA](https://arxiv.org/abs/1911.10035) reduces an audit of an outcome to testing sufficient assertions. None licenses arbitrary reuse of dependent observations.
- **Causal scope and accounting:** [Transportability](https://doi.org/10.1214/14-STS486) formalizes when causal information can move between domains; [Switchback Experiments](https://doi.org/10.1287/mnsc.2022.4583) provide randomized designs under carryover; [VanderWeele's four-way decomposition](https://pmc.ncbi.nlm.nih.gov/articles/PMC4220271/) distinguishes mediation and interaction. [Provenance Semirings](https://doi.org/10.1145/1265530.1265535) represent alternative and joint derivations, and [continuous distributed monitoring](https://www.cs.ox.ac.uk/people/graham.cormode/pubs/papers/cdsurveysigmodrecord.pdf) prices communication needed to track a function. Relabeling these methods as leases is not a win.

## First-test contract

- Inherit the [parent contract](collective-agents-2.md#first-test-contract). Start with enumerable two-to-four-agent CPU FleetWorld-tab fixtures. Predeclare local observables, allowable harmless interventions, competing predictions, what the verifier measures, dates of acquisition and delivery, and trace IDs. Commit the prediction table and branch distribution before the draw; log all assignments, including missing outcomes. Allow an unmodeled alternative (or abstention); never renew simply because all named rivals lost. No branch with zero support supplies evidence.
- Compare item leases, time/usage expiry, verified-trial counters, #314#01 with the same acquisition, #314#09 with the same commit and randomization, and an ordinary randomized audit at equal counts. For combined proposals run the strongest applicable baselines stacked, with the candidate's schedule where meaningful. A legal centralized scheduler sees only the same messages at the same times. Charge verification, traffic disruption, local compute, peak state, and all evidence bytes. An exhaustive oracle is a ceiling if it sees private information or exceeds those budgets.
- Score current-task progress and prequential world loss, mature authority accepted when wrong, needed authority denied when right, and parent C1–C5. For **every** card also score the fixed first-ten-task holdout before and after the stream, worst-agent and rare-task accuracy, and the named old slice at the relevant write/expiry/handoff. Use the full deployed route, including misses, delay, fallback or abstention. Hold unchanged old tasks separate from intentional revisions; holdout labels never become renewal evidence. Enumerate exact histories where feasible; otherwise pair seeds, report uncertainty, and compare retention at matched current-task progress and cost.

## A. What to renew (#314#01)

### 01. Stop when the surviving explanations prescribe the same action (P)
- **Mechanism:** Partition explanations by the safe actions they allow at a designated old read. Renew one action when every surviving explanation allows it, even if some explanations are still unresolved. Publish the scope and the partition version, not a claim that one explanation won.
- **Novelty vs nearest prior art:** Controlled Sensing already supports decision risk; SHANGRLA audits sufficient assertions. The bet is that an action certificate can be reused by multiple asynchronous callers without carrying a globally resolved diagnosis.
- **Cheapest first test:** Enumerate four hypotheses, two probes and two caller deadlines. Compare best risk-weighted diagnosis with action certificates on equal bytes; include a caller for whom every remaining disagreement matters.
- **Old-task retention check:** Score unchanged short-deadline calls whose safe action is invariant, and callers outside that scope who require the unresolved distinction.

### 02. Lease an exclusion instead of a winner (P)
- **Mechanism:** Store evidence against an unsafe action under a particular caller context. A recomposed skill must consume that exclusion as a constraint even when none of the tested implementations is retained.
- **Novelty vs nearest prior art:** Reiter computes conflicts; Zep retains evidence of failures. The ledger killed self-sealing prohibitions and [The Memory Trap](https://arxiv.org/abs/2611.07554v1) documents overgeneralization. The extra operation is reuse of a bounded *action exclusion* across independently versioned planners, not avoiding retests or reviving permanent bans.
- **Cheapest first test:** Two planners share one unsafe shortcut but otherwise disagree. Compare verified failure retrieval and each planner's ordinary expiring deny rule plus matched sandbox retests; include a shortcut made safe by a real revision.
- **Old-task retention check:** Test unchanged old tasks served by alternate routes and an adjacent old context where excluding the shortcut wrongly causes a deadline miss.

### 03. Renew an interface pair without renewing either endpoint (P)
- **Mechanism:** Make a receipt for the joint behavior of an ordered producer–consumer version pair. An endpoint that passes a solo trial cannot replace either half of the pair unless an interface-preserving witness covers the substitution.
- **Novelty vs nearest prior art:** SkillClaw compares full workflows, MultiEvoSkill binds claims to graph elements, and provenance records joint derivations. The bet is renewal of a specific edge across different graph versions and workflows, not graph scoping by itself.
- **Cheapest first test:** Use two producers and two consumers whose solo tests pass but one pair disagrees about units. Compare full-path and per-clause checks at fixed R; include an environment where the interface never varies.
- **Old-task retention check:** Replay normal old routes using both matched and cross-version endpoints before and after an endpoint upgrade.

### 04. Renew a compound contrast with two locally useless views (P)
- **Mechanism:** Two sites each observe a binary response that has the same marginal law under both rivals. Only the parity from synchronized observations of the same event separates them; renew one interaction claim from the pair, not two claims from the marginals.
- **Novelty vs nearest prior art:** Controlled Sensing can treat the pair as one experiment and Adaptive Submodularity is not guaranteed with complementary evidence. The bet is a reusable joint receipt under asynchronous joining, not that parity is novel.
- **Cheapest first test:** Enumerate matched bits with equal marginals but opposite parity; compare greedy marginal probes, a lawful paired-probe scheduler, and shuffled joins. Count correlation or timing IDs in bytes.
- **Old-task retention check:** Score the old composite workflow after delayed joins and unrelated single-site workflows that should gain no authority.

### 05. Split only at the action boundary (P)
- **Mechanism:** A counterexample after renewal partitions callers by which action their controller would take on the failure, not by surface similarity. Keep the existing receipt only on scopes with a valid invariance witness.
- **Novelty vs nearest prior art:** #314#05 splits on counterexamples and Transportability formalizes invariance. The narrower bet is that action equivalence gives a smaller transferable renewal partition than model or context equivalence.
- **Cheapest first test:** Five callers share the same apparent failure; a hard local guard makes it decision-changing for only two. Compare full eviction, context splits, and a guard-based split; include a guard that silently changes next round.
- **Old-task retention check:** Count live service for guarded old callers and false accepts on unchanged unguarded callers that expose the bad branch.

### 06. Test the one receipt whose expiry would strand an old caller (P)
- **Mechanism:** Work backward from lawful substitute routes to find evidence whose expiry would cut *all* timely paths for an old caller. Schedule the cheapest fresh separating check on the cut rather than the report with the oldest timestamp.
- **Novelty vs nearest prior art:** #314#10 already checks a planned path; diagnosis and provenance already express cut-like combinations. The bet is scheduling on the deadline-sensitive cut across routes that have not yet been chosen.
- **Cheapest first test:** A three-route toy service has one shared expiring interface and two expiring leaves. Compare oldest-first, utility-weighted sensing, and exact causal scheduling; include a live leaf-only route that destroys the cut.
- **Old-task retention check:** Measure late and failed service on the low-frequency caller with no timely substitute and on the old callers whose checks were deferred.

### 07. Combine receipts only if their uncertainty combines (P)
- **Mechanism:** Attach the admissible *joint* error constraint to cooperating certificates. If two sites share drift or verifier calibration, compare the joint worst case rather than multiplying reported reliability or treating a shared event as two trials.
- **Novelty vs nearest prior art:** Provenance Semirings encode common derivations, not calibrated joint errors for action authority. The claim is useful bounds when lineage is shared but known coupling is tighter than the no-assumptions bound.
- **Cheapest first test:** Enumerate shared and independent verifier noise with the same marginal error. Compare lineage deduplication plus conservative union bounds, exact small joint models, and naive independent pooling.
- **Old-task retention check:** Check rare old composite calls for correlated wrong renewals and easy old calls for false denial caused by an overly loose bound.

### 08. Collect a witness of non-identifiability with the rejection (P)
- **Mechanism:** When no legal probe separates an action-changing pair, return the two hypotheses and their equal response laws over the *current* legal menu. Reopen only when a dated scope, verifier or menu change breaks the witness.
- **Novelty vs nearest prior art:** Controlled Sensing already implies indistinguishable alternatives cannot be tested. The bet is using that negative certificate to suppress redundant fleet traffic without suppressing legitimate later evidence.
- **Cheapest first test:** Enumerate a menu with no separating action for ten rounds, then add one legal branch. Compare capped retries, cached diagnostics with TTL, and witness-triggered retries; include a change invisible to the witness holder.
- **Old-task retention check:** Measure old fallback service while the pair is unresolved and time to resume former service once a real distinction is available.

### 09. Make expiry relative to the rival that could return (P)
- **Mechanism:** Retain separate validity horizons for eliminated alternatives with distinct drift laws. Renew caller authority against the set of alternatives that can plausibly return by its next use, not the earliest expiry of an irrelevant rival.
- **Novelty vs nearest prior art:** Gray–Cheriton leases and ordinary changepoint models price time or drift; #314#08 already orders evidence. The bet is action-specific expiry derived from changing rival sets at matched false-authority rates.
- **Cheapest first test:** Give a fast-changing rival and a persistent rival opposite relevance to two callers. Compare min-TTL and a fresh changepoint filter plus leases; include misspecified fast drift.
- **Old-task retention check:** Score the rare old caller after the fast rival's first return and measure avoidable expiry for the unaffected caller.

## B. What a committed audit can establish (#314#09)

### 10. Commit to the whole response surface, not just the drawn answer (P)
- **Mechanism:** Commit a compact mapping from eligible branches to predictive distributions and the default/no-response case; renew scope only under a predeclared contrast across the mapping. One sampled branch cannot certify every entry.
- **Novelty vs nearest prior art:** NIST already fixes the randomized procedure; Controlled Sensing already fixes observation laws. The bet is that response-map commitments save later probe budget across audiences relative to per-audit commitments, without paying for spurious sharp predictions.
- **Cheapest first test:** Enumerate three harmless synthetic branches and an agent that can fit any disclosed branch. Compare point commitment, full table, and small parameterized map at equal bytes; include branches with identical predictions.
- **Old-task retention check:** Test unchanged workflows on branches the map compressed poorly, including the initial call on a branch not yet sampled.

### 11. Charge an opened audit that somehow failed to finish (P)
- **Mechanism:** Track assigned branches through completion, time-out, refusal and missing log. Renew only if the conclusion survives the worst admissible completion of censored outcomes, or a predeclared and justified missingness bound.
- **Novelty vs nearest prior art:** Selective inference warns against conditioning after selection; SHANGRLA addresses risk-limiting assertion tests. The fleet operation is a receipt that carries the censoring liability to downstream readers rather than letting each receiver see only returned successes.
- **Cheapest first test:** Enumerate one true and one false skill with equal observed success but different branch-dependent silence. Compare complete-case audit, missing-as-fail, and exact partial-identification bounds; include innocuous random time-outs.
- **Old-task retention check:** Score old tasks routed through genuinely slow agents as well as those routed through falsely renewed agents that selectively go silent.

### 12. Commit before assignment, blind through execution (P)
- **Mechanism:** In a harmless sandbox, randomize whether the executor sees the diagnostic assignment or only an observationally matched interface. The sealed forecast is the same in both arms. Renew prediction-only scope on blinded executions, and treat the disclosed–blinded gap as a separate claim.
- **Novelty vs nearest prior art:** Beacon commitments prevent pre-draw tailoring, not post-draw action changes; ordinary blinded trials already address disclosure. The bet is a transferable distinction between evidence of forecasting and evidence of successful disclosed control.
- **Cheapest first test:** A toy agent can force its predicted flag when assignment is shown but cannot alter the blinded read. Compare standard random auditing plus verification, always-blind, and graded scope; include a leakage arm.
- **Old-task retention check:** Score old autonomous calls without audit instructions separately from old calls that legitimately need an instruction to succeed.

### 13. Bind a draw to its pre-action world snapshot (P)
- **Mechanism:** Define an auditable tuple of eligible state, execution snapshot and response deadline. Late results can support the declared snapshot but not recertify a new state; record snapshot drift rather than discarding inconvenient branches.
- **Novelty vs nearest prior art:** NIST timestamps the random pulse and Switchback Experiments model lag. The bet is a cheap receipt that prevents asynchronous agents from laundering old responses into current authorization, while avoiding a global barrier.
- **Cheapest first test:** Enumerate delayed arrivals and one world flip between assignment and execution. Compare timestamp TTL, all-site barriers, and state-bound receipts, including hidden drift not captured by the snapshot.
- **Old-task retention check:** Measure unchanged old workflows with delayed verifiers and old tasks whose progress is threatened by a false post-flip authorization.

### 14. Audit the action sequence rather than the last branch (P)
- **Mechanism:** Commit predictions for two permissible orders of the same harmless operations. A fresh randomized order can renew an order-sensitive interaction only when carryover is included in the forecast and measured support.
- **Novelty vs nearest prior art:** Switchback Experiments already identify effects under carryover. The bet is to use a validated carryover difference as narrowly transferable evidence for future orders, not use randomization to pretend carryover is absent.
- **Cheapest first test:** Enumerate two operations that commute for one tool version but not another; compare single-branch audits and a matched switchback estimator. Include carryover beyond the proposed scope.
- **Old-task retention check:** Test old workflows in both historical orders, including the first call immediately after an audit could leave a changed state.

### 15. Separate an independent verifier from an independent outcome (I)
- **Mechanism:** Run a paired harmless challenge where a second verifier reads the same outcome and another where one verifier reads a separate independently executed outcome. Estimate measurement agreement and replication separately.
- **Novelty vs nearest prior art:** Zep tags strength by verifier and #314#17 distinguishes noise sources. This is a diagnostic for how those two operations should affect renewals, not a new estimator or a claim that independent readers imply independent trials.
- **Cheapest first test:** Enumerate correlated world shocks and independent reader errors, then swap the noise sources. Compare identity weighting and event-ID deduplication with matched checks.
- **Old-task retention check:** Test old tasks whose apparent multiple endorsements all measured one transient shock, and stable old skills from noisy readers.

### 16. Do not renew outside the common menu (P)
- **Mechanism:** Pin a pre-draw menu common to the lawful executions of compared policies. Separately log eligibility, assignment and execution, and permit a narrower claim when a selected branch lacks support in one policy; never silently substitute a convenient branch.
- **Novelty vs nearest prior art:** Controlled Sensing already defines the experiment menu. The bet is portable support constraints for different private fleets with action-dependent menus, rather than estimating a nonexistent common effect.
- **Cheapest first test:** A rare branch is legal for both policies until one changes state; compare intention-to-treat on valid common assignments, re-randomizing eligible draws, and a scope-aware refusal. Include disjoint menus.
- **Old-task retention check:** Measure rare old workflows that still need the disappearing branch, and unchanged workflows on the common menu.

### 17. Split audit feedback from the power to learn its answers (P)
- **Mechanism:** Give learners a coarse acceptance message, with the detailed diagnostic retained by a separate authority that can schedule fresh draws. Charge how much adaptation is possible from repeated accepts, rather than assuming a hidden answer stays hidden.
- **Novelty vs nearest prior art:** The reusable holdout already limits feedback leakage. The candidate object links a receiver's allowable feedback to a lease and asks whether coarse renewal plus targeted fresh diagnostics can preserve more live skills than standard reusable testing.
- **Cheapest first test:** Enumerate an adaptive rule selector that learns a four-bit verifier from repeated queries; compare fresh-only audits, binary feedback, and a matched reusable-holdout control with a new world drawn after the selection.
- **Old-task retention check:** Test old skills that need useful debugging feedback and unchanged held-out variants that an audit-adapted rule could no longer solve.

## C. What the fleet can share without multiplying evidence (both seeds)

### 18. Prove a bridge is diagnostic on both sides before transferring a receipt (P)
- **Mechanism:** Share a prospective audited contrast only if each recipient can show that its local hypotheses map the randomized branches and measured outcomes to the same action distinction. A subsequent map change revokes only the recipient's use.
- **Novelty vs nearest prior art:** Transportability already handles cross-domain identification and #314#03 leases translations. The narrower bet is that a bridge for a specific contrast is cheaper than translating full skills or causal models and more useful than ordinary per-site audits.
- **Cheapest first test:** Two toy schemas share a permuted response table until one adds a hidden fallback. Compare site trials, a passed full-schema mapping, and paired diagnostic mapping at equal R.
- **Old-task retention check:** Score old recipes on both sides after the fallback changes, including those that never used the translated branch.

### 19. Send a decision bracket instead of the audit trace (P)
- **Mechanism:** Transmit error-valid lower and upper summaries for unresolved rival contrasts; receivers can renew only if their own action threshold lies outside the bracket. Ask for refinement on a near-threshold call, without treating it as a new observation.
- **Novelty vs nearest prior art:** Distributed Monitoring tracks approximate statistics and confidence sequences handle repeated looks. The candidate combines them around heterogeneous actions and priced precision requests, rather than broadcasting one stopping decision to all sites.
- **Cheapest first test:** Three agents use distinct thresholds for a shared contrast. Compare full traces, fixed precision and adaptive refinement; include nearly coincident thresholds that force full precision.
- **Old-task retention check:** Score rare old calls nearest their thresholds, including when a refinement arrives after the normal deadline.

### 20. Reserve an audit for the verification opportunity a write would erase (P)
- **Mechanism:** Before authorizing a write that removes an old diagnostic route, reserve a lawful future distinguishing sample, or decline to grant that write durable authority. Choose the reservation by comparing old reads that would be untestable after deployment.
- **Novelty vs nearest prior art:** #314#22 reallocates checks after the live policy stops observing a slice; [#313#22](https://github.com/manojbajaj95/cl/pull/313) downgrades edits that disarm their own test. The bet is preserving a future opportunity for a *different* agent by reserving it before the write; stack the support gate with ordinary advance scheduling.
- **Cheapest first test:** Two writes improve a new task equally; one makes a rare old branch unreachable unless an independent sandbox slot was reserved. Compare random audits plus expiry, exact lookahead, and a world where no reservation can preserve the branch.
- **Old-task retention check:** Score ordinary old reads at the first loss of support and after expiry, not just the old case replayed in the sandbox.

### 21. Reject joint deployment even when both local audits pass (P)
- **Mechanism:** Attach forbidden co-exercise conditions to individually valid receipts when one agent's write changes which explanation a peer's live probe can distinguish. Check joint deployment rather than propagating a static dependency alert.
- **Novelty vs nearest prior art:** Mediation and interaction analyses separate direct and joint effects; MASkills assigns contribution using an individual omission counterfactual. The bet is enforceable cross-agent compatibility under joint deployment, not a new credit assignment rule.
- **Cheapest first test:** Two individually audited updates both cause the same success flag when combined, masking one failure. Compare independent leases, full factorial audits, and a predeclared interaction witness; include a truly compatible pair.
- **Old-task retention check:** Test old caller families exposed only to the combined rollout and those harmed by unnecessary mutual exclusion.

### 22. Test a completion claim against lawful refusal worlds (P)
- **Mechanism:** Commit not only to successful output but to which branches require saying “no valid recommendation.” Renew action and abstention scopes separately; actually serving the case remains necessary for old service credit.
- **Novelty vs nearest prior art:** Controlled Sensing allows risk-constrained decisions, and Zep preserves failures. The bet is separately shareable evidence of calibrated refusal for a composable skill, not relabeling abstention as accuracy.
- **Cheapest first test:** Randomly choose among two solvable cases and a harmless impossible case; compare binary verification, a standard selective classifier, and scoped certificates at matched coverage.
- **Old-task retention check:** Score unchanged solvable old cases that resemble the impossible case, plus old cases where unsafe fallback is worse than abstention.

### 23. Order the audit broadcasts to avoid spending the evidence twice (P)
- **Mechanism:** Publish assignment metadata or a coarse status first. Permit a late-arriving agent's forecast to use an existing outcome only if the outcome (and any informative status) was still hidden when it committed, with coverage computed for the joint use.
- **Novelty vs nearest prior art:** NIST handles commitment ordering, and selective inference handles post-selection validity. The bet is a small, causal disclosure transcript that recovers legitimate late forecasts without an all-sites barrier or pseudo-independent confirmations.
- **Cheapest first test:** Enumerate out-of-order commits and a status bit that leaks the result on one branch. Compare global barriers, fresh-only checks and exact selection-aware inference; log timestamps and dependencies in bytes.
- **Old-task retention check:** Score old tasks at slow receivers, both for missed renewals and for false renewals after an informative early leak.

### 24. Detect a wrong menu of explanations before renewing any winner (P)
- **Mechanism:** Commit both a rival-separating forecast and a falsification condition shared by the entire named family. If fresh challenge results violate the common bound, freeze relevant authority and request a new forecast family rather than choosing the least wrong rival.
- **Novelty vs nearest prior art:** Reiter finds inconsistencies, and simultaneous inference can test several hypotheses. The bet is reusing a shared family-failure receipt to reopen only affected action permissions, not restarting every skill's diagnosis.
- **Cheapest first test:** Two forecasts distinguish ordinary branches but both fail on a legal third behavior. Compare residual monitoring plus leases, best-rival renewal and selective reopening; include a noisy but correctly specified family.
- **Old-task retention check:** Test old calls in the violated scope and unchanged old calls outside it during the freeze and subsequent requalification.

### 25. Price the right to repurpose a receipt before seeing the result (P)
- **Mechanism:** A recipient preregisters alternative uses of one audit (different directions, callers or thresholds). Its reuse envelope accounts for the actual joint decision rule; after reveal, a new use requires valid selective inference or fresh evidence.
- **Novelty vs nearest prior art:** #314#25 assigns finite coverage rights and Confidence Sequences handle repeated looks, not arbitrary post-hoc targets. The proposed difference is pricing scope by the correlation of *predeclared* renewal decisions, not a flat reuse counter or a new independent vote.
- **Cheapest first test:** Two callers' renewal rules are identical in one world and oppose each other in another. Enumerate exact false-authority rates; compare a flat cap, multiplicity correction, exact joint testing and fresh-only audits.
- **Old-task retention check:** Track unnecessary expiry on near-duplicate old callers and false renewal when the ordinary old callers' interests actually diverge.

### 26. Replace a disappearing discriminator with a prospectively paired proxy (P)
- **Mechanism:** When an old diagnostic is due to vanish, overlap its final legal uses with a candidate successor test. Swap only the action contrasts the pair can support under an explicit invariance bound; let the rest expire.
- **Novelty vs nearest prior art:** Transportability requires assumptions for moving evidence and #314#03 tests translation between callers. The bet is buying *continuity of verification* across a change in available probes, without relying on correlation or retaining the old probe indefinitely.
- **Cheapest first test:** One binary read is removed after a brief overlap; the new read agrees on head traffic but reverses on a rare context. Compare re-audit at cutover, static proxy substitution, and prospective paired probes at equal cost.
- **Old-task retention check:** Test the first normally routed old call after the cutover on both the supported and unsupported slices, with delay or fallback counted.

## Deeper questions, ranked

1. **What is the smallest evidence object that can authorize a read without settling the diagnosis?** Start with 01, 03 and 04. Can an action-level certificate retain more old service than an equally informed, risk-weighted diagnostic policy plus ordinary leases? A tie with the same probes and cheaper ordinary bookkeeping would reduce this to a change of representation.
2. **Can a fleet keep diagnostic support alive when new writes change what it gets to see?** Combine 11, 16, 20 and 26. Compare prospective reservation with a randomized audit plus standard support accounting; include a system where there is no legal way to preserve a distinguishing branch.
3. **When can two audited permissions be exercised together or across callers?** Pair 07, 18 and 21. Can a small interaction or coupling certificate beat exhaustive joint audits at fixed bytes and R without failing on correlated drift and rare old routes?
4. **Can asynchronous sharing reuse a draw without enabling post-hoc claims?** Combine 12, 17, 23 and 25. Account for missed assignments and everything receivers observe before committing. Test whether any gain survives comparison to a lawful centralized audit log with fresh draws and calibrated selective reuse.
