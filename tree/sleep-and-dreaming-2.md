# Sleep and Dreaming 2: Commuting-Square Sleep Replay

Child of [root-sleep-and-dreaming.md](root-sleep-and-dreaming.md) (depth 1) · 26 cards · 4 ranked deeper questions · Ideas only; no GPU or experiments run

**Why this node exists.** The [review of PR #333, row 451][triage], gives two cards score 3:

1. **SD01 · Replay a square, not four worlds.** Fit two local rule edits from wake data and rehearse their two orders under coupled exogenous events. Keep the relation between the outcomes, not just the episodes. The result has to help a later learner. The review compares this to the ledger's write-skew line, but an order effect and a joint invariant violation that occurs in *both* orders are different labels.
2. **SD20 · Sleep with the next shift hidden.** Make a compact, irreversible commitment before seeing which old setting will return; then specialize. One commitment must make different settings cheaply recoverable. The reveal is a deadline and an information boundary, not a new method by itself.

**Thesis.** A compact learner may need to remember *where two changes may be exchanged*, and *where exchanging them would break something*, more than it needs to remember either complete world. Hidden return makes this a testable storage claim: can those relations buy back behavior under the same bytes and time when the returning setting wasn't known at compression time? An offline comparison can reveal consequences of an assumed world rule, not identify that rule from missing wake evidence.

## Shared contract and controls

- **Fixture and semantics.** Start with a finite dispatch grammar. Edit A changes how a request reserves stock; B changes when a queued request expires. In different states the edits commute, fail to commute, or have one illegal order. Include a case where both orders agree but break an old obligation and one where the final stocks agree but the order of customer-visible acknowledgments matters. A square is based on an initial state and specified events: the paths are A then B and B then A, with declared opportunities for reads/actions between edits. Record applicability, observable behavior (including deadlines), and any coupling assumptions separately. Add at least one rare old dialect and a subsequent change C. Split wake fitting, certificate fitting, and evaluation by scenario family; a known-law fixture demonstrates only separation, then refit the rules from wake traces with misspecification and decoys. Use simulator truth only to score.
- **Square controls (S).** Compare parent SD01, separate replay of all four world variants, equal-rollout Dyna-style world-model replay, single-order replay, and a flat learner given the *same* transitions and order/legality labels without the proposed structure. Charge fitting, both paths, rejected rollouts, symbolic checks, and retained bits. Give symbolic comparators the same fitted specs, not the ground truth. Expect no advantage from the square when order is immaterial or exact checking is already cheaper. Compare expected outcome laws separately from same-event counterfactual agreement; same PRNG seed alone does not ensure the same events.
- **Hidden-return controls (H).** On each run seal one code before any return cue; remove old logs, uncharged decoder state, old teachers, and the ability to change that code. A shared decoder/prior is allowed and charged if learned. After the cue, allow only a fixed allocation of scratch bits, observations, and computation. Fork the *same* commitment into every candidate awakening for evaluation, never pooling results into the committed learner. Compare parent SD20, commit after reveal (clairvoyant reference), no reveal, equal-compute generative replay of all settings, an equal-byte mixture of summaries, an exact task-ID router (charge its store), and a finite optimum over all encoders/decoders where feasible. Include an intentionally impossible bit/deadline cell and matched-budget ambiguous cues. Reveal is a normal observation except in the named oracles.
- **Retention and gates.** For every test, score ordinary old tasks and the card's specific hard slice before sleep, immediately after the normal interface returns, and after C; score both edit orders and all returning settings where applicable. Report worst old family as well as averages, time/examples to recover, solve rate by deadline, and new learning at matched old retention. An arm that abstains always does not pass. In A and C require a subsequent task or change to benefit, not just higher order-label accuracy. In C stack the strongest S and H controls at the same retained bits, evidence, peak working memory and computation; following the [ledger][ledger], no credit for a tie, save/restore alone, an outcome baked into the fixture, or quartet reweighting alone. **Primitive** means a candidate reusable object or operation, not a priority claim; **improvement** means a better use or test of an existing method and needs a large measured gain to advance.

**Literature check.** Hugging Face paper search surfaced executable dreaming, model patching, and recent rehearsal work; web discovery and arXiv abstracts were used to check older and cross-field comparators. [Dream Rehearsal][dream] already makes imagined old-task trajectories useful for continual model-based RL, and [DiCode][dicode] and [PatchWorld][patchworld] already manipulate executable world models. [Servois][servois] and [differencing abstractions][diff] already synthesize or verify commutativity conditions; [data-centric DPOR][read] already reduces equivalent schedules according to their reads. [Many-decoder rate–distortion][many] already treats an encoder that does not know which side information a decoder receives. The narrow targets here are downstream **learning** from relations between fitted edits and **bounded behavioral readaptation** from one code, not new commutativity checking or source coding in general.

## A · SD01: What does the square teach?

### SD2-01 · Export the guard, not the bitmap — PRIMITIVE
- **Mechanism:** Distill a square into a three-way guard over observable state: reorder, preserve order, or unknown. Export the smallest known counterexample to each attempted simplification. A successor uses the guard to decide where two already-learned policies can share a continuation.
- **Novelty vs nearest prior art:** [Servois][servois] already synthesizes commutativity conditions from method definitions. The candidate primitive is a learned, reusable guard at a *policy* interface; its claim is transfer between related fitted worlds, not superior symbolic inference on a fixed one.
- **Cheapest first test:** In S, fit on 2–4 stock units and hold out sizes 5–6 with the same occupancy-boundary relation. Give the exact checker its fitted program at the same online budget; compare a state-indexed truth table, a flat order classifier, and exact rechecking. Retrain a new dispatch objective from limited examples.
- **Old-task retention:** Check ordinary old orders and full-capacity ones, including the state next to each learned guard boundary.

### SD2-02 · Commute for a named reader — PRIMITIVE
- **Mechanism:** Store a certificate scoped to a reader, its legal read times, and its decision horizon. Two schedules can share teaching examples for the stock reconciler yet stay distinct for the acknowledgment reader. Attach the first decision-changing read when the certificate fails.
- **Novelty vs nearest prior art:** [Data-centric DPOR][read] defines equivalence via reads-from. The candidate object is a reader-indexed transfer certificate consumed during policy training, not reduction based on what a reader observes.
- **Cheapest first test:** Use equal stock endpoints with different mid-transition receipts. In S compare endpoint equality, exact observer-conditioned exploration, and ordinary per-reader distillation; introduce a new reader with the same observation interface but a different decision objective.
- **Old-task retention:** Test both old readers while requests are in flight, not just when queues have drained.

### SD2-03 · Attach a lesson to all admissible couplings — PRIMITIVE
- **Mechanism:** Keep an interval for paired order disagreement over admissible event couplings; carry a witness coupling for each bound. Expose a same-event invariance to training only when the bound licenses it. Otherwise use marginal predictions or keep the two alternatives.
- **Novelty vs nearest prior art:** [Gumbel-Max SCMs][gumbel] specify a counterfactual coupling, and [probabilistic product programs][couple] already use couplings in proofs. The proposed reusable object is a coupling-sensitivity interval that governs which cross-order policy targets survive compression.
- **Cheapest first test:** Fit binary stock-event models with identical observed marginals but opposite paired disagreements. In S compare a chosen Gumbel coupling, independent draws, and robust planning over the whole fitted model set; change the payoff on repeat failures and score selective transfer.
- **Old-task retention:** Preserve both old retry behavior with truly shared hazards and ordinary dispatch behavior where only the marginals matter.

### SD2-04 · Do not let a branch shift the noise tape — IMPROVEMENT
- **Mechanism:** Key noise to semantic event identities and mark an event absent if the alternate path never calls it. Test whether this fixes false order lessons without treating newly created events as matched ones.
- **Novelty vs nearest prior art:** [Event-keyed common random numbers][rng] already solve draw-index drift in branching simulators. This is an improvement/control: measure whether that correction materially improves *later policy acquisition* from SD01, not a new random-number scheme.
- **Cheapest first test:** In S let A insert an extra expiry draw before an unchanged delivery draw. Compare global seed reuse, independent seeds, and explicit per-event tapes; add a genuine order effect so making everything commute fails.
- **Old-task retention:** Score old delivery timing distributions and old timeout responses with and without the extra draw.

### SD2-05 · Store the third edit that breaks a swap — PRIMITIVE
- **Mechanism:** A swap claim may travel through a third edit C only with a certificate on the states it can reach after C. When that fails, export the shortest C-prefix that changes the validity of the swap as a reusable blocker. Base-state pairwise checks do not authorize arbitrary permutations.
- **Novelty vs nearest prior art:** [Servois][servois] already lets commutativity depend on state. The candidate primitive is to retain the *prefix that reaches a state where the guard changes* as supervision transferable to later schedule learning, rather than recomputing independence only to prune search.
- **Cheapest first test:** Add a priority rule C that enables a read after expiry, making A and B commute only before C. Compare all six permutations flat, exact DPOR on the fitted program, and base-state pair checks in S. Add a held-out C variant that enables the same read by a new trigger.
- **Old-task retention:** Check A-only, B-only and A+B tasks without C as well as legacy priority jobs where C ought not to block a reorder.

### SD2-06 · Learn oriented prerequisites, not just “conflict” — PRIMITIVE
- **Mechanism:** Export a directed legality rule from a square with one missing path, plus the earliest observation that decides its direction. Use the rule to teach scheduling of an unseen third edit without declaring the forbidden path an observed failure.
- **Novelty vs nearest prior art:** [Servois][servois] extends its method to left/right movers, and [categorical patch theory][patch] formalizes coinitial patches and merges. The reusable teaching object is a state-conditional prerequisite with an observation deadline for the successor learner.
- **Cheapest first test:** Cancellation before reservation is illegal for pending requests, valid for pre-reserved requests, and unresolved for an observation alias. In S compare symbolic precondition checks, an undirected conflict bit, and a precedence DAG at equal memory; insert an unfamiliar intermediate edit.
- **Old-task retention:** Verify that old pre-reserved requests can still cancel immediately and pending requests never lose the lawful cancel path.

### SD2-07 · Close an unequal square with an explicit repair — PRIMITIVE
- **Mechanism:** Where A→B and B→A diverge, search for bounded extensions on either path that restore the declared behavior without erasing the edits' intended effects. Store the extensions with a scope predicate, not a “commutes” label; no repair is allowed to undo an emitted acknowledgment.
- **Novelty vs nearest prior art:** [A Categorical Theory of Patches][patch] already uses pushouts for merging patches. The candidate operation learns an executable, consumer-constrained completion for *already diverged* fitted paths, with genuine repair cost and an infeasible case; an exact patch merge is a required baseline.
- **Cheapest first test:** In S use reservations repairable by refreshing a stale token and variants with an irreversible missed deadline. Compare replanning, patch merge followed by the same replanner, and independent repair demonstrations on new queue lengths.
- **Old-task retention:** Check old rollback-free workflows and old already-acknowledged orders, where a seemingly successful repair can double-book.

### SD2-08 · Carry a square across a settings boundary — PRIMITIVE
- **Mechanism:** Record which fitted mechanisms and observation maps justify a square, then transport it to another setting only after checking the needed invariances. Teach the successor to distinguish a renamed field from a changed dependency, rather than reusing whichever certificate has the closest embedding.
- **Novelty vs nearest prior art:** [Causal transportability][transport] already derives when causal effects can move across populations; [causal abstraction][causal] formalizes correspondence of mechanism transformations. The candidate object is a portable two-order lesson with separately checkable scope for each edge and readout.
- **Cheapest first test:** In S transfer from two depots to a third with relabeled bins; give a fourth a hidden extra limit. Compare exact transport on supplied diagrams, CoDA-style local composition, and rerunning all orders from limited target observations.
- **Old-task retention:** Keep depot-specific old limits as well as unchanged behavior in depots that share the source rule.

### SD2-09 · Save the suffix that refutes equality — PRIMITIVE
- **Mechanism:** For a square whose immediate results match, retain a shortest lawful continuation that makes the histories observably distinct. Use the suffix as training supervision on earlier choices, not as an observation the learner will have at decision time.
- **Novelty vs nearest prior art:** [Differencing abstractions][diff] verify commutativity by focusing on order-dependent differences. The candidate object is an executable *delayed distinguishing suffix* whose adaptation value is scored on new goals. Finding a counterexample by itself is prior art.
- **Cheapest first test:** Separate two equal-stock paths only when a refund request arrives two steps later. In S compare full suffix enumeration, hard-example mining, and flat imitation with the very same suffixes. Hold out refund lengths and prefix combinations.
- **Old-task retention:** Check ordinary stock jobs and older refund behaviors where the same suffix should produce no warning.

### SD2-10 · Teach the invariant and the swap as separate targets — IMPROVEMENT
- **Mechanism:** Factor the teacher's output into applicability, equality of path observables, and satisfaction of an old obligation. Never infer safety from equality or noncommutation from failure.
- **Novelty vs nearest prior art:** [Differencing abstractions][diff] already track differences rather than correctness of a business invariant; the [reviewer's write-skew line][triage] covers jointly unsafe edits. This is an improvement to teaching targets, not a new write-skew object or quartet loss.
- **Cheapest first test:** In S cross commuting/noncommuting with both-order-safe/both-order-unsafe cases and add one legal-but-unsafe order. Compare an exact invariant checker plus flat labeled replay with the same budget; a gain must carry over to a new invariant consumer.
- **Old-task retention:** Test the old invariant on both edit orders, even on the slice where their endpoints agree.

## B · SD20: What must survive before the reveal?

### SD2-11 · Encode a continuation, not a dialect — PRIMITIVE
- **Mechanism:** Compress settings into classes of interchangeable *decision continuations*. Put the distinction back only when the wake cue and a small decoder suffice to recover it. A codeword may collapse two distinct histories if their legal actions and deadlines agree.
- **Novelty vs nearest prior art:** [Many-decoder rate–distortion][many] gives the appropriate side-information baseline. The candidate object is a compact executable code judged by closed-loop decisions after the cue, rather than source reconstruction; compare a codec optimized on that same decision loss.
- **Cheapest first test:** In H exhaustively encode three dialects with redundant aliases and sparse deadline exceptions. Compare an exact task-loss code and reconstruction code; then test generalization when the utterance vocabulary expands but the continuations stay fixed.
- **Old-task retention:** Keep rare dialect exceptions and common old actions that aliases must not split incorrectly.

### SD2-12 · Commit an adaptation program rather than a warm start — PRIMITIVE
- **Mechanism:** Store a tiny executable program that consumes one to three legal return observations and constructs only the needed policy fragments. It cannot refit the carrier; unknown fragments must be learned from the wake budget or left unknown.
- **Novelty vs nearest prior art:** [MAML][maml] trains parameters for rapid gradient adaptation, while [offline recurrence][rec] consolidates context into fast weights. The candidate carrier is a budgeted program that constructs fragments in response to previously unknown evidence, not a larger initialization or saved task head.
- **Cheapest first test:** In H commit to a program for policy tables where a cue reveals an unknown ordering of labels. Compare a gradient warm start, compressed hypernetwork, exact program enumeration, and direct per-dialect tables; test an unseen cue combination.
- **Old-task retention:** Score all old dialects, with special attention to rare commands needing more than one cue.

### SD2-13 · Refine only when the second cue arrives — PRIMITIVE
- **Mechanism:** Design a frozen carrier with two executable reads. The first produces a lawful action before the second cue; the second specializes the policy without invalidating obligations created by the first. Optimize both decision times jointly.
- **Novelty vs nearest prior art:** [Successive refinement with side information][successive] already handles multiple reconstructions at successive stages. The candidate primitive is a decision-refinement operator whose first action can alter obligations and thus the feasible second response, not successive decoding alone.
- **Cheapest first test:** In H put a reservation deadline between a noisy depot cue and a later exact tool reply. Compare a two-stage source code plus an exact small POMDP planner against joint training, with equal scratch memory; include a first action that makes a later alternative impossible.
- **Old-task retention:** Score both old early decisions and their later completion, including jobs that never receive the second cue.

### SD2-14 · Rebind a bad first guess without rebuilding the policy — PRIMITIVE
- **Mechanism:** Separate the cue-dependent binding of an in-flight continuation from the observation-independent work it has already performed. A delayed disambiguator can rebind only if the carried record of actual prior actions admits the new continuation.
- **Novelty vs nearest prior art:** [PEARL][pearl] already updates a latent task posterior separately from control. The candidate operation is a certified rebinding of a partially executed policy, with explicit irreversibility tests and no claim that restoring weights restores the environment.
- **Cheapest first test:** In H occasionally misroute a reservation with a misleading first cue and correct it before shipping. Compare PEARL-style filtering plus replanning, restoring the pre-cue policy plus replaying observed actions, and carrying the whole prefix; price all prior actions.
- **Old-task retention:** Include routine old jobs whose cues never flip and cases whose irreversible step forbids rebinding.

### SD2-15 · Keep a shared observation budget and spend on the next useful cue — IMPROVEMENT
- **Mechanism:** Given a frozen code, rank available observations by the expected reduction in *by-deadline* decision regret among the settings that code can still recover. Charge the observation even if it does not distinguish settings.
- **Novelty vs nearest prior art:** [VariBAD][varibad] already trades off information gathering and return in Bayes-adaptive RL. This is an improvement/control for H: assess whether evaluating the code's recoverable decisions changes query allocation enough to matter against exact Bayes-adaptive planning.
- **Cheapest first test:** In H offer a cheap cue that resolves a costly action and a more diagnostic cue that distinguishes two behaviorally equivalent settings. Compare entropy reduction, fixed cue order, and Bayes-optimal probing at matched costs and evidence.
- **Old-task retention:** Test the old tasks that need no question and the old rare exceptions needing a cue under a tight deadline.

### SD2-16 · Store contrasts in dynamics, not full policies — PRIMITIVE
- **Mechanism:** Encode a small bank of transition differences among old settings. Let a reveal identify which combinations to instantiate; require the representation to support new reward objectives over the reconstructed dynamics, not merely recover the old action.
- **Novelty vs nearest prior art:** [Successor features][sf] separate dynamics from rewards for transfer with fixed dynamics; [CoDA][coda] exploits local factorizations. The candidate carrier decodes **changes in dynamics** under the reveal and is tested on new rewards, against an ordinary equal-bit factored world model.
- **Cheapest first test:** In H vary expiry and refill transitions independently, then reveal one ordinary return observation before giving a new stock-cost goal. Compare equal-bit transition tables, a tensor-factor model, and successor-feature transfer; include nonfactorable dynamics.
- **Old-task retention:** Check original rewards for each setting, especially the old refill exception outside the shared factors.

### SD2-17 · Leave two return ports live at once — PRIMITIVE
- **Mechanism:** Decode two settings into short-lived, disjoint scratch views of a single frozen carrier. Interleaved requests must preserve each view's outstanding obligations without providing the learner oracle routing labels.
- **Novelty vs nearest prior art:** [Online mixtures of tasks][mixture] already infer latent task assignments, and [PackNet][packnet] packs task-specific subnetworks. The candidate primitive is a carrier interface for simultaneous, independently cue-conditioned working views under a shared peak limit, not a new mixture or masking scheme.
- **Cheapest first test:** In H interleave two dialects whose early commands overlap and later callbacks require different actions. Compare a charged routed mixture, equal-bit packed heads, and independent decoders with the same cue history; vary the delay and view lifetime.
- **Old-task retention:** Measure single-setting jobs and mixed old in-flight jobs, including a rare task when both scratch views are occupied.

### SD2-18 · Optimize the worst recoverable slice, not the most likely return — IMPROVEMENT
- **Mechanism:** Pick the pre-reveal code against the maximum deadline regret on supported returning settings. Report the whole expected/worst-case frontier and let a code explicitly fail on a predeclared impossible slice.
- **Novelty vs nearest prior art:** [Many-decoder rate–distortion][many] already constrains several decoders' distortions. This is an improvement to hidden-return allocation: the loss is downstream bounded adaptation, and any gain must exceed a minimax codec with the same behavioral distortion.
- **Cheapest first test:** In H vary how rarely the third dialect returns and enumerate feasible codebooks at small budgets. Compare expectation-weighted replay, equal per-setting bytes, and exact minimax code; test a shifted return distribution.
- **Old-task retention:** Score rare and common dialects separately; don't pay for the rare improvement by silently dropping old common deadlines.

### SD2-19 · Preserve the ability to learn a distinction without preserving its answer — PRIMITIVE
- **Mechanism:** Keep an executable feature and update target for a distinction that wake evidence can relearn cheaply, and spend persistent bits on distinctions no admissible cue can reconstruct. The representation must account for the time and samples needed to turn a feature into a useful decision.
- **Novelty vs nearest prior art:** [MAML][maml] makes a learner easy to fine-tune, and [context channel capacity][capacity] treats finite memory and conditioning in CL. The candidate carrier explicitly splits surviving learnable interfaces from irrecoverable answers, not ordinary pruning or a warm start.
- **Cheapest first test:** In H make one dialect rule observable from two wake examples and a second rule unidentifiable until after the deadline. Compare compressed heads, a meta-learned initialization, and exact task-loss coding with the same examples. Swap which rule is learnable between task families.
- **Old-task retention:** Check both old cue-identifiable commands and old commands requiring a preserved bit before any label arrives.

### SD2-20 · Measure where recovery is impossible — IMPROVEMENT
- **Mechanism:** Enumerate pairs of wake histories and return prefixes that require different actions by the deadline. If two such cases can give the decoder the same cue and state, they cannot share a codeword for zero error; use an exact finite confusability graph as a capacity control.
- **Novelty vs nearest prior art:** [Many-decoder coding][many] already models uncertain side information, and [context channel capacity][capacity] explicitly asks what information a continual learner needs. This is a falsification tool, not a novel bound or a proposed learning mechanism. Use exact coloring only where the induced pairwise constraints and decoder class make it exact; otherwise treat it as a lower bound.
- **Cheapest first test:** In H enumerate four dialect histories with erased or misleading cues. Compare the lower bound to exhaustive joint encoder/decoder search and the measured recovery frontier, including the task-ID oracle that changes the information constraint.
- **Old-task retention:** Report actual per-dialect old behavior at one bit below, at, and above the feasibility boundary; do not infer retention from the bound.

## C · Combine the two lines only if their interaction pays

### SD2-21 · Commit a basis of exceptions to reordering — PRIMITIVE
- **Mechanism:** Commit generators for old settings plus a basis of state-scoped order exceptions. After the cue, assemble a setting from generators, using exceptions to recover only the order distinctions needed by its policy. Different ordered words with the same behavior may share bytes; a conflict class cannot be merged merely because it was rare.
- **Novelty vs nearest prior art:** [Data-centric DPOR][read] already quotients schedules by read equivalence and [patch theory][patch] composes patches. The candidate carrier uses exceptions to compress *across unknown return settings*, and must beat an equal-bit symbolic trace quotient followed by behavioral decoding.
- **Cheapest first test:** In S+H generate four dialect schedules from three edits, with just one state-scoped conflict. Compare generic compression of the exact quotient, a factorized world model plus an exception table, and the stacked parents. Hold out a legal schedule and use a dense-conflict negative.
- **Old-task retention:** Verify each source dialect, both orders, and the rare conflict state under its ordinary wake cue.

### SD2-22 · Let the first observable divergence decode the continuation — PRIMITIVE
- **Mechanism:** Before reveal, compile a partial policy shared by two edit orders up to the first lawful read that can distinguish them; at that read, specialize a fixed-budget suffix decoder. If no distinguishing read arrives by the decision deadline, keep only jointly lawful actions or abstain.
- **Novelty vs nearest prior art:** [Data-centric DPOR][read] distinguishes schedules by their reads and [PEARL][pearl] specializes on evidence. The proposed operation uses the *same* semantic boundary as both a square witness and an executable read point in a frozen carrier, rather than detecting a setting then switching to a separately stored policy.
- **Cheapest first test:** In S+H hold back the expiry receipt and vary whether it precedes shipping. Compare observer reduction plus a Bayes-adaptive controller, pinned policies, and a full contingent plan compiler; test a held-out sequence of intermediate requests.
- **Old-task retention:** Score old jobs that can finish on the shared prefix, those needing late specialization, and those whose legacy observations alias.

### SD2-23 · Share the witness, not the answer to it — PRIMITIVE
- **Mechanism:** Compile one reusable lawful witness query for squares across several old settings. Commit the query and a small action-continuation map, but not its answer; after reveal, use the ordinary result to resolve which residual order constraint applies. Charge queries and require answers that really arrive before action.
- **Novelty vs nearest prior art:** [Causal Confusion][confusion] already uses targeted interventions to resolve imitation ambiguity, and [data-centric DPOR][read] distinguishes schedules by their reads. The candidate object is a reusable square witness that reduces storage across possible returns because the same query decodes different old constraints.
- **Cheapest first test:** In S+H use one inventory inspection whose reply disambiguates order constraints in two dialects, and a third where it cannot. Compare exact information-gain queries plus separately compressed heads and no-query codecs at the same costs.
- **Old-task retention:** Preserve old no-inspection workflows and old dialects where the inspection is lawful but nondiagnostic.

### SD2-24 · Precompute a certificate with a hole instead of a table of answers — PRIMITIVE
- **Mechanism:** Before reveal, compile one relational program for an edit pair with a typed slot for a return-specific rule parameter. After reveal fill that slot and check the remaining obligation; do not finish a certificate if the cue identifies only a family containing incompatible values.
- **Novelty vs nearest prior art:** [Servois][servois] already synthesizes symbolic guards, including parameter-dependent conditions. The candidate carrier uses a partially evaluated guard to accelerate later policy updates across settings at equal *peak* storage and required wake compute, with ordinary symbolic partial evaluation as a control.
- **Cheapest first test:** In S+H vary an expiry threshold across dialects and add a hidden rule interaction not expressible by the slot. Compare precomputed per-setting guards, the generic solver after reveal, and off-the-shelf partial evaluation plus flat replay. Evaluate post-reveal learning under a strict deadline.
- **Old-task retention:** Check old threshold equalities and the unsupported dialect where the carrier must not assert a wrong swap.

### SD2-25 · Keep an unresolved square live across two blind nights — PRIMITIVE
- **Mechanism:** Preserve a compact record of exactly which new observation could refute a square claim. If the first return is uninformative, a second blind commitment must carry the unresolved branch too; only informative wake evidence can discharge it. Other old policies may update between nights.
- **Novelty vs nearest prior art:** [Offline recurrence][rec] consolidates contexts across offline phases; [counterfactual world models][cfwm] explain why factual transitions alone do not identify paired counterfactuals. The proposed carrier is a persistent, refutable order relation that survives repeated compression without treating simulation as new evidence.
- **Cheapest first test:** In S+H make the first return compatible with two square models and the second sometimes separating. Compare version-space tracking plus replay, last-night recency, and preserving every raw candidate. Include an uninformative second return; certificate coverage should not rise there.
- **Old-task retention:** Check after both nights, including the dialect that never returns and an old case for which the unresolved square changes nothing.

### SD2-26 · Swap the implementation without swapping the relation — IMPROVEMENT
- **Mechanism:** Cross two orthogonal transfers: hold the edit implementation fixed while changing its order relation, and preserve the order relation while replacing the implementation. Probe whether the compressed learner follows the learned relation rather than familiar edit identifiers or surface cues.
- **Novelty vs nearest prior art:** [Causal abstraction][causal] already checks mechanism-level alignment and [CoDA][coda] exploits local causal structure for recombination. This is a falsification design for the merged claim, not a candidate abstraction or another quartet objective.
- **Cheapest first test:** In S+H permute tool names and rule parameterizations independently of where capacity makes the edits conflict. Compare a structured carrier, its shuffled-square ablation, and flat training with identical supervision; match cue predictiveness and bit budgets.
- **Old-task retention:** Test the unrenamed old interfaces and the renamed versions where order behavior really is preserved. Score false transfer on the same-name, changed-relation cells separately.

## Ranked deeper questions

1. **Does remembering a square buy any later learning once the flat learner gets the same evidence?** Start with SD2-01/21/26. Cross relation-preserving and relation-changing transfers, then measure old and new behavior under S+H. If the fitted-model checker, ordinary compression, and flat supervision tie, keep SD01 as an analysis tool, not a carrier.
2. **When is a commuting-swap claim identified rather than an artifact of the dream?** Use SD2-03/04/08/25 to separate exogenous coupling, observable equivalence, legality, and model uncertainty. Seek a cheap admissible observation that shrinks the identification gap; if none exists, measure how much useful behavior survives honest uncertainty.
3. **Which bits must be committed, and which can wait for the world to answer?** Use SD2-11/19/20/23. Compare exact finite task-loss coding with real closed-loop latency and scratch constraints. Separate information no cue can supply from information the learner can compute but not before a deadline.
4. **Can a relation survive repeated specialization without harming an old in-flight decision?** Use SD2-02/05/13/22/25. Vary which consumer observes the seam and which shift returns next. Ask whether one scoped object composes across nights without rechecking every schedule, and where a third edit or delayed read makes that impossible.

[triage]: https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md#L451
[ledger]: https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md
[dream]: https://arxiv.org/abs/2607.19749
[dicode]: https://arxiv.org/abs/2602.08194
[patchworld]: https://arxiv.org/abs/2605.30880
[servois]: https://arxiv.org/abs/1802.08748
[diff]: https://arxiv.org/abs/2004.08450
[read]: https://arxiv.org/abs/1610.01188
[patch]: https://arxiv.org/abs/1311.3903
[gumbel]: https://arxiv.org/abs/1905.05824
[couple]: https://arxiv.org/abs/1607.03455
[rng]: https://arxiv.org/abs/2603.11084
[transport]: https://arxiv.org/abs/1503.01603
[causal]: https://arxiv.org/abs/2301.04709
[coda]: https://arxiv.org/abs/2007.02863
[many]: https://arxiv.org/abs/0901.1705
[successive]: https://arxiv.org/abs/0812.3285
[maml]: https://arxiv.org/abs/1703.03400
[rec]: https://arxiv.org/abs/2605.26099
[pearl]: https://arxiv.org/abs/1903.08254
[varibad]: https://arxiv.org/abs/1910.08348
[sf]: https://arxiv.org/abs/1606.05312
[mixture]: https://arxiv.org/abs/1812.06080
[packnet]: https://arxiv.org/abs/1711.05769
[capacity]: https://arxiv.org/abs/2603.07415
[confusion]: https://arxiv.org/abs/1905.11979
[cfwm]: https://arxiv.org/abs/2611.24778
