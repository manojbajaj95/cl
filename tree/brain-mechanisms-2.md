# Brain mechanisms II: when a recalled fact becomes writable, and what a write costs

**Depth 1 · Ideas only; no experiments run, no GPU.** Parent: [Brain & Biological Mechanisms](root-brain-mechanisms.md) ([PR #308][parent]). Read the [idea ledger][ledger] first. The [reviewer's PR #308 row][triage] gives score 3 to **BM18** (open only the retrieved rows implicated by a contradiction) and **BM23** (a regenerating, per-block budget for actual writes), and promotes neither to the top 10. This child asks whether either can become a reusable operation for a live continual learner, rather than a relabeled mask or rate limiter.

## What the literature already does

I searched Hugging Face Papers for lifelong sequential editing, neuron-level edit masks, contradiction-triggered editing, synaptic metaplasticity, and replenishable budgets; read the returned abstracts and checked the biology through Crossref and Europe PMC and the rate limiter against RFC 3290. The contrasts below describe what those sources establish, not a proof of novelty or a full implementation audit.

| Checked source | What this node does **not** claim as new |
| --- | --- |
| [Nader, Schafe & Le Doux][nader]; [Sevenster, Beckers & Kindt][sevenster] | Retrieval-dependent reconsolidation and prediction error as a condition for destabilization in the studied fear memories. These are biological precedents, not evidence that recall localizes an editable model weight. |
| [ROME][rome], [MEMIT][memit], [AlphaEdit][alpha] | Localized feed-forward edits, multi-association edits across layers, and projection to preserve old keys. None of these outcomes by itself distinguishes a live, short-lived write permission from edit-time parameter selection. |
| [NMKE][nmke]; [Does Localization Inform Editing?][localization] | Sparse neuron-level attribution and dynamic edit masks already exist. Causal tracing did not identify the best MLP edit layer in the studied setting; a read trace is not evidence of edit feasibility. NMKE, not just whole-layer editing, is a required control. |
| [GRACE][grace], [MELO][melo], [WISE][wise] | Retrieved activation codebooks, neuron-indexed adapter selection, and routed side weights that leave the main memory untouched. Better locality from a separate read path isn't evidence for in-place revision. |
| [EVEDIT][evedit], [MQuAKE][mquake] | Event-scoped edits with unchanged deduction anchors, and evaluation of consequences over multi-hop chains. Test which consequences should change as well as which neighbours must not. |
| [EWC][ewc], [Synaptic Intelligence][si], [OGD][ogd], [ENCORE][encore] | Importance penalties, path-dependent importance, protection by projection, and control of edit-layer matrix norm growth. Compare actual movement and old outputs, not just unclipped gradient norm. |
| [RFC 3290, Appendix A][bucket]; [Bandits with Replenishable Knapsacks][bwk] | BM23's basic refill-and-spend recurrence is a token bucket. Optimizing allocation with replenishment already exists. A new budgeting claim needs a useful *learning-specific* unit or operation, not a scalar bucket with a different name. |
| [Abraham & Bear][meta]; [Loss of Plasticity in Deep Continual Learning][plasticity] | Prior activity can alter subsequent plasticity; selectively reinitializing units already helps with loss of plasticity. A reservoir must improve burst retention without blocking sustained useful learning. |

## What all first tests must hold fixed

- **Write permission is not an editable fact address.** In an MLP, a “row” means a channel's input key and paired output value (a column in some layouts). Default to value-only writes and declare separately if a key can change. Record active channels on a live pre-correction read. A trusted contradiction refers to the version actually read and to the same entity, relation, and scope; plain surprise or an alternative valid answer is not enough. Scope mask, expiry and debit are enforced on **committed deltas**, including any optimizer side effects; use plain SGD or direct solves for the first CPU tests. Unopened channels stay unchanged; protected outputs can still drift through shared channels. Compare with ROME/MEMIT/AlphaEdit, NMKE, GRACE-style adaptors, all-rows and retrieval-only gates; for an attribution claim also compare equal-cardinality random or fixed masks. Include a fact that cannot be revised in the retrieved support.
- **Pay for movement, not elapsed training steps.** Default BM23 baseline: before each arrival at time `t`, block `b` receives `min(cap_b, balance_b + rate_b × elapsed)`; a committed delta costs `||ΔW_b||_F`. A write exceeding the balance is refused, scaled, or deferred by the declared policy. Every live intermediate move counts; a purely hypothetical candidate does not. The cost is total path length, not displacement, and there is no reset at a task boundary. Compare with tuned clipping (including a norm-matched arm), per-block LR decay, EWC/SI, ENCORE-style norm control, a rolling cap and a literal token bucket. Include long, steady drift and a short, entirely useful burst. Compare jointly on new-task gain, delay, refused work and retention; preservation by not learning is a loss.
- **Use matched streams and independent old-task measurements.** Start with a CPU key–value model, sparse two-layer MLP or exact tiny enumeration; an oracle is a diagnostic upper bound, never the deployed router. Train on a fixed old distribution A, learn task B, and measure normal A and previously learned B after new writes, at exposed prefixes and after expiry/refill. Use held-out paraphrases, same-subject alternate relations, same-value other subjects, and unrelated old tasks as applicable. Score intended supersessions as new-task efficacy, not as old-task retention failures; keep unaffected historical variants in A when still valid. Freeze retention floors and slices first, use separate admission probes, and match initial per-item margins for any forgetting-order claim. Charge persistent bytes, peak workspace, candidate evaluations, trace/probe calls, update steps and latency to every arm. On mixed cards compare with the strongest independent edit gate **plus** the strongest independent budget policy at the same cost; record the individual arms too. If the stacked control ties, do not claim a new primitive.

**P** = candidate primitive (the new object or operation is named); **I** = improvement, baseline or discriminating audit. These are proposals, not review verdicts.

## BM18: what a contradiction can make writable

#### BM2-01 · Compare-and-open on the version actually recalled — P
- **Mechanism.** Issue a short-lived write scope carrying the question scope, recalled answer version and live read mask. At commit, reject it if a newer answer has landed or the read no longer has that support. A duplicate confirmation never opens the scope.
- **Novelty vs nearest art.** [NMKE][nmke] already selects neurons per edit; a version check is ordinary compare-and-swap. The candidate operation binds the check to an observed *parametric recall*, not merely an edit-cache key. Compare with NMKE plus versioning of external edit records and with [GRACE][grace] plus the same stale-record filter.
- **Cheapest first test.** Let two verified corrections arrive out of order for one key, then change its support via an unrelated update while its version is unchanged. Match masks and query calls. Refuse the claim if external versioning plus a fresh mask ties.
- **Old-task retention.** After each attempted commit, score unaffected relations of that subject, other subjects sharing its answer, and a previously corrected fact.

#### BM2-02 · Ask for the cheapest missing read, not the biggest mask — P
- **Mechanism.** When the current live mask cannot realize a correction within collateral limits, return a missing-support witness from a failed local solve. A bounded follow-up query must actually retrieve the implicated support before it can enlarge the write scope.
- **Novelty vs nearest art.** [MEMIT][memit] distributes edits across layers; [NMKE][nmke] attributes relevant neurons. Neither comparison is defeated by a larger mask alone: test whether a failed *constrained* solve can select the next observation better than unrestricted attribution, random follow-ups or widest-mask selection with matched calls.
- **Cheapest first test.** Use a two-layer fact whose first read omits a needed channel; offer three real paraphrases, only one exposing it. Also offer a fact for which none suffices. Count useful revisions per call and unrevisable cases correctly refused.
- **Old-task retention.** Re-evaluate unaffected paraphrases and facts sharing the newly discovered channel after both the accepted and refused paths.

#### BM2-03 · Protect the other meaning of a shared channel — P
- **Mechanism.** Pair a positive read with an independently retrieved counter-read that activates the same channel but remains true. Open the channel only with a constraint on the counter-read's output, not a blanket prohibition on touching shared channels.
- **Novelty vs nearest art.** [AlphaEdit][alpha] and [OGD][ogd] protect outputs by projection. The candidate is an on-demand **paired scope witness**; compare with the same projector using fixed or matched retrieved anchors. If retrieving the paired witness adds nothing, this is anchor selection.
- **Cheapest first test.** Fit a three-channel linear value head whose unconstrained minimum-norm update damages a neighbour, but which still has a feasible edit when that neighbour's read is protected. Swap in an equally similar but uninformative counter-read; include an infeasible tied-feature pair.
- **Old-task retention.** Check unseen examples of the protected meaning and unrelated A; repeat after learning a second B correction using that channel.

#### BM2-04 · Tie two views to one opening or leave both closed — P
- **Mechanism.** A contradiction tied to two legitimate paraphrase views opens a compound scope only if one masked update can satisfy both and keep a negative contrast unchanged. If one view is missing, do not silently treat success on the other as completion.
- **Novelty vs nearest art.** [ROME][rome] evaluates paraphrase generalization and [NMKE][nmke] distinguishes general and specific neurons. The proposed operation enforces linked views at admission and expiry; compare against just batching paraphrases with NMKE and using union or intersection masks.
- **Cheapest first test.** Cross independently varied paraphrase and entity ambiguity in a sparse MLP; include a pair made incompatible by the negative contrast. Use disjoint paraphrases to measure whether the joint scope gives anything beyond training coverage.
- **Old-task retention.** Score both held-out view families on unchanged facts as well as homonyms, before and after the joint window.

#### BM2-05 · Separate a change in reality from a change in the question — I
- **Mechanism.** A scope discriminator distinguishes a genuine replacement from a previously valid answer being read under a new time or condition. With no discriminating evidence, use a provisional contextual answer without making the base channels writable.
- **Novelty vs nearest art.** [EVEDIT][evedit] already uses event descriptions and deduction boundaries, and [WISE][wise] routes between main and side memory. This is a test of gating in-place writes with observable scope rather than a new temporal editor.
- **Cheapest first test.** Alternate “current chair” and “chair in year X” queries with identical unqualified embeddings in a fact table. Compare event-conditioned editing, a timestamped cache, and a naive contradiction gate; include ambiguities no observation can disambiguate.
- **Old-task retention.** Retest valid historical answers, unaffected temporal queries and old tasks that do not use dates after each current-answer correction.

#### BM2-06 · Read through one path, write through another only with a witness — P
- **Mechanism.** Keep a retrieved shared value locked when it cannot change safely. Open a second, naturally retrieved downstream channel only after a local intervention shows that it can override the obsolete answer without altering the shared channel's other consumers.
- **Novelty vs nearest art.** [Localization vs. Editing][localization] finds that the read and best edit layer can differ; [MELO][melo] offers a routed adapter instead. The candidate is a paired read-to-write authorization, not the observation that another layer edits better. Compare best fixed layer and equal-size adapters.
- **Cheapest first test.** Use a sparse two-layer network where a common first-layer feature serves two facts but only one recalls a second-layer residual. Remove the residual in a negative arm. Require improvement on unseen contexts, not just a stronger edited logit.
- **Old-task retention.** Check the shared feature's other consumers and normal downstream tasks with and without naturally activating the edit site.

#### BM2-07 · Prevent a write from manufacturing its next permission — P
- **Mechanism.** Freeze the provenance of eligible channels before the first commit in a window. If changing a key makes a new channel fire, that firing alone cannot broaden the scope; require an independent, fresh contradiction on a live read outside that window.
- **Novelty vs nearest art.** Dynamic masking in [NMKE][nmke] is a close control; this is an anti-self-expansion rule, not a new attribution score. Compare with fixed masks and fresh re-attribution under identical evidence, not a mask that gets more queries.
- **Cheapest first test.** Set two sparse gates close to threshold so one truthful edit recruits the other's channel. Mix duplicate corrections and independent corrections; compare scope creep and the time to land legitimate second edits.
- **Old-task retention.** Measure all ordinary consumers of the recruited channel after every accepted step; check retained efficacy of earlier B edits when the later genuine correction finally arrives.

#### BM2-08 · Register which consequences may change — P
- **Mechanism.** A scope carries small, executable “must change” and “must stay” consequence lists from distinct reads. Only the necessary consequences are permitted to move; if the constrained local write cannot satisfy both, leave the base intact.
- **Novelty vs nearest art.** [MQuAKE][mquake] already measures ripple effects; [EVEDIT][evedit] already marks stable deduction anchors. The candidate is a transferable *write-admission* object bound to observed rows. Compare identical consequence constraints applied during full-layer editing, and [MeLLo][mquake]-style external correction.
- **Cheapest first test.** Update one edge in a small relational network with two affected two-hop queries and a shared unaffected edge. Hold out alternate paths and remove a required channel in one case; kill the local claim if equal-observation constrained global edits dominate.
- **Old-task retention.** Run unchanged chains of matching hop count and independent one-hop queries through ordinary inference, not just the consequence probes.

#### BM2-09 · Reopen a disputed correction without restoring the old model — P
- **Mechanism.** Retain a bounded link from a consolidated claim to its evidence version. Authenticated retraction requires a new read and contradiction before opening a fresh scope; it never authorizes replaying the inverse of an old delta on moved weights.
- **Novelty vs nearest art.** [GRACE][grace] gives a natural remove/replace-cache control; [WISE][wise] separates and merges edited weights. The in-place claim is retraction with unrelated intervening learning intact, not exact restoration. Compare with re-editing directly from latest evidence and with cache tombstones.
- **Cheapest first test.** Consolidate one claim, land two overlapping but valid edits, then retract the first claim. Give the learner explicit evidence for the restored answer in one branch, and no replacement in the other; the latter should abstain rather than infer the old value.
- **Old-task retention.** Check the two intervening edits and unedited shared-channel facts immediately after the retraction and after the next regular edit.

#### BM2-10 · Locate the failure of the opening rule before adding capacity — I
- **Mechanism.** Run nested feasibility checks: observed mask, equal-size alternate masks, all rows, and external correction. Split failures into bad localization, insufficient writable dimension, and infeasibility even with all rows under the same output constraints.
- **Novelty vs nearest art.** [Localization vs. Editing][localization] already shows a localization–edit gap; [NMKE][nmke] is the sparse mask comparison. This is a diagnostic audit, not a proposal to deploy an oracle.
- **Cheapest first test.** Exhaustively solve a 12-channel synthetic value head with held-out prompt variants; compare activation, intervention and random masks at the same cardinality and same protected reads. Include a case in which a plausible-looking witness misses an unobserved conflict.
- **Old-task retention.** Compare all feasible edit families on held-out neighbours and old tasks at matched revision efficacy. Feasibility on admission probes alone does not count.

## BM23: what plasticity should spend

#### BM2-11 · Establish that a literal token bucket earns its place — I
- **Mechanism.** Charge every block for its committed movement with a persistent token bucket. Test whether capacity-plus-refill is useful independently of any decisions about evidence or write location.
- **Novelty vs nearest art.** [RFC 3290][bucket] gives exactly the recurrence; [ENCORE][encore] checks edit-layer norm growth, while [EWC][ewc] protects important weights. This is a transfer baseline, not a primitive.
- **Cheapest first test.** Feed two-block online regression the same sample multiset in clustered and spaced order, with matched initial margins. Compare tuned step clipping, per-block LR decay, EWC/SI and a rolling movement cap; sweep cap/refill on a separate stream. Include a useful correlated burst that ought to land promptly.
- **Old-task retention.** Measure normal A error after each burst, after recharge and at matched B accuracy; include early B examples after sustained drift.

#### BM2-12 · Make each old read pay only for exposure it actually sees — P
- **Mechanism.** Give each declared old read family a refillable balance for signed margin loss. A candidate pays its measured decrease to every affected family (increases do not refund other debits), plus a small global write charge to limit drift outside the measured families.
- **Novelty vs nearest art.** [AlphaEdit][alpha] protects keys by projection; [OGD][ogd] removes old-gradient components. The proposed unit is *cumulative, family-specific harmful exposure*, not a static constraint or generic knapsack. Compare with exact old-read floors, soft anchor penalties and [replenishable allocation][bwk] fed the same costs.
- **Cheapest first test.** Use a linear readout with separate old directions and two equally sized moves, one benign for both and one harmful only for the rare read. Stress it with an omitted old direction; fail if the anchor control ties or omitted-slice damage simply moves elsewhere.
- **Old-task retention.** Evaluate independently sampled ordinary inputs for both old families and the omitted family, plus previous B, at each depletion.

#### BM2-13 · Do not refund an erased intermediate mistake — P
- **Mechanism.** Separate *unserved* hypothetical writes, which pay only if committed, from *served* intermediate weights. Opposite writes can be coalesced before serving but cannot cancel spent balances afterward, even if the final displacement is zero.
- **Novelty vs nearest art.** [ENCORE][encore] caps matrix norm growth; [SI][si] tracks a learning path and [RFC 3290][bucket] accounts for actual traffic. The proposed operation uses the model's publication boundary to decide when composable corrections are still free to cancel. Compare with always charging both, net displacement, and simple microbatching with the same opportunities to serve.
- **Cheapest first test.** Give two corrections opposite effects on an old read, with a useful orthogonal remainder. Insert an ordinary inference request between them in half the streams, and vary the deadline so delaying every commit cannot win.
- **Old-task retention.** Score A on the intervening request when due, after publication, and after the next B write. Final recovery does not erase a served failure.

#### BM2-14 · Let correlated requests share a write quota only if their effects agree — I
- **Mechanism.** Overlay a second cap for repeated, near-parallel *proposed deltas* pooled across arrival sources, while keeping block quotas. Mint no extra quota just because the same direction arrives from another source.
- **Novelty vs nearest art.** Hierarchical resource accounting is already covered by token-bucket and [replenishable allocation][bwk] baselines. The useful empirical question is whether delta geometry groups repetition better than source identity, not whether two counters are new.
- **Cheapest first test.** Compare duplicate gradients under different feature names, diverse gradients within one source, and a helpful parallel burst. Match accepted movement and query compute against per-source and per-block caps; count missed helpful updates.
- **Old-task retention.** Measure the old slice aligned with the repeated direction and a disjoint slice at equal useful B gains and equal delays.

#### BM2-15 · Make prepayment depend on the chord of a write, not its tangent — P
- **Mechanism.** Test a proposed endpoint on a shadow copy before charging it as a low-collateral write. Use a local linear estimate to reject obvious bad candidates; do not use it alone to admit a finite move across a known activation boundary.
- **Novelty vs nearest art.** [OGD][ogd] protects using an old gradient subspace; that first-order null is not a nonlinear guarantee. Endpoint checking is ordinary validation. The candidate is a reusable debit certificate with an explicit validity region, compared with fresh endpoint checks and conservative step splitting.
- **Cheapest first test.** Use a small ReLU read with zero derivative at the starting point but a harmful response after the proposed step crosses a kink; include a smooth region with many queries sharing one valid bound. Count checks saved as well as false admits.
- **Old-task retention.** Score old inputs on both sides of the kink, including unqueried offsets, after each exposed write and after the next one.

#### BM2-16 · Require the budget to mean the same thing after a harmless rescale — I
- **Mechanism.** Charge function-space movement on a fixed calibration set instead of raw per-block Frobenius movement when two parameterizations implement the same learner. Keep a separate fallback cap for unobserved inputs.
- **Novelty vs nearest art.** [Path-norm work][path] handles rescaling symmetries; [function-space continual learning][function] preserves prior functions rather than parameter coordinates. This tests whether the reservoir has a sensible unit; it does not claim invariance from the word “energy.”
- **Cheapest first test.** Rescale hidden units in a two-layer ReLU model and transport the *same candidate function changes* through both parameterizations. Compare raw norm, path-normalized movement, and matched read-probe cost. Include a direction invisible to calibration.
- **Old-task retention.** Compare A and earlier B outcomes across parameterizations on normal held-out inputs, including the invisible direction. Identical payment on calibration alone is insufficient.

#### BM2-17 · Buy progress at a different block without changing everyone else's computation — P
- **Mechanism.** When a block cannot afford a proposed write, let an alternate block execute a previously checked replacement only if its multi-read effect matches the original proposal on current inputs and respects independently protected reads. The destination pays; the depleted block cannot be credited for moving the request.
- **Novelty vs nearest art.** [WISE][wise] routes between learned weights, and [BWK][bwk] selects affordable alternatives. The candidate is a **write-effect substitution witness** for a normally executed network, not an inference router or a transfer of accounting tokens.
- **Cheapest first test.** Build two residual paths that can equally fix one output, but only one route preserves another stable output. Compare fresh exact selection, greedy cheap-block routing and wait-for-refill; include a case where no substitute exists. Require reuse to save checks over exact selection.
- **Old-task retention.** Evaluate unserved bystander reads and ordinary multi-path inputs after substitution and after the depleted block resumes writing.

#### BM2-18 · Find the burst protection no causal meter can promise — I
- **Mechanism.** Construct a matched useful burst and bad burst with the same observations until the last step. Characterize which write/defer decisions cannot distinguish them without extra evidence, and what latency that evidence costs.
- **Novelty vs nearest art.** [BWK][bwk] separates stochastic and adversarial arrivals. This transfers the observation limit to early continual adaptation, without claiming a universal lower bound from one construction.
- **Cheapest first test.** Enumerate two scalar online-regression streams identical until a confirmation or retraction. Compare immediate commit, holding, random throttling and a cheap noisy extra read; report the best causal frontier, with hindsight only as a reference.
- **Old-task retention.** Score old A on the indistinguishable prefix as well as after the split, and verify early B is still usable after delayed learning.

## Joint descendants: gate and budget must do more together than apart

#### BM2-19 · Decide whether a fact can be revised before its opening closes — P
- **Mechanism.** Before opening a live scope, compute a lower bound on the required movement and an upper bound on what its allowed blocks can pay before expiry. If the first exceeds the second, avoid a half-revision; retain evidence or request a narrower correction instead.
- **Novelty vs nearest art.** [NMKE][nmke] plus token buckets can mask and meter independently; [BWK][bwk] supplies feasibility accounting. The candidate is a scope-conditioned bound on *learning movement* that can reject an otherwise admissible edit, not a new scheduling result.
- **Cheapest first test.** Exact tiny linear solves with one cheap correctable fact and a second fact requiring an expensive channel whose refill comes too late. Compare against eager partial updates, deferred exact solves and the stacked gate/bucket. Include a loose bound requiring a full solve.
- **Old-task retention.** Check neighbours after refused and partial paths (including exposed prefixes), and previously learned B after retrying with genuinely new evidence.

#### BM2-20 · Revalidate the read only if intervening spending could change it — P
- **Mechanism.** Cache the gap between the last included and first excluded channel at opening. Accumulate conservative drift bounds for changes to its upstream read path; spend this gap only to decide whether the old mask is still valid. It grants no budget for the fact update itself.
- **Novelty vs nearest art.** [NMKE][nmke] gives dynamic attribution and [GRACE][grace] has activation-based lookup; ordinary cached bounds expire under drift. The candidate is a **spend-indexed read-validity certificate**, compared with re-attribution at every step or expiry by wall clock.
- **Cheapest first test.** Let equal-norm writes land on and off the path into a thresholded key. Construct a third case where upstream drift changes which answer was recalled even though top-k membership stays fixed; require a separate answer margin bound or re-read.
- **Old-task retention.** Re-evaluate old ordinary inputs near the switching boundary and remote inputs after eventual commit; no credit for a certificate that saves calls by missing stale scopes.

#### BM2-21 · Require a joint debit for a revision with indivisible consequences — P
- **Mechanism.** An edit across two retrieved blocks can be staged and published as a single event only when both local balances can pay and both output constraints hold. If either is missing, publish neither; retain only bounded evidence for retry.
- **Novelty vs nearest art.** [MEMIT][memit] already edits multiple layers and [EVEDIT][evedit] specifies event boundaries. Atomic publication is not new. Test whether making the *minimal jointly writable fact* the unit of payment avoids harmful intermediate behaviours that per-block admission plus ordinary batching cannot avoid at equal latency.
- **Cheapest first test.** Design a two-hop fact with a shared side relation that is broken by either partial write but intact after both; add a case where there is a safe partial order. Compare atomic global editing, independent block throttling and latency-matched buffering.
- **Old-task retention.** Score ordinary chain and side-relation queries at each public model version, including while deferred. Retest earlier B after the joint update and ordinary traffic that follows.

#### BM2-22 · Spend a little to diagnose shared interference before a full revision — P
- **Mechanism.** Use a bounded shadow intervention inside the currently opened rows to predict whether scaling the write will flip a protected neighbour. Charge the diagnostic to a separate probe budget; charge movement only if weights are published.
- **Novelty vs nearest art.** [ROME][rome] uses interventions to localize memory and [Localization vs. Editing][localization] cautions that localization does not tell us editability. The proposed diagnostic tests the *candidate update*, not recall attribution. Compare fresh full endpoint shadow checks, clipped updates and scale line search with identical compute accounting.
- **Cheapest first test.** Give a sparse MLP two edits with similar infinitesimal effects, one crossing a harmful nonlinear boundary only at higher dose. Count small interventions that correctly eliminate unsafe directions; stop if exact shadow evaluation is as cheap or prediction is unreliable.
- **Old-task retention.** Score held-out old inputs near and far from the boundary after the scaled accepted update, and recheck at normal later writes.

#### BM2-23 · Stop independent contradictions from spending the same old behaviour twice — P
- **Mechanism.** Tie active scopes to a shared old-read balance, even if they expose disjoint parameter rows. Check the next commit using remaining balance on that read, so two individually tolerable edits cannot quietly apply the same tolerated damage twice.
- **Novelty vs nearest art.** [AlphaEdit][alpha] preserves an anchor key set and [BWK][bwk] accounts for shared resources. The claim is about a **read-defined shared debit across disjoint masks**. Compare static floors, rolling validation, and the stacked localized gate with resource allocation on identical loss observations.
- **Cheapest first test.** Use two nonoverlapping write channels contributing independently to one old output. Give each edit a collateral drop of 0.6 against a remaining tolerance of 1 and add an equally informative alternate edit on the second channel with no drop. Include disjoint-effects and redundant-probe negatives.
- **Old-task retention.** Re-test the shared output using ordinary unseen inputs after each commit and after refill; keep unaffected A and previously learned B in the check.

#### BM2-24 · Keep the correction provisional when the base cannot afford a write — I
- **Mechanism.** Serve a verified correction from a compact provisional store while the in-place budget refills. Convert it into a base write only after a fresh contradiction with the *base* read, not merely repeated success from the provisional route.
- **Novelty vs nearest art.** [GRACE][grace] and [WISE][wise] already separate edited knowledge from base weights. This is a fair test of when consolidation earns its cost, not a novel dual-memory primitive. Compare persistent adapters, write-only with buffering, and routing plus a literal token bucket.
- **Cheapest first test.** Vary how often a corrected fact appears on new paraphrases missed by provisional lookup. Match peak bytes; measure latency and the number of base revisions avoided. Include a purely transient correction that should never reach the base.
- **Old-task retention.** Evaluate ordinary queries through the live router, plus base-only A and B after consolidation and after the provisional entry is retired.

#### BM2-25 · Retain a witness for why the right read could not be revised — P
- **Mechanism.** Keep a compact refusal witness that distinguishes missing read support, inconsistent trusted evidence, and insufficient local movement. Reconsider only when its named condition changes; never treat refill as new contradiction evidence.
- **Novelty vs nearest art.** [NMKE][nmke] supplies support selection, [EVEDIT][evedit] semantic scope, and [BWK][bwk] budget state. The candidate is a **failure-specific retry operation** shared by these layers, not three error codes. Compare exact re-solving on every arrival, periodic retry and independent controllers that cache their own failures.
- **Cheapest first test.** Construct equal-loss corrections with each distinct bottleneck, then vary the order of new probes, evidence and refill. Match storage and maximum decision delay; count retried solves and valid corrections missed by a stale diagnosis.
- **Old-task retention.** Test normal old inference while waiting, after successful retries, and on the nonrecovering branch; verify earlier B stays learned through repeated refusals.

#### BM2-26 · Let two valid corrections share one deployment, not one claim — P
- **Mechanism.** Search for a joint in-scope delta that realizes two separately verified contradictions for less movement than applying each alone. Both must be executable against the same pre-write read state; if one expires or is withdrawn, re-solve instead of publishing an inseparable partial edit.
- **Novelty vs nearest art.** [MEMIT][memit] already amortizes many edits and [ENCORE][encore] constrains edit norm. The only new claim would be that **two independent live permissions** can jointly afford an in-place change before expiry that separate solves cannot afford under their individual masks, without opening anything outside the union. Compare latency-matched batched MEMIT/AlphaEdit and batch NMKE with shared budget.
- **Cheapest first test.** Solve two compatible overlapping linear constraints for a single minimum-cost delta, then introduce a conflicting alternative or withdraw evidence just before commitment. Measure revision throughput at matched movement and delay, not merely the triangle inequality.
- **Old-task retention.** Test old interleaved requests before publication, shared neighbours and earlier B after it, and all old tasks on the revoked branch without counting the withheld correction as learned.

## Ranked deeper questions

1. **When does the live read offer enough writable support for a reliable revision?** Map the gap between a live causal mask, NMKE, an equal-size best mask, and all rows at matched write norms and retained outputs (BM2-02/06/10). Vary sparsity, shared features and paraphrase spread independently. If live scopes usually lose to equally small masks over unseen queries, prioritize evidence validation over weight-level reconsolidation.
2. **What should a regenerating budget measure: weight travel, effect on ordinary old behaviour, or both?** Replay the same on-path and off-path rescalings and burst schedules across token bucket, output-loss debit and hybrid (BM2-11/12/16/23). Report held-out A/B retention at equal sustained B gain and latency, including omitted probes and long drift. If the hybrid only protects the instrumented probes, it is not a retention primitive.
3. **Does coupling permission to spend change the achievable tradeoff or just avoid some work?** Cross fresh vs reusable scopes with independent vs scope-conditioned budgets (BM2-19/20/21/26). Include coupled factual updates and the strongest stacked controller; compare with a tiny exact causal optimizer on the same observations. A legitimate efficiency result is fewer probes at the same admitted writes; a Pareto claim also needs lower collateral or delay on unseen traffic.
4. **What extra observation justifies betting on an irreversible edit before ambiguity resolves?** Pair a legitimate reversal with a conflicting but valid alternate view, and a valuable burst with an indistinguishable harmful one (BM2-01/05/18/24). Compare waiting, provisional inference, and a budgeted targeted read. If matching all available observations eliminates any advantage, report the information limit rather than inventing a smarter gate.

[parent]: https://github.com/manojbajaj95/cl/pull/308
[ledger]: https://github.com/manojbajaj95/cl/blob/a122f42fc22cce58c2acaa84184a18dec9a5fe55/reviews/idea-ledger.md
[triage]: https://github.com/manojbajaj95/cl/blob/a122f42fc22cce58c2acaa84184a18dec9a5fe55/reviews/flood-triage.md#L426-L429
[nader]: https://doi.org/10.1038/35021052
[sevenster]: https://doi.org/10.1126/science.1231357
[rome]: https://arxiv.org/abs/2202.05262
[memit]: https://arxiv.org/abs/2210.07229
[alpha]: https://arxiv.org/abs/2410.02355
[nmke]: https://arxiv.org/abs/2510.22139
[localization]: https://arxiv.org/abs/2301.04213
[grace]: https://arxiv.org/abs/2211.11031
[melo]: https://arxiv.org/abs/2312.11795
[wise]: https://arxiv.org/abs/2405.14768
[evedit]: https://arxiv.org/abs/2402.11324
[mquake]: https://arxiv.org/abs/2305.14795
[ewc]: https://arxiv.org/abs/1612.00796
[si]: https://arxiv.org/abs/1703.04200
[ogd]: https://proceedings.mlr.press/v108/farajtabar20a.html
[encore]: https://arxiv.org/abs/2502.01636
[bucket]: https://www.rfc-editor.org/rfc/rfc3290.html#appendix-A
[bwk]: https://arxiv.org/abs/2306.08470
[meta]: https://doi.org/10.1016/S0166-2236(96)80018-X
[plasticity]: https://arxiv.org/abs/2306.13812
[path]: https://arxiv.org/abs/2310.01225
[function]: https://arxiv.org/abs/2403.10929
