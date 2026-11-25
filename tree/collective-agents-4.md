# Collective agents IV: keep the exclusion, retire the implementation

**Status:** Ideas only; no implementation, learner runs, or GPU work. **Parent:** [Collective agents III](collective-agents-3.md) ([PR #316](https://github.com/manojbajaj95/cl/pull/316)). **Review seeds:** [Flood triage, lines 434–437](https://github.com/manojbajaj95/cl/blob/046ce92971d3e1a19026e21bcbfa778785999d76/reviews/flood-triage.md#L434-L437) on [PR #6](https://github.com/manojbajaj95/cl/pull/6), with #316 on line 434: score-3 [#02, lease an exclusion instead of a winner](collective-agents-3.md#02-lease-an-exclusion-instead-of-a-winner-p) and [#21, reject joint deployment even when both local audits pass](collective-agents-3.md#21-reject-joint-deployment-even-when-both-local-audits-pass-p).

**Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/046ce92971d3e1a19026e21bcbfa778785999d76/reviews/idea-ledger.md). Self-sealing prohibitions, prohibition rebound, counterexample-guided lesson rewriting, unlabeled hybrid-skill identity contracts, and sparse coded merge audits are not revived here. Expiry and occasional exploration are controls; absence of violations under a guard is not fresh evidence for that guard. **P** marks a candidate reusable object or operation; **I** an improvement or diagnostic, not a new primitive.

## What would have to be new?

Keep two claims separate: **an action is harmful in a caller context**, and **a deployment prevents us from checking a distinction in time to serve that caller**. The second does not establish the first. A negative receipt should say which claim it supports, what action or probe it covers, what counts as fresh evidence and when that evidence ceases to travel. A deployment limit should be able to block one use without retiring every skill involved. If an ordinary shield plus versioned rules and matched joint audits retains the same old service at the same cost, there is no new primitive here.

## Literature check

Searched the Hugging Face papers index for runtime shielding, assume–guarantee reasoning, procedural skill validation, interference designs and drift-aware risk control; checked the linked arXiv abstracts directly (including prior work inherited from the parent). These are novelty hypotheses against specific controls, not claims of priority.

- **Enforcement and composition:** [Aegis (2410.05641)](https://arxiv.org/abs/2410.05641) uses counterexample-guided synthesis and Bayesian optimization to produce permissive runtime shields. [Formal Policy Enforcement for Agentic Systems (2602.16708)](https://arxiv.org/abs/2602.16708) already checks Datalog policies against event graphs at action time. [Compositional Shielding (2410.10460)](https://arxiv.org/abs/2410.10460) decomposes global safety into local assume–guarantee obligations. [Coordination Avoidance (1402.2237)](https://arxiv.org/abs/1402.2237) characterizes when operations can merge without violating an invariant. Use these as controls, not as unexplored design space.
- **Trace evidence:** [TriCEGAR (2601.22997)](https://arxiv.org/abs/2601.22997) learns and refines predicate abstractions for probabilistic model checking. [Mining Beyond the Bools (2603.06710)](https://arxiv.org/abs/2603.06710) jointly mines transformations and temporal specifications from traces. [FailBank (2609.39820)](https://arxiv.org/abs/2609.39820) turns runtime corrections into guarded policy updates. A better predicate, richer trace rule, or distilled shield is not by itself a new lease operation.
- **Skill evolution:** [Zep (2611.01386)](https://arxiv.org/abs/2611.01386) attributes skill fields to verified trace events; [SkillClaw (2604.08377)](https://arxiv.org/abs/2604.08377) synchronizes collectively evolved skills; [MultiEvoSkill (2610.34260)](https://arxiv.org/abs/2610.34260) uses typed skill graphs and dependency-aware edits. [The Memory Trap (2611.07554)](https://arxiv.org/abs/2611.07554) documents overgeneralization across contexts. Sharing a failure trace or attaching a guard to a skill graph is not sufficient novelty.
- **What a probe can establish:** [Independent-Set Design (2312.04026)](https://arxiv.org/abs/2312.04026) controls interference exposures in experiments; [Active Interventions (2109.02429)](https://arxiv.org/abs/2109.02429) selects interventions to learn causal structure. [Confidence Sequences (1810.08240)](https://arxiv.org/abs/1810.08240) bound time-uniform uncertainty under their assumptions, and [Non-Exchangeable Conformal Risk Control (2310.01262)](https://arxiv.org/abs/2310.01262) handles monotone losses under non-exchangeability with drift penalties. Neither turns a missing branch or a masked outcome into evidence.

## First-test contract

- Inherit the [parent contract](collective-agents-3.md#first-test-contract), including private local views, parent C1–C5, and the legally informed centralized control. Use enumerable two-to-four-agent CPU fixtures before any learner. Predeclare context, action semantics, evidence scope, tolerable harm, eligible interventions, exposed peer versions, canary support, and deadline. When randomizing, seal forecasts and the assignment policy first; log assignment, completion or censoring, and evidence ancestry. No support means no inferred clearance; expiry means unknown, not safe.
- Compare #314's claim renewal and independent receipts, winner retention, static blocklists, ordinary expiring exclusions, static dependency alerts, and fresh joint re-audits. Stack the strongest applicable ones with a permissive shield, scoped risk estimator or assume–guarantee monitor as appropriate, with the candidate's lawful information and acquisition schedule. Match real verifier calls, staging time, exposure, message/state bytes, and compute; report noncompliance and delay. An oracle that sees hidden labels or does more audits is a ceiling.
- Every card measures the fixed first-ten-task holdout before and after the stream, rare and worst-agent old-task service, new-task progress, false exclusions and missed harmful actions, and lost verification opportunities. Test the named old slice on the deployed route at the write, recomposition or expiry boundary; a timeout, unnecessary refusal or late fallback can fail an old task. Keep intentional revisions separate. No retention labels renew authority.

## A. Make exclusions outlive their winners (#316#02)

### 01. Transfer a prohibition by the effect, not the opcode (P)
- **Mechanism:** Store a negative receipt against a caller-visible effect such as losing an unresolved item. A recomposition must either map each relevant trace to the old effect vocabulary or request a new check at the first unmapped operation. Transfer the evidence without the plan that generated it.
- **Novelty vs nearest prior art:** Aegis enforces a supplied safety property and MultiEvoSkill gives edits a typed structure. The bet is a checkable translation of *empirical exclusion evidence* between unrelated skill graphs, not semantic shielding itself.
- **Cheapest first test:** Retire two tiny list handlers and replace them with a batch handler that sometimes drops a pending item. Compare keeping the winner, opcode and semantic deny rules with expiry, and an Aegis-style shield at equal audits; include a batch handler that genuinely preserves the item.
- **Old-task retention check:** Score old two-item handoffs that require the batch handler to meet the deadline and pending-item calls where the translated veto should still fire.

### 02. Demand a recovery witness, not a blanket exception (P)
- **Mechanism:** If a risky intermediate effect is recoverable in a private staging area, let a new planner discharge the inherited veto with a checked, timely recovery route before the first externally visible commitment. Invalidate that discharge if its recovery path changes, leaving the exclusion intact.
- **Novelty vs nearest prior art:** Aegis already tries to intervene permissively. The bet is separate expiration of negative evidence and a replaceable, proof-bearing recovery route, compared with the same recovery state built into a conventional shield.
- **Cheapest first test:** Enumerate allocate–revert–publish histories with slow or missing revert. Compare no exceptions, a fresh recoverability shield and the paired receipts; charge proof checking and include irreversible publication.
- **Old-task retention check:** Score old workflows needing provisional allocation as well as the old readers that could otherwise see an irreversibly incomplete result.

### 03. Consume a veto at the last point where it can still be enforced (P)
- **Mechanism:** Instead of rejecting a plan at its first possibly harmful step, pass a pending exclusion through nondestructive work; the receipt identifies the latest observable boundary where a legal continuation remains available. Stop before that boundary if its preconditions become unknown.
- **Novelty vs nearest prior art:** Event-graph enforcement can already check trace prefixes. The candidate object is a portable handoff of *when* a planner must resolve a veto, with the cost of missing the last intervention assigned to the planner that advanced the state.
- **Cheapest first test:** Recompose a three-step sorting workflow where inspection before packing reveals the correct route, but a new order packs first. Compare early veto, an equivalent temporal shield, and delegated boundary checking.
- **Old-task retention check:** Count routine old requests that need early preparation and rare requests for which delayed vetoes leave no timely alternative.

### 04. Distinguish a veto on using an action from a veto on forwarding its result (P)
- **Mechanism:** A negative receipt can constrain the output's use rather than its production; let a planner keep using a crude estimate for local planning but require that a consumer obtain independent evidence before using it to finalize a decision. Propagate the restricted-use label through simple derived outputs.
- **Novelty vs nearest prior art:** Formal Policy Enforcement can encode event-graph use restrictions; Zep stores cited evidence. The test is whether versioned, empirically renewed downstream-use restrictions convey useful scope across opaque planner replacements versus a static purpose label plus re-audit.
- **Cheapest first test:** Two estimate sources tie on averages; one fails on boundary cases consumed by a rare downstream caller. Compare all-or-nothing disablement, static scoped rules and restricted forwarding at fixed audits.
- **Old-task retention check:** Test unchanged internal estimates and old final-review tasks that should stop trusting the estimate even after an intermediate agent relabels it.

### 05. Quarantine a veto conflict without inventing a winning action (P)
- **Mechanism:** When two live, independently scoped exclusions remove each other's alternatives, issue a conflict record with an admissible fallback, if any, and the smallest set of observations that could reopen a timely action. Neither evidence source is overwritten; outside the overlap both retain their force.
- **Novelty vs nearest prior art:** Compositional Shielding already reasons about whether local obligations suffice for global safety. The bet is a runtime conflict record that directs fresh acquisition while preserving the contributing exclusions for unrelated callers.
- **Cheapest first test:** Two sites ban different routes for overlapping caller slices and an inexpensive third observation resolves one veto in some worlds. Compare most-recent-wins, unsatisfiable-core reporting plus random rechecks, and conflict-directed checks; include an overlap with no lawful route.
- **Old-task retention check:** Score deadline failures in the overlap and service for each unaffected old slice while the conflict is unresolved.

### 06. Let an observation channel retire before its negative evidence does (P)
- **Mechanism:** Separate the horizon of the harmful effect from the lifetime of the probe used to establish it. A signed change in the observation interface ends renewal through that channel but need not cancel the short, already earned interval of action exclusion. Any evidence known to be invalidated retracts immediately.
- **Novelty vs nearest prior art:** Drift-aware risk control already weights dated observations; parent #26 tests a successor proxy. Here there may be no replacement probe: the operation separates evidence validity from renewable access, tested against two ordinary TTLs.
- **Cheapest first test:** Remove a toy verifier while an independently justified effect bound still holds; vary whether the verifier removal coincides with an effect change. Compare synchronized expiry, independent TTLs, and condition-specific invalidation under equal information.
- **Old-task retention check:** Score old exposed calls during the verification gap and legitimate old calls after an effect-changing cutover.

### 07. Let a local legacy path narrow a global exclusion without overruling it (P)
- **Mechanism:** Give a caller a checked, expiring proof that its path cannot reach the receipt's harm predicate. It gets no general permission to take the action; each invocation must prove the same local invariant without disclosing the entire path.
- **Novelty vs nearest prior art:** Compositional Shielding already uses local guarantees to discharge obligations. The conjecture is that subtracting a locally proved scope from a fleet-wide empirical veto saves repeated broadcasts and full re-verification as legacy planners change.
- **Cheapest first test:** Construct a private workflow in which a read-only flag is immutable in one caller and mutable in another. Compare global refusal, local assume–guarantee checks with the same evidence and an applicability witness; include a stale flag schema.
- **Old-task retention check:** Score rare read-only legacy tasks and normal old mutable tasks on the first invocation after a schema change.

### 08. Test whether the guard actually protects the caller after recomposition (I)
- **Mechanism:** In a harmless fixture, seal the same candidate route before assigning direct veto, veto plus its proposed fallback, or a reference continuation. Separately measure a move of the harm to another step and the cost of lost service; do not count “guard fired” as protection.
- **Novelty vs nearest prior art:** FailBank already compares runtime corrections with useful outcomes. This is an attribution test for old callers under replacement, not a new way to learn corrections.
- **Cheapest first test:** In a synthetic queue, two fallbacks look equally safe at the blocked step but one creates the same error at handoff. Compare per-step violation counts with full-trajectory randomized execution, including a harmless fallback.
- **Old-task retention check:** Score complete old queue workflows and deadline loss in the no-harm arm, not merely the first corrected action.

### 09. Revoke a narrow transfer without revoking the source (P)
- **Mechanism:** Record the smallest set of assumptions introduced by a receiver while importing an exclusion. A failed assumption returns that receiver to local validation; it neither clears the source's veto nor invalidates other independently justified translations.
- **Novelty vs nearest prior art:** Zep cites evidence by field and TriCEGAR refines abstractions. The bet is evidence revocation by failed *translation step* through multiple receiving planners, not global repair of the learned context predicate.
- **Cheapest first test:** Three planners import an exclusion using either a shared unit converter or a private independent conversion. Change the shared converter; compare skill-wide recall, version-stamped policy maps, and selective invalidation at equal bytes.
- **Old-task retention check:** Check old calls at both dependent receivers for false denial or false clearance, and at the unaffected receiver for avoidable re-audit delay.

## B. Make co-deployment preserve what can be checked (#316#21)

### 10. Measure the contrast that vanishes, not just the outcome that stays good (P)
- **Mechanism:** A co-exercise receipt records a lower bound on separation between two rival response laws *under the proposed deployment*. If that bound is too small on a needed caller slice, suspend only the permission that depends on the contrast; keep unrelated permissions.
- **Novelty vs nearest prior art:** Active Interventions picks experiments for identification and Compositional Shielding composes safety obligations. The bet is a deployable diagnostic obligation with a distinct loss even when the observed service score is unchanged.
- **Cheapest first test:** Two local audits pass; a peer write forces the same completion flag under both rivals although final output is still correct on today's requests. Compare independent receipts, static alerts and matched joint audits that test both reward and separation; include a noninteracting pair.
- **Old-task retention check:** After a planted revision, score the old calls that depended on detecting it and the unrelated old calls that should continue normally.

### 11. Release the latest compatible pair rather than blacklist the agents (P)
- **Mechanism:** Record forbidden *version combinations* with the contrast that fails, and solve for a fresh set of versions that excludes only those combinations. Pinning a version is charged for new tasks it cannot handle; new versions do not inherit clearance from old aliases.
- **Novelty vs nearest prior art:** MultiEvoSkill has dependency-aware edits and Coordination Avoidance handles invariant-preserving merges. The narrower hypothesis is that evidence-supported incompatibilities can be reused across staggered rollouts better than ordinary version pinning plus re-audit.
- **Cheapest first test:** Three versions per agent; the earliest and newest mixed pairs pass while the newest pair masks a probe. Compare full rollback, dependency pinning, and an exact compatibility solver using the same joint observations.
- **Old-task retention check:** Score old probe-dependent calls during rollout and old callers for which an unnecessary global rollback loses a previously restored route.

### 12. Exclude a relative deployment order, not the final pair (P)
- **Mechanism:** Conditional clearance permits either stable configuration but bars one transition until a peer can collect a predeclared contrast. An acknowledgement grants passage only for the observed configuration and expires if another write intervenes.
- **Novelty vs nearest prior art:** Temporal specification mining and event-graph enforcers already express order. The candidate is reusing a verified *transition exclusion* when the steady-state compatibility matrix is unchanged.
- **Cheapest first test:** Both steady states are observable; writing A before B briefly erases the only cue of which transform ran. Enumerate all two-write orders and message delays; compare atomic updates, a static precedence rule and conditional order clearance.
- **Old-task retention check:** Score old requests arriving during the transition and at normal operation after both writes, including a fleet where the static order unnecessarily delays service.

### 13. Test whether a deployment kills a probe only during busy periods (P)
- **Mechanism:** Lease a minimum useful diagnostic opportunity by caller stratum and time-to-deadline, not just over all requests. Co-exercise is suspended only for obligations starved in the relevant stratum; quiet-period evidence cannot automatically substitute.
- **Novelty vs nearest prior art:** Independent-Set Design targets interference exposure, and parent #20 preserves future opportunities. The bet is detection of *conditional* starvation without reserving any extra diagnostics beyond the same joint audits.
- **Cheapest first test:** Give two old caller types opposing traffic peaks; a cache write makes probes finish late only when both are busy. Compare throughput-based gating, stratified randomized audits, and per-deadline obligations at equal audit count.
- **Old-task retention check:** Score old peak-time tasks that determine the shortage and old quiet-time tasks that should not suffer a global freeze.

### 14. Separate a third write that masks the test from one that changes the answer (P)
- **Mechanism:** For a suspected three-way incompatibility, factor the prospective joint test into an intervention on the observed diagnostic and a separate read of the caller outcome. Use the contrast pattern to distinguish changes in the measurement path from genuine changes in the underlying behavior.
- **Novelty vs nearest prior art:** Active Interventions already targets informative manipulations; joint factorial tests already identify interactions with support. The candidate is a portable negative receipt whose effect-versus-measurement distinction prevents unnecessary rollback, not sparse pairwise reconstruction.
- **Cheapest first test:** Enumerate all eight configurations: one three-way combination masks a flag; in a second world it genuinely repairs the old route. Compare pairwise alerts, full factorial checking and a predeclared paired read within the same audit budget; include a world with no independent read.
- **Old-task retention check:** Score old callers after legitimate repair, and after a masked rather than repaired failure, with rare joint exposure represented explicitly.

### 15. Put a co-exercise limit on the observer's actual control mode (P)
- **Mechanism:** A peer's controller can be advisory or authoritative. A joint receipt names in which mode its recommendations can change the contrast; moving from advice to action requires separate clearance even if the emitted recommendation is unchanged.
- **Novelty vs nearest prior art:** FailBank explicitly separates observe-only feedback from policy control; Compositional Shielding can model both. The bet is a mode-specific lease that preserves diagnostic use of an improvement before its execution permissions are known.
- **Cheapest first test:** Run a tiny routing scheduler where recommendations are equally accurate in both modes, but automatic routing removes one branch from a peer's verifier. Compare always-off, always-on, and staged mode control plus the same joint audit schedule.
- **Old-task retention check:** Score old calls helped by immediate advice and old rare calls for which automatic routing masks a later error.

### 16. Include a semantic check for false “independence” in the compatibility key (P)
- **Mechanism:** An agent may publish a counterexample to a claim that two updates use disjoint channels by showing that both change the same caller-visible diagnostic variable, without sharing local traces. A proven alias merges the affected keys and triggers one joint check.
- **Novelty vs nearest prior art:** TriCEGAR refines a state abstraction and Coordination Avoidance reasons over shared invariants. The proposed operation corrects an asynchronously maintained compatibility index when *distinct registered channels* turn out to resolve to the same observation.
- **Cheapest first test:** Two apparently separate fields share a default lookup in one world but not another. Compare named dependency alerts, centralized alias analysis on the same exposed data, and witness-triggered joint audits at fixed R.
- **Old-task retention check:** Score old callers relying on the shared default and old callers on genuinely separate channels after the alias report.

### 17. Admit a substitute diagnostic only if it catches the same bad deployment (P)
- **Mechanism:** A co-deployment may proceed if a substitute probe separates the same deployment-relevant rival pairs by the same old deadline. Clear only those rivals; a proxy that only agrees on compatible configurations gets no clearance.
- **Novelty vs nearest prior art:** Parent #26 prospectively pairs a disappearing probe with a successor; Active Interventions chooses experiments for identification. The narrower bet is a substitute conditional on the joint configuration, reusable across updates that share the same failure mechanism.
- **Cheapest first test:** Compare a proposed proxy with the original on compatible and incompatible sandbox deployments. Include a proxy that correlates perfectly on compatible traffic only; match paired-audit counts against fresh joint re-audit and static proxy substitution.
- **Old-task retention check:** Score first old calls after co-deployment on the incompatible slice and on unchanged slices where rejecting the substitute delays a useful write.

## C. Make both kinds of negative evidence work together

### 18. Require one deployable route, not just a set of locally safe choices (P)
- **Mechanism:** Before admitting another veto or compatibility limit, search for a timely old route whose action and diagnostic obligations can be met together. If none is known, stage the write without granting live authority; report whether the blocker is harm evidence, lack of observation, or deadline.
- **Novelty vs nearest prior art:** Compositional Shielding handles joint safety and permissiveness; parent #06 schedules expiring evidence on a route cut. The bet is better attribution and repair when *exclusion plus lost verification* creates a cut that neither creates alone.
- **Cheapest first test:** Two old routes: one newly vetoed, the other permitted only while an observable contrast survives. Compare a permissive shield plus independent leases, exact deadline scheduling with the same receipts, and the explicit combined cut.
- **Old-task retention check:** Measure old callers with no timely route and unchanged callers wrongly delayed by a stale cut.

### 19. Split the effect of a veto from the effect of losing its monitor (P)
- **Mechanism:** Where the fixture allows, cross a guard assignment with an independently assigned monitor path. A receipt can then attribute a changed result to guard enforcement, to missing measurement, or leave the effect unresolved if the assignments cannot be separated.
- **Novelty vs nearest prior art:** Interference designs and factorial experiments already estimate crossed effects. The bet is the downstream right to act on exactly one separable contrast, rather than either inheriting or discarding a full joint test.
- **Cheapest first test:** An exclusion shifts tasks to a queue a peer cannot observe. Run a 2×2 sandbox with and without an independent passive read; compare standard full joint audits plus scoped renewal with two distinct certificates at equal draws; include a read that changes scheduling.
- **Old-task retention check:** Score old cases misclassified as failures because they went unseen and old cases actually harmed by the reroute.

### 20. Roll back verification authority before rolling back the useful skill (P)
- **Mechanism:** On a compatibility violation, retract the affected source of renewal immediately but let already supported calls keep using the skill within their independently valid bounds. A fallback observer can restore renewal without reinstalling the predecessor; lost or contradicted action evidence still triggers the usual stop.
- **Novelty vs nearest prior art:** Zep gates active skill versions, and Compositional Shielding can synthesize local fallbacks. The hypothesis is that separate rollback units for evidence acquisition and service save real old work without preserving invalid action authority.
- **Cheapest first test:** A summarizer update improves a synthetic task but breaks a peer's detection rule. Compare full rollback, ordinary separate TTLs plus replacement auditing, and two-part authority rollback; include an update that invalidates both parts.
- **Old-task retention check:** Score ordinary old calls during the renewal outage and after an unrelated old action receipt expires.

### 21. Let the caller carry the denial reason across a failover (P)
- **Mechanism:** Send a compact witness that an action was denied for caller harm, or left unknown because one deployment masks the monitor. A backup can reuse the first as a veto and can resolve the second with its own admissible contrast; it must not turn either into the other.
- **Novelty vs nearest prior art:** Formal Policy Enforcement can follow event histories and Zep can export trace evidence. The candidate is interoperable failover semantics for negative authority, compared with shipping the same event graph and verifier log.
- **Cheapest first test:** Two sites deny the same request for different reasons; only the backup has an independent measurement. Compare retry-without-context, a status code plus ordinary recheck, and the two witness types at equal bandwidth and R.
- **Old-task retention check:** Test recoverable old calls under backup and rare blocked calls that should remain blocked after multiple handoffs.

### 22. Hold a pending write to the evidence scope it actually used (P)
- **Mechanism:** Stage a write with the specific exclusions it respects and observations on which it relies. At activation, revalidate those scopes against intervening writes, including other agents' newly published negative receipts; a stale observation requires a scoped recheck rather than whole-fleet validation.
- **Novelty vs nearest prior art:** Coordination Avoidance already identifies invariant-violating concurrent merges. The narrower question is whether a compact and versioned footprint of *what was observable* can shrink the necessary conflict set versus an equally informed serializable deployment process.
- **Cheapest first test:** Commit two synthetic updates made from the same old snapshot with delayed notices. Compare serial activation, atomic version checks plus joint retesting, and scoped activation; include two disjoint updates safe to overlap.
- **Old-task retention check:** Score old calls during the stale-snapshot window and normal calls waiting on unnecessary global serialization.

### 23. Preserve a dissenting implementation only when it can distinguish something (P)
- **Mechanism:** Keep an old implementation eligible for shadow testing only if its lawful behavior provides an outcome distinction for a live exclusion or joint constraint that no cheaper available route supplies. It gets no production permission from being a useful diagnostic.
- **Novelty vs nearest prior art:** SkillClaw compares candidates with incumbents; the parent preserves diagnostic opportunities. Here the incumbent itself is a paid, replaceable experiment, benchmarked against ordinary baseline retention plus active probe selection.
- **Cheapest first test:** Two retired handlers disagree only in one old context; one supplies an otherwise unavailable diagnostic until a new sandbox fixture arrives. Compare one frozen incumbent, active probe selection over all options, and explicit release of the shadow-only entitlement.
- **Old-task retention check:** Score ordinary callers affected by a false renewal after the incumbent is deleted and check that the old handler is never silently routed into live service.

### 24. Exchange two conditional vetoes without assuming either fleet was fully audited (P)
- **Mechanism:** Peers exchange which combinations of effect mapping and observability assumptions they have ruled out, which they can support, and where they have no result. Intersect the supported configurations without turning untested cells into clearances or transferring evidence between distinct caller slices.
- **Novelty vs nearest prior art:** Compositional Shielding already combines assumption–guarantee obligations; Non-Exchangeable Conformal Risk Control handles shifted evidence. The bet is a compact conditional boundary when only partial cross-fleet information may be shared, tested against ordinary assume–guarantee reasoning over the same data.
- **Cheapest first test:** Enumerate a private 2×2 table at each site with crossed unknowns. Compare union of negative lists, shared tables with ordinary expiry, and disclosure of only the boundary cells needed for the pending deployment.
- **Old-task retention check:** Score old federation calls on unknown intersections as well as site-local calls that should not lose a previously valid route.

### 25. Reject the shared abstraction before both receipt types fail together (I)
- **Mechanism:** Run a sealed synthetic sentinel where an action effect and a diagnostic flag have identical values in normal traffic but diverge on a legal edge case. A mismatch invalidates the common translation used by both receipt types, not the underlying verified traces.
- **Novelty vs nearest prior art:** TriCEGAR already refines trace abstractions; The Memory Trap documents scope errors. This is a negative test for correlated scope failure, not a claim to invent abstraction refinement.
- **Cheapest first test:** Alias two toy labels that disagree only on a rare handoff. Compare independent regression gates with a shared-scope sentinel at equal tests; include a world in which the labels really are interchangeable.
- **Old-task retention check:** Score old handoff calls facing false clearance and the unchanged high-frequency tasks affected by unnecessarily invalidating a shared representation.

### 26. Compile a replacement skill from what must remain possible, not from the old expert (P)
- **Mechanism:** Provide a new planner only supported exclusions and a specification of the probes and timely old routes it must leave possible. It proposes a fresh skill; independent verification of new behavior is still required. The old implementation and its successful trajectories are withheld.
- **Novelty vs nearest prior art:** Aegis synthesizes a permissive shield for a given policy, while MultiEvoSkill evolves a typed skill from experience. The ambitious bet is that portable negative evidence plus verification obligations can constrain de novo synthesis enough to recover useful behavior without an incumbent to copy.
- **Cheapest first test:** Enumerate tiny finite-state queue policies after deleting both incumbent implementations. Compare verified positives only, an ordinary shield plus joint-audit scheduler, and synthesis constrained by the paired receipt types at equal tests; include a world where negative evidence leaves too many policies.
- **Old-task retention check:** Use held-out, normally routed old tasks, including a rare route that requires a particular probe to remain useful, and count old variants that no compliant synthesized policy can serve.

## Deeper questions, ranked

1. **What survives a total change of implementation?** Start with 01, 07, 09 and 26. Is there a short, checked mapping that transfers scoped negative evidence and retains rare old service at lower verification cost than a semantic shield plus expiring rules and fresh re-audit? If the mapping requires reconstructing or retesting the old planner, the primitive fails.
2. **When is diagnosability an independent deployment obligation?** Start with 10, 14, 17 and 19. Hold present service fixed while varying whether a lawful probe can detect the first later regression. Compare matched ordinary joint audits that also measure separation; if explicit obligations buy no further timely retention, keep the audits and drop the new object.
3. **Can a fleet recover from negative evidence without forgetting it or making it permanent?** Combine 05, 06, 18 and 21. Explain a dead end, reopen the minimum legitimate scope, and still block the rare bad caller. Compare a permissive shield, a scoped TTL cache and active sensing together; include a dead end with no lawful intervention.
4. **Which checks really need coordination at activation?** Combine 11, 12, 22 and 24. Compare with serializable version activation and exact assume–guarantee checking on the same observable information. If the smallest sound footprint is every peer version or if rare-caller delays erase the gain, prefer the simpler centralized gate.
