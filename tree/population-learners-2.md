# Population continual learners 2: Preserve disagreement; retire a teacher

Depth 1 · 28 candidate primitives · **Ambitious but doable** · Ideas only; no experiments run

**Parent:** [PR #379](https://github.com/manojbajaj95/cl/pull/379) · [PL02: disagreement-preserving transplant](root-population-learners.md#pl02--disagreement-preserving-transplant--ambitious-but-doable-p) · [PL32: forget one teacher, preserve the convergent skill](root-population-learners.md#pl32--forget-one-teacher-preserve-the-convergent-skill--ambitious-but-doable-p). Neither parent scored 4; both were kept at 3. This node branches on how each could fail. **P** labels a candidate primitive: the mechanism specifies an operation or object another method can reuse. A renamed baseline, or a tie against it, does not earn that label.

## Literature and control contract

Checked the linked arXiv titles and abstracts and the FedWeIT proceedings page. Each gap is a distinction from the cited mechanism, not a claim of exhaustive novelty. The two control sets below apply **to every card in their respective branches**; individual cards add a close control or diagnostic.

- **A · Transfer.** Compare no import, plain donor delta with a tuned step size, [Federated Orthogonal Training (FOT)](https://arxiv.org/abs/2309.01289) protecting old layer-input subspaces, [Gradient Projection Memory (GPM)](https://arxiv.org/abs/2103.09762) on the recipient’s own old tasks, [FedWeIT](https://proceedings.mlr.press/v139/yoon21b.html) selectively transferring sparse task weights, [TIES](https://arxiv.org/abs/2306.01708) resolving tensor sign conflicts, and [PL01 bridge packets](root-population-learners.md#pl01--bridge-packets--ambitious-but-doable-p) on the same matched items. Also run flat PL02 and ordinary recipient-output [OGD](https://arxiv.org/abs/1910.07104) on **the same probes**; otherwise extra probe coverage can look like a new projection rule. Use shared initialization for weight-space controls; if examining incompatible bases, supply the same alignment to compatible comparisons and include functional distillation.
- **B · Expiring teacher.** Compare no retirement, [task-vector negation](https://arxiv.org/abs/2212.04089), teacher-free retraining, [SISA](https://arxiv.org/abs/1912.03817) with an isolated shard/slice replay opportunity, [FedEraser](https://arxiv.org/abs/2012.13891) adapted to the historical-update/shared-server setting it assumes, and [PL29 teaching-route cut](root-population-learners.md#pl29--distillation-cut-for-forgetting--ambitious-but-doable-p) under the same known graph. Report that graph’s blind spots separately. Compare **flat PL32** as well. Teacher-free retraining rebuilds affected descendants from allowed pre-teacher state, excluding derivative supervision, optimizer state and teacher-conditioned examples when those are in scope. A full replay oracle can exceed the cheap methods’ budget; report its cost. [TOFU](https://arxiv.org/abs/2401.06121) and the [digital forgetting survey](https://arxiv.org/abs/2404.02062) motivate retain/forget evaluation, but here the target is an identified teaching dependency, not deleting every occurrence of the behavior or certifying data erasure.

**Readouts.** In A, the comparison is on matched inputs with elicited, legitimate policies and task score separated from preference score. With recipient margin r, donor margin d and anchored sign s = sign(r₀ − d₀), protect a floor on s(r − d) *and* require that neither fork crosses its own relevant decision boundary. Ignore unsupported matches. With a fixed donor, the derivative of r − d is just the recipient derivative: equality protection on the same score and items is ordinary output preservation. A candidate must add something beyond renaming that Jacobian. In B, distinguish **independently supported**, **teacher-dependent**, and **unknown**; measure false retention of teacher-only behavior, loss of independent competence, and how often the system abstains. “Independent” means a clean witness or an allowed intervention, not merely agreement with someone else. In both branches freeze untouched A/B (at least one old local skill per cohort), keep guard/provenance probes separate from held-out tests, and match compute, observations, message bytes, archive size and serving cost where possible. All tests below are proposed CPU toys unless a larger model is explicitly needed.

## A · Why a disagreement-preserving transplant might fail

### PL2-01 · One-sided margin budget — Ambitious but doable (P)
- **Mechanism:** Replace an equality null space with spendable slack for each signed matched contrast. An import may narrow the gap down to the anchored floor, but may not move either endpoint across its own decision boundary. Carry unspent slack into the next transplant rather than resetting the anchor to the latest smaller gap.
- **Nearest prior / gap:** [OGD](https://arxiv.org/abs/1910.07104) protects old outputs; [PCGrad](https://arxiv.org/abs/2001.06782) removes conflicting gradient components. Neither comparator is a persistent, anchored budget on matched policy disagreement.
- **Cheapest first test:** Two two-dimensional classifiers with a shared feature direction that consumes slack but preserves decisions. Compare flat PL02 and identical one-sided constraints on own outputs, with a second donor that would exhaust the budget. Tie if same-probe own-output bounds recover the frontier.
- **Old-task retention:** Score untouched A/B and both original policy decisions after the second import in both orders.

### PL2-02 · Calibrated action-rank cone — Ambitious but doable (P)
- **Mechanism:** Translate each fork’s private action scores into an ordering on a common action set. Exchange ties and pairwise order constraints, not raw margins, and admit deltas only within the resulting decision cone. A separately measured confidence floor covers abstention.
- **Nearest prior / gap:** [TIES](https://arxiv.org/abs/2306.01708) elects signs of weights; [OGD](https://arxiv.org/abs/1910.07104) preserves outputs. The cone is invariant to private monotone recalibration of scores while protecting which actions each fork prefers.
- **Cheapest first test:** Three-action classifiers with known temperature and nonlinear monotone distortions. Compare matched-probe ordinal distillation and post-hoc calibration plus PL02; tie if calibration recovers the same route decisions and shared gains.
- **Old-task retention:** Check untouched A/B including prior ties and abstentions after two differently calibrated donors.

### PL2-03 · Paired common-mode write — Ambitious but doable (P)
- **Mechanism:** When both forks adopt a shared update, jointly choose two patches whose changes to corresponding decision contrasts agree. Unlike projecting each patch onto its own null space, permit common motion, provided each fork’s action floor still holds.
- **Nearest prior / gap:** [FOT](https://arxiv.org/abs/2309.01289) modifies a global aggregate to protect old layer-input subspaces. This operation couples two *distinct* recipient writes through a shared functional difference rather than broadcasting one protected update.
- **Cheapest first test:** Two small heads with different parameterizations, a nuisance shift that requires paired motion, and a near-boundary policy case. Compare independent projections and shared-logit distillation. Tie if independent one-sided admission matches.
- **Old-task retention:** Score untouched A/B on both heads and their genuine conflict before and after the coupled write.

### PL2-04 · Missing-support fork certificate — Ambitious but doable (P)
- **Mechanism:** Bind a protected contrast to the intersection of validated contexts. Where only one fork has support, emit an unresolved match with the single missing counterpart needed to admit that part of the delta. Permit the supported portion to travel alone.
- **Nearest prior / gap:** [FedWeIT](https://proceedings.mlr.press/v139/yoon21b.html) transfers task-specific weights selectively; PL01 supplies a bridge pair. The certificate explicitly withholds an export on unpaired support without vetoing the entire shared improvement.
- **Cheapest first test:** Two cohorts supply observations on overlapping intervals, with a policy reversal only outside the overlap. Compare nearest-neighbor matching, bridge packets and withholding the full patch. Tie if overlap trimming alone matches at equal queries.
- **Old-task retention:** Score untouched shared A/B and both forks’ old private-support variants; report unmatched contexts separately.

### PL2-05 · Finite-step contrast crossing record — Ambitious but doable (P)
- **Mechanism:** Turn an import into a sequence of proposed increments. Record the first candidate step at which a guard not used to fit the local Jacobian detects a gap-floor breach, re-estimate there, and ship only the safe prefix and residual as distinct objects.
- **Nearest prior / gap:** [Adam-NSCL](https://arxiv.org/abs/2103.07113) trains in old-feature null spaces; it does not represent the first failing segment of a received delta as an independently reusable remainder.
- **Cheapest first test:** A two-layer ReLU pair where a tangent-safe delta crosses an activation boundary. Compare equal-probe line search, relinearized PL02 and prefix/residual exchange to a third fork. Tie if ordinary line search gives the same downstream reuse.
- **Old-task retention:** Score untouched A/B at each accepted checkpoint and after a third fork imports the residual.

### PL2-06 · Contrast commutator ledger — Ambitious but doable (P)
- **Mechanism:** For two admitted writes p and q, save the difference in matched-contrast slack between importing p then q and q then p, recomputing the projection at each intermediate state. An order-sensitive edge travels with the pair; it can constrain the next rebase.
- **Nearest prior / gap:** [TIES](https://arxiv.org/abs/2306.01708) handles sign disagreement in a static merge. Root PL07 and the ledger’s write-skew cover interaction tests; the narrower claim is that the *signed order difference* is portable advice for a later recipient, not just a conflict alert.
- **Cheapest first test:** Two nonlinear toy heads admit both deltas alone; reverse order on a third head. Compare endpoint-only combined probe veto and full pairwise replay at equal calls. Tie if scalar order-free interference predicts admission.
- **Old-task retention:** Recheck A/B after both orders and after a third, unrelated transplant.

### PL2-07 · Falsifiable contrast basis — Ambitious but doable (P)
- **Mechanism:** Compress a recipient’s guard Jacobian into a basis plus an omitted-direction exception interface. A donor proposes a new delta to a recipient-side adversary searching for a matched item where the basis predicts no contrast movement but the full model moves.
- **Nearest prior / gap:** [GPM](https://arxiv.org/abs/2103.09762) compresses important past gradients using representation subspaces. Here a concrete incoming write may falsify the compressed basis and mint the next exception; retained variance is not the admission test.
- **Cheapest first test:** Tiny adapter with a low-variance but decisive rare contrast. Compare GPM at equal rank, fixed held-out guards and uniform basis refresh. Tie if routine refresh catches the same rare breaches per probe.
- **Old-task retention:** Score A/B on frequent and rare contrast groups after three compressed exchanges.

### PL2-08 · Diagnostic bridge reversal — Ambitious but doable (P)
- **Mechanism:** Supply a second pair that reverses the cohort cue while holding preferences fixed, in addition to PL01’s pair that flips legitimate preference while holding task fixed. Only protect the contrast component that follows the elicited preference across the cue reversal.
- **Nearest prior / gap:** [FedWeIT](https://proceedings.mlr.press/v139/yoon21b.html) selects weighted sparse transfer; PL01 alone cannot disambiguate a shortcut correlated with preference on both supplied inputs. The object is a four-cell test that can invalidate the *thing protected*.
- **Cheapest first test:** Symbolic style tasks where font predicts policy in training but not at evaluation. Compare plain bridge, nuisance augmentation and invariant replay on the same four labels. Tie if augmentation alone protects the legitimate contrast while breaking the shortcut.
- **Old-task retention:** Score A/B on old style choices with normal and swapped cues after exchange.

### PL2-09 · Donor-motion accounting — Ambitious but doable (P)
- **Mechanism:** Store separate observations of recipient and donor movement against frozen reference policies. On a new round, attribute gap shrinkage to their respective changes; a recipient cannot treat genuine donor revision as slack granted to its own import.
- **Nearest prior / gap:** [Git-Theta](https://arxiv.org/abs/2306.04529) tracks parameter ancestry; [OGD](https://arxiv.org/abs/1910.07104) protects a previous model’s outputs. The operation separates two moving policy endpoints before updating a relative protection dispatch.
- **Cheapest first test:** Both forks change asynchronously; one donor changes a valid local rule while an older transplant arrives. Compare a frozen donor anchor, continuously recomputed PL02 and per-fork ordinary version pins. Tie if version pins preserve equal transfer without stale constraints.
- **Old-task retention:** Check untouched A/B separately for both evolving cohorts, neither scoring retired preferences as still live nor quietly replacing preserved ones.

### PL2-10 · Contrast feasibility witness — Ambitious but doable (P)
- **Mechanism:** When no update in the exposed adapter span satisfies a new gain target and all old policy floors, return the smallest conflicting set of guard inequalities and the span in which infeasibility was checked. A third fork can offer a new writable direction instead of another scaled version of the same delta.
- **Nearest prior / gap:** [Adam-NSCL](https://arxiv.org/abs/2103.07113) limits optimization to a protective space; [LoraHub](https://arxiv.org/abs/2307.13269) chooses a composition from existing adapters. The reusable object is scoped refutation of a *class* of proposed imports that can guide expansion, not a global impossibility claim.
- **Cheapest first test:** A two-dimensional linear guard system where a third adapter adds the only feasible direction. Compare rejection bit, raw active constraints and automatic rank increase. Tie if ordinary capacity growth at equal rank and FLOPs finds the same repair.
- **Old-task retention:** Check untouched A/B before the rejected import and after expanding the writable span.

### PL2-11 · Contrast-preserving recipient rebuild — Ambitious but doable (P)
- **Mechanism:** For models that share behavior but not coordinates, send donor before/after functional effects plus a contrast budget. Fit the recipient’s *increment* against those effects under the budget, leaving its baseline outputs free on contexts the donor never observed.
- **Nearest prior / gap:** [FedMD](https://arxiv.org/abs/1910.03581) distills across heterogeneous clients; PL01 supplies matched examples. The distinct proposal is distillation of increments under per-item disagreement floors, with attribution to the receiving update rather than consensus on absolute predictions.
- **Cheapest first test:** A linear and a two-layer classifier share a decision interface but are not weight-compatible. Compare absolute distillation, increment-only distillation and bridge replay at equal labels. Tie if adding a private-output trust region to ordinary distillation suffices.
- **Old-task retention:** Score untouched A/B in both architectures, especially the recipient’s unshared old contexts after a round-trip transfer.

### PL2-12 · Coalition conflict witness — Ambitious but doable (P)
- **Mechanism:** Keep a graph of legitimate matched disagreements, each with a floor and cohort authority. Multiple updates may satisfy every edge involving the importing fork today yet make an upcoming joint adoption infeasible; a short cycle witness records which pending edge forces the conflict.
- **Nearest prior / gap:** [FOT](https://arxiv.org/abs/2309.01289) aggregates protection of global past tasks; [PCGrad](https://arxiv.org/abs/2001.06782) addresses pairwise task-gradient conflict. This object is a graph-level, context-scoped certificate about pending multi-fork adoption, not a majority vote.
- **Cheapest first test:** Three scalar-margin learners each permit a local move; the combination closes one directed edge. Compare per-receiver constraints, joint constrained solve and local cycle disclosures with one edge per message. Tie if simply sharing each local guard clears the same conflicts.
- **Old-task retention:** Evaluate untouched A/B, including the least represented cohort, after the three-way rollout.

### PL2-13 · Reversible contrast escrow — Ambitious but doable (P)
- **Mechanism:** Keep the imported component that most reduces guard slack in an independently switchable adapter until both forks test it on a new matched batch. If it fails, detach that component and revalidate any local updates that learned against it before consolidating.
- **Nearest prior / gap:** [FedWeIT](https://proceedings.mlr.press/v139/yoon21b.html) separates global and task-specific parameters; [Git-Theta](https://arxiv.org/abs/2306.04529) supports structured version history. The escrow makes a *specific closing component plus its dependent writes* removable after a recipient has continued learning.
- **Cheapest first test:** Split a delta in a tiny residual net and introduce one latent guard violation after a local update. Compare full patch rollback, shadow release and isolated adapters with ordinary dependency tracking. Tie if generic shadow rollback matches.
- **Old-task retention:** Score untouched A/B and unrelated local skills acquired during escrow, before and after selective withdrawal.

### PL2-14 · Future-plasticity disagreement probe — Ambitious but doable (P)
- **Mechanism:** Protect not only the present disagreement but each fork’s ability to deepen its own preference with one authorized local step. Include the two post-step contrasts in the transfer contract only when the next-step examples are independently witnessed.
- **Nearest prior / gap:** [GPM](https://arxiv.org/abs/2103.09762) preserves old important representation subspaces; root PL03 tests learnability after reunion. Here the return value of a matched local learning step qualifies an import even when forks remain separate.
- **Cheapest first test:** Two ReLU heads retain opposite outputs on guards after a transplant, but one loses the channel it would use for the next local refinement. Compare flat PL02 and preservation of gradient norms alone. Tie if present outputs and step norms identify the same bad imports.
- **Old-task retention:** Score untouched A/B after import and again after each fork takes the allowed local step.

## B · Why retiring a teacher might erase the wrong thing

### PL2-15 · Four-way teaching receipt — Ambitious but doable (P)
- **Mechanism:** At adoption, test small branches with neither source, teacher only, independent evidence only and both, using matched training budgets. Record whether independent evidence suffices and whether the sources only work jointly. At expiry, replay from the independently sufficient branch or return unknown if the comparison did not resolve it.
- **Nearest prior / gap:** [SISA](https://arxiv.org/abs/1912.03817) isolates training influence for cheaper replay; [TRAK](https://arxiv.org/abs/2303.14186) attributes predictions to data. The four-way receipt tests substitution and synergy between teaching routes instead of summing per-source attribution.
- **Cheapest first test:** Tiny classifier with redundant, complementary and teacher-only features. Compare single-source attribution, equal-budget two-way ablation and full teacher-free replay. Tie if no interaction cell changes the retirement decision.
- **Old-task retention:** Score untouched A/B and unrelated independent skills after switching to the teacher-free branch.

### PL2-16 · Independence challenge, not agreement — Ambitious but doable (P)
- **Mechanism:** Request an intervention on which a teacher shortcut and the independently proposed rule disagree, then ask whether an allowed teacher-free child learns the rule on a disjoint split. If no such intervention exists under the access constraints, keep the source status unknown; a positive outcome is not proof about the original model’s weights.
- **Nearest prior / gap:** [Influence functions](https://arxiv.org/abs/1703.04730) trace predictions back to examples under a local approximation; [TOFU](https://arxiv.org/abs/2401.06121) tests forget/retain performance. This challenge seeks new evidence that a viable substitute need not inherit the teacher.
- **Cheapest first test:** Decision tables where the teacher uses a color shortcut and the child can query one orthogonal cue. Compare random fresh queries, apparent agreement and scored attribution. Tie if random queries resolve as many cases at matched cost.
- **Old-task retention:** Score A/B in color-present and swapped-color regimes after adopting a resolved replacement, not just on the distinguishing query.

### PL2-17 · Unknown with a counterexample pair — Ambitious but doable (P)
- **Mechanism:** Attach two feasible histories to an unknown label: one where retained evidence would suffice after expiry and one where it would not. Carry the minimal discriminating observation forward, so a later peer can resolve the case without rerunning all audits.
- **Nearest prior / gap:** [TRAK](https://arxiv.org/abs/2303.14186) estimates source contributions; [TOFU](https://arxiv.org/abs/2401.06121) checks departure from retain-only behavior. The proposed abstention is constructive: it shows why current records cannot support either source assignment and specifies what might separate them.
- **Cheapest first test:** Enumerate tiny learning histories with identical final state and visible metadata but distinct teacher-free counterfactuals. Compare attribution thresholds, generic abstention and paired-history unknowns with one later query. Tie if simple uncertainty ranks the same queries.
- **Old-task retention:** Score A/B while uncertain paths are quarantined and after the first safely resolved path returns to service.

### PL2-18 · Descendant-contamination frontier — Ambitious but doable (P)
- **Mechanism:** Label checkpoints by the last point at which the affected subnetwork’s weights, optimizer and incoming training examples were all independent of the teacher. Rebuild from that point only for affected behaviors; split an apparently clean weight slice when its optimizer or input stream is tainted.
- **Nearest prior / gap:** [SISA](https://arxiv.org/abs/1912.03817) resumes an affected shard before the relevant slice; [FedEraser](https://arxiv.org/abs/2012.13891) reconstructs from retained historical client updates. This frontier follows derivative supervision and other learning state across forks rather than input ownership or client ID alone.
- **Cheapest first test:** Two-layer toy model with uncontaminated weights but teacher-derived optimizer momentum in one block. Compare weight-only rollback, SISA plus ordinary source labels and full replay. Tie if reconstructing from the latest weight checkpoint is just as faithful to the clean oracle.
- **Old-task retention:** Score A/B right after reconstruction and after the first optimizer step, when hidden carryover would surface.

### PL2-19 · Curriculum edge excision — Ambitious but doable (P)
- **Mechanism:** Record who chose each trial as well as who supplied the label. When the teacher picked examples that were then locally labeled, regenerate the selection on a teacher-free shadow, not the labels; preserve examples that independent selection also reaches.
- **Nearest prior / gap:** [FedEraser](https://arxiv.org/abs/2012.13891) removes a target client’s contribution from an aggregate with historical updates; a PL29 cut blocks future paths. Here a past teacher affects what independent evidence became observable even though no teacher labels remain.
- **Cheapest first test:** An active linear learner receives local labels on teacher-selected boundary points. Compare removing only teacher-labeled samples, reselecting queries and full replay with teacher-free choices. Tie if label-only tracking predicts the same result after one more round.
- **Old-task retention:** Score untouched A/B on both regions over- and under-sampled by the teacher after reselection.

### PL2-20 · Source-conditioned functional splice — Ambitious but doable (P)
- **Mechanism:** Learn a small substitute from verified independent evidence, then replace only the causal feature path on which the expired teacher still affects responses. Merge the substitute only if swapping its activations preserves independent behavior without restoring a deliberately planted teacher-only side effect.
- **Nearest prior / gap:** [Task Arithmetic](https://arxiv.org/abs/2212.04089) negates a task direction; [TracIn](https://arxiv.org/abs/2002.08484) traces training-example influence. The splice uses an intervention to test replacement of a teacher-dependent route, rather than treating all current competence as its effect.
- **Cheapest first test:** Tiny MLP with two routes to the same skill and distinct side effects. Compare equal-rank negation, independent distillation with no targeted splice and activation replay. Tie if ordinary clean distillation matches with equivalent A/B retention.
- **Old-task retention:** Recheck untouched A/B, including unrelated functions sharing the cut feature, after the splice and a continued-learning step.

### PL2-21 · Independent relearning witness — Ambitious but doable (P)
- **Mechanism:** Train a short-lived child starting from an audited pre-teacher state. Give it only independently selected evidence and use a demonstrated learning trajectory as a portable receipt that justifies restoring the skill through that child. Do not use fast reacquisition from contaminated weights as evidence of independence.
- **Nearest prior / gap:** [SISA](https://arxiv.org/abs/1912.03817) reduces replay cost; [Artificial Generational Intelligence](https://arxiv.org/abs/2406.00392) studies transfer across generations. This operation asks a clean trained child to stand as a positive witness of replaceability, not as proof that a modified original has forgotten.
- **Cheapest first test:** Synthetic symbolic skill with adjustable sample requirements. Compare brief clean-child learning, post-negation relearning and equal-budget retraining from the freshest eligible checkpoints. Tie if random clean restart at the same budget yields the same viable transfer receipts.
- **Old-task retention:** Score old A/B on the adopted version after transferring the witnessed skill, rather than only on the disposable child.

### PL2-22 · Delayed-reconnection embargo — Ambitious but doable (P)
- **Mechanism:** Give incoming artifacts a behavior-scoped admission state of independent, blocked or unknown when an offline peer rejoins after expiry. Revalidate equivalent behavior against an allowed independent witness before admitting ambiguous artifacts, rather than permanently banning the peer or treating a new commit as clean.
- **Nearest prior / gap:** [Git-Theta](https://arxiv.org/abs/2306.04529) tracks structured commits; PL29 cuts known teaching edges. This gate exercises cases where a permitted returning peer may carry a stale relationship via a transformed model or a genuinely independent implementation.
- **Cheapest first test:** Four-peer replay DAG with two returning distillates that have different ancestry and the same skill. Compare full node exclusion, plain teaching-route cut and fresh commit checks. Tie if source-aware graph quarantine alone distinguishes them.
- **Old-task retention:** Score A/B during disconnection, immediately on return and after one new peer-to-peer transfer.

### PL2-23 · Convergent-skill replacement cut — Ambitious but doable (P)
- **Mechanism:** Model an independently witnessed substitute as an edge that can be installed *before* deleting an expiring edge. Choose replacement plus cut together; a cut is invalid if it disconnects the only remaining provider of a legitimate rule.
- **Nearest prior / gap:** PL29 cuts teaching routes to prevent revival; [FedMD](https://arxiv.org/abs/1910.03581) provides heterogeneous distillation to move a skill. The joint operation transfers responsibility to a known independent teacher and tests continuity under the new graph, rather than cutting then trying to recover service.
- **Cheapest first test:** Five-node graph with one approved substitute for two behaviors but only one safe redirect. Compare cut-only, sequential greedy repair and optimal joint planning with access to the same graph. Tie if planning with ordinary reachability meets all the functional constraints.
- **Old-task retention:** Verify old A/B on every affected path during the handover and after a stale peer rejoins.

### PL2-24 · Selective re-teaching seal — Ambitious but doable (P)
- **Mechanism:** After retirement, certify an independently recovered implementation as eligible to *teach*, not merely serve. Test a clean downstream learner’s behavior and the retired teacher’s marker under matched teaching interactions; revoke the seal if the recipient reproduces the teacher-only marker.
- **Nearest prior / gap:** [TOFU](https://arxiv.org/abs/2401.06121) compares an unlearned model against one trained without the forget data; PL29 tests a reconnection. This seal directly tests what an allowed implementation causes a fresh third party to learn.
- **Cheapest first test:** Two clean-looking teachers answer every standard A/B probe alike, but one encodes a stale convention in demonstrations used for training. Compare standard retention/forget probes, direct trajectory inspection and the recipient seal at equal query cost. Tie if direct inspection discriminates just as reliably.
- **Old-task retention:** Score A/B on both approved teachers and their students after one permitted teaching cycle.

### PL2-25 · Attribution disagreement as a query trigger — Ambitious but doable (P)
- **Mechanism:** Compare a checkpoint-derived attribution with a small counterfactual removal. Spend the next scarce clean query only where they disagree about whether an allowed source can replace the expiring one; return unknown if they agree only under untested assumptions.
- **Nearest prior / gap:** [TracIn](https://arxiv.org/abs/2002.08484) traces training-example influence and [TRAK](https://arxiv.org/abs/2303.14186) approximates data attribution at scale. This operation uses disagreement to choose a source-separating intervention, not as a confidence score for pre-existing removal.
- **Cheapest first test:** Two interacting data sources in small nonlinear learners; budget one extra query each. Compare attribution threshold, uncertainty sampling and discrepancy-triggered intervention. Tie if calibrated uncertainty alone resolves as many true cases.
- **Old-task retention:** Measure untouched A/B after both positive resolution and refusal to resolve; report the service cost of unknown decisions.

### PL2-26 · Set-valued retirement under order ambiguity — Ambitious but doable (P)
- **Mechanism:** Where timestamps determine only a partial order, replay a bounded set of legal teacher-free histories. Preserve a skill only on scopes where every candidate supports it; otherwise report the range and the missing ordering fact that would change the disposition.
- **Nearest prior / gap:** [FedEraser](https://arxiv.org/abs/2012.13891) reconstructs with available historical updates; SISA’s replay relies on ordered slices. The retirement output here is a partial identification result over compatible schedules, not a guess at one chronology.
- **Cheapest first test:** Three noncommuting updates, observed partial order and one queryable timestamp. Compare arbitrary topological replay, majority vote and interval retirement. Tie if all legal schedules actually yield the same retained decision.
- **Old-task retention:** Score A/B across the replay set and on the deployed outcome while unresolved branches are withheld.

### PL2-27 · Source-tagged nonlinear interaction quarantine — Ambitious but doable (P)
- **Mechanism:** When an expired teacher and an allowed source jointly created a useful skill, keep the evidence for each allowed main effect but quarantine the interaction until a clean child reproduces it from allowed inputs. A rule learned strictly through synergy is not relabeled independent just because half the inputs are allowed.
- **Nearest prior / gap:** [Task Arithmetic](https://arxiv.org/abs/2212.04089) composes and negates task vectors; [Towards Unbounded Machine Unlearning](https://arxiv.org/abs/2302.09880) studies repeated deletion. This proposal separates source-conditional interaction for selective quarantine, rather than deleting a vector for the whole task every time.
- **Cheapest first test:** An XOR-like skill requires both input channels, one teacher-supplied. Compare additive negation and retuning on retained data; use PL2-15 receipts as the detection baseline. Tie if selective replay attains the same clean-reference agreement with no quarantine record.
- **Old-task retention:** Score A/B and the allowed main effects both during quarantine and after independently validated interaction recovery.

### PL2-28 · Retirement-stable fork audit — Ambitious but doable (P)
- **Mechanism:** Before switching to a verified independent replacement, check that it can learn one later allowed update without reactivating the expired marker or closing a legitimate cohort disagreement. Keep the pair of failing successor update and behavior as a transfer veto if the replacement fails.
- **Nearest prior / gap:** [Forgettable Federated Linear Learning](https://arxiv.org/abs/2306.02216) certifies target-client removal in its linearized framework; PL02 protects contrasts today. This audit concerns a named successor write and a separate functional obligation to other living forks, not a stronger removal certificate.
- **Cheapest first test:** Two tiny forks agree on the recovered skill but one implementation contains a dormant marker revealed by one later legal update. Compare one-shot forget/retain tests, independent replay and a matched-budget random successor challenge. Tie if ordinary holdouts find all failures exposed by the named write.
- **Old-task retention:** Score untouched A/B per cohort before retirement, after replacement and after the successor update, including old matched disagreements.

## Ranked deeper questions

1. **When is disagreement preservation more than ordinary output preservation?** (PL2-01, PL2-03, PL2-08, PL2-09) First eliminate the fixed-donor equality case using identical probes. Put both forks in motion, cross cue reversals with legitimate disagreement, and compare anchored slack and joint writes to same-probe own-output guards. A relative primitive earns its name only if it buys a better gain–retention frontier without erasing legitimate choices.
2. **What evidence licenses keeping an independently supported skill?** (PL2-15–PL2-17, PL2-19, PL2-21) Plant redundant evidence, teacher-induced sampling and genuine synergy in the same tiny stream. Against the teacher-free replay oracle, score correct replacements and abstentions separately. If cheaper receipts cannot distinguish independence from a teacher-shaped curriculum, investigate the unknown cases rather than promoting attribution scores into deletion claims.
3. **Does retiring one route survive a new generation?** (PL2-18, PL2-22–PL2-24, PL2-27) Return a distilled stale peer after a partition and let a clean peer try to teach the skill through the replacement. Require the teacher-only marker not to revive, the independent skill to keep propagating, and A/B to remain intact along live paths. If a teaching-route cut plus normal retraining does all three, keep the simpler method.
4. **Can a transfer contract anticipate order and future writes cheaply enough to matter?** (PL2-05–PL2-07, PL2-12–PL2-14, PL2-28) Compare sign/order records, cycle witnesses and one-step lookahead against equal-budget line search, random challenge and full replay. Reject mechanisms that only catch violations on their own probes or cost more than revalidating the entire next import.
