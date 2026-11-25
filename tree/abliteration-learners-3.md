# Child: Preserve future reads; teach at the first fork

Child node (depth 2) · 30 candidate cards (AL3-01–AL3-30) · 5 ranked deeper questions · Ideas only; no experiments run

**Request (Manoj).** Deepen the two ideas kept at 3 in [PR #404](https://github.com/manojbajaj95/cl/pull/404); aim for a new primitive, not another steering variant. The edge line continues [AL2-02](./abliteration-learners-2.md#al2-02--fit-the-counter-to-a-difference-of-causal-responses), [AL2-04](./abliteration-learners-2.md#al2-04--match-the-scalar-swap-which-route-supplied-it) and [AL2-11](./abliteration-learners-2.md#al2-11--install-an-edge-counter-before-a-downstream-skill-arrives), from [#402 AL11+AL08](./root-abliteration-learners.md#al11--subtract-a-dependency-edge-not-a-feature). The fork line continues [AL2-17](./abliteration-learners-2.md#al2-17--find-the-first-branch-where-inhibition-helps) and [AL2-20](./abliteration-learners-2.md#al2-20--teach-only-the-verified-fork), from [#402 AL28](./root-abliteration-learners.md#al28--teach-a-missing-distinction-by-intervening-before-gathering-labels). Promotion without RL stays a control: the review rated it an improvement (CAA/ITI, CAST, and the known REINFORCE identity).

**Thesis.** An edit should leave behind something useful to the *next* learner. The edge primitive is a counter with a transport for future reads: cancel one source-to-sink use, and leave a small map that translates how a later learner can read that source without knowing its future labels. The fork primitive is a transferable preference witness: briefly intervene at the first premature choice to discover an alternative, then store a same-prefix action comparison with evidence about which suffix policies justify it. Both objects must pay their way under changes not disclosed when they were built.

## Is this pursuable? Short answer

- **Edge: preserve the ability to learn from a source, not just its decoded value.** Let the rank-1 counter read a source scalar and write only into the implicated sink. On unlabeled paired views of the base and edited model, fit a small map from an edited accessible view back to the relevant base source coordinates. Freeze it before revealing later tasks. A later learner may express a read in those coordinates and pull it back through the map. The map cannot restore information absent from its inputs; any advantage over a direct read must come from the restricted coordinates or the prior they impose on fitting from few labels. Compare how many labeled examples later *legitimate* consumers need at matched present shortcut error, retention, capacity, and serving cost. A decoder that reconstructs the source but doesn't reduce future supervision is not a win; an extra tap that accounts for all the gain is the raw-tap baseline.
- **Fork: separate a real preference from the sampler that found it.** Inhibit only at the first observable premature commitment; use it to nominate an action pair. With the hook off, replay both actions from the identical clean prefix under independently chosen continuation policies and verify their outcomes. Write an accepted-minus-failed preference only at that fork and only in the contexts where the clean comparison supports its sign. A suffix-sensitive result can be useful evidence not to write, rather than a universal label. No sampling edit or cache at deployment.

**Scope.** Read the updated [idea ledger](https://github.com/manojbajaj95/cl/blob/7f18166e345b658357f15e4c027a8a9f8adf367b/reviews/idea-ledger.md) and [flood triage](https://github.com/manojbajaj95/cl/blob/7f18166e345b658357f15e4c027a8a9f8adf367b/reviews/flood-triage.md): both parent directions are candidate primitives at 3, none at 4. Future-edit witnesses already appear in [#374](https://github.com/manojbajaj95/cl/pull/374); clean branching, fork tapes and reversal-based credit appear in [#51](https://github.com/manojbajaj95/cl/pull/51). The novelty bets are transport of future reads without future labels and reuse of a *measured action comparison* across continuation changes, not future-edit cost or branching by themselves. PR #24's diffuse damage result means the edge need not exist. Work on benign skills and preserve policy behavior; refusal ablation is prior art only.

**Shared conventions.** Every first test is a proposal. Start with an identifiable CPU toy, then require a small frozen model with independently confirmed shortcuts. Freeze nomination, write fitting, and retention calibration before held-out task families are revealed. For edge tests, match initial correction and old-task performance, count the tap, access map and calibration forwards, and measure labels to a preset held-out target (report failures to reach it). For forks, split pilot localization, discovery, clean validation, training and test. Count failed sampling, forced turns, clean replay, tokens and verifier calls against each arm; report equal total samples first, equal total cost separately. Give competing arms the same boundary information; hold out continuation policies or problem families as specified. Report base-task and fixed policy-sentinel retention with the active learned write, plus the card-specific slice.

## Literature check

Positioning from the review and named prior art, not a new priority search. Each card inherits its line's controls; the first test names the most diagnostic comparisons.

| Line | Already available | What a card here must add |
|---|---|---|
| Preserve a learnable source (A–B) | Arditi directional ablation, LEACE, sink-local ablation, ActAdd; source-aware ReFT/LoRA with the same tap and rank; ROME/MEMIT; [#400 HL15](https://github.com/manojbajaj95/cl/pull/400); #374 future-edit tests | Same present correction, then an independently chosen consumer. Compare a raw tap, fixed protected subspace and ordinary feature alignment or replay at matched bytes. Beat them in later supervision, not only source reconstruction. |
| Discover and teach a first fork (C–D) | Best-of-N rejection sampling fine-tuning (RFT), STaR, GRPO (and PPO if feasible), all at equal total rollouts and verifier calls; Step-DPO/VinePPO-style clean branching; branch temperature; whole-trace distillation; keep the inhibitor | Same first-commitment information and same positive-writer budget where applicable. The finished model must improve from a clean restart. Beat clean branching and a pooled branch-preference writer, not only full-rollout distillation. CAA/ITI and CAST are optional steering controls, not the proposal. |

## A · Make a counter preserve a source a later learner can use

### AL3-01 · A counter that carries a map for future reads
- **Primitive** (return a localized counter and a label-free map that later learners can reuse to translate readouts).
- **Mechanism:** Fit a source-keyed rank-1 counter to the open-versus-held path response. On separate unlabeled witnesses fit `L` such that `L z_edited` approximates source coordinates from the clean view. A future linear read `wᵀh_source` becomes `(Lᵀw)ᵀz_edited`; learn `w` only after drawing a new consumer and freeze `L` throughout.
- **Nearest prior / gap:** Feature alignment and adapter recompile transfer known features or edits; AL2-11 measures future learnability. Here the counter publishes a reusable coordinate map for unknown readers instead of naming or training those readers in advance.
- **Cheapest first test:** Cancel a planted erroneous relay, then draw unseen table-operation consumers. Cross edge counter versus sink-local correction with map versus direct read. **Kill** if raw tap plus a matched readout, ordinary feature alignment, or source-aware ReFT matches labels to target and retention at equal cost.
- **Old-task retention:** First correction and earlier legitimate uses at both endpoints after installing the new readout.
- **Risk / likely tie:** If there is a free unchanged tap, or alignment is an exact inverse by construction, the object adds no value. Test a restricted live view that still preserves information.

### AL3-02 · Reserve the observable source, not a blind span
- **Primitive** (learnability is defined against an explicitly available future input interface).
- **Mechanism:** Track which source distinctions are inferable from representations a later consumer can actually access. Constrain a counter to preserve those distinctions in the live interface, not all variation at a hidden layer. Draw future tasks from a broad declared family of distinctions rather than from a list of labels.
- **Nearest prior / gap:** AlphaEdit-style protected subspaces and #374 future-write checks protect fixed observations or previously scoped edits. This proposal budgets preservation by access for unknown consumers in a family.
- **Cheapest first test:** Choose between two equivalent current counters, only one of which leaves informative live coordinates. **Kill** if random reserved rank or raw feature preservation gives equally good worst-family learning curves.
- **Old-task retention:** Noninterfering tasks that exploit the preserved interface and old tasks outside the declared family.
- **Risk / likely tie:** The family can encode the held-out task if stated too narrowly; draw independent consumers after counter fitting.

### AL3-03 · Measure tuition paid after an initially indistinguishable repair
- **Improvement / assay** (compare later sample cost without smuggling in a present-day accuracy advantage).
- **Mechanism:** Match interventions on shortcut error and legitimate-use scores before teaching any new task. Draw a hidden set of future consumers that differ in source dependence, then estimate labels-to-target curves including noncompletion.
- **Nearest prior / gap:** AL2-11 and #144 future-edit cost; add paired counter and baseline operating points so a later win cannot be explained by a better starting error rate.
- **Cheapest first test:** Seed two held-out table transformations using the source and two matched transformations using an independent signal. **Kill** if equally good sink-local ablation shows the same label-cost curve on source-dependent tasks.
- **Old-task retention:** Original correction at every point on the later learning curve.
- **Risk / likely tie:** Poor overlap in present-day performance can make matching uninformative; report feasible ranges rather than extrapolating.

### AL3-04 · Spend one extra coordinate to keep the source accessible
- **Primitive** (an inhibition can relocate a lost source component into a separately readable channel).
- **Mechanism:** If a counter removes the only live copy of a source component from a sink's downstream interface, route one calibrated scalar into a narrow read-only slot not used by the current decision. Size the slot without future labels and teach later consumers to read from it.
- **Nearest prior / gap:** Side-channel taps, lateral adapters and protected subspaces; the bar is a cheaper, task-blind relocation at the same interface budget, not writing a source copy into memory.
- **Cheapest first test:** Compare one relocated scalar, one raw tap and one randomly chosen retained coordinate under the same access constraints. **Kill** if raw tap or residual adapter plus a fixed saved projection matches future sample cost and serving cost.
- **Old-task retention:** Earlier consumers of both the original source and the site holding the new slot.
- **Risk / likely tie:** A slot reachable by the old sink is not isolated; probe its actual behavior rather than asserting architectural exclusivity.

### AL3-05 · Preserve low-variance contrasts that later learners cannot infer
- **Primitive** (reserve learnability of distinguishable source pairs, not average reconstructability).
- **Mechanism:** Select unlabeled source pairs with reliably different behavior under small benign interventions, including small-variance components. Fit a recoverable live view against their separation; later tasks need not reuse the witness examples or known labels.
- **Nearest prior / gap:** Metric learning and functional-feature preservation; treat contrast witnesses as a reservation for future readers, then compare against reconstruction of the same rank.
- **Cheapest first test:** Mix high-variance distractors with one reliable low-variance table cue. **Kill** if ordinary supervised-null-space protection, PCA plus matched raw tap, or general feature alignment equally reduces later evidence needs.
- **Old-task retention:** Legitimate high-variance consumers as well as the original edited task.
- **Risk / likely tie:** A low-variance cue can be unlearnable under realistic noise; split-half reliability gates any claim.

### AL3-06 · Reconstruct what the source changes, not what the source looks like
- **Primitive** (the read map preserves a source intervention response rather than activation reconstruction error).
- **Mechanism:** Fit a small transport using the difference in accessible activations before and after benign source swaps; compare against a map trained on absolute states. Teach a future reader on different source values and independently drawn contexts.
- **Nearest prior / gap:** Causal abstraction and feature regression; isolate whether training on paired source changes preserves usable signal at equal cost when nuisance dominates absolute states.
- **Cheapest first test:** Draw new legitimate table consumers under a changed distractor distribution. **Kill** if absolute alignment or source-aware LoRA matches the response map on labels-to-target under shift.
- **Old-task retention:** Stable environments where the original nuisance signal remains a useful field.
- **Risk / likely tie:** Counterfactual swaps may be unnatural; include genuine matched inputs and deliberately irrelevant swaps.

### AL3-07 · Blind the current writer to tomorrow's target labels
- **Improvement / assay** (distinguish preserved learnability from pretraining the next task).
- **Mechanism:** Split task generation between the writer, who sees unlabeled views only, and an independent chooser who selects future valid source consumers after the writer is frozen. Include unseen mixtures of benign operations, not merely new examples of old operations.
- **Nearest prior / gap:** Held-out-task evaluation and #374 future-edit checking; designed to make the transport claim falsifiable without revealing the future head.
- **Cheapest first test:** Compare the blind map against a deliberately leaked label-aware ceiling and a raw-tap floor. **Kill** the general preservation claim if savings survive only for future targets predictable from calibration.
- **Old-task retention:** Old source-dependent and independent tasks chosen before the split.
- **Risk / likely tie:** If every sampled target is equivalent up to renaming, task separation is superficial.

### AL3-08 · Bound how much later learning depends on one surviving view
- **Improvement / assay** (identify which interface carries the claimed benefit).
- **Mechanism:** Evaluate later learning with the edited live view, its calibrated map, and an oracle clean source. Remove one permitted channel at a time before training, and repeat with the removed channel replaced by noise at the same scale.
- **Nearest prior / gap:** AL2-03 tap accounting and ordinary ablation; identify dependence of later *sample cost* rather than whether a readout is already encoded.
- **Cheapest first test:** Use one hidden and one visible consumer of the edited source. **Kill** the portable-map claim if the benefit is entirely an uncharged clean state read or persists with the relevant view randomized.
- **Old-task retention:** Existing tasks with the intended production interface and the map absent or present, as applicable.
- **Risk / likely tie:** Removing a channel may break the model for unrelated reasons; use an additive matched-capacity read path rather than masking base state.

## B · Carry the learnability guarantee forward without overclaiming it

### AL3-09 · Compose maps for edits made before a skill exists
- **Primitive** (future readers can reuse a source view across more than one repair).
- **Mechanism:** After each of two counters fit a map from the newly available view to the previous view on unlabeled pairs. Compare composing the two maps, fitting a direct base-to-current bridge, and teaching directly on the final representation. Reveal the future reader only afterward.
- **Nearest prior / gap:** Feature-alignment composition and #400 adapter recompilation; the object substitutes for labeled teaching across a sequence of counters, not porting an existing trained adapter.
- **Cheapest first test:** Two independently nominated counter sites, one existing legitimate user and one later user. **Kill** if raw tap or same-byte direct realignment always matches the composition's label savings.
- **Old-task retention:** Both original fixes and legitimate users after both writes.
- **Risk / likely tie:** Linear composition can amplify errors; report stability rather than claiming exact preservation.

### AL3-10 · Keep the first skill from being inherited by the later reader
- **Primitive** (a learned read map can carry the source while excluding the earlier edited task's correction signal).
- **Mechanism:** Enforce agreement across pairs with the same source value but contrasting earlier task labels. Test whether an unseen reader can use the mapped view without learning the old shortcut scope as a proxy.
- **Nearest prior / gap:** LEACE and invariant representation learning; use the same-source contrasts to protect a future read against the original counter's side effects, not to erase the source.
- **Cheapest first test:** Teach a future consumer whose labels deliberately contradict the earlier editor's learned scope. **Kill** if task-blind alignment or same-tap ReFT matches transfer after correlation reversal.
- **Old-task retention:** The original correction under both correlations and unrelated legitimate uses.
- **Risk / likely tie:** The correction signal might legitimately reveal which source is relevant; do not enforce invariance where the source itself changes.

### AL3-11 · Revoke a bad edge write without charging a second tuition
- **Primitive** (a counter's read map can migrate a reader trained during the counter's lifetime).
- **Mechanism:** Teach a legitimate consumer on the edited representation, then revoke the old counter when a new witness shows it was mislocalized. Convert the reader through paired views if possible; compare raw restore and restore plus retraining at the same evidence budget.
- **Nearest prior / gap:** Rollback, #400 recompilation and AL2-15 attribution retraction; separate a later reader's migration from merely preserving its weights.
- **Cheapest first test:** Mislocalize one of two benign correlated table cues, train a legitimate later read, then expose the mismatch. **Kill** if replay or ordinary adapter realignment preserves both tasks at equal cost.
- **Old-task retention:** Previously learned reader plus legitimate old uses outside the revoked scope.
- **Risk / likely tie:** If the later reader always uses an unchanged upstream source, persistence is bookkeeping, not a transport result.

### AL3-12 · Repair only the missing part of the later evidence
- **Primitive** (the counter reports a missing source contrast that a later learner can target with a question).
- **Mechanism:** When the map reproduces some but not all paired source effects, retain a compact residual diagnostic. Let a future learner request labels discriminating the missing contrast, without retaining full old data.
- **Nearest prior / gap:** Active learning and future-write witnesses; target the difference between interventional source responses rather than uncertainty in the future labels alone.
- **Cheapest first test:** Retain two of three accessible source factors and vary which factor the later reader needs. **Kill** if ordinary uncertainty sampling or querying random missing features reduces labels equally.
- **Old-task retention:** Earlier cases using the missing contrast and the original corrected decision.
- **Risk / likely tie:** A residual diagnostic could become an indirect cache of future labels; constrain it to unlabeled contrast statistics.

### AL3-13 · Choose the counter that minimizes worst-reader tuition
- **Primitive** (edit selection uses a bracket on later read cost from an unlabeled family of admissible contrasts).
- **Mechanism:** Among current-equivalent counters, compare how dispersed and separable a predeclared family of source contrasts remains in each accessible view. Use this as a proxy for worst later label cost and test against actual hidden consumers, not against the proxy alone.
- **Nearest prior / gap:** Experimental design and stable embeddings; the question is whether a current repair can be ranked by future learnability better than rank headroom or present accuracy.
- **Cheapest first test:** Three equally effective counters and independent later readers at several source-noise levels. **Kill** if the contrast-based ranking predicts future tuition no better than smallest weight change or flat headroom.
- **Old-task retention:** Exclude any counter exceeding the fixed old-task damage budget before ranking.
- **Risk / likely tie:** Good conditioning does not guarantee useful causal information; test readers outside the fitting contrasts and mark scope limits.

### AL3-14 · Check that tuition management is cheaper than storing source examples
- **Improvement / assay** (accounting boundary for the edge object).
- **Mechanism:** Charge label-free paired views, map bytes, and runtime read cost against a replay baseline that stores source examples and trains future readers on demand. Compare both equal-label and equal-total-cost curves.
- **Nearest prior / gap:** #144 lifecycle cost and AL2-03 tap accounting; tests whether the future-skill benefit survives keeping a small ordinary sample bank.
- **Cheapest first test:** Vary the number of independent future consumers sharing a single correction. **Kill** if replay or direct source access dominates across the sweep at matched first-task performance.
- **Old-task retention:** Same slice and thresholds on every cost curve.
- **Risk / likely tie:** Storing outputs is enough in some benign tasks; give replay the strongest permitted representation.

### AL3-15 · Distinguish preservation from relearning the source from scratch
- **Improvement / assay** (diagnose whether the later reader uses retained evidence at all).
- **Mechanism:** After teaching later consumers under matched first-task corrections, vary access to the original source and optional input-correlated proxies separately. Compare how accuracy changes under randomized source values and under held-out proxy reversals.
- **Nearest prior / gap:** Interchange interventions, AL2-04 provenance and #374 future edits; distinguishes a cheaper path to the same causal source from learning a different route to the benchmark answer.
- **Cheapest first test:** Use table values with a learnable but spurious proxy, then reverse it. **Kill** the preservation interpretation if label savings survive removing the source only while the proxy remains.
- **Old-task retention:** Valid proxy use where it is the actual target and original legitimate source uses.
- **Risk / likely tie:** An alternative route can be useful in deployment; report it separately rather than crediting the proposed primitive.

## C · Inhibit only the first premature commitment, then verify the fork

### AL3-16 · A fork witness with a continuation contract
- **Primitive** (a preference example carries the regimes in which it is valid, not only the winning branch).
- **Mechanism:** Inhibit one first commitment for discovery. From the clean prefix force each nominated action and estimate paired verifier-score differences under a small panel of continuation policies. Store the fork, action pair, and per-policy uncertainty; permit a clean preference write only when the sign has support in the declared regime. On a compatible solver change, check the same witness with a small fresh sample rather than discovering the fork again.
- **Nearest prior / gap:** Step-DPO/VinePPO and #51 fork tapes provide branching and credit. The proposed object separates discovery from a reusable comparison conditioned on who finishes the job; test it against both clean branching and pooled robust-advantage baselines.
- **Cheapest first test:** Two-stage arithmetic tasks where one shortcut is reliably premature and another is harmful only under weak continuation. **Kill** if pooled fork labels or fresh clean branching matches held-out policy-swap accuracy and revision cost at the same rollouts and retention.
- **Old-task retention:** Contexts where the shortcut is correct and tasks whose clean downstream solver already succeeds.
- **Risk / likely tie:** A finite panel does not justify a guarantee about unseen solvers. Test a held-out solver and allow the contract to abstain outside support.

### AL3-17 · Put an interval around the first preventable choice
- **Improvement / assay** (test whether the localization is precise enough to justify a fork write).
- **Mechanism:** On a separate discovery set, compare short interventions on candidate decision windows. Locate the earliest window that exposes a verifiably better option on clean replay; test whether the immediately earlier and later windows have distinguishable effects at matched intervention strength.
- **Nearest prior / gap:** AL2-17, activation patching and #51 reversal-based credit depth; this is operational localization of an observed choice, not proof of an earliest internal thought.
- **Cheapest first test:** Benign sorting or arithmetic with two observable choices. **Kill** if nearby windows or branch-only temperature match the useful fork yield at equal samples.
- **Old-task retention:** Correct early commitment and cases with the opposite choice ordering.
- **Risk / likely tie:** Tokenization and free-form traces may obscure the choice. Start with explicit constrained action choices and verify transfer before generalizing.

### AL3-18 · Use inhibition as a proposal mechanism, not as a label
- **Improvement / assay** (close the causal gap between sampler behavior and clean action preference).
- **Mechanism:** Let the intervention nominate actions only during the first decision. Force the same two actions from the clean prefix and resample suffixes. Label the cleaner preference from verifier results alone; score when edited sampling's apparent winner reverses under clean replay.
- **Nearest prior / gap:** AL2-20 and off-policy branch evaluation; separates discovering an action from valuing it.
- **Cheapest first test:** Seed cases where an apparently successful alternative requires continuing under the edited policy. **Kill** if clean replay adds no useful correction beyond matching entropy or whole-rollout verification.
- **Old-task retention:** Clean decisions for which the edited sampler favors an unnecessary detour.
- **Risk / likely tie:** Forced actions rare under the base can leave it in unfamiliar prefixes; report support and compare cases of similar rarity.

### AL3-19 · Learn the fork only if both actions are executable cleanly
- **Primitive** (a fork witness includes a check of downstream feasibility, not merely two action labels).
- **Mechanism:** Distinguish an action with bad outcomes under adequate continuations from a valid action the clean solver cannot yet complete. Use a bounded checklist of verified suffix steps to tell those apart; defer the write when the observed difference is a missing solver skill.
- **Nearest prior / gap:** Process supervision and advantage estimation; the proposed object turns lack of suffix competence into a reason to withhold a preference and revalidate it after a solver update.
- **Cheapest first test:** One arithmetic branch is initially hard to finish but becomes viable after adding a known routine. **Kill** if Step-DPO using clean branch rollouts or a scalar success threshold handles the solver upgrade equally well at the same cost.
- **Old-task retention:** Cases where the initially harder action is necessary and remains correct.
- **Risk / likely tie:** The checklist could provide privileged strategy hints; give all arms access to the same process verifier.

### AL3-20 · Pair outcomes without pretending two rollouts share a future
- **Improvement / assay** (estimate fork effects without treating sampling noise as causal credit).
- **Mechanism:** Replay each action with multiple independent continuation draws; block comparisons by prompt and, in exact simulators, shared exogenous conditions. Compare the precision and sign stability to one accepted and one failed trace.
- **Nearest prior / gap:** Best-of-N, VinePPO, randomized blocking; this estimates whether the evidence is good enough to support a transferable witness.
- **Cheapest first test:** Simulator with noisy continuation length or stochastic distractors. **Kill** multi-draw screening if it fails to improve held-out sign stability at equal verifier calls.
- **Old-task retention:** Old decision rules exposed to the same stochastic suffixes.
- **Risk / likely tie:** Common seeds do not make free-form model continuations counterfactual twins; only pair explicitly shared environment randomness.

### AL3-21 · Write at the commitment, not a correlated token
- **Improvement / assay** (test where stored fork support should affect the clean model).
- **Mechanism:** With the same verified action pairs, train a prefix-local preference write at the nominated choice and a matched writer before or after it. Check clean forcing of the alternative and behavioral gain on unseen wording.
- **Nearest prior / gap:** Step-DPO and AL2-20; the usefulness of the first-fork location must survive a matched objective and data.
- **Cheapest first test:** A decision with two different surface realizations and the same executable effect. **Kill** if whole-trajectory RFT or equally sized neighboring writes match clean transfer and scope.
- **Old-task retention:** Same tokens used in old tasks as noncommitment text, plus correct use of the shortcut.
- **Risk / likely tie:** If constrained decoding exposes the answer-bearing token, score free execution on held-out renderings too.

### AL3-22 · Cite an action collision, not a loss of confidence
- **Primitive** (the negative part of a fork witness can name a competing legitimate intent that would be harmed by a global write).
- **Mechanism:** For visually similar prefixes test the same two actions under opposite valid task goals. Keep both verified comparisons and use them to scope the write to the goal where premature commitment is harmful.
- **Nearest prior / gap:** Contrastive preference conditioning and AL2-28/CAST; the added operand is an action-level protective counterfactual validated under clean suffix policies, not a steering trigger alone.
- **Cheapest first test:** Two table requests share a prefix but differ on whether approximation is permitted. **Kill** if task-gated Step-DPO or a simple goal router matches drift and opposite-goal retention.
- **Old-task retention:** Valid approximate solutions and unrelated exact tasks.
- **Risk / likely tie:** The goal label may fully resolve the conflict, making the witness little more than ordinary labeled data.

### AL3-23 · Re-evaluate the committed choice when verifier preferences change
- **Primitive** (reuse a recorded clean comparison with a different scoring rule without conflating it with the old label).
- **Mechanism:** Keep small normalized outcome summaries for both clean branches. When a benign verifier changes (e.g. valid approximations get a tighter tolerance), rescore both, check what remains within support, and revise only the original action comparison.
- **Nearest prior / gap:** Off-policy reward relabeling and #51 fork tapes; the claim is lower revision cost from outcome summaries at the first fork, not novelty of scoring old trajectories again.
- **Cheapest first test:** A numeric tolerance change with stable action and continuation semantics. **Kill** if raw rollout storage plus RFT or clean fork recollection matches cost at equal bytes.
- **Old-task retention:** Old objectives that are still legitimate in explicitly scoped requests.
- **Risk / likely tie:** A new verifier may require information not captured by summaries; do not infer unobserved outcomes from old acceptance.

## D · Make verified fork evidence reusable after the solver changes

### AL3-24 · Retest only the suffix regime that could reverse the comparison
- **Primitive** (partial revalidation is driven by the witness's measured sign instability).
- **Mechanism:** After a benign solver update, reserve a small validation quota for forks with close or differing verified advantages in predecessor policies. Recheck a sample of nominally stable forks as a falsification control. Reuse or withdraw the clean fork labels only within accepted scopes.
- **Nearest prior / gap:** Off-policy reuse and drift checks; compare using action-pair sensitivity to suffix policies against using generic policy distance or reward uncertainty.
- **Cheapest first test:** Swap between two clean arithmetic continuation strategies and hold out a third. **Kill** if uniform revalidation or per-fork uncertainty without policy conditioning matches stale-sign error at equal verifier calls.
- **Old-task retention:** Stable and withdrawn forks, including old tasks where the shortcut is valid.
- **Risk / likely tie:** Policy changes can reverse stable-looking preferences abruptly; require independent audit sampling rather than asserting safety from past agreement.

### AL3-25 · Keep counterfactual disagreement without teaching either branch
- **Primitive** (an unresolved fork witness is reusable evidence about what must be verified next).
- **Mechanism:** When acceptable continuation policies give opposing action preferences, keep the negative and positive comparisons separately and decline the write. When a new solver or clarified task goal arrives, validate only the unresolved contrast before making a clean local update.
- **Nearest prior / gap:** AL31 abstention, robust preferences, #51 fork tapes; retaining the distinct continuation-dependent measurements must help more than storing “uncertain” or a scalar mean.
- **Cheapest first test:** Mix stable forks, solvable ambiguities and genuinely unresolvable tasks. **Kill** if a pooled interval with a standard uncertainty-based query policy resolves the same forks at lower cost and equal retention.
- **Old-task retention:** Both previously acceptable branches when permitted by the original goals.
- **Risk / likely tie:** Contextual task relabeling could do the work; give the controls the same goal information.

### AL3-26 · Transfer the verified fork by action effect, not answer spelling
- **Primitive** (a clean comparison can be rebound to new encodings of the same two executable choices).
- **Mechanism:** Record a small observable effect signature for the forced actions, such as which table columns they commit to and whether the commitment is reversible. Use it to find homologous choices under a changed encoding and verify the sign on new clean replays.
- **Nearest prior / gap:** #51 action transport and AL26 relation edits; the proposed transfer is the whole comparison with its continuation scope, not a chosen action or a policy vector.
- **Cheapest first test:** Change the surface encoding and choice order while preserving executable effects. **Kill** if a clean normalized branch-preference baseline transfers at the same number of new verifier calls.
- **Old-task retention:** Old encodings and cases where similar spelling denotes a different action.
- **Risk / likely tie:** A hand-written action schema may solve transfer outright. Give it to a symbolic preference table control too.

### AL3-27 · Separate a robust fork from an interchangeable decomposition
- **Improvement / assay** (check whether local teaching is justified when several paths achieve the same goal).
- **Mechanism:** Include cases where both first actions can lead to equally correct solutions under adequate continuation. The witness should decline a directional vote there, even if a particular sampler prefers one branch, unless the task explicitly values cost.
- **Nearest prior / gap:** Best-of-N path selection and verifier tie handling; stress-test the witness's ability to reject false preferences from differing reachability.
- **Cheapest first test:** Two equivalent exact arithmetic decompositions plus one genuine early mistake. **Kill** if the proposed witness makes just as many unjustified writes as clean Step-DPO or pooled verifier labels at matched useful corrections.
- **Old-task retention:** Diversity among valid strategies when the user's task does not prefer one.
- **Risk / likely tie:** Equal verifier reward does not imply equal cost; report efficiency separately instead of injecting it into the label post hoc.

### AL3-28 · Keep a later correction from rewriting credit for the first choice
- **Primitive** (a verified fork records whether later recoverability, rather than the early action, creates the preference).
- **Mechanism:** Pair clean branch outcomes under both a competent repair policy and a policy that cannot revise earlier commitments. For an explicitly irreversible task, teach only mistakes robust to the permitted recovery; in reversible tasks tag the disagreement instead of treating success after repair as evidence the first choice was sound.
- **Nearest prior / gap:** #51 reversal-based credit, Step-DPO and hindsight credit assignment; use recovery sensitivity to decide whether to write at the first fork after a downstream repair is added.
- **Cheapest first test:** A symbolic planner with and without a verified legal undo. **Kill** if clean advantage estimation using the actual recovery policy matches later transfer and revision cost.
- **Old-task retention:** Tasks where trying an early option and legally undoing it is valid.
- **Risk / likely tie:** A recovery-enabled policy may alter the task budget; equalize allowed actions and score within matched regimes.

### AL3-29 · Teach the smallest policy change the comparison supports
- **Improvement** (control the generalization scope of a local preference writer).
- **Mechanism:** Train a narrow writer using only verified fork pairs. Compare direct preference labels, uncertainty-weighted labels and a reversible small-dose writer without changing the sampling evidence. Test held-out prefixes that differ in a single legitimate task qualifier.
- **Nearest prior / gap:** Step-DPO, conservative policy updates and conditional steering; constrains generalization from the proposed witness rather than asserting a new update family.
- **Cheapest first test:** One unambiguous and one scope-sensitive arithmetic choice. **Kill** if weighting or dose control yields no better retention/gain frontier than a tuned matched-rank preference writer.
- **Old-task retention:** The same action pair in old contexts with an opposite valid preference.
- **Risk / likely tie:** A smaller update can appear safer because it does less; compare at matched gain on corrected contexts.

### AL3-30 · Price the fork witness after multiple legitimate solver changes
- **Improvement / assay** (check whether reuse actually beats regenerating fresh rollouts).
- **Mechanism:** Measure full cost of discovery, forcing, verification, clean writing, storage, and revalidation over multiple shifts in a benign continuation solver. Compare against fresh equal-sample best-of-N RFT, STaR, GRPO and a clean fork collector. Score total cost only alongside comparable current gain and old-task retention.
- **Nearest prior / gap:** #144 edit lifecycle accounting, #51 branch rolls and #404 replay costs; the test sets a reuse threshold for a fork witness, not a claim that accounting is a primitive.
- **Cheapest first test:** Three controlled solver swaps on two small task families. **Kill** the reuse claim if no regime beats fresh clean branching or best-of-N under equal retained accuracy.
- **Old-task retention:** All old solver/task scopes after each change, including valid shortcut uses.
- **Risk / likely tie:** Verification overhead may dominate at small task count; report where a witness is not worth keeping.

## Ranked deeper questions

1. **Can a counter leave a reusable map for readers trained after the edit, without seeing their labels (AL3-01, AL3-03, AL3-06–AL3-08)?** Draw the later consumers after fitting; match the first correction. The bar is later labels-to-target and retention above a raw tap, equal-rank source-aware ReFT/LoRA, sink-local ablation and ordinary feature alignment. Reconstruction alone is not evidence.
2. **Can a verified first-fork preference survive changing who finishes the rollout (AL3-16, AL3-18, AL3-24–AL3-25)?** Use inhibition only to discover actions, then validate the pair on a clean restart. Compare the continuation-scoped witness against pooled clean Step-DPO/VinePPO-style forks and fresh branching at equal cost; test reversal detection under a held-out solver.
3. **Does first-commitment inhibition contribute unique teaching evidence after paying for both clean branches (AL3-17–AL3-21, AL3-30)?** Compare to equal-sample best-of-N RFT, STaR, GRPO and local temperature, with the same localization information. If clean alternatives match final held-out gain and retention, do not credit the sampling intervention.
4. **Do future reads remain cheap through a second counter or a retraction (AL3-09, AL3-11–AL3-15)?** Fit both maps before drawing the reader. Compare composition and reader migration to direct alignment, replay and #400-style recompilation. If a raw tap accounts for all of the benefit, the transport adds nothing.
5. **Can the witness separate a wrong commitment from a later repair, changed goal or equally valid decomposition (AL3-19, AL3-22–AL3-28)?** Cross executable choices with continuation competence and valid user goals; a useful object withdraws weak labels without sacrificing stable ones. Beat a pooled interval plus ordinary abstention at equal verification cost.
