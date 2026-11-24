# Fossil beliefs: inherit the procedure, not its old premises

**Status:** research ideas only; no new experiments run. **Parent:** [Cross-generation inheritance](cross-generation-inheritance.md) ([PR #130](https://github.com/manojbajaj95/cl/pull/130)). That node's first ranked question is this node's scope: how to transfer a skill from an old fine-tune without undoing the successor's factual corrections. This is not edit transport, forecasting which lessons go obsolete, or a general model-merging proposal.

## What the gate leaves unsolved

Let `B0` be the ancestor base, `F0` its fine-tune, and `B1` the successor before inheritance. `Q` is the skill region and `R` the region where the world changed from `W0` to `W1`. A skill can be world-independent, depend on a current fact (keep the rule, change the answer), or deliberately override a default (an owner policy, not a new fact). For example, a planner should keep its route-ranking rule when a bridge closes, call the current world for open routes, and still honor a fleet's explicit vehicle restriction. An archived question about the bridge before closure is a separate task, not an error to erase.

In the parent's [eight-seed NumPy toy](probes/cross_generation_probe.py), plain KD gives **84.3% old-world answers on `R ∖ Q`** (0.6 pp s.e.), versus 3.0% for `B1`. This is a rate over the whole slice, not the conditional probability that an individual answer correct in `B1` flipped. On that slice plain KD keeps 3.2% correct `W1` answers; other errors need not be fossils. This rate is a synthetic result, not an estimate for real successors. The **baseline** is the parent's disagreement-gated KD: train `B1` against `F0`'s soft target only when total variation between `F0` and `B0` exceeds 0.5; otherwise use the frozen `B1` target. It attains **57.8% skill / 75.9% corrections kept / 12.2% fossils / 84.8% untouched old-task accuracy**. Plain KD has 73.5% skill; no inheritance has 95.2% untouched old-task accuracy. Neither pure imitation nor stronger indiscriminate anchoring solves the trade-off.

The gate asks *where the fine-tune changed predictions*, not *which premise made an action appropriate*. Outputs alone need not identify that difference: when two skills give identical answers under `W0` but different answers under `W1`, observing `F0` only under `W0` cannot distinguish them. The ideas below test which extra observations, representations or update operations are worth paying for.

## Prior-art and ledger screen

- [TuneShift-KD](https://www.alphaxiv.org/abs/2603.24518) uses base/fine-tune perplexity gaps and iterative synthetic examples to transfer specialized knowledge. Selecting ancestor-disagreement examples or generating more of them is a control, not a contribution.
- [Proxy-tuning](https://www.alphaxiv.org/abs/2401.08565) adds the tuned-minus-untuned output difference at decoding time. The parent's failed delta KD distills a related raw additive target; it does not refute decoding-time proxy-tuning. [Fine-tuning transfer](https://www.alphaxiv.org/abs/2503.20110) and [Re-Basin of Task Vectors](https://www.alphaxiv.org/abs/2505.22697) transfer or align parameter deltas. Use these where applicable; a better-aligned delta is not evidence of separating skill from belief.
- [Propagating Knowledge Updates Through Distillation](https://www.alphaxiv.org/abs/2306.09306) distills a fact supplied in context into its implications. [DistillMIKE](https://aclanthology.org/2024.findings-acl.455/) already combines edited and unedited teachers on in-scope and out-of-scope inputs; [MixSD](https://huggingface.co/papers/2605.16865) mixes contextual and native self-distillation to balance injection and retention. A `W1`-conditioned ancestor, direct correction replay, and two-teacher patching are controls whenever the method gets the same correction evidence. The target here includes the specialized procedure on new premises, not just propagation of a new fact.
- [Causal distillation (DIITO)](https://aclanthology.org/2022.naacl-main.318/) already teaches a student to match teacher interchange interventions. Use it as a control when sharing intervention access. The question here is which interventions one should **not** copy when model generations know different things.
- Start from the [idea ledger](https://github.com/manojbajaj95/cl/blob/ab56d845b9adf2ac9f6dbba4a0ce11379a038056/reviews/idea-ledger.md) ([PR #6](https://github.com/manojbajaj95/cl/pull/6)): no generator-identity claims (self-quizzing tied), no new prior-art claim for counterfactual-context training (KAFT), no margin-only routing claims (MX2), no obsolescence forecast from unreliable labels (Fleet Q2/Q3), and no claimed wins by construction (save/restore, quartet reweighting, or frozen-backbone guarantees). [Edit transfer (PR #76)](https://github.com/manojbajaj95/cl/pull/76) already covers transmitting evidence instead of conclusions; that is a comparator, not the claimed novelty here. This quick alphaXiv/HF screen only sets controls, not priority.

## First-test contract (CPU only)

- Start with a finite simulator or tiny NumPy learner and paired worlds. Hold out combinations and world shifts, not just random examples. Use `Q ∩ R` tasks with a **separately scored world query** and a skill decision that consumes it. Keep world truth and skill labels in the evaluator only; when a card assumes extra artifacts, a trusted current lookup or explicit user policy, expose the same inputs to its controls and account for their cost. Include cases where `B1` is confidently wrong, so disagreement with the ancestor is not itself a correction. For a stochastic test use at least eight paired seeds, report paired uncertainty; replicate a surprise at ten or more before explaining it.
- Compare against the fixed parent gate, a validation-tuned gate/strength sweep, plain KD, no inheritance, and the card's closest control, matching queries, transferred bytes and update/inference budgets where relevant. Include matched-temperature and replay controls when confidence or replay can explain a win. For skill score, report independent, conditional and explicit-override slices; for corrections and fossils report `R ∖ Q` and companion world queries inside `Q ∩ R`. Include unrelated old-task accuracy on `¬(Q ∪ R)`, its absolute drop from `B1`, and retention of any earlier skills present in the setup. Count abstentions/timeouts separately and as failures at fixed coverage unless a costed fallback is used.
- Advance a candidate only if it improves skill at matched fossil rate or reduces fossils at matched skill, with corrections kept non-inferior and old-task accuracy no more than 2 pp below the gate. Always show the gap to `B1`; tying the gate on old tasks does not mean old competence is preserved. Compare Pareto frontiers, not just favorable single thresholds. The first tests below name additional falsifiers and old-task slices.

## Research ideas (22 cards)

### A. Find out what is identifiable before copying anything

#### 1. Minimal separating world queries

- **Mechanism:** Maintain a small version space of skill rules consistent with ancestor observations. Choose the cheapest premise intervention whose answer would distinguish rules that prescribe different actions under `W1`; stop querying when remaining ambiguity cannot change the deployment action.
- **Novelty bet — primitive candidate:** The unit of active transfer is an intervention that separates a specific pair of *deployment-relevant* hypotheses, not a likely skill prompt (TuneShift-KD) or a generic disagreement audit (parent card 22).
- **Cheapest first test:** Enumerate eight routing rules, including “take the shortest open path” and “always choose bridge A when reachable,” in worlds where their historical choices tie. Compare randomized premise swaps and entropy-based active queries at equal query count; reject if fewer ambiguous actions are not resolved.
- **Old-task retention check:** Re-score paths on unchanged graphs, including rare equal-cost tie cases, and ordinary map lookups outside routing.

#### 2. Disposable negative-control ancestors

- **Mechanism:** Build a sham fine-tune from `B0` with the same optimization and label frequencies but shuffled skill assignments. Use the direction of its output shifts, validated on a separate panel, as a negative control for changes caused by the recipe rather than by the skill; remove only supported nuisance directions.
- **Novelty bet — improvement:** Unlike subtracting the untuned base as in proxy-tuning, this tests whether the *training operation itself* generates anti-transfer. A temperature correction is the obvious tying control.
- **Cheapest first test:** Use a six-class linear model and vary anchor temperature and class imbalance independently. Compare a single sham panel with temperature- and bias-calibrated delta KD; stop if the sham only estimates temperature and class bias.
- **Old-task retention check:** Evaluate unchanged examples separately for prevalent and rare classes; do not accept recovery that merely changes the class prior.

#### 3. Queries for the rule, not the answer

- **Mechanism:** Compare premise overrides that should affect one sub-decision with placebo overrides of irrelevant fields. Transfer a sparse input-to-action dependency map only where the two interventions produce distinguishable response patterns.
- **Novelty bet — primitive candidate:** The target is a map of which variables may influence which decisions, not the responses to a set of KAFT-style counterfactual prompts or DIITO's full intervention dynamics.
- **Cheapest first test:** In a dispatch table, switch both bridge status and an irrelevant depot nickname. Test a held-out relevant status and nickname against equal-query contextual KD, including a control given the same changed outputs but not the paired contrasts.
- **Old-task retention check:** Test old depot-name retrieval and route ranking separately; suppressing a name dependency in ranking must not erase the name elsewhere.

#### 4. Clarification as part of the inherited skill

- **Mechanism:** Where two observationally equivalent rules differ under `W1`, emit the *one policy question* that distinguishes them (e.g. “is this vehicle restriction contractual or historical?”). Until answered, choose only from actions both rules permit; reuse the answer for all affected cases.
- **Novelty bet — primitive candidate:** The purchased object is one policy bit resolving a whole class of cases, not a factual edit, a confidence threshold or a replay label.
- **Cheapest first test:** In a table of ambiguous routing policies, assign one answer to each ambiguity class. Compare one clarification with one labeled trajectory or selective KD at equal human-response and abstention costs.
- **Old-task retention check:** Track unchanged route success and unnecessary clarification on legacy cases where all candidate rules already agree.

#### 5. Donor evidence that survives an unknown correction

- **Mechanism:** Find a minimal *set of premises* sufficient for the donor's choice by deleting premises and requiring the donor to propose an alternative. Transfer the set and the action together; when a premise fails, recompute only the implicated branch rather than discarding the entire lesson.
- **Novelty bet — primitive candidate:** The artifact includes a repairable dependency between a choice and its premises. Evidence-only transfer (PR #76) and rewriting the precondition after failure (ledger kill) are controls with the same evidence.
- **Cheapest first test:** Exhaustively ablate premises in two-hop scheduling rules with redundant sufficient premises. Compare premise-set repair with full recomputation or an instruction rewrite under equal lookup budget; require held-out compound corrections.
- **Old-task retention check:** Keep success on the unchanged scheduling branch, including cases supported by a different sufficient premise set.

### B. Change the interface between skill and belief

#### 6. Fact slots with expiring bindings

- **Mechanism:** Transfer a controller whose world inputs are typed, successor-resolved slots. Bindings record which source/version resolved a slot and are invalidated on a version change; the controller cannot cache a bare ancestral value across versions.
- **Novelty bet — primitive candidate:** Parent lore already proposes reusable programs. This adds a binding lifetime and explicitly tests whether invalidation of only affected slots buys reuse over recomputing everything.
- **Cheapest first test:** In a stateful timetable, change one of three fields between requests. Compare the slot artifact with fresh retrieval on every request and with a cache cleared on any update, matching lookup budgets. Require correct behavior under delayed invalidation too.
- **Old-task retention check:** Preserve unchanged field queries and unchanged routes under the same cache budget; count needless invalidations that cause missed deadlines.

#### 7. Role-equivariant skill operators

- **Mechanism:** Learn the action operator in interchangeable roles (“available source,” “overflow destination”), not entity IDs. Query matched role permutations and enforce that the action permutes with the roles. Bind roles using the successor's state estimator at use time.
- **Novelty bet — primitive candidate:** Matching outputs under rephrasing is not role equivariance. Unlike gate-based KD, this can carry the *same* policy through arbitrary reassignment of the old and new entities to the roles.
- **Cheapest first test:** Use a tiny inventory game with unseen permutations and entities occupying multiple roles. Compare canonicalized KD and permutation augmentation with the same examples; drop if either ties.
- **Old-task retention check:** Probe unchanged role routines and literal identity lookups so an aliasing error cannot masquerade as useful invariance.

#### 8. Transfer an ordering with successor-side feasibility

- **Mechanism:** Transfer donor pairwise action preferences only conditional on candidates being jointly feasible. Ask the successor to recompute feasibility, then use the donor ordering to select among valid actions.
- **Novelty bet — primitive candidate:** Unlike the parent's ordinal *answer flips*, the transferable object is a choice ordering over alternatives, and the feasibility boundary is recomputed before the ordering is applied.
- **Cheapest first test:** In a four-action allocator, elicit donor preferences with candidate menus, then substitute new capacity limits. Compare final-answer KD plus a legality mask and a preference learner given the same menus but ignoring jointly feasible comparisons.
- **Old-task retention check:** Test legacy menus and tasks that ask for capacity rather than a decision; score tie-breaking and rare formerly feasible choices.

#### 9. Refuse premise substitution across scopes

- **Mechanism:** Attach authority and scope types to inputs: verified world observation, user instruction, and fictional assumption. Bind facts only inside their scope, and require an explicit override for policy actions. A simulated premise cannot fill a factual slot.
- **Novelty bet — primitive candidate:** The bet is on *typed substitution across episodes*, not generic skepticism or stronger context steering. A scope token and direct scoped KD are the tying controls.
- **Cheapest first test:** Route the same instruction through real, hypothetical and user-policy modes, then interleave modes with conflicting facts. Match tokens against tagged KD and a hard three-way router with equal parameters.
- **Old-task retention check:** Retain old hypothetical reasoning and ordinary dispatch for both modes; preventing fossils by ignoring all hypotheticals fails.

#### 10. Inherit a policy for spending world queries

- **Mechanism:** Transfer a planner's estimate of which unresolved premise could change its next action, but make the successor spend an explicit lookup budget only on those premises. Recalculate the priority after every lookup using successor values.
- **Novelty bet — primitive candidate:** This transfers an adaptive *order of evidence acquisition*, not the parent's fixed developmental order or an uncertainty-only retrieval trigger.
- **Cheapest first test:** In small graphs with correlated closures and a one-lookup budget, compare to lookup-by-uncertainty, full donor KD with the same budget, and a successor-only value-of-information heuristic. Require a win on unseen correlation structures.
- **Old-task retention check:** Score old routes at the same budget and unchanged low-uncertainty requests for which looking anything up is wasteful.

### C. Train the interaction, not just the target

#### 11. Noncommuting correction and inheritance

- **Mechanism:** On shadow students, measure the discrepancy between “inherit then correct” and “correct then inherit” on correction probes. Use that order effect to select or scale the inheritance update applied to the real student; preserve authorized skill changes even if order-sensitive on the skill query.
- **Novelty bet — improvement:** Tests whether actual update ordering diagnoses resurrection beyond gradient cosine or static quartet reweighting. Compare both stacked controls and ordinary corrected-target KD.
- **Cheapest first test:** Use a tiny nonlinear classifier with two correction updates. Fit the scale on one correction, test on another; compare equal-step gradient accumulation, gradient projection and correction replay. Reject if order measurements do not improve the held-out frontier.
- **Old-task retention check:** Measure unchanged accuracy after each update and final performance on a previously inherited skill; no transient catastrophic drop hidden by the final score.

#### 12. Project against a distribution of future corrections

- **Mechanism:** Estimate a low-rank span of gradients from simulated plausible corrections, including conditional consequences, and price inheritance directions by their damage to those gradients. Fit the span without seeing deployment corrections.
- **Novelty bet — improvement:** OGD/GEM and certified retention already cover protection against known tasks. The test is whether simulated *future* correction directions protect edits not yet made, beyond ordinary old-task protection.
- **Cheapest first test:** Sample low-rank family shifts and rotate a held-out correction direction. Compare norm-matched random, old-task OGD, and replay-plus-OGD controls at equal update allowance; include an unrelated shift to exhibit the expected failure.
- **Old-task retention check:** Report stable-label tasks and prior custom skills across the learning curve; protection that merely prevents parameter movement will show up as no skill gain.

#### 13. Distill marginals, not a fabricated joint answer

- **Mechanism:** If old and current world facts are uncertain, supervise the successor's fact marginal from its own calibrated beliefs and its action conditional from donor counterfactuals. Marginalize over the successor's probabilities to get the action distribution instead of inheriting a joint distribution with the ancestor's prior.
- **Novelty bet — improvement:** Unlike proxy-tuning or MixSD token mixing, this enforces a specific conditional/marginal split. A small factorized action head trained by ordinary KD may tie; that is the control.
- **Cheapest first test:** Use two noisy binary facts and actions whose optimal choice changes with the probability, not just with the modal fact. Compare joint KD from a `W1`-conditioned donor and argmax grounding at equal sample count.
- **Old-task retention check:** Recheck old world calibration and old decisions under uncertainty, not just top-1 score.

#### 14. Worst-case grounding when facts are correlated

- **Mechanism:** If only marginal fact beliefs are available, construct the set of joint distributions consistent with those marginals and choose the inherited action with lowest worst-case regret. Let the successor narrow the set if it has evidence of the dependence.
- **Novelty bet — primitive candidate:** The ambiguity set describes *which beliefs the successor is justified in combining*, not which skill labels are trusted. This is robust decision theory applied at the donor/successor interface; novelty hinges on beating robust planning with no donor and independent grounding with the donor.
- **Cheapest first test:** A two-edge route with identically calibrated closure marginals but shifting dependence. Compare independent marginalization, robust planning from scratch, and correction replay; charge conservative detours in the objective.
- **Old-task retention check:** Score travel cost and success on unchanged correlated and independent route sets; always detouring is a retention failure.

#### 15. Distill successor-grounded credit on trajectories

- **Mechanism:** Replay a donor trajectory in the current simulator, replace an invalid step with a feasible alternative, and teach state-conditional preferences only at steps whose downstream utility preserves the intended goal. Distill negative credit for decisions whose advantage disappears after grounding.
- **Novelty bet — primitive candidate:** The transfer object is grounded *local credit*, not the new-world trajectory itself (on-policy KD or hindsight relabelling). Test whether it carries reusable decisions to new states where repaired trajectories are absent.
- **Cheapest first test:** In a four-step grid planner, replay a donor from routes that became invalid and evaluate on unseen starts. Compare equal-step hybrid rollouts, SFT on repaired paths and reward-model re-optimization.
- **Old-task retention check:** Re-evaluate unchanged routes and earlier navigation skills with different goals; penalize extra steps as well as failure.

#### 16. Paired students reveal learning-induced fossil leakage

- **Mechanism:** Train one disposable student on a candidate inheritance batch and another on matched old-task replay. Use disagreements on held-out, newly constructed world-question paraphrases to select a *repair batch for the next update*, not to relabel the original donor examples.
- **Novelty bet — improvement:** In contrast to the parent triangulation card, the diagnostic measures collateral spillover *after the learner applied* a batch, including on inputs neither teacher selected. Direct audit-and-replay and matched-compute leave-one-out are required controls.
- **Cheapest first test:** Use one KD minibatch with correlated skill/world features, construct fresh probe contexts from the simulator, and compare paired-student repair to direct correction replay plus gate at equal total steps and probes.
- **Old-task retention check:** Track paraphrases of unaffected old answers and unrelated old tasks on a third held-out set never used to pick repairs.

### D. Protect the successor over time

#### 17. Historical namespace, current-default read

- **Mechanism:** Keep `W0` behavior only in a time-qualified output channel. Require a valid time reference for historical reads and teach the unqualified channel to consult `W1`; measure cross-channel leakage after later learning.
- **Novelty bet — improvement:** This is not the ledger's time-travel save/restore or a claim that a frozen historical adapter never forgets. The bet is joint, shared-capacity retention without historical answers bleeding into ambiguous present queries.
- **Cheapest first test:** Train on dated and undated dispatch queries, then add a third world with an overlapping partial reversal. Compare timestamp prompting, separate adapters and an equally sized retrieved history.
- **Old-task retention check:** Test verified historical answers, unchanged facts and routine current requests after the third update; an undated answer cannot be scored as correct just because it was once true.

#### 18. Audit for cheap reactivation, not just low fossil probability

- **Mechanism:** Before consolidation, simulate several small, benign future updates with `W0` answers withheld. Prefer a transfer whose worst measured reactivation is smaller at equal immediate performance, then test held-out update families.
- **Novelty bet — improvement:** Parent card 18 poses the latent re-emergence question. The added operation is selecting the initial write using a budgeted reactivation tournament, not predicting risk from lineage or adding a confidence gate.
- **Cheapest first test:** Give a toy student different inheritance losses with equal immediate fossil rates, then train on benign style or class-prior shifts. Compare selection by immediate fossil margin and post-update correction replay at equal compute; require held-out predictive value.
- **Old-task retention check:** Track unrelated skills and old-task margins pre/post each benign update; rule out a candidate that “wins” by being unable to learn the later task.

#### 19. Verify correction provenance before authorizing override

- **Mechanism:** Partition conflicts by current evidence provenance. Authorize a factual override from an independent measurement, but not from multiple models trained on the same source; leave unsourced disputes unresolved while still transferring nonconflicting skill components.
- **Novelty bet — primitive candidate:** The object is a source-dependence graph for adjudicating *specific conflicting premises*, not a scalar lineage debt or a fleet majority vote. Prediction-free verification is distinct from the ledger's killed obsolescence forecasts.
- **Cheapest first test:** Simulate three sources with cloned and independent errors and flip which generation is right. Compare source-blind consensus, direct lookup and verified two-teacher KD with equal evidence. Require robustness when provenance is partially missing.
- **Old-task retention check:** Score true old facts repeated by the ancestor and legitimate inherited exceptions, so refusing all donor claims does not count as safety.

#### 20. Correction leases tied to skill dependencies

- **Mechanism:** When two skills consume the same corrected fact, require them to depend on the same versioned correction record. A superseding fact invalidates only affected derived actions, and actions are regenerated jointly before returning to service.
- **Novelty bet — primitive candidate:** Card 6 concerns per-call binding and caching. This card concerns coordinated repair of *persistent outputs shared across skills*, where duplicate local corrections can disagree. A versioned global store without dependency-driven regeneration is the control.
- **Cheapest first test:** Interleave two saved products (e.g. a route plan and a load forecast) with a bridge correction between writes. Compare global cache flush, per-skill refresh, and dependency-driven joint refresh at equal regeneration budget.
- **Old-task retention check:** Measure availability and accuracy on unaffected products during refresh as well as earlier plans and forecasts after the change.

#### 21. Make successive inherits compose in either order

- **Mechanism:** For skills with independent declared goals that read shared world facts, fit updates so inheriting A then B and B then A agree on composed behavior under fresh world inputs. Keep asymmetric order only when goals genuinely depend on one another.
- **Novelty bet — primitive candidate:** The claim is selective order-independence *under world substitutions*, not a generic composition contract or merge optimization. Direct training on generated joint labels at equal budget is mandatory per the ledger.
- **Cheapest first test:** Inherit a routing rule and a packing rule, each referring to a shared depot status. Use a withheld combination of changed depot and load. Compare joint-label KD and rehearsal plus gate; reject if alternate-order training does not help beyond both.
- **Old-task retention check:** Score A and B separately after both orders, plus unrelated requests after each stage. A merge that forgets both skills is trivially order-independent.

#### 22. Allocate a finite audit budget by consequence, not disagreement

- **Mechanism:** Use a simulator to map one disputed premise to the set of downstream decisions affected by its correction. Spend audit work on the highest reduction in expected downstream regret per verified premise, and retarget all affected updates from the result.
- **Novelty bet — improvement:** The hypothesis is shared downstream value even for low-disagreement premises, not a new margin gate or a resurrection of sparse syndrome checks (the ledger found diffuse damage). Charge the cost of constructing the dependency estimates.
- **Cheapest first test:** Simulate both diffuse influence and a few shared premises across planning tasks. Compare audit by disagreement, uniform queries, and direct end-task audit at equal total cost. No claim if it only wins when concentration is explicitly built in.
- **Old-task retention check:** Include old tasks unrepresented in the regret weighting and worst-group retention on rare old requests; report who pays for reallocating the audits.

## Ranked deeper sub-questions

1. **What is the cheapest evidence that identifies a rule when the old world makes rival rules look identical?** Start with cards 1, 3 and 4. Produce indistinguishable pairs, then measure how many premise interventions or policy bits are needed to separate them under a held-out `W1`. If the accessible interventions do not separate them, report the ambiguity instead of treating agreement with `B1` as proof.
2. **Can the successor supply the premises while the ancestor supplies the procedure, even when neither is wholly right?** Compare cards 6–9 and 13 on `Q ∩ R`, with fallible lookup and user overrides kept separate. Advance only if both the skill decision and the companion fact query beat the gate/conditioned-KD frontier without degrading untouched tasks.
3. **Where does the correction get lost: in the target, the write, or later learning?** Compare an oracle-premise donor target, a frozen decoding proxy and a written student, then apply benign updates (cards 11, 16 and 18). If correcting the target fixes all three phases, do not add a write-time or reactivation mechanism.
4. **Do independently safe inherits stay safe when they share facts over generations?** Cards 19–21. Use four generations, held-out combinations, a real reversal and at least one tempting but wrong successor belief. Require retention of earlier skills and compare against shared retrieval plus the gate at equal cost; if that stack ties, stop.
