# Brain mechanisms III: who can spend an old read's remaining margin?

**Depth 2 · Ideas only; no experiments run, no GPU.** Parent: [Brain mechanisms II](brain-mechanisms-2.md) ([PR #315][parent]). Read the [idea ledger][ledger] first. The [reviewer's PR #315 row][triage] leaves two ideas at score 3: **BM2-23**, where disjoint write masks can spend the same old behavior's tolerance, and **BM2-07**, where a write cannot use the channels it just recruited as permission for another write. This node asks what a continual learner can do when the update changes both the behavior being protected and the route by which the next update would be authorized.

## What the literature already does

I searched Hugging Face Papers for lifelong editing with retention/trust regions, localized masks and edit interference, and causal attribution for editing; then checked the cited titles and abstracts at arXiv. These are comparisons to the mechanisms described in those sources, not claims of exhaustive priority. In particular, the search hit [Causal Edit Serialization][ces] edits tokens in a causal text stream, not the scope of a subsequent parametric write.

| Checked sources | What we should not claim as new |
| --- | --- |
| [AlphaEdit][alpha], [RLSEdit][rls], [Orthogonal Gradient Descent][ogd], [CABA][caba] | Null-space protection, soft cumulative key/value fitting with a fixed anchor, gradient projection, and held-out KL floors with tested interpolation and sequential composition. A ledger that only compares current anchors with a fixed floor is a floor check; CABA is the direct comparator for post-update budget gates. |
| [Bandits with Replenishable Knapsacks][bwk], [Dual Mirror Descent][dmd] | Allocation with replenishment and an online price per shared resource. Use the same old-read observations and charge the same queries; beating a per-block bucket is not enough. |
| [NMKE][nmke], [ACE][ace], [CaKE][cake], [Localization vs. Editing][loc], [Activation Patching: Metrics and Methods][patch] | Edit-time sparse attribution, query–value pathway selection, circuit-guided training samples, and controlled tests of mechanistic attribution. Finding a causal channel does not establish the right to write it, and a patch can change the apparent support. |
| [ENCORE][encore], [Model Editing at Scale][scale], [The Butterfly Effect of Model Editing][butterfly], [EtCon][etcon] | Norm regularization, cumulative degradation, hard edits that cause acute collapse, and constrained editing followed by autoregressive consolidation. None is a reason to rely on a singleton edit score. |
| [MEMIT][memit], [GRACE][grace], [WISE][wise], [EVEDIT][ev], [MQuAKE][mq], [CoRE][core] | Batch writes, external/routed edits, semantic boundaries, edited consequences and robustness in context. Include these when the proposal could be replaced by batching, routing, more representative context or clearer scope. |

## What all first tests must hold fixed

- **One observable unit for each claim.** Fix separately (i) an old read's loss from a frozen reference on an unchanged input and (ii) extra episodes of harm while the model is live. Without the second quantity, exact current-floor validation subsumes a debit on endpoint damage. Never reset the reference because today's model answers differently. Keep admission probes separate from held-out ordinary A and earlier learned B. Do not count a superseded fact as forgetting; measure other valid contexts of the fact. Log absolute floors, worst slice, exposed-prefix and endpoint retention, new gain, and latency at matched update and probe budgets. In all tests, run A and earlier B after the newest accepted update, not only on a shadow branch.
- **Permission is separate from spending.** A live contradiction names external evidence and a read of the same proposition. Record its support before the window's first commit. An edit-induced activation alone cannot widen the mask; use a fresh, independently grounded contradiction on a live read in a new window for actual expansion. Where a card uses a replay or shadow intervention, it can reject, prioritize or narrow a candidate; it cannot mint contradictory evidence. Enforce masks on actual deltas (direct solves or plain SGD on CPU).
- **Beat both parent controls on equal terms.** For damage: per-block BM23, AlphaEdit, static old-read floors, rolling validation and BWK on identical observations, with an antagonistic or nonadditive pair as well as an additive one. For permission: BM18, NMKE, equal-size fixed masks and fresh re-attribution on identical evidence, including a legitimate expansion. Include RLSEdit for soft retention and exact enumeration as a diagnostic ceiling, not a deployable baseline. Mixed cards must beat the strongest authorization control **stacked** with the strongest retention controller. Match persistent bytes, peak workspace, probe/candidate calls and per-request delay; match starting margins for any order-of-forgetting claim. Do not infer sparse damage from disjoint masks: the [ledger][ledger] found diffuse edit damage (PR #24), and its Gramian forecast and first-order forgetting failures rule out using those forecasts as substitutes for observations.

**P** = candidate primitive (a reusable object or operation); **I** = improvement or discriminating audit. These are proposals, not review verdicts.

## BM2-23: what can a shared read spend?

#### BM3-01 · Debit exposure rather than final injury — P
- **Mechanism.** Give a read an allowance in cumulative positive excess loss across served requests, so two live versions with equal edit movement and equal duration can cost different amounts. An unchanged but degraded version keeps drawing on the allowance whenever the old read is served.
- **Novelty vs nearest art.** [BWK][bwk] handles replenishing resources and [CABA][caba] bounds anchor divergence at update time. BM2-13 already charges live writes even when they cancel. The narrower candidate is a debit stream driven by ordinary reads *between* writes, weighting their excess loss rather than write count or elapsed time.
- **Cheapest first test.** Enumerate two disjoint writes that cancel, with 0, 1 or 8 ordinary queries between them; vary the severity of each missed answer at the same error count. Match the endpoint, absolute floor and deadlines. Drop if rolling severity-weighted counts or microbatching tie on delivered corrections and observed harm.
- **Old-task retention.** Test independently drawn A and earlier B at each exposed prefix, including when the cancelling write never arrives.

#### BM3-02 · Spend only on the error an edit introduced — P
- **Mechanism.** Keep a co-served frozen comparator on a bounded sample of requests and debit current-only errors, not shared errors or net loss. Improvements on comparator failures cannot pay for new failures elsewhere.
- **Novelty vs nearest art.** [RLSEdit][rls] regularizes toward an anchor mapping and [CoRE][core] reduces context-sensitive drift. This is a non-nettable resource in the joint distribution of old and current outcomes, rather than a norm or score difference. Compare an exact per-item floor when it fits.
- **Cheapest first test.** In a finite table simulate two streams with identical aggregate error and different disagreement patterns; run margin-matched alternatives and charge all comparator calls. Stop if a paired rolling non-regression check buys the same throughput.
- **Old-task retention.** Score full A and earlier B, separating fixed reference errors, newly introduced errors, and recovered errors on unseen inputs.

#### BM3-03 · Give a served trajectory one damage account — P
- **Mechanism.** Reserve tolerance on an old trajectory's terminal outcome, not separately on each intermediate read. Debit once for a failed trajectory even if two changed reads lie on its path; charge an alternate path if that is where ordinary execution goes.
- **Novelty vs nearest art.** [MQuAKE][mq] identifies entailed changed answers; [EtCon][etcon] consolidates with trajectory rewards. The proposed operation allocates one outcome allowance across otherwise independent writers. Exact end-to-end validation plus BWK is the close control.
- **Cheapest first test.** Enumerate a two-step decision tree with redundant and complementary read errors. Compare per-read charges with a sampled trajectory debit at equal simulator calls; drop if exact episodic floors or the stacked control tie.
- **Old-task retention.** Test normal closed-loop old episodes including alternate paths, plus unrelated tasks and formerly learned branches.

#### BM3-04 · Price a read contingent on its other consumers — P
- **Mechanism.** Replace a pooled read balance with a vector indexed by semantic consumers of the same internal output. Debit the same change differently where the consumer's decision actually crosses a boundary; do not let unused tolerance in a frequent consumer buy errors in a rare one.
- **Novelty vs nearest art.** [EVEDIT][ev] separates changed facts from deduction anchors, while [CoRE][core] treats context-dependent edit failures. A consumer-indexed budget is a candidate reusable debit unit, but separate static slice floors plus BWK may already cover it.
- **Cheapest first test.** Use two frozen heads with different thresholds on the same read, balanced for starting margins by adding independent residuals. Cross shared versus disjoint masks with head traffic imbalance. Drop if the best slice-floor controller ties at equal probes.
- **Old-task retention.** Run both ordinary heads on unseen examples, reporting the rare head separately, and include prior B.

#### BM3-05 · Reserve against every still-plausible old read — P
- **Mechanism.** When old probe data leave multiple plausible assignments of a shared effect to slices, hold one reservation against the feasible set, release it only on a distinguishing labeled old request, and forbid a writer from selecting the favorable assignment.
- **Novelty vs nearest art.** [Dual Mirror Descent][dmd] prices separate resources; [AlphaEdit][alpha] protects specified keys. The object here is a contingent claim over alternative *identities* of the charged read, not a new optimizer. Compare robust constraints on the same alternatives and worst-case independent reservations.
- **Cheapest first test.** Enumerate two indistinguishable alias assignments and a low-cost query that resolves one. Include an unresolvable pair. Stop if robust static floors plus the same query schedule match both admissions and loss.
- **Old-task retention.** Test every alias class on held-out old queries, including the one the controller thought less likely, and replay earlier B at the end.

#### BM3-06 · Cancel an unpublished reservation, not an exposed mistake — P
- **Mechanism.** Split provisional capacity from accrued harm. Re-debit a replacement candidate against the live model rather than its discarded predecessor. Refund only its unused reservation, never exposure already incurred by a deployed portion.
- **Novelty vs nearest art.** [MEMIT][memit] batches edits, [BWK][bwk] can credit replenishment, and BM2-13 already distinguishes served from unserved writes. The proposed object is a transferable **reservation on the unserved remainder** of a partially published change, not merely a rule against refunding past harm. If atomic batching at matched latency suffices, it is bookkeeping.
- **Cheapest first test.** Enumerate a two-edit build with a withdrawal immediately before or after one partial publication. Compare atomic and rolling endpoint controllers with the same deadlines. Require useful early updates, not just fewer overruns by waiting.
- **Old-task retention.** Measure old A and learned B during partial publication, on cancellation and after the replacement; score the requests served before repair as well.

#### BM3-07 · Settle damage in the order reads can observe it — P
- **Mechanism.** Permit different cohorts to observe candidate versions in different orders, but account for each cohort's actual observed prefixes. Merely computing two orders on a shadow model costs no damage; a real served prefix does.
- **Novelty vs nearest art.** [WISE][wise] routes and shards edits, and [EtCon][etcon] checks generation after editing. The candidate operation is a per-cohort exposure settlement for the *same* eventual parametric state, not an order-dependent weight predictor.
- **Cheapest first test.** Enumerate two additive updates with unchanged final weights, two traffic schedules and one short deadline. Compare with norm-matched joint publication and a cohort floor plus BWK; discard if cohort routing alone ties with the same memory.
- **Old-task retention.** Follow each cohort's ordinary old reads throughout; also test cross-cohort old traffic and past B after versions converge.

#### BM3-08 · Buy a repair only when it removes live liability — I
- **Mechanism.** Rank feasible restorative deltas by reduction in projected exposure for the currently strained old reads, while charging any harmed read like an ordinary edit. Do not replenish on a promised repair.
- **Novelty vs nearest art.** [OGD][ogd] and [RLSEdit][rls] already protect old behavior in the optimizer; using an observed old-read price to select a restorative step is an improvement hypothesis, not a forgetting predictor.
- **Cheapest first test.** Enumerate exact key–value solves for two repair targets with equal training loss and different live frequency; compare direct old replay, equal-byte anchor regularization and a BWK price. Discard unless selective repair advances the A/B Pareto front.
- **Old-task retention.** Score both repaired and nonrepaired old reads on held-out A and verify that repairs do not unlearn B.

#### BM3-09 · Charge a protected alternative before it is selected — P
- **Mechanism.** For a known ensemble of ordinary decoders on one read, reserve sufficient headroom for any permitted decoder, even if the current top answer stays fixed. Release only if the relevant decoder is retired externally.
- **Novelty vs nearest art.** [AlphaEdit][alpha] pins preserved keys rather than pricing allowed downstream decoders; [CoRE][core] tests context-induced failures. A decoder-indexed claim can transfer with a read, but simple logit floors may subsume it.
- **Cheapest first test.** Use two known linear readouts, switch them on an externally set schedule, and compare logit/L2 protection, per-decoder floors and BWK with equal observations. Include a decoder that never switches.
- **Old-task retention.** Test both decoders on their ordinary old tasks even before switching and on unseen inputs afterward; record earlier B through the same interfaces.

#### BM3-10 · Make the floor equivalence explicit — I
- **Mechanism.** Run an exact endpoint-floor checker on every candidate with a common old reference; track the exposure allowance as a separate optional state variable. Test for a capacity region where that extra state changes admissible decisions.
- **Novelty vs nearest art.** [AlphaEdit][alpha] protects old anchors, [RLSEdit][rls] softens preservation and [BWK][bwk] adds resource history. This is a test of reducibility, not a new controller: if damage is endpoint-only and exact floors are cheap, reject the ledger claim.
- **Cheapest first test.** Enumerate all short streams of two disjoint masks and one shared read, with additive, cancelling and synergistic damage. Include equal-endpoint histories with unequal served errors. Drop the new state if exact validation with a shared prefix bound always ties.
- **Old-task retention.** Report old performance independently at every exposed prefix and the endpoint, then revisit A and earlier B after sustained drift.

## BM2-07: distinguish a new observation from a write's echo

#### BM3-11 · Read the new contradiction on both sides of the first write — P
- **Mechanism.** For an externally verified fresh correction, shadow-read the same witnessed input against the pre-window model. Classify newly active channels as corroborated or write-dependent. A write-dependent channel needs independent support or goes to the necessity test in BM3-12 rather than being opened by the shadow.
- **Novelty vs nearest art.** [NMKE][nmke] chooses a sparse mask from current attribution; [ACE][ace] traces query–value pathways. The candidate operation is a two-version eligibility check on one event, not a better single-version causal mask.
- **Cheapest first test.** Use a two-gate MLP, one threshold switched by the first edit and one switched only by an exogenous input change. Compare BM18, frozen masks and fresh NMKE at equal forward calls. Fail if the paired read only reproduces staleness or threshold noise.
- **Old-task retention.** Test old consumers of both gates and previously learned corrections on normal inputs, including one where expanding scope is necessary.

#### BM3-12 · Require a witness of necessity, not just activity — P
- **Mechanism.** Given a fresh grounded contradiction, compare the best old-scope candidate with one using the requested channel. Escalate only if the old scope cannot attain the declared new-fact and old-read constraints within the same update budget. For tiny models use exhaustive solves; solver failure is not a certificate.
- **Novelty vs nearest art.** [Localization vs. Editing][loc] shows causal trace is not an editability test; [OGD][ogd] projects away restricted changes. The candidate primitive is permission to expand for a specific counterexample to *sufficient scope*, not the ledger's killed sparse-rank certificate.
- **Cheapest first test.** Enumerate equal-sized finite writes in a sparse MLP with paired cases: recruited channel is a shortcut versus sole feasible solution. Compare fresh attribution, fixed masks and direct constrained editing with access to the same evidence. Discard if the witness adds no selectivity.
- **Old-task retention.** Hold out independent consumers of the newly opened channel, ordinary unrelated A, and all earlier accepted B.

#### BM3-13 · Hand off a read role without widening the write — P
- **Mechanism.** When permitted support migrates to another channel, test whether substituting one channel for the other preserves the read's role across anchored contexts. If fresh independent contradiction authorizes it, replace the slot instead of granting both channels write access.
- **Novelty vs nearest art.** [ACE][ace] selects Q–V pathways and [NMKE][nmke] refreshes a mask. A witnessed exchange of an old permission for a new one is distinct from union or unrestricted refresh only if it preserves role at fixed cardinality; compare top-k re-attribution.
- **Cheapest first test.** Use a sparse model with redundant routes in one branch and role-sharing in another. Choose ordinary contexts in which interchange has different consequences. Match patch calls and charge rejected swaps.
- **Old-task retention.** Test both routes' old consumers, including contexts not used in the equivalence test, and earlier B after the handoff.

#### BM3-14 · Trace what the latest edit could not have caused — P
- **Mechanism.** For a fresh contradiction whose new scope may be an echo, shadow-intervene on the changed upstream edge alone. Treat a stable downstream witness as potential independent support; if the answer or support changes under plausible patch choices, abstain from expansion.
- **Novelty vs nearest art.** [Activation Patching: Metrics and Methods][patch] already studies such interventions and their sensitivity. The candidate interface asks which evidence remains admissible under removal of a specific writer's influence, not where the largest causal effect lies.
- **Cheapest first test.** Compare two exact sparse graphs with the same post-edit activation but different mediation; include a case where edge intervention produces an invalid hybrid and require abstention. Use identical call budgets for fresh attribution and dual-version reads.
- **Old-task retention.** Run natural, unpatched old queries of both mediated and unmediated relations, plus earlier learned updates; patched read success does not count.

#### BM3-15 · Give a correction one scope across repeated paraphrases — P
- **Mechanism.** Bind authorization to the verified contradiction's semantic scope, not its presentation. Repeated paraphrases can narrow the admitted write to corroborated support but cannot pool new channels unless a fresh independent contradiction grounds an expansion.
- **Novelty vs nearest art.** [CoRE][core] explicitly strengthens edit robustness in preceding contexts, and [EVEDIT][ev] scopes edits by events. The proposed operation is budgeted reuse of a verified claim without multiplicity of write permissions. Compare semantic deduplication plus fresh NMKE.
- **Cheapest first test.** Interleave duplicated paraphrases that recruit different near-threshold channels with equally similar requests exposing genuinely different old errors. CPU exact labels; equal number of read calls. Drop if event deduplication alone suffices.
- **Old-task retention.** Test unchanged alternate meanings of the same names and ordinary paraphrases from old tasks; require learning the real second correction without disturbing earlier B.

#### BM3-16 · Record an eligibility change even when the answer stays right — I
- **Mechanism.** Shadow-track channel eligibility on unchanged old reads that remain correct. Surface silent promotions as a diagnostic, then check whether a later contradiction would produce harmful expansion without independent evidence.
- **Novelty vs nearest art.** [Model Editing at Scale][scale] tracks degradation and [NMKE][nmke] tracks edit attribution; testing churn before accuracy drops is an audit. A norm or activation-drift alarm is a required control, not a straw man.
- **Cheapest first test.** In a sparse model, construct equal-answer and equal-norm edits with one near-threshold route moved. Compare both alarms for predicting differences in *actual allowed writes*, not for rediscovering the threshold.
- **Old-task retention.** Re-run those old reads, all neighboring old route consumers and prior B after a later legitimate update; classify churn without damage separately.

#### BM3-17 · Spend a probe on the dispute that separates origin stories — P
- **Mechanism.** If new support might come from an exogenous change or prior edit, select an ordinary query on which the two causal accounts disagree before requesting a label. Use the result only if it independently contradicts a live read; otherwise refuse expansion.
- **Novelty vs nearest art.** [CaKE][cake] curates circuit-guided samples and [BALD][bald] already picks queries using information gain. The candidate acquisition target is uncertainty over *which future writes a label can independently authorize*, not predictive uncertainty or generic origin classification; include BALD over the same causal hypotheses.
- **Cheapest first test.** Enumerate two hypotheses that agree on all active inputs but disagree on one cheap reachable query; include a graph without any reachable separating query. Compare random and maximum-disagreement attribution probes on the same external label allowance.
- **Old-task retention.** Measure ordinary A on nonqueried examples and previous B after resolution, including false positives on a nearby proposition.

#### BM3-18 · Judge first expansion after the window boundary against its origin — P
- **Mechanism.** Carry a bounded record of channels recruited by the previous window into the next one. Do not launder recruitment merely by waiting; expansion still needs the first independently witnessed new contradiction for that read. Drop the record when its live route ceases to differ or it is legitimately authorized.
- **Novelty vs nearest art.** [NMKE][nmke] updates masks as edits arrive and [GRACE][grace] stores update history externally. The candidate state is a cross-window restriction *on permission* without pinning the activation or storing the old model indefinitely.
- **Cheapest first test.** Run a three-window sparse stream in which equal delays precede an echo, a legitimate second correction and reversal of the first route change. Compare longer frozen windows, fixed masks and equally evidenced fresh re-attribution at equal bytes.
- **Old-task retention.** Test old consumers in each window; continue through the legitimate reauthorization and measure A and earlier B, not just how many writes were blocked.

## Joint descendants: make permission and spending constrain one another

#### BM3-19 · Do not let a route change erase who pays — P
- **Mechanism.** Index liability by the public read and its old valid outcome, never by the channel realizing it. If it moves, carry the debits to the same read even while the new channel is ineligible to write. If the public read splits semantically, require explicit external disambiguation rather than free balances.
- **Novelty vs nearest art.** [AlphaEdit][alpha] protects key vectors and [BWK][bwk] assumes defined resource identities. The candidate is a transfer of outstanding behavioral liability across changes in internal support. Compare a static input-level floor and BWK on fixed public identities; if they tie, there is no new operation.
- **Cheapest first test.** Use a two-route switch keyed by the first edit, then offer competing disjoint-mask corrections. Include a switch with no behavioral effect and a genuine semantic split. Match probes, new gain and latency.
- **Old-task retention.** Test the same old meanings through both natural routes, plus unaffected A and previously learned B after the switch.

#### BM3-20 · Do not let a write switch off its own meter — P
- **Mechanism.** Commit a small fixed audit schedule on public old inputs before edits; mark a disappeared read or unobservable consequence unresolved rather than safe. Keep its reservation until a later ordinary query or a matched observation settles it.
- **Novelty vs nearest art.** [Selective Labels][selective] already studies actions that conceal outcomes; the [PR #313 review][triage] explicitly calls out writes that disarm their own tests. The narrower proposal is to keep a particular old-read liability encumbered when a scope-changing write hides the observation that would release it. Compare selective-label correction and randomized unconditional audits at fixed exposure.
- **Cheapest first test.** In a branching CPU agent compare a correction that eliminates old failures with one that hides the affected branch by skipping the read. Include naturally absent branches. Fail if fixed external audit plus a static floor and BM2-07 admit the same useful changes.
- **Old-task retention.** Report ordinarily reachable old outcomes, task completion and rate of missing old reads separately; run held-out A and earlier B without forcing the audited route.

#### BM3-21 · Make revoked authority survive a recharge — P
- **Mechanism.** When a fresh read invalidates a scope's provenance, its remaining reservation is released to other eligible requests, but refill cannot reactivate that scope. Conversely fresh evidence cannot recycle exposure already spent.
- **Novelty vs nearest art.** [BWK][bwk] models replenishment and [NMKE][nmke] refreshes eligibility. The proposed operation is selective invalidation of a linked claim on shared old behavior. Compare independent authorization and resource state machines; if their composition ties, treat this as bookkeeping.
- **Cheapest first test.** Enumerate revocation, refill and independent evidence in all arrival orders for two disjoint corrections sharing an old read. Compare the stacked controller at equal bytes; require lower delay on a valid queued write at matched retention.
- **Old-task retention.** Measure ordinary A and earlier B after revocation, refill and the legitimate queued commit, including one nonrecovering old behavior.

#### BM3-22 · Allocate the right to observe separately from the right to modify — P
- **Mechanism.** A contradictory read can nominate a channel for a fixed-cost observational probe without authorizing a delta. Give the probe priority when its result would distinguish competing liabilities for the last headroom of a shared old read.
- **Novelty vs nearest art.** [ACE][ace] attributes editable pathways and [BWK][bwk] prices scarce actions. The candidate is a joint admission query whose answers change both feasible scope and which older behavior would pay; an allocation of audit calls alone is old territory.
- **Cheapest first test.** With one label query, compare an independent attribution-plus-budget stack to an exact choice that distinguishes two candidate writes with identical immediate gain. Include a case where evidence changes only one of the decisions.
- **Old-task retention.** Measure ordinary old queries on both potentially charged reads and previous B, before and after the selected full update; designation as “probe-only” must not count as learning.

#### BM3-23 · Commit a repair and a correction only if neither bootstraps the other — P
- **Mechanism.** Search joint candidates for a new correction plus an old-read repair. Each delta must have independent authorization on the common prepublication model, even if they can afford only atomic publication because separate exposure is too costly.
- **Novelty vs nearest art.** [MEMIT][memit] already batches edits, [RLSEdit][rls] trades fitting against preserved anchors. The proposed primitive is a jointly affordable candidate certified against *preexisting* permissions; compare BM2-26 and batched constrained editing with refresh before the batch.
- **Cheapest first test.** Enumerate a legitimate cancelling pair and another whose repair is available only on a channel the new correction activates. Compare atomic and sequential baselines with exactly the same candidate set and deadline; drop if preflight checks alone reproduce the tradeoff.
- **Old-task retention.** Test old A at every served version and earlier B after publication; on rejection, require the ordinary pre-edit old behavior to remain available.

#### BM3-24 · Give irreversible outputs stricter settlement than recoverable state — P
- **Mechanism.** Use separate liability for persistent public errors and reversible internal state. Permit a tentative action behind a publish gate only when it cannot affect the live authorization evidence or leak an old answer before validation.
- **Novelty vs nearest art.** [WISE][wise] isolates side memory and [EtCon][etcon] aligns downstream generation; shadow editing alone is not novel. The candidate operation segregates error liability and evidence provenance across a declared publication boundary. Compare standard shadow validation plus the stacked controller.
- **Cheapest first test.** Build a finite agent with a reversible local step and an externally observed decision, both of which can activate the same gate. Include a hidden-state path that affects the next live read and must not pass. Require more useful corrections at the same old-output exposure.
- **Old-task retention.** Score old outputs in normal operation and probe whether deferred state changes corrupt later old reads or previously learned B even if nothing was published immediately.

#### BM3-25 · Reject an edit that only improves its approval score — I
- **Mechanism.** Replay each flow of edits under two dashboards: one measuring approved writes and internal probe scores, one measuring executed old tasks and independently grounded corrections. Perturb only whether a gate or admission probe can be affected by a preceding write.
- **Novelty vs nearest art.** [The Butterfly Effect of Model Editing][butterfly] studies damaging edits, and [EtCon][etcon] finds controlled versus autoregressive evaluation gaps. This is a stress test for the specific feedback loop between scope and debit, not a new metric for all editing.
- **Cheapest first test.** Cross pre-window/fresh masks with fixed/route-selected debit probes on the same short CPU streams. Include genuine old-task improvement that also raises scores. If the strongest independent stack eliminates the gap, stop.
- **Old-task retention.** Use separately held-out old tasks under regular routing, report past B and window-by-window worst A, and match new learning and served-request counts before attributing a gap.

#### BM3-26 · Identify when one extra bit would make a safe edit possible — I
- **Mechanism.** Pair worlds with identical currently observable support, balances and contradiction evidence but different feasible next edits. Find the cheapest external observation that separates the worlds; abstain when none exists instead of fitting a confidence threshold.
- **Novelty vs nearest art.** [BWK][bwk] already addresses unknown online inputs and [Localization vs. Editing][loc] warns that read localization is not an editability signal. This is an information-limit audit of the conjunction of old-read spending and independent authorization, not an online allocation theorem.
- **Cheapest first test.** Exhaust a small two-gate, two-read model and compare exact causal optimizers with and without a single independent label, holding movement and deadlines fixed. Include a redundant bit and report what fraction of conflicts the real bit can settle.
- **Old-task retention.** On both worlds measure A and previously acquired B on ordinary interleavings, including the cost of abstention when an edit could in fact have landed safely.

## Ranked deeper questions

1. **When is a shared old-read budget strictly more useful than exact floor checks?** Start with BM3-10 and BM3-01/03. Hold willingness to learn and allowed publication delay fixed, then compare equal-endpoint histories that serve different old errors. If endpoint plus simple rolling exposure checks cover all gains under identical observations, retire the new ledger. If not, ask which read definition transfers to unseen A without sacrificing earlier B.
2. **How often does a valid new correction actually need an edit-recruited channel?** Use the narrow oracle in BM3-12, then test the two-version and mediation witnesses in BM3-11/14 against equal-evidence re-attribution. A lower rate of unauthorized openings is not progress if legitimate second revisions stall; compare success and delay at equal held-out neighbor retention.
3. **Can a useful controller stop a write from redefining both its permission and its bill?** Run BM3-19/20/25 as a crossed comparison of fresh versus provenance-bound masks and route-selected versus public-read debit. Demand an advantage over fixed public probes plus independently verified permissions at equal cost. A write that actually removes failures must pass the same test as one that just hides them.
4. **When should the learner buy information instead of preserving more headroom?** Use BM3-05/22/26 to find observationally indistinguishable alternatives and measure what a label or normal read can disambiguate. Compare exact causal policies at the same budget; if the extra observation rarely changes the admissible write set, prefer the cheaper stacked controller.

[parent]: https://github.com/manojbajaj95/cl/pull/315
[ledger]: https://github.com/manojbajaj95/cl/blob/5e9fd48a1e67e598092b9ab9f50e730ff4214283/reviews/idea-ledger.md
[triage]: https://github.com/manojbajaj95/cl/blob/5e9fd48a1e67e598092b9ab9f50e730ff4214283/reviews/flood-triage.md#L430-L433
[alpha]: https://arxiv.org/abs/2410.02355
[caba]: https://arxiv.org/abs/2610.40740
[rls]: https://arxiv.org/abs/2601.15686
[ogd]: https://arxiv.org/abs/1910.07104
[bwk]: https://arxiv.org/abs/2306.08470
[dmd]: https://arxiv.org/abs/2011.10124
[nmke]: https://arxiv.org/abs/2510.22139
[ace]: https://arxiv.org/abs/2510.07896
[cake]: https://arxiv.org/abs/2503.16356
[loc]: https://arxiv.org/abs/2301.04213
[patch]: https://arxiv.org/abs/2309.16042
[encore]: https://arxiv.org/abs/2502.01636
[scale]: https://arxiv.org/abs/2401.07453
[butterfly]: https://arxiv.org/abs/2402.09656
[etcon]: https://arxiv.org/abs/2512.04753
[memit]: https://arxiv.org/abs/2210.07229
[grace]: https://arxiv.org/abs/2211.11031
[wise]: https://arxiv.org/abs/2405.14768
[ev]: https://arxiv.org/abs/2402.11324
[mq]: https://arxiv.org/abs/2305.14795
[core]: https://arxiv.org/abs/2505.23026
[ces]: https://arxiv.org/abs/2610.22820
[bald]: https://arxiv.org/abs/1112.5745
[selective]: https://arxiv.org/abs/1807.00905
