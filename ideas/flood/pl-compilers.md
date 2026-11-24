# Flood: 64 compiler and programming-language primitives for continual learning

The angle is to give learning new objects and operations, not just to rename training as compilation. These are raw proposals, not novelty verdicts. I screened against the [idea ledger and flood triage](https://github.com/manojbajaj95/cl/pull/6) and neighboring floods, especially [programs-weights](https://github.com/manojbajaj95/cl/pull/39), [NOOA](https://github.com/manojbajaj95/cl/pull/41), and [CL-Bench](https://github.com/manojbajaj95/cl/pull/48). The designs avoid re-proposing the current top three (prompt-addressable checkpoints, round-trip consolidation, and the self-readable seed log) or reviving ledger kills.

Each first test is a proposed cheap pilot, not a result. Match writable parameter count, persistent memory, examples, or simulator calls as appropriate. Measure the named old-task retention on held-out inputs against performance immediately before the intervening learning, as well as against the control; require new-task adoption too.

## Types that control what can be learned

### 01. Existential memory packages
- **Mechanism:** A feature-producing learner exports a package `∃R. (encode, compare, update)`. Consumers may compare or update opaque values of type `R` but never inspect coordinates. A new experience can trigger a rewrite of the encoder and its private store together without retraining the consumers.
- **Why it might be new:** Representation independence is familiar in PL; here an entire body of learned state can change representation without making those coordinates part of every downstream task's memory.
- **Cheapest test / retention:** Learn two nearest-prototype classifiers over a common latent store, replace its encoding with a learned low-dimensional one while adding class families, and compare to clients trained against exposed vectors. Retest both original classifiers on held-out old classes without updating their heads.

### 02. Blame-transferring casts
- **Mechanism:** A learned value crossing a typed boundary carries a producer version and an independent check of the consumer's extra assumptions. A failed check assigns a correction to the producer for contract violations, or to the consumer's adapter if its assumptions were stronger than the contract.
- **Why it might be new:** Gradual typing adds blame to casts; the new operation is routing a learning example to the party responsible for the misuse, not freezing typed weights or assigning loss to every upstream step.
- **Cheapest test / retention:** Simulate learned date normalizers used by two report tools, with malformed dates and a new consumer demanding stricter bounds. Compare blame-routed corrections to updating the last failing module. Retest old date sources and the original reports on held-out inputs.

### 03. Linear evidence types
- **Mechanism:** Make the right to count an observation a linear resource. Deriving two lessons from one observation can produce two reusable predictors, but their fusion must reunite the original evidence token or explicitly trade it for fractional credit.
- **Why it might be new:** Provenance semirings and Bayesian data incest are neighbors. The object is a transferable write right enforced through derivation and fusion, not a similarity filter for duplicate lessons.
- **Cheapest test / retention:** Use a Bernoulli bandit stream where the same event arrives through two noisy summarizers; compare to exact text deduplication plus matched storage. Retest reward and calibration on old bandits after a new reporting channel and new arms arrive.

### 04. Variance-checked concept replacement
- **Mechanism:** Annotate every import of a learned predicate by polarity: positive consumers may tolerate enlarging its extension, negative consumers may tolerate shrinking it, and invariant ones need a two-way conversion. A predicate rewrite compiles mixed uses into a common core plus only the necessary compatibility branches.
- **Why it might be new:** This applies subtyping variance to a learned concept's changing truth set across multiple clients, rather than testing one new classifier against a single stable ABI.
- **Cheapest test / retention:** Stream refinements of a synthetic document predicate shared by allow, exclude, and exact-count tasks. Compare against one shared retrained classifier and per-task heads at matched capacity. Retest old exclusion and count queries explicitly, not just aggregate predicate accuracy.

### 05. Session-typed belief updates
- **Mechanism:** A persistent belief exposes different operations depending on its protocol state: a hypothesis can consume confirming evidence, a confirmed belief can be queried as a fact, and a superseded belief can answer historical questions but not trigger present actions. The role of an observation in the protocol, not just its content, determines the legal update.
- **Why it might be new:** Session types check dialogue structure; here the durable learned object is governed by an evidence protocol even when observations arrive across episodes.
- **Cheapest test / retention:** Train a toy inventory agent with propose/confirm/withdraw events, duplicated messages, and new vendors. Compare with a flat typed event table. Retest historical inventory queries and old confirmed-item decisions after adding the new vendors.

### 06. Type-class instances learned from laws
- **Mechanism:** Learn an instance for each newly encountered data family by fitting a small set of operations jointly to algebraic laws. Existing generic callers reuse the new instance via dictionary passing rather than learning the tasks again.
- **Why it might be new:** Type classes and invariant losses are known; the unit of continual acquisition is a reusable law-abiding dictionary that enables callers never seen during its acquisition.
- **Cheapest test / retention:** Infer combine/identity for new toy aggregation operators from a few examples plus associativity. Compare against separate task-conditioned heads; test unseen uses such as balanced reduction and retest old aggregators under fresh parenthesizations.

### 07. Parametricity probes for frozen generics
- **Mechanism:** A reusable named operation claims not to depend on the identity of its element type. Check this by applying random element bijections and transporting results back; train only its new type-specific argument module unless the claim fails.
- **Why it might be new:** Metamorphic tests and equivariant nets are neighbors. Parametricity acts as a train-time decision about which part of a growing library a lesson is even allowed to change.
- **Cheapest test / retention:** Add symbol alphabets to a network that groups and permutes lists, comparing random-relabel training with a joint fine-tune. Retest held-out old alphabets and a held-out generic caller, not just old examples with relabeled tokens.

### 08. Affine activation borrows
- **Mechanism:** Give a new skill a read-only borrow of an old feature during a forward call and a private writable view only on a declared slice. A borrow may not escape into persistent state: if it does, materialize an owned representation and redirect only the escaping consumer.
- **Why it might be new:** Frozen features and lateral adapters are neighbors; static/dynamic escape determines when learned state acquires an independent representation, rather than deciding whether agent notes should persist.
- **Cheapest test / retention:** Train small recurrent classifiers with both transient feature consumers and delayed-state consumers; compare borrowing plus promotion to always-copy and frozen sharing. Retest old immediate and delayed classifiers after conflicting later tasks.

## Dataflow and incremental compilation

### 09. Phi nodes for learned state
- **Mechanism:** Give every write to a scratch variable a single-assignment identity. At joins, train one explicit phi node to combine mutually exclusive predecessors, using provenance tags rather than blending all writers into the same slot.
- **Why it might be new:** SSA isolates join semantics; the learned object is the join rule, so adding a producer need not alter the rules used inside existing branches.
- **Cheapest test / retention:** Learn a toy recurrent agent with two routes to an intermediate count, then add a third route. Compare against a shared scratch head with the same capacity. Retest old branch pairs and nested joins after adding the third.

### 10. Self-adjusting gradient graphs
- **Mechanism:** Cache local sufficient statistics and Jacobian-vector closures along the execution dependency graph. A corrected lesson invalidates only touched ancestors/descendants needed to update the training objective; unaffected contributions are reused exactly in a restricted differentiable DAG.
- **Why it might be new:** Self-adjusting computation normally saves inference work; the primitive here consumes deltas to the objective and incrementally repairs a learned model, not merely a cached answer.
- **Cheapest test / retention:** Use a DAG of linear regressors with some shared frozen features and a stream of label amendments. Compare with full refitting and equal-wall-time replay; measure work and retained MSE on untouched old regressor tasks.

### 11. Visibility-specific rebuilds
- **Mechanism:** A learned symbol exports several views, e.g. ordering, equality, or calibrated score. Clients depend on a specific view. When the producer changes, relink only clients whose observable view changed, using a view-specific fingerprint.
- **Why it might be new:** Incremental builds distinguish interface from implementation; here two clients of the same learned representation have different invalidation equivalence relations, not a single ABI epoch.
- **Cheapest test / retention:** Change a learned ranker's score scale while adding a new query domain; compare to version-wide invalidation. Retest order-only old clients, and retest old threshold clients after recalibrating only those affected.

### 12. Incremental dual numbers for edited meaning
- **Mechanism:** Carry old-to-new semantic deltas through a differentiable workflow along with values. A learned component consumes `(value, change)` and predicts the new output change; exact residuals update its derivative model locally when discontinuities appear.
- **Why it might be new:** Incremental lambda calculus and forward-mode AD are neighbors. A learned *change interface* lets clients consume edits without fetching all past meanings or rebuilding their full prediction path.
- **Cheapest test / retention:** Stream small scale and occasional threshold shifts through a three-stage scoring workflow. Compare change propagation to one-stage linearization and last-stage replay. Retest old unchanged source families and old changed ones against current correct end-to-end labels.

### 13. Backward slices of retention obligations
- **Mechanism:** Slice each old assertion backward through both data and branch dependencies, then compile its current objective to the nearest shared cut. Keep only the cut-level witness and constraint, not the original trajectory or a frozen upstream model.
- **Why it might be new:** Program slicing and activation replay are neighbors. The retained object is an executable partial objective with explicit control-dependence predicates, not an importance mask or a replayed call subtree.
- **Cheapest test / retention:** Learn a two-route scheduling agent and repair one shared decision. Compare to cut activations without branch predicates and same-memory end-to-end replay; retest held-out old schedules on both routes.

### 14. Negative-dependency invalidation
- **Mechanism:** A learned decision records absences as dependencies: e.g., a default was chosen only because no more specific entry existed. Index those negative queries, then push new facts to the old decisions that must be revalidated despite no old artifact having changed.
- **Why it might be new:** Negation maintenance in databases is known; turning its invalidations into targeted adaptation examples catches interference that dependency tracing over executed components cannot see.
- **Cheapest test / retention:** Add increasingly specific catalog entries to a toy chooser. Compare to positive trace invalidation with equal updates. Retest both old fallback inputs that should keep their answer and old inputs that should now use the learned specific answer.

### 15. Equality saturation over reusable skills
- **Mechanism:** Store several verified equivalent compositions of reusable learned operators in an e-graph. When one operator drifts or becomes expensive, extract a surviving expression, making repair a local choice of implementation rather than a parameter rollback.
- **Why it might be new:** An e-graph keeps equalities live even when it picks no implementation today; this banks alternative proofs and recovery paths during learning rather than superoptimizing one delta after the fact.
- **Cheapest test / retention:** Learn a tiny library of string transformations and add a dialect that breaks one equivalence on a subset. Compare to a library storing only its cheapest compositions. Retest old transformation pipelines on withheld strings.

### 16. Differentiable build cuts
- **Mechanism:** Make intermediate summaries learnable at build boundaries. An auxiliary loss optimizes the summary to be a sufficient statistic for multiple downstream skills while minimizing how often data edits cross the boundary and trigger rebuilding them.
- **Why it might be new:** Learned bottlenecks and incremental build partitioning are neighbors; the bottleneck is trained for *rebuild cost under edits*, not maximal transfer or minimum representation drift.
- **Cheapest test / retention:** Learn shared features for three synthetic document readers and stream changes to independent sources. Compare to a standard multitask bottleneck with equal bytes. Retest old readers on held-out documents at a fixed rebuild budget.

## Runtime adaptation without history replay

### 17. On-stack skill replacement
- **Mechanism:** At declared safe points in a running episode, rebuild a new controller's local frame from old live variables and the continuation's required invariants. Only the active suffix changes; no reset, prompt selecting an old model, or checkpoint needs to exist.
- **Why it might be new:** VM on-stack replacement is the neighbor; the mapping between continuously learned local states is itself a learned, validated artifact at the control-frame level, not inter-layer stitching.
- **Cheapest test / retention:** Replace a partially executed toy delivery planner when a new rule arrives at step five; compare to restart and naive latent copying. Retest interrupted old deliveries with traps that make restarting impossible.

### 18. Delimited learning continuations
- **Mechanism:** When an agent suspends a decision pending evidence, store the exact remaining learned computation and its write scope. Later feedback resumes only that continuation, leaving unrelated decisions made in the meantime untouched.
- **Why it might be new:** Compared with delayed-feedback replay or gradient IOUs, the stored object is a resumable choice of *what to learn next*, including a scoped local environment, not a precomputed update.
- **Cheapest test / retention:** Simulate two interleaved ordering policies with delayed approvals, where evidence is only useful inside a pending branch. Compare to queued-example replay; retest old approved orders and unaffected pending branches after new evidence.

### 19. Demand-driven thunks for unlabeled episodes
- **Mechanism:** Leave an unforced thunk containing a compact dispatcher and captured observations. The first verified future consumer requiring a specific statistic forces precisely that computation, memoizes it, and releases the observations if no other demanded projection remains.
- **Why it might be new:** Lazy evaluation and episodic replay are neighbors. This defers the *representation* of what was learned to the first demonstrated use, not just commitment to one of several pre-trained hypotheses.
- **Cheapest test / retention:** Stream unlabeled grid visits and introduce rule queries requiring different counts. Compare lazy captures to eager learned summaries at matched peak bytes. Retest old query types and already-forced answers after novel query types arrive.

### 20. Hysteresis as a calling convention
- **Mechanism:** Skill callers must pass a short proof of consistent recent observations before a learned callee switches modes. The callee returns a mode lease with a renewal policy; it cannot be switched solely by a single borderline observation.
- **Why it might be new:** Hysteretic routers exist; making the lease local to a call chain means one module can learn a new switch criterion without changing the timing assumptions of other modules.
- **Cheapest test / retention:** Stream two operating protocols with transient impostor observations and add a third. Compare to confidence routing and fixed smoothing. Retest old protocol transitions and steady-state success, including streams where the new protocol briefly appears.

### 21. Resumable failures as training data
- **Mechanism:** A learned callee can return a suspended computation plus an explicit unresolved obligation. The caller supplies a value that resumes the original computation; only that supplied intervention becomes supervision for the callee's missing primitive.
- **Why it might be new:** Algebraic effects and exception-based recovery are neighbors. Rather than learning a handler or restarting a rollout, the engine can collect supervision at the unresolved slot before returning to the old execution.
- **Cheapest test / retention:** Teach a toy spreadsheet assistant a new missing-unit conversion using caller-supplied resumptions. Compare to full corrected trace training and separate rule handlers; retest old formulas that share the callee but never raised the obligation.

### 22. Tail-position memory fusion
- **Mechanism:** Where learned state from a callee is immediately forwarded to another callee, erase the intermediate serialization after compiling the two update functions together. Require an equivalence test for the continuation, not for the transient state that no client sees.
- **Why it might be new:** Deforestation and tail calls are neighbors; in contrast to compressing repeated plans, this fuses *successive memory updates* whose intermediate learned state need never be materialized.
- **Cheapest test / retention:** Fuse pairs of running-summary updates in a toy stream analytics agent; compare to generic state compression. Retest old query continuations including an interleaved caller that does inspect the intermediate value and should remain unfused.

### 23. Deoptimization with write restitution
- **Mechanism:** A speculative fast skill may make tentative writes while assuming a stable environment. When its guard fails, map those writes to explicitly named restitution operations on the slow path so that valid discoveries survive and invalid effects are corrected.
- **Why it might be new:** Ordinary JIT deopt restores execution state; this preserves verified knowledge generated during the wrong specialization rather than discarding it or rolling back all weights.
- **Cheapest test / retention:** In a grid courier simulator, specialize for open doors, learn a valid shortcut, then discover a stale door assumption. Against rollback plus replay, test recovery cost and retained performance on original routes after the specialization fails.

### 24. Competing legal lowerings
- **Mechanism:** A checked skill has several target realizations with distinct numerical costs and stability under learning. Maintain observational equivalence at a test boundary, then let the runtime select a realization according to remaining adaptation budget, not task identity.
- **Why it might be new:** Multi-target compilers and conditional compute are neighbors; spending *future write bandwidth* as a runtime resource is the distinctive choice, even for the same input and semantics.
- **Cheapest test / retention:** Lower a small skill to fixed-point code or a trainable feature head; introduce alternating new tasks under a strict write budget. Compare to selecting by inference cost only. Retest old tasks under both low- and high-budget execution.

## ABI evolution and composable learned components

### 25. Semantic version intervals inferred from examples
- **Mechanism:** Each caller learns a compatibility interval over changes to particular behaviors, not just over model releases. On a breaking change, find the smallest subset of call sites that need a shim while letting other callers adopt the new semantics directly.
- **Why it might be new:** Semver and API compatibility are neighbors. The range is checked against behavioral dimensions of a learned interface; a single release can be a major change for one use and a minor change for another.
- **Cheapest test / retention:** Evolve a toy unit parser through spelling additions and one rounding change. Compare one global version rule to use-specific ranges. Retest original users at values near the old rounding boundary and users that should gain new spellings.

### 26. Calling-convention negotiation for learned uncertainty
- **Mechanism:** Two components negotiate not only a tensor shape but how uncertainty is encoded (sample set, calibration bins, or a sufficient statistic). A downstream consumer can request an upgrade only if its decision has become sensitive to lost information.
- **Why it might be new:** Calibration and ABI work protect a contract; an adaptive bidirectional protocol makes information precision conditional on what the old and new callers actually need.
- **Cheapest test / retention:** Give a classifier several learned downstream decision rules, then add a tail-risk rule. Compare to fixed logits and uniform high-precision output at matched bandwidth. Retest old decision accuracy and calibration after negotiation.

### 27. Capability-bearing gradient edges
- **Mechanism:** Grant a task a limited capability to pass learning signals through a module boundary: e.g. only modify calibration or fund up to a fixed cumulative change. Delegation to derived tasks attenuates that capability instead of silently inheriting full optimizer access.
- **Why it might be new:** Gradient masking and capability systems are neighbors. The right to update is an explicit composable object with a conservation rule over downstream derivations.
- **Cheapest test / retention:** A toy multitask encoder serves two trusted readers and many derived noisy readers. Compare attenuated delegation to fixed per-head LR and gradient clipping at equal training budget. Retest base reader tasks and established derived readers after adding the noisy ones.

### 28. Link-time generic specialization with coherent instances
- **Mechanism:** Let independent skills propose incompatible implementations of a latent operation. At composition time select one implementation per run and adapt all its uses together, rejecting mixtures whose identity laws fail even when each individual call fits.
- **Why it might be new:** Type-class coherence and dispatch are known; the primitive prevents acquired modules from independently choosing different meanings for a shared latent operation inside one novel composition.
- **Cheapest test / retention:** Compose sorting and deduplication modules that learned different notions of equality. Compare to local routing per call, then retest previously successful sort/dedup pipelines and tasks from both source domains.

### 29. Link-time optimization of learning rules
- **Mechanism:** Every module exports a local update rule. Linker-level passes contract shared forward features once and rewrite update operators so coupled parameter uses are accounted for jointly, rather than applying each independently learned rule to the same weights.
- **Why it might be new:** Module linking usually connects functions; this links *trainers*, potentially exposing whole-program identities invisible when optimizer policies are learned independently.
- **Cheapest test / retention:** Connect regressors that share an affine bias and export per-module least-squares updates. Compare composition-aware normal equations to per-module update averaging and equal-budget fine-tuning. Retest held-out old regressors after adding a coupled new head.

### 30. Weak imports for optional memories
- **Mechanism:** A caller marks an import as optional and provides an executable default. Train both resolutions from the start, then allow a newly acquired provider to bind the import only when it improves a held-out caller-specific risk functional.
- **Why it might be new:** Weak symbols and modality dropout are neighbors. Unlike weak references or plain skill routing, optionality lives in the *consumer's interface* and declares an already-trained missing-provider behavior.
- **Cheapest test / retention:** Train a toy estimator that optionally uses an external weather helper; add a new helper available only for some regions. Compare to unconditional linking and random helper dropout. Retest old regions with both missing and present providers.

### 31. Cross-module obligations as link inputs
- **Mechanism:** When linking learners, solve small compatibility witnesses (e.g. an adapter mapping between two local units) from equations emitted by both sides. The link artifact supplies only the witness; neither side changes its private weights.
- **Why it might be new:** Proof-carrying components and adapters are neighbors. The linker solves for a concrete existential shared witness from constraints on both modules, not a best-fit relocation learned on joint trajectories.
- **Cheapest test / retention:** Link independent normalization and threshold learners with hidden affine units using two exact anchor equations. Compare to training an adapter with the same examples; retest the modules' old stand-alone tasks and linked old combinations.

### 32. Opaque nominal identities for discoveries
- **Mechanism:** Generative modules mint unforgeable identifiers for concepts when semantics cannot yet be proven equal. Every learner that re-exports a discovery must preserve identity; explicit coercions can relate two identifiers without making them substitutable everywhere.
- **Why it might be new:** Nominal types and entity resolution are neighbors. Fresh names provide a way to *keep meanings apart* even when embeddings, surface names, and signature hashes coincide.
- **Cheapest test / retention:** Teach an inventory model two products with the same abbreviation from independent catalogs, then introduce a crosswalk for some synonyms. Compare with lexical and embedding merges. Retest original catalogs and crosswalk queries, including exclusions that must stay distinct.

## Effects and observations that survive composition

### 33. Handler-local credit ledgers
- **Mechanism:** Record the effect invocation before interpreting it, then attach outcome credit at the handler. If the same intent can be interpreted by multiple handlers, a newly learned handling rule updates only the relevant interpretation, not the originating policy's skill at choosing intents.
- **Why it might be new:** Hierarchical RL credit and algebraic handlers are neighbors. Effect interpretation gives counterfactual credit a stable handle despite switching simulators, without distilling outcome classes.
- **Cheapest test / retention:** Run a toy pantry planner against two fulfillment simulators and change only the new simulator's substitution rule. Compare to retraining the intent policy and to separate complete policies. Retest old pantry budgets and ingredient choices with the original handler.

### 34. Effect masking by observation
- **Mechanism:** Hide internal writes whose values cannot be observed by an exported interface. Different training rules can then rewrite hidden local state freely while preserving a visible effect trace; any new client that inspects previously hidden state requires a new interface.
- **Why it might be new:** PL encapsulation and behavioral regularization are neighbors. The learner gets a mechanically inferred license to change unobservable effects, not a bound on overall parameter movement.
- **Cheapest test / retention:** Let a small inventory agent learn new packing rules that alter internal scratch counters but not receipts. Compare to freezing all traced decisions and to unconstrained retraining. Retest old receipt tasks and receipts from mixed old/new packing modes.

### 35. Typed transactions over heterogeneous memory
- **Mechanism:** Stage one lesson's writes to a table, a learned policy, and a cache. A shared semantic transaction checks dependencies between all three and publishes the new interpretation atomically; an operation observing any two must see matching meaning epochs.
- **Why it might be new:** Transactional memory is known; the transaction here serializes *interpretations* across learned and symbolic carriers with different write latencies, rather than simply rejecting a bad harness diff.
- **Cheapest test / retention:** Simulate a price-class policy updated before its lookup table is rebuilt. Compare atomic publication against independently verified carrier updates. Retest held-out old price queries during, not just after, the delayed commit.

### 36. Effect-row polymorphic lessons
- **Mechanism:** Separate a reusable lesson's policy from an open row of effects it does not care about. Instantiate the policy with different local handlers, and learn a new handler when adding an effect without retraining the policy's data-independent decisions.
- **Why it might be new:** Effect polymorphism and modular options are neighbors; the row variable is an explicit claim about which future effects can be added without changing the learned policy.
- **Cheapest test / retention:** Reuse a toy booking policy with optional notification and loyalty effects introduced in sequence. Compare to adapter-per-environment and separate policies. Retest original booking under both original and enriched effect rows.

### 37. Temporal effects as learnable commitments
- **Mechanism:** A write can return a durable, typed future obligation (e.g. confirm before using a counter or cancel it when a condition changes). The scheduler learns when to fulfill these obligations but must preserve their deadline and dependency order as the policy changes.
- **Why it might be new:** Temporal logics and constrained RL are neighbors. The old-task memory object is an *outstanding obligation* that outlives the policy which created it, not just a prefix to replay.
- **Cheapest test / retention:** Simulate a library agent adding renewals while old reminders are pending. Compare to an unconstrained recurrent policy and timestamp-only reminders. Retest deadline satisfaction for obligations issued before learning and old checkouts started afterward.

### 38. Observational credit equivalence
- **Mechanism:** Quotient traces by what an evaluator can observe. When internal refactors split or fuse operations, preserve training credit across all proven-equivalent traces by assigning targets at the quotient boundary rather than to named internal steps.
- **Why it might be new:** Bisimulation and reward shaping are neighbors; the enduring artifact is a credit assignment stable under semantic refactoring, not an outcome-only distillation target.
- **Cheapest test / retention:** Refactor a tiny stock tracker into one- and two-stage update implementations while adding a new stock operation. Compare preserving boundary credit to redistributing step rewards uniformly. Retest old balanced-stock sequences and delayed-reward on old cases.

### 39. Provenance-preserving counterterms
- **Mechanism:** Maintain a separate correction function for a known biased observation process. At composition time apply it only to derivations that actually used that process; keep mixed-source derivations with ancestry-dependent corrections instead of globally fine-tuning the policy.
- **Why it might be new:** Bias correction and provenance are known; combining them makes it possible to repair the *consequences* of past evidence without reissuing evidence or inverting a learned parameter write.
- **Cheapest test / retention:** Fit toy forecasters on two observation sources, then reveal a biased calibration channel. Compare selective ancestry correction to global recalibration. Retest unaffected old-source forecasts and corrected mixed-source old forecasts.

### 40. Commuting squares for runtime remedies
- **Mechanism:** A repair can enter at observation normalization, interpretation, or output. Save explicit diagrams relating these entrances so later learning can move a repair around a changed component while preserving the caller's result, with equality tested only on the repair's claimed domain.
- **Why it might be new:** Commuting diagrams and middleware normalization are neighbors. This transports a *semantic remedy across a boundary within a workflow*, not a task vector across base-model versions.
- **Cheapest test / retention:** Fix an off-by-one in month counting in a toy planner, then replace the date normalizer. Compare transport via the diagram to keeping the intercept fixed or re-learning it. Retest old boundary dates and old unaffected calendar queries.

## Staged learning and safe transformations

### 41. Hygienic macros for learned policies
- **Mechanism:** A macro distilled from repeated agent workflows expands into a policy fragment with fresh latent slots and explicit imports. Training on a macro call updates its declared arguments and generated slots without accidentally binding a same-named memory in the caller.
- **Why it might be new:** Policy templates and weight-space macros are neighbors. Hygiene, not macro generation, is the CL operation: it protects previously learned meaning when reusable structure is inserted in a new scope.
- **Cheapest test / retention:** Learn repeated inventory workflows with distinct meanings for `count` and expand a shared macro into a new domain. Compare to textual substitution and manual slot prefixes. Retest old workflows on nested calls with shadowed names.

### 42. Multi-stage acquisition of latent features
- **Mechanism:** Label an intermediate operation as depending on compile-time examples, deployment-time context, or still-unseen future evidence. Specialize only earlier-stage dependencies into parameters; preserve later-stage parts as residual trainable arguments with their own objective.
- **Why it might be new:** Staged programming and conditional adapters are neighbors. The stage assignment determines *which computations are still learnable on later evidence*, not merely precomputation for a fixed user.
- **Cheapest test / retention:** Learn a protocol with shared syntax, per-environment units and one late-arriving calibration table. Compare stage-typed specialization to eager full fine-tuning and static partial evaluation. Retest earlier protocols after units and calibration become known.

### 43. Metaobject protocols for learning hooks
- **Mechanism:** Define an explicit protocol for how predictions, gradients, and persistent writes enter a learner. A task can replace one hook (e.g. gradient normalization) by learning an implementation compatible with the rest, and the hook can override defaults for only explicitly tagged downstream learners.
- **Why it might be new:** Metaobject protocols and learned optimizers are neighbors; a local hook changes how a group learns without forcing every group to adopt a new optimizer or allowing arbitrary harness rewrites.
- **Cheapest test / retention:** Add a heavy-tailed regression family that learns a robust normalization hook. Compare to a global learned optimizer and fixed per-family optimizers. Retest old regressors and their ability to learn a small follow-up task.

### 44. Derivative-preserving refactors
- **Mechanism:** Permit a rewrite of a learned module only if it preserves both present outputs and the effect of designated future updates on those outputs. Fit a transport of optimizer coordinates to preserve the required directional derivatives when moving parameters.
- **Why it might be new:** Network morphisms and optimizer-state transfer are neighbors. The transformation preserves a declared *family of future learning operations*, not just current behavior or inherited optimizer moments.
- **Cheapest test / retention:** Factor or widen a toy linear network midstream, compare forward-equivalent refactoring against derivative-preserving refactoring, and measure whether named update trajectories stay matched on later examples and whether old held-out regression error stays unchanged.

### 45. Learning-aware common subexpression elimination
- **Mechanism:** Merge two equivalent latent operators only when their expected future correction signals agree under the same input map. If outputs match today but a future update would expose a difference, keep distinct writable parameters with a shared forward cache.
- **Why it might be new:** Distillation and function deduplication usually compare behavior at a point. This explicitly separates safe inference sharing from safe *write* sharing.
- **Cheapest test / retention:** Use two synthetic rules identical on initial samples but with opposing corrections on a new branch. Compare to activation-based merging and no merge. Retest old cases and a control pair that truly should continue sharing after the new labels.

### 46. Evolving differentiable bidirectional views
- **Mechanism:** A lens translates a field in a learned representation to a stable client view and lifts edits on the view back into the private state while retaining hidden information. When the view changes, learn its complement so old read/write laws continue to hold for old clients.
- **Why it might be new:** Bidirectional programming and latent editing are neighbors. The tested object is an evolving learned `get/put` pair with noninterference laws, not a representation migration or a code–weight round trip.
- **Cheapest test / retention:** Train a small color/shape representation with an editable color view, then add a texture view. Compare to independent linear steering directions; retest old color writes and check that original shape recognition survives sequences of both edits.

### 47. Supercompiling composed training loops
- **Mechanism:** Partially execute several trainers on symbolic batch statistics, then fold repeated update states into one residual training program. The residual recurrence removes redundant updates while representing the same allowed sequence of trainer interactions.
- **Why it might be new:** Optimizer fusion saves kernels; supercompilation specializes *the trainer interaction* and can produce a recurrence that was not in any trainer, rather than finding a sparser fixed weight delta.
- **Cheapest test / retention:** Alternate exact small linear updates with a normalization step and synthesize a residual loop over sums. Compare to ordinary fused kernels against identical stream prefixes; retest old fits after inserting a new trainer into the loop.

### 48. Rewrite rules over corrections
- **Mechanism:** Represent a correction as an intervention on a named expression. When later changes alter that expression's shape, rewrite the correction using checked rules acting on the intervention itself, then apply it at the new expression.
- **Why it might be new:** Refactoring-aware patch transfer and term rewriting are neighbors. The primitive moves an *instruction for how to change meaning* that has not yet been applied, rather than merging committed parameter versions.
- **Cheapest test / retention:** Queue a pending unit correction in a small learned scoring DSL, refactor addition/multiplication order, then apply it by rewriting. Compare to line-anchored pending corrections and re-fitting; retest prior scoring scenarios outside the correction domain.

## Static analyses with learning-specific outputs

### 49. Relational abstract domains for skill reuse
- **Mechanism:** Maintain a relational abstract summary (e.g. an interval on `f(x)-g(x)`) of two existing components. When encountering a new caller, decide whether it can substitute one for the other *for its own observable* without estimating either component's full error.
- **Why it might be new:** Unlike abstract interpretation of a proposed parameter update, this analysis produces a justified reuse decision before training and can exploit correlated errors invisible to independent bounds.
- **Cheapest test / retention:** Use two tiny score estimators with correlated errors and a downstream rank decision. Compare reuse under difference intervals to independent error intervals. Retest old rankings and estimators after using freed capacity for a new task.

### 50. Widening and narrowing the hypothesis language
- **Mechanism:** When support arrives indefinitely, widen a description of feasible rules into a finite abstract family to ensure online convergence. A later counterexample narrows only the affected family and teaches the learner a finer distinction rather than forcing global rule expansion.
- **Why it might be new:** Widening/narrowing in static analysis and version spaces are neighbors. This puts an explicit budget on the *expressiveness* of CL state, not just number of stored examples or parameters.
- **Cheapest test / retention:** Stream increasing numeric ranges and rare modular exceptions to a rule learner. Compare interval-to-strided-interval widening with reservoir examples. Retest old range decisions and rare old exceptions after new exceptions arrive.

### 51. Must/may learned dependencies
- **Mechanism:** Distinguish dependencies observed on every acceptable execution from those occurring on at least one. A revision of a may-dependency can select a still-valid alternative; revision of a must-dependency incurs a mandatory repair before execution.
- **Why it might be new:** Static may/must analysis does not usually treat learned behavior as a nondeterministic implementation. This turns ambiguity over old correct implementations into an explicit resource for ongoing adaptation.
- **Cheapest test / retention:** Learn multiple acceptable grid routes, then change an optional corridor and later an unavoidable one. Compare to single-trace and all-path invalidation. Retest original destinations, including route choices never executed during training.

### 52. Product programs for forgetting localization
- **Mechanism:** Execute old and new components in lockstep on coupled symbolic inputs and stop at the first violated relation. Compile the failing relation, not the output delta, into a paired training example at that boundary.
- **Why it might be new:** Relational verification and differential fuzzing are neighbors; the primitive learns from a cross-run *alignment relation*, able to distinguish legitimate internal change from real old-task loss.
- **Cheapest test / retention:** Train two-stage arithmetic executors where intermediate representations legitimately shift while one branch regresses. Compare product-generated constraints to output-difference fuzzing and layer matching. Retest old arithmetic on withheld compositions.

### 53. Counterexample generalization by proof interpolation
- **Mechanism:** When a new rule conflicts with an old proof, extract a separator using only the symbols shared by the new rule and the old proof. Add that separator as a durable obligation instead of storing each individual counterexample.
- **Why it might be new:** Craig interpolation and constraint extraction are neighbors. Old-task retention is represented by small *shared-vocabulary* obligations surviving rewrites of either side.
- **Cheapest test / retention:** Use a SAT-backed Boolean task learner with repeating violations across many input combinations. Compare interpolants to exact counterexample replay with equal storage; retest held-out old combinations after learning a partly conflicting task.

### 54. Angelic holes as transfer interfaces
- **Mechanism:** Preserve partial solutions with unspecified operations, but store a witness that at least one completion works. New learning can fill a hole with a more general operation only if every previously promised caller still has a suitable completion.
- **Why it might be new:** Sketching and adapters are neighbors. The persistent learned object promises *existence of compatible completions*, not a frozen implementation, retrievable old policy, or concrete deferred-hypothesis branch.
- **Cheapest test / retention:** Learn partial sorting and grouping procedures sharing a comparator hole, then acquire case-insensitive ordering. Compare constrained fill to freezing the first comparator and to unconditional replacement. Retest old procedures on tie cases.

### 55. Termination budgets for ongoing self-edits
- **Mechanism:** Require each internal edit in a refinement episode to strictly reduce a well-founded measure over unresolved dependencies. A genuinely new observation can start a new episode, but internal edits cannot create an endless repair cascade.
- **Why it might be new:** Ranking functions and churn penalties are neighbors. The measure constrains a sequence of admissible rewrites rather than scoring a policy's immediate behavior; there is no stability exponent to estimate.
- **Cheapest test / retention:** Use a rule graph where fixes for defaults can bounce between aliases, and add new rule families. Compare ranking-certified edits to a retry cap. Retest old query accuracy after repair convergence and track churn.

### 56. Relational counterfactual frame rules
- **Mechanism:** To learn a new behavior, demonstrate a local pre/post relation and derive a frame of independent old state from verified separation of observables. Reuse that frame for later edits unless an observed alias disproves separation.
- **Why it might be new:** Separation logic and local model edits are neighbors; the reusable knowledge is a defeasible proof that two *observations* are independent, not sparsity or orthogonality of the underlying parameter writes.
- **Cheapest test / retention:** Add record transformations to a toy system with hidden references between some fields. Compare inferred frames to coordinate masks and full rechecking. Retest old queries over both unaliased and falsely presumed-independent records.

## Memory representations, migrations, and wild cards

### 57. Generational GC with cross-memory write barriers
- **Mechanism:** When a mature memory is written or rebound to a young dependency, a write barrier adds that edge to a remembered set. Compact young memory without rescanning old skills, tracing from those recorded edges as well as direct roots.
- **Why it might be new:** Prior reachability GC proposals decide what to retire. A write barrier adds an incremental *maintenance protocol* across memory substrates and lets collection run at different frequencies.
- **Cheapest test / retention:** Simulate a few durable policy tables plus many newly learned exceptions; compare nursery/barrier collection to full mark-and-sweep under matched peak bytes. Retest old policies that depend on young exceptions as well as old policies with no such dependencies.

### 58. Ephemerons for conditional memories
- **Mechanism:** An ephemeron's value stays live only if its key is reachable without traversing the value. Model a specialized learned exception as the value and the independently acquired context in which it matters as the key; a self-referential exception cannot keep its context artificially alive.
- **Why it might be new:** Weak references and reachability GC are neighbors. Ephemeron semantics give a precise fix for sets of mutually reinforcing notes masquerading as still useful because they keep pointing to each other.
- **Cheapest test / retention:** Simulate agents caching exception rules with circular references; compare ephemeron collection to LRU and standard weak references at matched memory. Retest old exceptions whose contexts recur independently and old base tasks where stale exceptions should no longer fire.

### 59. Lazy migrate-on-write with old-reader projections
- **Mechanism:** Migrate old memories one record at a time when modified; new readers use temporary views of unmigrated records and old readers get reverse projections of migrated records. Update the migration only when a real view fails, rather than rewriting all records as soon as a schema evolves.
- **Why it might be new:** CL-Bench B1 proposes typed schema migrations. The distinct operation is a *mixed-schema* store in which individual learned objects move at first write and retain old-reader interoperability throughout the migration.
- **Cheapest test / retention:** Evolve a toy ingredient registry twice with a small rewrite budget. Compare against eager up/down migration and plain lazy translation without write-back. Retest old recipe lookup after each interleaved migration, not just the final state.

### 60. Learnable complements for lossy memory compaction
- **Mechanism:** After merging two summaries, train a complement containing only information needed to reconstruct their separate contributions to currently live clients. Future observations can update the merged summary jointly without destroying the distinctions those old clients still need.
- **Why it might be new:** Residual coding and sufficient statistics are neighbors; the complement is client-conditioned and survives consolidation as a separate writable object, rather than targeting full example reconstruction.
- **Cheapest test / retention:** Merge small class-prototype stores and compare a learned complement to an extra global codebook of the same size. Stream new classes; retest old fine-grained category queries that depend on distinctions lost in the merge.

### 61. Contextual equivalence as a currency for memory reuse
- **Mechanism:** Define observational equivalence under an explicit set of callers. Intern their common view, retaining a small per-object recipe for reacquiring discarded information. When a new caller breaks equivalence, use its distinguishing query to reacquire just that projection and split the new view; old callers keep the canonical object.
- **Why it might be new:** Hash-consing and representation reuse are neighbors. The equivalence class of a learned object is conditional on a growing *language of uses*, not a permanent hash of weights, type signature, or update.
- **Cheapest test / retention:** Intern two running means, retaining only source identifiers; add a quantile caller and allow a bounded fresh sample per source. Compare to permanent deduplication and retaining both histories. Retest earlier mean queries after splitting and measure storage and reacquisition cost.

### 62. Learned reduction orders for nonterminating experience
- **Mechanism:** Learn a strategy for reducing a stream of pending update expressions to normal form under a bounded compute budget. Expensive reductions are delayed when they do not affect the demanded output, but a fairness constraint guarantees old suspended tasks cannot starve.
- **Why it might be new:** Curriculum learning chooses examples; this chooses which *subexpression of a learning operation* to execute next, trading weak-head progress against eventual normal form.
- **Cheapest test / retention:** Give a toy recursive estimator cheap outer corrections and expensive inner refinements, with frequent new streams. Compare learned reduction order to FIFO partial training and greedy loss priority. Retest old refinements for both convergence and worst-case delay.

### 63. Compiler-checked anti-unification of task structure
- **Mechanism:** Anti-unify two task descriptions into their least general common structure with typed holes. Compile old tasks as fixed instantiations, learn only a solver for the new hole values, and reject factoring if the generated old instances cease to be equivalent.
- **Why it might be new:** DreamCoder-style library induction and templates are neighbors. Preserving the exact instantiation maps gives a reusable way to generalize the *space of admissible future tasks* without replacing previously acquired task programs.
- **Cheapest test / retention:** Stream short list-transformation problems with shared structure and progressively harder hole fillers. Compare to generic library search and nearest-task copying. Re-run old programs on held-out inputs, including holes used in more than one position.

### 64. Type-directed cost semantics for retention
- **Mechanism:** Attach to each learned task a composable estimate of worst-case call cost. Treat a task as forgotten if it still returns the correct answer but now exceeds its old latency or tool-use bound; use the inferred cost expression to target only the newly expensive dependency.
- **Why it might be new:** Resource-aware type systems and latency objectives are neighbors. The primitive propagates *old nonfunctional guarantees* through compositional learning rather than bounding global inference cost or measuring old accuracy alone.
- **Cheapest test / retention:** Add an expensive resolver to a tiny learned document workflow. Compare cost-aware rewrites to accuracy-only regression checks and a global latency cap. Retest old answers and worst-case tool calls on old long-tail inputs, where correctness alone would hide the regression.
