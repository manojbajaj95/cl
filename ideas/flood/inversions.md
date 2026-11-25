# Flood: make continual learning's failure modes useful

What if forgetting were an output, interference were an operator, and drift were something you could learn to use rather than suppress? These are 64 raw proposals for models and agents, not novelty verdicts. I screened for obvious repeats against the [ledger and flood triage on PR #6](https://github.com/manojbajaj95/cl/pull/6) and skimmed neighboring floods. **Primitive** means a proposed reusable object or operation; **improvement** means a new use of existing machinery.

First tests are CPU-sized unless noted. Match the relevant resources (updates, bytes, queries or slots), evaluate on held-out examples, and record each old task's pre-stream score alongside its final score; report worst-old as well as average-old so a new win cannot hide a lost skill. Where the environment genuinely revises a contradictory rule, score old tasks under their original conditions and revised ones under the new conditions, without oracle task IDs unless all arms get them. For text-lesson pilots add same-length filler and source-fit entropy-matched no-lesson controls.

## I. Forgetting as a writable channel

### 01. Memory by missing answers — primitive
- **Mechanism:** Train excess associative answers, then encode a task code by saturating selected high-redundancy entries with contradictory labels until they abstain. Downstream modules query the presence or absence of these entries; the remaining entries still answer normally.
- **Why it might be new:** Sparse coding stores active entries; here a selectively destroyed association is readable data, without an explicit mask at inference.
- **Cheapest first test:** Use a NumPy associative net with an XOR of erasure bits as a held-out routing task. Compare equal-byte positive association bits and random erasure; check all pre-stream associations outside the write bank still decode.

### 02. Survivor sketches — primitive
- **Mechanism:** Learn paired representations of old examples, one trained to be easy to overwrite and one robust. Use the surviving stream after a standardized destructive update as a lossy compressor, then train a decoder to recover old labels from it without access to pre-overwrite features.
- **Why it might be new:** Unlike ordinary bottlenecks or robust distillation, the codec's encoding operation is actual subsequent training, not a fixed mask or quantizer.
- **Cheapest first test:** In a two-layer MLP use 20 update batches as the encoder and compare equal-rate PCA and random masking. Test decoded accuracy on unseen old examples from each learned class and accuracy on the overwrite task.

### 03. Relearning as the read head — primitive
- **Mechanism:** Write a skill so a fixed probe gradient step, on a public unlabeled objective, switches that skill on even after it becomes inaccessible at zero steps. Train through the overwrite and probe steps so the dormant information lives in how learning proceeds rather than in the current prediction.
- **Why it might be new:** MAML and savings in relearning are close; the proposed read API is a label-free, skill-selective learning step, not initialization for fitting labeled returns.
- **Cheapest first test:** On cyclic Boolean tasks meta-train an MLP with null-logit matching before the probe step. Compare replay-trained and ordinary MAML learners at equal calls; verify unchanged old tasks without probing and revived old tasks after probing on held-out inputs.

### 04. Teach the forgetting frontier — primitive
- **Mechanism:** Intentionally remove a brittle shortcut and train a boundary decoder to recognize where the loss of that shortcut flips answers. Use the boundary, not the old shortcut or a full checkpoint, as a feature for future tasks that depend on knowing when the shortcut was misleading.
- **Why it might be new:** Counterfactual explanation and concept erasure are close; the product is a reusable detector of the *domain of damage*, not an invariant predictor.
- **Cheapest first test:** Erase a stripe cue from a synthetic image classifier; predict when an unseen shift misleads using the learned boundary versus supervised cue probes. Recheck old shape and texture judgments where their cues remain valid.

### 05. Learn by cutting holes into a manifold — primitive
- **Mechanism:** Represent exceptions by training a denoising model to stop reconstructing small neighborhoods of a previously learned manifold. At inference, run the denoiser and treat failed reconstruction as a negative membership witness; genuine neighboring points should still reconstruct.
- **Why it might be new:** One-class classification models supports; this adds a continual write operation that carves exceptions into the support without learning an extra classifier per exception.
- **Cheapest first test:** Remove disks from a synthetic 2D ring in three waves; compare with equal-parameter anomaly heads and rehearsal. Verify previous holes still reject and old inlier arcs still reconstruct.

### 06. Unlearning as an assay for concept ancestry — primitive
- **Mechanism:** Temporarily unlearn a candidate prerequisite on a disposable model, then see which other skills break on predeclared input perturbations. Store the break pattern as an edge in a prerequisite graph and use it to order future teaching.
- **Why it might be new:** Causal tracing usually intervenes on units or activations. The intervention here is learning-induced removal of a functional capability, with causal predictions about how to teach the next task.
- **Cheapest first test:** On tiny compositional arithmetic, choose the order of a held-out composition's prerequisites from removal effects versus feature similarity and random order. On the deployed model re-run every old operator and composition after the new lesson.

### 07. Discard the exemplar, keep its veto — primitive
- **Mechanism:** Each exemplar leaves behind only a callable counterfactual veto: a compact constraint on which extrapolations that exemplar would have contradicted. When a new skill proposes a broad rule, old vetoes restrict its domain without needing to reconstruct the former examples.
- **Why it might be new:** Support vectors and constraint replay are neighbors; here a forgotten example exports an executable *negative specification* over rules, with a separate rule learner consuming it.
- **Cheapest first test:** Stream clauses for a tiny decision-list synthesizer; compare equal-byte exemplar replay and old-rule freezing on novel extrapolations. Re-evaluate each old clause on fresh satisfying and violating inputs.

### 08. Forgetting under contract — primitive
- **Mechanism:** Let a task provide transformations under which it consents to being wrong internally, provided inverse output transforms repair the error. New tasks can overwrite the shared representation by inducing one allowed transform; a tiny external contract interpreter restores old semantics.
- **Why it might be new:** Equivariant nets enforce a known symmetry from the start; this makes a post-write change of semantics an explicit negotiable interface.
- **Cheapest first test:** Stream games whose actions can be relabeled or reflected; learn permitted transforms from a few anchors versus replay and fixed relabeling. Retest old games through the interpreter plus a non-equivariant old task whose contract forbids remapping.

### 09. Sacrificial prototype skin — improvement
- **Mechanism:** Give a class a durable interior and expendable boundary prototypes, then deliberately overwrite the skin when adjacent classes arrive. Retrain just local interfaces using the old skin's now-wrong predictions to place new joints.
- **Why it might be new:** Prototype rehearsal preserves centroids; the intended artifact here is the *shape of the loss* on edge prototypes, used as supervision for a revised boundary.
- **Cheapest first test:** Stream adjacent moons in 2D; compare nearest-prototype rehearsal and uniform prototype overwrite at equal slots. Evaluate each old class separately on clean cores and near the revised interfaces.

### 10. Mutually destructive dialects as a language — primitive
- **Mechanism:** Train three few-shot prompt dialects, including strings that induce old dialect mistakes selectively. A tiny interpreter learns to compose those induced mistakes to answer new queries, e.g. a pair of predictable flips implements a context-dependent identity.
- **Why it might be new:** Prompt ensembling computes over helpful prompts; this treats controllable, cross-dialect failure as an instruction with composition semantics.
- **Cheapest first test:** Use a two-head transformer on synthetic symbol transduction; test unseen compositions against extra ordinary prompt tokens and shuffled destructive dialects. Retest standalone old dialects before and after learning the interpreter.

### 11. Federated forgetting receipts — primitive
- **Mechanism:** A learner that discards local data sends peers an aggregate distribution of which of their public hypotheses it can no longer distinguish after deletion. Peers use that ambiguity report to assign the next measurements to the sites that still can distinguish those hypotheses.
- **Why it might be new:** Federated active learning shares uncertainty scores; a receipt reports uncertainty *created by a specific deletion*, with a different assignment target than predictive entropy.
- **Cheapest first test:** Simulate four sensors on a switching linear system with overlapping feature losses. Compare current uncertainty and random scheduling at matched queries; test held-out old calibration conditions at every site after several deletion rounds.

### 12. Expiry as a sensor for missing context — primitive
- **Mechanism:** Arrange for duplicate skills to lose different refinements on a fixed schedule. Which ordinary questions begin producing disagreement reveals that a context variable the learner had ignored is now needed; use that pattern to ask one disambiguating question.
- **Why it might be new:** Query-by-committee samples plausible models; this committee is designed to disagree when *specific information expires*, not when posterior samples happen to diverge.
- **Cheapest first test:** Have two policies solve a routing toy before a hidden rule starts changing destinations. Compare equal-query uncertainty sampling and random expiry; retest all original destinations including after awaiting the answer.

### 13. Lossy deletion with signed remainder — primitive
- **Mechanism:** As overlapping recipes are removed from an agent store, keep a sparse signed difference between their abstract input-output effects. Solve for new recipes from those signed remainders plus current recipes whenever the deleted distinction becomes relevant.
- **Why it might be new:** Delta compression keeps an old object reconstructible; this stores only an effect relation and permits any new implementation satisfying it.
- **Cheapest first test:** Evict string transforms from a finite DSL and synthesize equivalent held-out compositions. Compare equal-byte recipe compression and memoized outputs; re-run old primitive and composite calls on new strings.

### 14. Delete capacity to force a rendezvous — improvement
- **Mechanism:** Periodically remove the distinct intermediate representations two skills use for the same subproblem. Force both to go through a shared bottleneck afterward; only accept the pair if the missing feature returns identically for both.
- **Why it might be new:** Feature alignment measures existing agreement; destructive rendezvous creates a situation where sharing must be learned to recover.
- **Cheapest first test:** Use two small regression networks with distinct nuisance cues; compare with soft activation alignment and random pruning. Test old noiseless and nuisance-shifted splits plus transfer to a third relationship.

### 15. Abandon answers; remember answers to contrasts — primitive
- **Mechanism:** After learning an old task, allow its absolute scores to decay but distill only contrasts between query pairs. A new stream supplies a few absolute anchors, which convert surviving comparisons into predictions on both old and new inputs.
- **Why it might be new:** Preference learning already uses pairs; the CL operation deliberately changes the conserved quantity from labels to cross-task relative information, letting a future task re-anchor it.
- **Cheapest first test:** Stream shifted ordinal-regression tasks with shared latent ranks; compare equal-byte score distillation and rank distillation without future re-anchoring. Check old rank and absolute calibration on held-out inputs after each refit.

### 16. Scholarship for the last knower — primitive
- **Mechanism:** Let an agent population lose knowledge unevenly. For each threatened skill, ask the least replaceable remaining solver to teach a dissimilar peer, where replaceability is measured by whether another peer can recover the same answer via a different plan.
- **Why it might be new:** Fleet skill retention and stemmatic reconstruction are neighbors; this operation pairs deliberate diversity of failure with cross-implementation teaching *before* extinction.
- **Cheapest first test:** Simulate three DSL agents with limited operator libraries; compare uniform teaching and trainer chosen by recent success. Test novel compositions and each earlier operator family after repeated library turnovers.

## II. Interference as compute

### 17. Collision as a conjunction gate — primitive
- **Mechanism:** Learn two additive adapters that individually solve standalone tasks but jointly jam a particular hidden unit only on their input overlap. Read the jam with a fixed comparator, then use it to perform a new action without any joint adapter.
- **Why it might be new:** TIES tries to remove sign conflicts; here a trained collision implements an AND over learned predicates and can be composed with other gates.
- **Cheapest first test:** Fit rank-one adapters for two text-free attributes, then test conjunctions including unseen corners of the input space. Compare ordinary adapter sums and an equal-parameter explicit gate; retest both old attributes with their adapters alone and with the new gate present.

### 18. The contradiction register — primitive
- **Mechanism:** Stack incompatible rules in one module and dedicate a register to the residual that cannot satisfy both. Expose that residual to later training as an input feature; the original rules should continue to work where they do not overlap.
- **Why it might be new:** Gradient surgery resolves the conflict before inference. The register gives subsequent skills durable access to structured disagreement instead of cleanly separated experts.
- **Cheapest first test:** Train linear rules that disagree on certain locations, then learn which latent exception is implicated using residuals versus plain expert disagreement or uncertainty. Recheck both old rules in valid regions and on disambiguated overlap.

### 19. Order-sensitive updates as a relation — primitive
- **Mechanism:** Write a relation between A and B by learning small updates whose composition A→B produces a deliberately different behavioral probe signature than B→A. Read that difference on temporary copies; deploy either order for normal task solving only if both preserve released tasks.
- **Why it might be new:** BCH correction and holonomy cards are close; this writes queryable *relations between skills* into prescribed commutator responses, rather than removing or merely accumulating order effects.
- **Cheapest first test:** On a tiny MLP learn a directed relation between symbol transformations; test unseen pairs versus gradient cosine and an equal-byte relation table. Recheck each old transformation after each probe-update order.

### 20. Corrupt to compose — primitive
- **Mechanism:** Have learners A and B exchange the predictions on which the other's update just made them worse, without the original inputs' labels. Train a small composition head to turn those specific error transitions into routing decisions on a third task.
- **Why it might be new:** Stacking consumes contemporaneous expert outputs; this consumes task-induced failure transitions, asking whether “how the other learner broke me” carries unique information.
- **Cheapest first test:** On hidden-mode Boolean tasks compare trained routing using transitions, current logits, and shuffled transitions at equal feature width. Retest the old A and B tasks on held-out examples after the same update stream.

### 21. Write interactions without writing marginals — primitive
- **Mechanism:** Update a network only with quartets whose individual feature marginals and labels cancel but whose joint residual has a task-specific sign. Use the quartets to teach pure cross-feature relations without moving the model's predictions when either variable is unavailable.
- **Why it might be new:** Factorial contrasts are familiar; treating a marginally invisible factorial packet as a write format enables editing a relationship without rewriting either old concept.
- **Cheapest first test:** Add three interaction rules to a tiny embedding model with known singleton skills. Compare ordinary joint examples and gradient projection at matched updates; retest old singleton predictions and previously added interactions on unseen combinations.

### 22. Learned friction between adapters — primitive
- **Mechanism:** Give each adapter one cheap internal stress signal driven by other adapters trying to use the same feature. When two adapters co-activate, their paired stress signals jointly select a small correction, and the correction is trained on only a few overlapping cases.
- **Why it might be new:** Conditional adapters and routing see task inputs; here conflict-induced stress is itself a composable signal passed between parameter edits.
- **Cheapest first test:** Stream symbol transducers with overlapping internal features. Compare a wider adapter router and activation-magnitude control; verify each old transducer alone and mixed with both seen and unseen partners.

### 23. Prediction shifts as messages between lessons — primitive
- **Mechanism:** Run two independently editable prompts on a constrained task and let each receive only the other's task-induced *change* in a small action-probability vector. Optimize text edits so the changes form a shared code for complementarities, then freeze that code before adding another lesson.
- **Why it might be new:** Multi-agent communication often adds free-form or learned messages. The proposed channel is the signed interference a candidate lesson causes, rather than another explicit text field.
- **Cheapest first test:** Search a finite vocabulary of lesson edits for a three-action puzzle; compare equally wide literal message codes and shuffled deltas. Retest earlier lesson combinations from fresh starts after new edits.

### 24. Learn the exceptions by making policies fight — improvement
- **Mechanism:** Instead of minimizing loss on an old replay set, tune a sandbox policy on a new rule specifically until it breaks the widest range of old inputs. Fit a tiny conflict classifier on the observed transitions and use it to seek actual labels only for likely exceptions before updating production.
- **Why it might be new:** Adversarial replay hunts hard inputs; this intervention adversarially writes the new policy so previously hidden old/new semantic conflicts become observable.
- **Cheapest first test:** Stream overlapping rules with sparse exceptions in a table-world; compare margin sampling and ordinary fine-tune-disagreement at equal label budget. Retest all prior normal and exception cases on held-out states.

### 25. KV collision as a join — primitive
- **Mechanism:** Store keys for two streams in one cache so their values cancel only when both streams match a query. Put a trained readout on the near-zero sum to produce an intersection token, with explicit absence examples to distinguish cancellation from no match.
- **Why it might be new:** Retrieval composes results after reads; the proposal uses destructive interference *inside* attention to perform a join.
- **Cheapest first test:** Use a toy softmax-attention layer for evolving relational tables; compare equal-slot separate caches plus an explicit join. Retest historical non-deleted memberships and earlier joins after table additions.

### 26. Deliberately aliased slots with context parity — primitive
- **Mechanism:** Force multiple KV entries to share a key while alternating their value signs across two attention heads. Train later contexts to supply a parity bit that recovers a different mixture, so ambiguity creates a handle for accessing more than one association.
- **Why it might be new:** Hash memories try to resolve collisions by remapping or overprovisioning; this turns a collision plus a contextual parity bit into a new read/write unit.
- **Cheapest first test:** Stream key-value lookups through a two-head transformer at a fixed cache size; compare ordinary hashed slots and equally sized separate heads. Check old task-specific lookups and combined queries after all writes.

### 27. New learning from damaged consensus — primitive
- **Mechanism:** Consolidate only behaviors that survive a tournament in which each task learner tries to spoil the others' held-out agreement using its own training loss. Store the resulting equivalence classes of outputs as shared abstractions, not a consensus model.
- **Why it might be new:** Invariant risk minimization compares environments; the environments here become adversaries in *parameter-write space*, and surviving equivalence classes can be read independently.
- **Cheapest first test:** In a toy causal classification stream, compare write-survival classes to pooled agreement and IRM features on a new intervention. Retest each old environment and the learned abstractions after the next tournament.

### 28. Cross-talk as error bars — improvement
- **Mechanism:** Allow a controlled amount of cross-talk in a population-coded adapter and learn to decode direction, not just magnitude, of cross-talk as uncertainty about future tasks. Use that prediction to decide when the model should request a missing feature rather than guess.
- **Why it might be new:** Ensemble uncertainty uses independent models; controlled collisions between known stores can be tuned to distinguish particular types of uncertainty.
- **Cheapest first test:** Use overlapping low-rank regressions with feature-dependent noise. Compare MC dropout and the same adapters fitted to suppress cross-talk; test old predictions and calibration at matched request budgets.

### 29. Pair lessons to synthesize a safe deadlock — primitive
- **Mechanism:** Represent high-consequence decisions with two intentionally conflicting recipes that independently block each other's default. Only a newly learned witness can break the deadlock, and witnesses can be re-used on other compatible pairs.
- **Why it might be new:** Ordinary arbitration picks a winner; here the stable product of overlap is an explicit *no-action state* that requires evidence of a certain kind to leave.
- **Cheapest first test:** In a simulator with irreversible toy moves, compare deadlock pairs with fixed abstention rules and a resolver classifier at equal supervision. Run old admissible and prohibited pathways with and without witnesses to check retained success and restraint.

### 30. Rewrite the winner into the loser — primitive
- **Mechanism:** When skills clash, train the losing skill on inputs where the winner fails, not where the winner succeeds. Expose only the loser’s correction on those inputs and let future arrivals recursively write against that correction.
- **Why it might be new:** Boosting fits ensemble residuals from a labeled dataset; this turns the displaced skill itself into an addressable residual and defines where subsequent skills attach.
- **Cheapest first test:** Stream four disjoint-plus-overlapping arithmetic domains; compare ordinary residual boosting and prefix-routed specialist adapters at equal parameters. Retest old domains, especially old inputs misrouted by the latest winner.

### 31. Use a disagreement as a variable binding — primitive
- **Mechanism:** Two small programs deliberately output different values when they receive the same unbound symbol. For a new task, find a substitution that makes the outputs agree; remember the resulting binding rather than either candidate answer.
- **Why it might be new:** Logic unification operates on explicit syntax; this performs a behavioral version through clashes between partially learned skills, even when their internal implementations are opaque.
- **Cheapest first test:** Fit two tiny sequence operators implementing different views of a latent symbol mapping. Compare with literal embedding alignment and an explicit unifier at matched calls; retest both old operator suites plus stored bindings after a third operator arrives.

### 32. Interference masks as portable experiments — primitive
- **Mechanism:** Represent a diagnostic as the pair of edits that causes a targeted, reversible disagreement on a disposable replica. Ship the diagnostic, not a proposed fix; another learner runs it to decide locally which of two next lessons would distinguish its current failure.
- **Why it might be new:** Model-edit locality probes check collateral damage; here the damage pattern is deliberately constructed as a transportable experiment and can be useful even when the edits are useless for deployment.
- **Cheapest first test:** Transfer paired probes across seeds of a tiny shortcut learner. Compare with input-only challenge sets and random equal-norm paired edits; check old capabilities on the final production models after following the diagnostic's lesson recommendations.

## III. Drift, optimizer history, and lost plasticity as resources

### 33. Optimizer-state reflexes — primitive
- **Mechanism:** Train the first moment of an optimizer on a stream so that a prescribed sequence of tiny probe gradients produces a task-specific direction before any appreciable change in the loss. Use the direction to pick the next data source, while freezing the predictor during the read.
- **Why it might be new:** SM25 inherits optimizer state to learn faster; this exposes the optimizer as a callable filter for action selection, with the predictor untouched by reads.
- **Cheapest first test:** On alternating logistic tasks, compare learned reflexes to a gradient-history window and fresh moments at matched state bytes. Recheck old classifiers after acting on each reflex for several rounds.

### 34. Fuse weights that burn out on misconceptions — primitive
- **Mechanism:** Give a feature multiple use-dependent learning rates, including a sacrificial one whose learning rate falls irreversibly after enough contradictory updates. Detect that burned-out route and use it to prevent future tasks from relearning the same shortcut through that route.
- **Why it might be new:** Metaplasticity protects memories by making them stiff. This uses selective stiffening as a negative memory of which feature-use pair should not be trained again.
- **Cheapest first test:** Inject a recurring spurious cue into split synthetic tasks. Compare EWC and equal-sparsity pruning; test old valid cues and old exceptions plus how often the shortcut returns.

### 35. Cash out collapse as a basis expansion — primitive
- **Mechanism:** On a training copy, push an old representation until one feature cluster collapses into another. Allocate a single daughter feature to the cluster where this produces complementary prediction errors and train it on the union; the production copy receives the daughter rather than the collapse.
- **Why it might be new:** Net2Net and grow-when-required start from functioning features or current error; here deliberately destroying a distinction proposes where a new feature should go.
- **Cheapest first test:** In a 16-unit ReLU net with a fixed growth budget, compare collapse-driven splits to largest-residual and random splits. Check every old function before and after adding each daughter.

### 36. Skill keys that move with the model — primitive
- **Mechanism:** Define a key as the *response trajectory* of a fixed query to ordinary fine-tuning rather than its current embedding. Train a readout on short trajectories so the appropriate skill can be located by how the query moved, not where it ended.
- **Why it might be new:** Transport methods align static representations across states. A trajectory key can distinguish queries with the same final embedding but different responses along the way.
- **Cheapest first test:** Stream nuisance shifts into an embedding model with two deliberately colliding terminal embeddings. Compare static aligned centroids and endpoint deltas at matched bytes; retest old skill routing after multiple shifts.

### 37. Borrow curvature from the tasks that went rigid — improvement
- **Mechanism:** Identify old features that no longer learn quickly but whose gradients still predict local scaling across new data. Reuse only their normalization statistics to precondition an entirely different trainable block, leaving the rigid features untouched.
- **Why it might be new:** K-FAC and optimizer-state transfer use curvature locally or inherit it wholesale; this decouples a useful preconditioner from the untrainable feature that produced it.
- **Cheapest first test:** Freeze a saturated encoder and train small heads on scaled regressions. Compare its transferred preconditioner with a diagonal Adam warm start and shuffled statistics; retest old heads on untouched old evaluation sets.

### 38. Handoff via deliberate optimizer shock — primitive
- **Mechanism:** On a task switch, perturb second moments in a prescribed subspace for exactly one step. Train a routing module on the resulting transient instability pattern to identify which components should exchange responsibility.
- **Why it might be new:** Warm restarts seek to avoid bad transients; the transient here is an elicited diagnostic with an explicit learned interpretation at each handoff.
- **Cheapest first test:** Simulate a two-expert regressor with abrupt causes changing at different times. Compare learned shock routing to moment resets and equal-cost gradient norm probes; retest old mappings with the new router.

### 39. Optimize for distinguishable failure kinetics — primitive
- **Mechanism:** Train old skills to decay at visibly different *shapes* under a standard stress sequence, while matching their unstressed behavior. Decode shapes to distinguish missing prior knowledge, wrong routing and output calibration when these produce the same initial failure.
- **Why it might be new:** Programmable half-life sets how long something lasts, and learning-primitives W2 fingerprints training data from observed decay. This deliberately programs the shape of damage to distinguish causes of an otherwise identical failure.
- **Cheapest first test:** Plant three failure causes in a tiny MLP and match first-step loss across them. Compare decay signatures with endpoint losses and logit telemetry; check unstressed old tasks plus old tasks recovered by the diagnosed intervention.

### 40. Drift-labelled apprenticeship — primitive
- **Mechanism:** Have a learner predict a teacher's next incremental change on anchors rather than the teacher's labels or exact final state. At deployment use the learned change predictor to adapt from an unlabeled drift cue, and constrain its action to ordinary updates rather than switching teacher versions.
- **Why it might be new:** Trajectory matching and ontogeny distillation see training history; this learns a conditional update from the direction of change, so a student can extrapolate a running drift rather than replay a history.
- **Cheapest first test:** Track tiny teachers fitting drifting linear systems and hold out drift velocities. Compare endpoint distillation and extrapolating logits; check old stationary systems and earlier regimes when they recur.

### 41. Phase-cancel optimizer writes but keep the aftereffects — primitive
- **Mechanism:** Apply two equal and opposite minibatch gradients to a predictor, restoring the parameter vector explicitly afterward. Keep the optimizer's asymmetric state response and train later tasks to use that response to select a learning rate or subspace.
- **Why it might be new:** State-only warm starts and LR schedules as messages are near neighbors; this is a write operation that cancels parameter changes while deliberately leaving a learning policy behind.
- **Cheapest first test:** On a recurrent logistic stream, compare balanced gradient pulses with copying an Adam state and a learned LR scheduler at equal storage. Measure the first updates on returns and check each previously learned mapping with the deployed weights.

### 42. Forget the metric, preserve the ordering — primitive
- **Mechanism:** Let representation distances drift freely across updates as long as a sparse set of triplet orders survives. A new task learns with its own metric and invokes those order constraints only where it uses an older concept.
- **Why it might be new:** Metric learning uses triplets to build one space; this makes partial ordinal geometry a durable skill interface that survives replacement of the metric itself.
- **Cheapest first test:** Sequentially fit incompatible scalings of a small 2D retrieval space. Compare triplet contracts to embedding distillation and independent spaces at matched bytes; rerun old top-k retrieval and old triplets from unseen points.

### 43. Intentional feature retirement creates a moving vocabulary — primitive
- **Mechanism:** Enforce a ban on reusing a feature's old numeric slot after retirement, but ask a decoder to label the concept a new slot initially substitutes for. Track these substitution chains to infer reusable concept correspondences rather than maintaining stable indices.
- **Why it might be new:** Dictionary learning recycles atoms; this treats forced slot loss and subsequent substitution as the measurement of semantic equivalence under adaptation.
- **Cheapest first test:** Train a sparse dictionary on shifting glyphs; compare substitution chains to cosine alignment and a fixed dictionary at equal capacity. Retest old glyph labels and composites via the decoder after multiple retirements.

### 44. Train a switchboard out of gradient deserts — primitive
- **Mechanism:** Use saturation to induce narrow areas in input space in which a designated module cannot update from supervised error. An independent module learns to detect those areas and hands new learning to a corresponding alternative solver, using inability to learn as the routing cue.
- **Why it might be new:** Mixtures of experts route by context or competence; deliberately sculpted *unlearnability* defines where responsibility transfers, even without divergent output predictions.
- **Cheapest first test:** Train two tiny experts on functions whose inputs overlap but whose useful gradients differ. Compare gradient-desert routing with entropy and learned task routing at matched compute; verify held-out old outputs and route choices.

### 45. Run drift in two directions to learn what can be ignored — improvement
- **Mechanism:** Present a reversible domain shift to two learners in opposite temporal order. Keep data-dependent features whose local prediction derivatives agree after accounting for the reversed sign of the shift; don't require their absolute predictions to agree.
- **Why it might be new:** Invariance training seeks static agreement; this uses *equivariance of directional drift* to tell legitimate change from order-induced fit.
- **Cheapest first test:** Rotate a feature distribution clockwise and counterclockwise under a fixed causal law, with order-specific distractors. Compare against pooled augmentation and final-state ensembling; check the old angles on fresh examples and the unseen intermediate angles.

### 46. Make slow plasticity a clock for delayed rewards — primitive
- **Mechanism:** Give replicated features distinct refractory periods after an update. A sparse reward event is credited to features that are now emerging from their refractory period, so targeted past events are selected by the temporary inability to update.
- **Why it might be new:** Eligibility traces decay a stored activity signal. This uses the trajectory of a trainable plasticity gate, allowing windows with delayed eligibility rather than just monotone decay.
- **Cheapest first test:** In a small delayed-choice bandit with distractor events, compare refractory keys to exponential traces and a history window at matched state bytes. Retest old choice contexts and their original reward delays after new contexts enter.

### 47. Train on wrong coordinates to export an invariant skill — primitive
- **Mechanism:** Before a handoff, deliberately refactor one model's hidden units with several disruptive substitutions that preserve only most of its outputs. Distill just the operator behavior that survived each change into a compact interface another model can implement.
- **Why it might be new:** Stable ABI enforces compatibility, and task-vector transport moves deltas. This uses *selective breakage under interface changes* to discover the smallest behavior worth exporting.
- **Cheapest first test:** Use permuted and partially remixed hidden channels in small transducers; compare failure-filtered contracts to random and output-only distillation at equal bytes. Test old source operations and the exported operations on fresh target inputs after more learning.

### 48. Learn a new axis from formerly simultaneous failures — primitive
- **Mechanism:** Overwrite a learner with two unrelated new skills in alternating short bursts and locate old probes that fail in lockstep. Introduce a new latent axis specifically to independently vary the two failure sets, then make that axis available for a future task.
- **Why it might be new:** Disentanglement usually starts from independent labels or interventions on inputs; this uses accidental dependencies induced by mutually disruptive learning as the evidence for a missing coordinate.
- **Cheapest first test:** Use a bottleneck MLP with two initially entangled sensory factors. Compare failure-driven expansion with ordinary residual PCA and random dimension growth; test old factors independently after an unseen combination is taught.

## IV. Agents that need a changing world

### 49. Keep the exception that disappeared — primitive
- **Mechanism:** When a lesson is superseded, preserve a single executable contrast between a case where it mattered and a near neighbor where it did not. When tooling changes again, run the contrast to discover if the old distinction has returned under new names.
- **Why it might be new:** Regression fixtures check stability; this is a test that is *supposed* to stop distinguishing cases during some regimes, then activates learning when the distinction returns.
- **Cheapest first test:** Rename and later reintroduce a parsing distinction in a toy API. Compare one contrast per obsolete lesson with one old happy-path fixture and semantic retrieval at matched queries; verify task success in the returning regime and on all unaffected old formats.

### 50. Reuse a lesson's failure, not the lesson — primitive
- **Mechanism:** Compile a failed lesson into an ordered sequence of checks for where it stopped working. When a new task fails in the same way, execute that sequence to narrow which assumption needs relearning without retrieving the old prescription.
- **Why it might be new:** Case-based repair reuses past solutions; here a discarded solution exports a reusable measurement procedure that need not recommend an action at all.
- **Cheapest first test:** Build benign toy workflow tools with one latent assumption changed at a time. Compare cached success recipes and unordered checklists at matched tool calls; retest previously solved workflows, including an older one that reused the failed diagnostic.

### 51. Evidence that survives plan substitution — primitive
- **Mechanism:** Before storing a lesson, force the agent to complete the task with its preferred operator disabled. Save only an executable evidence-producing step that appears in both valid plans; later the agent must build a new plan around that evidence.
- **Why it might be new:** Plan diversity yields multiple solutions. This makes controlled loss of a planning affordance an extractor for small portable evidence obligations, not for the plans themselves.
- **Cheapest first test:** In a grid puzzle with redundant observables, compare stored evidence steps, shortest plans, and randomly masked plans at equal bytes. Test new layouts and replay old goal types with their old tool menus.

### 52. Harness changes that are only valid in opposition — primitive
- **Mechanism:** Keep paired policy patches that are deliberately invalid alone: one removes an assumption another used, and the other supplies a new source of evidence. Treat their joint activation as an indivisible update and teach later patches to depend on the pair's removal/replacement interface.
- **Why it might be new:** Transactional patching applies edits atomically; the new unit is a learned pair whose *functional* meaning comes from mutually offsetting breakage.
- **Cheapest first test:** Evolve two-step toy tool policies with obsolete assumptions, comparing paired evolution with ordinary two-edit search and a rollback gate at matched evaluations. Replay old workflows with both rules composed and with other old patches present.

### 53. Use stale plans as a ruler for affordance change — primitive
- **Mechanism:** Execute a tiny panel of intentionally stale plans in a simulator, storing the first state at which each deviates from its old outcome. Interpret the ordered failure positions as coordinates for the new environment and use nearby coordinates to choose a repair.
- **Why it might be new:** Drift alarms report that tools changed; these plan breakpoints form a reusable coordinate system for transferring fixes between different changes.
- **Cheapest first test:** Mutate a toy crafting simulator by disabling or delaying recipes. Compare breakpoint coordinates to tool metadata and final-success bits; retest all old plans in unmodified variants and previously adapted plans in their matching variants.

### 54. Scrap heap as a compiler target — primitive
- **Mechanism:** Delete retired skill implementations but retain their old test failures as executable input/output constraints on candidate compositions; keep expected answers only for those failure cases. As the live skill vocabulary changes, synthesize fragments that cover multiple constraints across old retirement batches, even if no old skill is reconstructed.
- **Why it might be new:** The round-trip consolidation leader translates between code and weights. This translates *selective negative evidence* into new executable modules directly, with no old code or weight copy to decompile.
- **Cheapest first test:** Retire DSL programs after primitive substitutions; compare failure-only synthesis with positive demo synthesis and keeping retired code at equal bytes. Retest each old spec on fresh inputs, not just its archived failures.

### 55. Agents teach by refusing at different points — primitive
- **Mechanism:** Train a teacher to stop a student sequence at intentionally different failure boundaries while never supplying the right action. The student learns a reusable segmentation of a task from the different places the teacher withholds continuation.
- **Why it might be new:** Intervention learning uses where a human naturally takes over; this deliberately programs the location of refusal as a compressed lesson that teaches a subgoal boundary.
- **Cheapest first test:** Use scripted teachers for three procedurally generated logic puzzles. Compare boundary-only instruction with equal-bit success flags and explicit subgoal markers; retest old puzzles without the teacher after training on another puzzle family.

### 56. A skill stores the question it cannot answer — primitive
- **Mechanism:** When skill A repeatedly loses to a new skill on a shared region, store only the shortest question whose answer collapses their disagreement. Inject that question into future skill training as an extra observation, not a retrieval key.
- **Why it might be new:** Ask-when-stuck retrieves atoms via a failure signature. This converts skill interference into acquisition of an observation variable that future skills can learn to request autonomously.
- **Cheapest first test:** In a constrained-action toy with one queryable hidden attribute, compare learned questions to entropy requests and failure-indexed memory at matched queries. Retest old ambiguous and unambiguous tasks without revealing task identities.

### 57. Memory with deliberately incompatible units — primitive
- **Mechanism:** Let different agent skills independently choose incompatible units for intermediate state. Force a conversion only when the plans disagree on an outcome, and add to a shared registry solely the conversions that resolve multiple disputes.
- **Why it might be new:** Schema migration prescribes a mapping up front. Here disputes between functioning local dialects are the measurement that discovers a common interface over time.
- **Cheapest first test:** Generate toy calculators with independently permuted latent units; compare inferred dispute conversions to fixed canonical units and pairwise mapping at matched demonstrations. Recheck old local plans plus earlier cross-unit plans on new numbers.

### 58. Harness fault injection as a curriculum language — primitive
- **Mechanism:** Define a lesson by which existing planning affordances are temporarily unavailable, not by a textual directive or new problem. Train a scheduler to compose these outages into practice episodes that teach recovery skills.
- **Why it might be new:** Domain randomization samples faults; this gives teachers editable, composable lessons whose payload is removal of a capability at a precise execution phase.
- **Cheapest first test:** Train tabular agents in small multi-route mazes with simulated sensor outages. Compare a learned outage curriculum to random outages and state difficulty sampling; retest old navigation both under normal operation and under earlier faults not used in the final curriculum.

### 59. Convert drift into a positional code for agent memory — primitive
- **Mechanism:** Permit a short memory fragment's words to drift under repeated compression, but train its reader to infer the fragment's place in a dependency chain from the asymmetric way its details erode. Reconstruct enough order to execute compositions without explicit absolute timestamps or restoring old text.
- **Why it might be new:** Aging clocks track staleness; here structured erosion stores a *relative dependency address* useful for execution rather than timekeeping or retrieval recency.
- **Cheapest first test:** Use a scripted token compressor and chains of toy transformations. Compare with explicit timestamps, generic age markers and uniform decay at equal bytes; test old independent and composite skills after new chain entries.

### 60. The default is whatever survives losing its sponsor — improvement
- **Mechanism:** Periodically remove the rule, role, or hint that originally sponsored a plan, and see whether other independently obtained evidence can reconstruct the procedure. Promote plans to default only if reconstruction works under future variants where the sponsor is absent.
- **Why it might be new:** Convergent-edit promotion counts independent rediscoveries; this is a targeted intervention on a plan's dependencies, rather than comparing naturally occurring edits across families.
- **Cheapest first test:** Use program synthesis in a toy workflow grammar with some irrelevant tips. Compare sponsor ablation with recency and independent rediscovery at matched generation calls; retest old workflow success and tip-dependent exceptional cases.

### 61. Route by the residue of an intentionally broken protocol — primitive
- **Mechanism:** In a simulator, provide the agent a harmless test command that every supported protocol rejects but in different, controlled ways. Learn a repair macro indexed by the rejection sequence, then require the macro to work on protocols whose names and surface fields have changed.
- **Why it might be new:** Capability negotiation advertises a menu; this uses the shape of a failed interaction as an executable interface for discovering affordances without a shared version vocabulary.
- **Cheapest first test:** Implement three toy board-game protocols with structured negative acknowledgments. Compare learned rejection macros with metadata-based routing and ordinary probing at equal calls; retest held-out moves under every old protocol after new variants arrive.

### 62. A library that learns from abandoned branches — primitive
- **Mechanism:** When a planner drops a partial plan, keep the narrow relational invariant it already established, but discard all steps and the unfinished goal. New plans can use that invariant as a certified starting point only if the environment still validates it on a small witness.
- **Why it might be new:** Search caches usually reuse explored states or costs; this exports an incomplete branch's validated *sub-result* for plans that do not share its start state or original objective.
- **Cheapest first test:** Use graph puzzles with shared substructures and disjoint goals. Compare abandoned-branch invariants with equal-byte memoized states and successful subplans; retest older puzzles, including previously used witnesses that become invalid when edges move.

### 63. A canary that must go extinct — primitive
- **Mechanism:** Embed a benign obsolete assumption in a dedicated toy skill and train agents to stop relying on it at different stages of an environment transition. Read the resulting extinction order as a causal probe of which affordances changed first, then choose which production skills to adapt.
- **Why it might be new:** A canary ordinarily detects any failure; a deliberately doomed bundle produces an order code intended to distinguish multiple change processes with the same endpoint.
- **Cheapest first test:** Simulate two orders of tool removal that end in identical tool menus but require different continuity fixes. Compare extinction-order routing with final failures and a change-log control at equal bytes; retest old workflows under unchanged and returning conditions.

### 64. The lesson is an executable scar — primitive
- **Mechanism:** After a difficult recovery, mutate the workflow once so the same interruption would leave a different observable trace next time. Retain the trace-producing change, not a written description of what went wrong; a later agent can teach itself from that trace before knowing how to fix the recurrence.
- **Why it might be new:** Logging records chosen events, and reflective memory stores diagnoses. Here a recovery writes a mechanism that causes the next recurrence to generate its own diagnostic data.
- **Cheapest first test:** In a simulator of benign multistep jobs, compare event re-instrumentation with reflective notes and ordinary fixed logging at matched trace bytes. Retest earlier job families, including those that share steps but not the original interruption.
