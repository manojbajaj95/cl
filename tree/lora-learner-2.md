# LoRA Learner 2: When the Hill Forks

Child of [A LoRA-Writing Learner](root-lora-learner.md) ([PR #344](https://github.com/manojbajaj95/cl/pull/344), depth 1) · 26 candidate primitives · 4 ranked questions · Ideas only; no experiments run

**Thesis.** Each user's feedback is a proposed uphill direction for a skill. Users can disagree because their feedback is noisy, because they took different routes around an obstacle, or because they actually prefer different summits. Keep climbing together while an admissible common move works. Fork learning if the users will need to respond differently to the same future correction, even when today's answers agree. Fork serving only when sharing fails under the declared budget **and** the system can tell which hill a request belongs to before acting. Rejoin if one skill can again deliver both the behavior and the needed future learning.

**Parent verdict.** [Flood triage row 470][triage] gave score 3 to LL17 (shared-write infeasibility plus feasible, callable children) and LL22 (separate amendment coordinates before serving outputs differ). The [ledger][ledger] rules out reviving a split-only retrieval hierarchy or treating present loss, a Gramian score, or effortless checkpoint restore as a useful learning fork. The generator isn't the novelty: a Learner writes real low-rank factors into a frozen Executor, but each proposal below needs to earn its keep **after** the first write.

## Shared repeated-revision protocol

- **Fixture.** Use a tiny frozen linear or ReLU Executor whose skill chooses among observable actions. Users or consenting cohorts provide pairwise feedback on the same alternatives. Stream: common initial skill → disputed correction C → intervening D → second amendment E (opposite, independent, or shared) → returns to old A/B, including rare B. Include stationary label noise, asymmetric noise, changing user composition without changed preferences, permanently different hills, temporarily different hills, and two hills invisible before action. Offer an ordinary user-provided preference cue or a paid query, never hidden cohort labels. Reuse matched action pairs and audit by user/cohort without inferring an identity from a protected attribute. In the toy, true utilities are for scoring; the writer and all non-oracle controls receive the same observations.
- **The baseline on every card (“Stack”).** Train or emulate small **static Text-to-LoRA and Drag-and-Drop writers** (description and prompt-batch inputs). At each revision rerun the frozen writer on the updated source/evidence, refine by **per-skill distillation**, and serve from an equally budgeted **routed LoRA library**. Use the better matched variant and give it the same user cue, source, feedback, router options, and write schedule. Also allow a continuous cue-conditioned shared adapter as a strong test of what counts as “shared.” Compare at fixed total live/peak bytes (parents, sidecars, certificates, router, and stored evidence), inference compute, and annotation/query limits; count rejected writes and all distillation. The per-card baseline line gives the specific repeated-stream advantage needed, not an assumed result. Shared-parent rank alone is not the budget.
- **What a proof licenses.** Let the allowed shared writes be `U`, with a specified rank/byte cap, trust radius or horizon, update ports, observation interface and old-task floors. A split needs (1) a checkable witness that no member of `U` meets **both** cohort improvement floors, (2) feasible children under the *same total budget* including routing, and (3) a pre-action separator at the claimed error/query budget. Exact finite checks prove only the declared toy statement. In a linearized convex relaxation, a dual contradiction can rule out the tighter original class only if the relaxation contains it; a local approximation without certified error is not a nonlinear impossibility proof. Inferred feedback constraints need independent validation or an explicit uncertainty model; a negative cosine or optimizer timeout is not a certificate. Use exact enumeration as a tie-seeking control, not a claim that neurons can infer proofs.
- **Learning fork.** Serving still uses one skill. Distinct amendment coordinates are state updated by authorized feedback, not two private answers cached under a mask. Pre-register a held-out intervention that can refute the predicted difference in response, and collapse the fork if the common updater passes it. Give an equal-cost symbolic sidecar the same inputs, alongside one meta-updater, immediate clone, and clone on observed answer disagreement.
- **Retention.** Every card includes the normal hidden A/B return evaluation immediately after each revision, on rare old traffic, and after E. Its extra slice tests likely damage. Report per-cohort and worst-cohort outcomes with a preregistered floor, solve rate, and fresh adaptation at matched retention. Never rescue old tasks by secretly selecting a frozen parent. “Don't write,” delaying forever, and “ask everyone” do not win.

## Literature check

Used Hugging Face Papers discovery and checked original arXiv records/abstracts; the comparisons are a mechanism-level screen, not priority claims.

| Nearest prior | Boundary for this node |
|---|---|
| [Text-to-LoRA][t2l] generates LoRA from task descriptions; [Drag-and-Drop][dnd] writes it from a handful of unlabeled prompts; [OPCD][opcd] uses student trajectories for context distillation; [Arrow][arrow] routes into a pre-existing adapter library. | Repeatedly regenerating, distilling and routing is the baseline, not a primitive. |
| [MaxMin-RLHF][maxmin] fits a mixture of preference distributions and learns an egalitarian objective. [P-RLHF][prlhf] jointly learns a lightweight user model and personalized LM. [Variational Preference Learning][vpl] infers user latents and conditions reward and policy models on them. [MiCRo][micro] uses a mixture preference model and context-aware routing. [Personalized Soups][soups] combines independently aligned models according to user preferences. | Multi-hill objectives, individual latents, mixtures and parameter interpolation are already known. Ask when the same live skill can no longer be shared and when only its update rule needs to diverge. Reward data can leave policies underdetermined ([partial reward identifiability][id]). |
| [MGDA-style multi-task optimization][mgda] seeks Pareto solutions; [PCGrad][pcgrad] projects conflicting gradients; [Graph Coloring][color] groups compatible updates. [DEN][den], [SEMA][sema], [CN-DPM][dpm], [DIMoE][dimoe], and [CDSP-MoE][cdsp] cover expansion, drift, task-free expert growth, and structural conflict. [O-LoRA][olora], [InfLoRA][inflora] and [DUET][duet] provide strong shared-space protection controls. | Try an admissible shared move before growth. Even a sound common-descent obstruction doesn't identify a callable branch or guarantee safety on old requests. |
| [MEND][mend] learns localized edit transforms; [learned optimizers][opt] generate updates; [OML][oml] meta-learns representations for continual learning; [ACL][acl] meta-learns CL algorithms; [GLAM][glam] groups and merges LoRAs. | Different learning rules, optimizer state and adapter merging are not novel in isolation. Test a fork with one serving skill, a measurable difference in response to feedback, and a rejoin that preserves that response. |

## A · Prove sharing fails before forking answers

### L2-01 · Obstruction with a callable counterexample
- **Mechanism:** Store a minimal set of cohort/retention inequalities that rules out sharing, plus each child's feasible write and the pre-action feature that separates their requests. If any part expires, the certificate no longer licenses a split.
- **Novelty vs nearest prior art:** [MGDA][mgda] searches for Pareto improvement; [DEN][den] splits drifting units. The candidate is a joint receipt for impossibility, feasibility and callability, not another common-descent optimizer.
- **Cheapest first test:** Enumerate an integer-bounded two-output head, including a negative-gradient cell with a feasible curved path and a cell where children work only with an unavailable oracle cue.
- **Old-task retention:** Route former shared calls, especially the rare near-boundary slice, through the children after C and E.
- **Beat the Stack on revisions:** After E changes one inequality, retain the unchanged proof pieces and use fewer paid write attempts to reach the same cohort floors; compare full exact rechecking too.

### L2-02 · Ask where one-hill and two-hill disagree
- **Mechanism:** Maintain both a shared objective with per-user noise/rater reliability and a two-objective explanation. Request the matched comparison that best separates their consequential predictions; only apply L2-01 once sharing fails for the resulting admissible models.
- **Novelty vs nearest prior art:** [MaxMin-RLHF][maxmin] fits latent preference mixtures and [MiCRo][micro] routes them. The candidate uses the competing models to buy evidence for or against an irreversible growth decision, not just improve mixture likelihood.
- **Cheapest first test:** Generate equally discordant labels from a single summit with asymmetric flips and from two summits. Select one repeat comparison or a shared calibration pair; compare posterior uncertainty sampling with the same annotations.
- **Old-task retention:** Check old users with inconsistent historical feedback and the low-volume cohort after the diagnostic and E.
- **Beat the Stack on revisions:** Spend fewer labels and child writes on noisy C/D, then reach both true cohort floors faster after E; lower split count alone doesn't win.

### L2-03 · Cluster directions conditional on the same move
- **Mechanism:** Group feedback by signed response to the same paid perturbations, rather than raw gradient or rater embedding. A group is reusable only if its directional agreement survives a change in task difficulty or response phrasing.
- **Novelty vs nearest prior art:** [MiCRo][micro] clusters preference distributions and [Graph Coloring][color] partitions conflicting gradients. Here an intervention-indexed group is the unit carried into a later *write feasibility* decision; ordinary clustering on the same probe results is the control.
- **Cheapest first test:** Cross user objective with wording and proposal quality; reverse their correlations at D. Compare gradient, user-embedding and probe-response grouping with held-out users.
- **Old-task retention:** Check users who choose different words for the same direction and older cross-cohort requests.
- **Beat the Stack on revisions:** Reuse direction groups across the reversal and reach both floors with fewer fresh labels or adapter writes at E; a matched offline router may tie.

### L2-04 · Prove a detour is not enough
- **Mechanism:** Require an obstruction over a finite sequence of legal, retaining shared writes, not just one step. Preserve a feasible detour rather than split if it reaches both improvement floors by the deadline.
- **Novelty vs nearest prior art:** [PCGrad][pcgrad] treats current gradient conflict; [DUET][duet] constrains preservation during projection. Bounded reachability is standard; the proposed reusable object is a horizon-scoped birth decision whose validity can be tested after revisions.
- **Cheapest first test:** Enumerate a three-state factor lattice with an initially flat step needed to reach a joint improvement; add a matched cell with the bridge removed. Compare trust-region search and one-step birth.
- **Old-task retention:** Check old requests at *every served step* of each detour, not just the endpoint.
- **Beat the Stack on revisions:** Avoid a costly unnecessary pair at C and finish E by the same deadlines using fewer modules or paid refinements; match search compute.

### L2-05 · Spend an extra rank before declaring two hills
- **Mechanism:** Produce a rank-budget ladder of falsifiers: for which budgets is sharing ruled out, and at what budget does a legal shared witness first appear? The allocator may buy rank instead of a router.
- **Novelty vs nearest prior art:** [InfLoRA][inflora] designs interference-free subspaces and [DIMoE][dimoe] evolves expert capacity. Test a joint rank/route price boundary, not an adaptive-rank schedule.
- **Cheapest first test:** Use rank-one and rank-two 2×2 quantized edits; enumerate the cheapest shared and split solutions as router bits increase. Compare rank-adaptive distillation and exact search.
- **Old-task retention:** Check the original tasks near the directions consumed by one more rank, through the same interface.
- **Beat the Stack on revisions:** Reuse the boundary to absorb D/E at lower peak bytes or fewer retrains than adding/routing independently distilled skills; fail if the Stack already picks the same rank with the same effort.

### L2-06 · Make an obstruction robust to rater replacement
- **Mechanism:** Compute whether sharing is still infeasible when any one rater's constraint or a fixed fraction of doubtful labels is removed. Report a witness family, not a majority vote. If only one reliable user needs another hill, use explicitly individual scope instead of asserting a cohort split.
- **Novelty vs nearest prior art:** [MaxMin-RLHF][maxmin] protects against aggregation over diverse groups. A deletion-robust proof about the *admissible LoRA intervention* differs from robust reward fitting; use both together as a control.
- **Cheapest first test:** Exact finite pairwise utilities with one duplicated rater, one rare coherent preference group, and one consistently noisy annotator; compare robust mixture fitting plus a conflict threshold.
- **Old-task retention:** Verify minority old skills are not silently overwritten when their evidence is sparse.
- **Beat the Stack on revisions:** Churn fewer children under repeated rater turnover while matching gains on the stable minority; do not count rejecting real minority preferences as savings.

### L2-07 · Split only the intersection the router can actually observe
- **Mechanism:** When a cue separates cohorts only on a subset of requests, write branches only on that subset and share behavior elsewhere. The certificate names the ambiguous slice and its best legal common action.
- **Novelty vs nearest prior art:** [P-RLHF][prlhf] models user preferences and [Arrow][arrow] routes by inputs. This candidate restricts split scope by observed identifiability, with a separate obstruction and safety floor for each scope.
- **Cheapest first test:** Create aligned and conflicting choices with a cue missing systematically on one region; compare full cloning, masked routing, and exact cue-conditional shared optimization.
- **Old-task retention:** Check old requests lacking cues and rare old calls on the scope boundary.
- **Beat the Stack on revisions:** Limit D/E updates to the identifiable region and lower total routed write cost without increasing wrong-branch actions on the hidden region.

### L2-08 · Counterfeit hills from changed exposure
- **Mechanism:** A split requires opposition on common proposals or an overlap bound that makes the effect identifiable. If users only saw different choices generated by the current skill, request a shared proposal before reading the disagreement as separate hills.
- **Novelty vs nearest prior art:** [Reward identifiability][id] characterizes observational ambiguity and [VPL][vpl] models latent preferences. Here common-proposal support is an explicit precondition on an adapter birth, not reward estimation alone.
- **Cheapest first test:** Match the observed label histograms of exposure-biased common utility and genuinely conflicting utility; buy one shared pair, then compare active overlap collection plus task-free growth.
- **Old-task retention:** Check users whose rare old option was previously never proposed and those who normally take the default response.
- **Beat the Stack on revisions:** Avoid copying adapters on exposure shifts C/D and need fewer changed proposals to reach real gains after E; count the paid common proposal.

### L2-09 · Let a new cue retire the old obstruction
- **Mechanism:** Index the impossibility proof to the information available to the shared Executor. An early split may rely on a paid question whose answer is used only by the router. If a later request exposes the preference directly to the Executor, invalidate the old proof and check whether one cue-conditioned LoRA can replace the branches.
- **Novelty vs nearest prior art:** [Personalized Soups][soups] changes the model with declared preferences and [SEMA][sema] responds to representation shifts. The proposed operation tests whether a change in what the Executor *observes* changes which split is necessary.
- **Cheapest first test:** Start with a paid router-only query, then reveal an intrinsic cue to every arm after D; corrupt a matched cue in another arm. Compare learned cue-conditioned serving and unconditional branch persistence.
- **Old-task retention:** Check clients that still omit the cue and the old default with misleading cue values.
- **Beat the Stack on revisions:** Collapse live bytes ahead of E and adapt in one update rather than updating two library entries, without misserving uncued old clients.

## B · Fork learning while answers still agree

### L2-10 · Fork from a contrast between future updates
- **Mechanism:** With one output policy and one common feedback payload, predict which new collateral changes each authorized cohort would accept. Keep separate amendment coordinates only if the held-out correction yields two different required changes.
- **Novelty vs nearest prior art:** [MEND][mend] applies a learned edit transform; [ACL][acl] learns a continual update algorithm. The candidate is a rule for allocating and scrapping a fork in a *currently common* skill, with an intervention that can disprove it.
- **Cheapest first test:** Use two decision tables with identical current answers. An identical correction is broad in one and a one-case exception in the other. Train on independent correction pairs, then test the next correction in a fresh cell.
- **Old-task retention:** Require identical initial serving, then check untouched A/B cases where an overbroad amendment would spill.
- **Beat the Stack on revisions:** Retain one serving adapter through C and apply E using fewer examples or bytes than separate distilled library entries, without waiting for costly user-visible errors.

### L2-11 · Fork who may amend a rule, not who may call it
- **Mechanism:** Keep one predictor but write separate feedback routes for clients with different amendment authority. Identical observations can alter a private coordinate for one caller and be treated as transient evidence for another.
- **Novelty vs nearest prior art:** [P-RLHF][prlhf] learns user-conditioned responses, and [MEND][mend] localizes edits. The candidate is distinct *learning authority* despite equal serving privileges and outputs; a symbolic authority table is the control.
- **Cheapest first test:** Two workflow owners request the same present behavior, but only one may change a particular default. Alternate accepted fixes and rejected amendments; match authenticated scope evidence.
- **Old-task retention:** Check ordinary use by both scopes after each accepted and refused change, including a rare old exception.
- **Beat the Stack on revisions:** Update only the affected amendment route after D/E instead of redistilling both caller skills; compare the equal-byte authority sidecar.

### L2-12 · Give feedback two inheritance paths
- **Mechanism:** One coordinate accumulates corrections shared across users; a second carries an independently mutable private amendment. A cross-application probe verifies that the exact same authorized shared correction takes effect once for both, while a private one does not leak.
- **Novelty vs nearest prior art:** [DEN][den] timestamps copies, [OML][oml] learns sharing that preserves plasticity, and [P-RLHF][prlhf] separates user conditioning. The target is a change to a live inheritance rule, not a static shared/private parameterization.
- **Cheapest first test:** Start with two indistinguishable toy service styles. Alternate a common clause amendment and corrections that should travel on only one feedback edge. Add a held-out order and compare explicit shared/private factors trained jointly.
- **Old-task retention:** Check both old scopes after each amendment, not just the skill whose feedback triggered it.
- **Beat the Stack on revisions:** Achieve the shared E correction with one checked write rather than two while preserving D's private gain; no gain if the Stack's shared adapter plus sidecar already does it.

### L2-13 · Fork the interpretation of a negated preference
- **Mechanism:** Maintain distinct amendment directions for “undo the last change” and “I prefer the opposite,” which coincide in some states but diverge when intervening revisions changed the baseline. A probe checks which interpretation each user actually endorses.
- **Novelty vs nearest prior art:** [VPL][vpl] models latent preference modes; [learned optimizers][opt] already use history when mapping gradients to steps. This fork is keyed to a user's verified meaning of feedback across revisions, not latent step-size tuning.
- **Cheapest first test:** Two choices share original and first-revision outputs; insert D so “undo C” no longer equals “want the opposite.” Compare an explicit semantic two-state updater and a recurrent learned optimizer.
- **Old-task retention:** Check innocent intervening D behavior and original requests outside C's changed region after the negated feedback.
- **Beat the Stack on revisions:** Retain a small feedback interpretation instead of redistilling histories; fewer corrections to restore both users after E at the same accuracy.

### L2-14 · Learn two stopping rules for the same climb
- **Mechanism:** Users prefer the same next answer today but differ on when improvements stop being desirable. Store a separate amendment threshold conditioned on observable context; serving remains shared until a calibrated probe crosses one threshold but not the other.
- **Novelty vs nearest prior art:** [Personalized Soups][soups] merges models for preference mixtures and [P-RLHF][prlhf] personalizes outputs. The claim is a cheap fork of *when future feedback keeps moving the model*, before another answer policy is justified.
- **Cheapest first test:** Two users favor stronger brevity up to different cutoffs. Vary whether complaint probabilities are monotone or noisy, and compare a shared updater with a continuous preference-strength control.
- **Old-task retention:** Check old verbose requests with explicit exceptions and rare brief requests below both cutoffs.
- **Beat the Stack on revisions:** Use fewer feedback events and no duplicate serving weights before crossing the cutoff, then stay within both users' bounds on D and E.

### L2-15 · Test an amendment twice with the recipient swapped
- **Mechanism:** In scratch state replay feedback once with its owner and once assigned to another scope, holding the supplied action pair fixed. Install the private coordinate only when the contrast predicts an independent, observable difference in a permitted future correction.
- **Novelty vs nearest prior art:** [P-RLHF][prlhf] conditions on user signals and [MEND][mend] assesses edit locality. The candidate couples an edit intervention to a fork commitment rather than using an ordinary user ablation to validate serving output.
- **Cheapest first test:** Use identical current histories with a later known correction rule. Swap scope on a sandboxed candidate; compare a user-embedding shuffle and a return-only control at equal interventions.
- **Old-task retention:** Test actual old scopes after serving normally; the swapped replay must never update a real customer's skill.
- **Beat the Stack on revisions:** Pay fewer real-world corrections after D/E by rejecting false private updates in scratch; count the extra scratch trials and miss rate.

### L2-16 · Reserve opposite amendments in one bounded write port
- **Mechanism:** While serving answers still tie, write two allowed directions to an unused amendment coordinate. The next validated feedback selects a direction, with no private serving weights saved in advance.
- **Novelty vs nearest prior art:** [OML][oml] makes future online updates easier and [InfLoRA][inflora] reserves noninterfering subspaces. This is a concrete two-way edit port with an intervention-based retirement rule, not a readiness score or generic basis allocation.
- **Cheapest first test:** Enumerate a rank-one writable port in a quantized linear head: valid upward and downward moves leave unrelated outputs fixed; include a case where one move is impossible. Compare a fixed shared basis, equal-rank clone and precomputed amendments.
- **Old-task retention:** Check unrelated old outputs before any move and after either signed amendment, including when the unused direction is retired.
- **Beat the Stack on revisions:** Make either later amendment fit one paid write with lower peak bytes than pre-distilled children, then retain usefulness after E; equal-cost precomputation may tie.

### L2-17 · Close a learning fork with a forward counterexample search
- **Mechanism:** Periodically try to find one legal feedback sequence on which two currently equivalent amendment routes still need distinct updates. Close the fork only on a scoped equivalence check; silence or absence of complaints is not a merge signal.
- **Novelty vs nearest prior art:** [GLAM][glam] groups and merges adapters, [ACL][acl] learns update dynamics. The merge target here is equivalence of future learning on a bounded feedback alphabet, not parameter closeness or current outputs.
- **Cheapest first test:** Enumerate two short feedback sequences on a finite updater pair whose differences emerge only on the second correction; compare end-to-end merge checks at a fixed query budget.
- **Old-task retention:** Check current old answers and both orders of old-user amendments after closure.
- **Beat the Stack on revisions:** Reclaim dormant sidecar bytes after D while avoiding an E regression that behavior-only merging misses; include exact re-distill and merge as a comparator.

## C · Follow moving hills, and rejoin when sharing returns

### L2-18 · Proof with an expiry condition, not an expiry date
- **Mechanism:** The obstruction names the assumptions that make it valid (for example, old floor, user cue error, or measured feedback interval). Keep both children only while those assumptions survive independent checks; don't resplit or rejoin on a schedule.
- **Novelty vs nearest prior art:** [SEMA][sema] detects shift and [DIMoE][dimoe] evolves a pool. Here the trigger is invalidation of a specific logical dependency and a fresh test of sharing, not generic drift.
- **Cheapest first test:** Alternate feedback drift outside and inside the active proof constraints, with matched marginal statistics. Compare periodic rechecks and shift-triggered growth/merge.
- **Old-task retention:** Recheck old tasks both when the proof remains live and when it is retired, especially cases protected by the changed bound.
- **Beat the Stack on revisions:** On D/E, rerun only implicated checks and avoid unnecessary regeneration while adapting as quickly after real changes.

### L2-19 · Rejoin behavior, keep the separately teachable directions
- **Mechanism:** If one serving write now clears both floors, replace children with one adapter but leave two cheap amendment coordinates where a later authorized intervention still predicts different corrections.
- **Novelty vs nearest prior art:** [GLAM][glam] merges adapters and [OML][oml] optimizes future learnability. The candidate is a *partial reverse* of serving split: serving merges before amendment semantics can merge.
- **Cheapest first test:** Run permanently distinct, temporarily aligned but re-diverging, and truly converged toy hills. Compare merge-all, keep-all, and GLAM plus an equally sized sidecar.
- **Old-task retention:** Check old clients who previously used each child immediately after rejoin and through the next two amendments.
- **Beat the Stack on revisions:** Cut serving bytes in the common phase and need fewer examples on renewed divergence than merge-all, without costing as much as keep-all.

### L2-20 · Need both directions to agree before rejoining
- **Mechanism:** Test whether corrections from either former child can be executed in one common write path while preserving the other's service and ability to accept its next ordinary correction. Record the first order in which the rejoin fails.
- **Novelty vs nearest prior art:** [GLAM][glam] limits growth by grouping weights and [DUET][duet] preserves old/new losses during an update. The test concerns two *ordered later updates* after a merge, not preservation at its insertion.
- **Cheapest first test:** Use a tiny finite nonlinear update table where a merged adapter passes today's checks but A→B destroys B's next valid edit; compare checking only single updates and exhaustive ordered checking.
- **Old-task retention:** Check old A/B under both orders and after either interrupted sequence.
- **Beat the Stack on revisions:** Spend fewer rollback/redistillation attempts after E than behavior-only merge with a routed library, charging the extra pre-merge trials.

### L2-21 · Rejoin the rule across changes in who shows up
- **Mechanism:** Separate a changing mix of users from a change in the hills. Rejoin only if a common write clears the old and new cohort floors under fixed per-user weights and over matched request support.
- **Novelty vs nearest prior art:** [MaxMin-RLHF][maxmin] targets equity across groups and [MiCRo][micro] models mixtures. The candidate is a falsifier for population-driven false convergence inside a skill rejoin.
- **Cheapest first test:** Make one cohort disappear temporarily, matching pooled agreement with a case of real convergence. Use bounded observations and compare max-min fitting and a frequency-weighted merge.
- **Old-task retention:** Return the missing old cohort without notice and score rare users individually.
- **Beat the Stack on revisions:** Reduce mismerges and repeated rebuilds during user churn at matched live bytes, not by indefinitely keeping dead branches.

### L2-22 · Reuse the separating comparison, not the previous children
- **Mechanism:** When rejoining, discard child adapters; retain a tiny action pair plus the scope of its prior diagnostic validity. If the hills later separate differently, test the pair, relearn only the directions still supported, and discard the obsolete explanation.
- **Novelty vs nearest prior art:** [CN-DPM][dpm] grows experts and [GLAM][glam] merges; the parent LL23 proposed a separating witness. The tighter test here requires changed objectives after rejoin and checks where an old comparison fails, so restoring old children is wrong.
- **Cheapest first test:** Alternate opposite → common → differently opposite choices; allow one shared comparison after the last shift. Compare held adapter copies, fresh active preference discovery, and a shuffled comparison.
- **Old-task retention:** Test ordinary old actions while merged and on new routes, including tasks once diagnosed by the now-obsolete comparison.
- **Beat the Stack on revisions:** Match the new separation with fewer purchased labels than fresh routing and fewer stored bytes than keeping old children; stale splits are failures.

### L2-23 · Split only what survives the feedback time scale
- **Mechanism:** Allow a private learning fork for short-lived directional disagreements. Require a holding-time premise before a permanent serving split, and revoke it when both objective models predict a common summit over the next revision horizon.
- **Novelty vs nearest prior art:** [CN-DPM][dpm] adds components and [Graph Coloring][color] recomputes temporary compatibility groups. The candidate is a reversible *learning-fork versus serving-fork decision* conditioned on persistence, not a cooldown alone.
- **Cheapest first test:** Match the first two feedback rounds in transient and persistent conditions; vary whether an announced deadline predicts persistence. Compare fixed hysteresis and Bayesian change detection with the same predictor.
- **Old-task retention:** Check rare old cases during the temporary fork and after disagreement ends without permanent routing changes.
- **Beat the Stack on revisions:** Spend less on full adapter creation across transient C/D, while meeting each cohort's enduring E target by the same deadline.

### L2-24 · Rejoin at a third hill neither child currently occupies
- **Mechanism:** Seek a new shared solution that meets both amended floors instead of averaging or selecting a current child. Merge only with a feasible move from the current pair and an ordinary-feedback test of the resulting shared updater.
- **Novelty vs nearest prior art:** [Personalized Soups][soups] combines aligned models and [GLAM][glam] merges groups. The differentiator is that old child interpolation can be infeasible while a newly synthesized shared write and a legal transition exist.
- **Cheapest first test:** Enumerate a tiny nonlinear policy where child interpolation crosses a bad region but a third quantized delta works. Compare exact joint refit, straight merge and distillation from both children.
- **Old-task retention:** Test old service at transition points and each former child's valid corrections after the new shared skill goes live.
- **Beat the Stack on revisions:** Pay for one new write, then prove D/E need fewer updates than keeping or regenerating both children; ties against joint refit do not advance.

### L2-25 · Give a rejoin back its right to refuse
- **Mechanism:** A shared skill can rejoin for ordinary use but decline a specific amendment class when the available feedback cannot distinguish scope; use a pre-action query rather than accepting a correction across both hills.
- **Novelty vs nearest prior art:** [MiCRo][micro] routes contextual preferences and [MEND][mend] edits locally. The proposed rejoin changes **which future feedback may write**, not whether current serving is personalized; selective classification is a required control.
- **Cheapest first test:** Two currently aligned policies disagree only about edits received through an ambiguous source. Compare merge-with-query, merge-and-learn, and a static sidecar rule at the same question budget.
- **Old-task retention:** Check routine requests in both cohorts after ambiguous feedback and after a legitimate scoped correction.
- **Beat the Stack on revisions:** Share normal serving cheaply through E while making fewer unscoped changes than the always-distill library and paying fewer queries than blanket abstention.

### L2-26 · Pay to keep the next split possible
- **Mechanism:** Among two equally good rejoin writes choose the one with a cheaper *verified pair of later split moves* under the fixed write interface. No later child is stored; the open directions must remain useful after an unrelated revision.
- **Novelty vs nearest prior art:** [OML][oml] learns representations that support future updates, and [GLAM][glam] groups adapters. Unlike the ledger's failed readiness predictor, this uses explicit held-out interventions and checks the actual cost to split again, not a proxy for capacity.
- **Cheapest first test:** In a finite low-rank space, enumerate rejoin ties that differ on allowed future paths; follow with an unrelated E and test whether the two paths survive. Compare equal spare rank, meta-initialization, and no rejoin.
- **Old-task retention:** Include low-frequency original behaviors dependent on the open port and check them after either future split.
- **Beat the Stack on revisions:** Yield lower cumulative write cost over two split–rejoin cycles than independent regenerated adapters, at matched current behavior and revisability; charge any retained structure.

## Ranked deeper questions

1. **Can a Learner tell two hills from noisy feedback on one hill?** Find the fewest common comparisons that can rule out a shared write under uncertainty *and* certify that the children will be callable before action (L2-01–L2-08). If a continuous shared adapter or a same-budget mixture wins, keep sharing.
2. **Can we justify forking learning without serving two answers?** Require an intervention that separates the future edits two users would accept while their current actions coincide. Compare the fork against a single learned updater, an equal-byte symbolic sidecar and the full Stack over repeated corrections (L2-10–L2-17).
3. **When do the hills really merge?** Distinguish real convergence from a temporary disappearance of one cohort or agreement on current answers. Ask whether it is cheaper to rejoin serving and keep amendment routes than to rejoin both or retain both children (L2-18–L2-26).
4. **Does proof-gated growth pay for the proof?** Measure cumulative feedback, peak bytes, proof work, and distillation across multiple splits and reversals. If the strongest static-writer + distillation + routed-library Stack matches retention and revision cost, none of the certificate machinery earns its place.

[triage]: https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md#L470
[ledger]: https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md
[t2l]: https://arxiv.org/abs/2506.06105
[dnd]: https://arxiv.org/abs/2506.16406
[opcd]: https://arxiv.org/abs/2602.12275
[arrow]: https://arxiv.org/abs/2405.11157
[maxmin]: https://arxiv.org/abs/2402.08925
[prlhf]: https://arxiv.org/abs/2402.05133
[vpl]: https://arxiv.org/abs/2408.10075
[micro]: https://arxiv.org/abs/2505.24846
[soups]: https://arxiv.org/abs/2310.11564
[id]: https://arxiv.org/abs/2203.07475
[mgda]: https://arxiv.org/abs/1810.04650
[pcgrad]: https://arxiv.org/abs/2001.06782
[color]: https://arxiv.org/abs/2509.16959
[den]: https://arxiv.org/abs/1708.01547
[sema]: https://arxiv.org/abs/2403.18886
[dpm]: https://arxiv.org/abs/2001.00689
[dimoe]: https://arxiv.org/abs/2605.07494
[cdsp]: https://arxiv.org/abs/2512.20291
[olora]: https://arxiv.org/abs/2310.14152
[inflora]: https://arxiv.org/abs/2404.00228
[duet]: https://arxiv.org/abs/2611.29269
[mend]: https://arxiv.org/abs/2110.11309
[opt]: https://arxiv.org/abs/1606.04474
[oml]: https://arxiv.org/abs/1905.12588
[acl]: https://arxiv.org/abs/2312.00276
[glam]: https://arxiv.org/abs/2509.13211
