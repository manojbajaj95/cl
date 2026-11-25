# Child: Learnability certificates and fork invalidation

Child node (depth 3) · 30 candidate cards (AL4-01–AL4-30) · 5 ranked deeper questions · Ideas only; no experiments run

**Request (Manoj).** Build on the two ideas rated 3 in [PR #406](https://github.com/manojbajaj95/cl/pull/406), aiming for genuinely new primitives. The read line deepens [AL3-01](./abliteration-learners-3.md#al3-01--a-counter-that-carries-a-map-for-future-reads), [AL3-06](./abliteration-learners-3.md#al3-06--reconstruct-what-the-source-changes-not-what-the-source-looks-like) and [AL3-13](./abliteration-learners-3.md#al3-13--choose-the-counter-that-minimizes-worst-reader-tuition). The fork line deepens [AL3-16](./abliteration-learners-3.md#al3-16--a-fork-witness-with-a-continuation-contract), [AL3-24](./abliteration-learners-3.md#al3-24--retest-only-the-suffix-regime-that-could-reverse-the-comparison) and [AL3-28](./abliteration-learners-3.md#al3-28--keep-a-later-correction-from-rewriting-credit-for-the-first-choice).

**Thesis.** A frozen read map by itself is a compatibility transform. A table of action values under multiple finishers is policy evaluation. The bets here are two operations those objects could support: *admit or deny a future reader based on what its edit preserved*, and *invalidate only the fork preferences a particular solver change could reverse*. Both have to deliver fewer labels or verifier calls at matched behavior, not just a new name for a score.

## Is this pursuable? Short answer

- **Read primitive: a counter ships a frozen map and an auditable boundary for later readers.** Fit the rank-1 source-keyed counter and a small read map on unlabeled clean/edited source-swap pairs. For each candidate counter/map pair, estimate which declared source contrasts remain distinguishable above live-view noise. Choose for later learnability at equivalent present correction. Freeze both the map and its boundary before revealing independently drawn legitimate consumers. The boundary should let a later learner decide whether to use the frozen map, request more evidence, or use a different view. Test both accepted and rejected readers. A map cannot restore absent information, and ambiguity on a finite witness set is not a universal impossibility result.
- **Fork primitive: a solver change queries a continuation contract.** Inhibit only the first premature commitment to nominate actions. Restore the clean model; force each action from the same prefix and record verifier-score differences across a policy panel, including a policy without the relevant repair capability where feasible. Fit the clean writer only on scoped accepted-minus-failed preferences. After a solver replacement, spend revalidation budget on forks whose sign could become unstable *under that change*, not merely those historically close to zero. Audit a random sample of skipped forks; that audit is charged and does not re-label the skipped pool.

**Scope.** The revised [idea ledger](https://github.com/manojbajaj95/cl/blob/5e603e4021dca7a8657458ba377a539a48d6e133/reviews/idea-ledger.md) and [flood triage](https://github.com/manojbajaj95/cl/blob/5e603e4021dca7a8657458ba377a539a48d6e133/reviews/flood-triage.md) keep both directions at 3. Don't claim novel alignment, robust preference learning, or policy reuse. The contribution must be an operation on an edit or verified fork that plain alignment or policy reuse cannot match at equal total cost. Keep tasks benign and preserve original policy behavior; refusal suppression is not an aim.

**Shared conventions.** Everything below is proposed. Use a CPU-identifiable toy and then a small model with independent evidence of the shortcut. Separate nomination, fitting, calibration and held-out task or solver families. For read cards, fix present correction and retention, charge taps, map state, calibration and serving time, and report later labels to a preset accuracy target (count failures). Give alignment baselines the same sites, pairs, output dimension and calibration budget; include both absolute-view and swap-difference inputs. For fork cards, charge discovery, clean replay, panel estimation, audits, verifier calls and tokens; match total rollouts and verifier calls across RFT, STaR and GRPO before comparing full cost. Recheck gain on a clean restart with no inhibition or rollout cache. Every card inherits the base-task and fixed policy-sentinel retention check.

## Literature check

Named-control positioning from #406, not a new priority search. Every card inherits its branch's controls and highlights the test most likely to falsify it.

| Line | Already available | What a card here must add |
|---|---|---|
| Preserve future readers (A–B) | [Backward-compatible training (BCT)](https://arxiv.org/abs/2003.06343) and BCT-style learned transforms; [model stitching](https://arxiv.org/abs/2106.07682); Procrustes/CCA; raw source taps, same-tap ReFT/LoRA, sink-local ablation, LEACE, and stored examples | Compare frozen transforms trained on the same unlabeled pairs and a stitch trained against old legitimate heads at the same fitting budget. Test all with the same future head and routing budget. Must beat the strongest alignment plus a generic uncertainty gate, not just a raw tap. |
| Reuse verified first forks (C–D) | Step-DPO, VinePPO, [generalized policy improvement (GPI)](https://arxiv.org/abs/1606.05312), iterative DPO with relabeling, RFT, STaR, GRPO; pooled clean forks, interval-plus-abstention, and fresh branching | Give GPI and clean-fork methods the same panel and solver-change information. Compare wrong-sign writes at equal audit and verification cost against fresh/iterative relabeling; the claim is surgical invalidation, not choosing the best evaluated panel policy. |

## A · Make a frozen map state which future reads it can support

### AL4-01 · Ship an admissibility test with the read map
- **Primitive** (a frozen counter emits a map and a test that can reject a later reader before training it).
- **Mechanism:** Fit the map on benign source-swap pairs. For a declared source family, retain a small sketch of the contrast errors and the live-view noise. For a requested read direction, project both sketches onto that read and test whether a conservative lower bound on the recovered contrast clears the requested precision. Admit, abstain, or offer a different allowed view without refitting the map.
- **Nearest prior / gap:** BCT-style transforms, stitching and Procrustes/CCA align views; compare them with identical gates. Novelty would be the pretraining admission operation that predicts cost for a reader not yet fitted.
- **Cheapest first test:** Freeze three maps with similar reconstruction, draw unseen table readers needing different contrasts, and test at equal routing coverage. **Kill** if alignment or stitching plus a generic signal-to-noise gate predicts labels-to-target just as well.
- **Old-task retention:** Original correction and legitimate consumers with the same map enabled.
- **Risk / likely tie:** Some tasks cannot state their desired contrast without labels. The operation is scoped to tasks with declared input distinctions; AL4-06 tests the weaker-information setting.

### AL4-02 · Return an ambiguity witness, not a low score
- **Primitive** (a rejected reader can receive an explicit pair that its live view fails to distinguish).
- **Mechanism:** Store a compact reference to two matched source-swap cases whose clean source values differ but whose edited-view contrast is inside the measured noise floor. Use such witnesses to explain a denied read and nominate a relevant alternative tap, not to infer irrecoverability beyond the observed interface.
- **Nearest prior / gap:** Contrastive examples, conditional independence tests and #406 AL3-06; add a concrete witness that informs recovery rather than a scalar failure score.
- **Cheapest first test:** Make two readers equally low-scoring by global reconstruction but only one ambiguous in the live view. **Kill** if CCA residuals with nearest-pair retrieval recover the useful alternative view at equal memory and calls.
- **Old-task retention:** Existing legitimate reuse in the ambiguous cases and the original corrected task.
- **Risk / likely tie:** One noisy pair may be accidental; require corroboration on fresh matched cases and keep the rejection scope local.

### AL4-03 · Compare counters by the evidence matrix, not mean alignment
- **Primitive** (a present-day counter is selected using the worst-supported contrast in a frozen reader family).
- **Mechanism:** Estimate a noise-normalized separation matrix on a small panel of intervention responses, then score the weakest requested contrast in the predeclared family. Freeze the chosen counter and map. Retain competing current-equivalent maps for diagnostic comparison.
- **Nearest prior / gap:** E-optimal design, whitening, CCA and AL3-13; test whether the matrix predicts intervention-specific future evidence needs after a counter, not whether a minimum eigenvalue is new.
- **Cheapest first test:** Plant common low-noise source contrasts and an uncommon one with similar clean magnitude. **Kill** if Procrustes/CCA plus matched whitening or an ordinary conditioning criterion predicts later label cost equally well.
- **Old-task retention:** Existing rare legitimate uses, not just common source consumers.
- **Risk / likely tie:** The weakest contrast can be dominated by estimation noise; use shrinkage and calibration folds shared across arms.

### AL4-04 · Isolate the value of choosing the counter, not just the map
- **Improvement / assay** (determine whether later learnability belongs to the edit decision).
- **Mechanism:** Cross learned versus fixed current-equivalent counters with learnability-selected maps versus standard alignment. Hold the live feature budget and future reader constant, including action admission gates where available.
- **Nearest prior / gap:** BCT, stitching, AL3-01's counter/map factorial; this test checks whether optimization on contrasts actually has an interaction with counter choice.
- **Cheapest first test:** Two counter sites in a toy table relay with one planted downstream reader and one independently sampled reader. **Kill** the coupled primitive if fixing the counter and using ordinary stitching matches the joint method.
- **Old-task retention:** Current error and prior readers matched before and after the future-read update.
- **Risk / likely tie:** No overlap in current correction prevents the factorial comparison; report that as uninformative rather than relaxing constraints post hoc.

### AL4-05 · Make compatibility with existing readers a deliberate placebo
- **Improvement / assay** (distinguish read recovery from making the next skill cheaper).
- **Mechanism:** Tune a BCT-style transform or stitch to match current legitimate heads, then match or stratify maps on current head agreement. Fit the same unseen later readers on each frozen view and check whether contrast-based selection adds predictive value within each stratum.
- **Nearest prior / gap:** BCT's backward compatibility is an explicit control; agreement with old heads should not be mistaken for accessible source information for new heads.
- **Cheapest first test:** Give old readers one projection of a two-factor benign source and hold out the other for independently drawn tasks. **Kill** if current-head-compatible maps match both latent-factor tasks and unrelated controls with the same bytes.
- **Old-task retention:** Old heads under the edited read interface and as actually deployed.
- **Risk / likely tie:** A deliberately blind historical head panel can be too easy to beat; include a richer matched head panel from independent old tasks.

### AL4-06 · Ask one unlabeled question before training a future reader
- **Primitive** (the preserved interface supplies a query that identifies whether a future read is in scope).
- **Mechanism:** A later learner receives a task description but no explicit source contrast. Ask it to nominate a benign pair of inputs that should be distinguished, without supplying answers; test the pair through the frozen map to choose a view or reserve labeling budget.
- **Nearest prior / gap:** Active learning and BCT-style compatibility checks; test admission from task-intent pairs before any target examples are labeled.
- **Cheapest first test:** Hold out rule descriptions with unseen legitimate table comparisons. **Kill** if a generic embedding-distance heuristic with the same nominated inputs matches labels-to-target and rejection errors.
- **Old-task retention:** Existing reads for tasks that reuse those inputs under different descriptions.
- **Risk / likely tie:** A description may leak enough to solve the reader in context; give every baseline the same description and pair.

### AL4-07 · Hold out nuisance regimes, not just contrast pairs
- **Improvement / assay** (test whether the map preserves the requested distinction under a benign distribution change).
- **Mechanism:** Fit on matched source swaps under two nuisance regimes; test future readers on a third regime in which the nuisance–source relationship reverses. Compare alignment on absolute states and on the exact same changes.
- **Nearest prior / gap:** Causal/invariant representation learning and AL3-06; checks whether the reported future learnability is stable under modest shifts, not just a lucky fit.
- **Cheapest first test:** Change formatting and field order separately while retaining the source's semantics. **Kill** if swap-difference CCA or model stitching generalizes as well.
- **Old-task retention:** Earlier formatting regimes, including legitimate nuisance uses.
- **Risk / likely tie:** Test views may no longer support the contrast at all; distinguish map failure from a changed physical interface.

### AL4-08 · Mask only the reader labels; keep baseline information equal
- **Improvement / assay** (prevent an unfair comparison to alignment methods).
- **Mechanism:** Provide each baseline equal clean and edited views, access to the same swap metadata and admissible old-head data, plus identical later examples. Fit labels-to-target curves with the same regularizer selection and repeated hidden-reader draws.
- **Nearest prior / gap:** #406's raw-tap control and matched stitching; detects savings caused by granting the new map better unlabeled evidence or supervision.
- **Cheapest first test:** A two-factor toy followed by a small-model table stream. **Kill** the map-specific claim if the advantage disappears when aligners receive swap metadata and the same regularization budget.
- **Old-task retention:** Same fixed tasks and legitimate reader checks across transforms.
- **Risk / likely tie:** Equal parameter counts can conceal different serving state; account for both.

## B · Make the boundary actionable across edits

### AL4-09 · Route complementary maps by missing contrast
- **Primitive** (a future reader can assemble only the supported parts of its read).
- **Mechanism:** Ship two narrow frozen maps from different permitted views, each with evidence for different contrasts. Map a composite future read into supported components; use both views only if a requested distinction requires both, otherwise use the cheaper one.
- **Nearest prior / gap:** Multi-view CCA and routed adapters; compare admission and fallback at equal combined capacity rather than comparing two maps to one small stitch.
- **Cheapest first test:** Later readers require either one source factor or a combination. **Kill** if joint CCA or a same-cost two-view stitch matches label cost and serving usage at equal accuracy.
- **Old-task retention:** Original correction and earlier reads when both views are active.
- **Risk / likely tie:** Component semantics may be additive only on a toy; hold out nonlinear combinations and allow abstention.

### AL4-10 · Find the smallest rescue view for a denied read
- **Primitive** (a failed read test returns the minimal extra access worth trying).
- **Mechanism:** Rank allowed alternative source views by how much they restore the particular contrast in the ambiguity witness. Offer one small independent tap only when its expected label savings exceed a fixed serving budget.
- **Nearest prior / gap:** AL3-04 relocation, feature acquisition and conditional computation; the hypothesis is targeted rescue of the denied distinction without lifting all future readers into a larger interface.
- **Cheapest first test:** Offer three equally sized tap candidates to readers needing different missing factors. **Kill** if active feature selection or a raw-tap classifier with the same witness chooses equally efficient rescues.
- **Old-task retention:** Present correction and legitimate tasks sharing the rescue site while the tap is active.
- **Risk / likely tie:** A broadly informative tap might dominate for every task; then retain that tap rather than claiming adaptive rescue.

### AL4-11 · Compose only the evidence that survives a second counter
- **Primitive** (the admissible family can be narrowed across edits without refitting already shipped read maps).
- **Mechanism:** Keep the first map frozen. Fit a second per-edit change certificate on paired contrast witnesses and transport only distinctions whose shared support remains adequate. Retest a small sample of carried distinctions to detect falsely optimistic composition.
- **Nearest prior / gap:** AL3-09 map composition and ordinary stitching chains; the operation composes admission evidence, not merely transformation matrices.
- **Cheapest first test:** Two counters each perturb a different downstream view. **Kill** if direct BCT-style refresh or composed CCA plus a generic gate gives the same later label savings at the same update cost.
- **Old-task retention:** Both original corrections and the oldest already deployed legitimate reader.
- **Risk / likely tie:** Intersecting scopes may be overly conservative; measure lost useful readers as well as bad admissions.

### AL4-12 · Audit a reader that passes one map but fails another
- **Improvement / assay** (separate a practical training advantage from different score calibration).
- **Mechanism:** Sample disagreements at equal advertised admission coverage, then teach those readers blind to the gate's prediction. Score labels-to-target, failure rate and calibration in each disagreement direction.
- **Nearest prior / gap:** Selective prediction and BCT-style validation; measures decision utility rather than recalibrating thresholds until a chosen map wins.
- **Cheapest first test:** Same held-out readers for contrast map, stitch and CCA gates. **Kill** if disagreements are indistinguishable from threshold noise or no more informative than raw reconstruction loss.
- **Old-task retention:** All retained pre-existing reads at the fixed thresholds.
- **Risk / likely tie:** Disagreement sampling changes the test mix; report the original population coverage alongside targeted audits.

### AL4-13 · Reserve a read for opposite future labels
- **Primitive** (an edit preserves a two-sided distinction without choosing its future label).
- **Mechanism:** Challenge a frozen map with two later legitimate tasks requiring opposite labels over the same source contrast. Both should be easy to teach once the user supplies the rule; the earlier correction must not bias either sign.
- **Nearest prior / gap:** Task-blind feature alignment and AL3-10; test whether learnability preserves a reusable distinction rather than smuggling in a default preference.
- **Cheapest first test:** Independently assign ascending or descending to an unseen table operator after map freeze. **Kill** if Procrustes/CCA or a backward-compatible stitch achieves the same symmetric labels-to-target at equal dimension.
- **Old-task retention:** Existing legitimate ordering operations when both later readers are present.
- **Risk / likely tie:** Linear binary heads can flip a sign for free after fitting; use unseen qualified combinations as a second condition.

### AL4-14 · Export a smaller map only for the rights it keeps
- **Primitive** (compression can explicitly withdraw some future read guarantees).
- **Mechanism:** When shrinking a shipped map, identify contrast families whose measured separation falls below the prior admission threshold. Update the published admissible family and let later readers request only views still supported.
- **Nearest prior / gap:** Adapter compression, feature alignment and selective prediction; the bar is avoiding false admissions under a resource change, not compression itself.
- **Cheapest first test:** Compress a map to two ranks while retaining or withdrawing reads by the frozen contrast evidence. **Kill** if generic low-rank truncation plus recalibration on old heads matches future failure and label cost.
- **Old-task retention:** Old completed readers supported by the smaller map and suppression of the original shortcut.
- **Risk / likely tie:** Revalidation metadata may cost more than the saved map bytes; count it explicitly.

### AL4-15 · Measure when one unlabeled audit repays its cost
- **Improvement / assay** (find the lifetime boundary for carrying a map and its evidence).
- **Mechanism:** Compare amortized labels, calibration forwards, storage and serving cost as the number and diversity of hidden future readers rise. Include source sample replay and cheap standard alignment without admission.
- **Nearest prior / gap:** #406 AL3-14 lifecycle accounting; check the new admission operation against ordinary time-to-teach and retention.
- **Cheapest first test:** Reveal one, three, then eight independent legitimate readers after freezing. **Kill** if stitch, CCA or equal-byte stored examples dominate every plausible regime.
- **Old-task retention:** Require nonregression on the original correction and earlier readers at every step.
- **Risk / likely tie:** Repeated readers from a narrow family inflate amortization; vary family membership and report one-reader cost.

## C · Make the continuation contract depend on what the solver changed

### AL4-16 · Invalidate a fork using the solver's change footprint
- **Primitive** (a solver update can invalidate a subset of stored preferences without relabeling the full fork pool).
- **Mechanism:** For each clean forced-action fork, store its margins across the policy panel and whether each branch can encounter the relevant repair capability. For a comparable deployed policy with an old positive lower margin bound `m`, skip revalidation if the certified absolute changes to the two branch values, `d₊` and `d₋`, satisfy `m > d₊ + d₋`; recheck otherwise, including unknown coverage. Use exact reachability first in a finite simulator; in a model use estimated footprints with audits, not guarantees.
- **Nearest prior / gap:** GPI selects using policy values; iterative DPO refreshes labels; Step-DPO/VinePPO supply branch data. The proposed operation uses a *particular capability change* to narrow which old local preferences need new evidence.
- **Cheapest first test:** Construct two solver upgrades with equal global policy distance affecting disjoint downstream repairs. **Kill** if GPI over the same panel, pooled sign intervals plus a drift gate, or fresh branching achieves the same wrong-sign rate at equal revalidation cost.
- **Old-task retention:** Old forks outside each footprint and settings where the habitual first action is legitimate.
- **Risk / likely tie:** A capability tag is not a proof of nonreachability. An unbounded or unobserved change must not be classified stable.

### AL4-17 · Cancel a shared suffix effect before revalidating the fork
- **Primitive** (verified shared continuation effects are removed from the bound on preference drift).
- **Mechanism:** In a finite task, mark where both forced branches reach the same sufficient state with the same remaining budget and reward semantics. Solver updates affecting only that common tail change both values equally and therefore leave the difference intact. For partially shared tails, use a bound on unequal reach probability and retest if needed.
- **Nearest prior / gap:** Bellman decompositions and transposition reuse; the test is whether shared-suffix cancellation avoids valid rechecks beyond independent action-value bounds or plain GPI.
- **Cheapest first test:** Use forks with identical, unequal and nonoverlapping tail occupancy under a local benign repair upgrade. **Kill** if a matched state-based GPI cache plus intervals saves the same calls at equal stale-sign error.
- **Old-task retention:** Old forks with unequal prefix costs and cases where apparent merging must not justify reuse.
- **Risk / likely tie:** Matching visible text is not sufficient state equivalence; include elapsed steps, budget and any hidden state affecting return.

### AL4-18 · Use a no-repair panel member as a discriminating witness
- **Primitive** (the panel can say which comparisons depend on a particular recovery, rather than merely report inter-policy variance).
- **Mechanism:** Pair a clean solver with a version barred from one legitimate downstream repair, otherwise using the same rules. Identify changes to the fork sign or margin sensitive to that repair and retain the paired measurements as queryable contract evidence.
- **Nearest prior / gap:** AL3-28, GPI policy panels and ablation studies; the question is whether a minimally matched pair helps route future revalidation better than random solver diversity.
- **Cheapest first test:** Compare equal-sized panels with and without a matched no-repair member on an unseen repair upgrade. **Kill** if alternative policy panels or branch-temperature trials identify unstable forks as accurately at equal samples.
- **Old-task retention:** Tasks where recovery is valid and valuable, and nonrepairable tasks that shared the same first action.
- **Risk / likely tie:** Silencing repair may change earlier downstream behavior too; verify policy differences outside that repair or mark the footprint broader.

### AL4-19 · Compare preferences under each policy before selecting a policy
- **Improvement / assay** (distinguish margin reuse from choosing a different finisher for each action).
- **Mechanism:** Report paired action differences under each fixed finisher, and separately a GPI arm with its legitimate policy selection. Do not substitute a difference of independently maximized action values for a stable sign under one deployed solver.
- **Nearest prior / gap:** GPI and off-policy action evaluation; the two comparisons answer different deployment questions and neither gets called a novel objective.
- **Cheapest first test:** Give two actions different best finishers while keeping the deployed finisher fixed on selected tasks. **Kill** the contract advantage if GPI plus solver-aware uncertainty matches wrong-sign writes and revalidation cost under the same deployment constraints.
- **Old-task retention:** Tasks where changing the finisher is permitted and tasks where the old finisher must stay fixed, reported separately.
- **Risk / likely tie:** GPI's ability to switch finishers can be a real win in some deployments; report that scenario instead of forbidding a useful baseline everywhere.

### AL4-20 · Turn an unseen repair into a coverage failure, not a stable sign
- **Primitive** (contracts can explicitly invalidate outside-panel reuse before checking every affected preference).
- **Mechanism:** Test the new solver on a small shared panel of diagnostic suffixes. If a behavior change falls outside recorded footprint categories, treat associated forks as unknown and broaden the audit rather than trusting past sign agreement. Inspect how much invalidation is needed to attain the error target.
- **Nearest prior / gap:** Distribution-shift detection and interval-plus-abstention; compare targeted unknown-scope invalidation with ordinary global abstention.
- **Cheapest first test:** Add a solver capable of a repair absent from every previous panel member. **Kill** if a generic policy drift test is as selective at the same wrong-sign risk and verifier cost.
- **Old-task retention:** Old preferences not involving the new repair and older legitimate handling of the repaired cases.
- **Risk / likely tie:** A small shared diagnostic set may miss a rare solver capability; random audits of assumed-stable forks remain required.

### AL4-21 · Hold out solver changes, not just solver names
- **Improvement / assay** (check whether a footprint abstracts the kind of update instead of recognizing known solvers).
- **Mechanism:** Separate policy-panel estimation from final upgrades by both solver identity and capability transition. Hold out replacements that change an untrained combination of continuation behaviors while keeping the first fork observable.
- **Nearest prior / gap:** AL3-24's held-out solver and policy generalization tests; expose whether panel performance is merely interpolation by solver identity.
- **Cheapest first test:** Fit on isolated tolerance and recovery-speed changes; test a held-out simultaneous change under equal rollout budgets. **Kill** if the contract only works for solver changes already used to calibrate its footprints.
- **Old-task retention:** All earlier configurations, scored independently rather than averaged.
- **Risk / likely tie:** Unknown changes may warrant broad invalidation; score abstention and coverage so universal abstention cannot win.

### AL4-22 · Separate discovery credit from invalidation credit
- **Improvement / assay** (test first-commitment inhibition independently of the new contract).
- **Mechanism:** Cross clean versus briefly inhibited discovery with pooled versus footprint-conditioned contracts. Match the number of proposals and charged clean replays. Evaluate clean writes before and after a held-out solver change.
- **Nearest prior / gap:** AL2-16 and AL3-18, best-of-N RFT and STaR; contract usefulness must not be assigned to inhibition, and a better sampler must not be credited as a better invalidator.
- **Cheapest first test:** Two symbolic forks, one with inherently rare alternatives and one easy to branch cleanly. **Kill** the combined claim if clean VinePPO-style branching plus an ordinary interval gate matches the stacked method.
- **Old-task retention:** Correct uses of the heuristic during clean serving, before and after solver replacement.
- **Risk / likely tie:** Clean branches given optimal actions by a script are a ceiling, not an equal-search baseline; give every arm the same proposal interface.

### AL4-23 · Measure the missed sign flips among skipped forks
- **Improvement / assay** (charge and verify the apparent savings from not relabeling stable forks).
- **Mechanism:** Randomly audit a prespecified sample from the skipped set and independently replay both branches with the new solver. Estimate missed flip rate and its uncertainty; compare on the same sampled population with interval abstention and iterative DPO.
- **Nearest prior / gap:** Selective-risk auditing and AL3-24; this is the required falsifier for selective revalidation, not a new update method.
- **Cheapest first test:** Seed rare reversals in an otherwise stable fork stream. **Kill** selective reuse if uncertainty on missed flips prevents ruling out a worse error rate than fresh verification at the required coverage.
- **Old-task retention:** Audit nominally stable old-task forks as well as current ones.
- **Risk / likely tie:** Tiny audits cannot certify rare errors; report the largest miss rate compatible with the sample.

## D · Make the contract useful when solvers change repeatedly

### AL4-24 · Distinguish the changed policy from a changed task goal
- **Primitive** (a stored comparison can separately invalidate a solver assumption and a verifier assumption).
- **Mechanism:** Store branch outcome summaries and which repair judgments made the preference valid. When the solver alone changes, recheck vulnerable continuations; when the verifier alone changes, rescore compatible summaries before replaying anything.
- **Nearest prior / gap:** AL3-23 reward relabeling, iterative DPO and GPI; the novelty bet is cheaper targeted updates when the two axes change independently rather than retrying all previous forks.
- **Cheapest first test:** Change a benign arithmetic tolerance and an allowed downstream correction in separate updates. **Kill** if capped replay plus ordinary relabeling matches total cost and wrong-sign error.
- **Old-task retention:** Old task goals still explicitly requested and old forks with unchanged solvers.
- **Risk / likely tie:** An outcome summary may not support rescoring under a genuinely new verifier; classify such forks unknown.

### AL4-25 · Revalidate a capability once for a family of forks
- **Primitive** (one shared probe can update dependencies of multiple fork witnesses within a measured applicability range).
- **Mechanism:** Find a recurring repair capability with an independent success probe. Update its estimated strength once after a solver change, use stored branch sensitivity to decide which fork intervals need rechecking, and validate transfer on random family members.
- **Nearest prior / gap:** Successor features, GPI and modular policy evaluation; must beat a GPI/successor-feature baseline with the same decomposition rather than claim that sharing statistics across tasks is new.
- **Cheapest first test:** Many table forks use one downstream rounding repair in different contexts. **Kill** if the shared probe fails to predict new-solver reversals beyond generic solver benchmarking, or decomposition-aware GPI gets the same savings.
- **Old-task retention:** Earlier contexts using the same repair and tasks falsely grouped by superficial token similarity.
- **Risk / likely tie:** A capability may behave differently across contexts; discount shared evidence when residuals vary by family.

### AL4-26 · Carry forward contracts through two updates with explicit uncertainty debt
- **Primitive** (the amount of unverified change a retained label has accumulated determines its next recheck).
- **Mechanism:** Keep the last independently verified fork margin and conservatively accumulate change bounds from consecutive solver updates. Reopen a fork once the sum can cross the original margin, even if each individual update looked harmless. Reset only after fresh clean verification.
- **Nearest prior / gap:** Incremental invalidation and trust-region bounds; compare against a rolling policy distance rule and an interval updated from the original checkpoint.
- **Cheapest first test:** Compose two benign repair upgrades whose small separate effects produce a sign flip together. **Kill** if periodic refresh, generic cumulative drift, or iterative DPO matches stale-sign error and verifier usage.
- **Old-task retention:** Old stable forks across both changes and previously revalidated forks where the original preference remained valid.
- **Risk / likely tie:** Summed bounds can be loose; measure useful skip rate rather than claiming conservative bounds are always economical.

### AL4-27 · Choose the one new finisher that can resolve the most disputed forks
- **Improvement** (active panel selection using existing contract uncertainties).
- **Mechanism:** For forks whose signs differ across the current panel, pick a new affordable finisher predicted to separate two remaining explanations, such as wrong early choice versus missing downstream repair. Compare with adding a diverse or highest-return policy instead.
- **Nearest prior / gap:** Active experimental design and GPI policy panel expansion; improve panel information without calling the policy set itself a new primitive.
- **Cheapest first test:** Three candidate finishers and two competing errors in a finite symbolic task. **Kill** if random or diversity-based panel growth resolves the same disputes at equal verification cost.
- **Old-task retention:** Existing writes on stable forks after the panel grows and legitimate unresolved cases left unwritten.
- **Risk / likely tie:** Candidate-policy predictions can fail after shift; reserve sampling for falsifying the proposed separation.

### AL4-28 · Withdraw a preference without deleting the fork's competing evidence
- **Primitive** (an invalidated write can lose authority while retaining both measured branches for future reuse).
- **Mechanism:** On failed revalidation stop applying the local preference. Retain the paired outcomes and the solver regimes that supported each sign. If the older regime returns, revalidate a small matched sample instead of reconstructing the choice from successful traces alone.
- **Nearest prior / gap:** Iterative DPO relabeling and AL3-25 disagreement storage; test revocation and scoped reuse against a replay system that retains both labels at equal bytes.
- **Cheapest first test:** Alternate two continuation policies with opposite verified preferences. **Kill** if ordinary versioned branch replay with iterative DPO matches correction lag and retention at equal verification and state.
- **Old-task retention:** Both solver regimes where still in service, plus legitimate cases of the habitual action.
- **Risk / likely tie:** An exact solver rollback with saved labels is trivial; test returns that retain the relevant capability with a changed implementation.

### AL4-29 · Learn that two solver changes are equivalent for one fork, not all forks
- **Primitive** (revalidation evidence can be reused across updates with the same branch-relative effect).
- **Mechanism:** Compare two solver deployments that change different absolute continuation behaviors but leave the measured *difference* between the two actions unchanged for a subset of forks. Record equivalence only for this measured regime and test it on held-out forks with corresponding branch structure.
- **Nearest prior / gap:** State abstraction and GPI; the metric is lower task-specific preference refresh cost beyond absolute value or generic policy similarity.
- **Cheapest first test:** Changes to two different finishing routines yield matched effects on symmetric but not asymmetric forks. **Kill** if GPI plus pooled intervals groups the same forks without additional wrong signs at matched cost.
- **Old-task retention:** Asymmetric forks exempt from reuse and unchanged base-task decisions.
- **Risk / likely tie:** Equal differences on the panel do not imply equivalence on new tasks; require fresh audits before using the grouping.

### AL4-30 · Charge the whole contract against strong continual baselines
- **Improvement / assay** (check whether selective verification still matters after bookkeeping and missed changes).
- **Mechanism:** Run the proposed comparison over multiple solver swaps with predeclared retention and wrong-sign budgets. Charge panel construction, footprint estimation, storing both branches, audits and clean writes. Compare matched-rollout RFT, STaR, GRPO, and matched-cost GPI, fresh VinePPO-style branches and iterative DPO.
- **Nearest prior / gap:** AL3-30 lifecycle accounting; this is the check against a complicated method that wins only by undercharging its controls.
- **Cheapest first test:** Two small task families, one local solver upgrade and one broad unanticipated change. **Kill** if the contract has no regime with fewer verifier calls at matched old-task retention, clean held-out gain and wrong-sign risk.
- **Old-task retention:** Earlier tasks with legitimate shortcut use after both upgrades, including a random sample of skipped forks.
- **Risk / likely tie:** Broad upgrades may erase most savings; report separate local and broad regimes.

## Ranked deeper questions

1. **Can a frozen counter tell an unseen learner which distinctions it has preserved before that learner spends labels (AL4-01–AL4-06, AL4-12)?** Match present correction and give BCT-style transforms, stitching and Procrustes/CCA the same paired data and gates. Start with declared contrasts, then try unlabeled task-intent pairs. If labels-to-target and bad admissions do not separate, call it a compatibility transform.
2. **Can a solver change invalidate only the fork preferences it could reverse (AL4-16–AL4-21, AL4-23)?** Start from exact change footprints and common-tail cancellation; test on a held-out upgrade and audit skipped forks. Beat GPI on the same panel and clean Step-DPO/VinePPO plus abstention at matched wrong-sign risk and coverage. Do not extrapolate finite-state guarantees to model solvers.
3. **Does admission evidence survive a second counter or a tighter interface without retraining the first map (AL4-09–AL4-15)?** Compare scope composition and targeted rescue with direct stitching or CCA plus recalibration. The useful result is fewer labels and false admissions at matched present behavior and total cost, not agreement between maps.
4. **Does first-commitment inhibition produce better verified forks, or is all the gain in the revalidation rule (AL4-22, AL4-30)?** Cross the discovery and contract variants. Use equal-sample best-of-N RFT, STaR and GRPO and clean branches with the same fork information. Require a gain from a clean restart and preservation of legitimate uses.
5. **Which reuse survives multiple solver changes and changing goals (AL4-24–AL4-29)?** Compare to iterative DPO relabeling, ordinary reward relabeling and GPI with the same information and samples. Charge all audits and measure both stale preferences and useful preferences wrongly withdrawn.
