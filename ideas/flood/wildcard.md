# Wildcard flood: 60 continual-learning primitives

Five source fields, twelve raw hypotheses each. Treat the cards as ambitious but doable at toy scale; they're mechanisms to review, not novelty verdicts or pilot results. Each starts with a CPU-sized test of the proposed operation, not a claim about production-scale retention.

**Common first-test rule.** Train or write on a prequential stream; seal held-out old and new probes, score old probes before the new stream and after every write, and keep old-task identifiers hidden unless the task itself supplies them. Score each retained cohort separately, including tests of old skills in combination where applicable. Compare at matched persistent bytes and report extra probe, training and inference costs. Toy programs can be the starting learner, but a test in which retention follows from freezing a perfect old branch is only a positive control. For learned or text lessons, add same-length filler and a no-lesson temperature fit only on development tasks. See the [ledger and flood triage](https://github.com/manojbajaj95/cl/pull/6) for earlier candidates and the [stream contract](../../docs/research-process.md) for scaling up.

## Art and material practice

### WC01 · The uncut stencil
- **Mechanism:** Write a lesson as a cutter that carves *new input regions out of the old rule's domain*, using distances to previously learned decision contours rather than absolute coordinates. When old contours move after benign calibration, re-cut in the new relative coordinates.
- **Why it might be new:** The persistent object is a boundary-relative cut, not a frozen router or correction keyed by absolute activations. Level-set methods and local model editing are near neighbors.
- **First test + retention:** On a 2D sector classifier, insert a thin wedge specified relative to two old curves, then shear the feature map. Compare fixed-coordinate patches and patches retrained from the same examples; score the moved wedge and old near-seam sectors, not just distant old points.

### WC02 · Edit an anamorph, not a view
- **Mechanism:** Store the set of coupled latent changes whose projections produce a desired change in one view and no change in others. Later evidence from a different view selects among that set, rather than overwriting the first interpretation.
- **Why it might be new:** A write leaves behind a system of projection constraints that later writes can intersect. Multi-view learning and deferred-commitment weights are close; the wager is that different views constrain a single change enough to avoid saving candidate models.
- **First test + retention:** In a tiny multiview shape generator, correct one silhouette and then revise the inferred depth from another angle. Compare sequential latent regression and equal-byte replay; check the corrected first silhouette and unrelated old shapes from unseen views.

### WC03 · Pentimento operators
- **Mechanism:** A composition stores not just edited components but a minimal recipe for *how later components read the parts that an earlier edit covered*. Repainting the buried component regenerates only that borrowed contribution to the current function.
- **Why it might be new:** The stored artifact is a reusable transformation from a hidden earlier decision into a later dependency, not the previous decision itself. Provenance, program slicing and causal mediation are near neighbors.
- **First test + retention:** Teach a pipeline to classify shapes, then add a color rule that borrows one suppressed shape feature. Correct the buried category and compare dependency transport with replay and full dependency retraining. Rescore unchanged shape classes and the old color cases that should not change.

### WC04 · Grout that learns independently of tiles
- **Mechanism:** Give reusable features oriented boundary ports. Train a directional seam operator only when separately learned tiles first touch; let seams compose to connect a tile pair that was never trained together.
- **Why it might be new:** Adjacency between skills has its own writable parameterization and algebra; it is not just a choice of skill router. Near programs-weights P17 and adapters; the distinctive bet is transfer of a *learned seam* across rearrangements, without shared symbols.
- **First test + retention:** Learn local 2D navigation policies on three textures and seams on two pairings. Predict a fourth seam with the reverse/composition rule; compare direct interface adapters and generic fine-tuning. After a seam correction, retest old interiors and both trained crossings.

### WC05 · Readymade appropriation
- **Mechanism:** Permit the same frozen feature to carry two roles via independent *read transformations* trained on very few demonstrations. Search for reuses by analogy between role behaviors, not by textual names or gradient alignment.
- **Why it might be new:** The update is a new interpretation of an existing feature without an obligation that old and new roles share a meaning. Feature reuse and linear probing are close; compare explicitly with random feature selection.
- **First test + retention:** Repurpose a frozen Sudoku row-conflict detector as the recognizer for repeated chords in a synthetic sequencer. Try feature matching against equal-data probes and random read transforms; then learn collision detection in periodic schedules and check both initial Sudoku and chord accuracy.

### WC06 · Two-sided registration marks
- **Mechanism:** Every learned mapping between an agent's memory store and model activations exports sparse fiducials *on both sides*. Update each side independently, then estimate which fiducials slipped together and apply a single correspondence repair instead of rewriting the lessons.
- **Why it might be new:** Registration is a first-class object that fixes simultaneous drift of the index and the reader without either being the reference. Representation alignment and stable ABI work are close.
- **First test + retention:** Relabel a key store and rotate a tiny encoder with a partially overlapping corruption. Fit registration from eight paired fiducials; compare aligning to either old side alone and replay at equal bytes. Check old routines whose exact key/activation pair never appeared among the fiducials.

### WC07 · Exquisite-corpse interfaces
- **Mechanism:** Train contributor agents with mutually hidden interiors and only a narrow strip of a collaborator's partial output. Continually learn a *completion distribution at the seam* so an unseen replacement can finish the artifact without either agent retraining on the other's whole trajectory.
- **Why it might be new:** The communication primitive is an uncertainty-bearing unfinished artifact, not an instruction, fixed signature or anonymous skill transplant. Split learning and multi-agent conventions are close.
- **First test + retention:** Have two learners fill alternating blocks of procedural sketches; replace one with a new drawing style. Compare partial-stroke continuation with fixed-width messages and joint imitation. Retest original and mixed pairings on unseen outlines.

### WC08 · Relief molds from mistakes
- **Mechanism:** In mechanics where push and pull are dual, fit the *negative shape of a failure*: the least input-side deformation that turns a bad trajectory into a boundary-case success. Cast new task-specific corrections by applying the inverse deformation in other environments.
- **Why it might be new:** A failure can produce a transferable correction without ever observing a successful action sequence for that task. Inverse optimization and hindsight relabeling are close; the bet is that a shared corrective deformation beats per-environment hindsight.
- **First test + retention:** In a linear table-slider simulator, enumerate small perturbations of recorded misses until the first success, then cast corrections on a second surface. Compare fitted inverse dynamics and relabeled trajectories with the same simulator calls; after learning a second mold check old surfaces and previously successful trajectories.

### WC09 · Kinetic mobile weights
- **Mechanism:** Let nodes in a skill graph learn how to rebalance themselves from locally broadcast loads. Add a skill by applying its demand at one attachment point and letting the rest settle; keep separate local stiffness fields learned from old behavior.
- **Why it might be new:** The update is docking plus distributed relaxation, rather than projecting a proposed global delta with a saved old-task gradient. Equilibrium propagation and constrained optimization are near neighbors.
- **First test + retention:** In a linear branching network, attach a new output using only local load messages and equal update steps. Compare a global projection and equal-byte replay. Probe old outputs outside the calibrated attachment cone and count the messages needed to recover them.

### WC10 · Lenticular weights
- **Mechanism:** Learn a skill in the *difference* between two small allowed view perturbations, while ordinary unperturbed outputs stay fluent. The learner reads a paired forward rather than decoding a stored old model or a task tag.
- **Why it might be new:** The storage channel is a learned response to controlled view changes. Nearby: directional derivatives, watermarking and weight-space question barcodes; the latter probe edits, whereas this direction carries a useful policy.
- **First test + retention:** Train a tiny classifier on two interleaved label rules using paired one-pixel input perturbations for the new rule. Compare a same-parameter second head and a learned probe token; measure old unperturbed accuracy and whether later ordinary training erases the new perturbation-carried rule.

### WC11 · Inbetweenable learning
- **Mechanism:** Write an edit as endpoint plus a trajectory whose intermediate models implement identifiable, progressively stronger subsets of the new skill. Define operators for pausing at, composing with, and graduating from a subset.
- **Why it might be new:** A partial write has a semantic contract rather than a weight interpolation coefficient. Mode connectivity and curriculum schedules are close; simple linear interpolation is the obvious control.
- **First test + retention:** Learn three increasingly expressive bracket operations in one edit. Compare a spline of low-rank updates with linear interpolation and sequential adapters. At every intermediate stop, check the intended subset, penalties for premature operations, and held-out accuracy on the previous bracket grammar.

### WC12 · Raking-light restoration
- **Mechanism:** Discover inputs under which two almost-identical forward passes disagree much more than under ordinary inputs. Store the optimized illumination pattern as a procedure for reproducing a threatened *distinction*, not as a replay example or an output checksum.
- **Why it might be new:** The memory generates a contrast conditional on the current reader, and moves the reader back toward being sensitive to it. Active query synthesis and adversarial distillation are close.
- **First test + retention:** Create two rare, visually subtle shape distinctions in a tiny CNN, then learn textures. Compare regenerating contrast probes on demand with static adversarial probes and hard-example replay; score old distinctions on separately rendered images, not the optimized probes.

## Music and performance

### WC13 · Counterpoint updates
- **Mechanism:** Treat a skill as a voice and a write as a move in a score of joint responses. Teach a small set of motion rules for two voices to change in opposite or oblique directions while carrying independently readable information in their timing and relative lag.
- **Why it might be new:** The unit being protected is voice separation over a sequence, not parameter orthogonality at an input. Gradient surgery and independent component analysis are close.
- **First test + retention:** Train two temporal output streams with shared readout bandwidth, then add a third. Compare motion-constrained writes with gradient surgery; score new stream accuracy and both old streams under unseen simultaneous inputs and shifted beat offsets.

### WC14 · Hocketed memory
- **Mechanism:** Split a capability across readers that operate on strictly alternating subsets of the input, passing only a learned continuation state. Teach a replacement part on wholly different data while the rest of the original skill is live.
- **Why it might be new:** The persistent interface is the information carried by *not* playing on successive events; the skill exists in the relay, not in either participant. Recurrent networks and pipeline parallelism are close.
- **First test + retention:** Train two tiny agents to parse alternating tokens of a parity-plus-nesting language. Replace one reader to add new token classes and compare joint fine-tuning and one-reader adapters. Retest original syntax and old/new tokens crossing a relay boundary.

### WC15 · Enharmonic write pivots
- **Mechanism:** Let one internal element have identical current output but two distinct update rules under different structural roles. Learn to use these “same note, different spelling” pivots to transfer an update without transferring the entire context.
- **Why it might be new:** What is shared is a presentation with two valid *learning dynamics*, rather than a feature unchanged across tasks. Context-conditioned meta-learning and role-filler binding are close.
- **First test + retention:** Train a transducer where one symbol acts as either delimiter or operand with identical single-step output. Introduce a grammar modification through that token and compare with global token edits and context adapters; test the old role on unseen strings and the new role on unseen contexts.

### WC16 · Cadences that settle a write
- **Mechanism:** Keep streaming credit in a structured state. Emit small *closing phrases* that identify which pending eligibility chain completed; resolve only that chain and leave partial phrases open to extension or correction.
- **Why it might be new:** A learned action suffix makes credit addressable by a semantic closure event rather than by a timestamp or terminal reward. Reward machines, eligibility traces and deferred-commitment weights are close.
- **First test + retention:** Interleave two synthetic craft recipes with delayed feedback and shared endings. Compare learned closure phrases with hand-built temporal credit and eligibility traces under equal bits. Then introduce an overlapping third recipe and retest completion and credit assignment for both old recipes on new interleavings.

### WC17 · Learn a temperament, not a key
- **Mechanism:** Learn a small shared “temperament” that deforms exact feature ratios. Each skill supplies tolerances on those ratios, so adapting to new scales can be achieved by retuning common intervals rather than patching each player.
- **Why it might be new:** The primary learner state is a slack-bearing system of approximate equalities among feature distances. Relative position, shared metrics and constraint solving are close.
- **First test + retention:** Train a few motif recognizers whose interval requirements cannot all be exact on a quantized grid; add previously unsupported scales. Compare retuning jointly with independent scale normalization and fine-tuning; measure held-out loss on every old scale, including the most detuned one.

### WC18 · Prescriptive ornaments
- **Mechanism:** Distill a new skill into a local transformation on a well-learned action sequence: add grace actions, split one action or delay its release. Re-evaluate the ornament against the current base sequence each time the base changes.
- **Why it might be new:** The learned object is an operation on *how a skill unfolds* that can migrate to a new base without copying the original policy. Options and program rewrite rules are close; transfer to an unrelated sequence is the bar.
- **First test + retention:** Teach an agent to add a safety recheck to two toy assembly routines, then learn a third routine and change the first one's tool order. Compare with storing finished policies or invoking a generic check everywhere; retain unornamented proficiency and completion on the original tasks.

### WC19 · Timbre-preserving instrument swaps
- **Mechanism:** Store per-skill transformation of a standardized “excitation” action into a measurable trace envelope. When a tool changes, find a new way to reproduce the envelope rather than matching tool inputs or replaying exact old outputs.
- **Why it might be new:** Envelope equivalence allows some differences in low-level behavior that policy distillation penalizes, but retains dynamics that final-task success misses. System identification and inverse tools are neighbors; the proposal is not to learn a tool inverse from logged inputs.
- **First test + retention:** Replace the motion tool in a small cursor environment with one that adds inertia. Match envelopes from single pulses and compare against inverse dynamics and terminal reward. Rescore held-out old navigation routes and transition profiles for unrelated tools.

### WC20 · Call-and-response writes
- **Mechanism:** The writer supplies half of a learned contrast; the recipient's own proposed response generates the missing half and determines the actual update. Memory is the pairing rule, not a static lesson to retrieve.
- **Why it might be new:** The same transmitted signal can make recipient-specific, complementary edits without access to source weights. Self-distillation and active teaching are close; compare to simply transmitting the best teacher example.
- **First test + retention:** Give two tiny parsers different systematic confusions. Send the same synthetic cue to both and train on their generated contrast pairs; compare equal-token static demos. Then add another ambiguity and rescore each parser's original and newly corrected grammar.

### WC21 · Rests as observations
- **Mechanism:** Learn an explicit, outcome-labeled “nothing was played here” operation that writes only when an expected event is missing, while censoring windows in which the learner could not have observed the event.
- **Why it might be new:** A deliberate absence can carry reusable change information without being encoded as a negative example everywhere. Survival models and censored bandits are close; the transfer target is the same absence operator under a different observation pattern.
- **First test + retention:** In a 20-state event simulator, remove one periodic cue and add irregular observation dropout. Compare learned rests to no-event flags and a censor-aware hazard model; test old intact schedules and old “not observed” behavior after adapting to the new schedule.

### WC22 · A rehearsal score with movable tempo
- **Mechanism:** Store a skill's internal checkpoints as qualitative phase crossings; learn progress-dependent local time warps when work speeds up or stalls. Tempo changes the pace of learning and execution without renumbering the skill's semantic events.
- **Why it might be new:** One durable phase object aligns streaming credit, partial plans and replay, not just trajectories after the fact. Dynamic time warping, phase-variable policies and SMDPs are close.
- **First test + retention:** In a timed sorting simulator, change dwell times and delay one step unannounced. Compare phase-local adaptation with DTW-aligned replay and an SMDP baseline. On old timing distributions, measure ordinary completion and correct recovery from previously learned stalls.

### WC23 · Rubato budgets
- **Mechanism:** Define writes that may borrow capacity from a later step but must repay it at the next phrase boundary; let fast within-phrase variants practice while outer phrase behavior stays in time. The learned variable is where to borrow and what repayment move works.
- **Why it might be new:** A retention debt is assigned to a semantic synchronization point and repaid by another skill operation, not by an LR budget. Plasticity credit lines and bounded-delay scheduling are known repo neighbors.
- **First test + retention:** In a two-stage sequence transducer, adapt to a delayed token by shifting hidden-state work between stages. Compare matched global slack and fixed per-stage capacity. Check both transient and end-of-phrase old correctness under novel delay patterns, including a second write before repayment.

### WC24 · Sympathetic vibration
- **Mechanism:** Give each module a trainable response curve to short drive signals. Rehearsing one skill with a deliberately shaped drive excites neighbors that share dynamics, exposing when their learned responses have fallen out of tune.
- **Why it might be new:** A practice event carries an active resonance probe for multiple other skills instead of retrieving their examples one at a time. Near multi-task distillation, control frequency-response identification and coded probes; response overlap must predict useful transfer, not just covariance.
- **First test + retention:** Train small recurrent filters with overlapping spectra; rehearse one under a learned drive and compare equal-compute independent replay and a random drive. Score all old filters at held-out frequencies after new filters arrive; check the effect disappears for disjoint spectra.

## Linguistics

### WC25 · Suppletive skill families
- **Mechanism:** Learn a common abstract operation together with residue rules that allow entirely different implementations in irreducible contexts. Later, revise the abstract operation and ask each implementation to satisfy it using its local primitives, without requiring a shared parameter direction.
- **Why it might be new:** Two unrelated implementations can count as the *same writable skill*. Polymorphism, multitask distillation and hierarchical skill inheritance are close; the difficult case is discovering the shared revision from a single implementation.
- **First test + retention:** Teach list reversal in a stack DSL and a cursor DSL, then change the treatment of one sentinel using stack examples only. Compare shared embedding and separately written policies; test transfer of the edit to the cursor and old sentinel-free and unrelated DSL tasks.

### WC26 · Syntactic islands for gradient flow
- **Mechanism:** Learn scopes whose internal gradients cannot escape *via specified use paths*, but remain writable when the same module is used outside an island. Implement the rule as a path-conditional backward operator rather than a per-weight mask.
- **Why it might be new:** The write boundary is a particular occurrence of a module in a derivation. Stop-gradient, context-conditioned adapters and OGP are close, but none of those comparators needs path-selective updates to reused parameters.
- **First test + retention:** Reuse a small arithmetic module both directly and under quoted subexpressions. Add a contextual operator; compare path-conditioned gradients, global masks and matched adapters. Check untrained quoted expressions, direct old expressions and direct/quoted mixtures.

### WC27 · Garden-path plasticity
- **Mechanism:** Retain *unused factor assignments* from the first parse of an experience. If later feedback shows the parser took a garden path, rebind its accumulated local update statistics to the alternate factors rather than run experience through the whole learner again.
- **Why it might be new:** Learning reanalysis can be an operation on sufficient statistics rather than on model snapshots or raw experience. Online EM and deferred commitment are close; the wager is correct reassignment after multiple already-committed writes.
- **First test + retention:** Stream partially disambiguated strings from two finite-state grammars with late disambiguators. Compare reassignment, online EM and equal-byte experience replay; check held-out strings from the earlier grammar and count falsely reassigned old sufficient statistics.

### WC28 · Lexical blocking as a learned interaction
- **Mechanism:** Learn a blocking relation from an attested exception to *other possible expressions of its meaning*. That relation edits the shared generator's productive rule on nearby inputs, while allowing the excepted operation when explicitly quoted.
- **Why it might be new:** A single learned item carries an inference-time shadow over unobserved alternatives, instead of only occupying a high-priority lookup key. Exception dictionaries and unlikelihood training are close.
- **First test + retention:** In a nonce-language inflector, teach irregular forms and reveal later dialects where specific alternates remain legal. Compare exception lookup plus unlikelihood and analogical blocking. Score novel stems in old regular classes, remembered irregulars, and correctly quoted blocked forms.

### WC29 · Invent arbitrary agreement classes
- **Mechanism:** Assign newly learned skills arbitrary latent classes and require skills that compose well to agree through one of several slots. Reassign classes as evidence about composition arrives; preserve classes through permutations using compatibility, not class names.
- **Why it might be new:** Artificial morphology lets the learner express a low-bit combinatorial rule about *which learned operations can compose*, even when no semantic label separates the classes. Learned typing and feature hashing are close.
- **First test + retention:** Learn twenty toy robot commands with latent interface conflicts. Compare learned redundant agreement slots with hashed tags and dense pair scoring at equal bytes. Test unseen pairs involving new commands and hidden old-old combinations after reclassification.

### WC30 · Anaphora over writes
- **Mechanism:** A learned action can refer to “the mechanism I just changed in that case.” Bind a later update to the causal *role* of an earlier write, then resolve it to the current implementation using small interventions. No old weight snapshot is the referent.
- **Why it might be new:** Writes become referents in subsequent learning instructions, with reusable semantic pronouns instead of parameter addresses or commit IDs. Program slicing, referential games and typed weight linkers are close.
- **First test + retention:** Teach a tiny classifier conditional feature uses, refactor its feature assignment, then issue a follow-up “apply that change also when X.” Compare activation similarity and stored indices. Check held-out instances of the referred change and unrelated old feature uses.

### WC31 · Harmony across a patch chain
- **Mechanism:** Assign a learned “vowel” state to updates, with local propagation making adjacent edits select compatible implementations even when neither can observe the other's task. Change one edit's realization and allow the harmony wave to update its neighbors.
- **Why it might be new:** A learned constraint propagates through the *realizations of writes*, not through the task outputs. Constraint propagation and module linking are near; the interesting case has multiple valid realizations and no global interface standard.
- **First test + retention:** Give each stage in a four-stage transducer two equivalent internal encodings; add a stage whose write fixes one encoding. Compare local harmony, full re-synthesis and fixed global channels. Retest all old compositions through changed and untouched stages using secret inputs.

### WC32 · Cancellation of accommodated premises
- **Mechanism:** When an episode only makes sense under a missing premise, install an explicit provisional premise with consumer-specific contribution paths. A later cancellation subtracts only the extrapolations licensed by that premise, not everything learned in the same episode.
- **Why it might be new:** A presupposition is a separately editable cause of generalization across otherwise unrelated updates. Belief revision and counterfactual sparse rollback are close; mixed-origin skills are the point of departure.
- **First test + retention:** Stream scheduling tasks implying a shared, initially unstated opening time. Later reveal it was exceptional. Compare episode retraction and belief-state replay with premise cancellation; test older unaffected bookings and cases with independent evidence for the original opening time.

### WC33 · A quotative training channel
- **Mechanism:** Learn to simulate an observed lesson or policy “in quotation” without allowing it to directly train default behavior. A learned unquoting operator promotes only transformations that survive applying the same quote to multiple independent situations.
- **Why it might be new:** Quotation is a write mode that makes a policy executable without making it normative; promotion consumes a behavior difference across worlds. Shadow policies and offline imitation are close, as is the ledger's promotion work; test quote-swap independence, not frequency of rediscovery.
- **First test + retention:** Feed a tabular dispatch learner transcripts from two demonstrators with different local conventions. Quote both, then promote a shared lawful ordering; compare source conditioning and balanced imitation. Test pre-stream dispatch, quoted local rules, and the absence of accidental adoption on default probes.

### WC34 · Resegment without changing the performance
- **Mechanism:** Keep the learner's own skill boundaries editable. When a repeated suffix starts occurring independently, split old composite updates at that boundary and migrate the suffix's learned variation into a shared write unit while maintaining the observed behavior.
- **Why it might be new:** Unit discovery is applied to the boundaries of *prior learning operations*, allowing later examples to change the granularity at which old knowledge is editable. BPE, hierarchical options and OO refactoring are close.
- **First test + retention:** Stream symbol transductions where two fixed macro commands later expose a shared suffix on a new stem. Compare BPE-style segmentation of demos, append-only skill libraries and update resegmentation. Retest old full macros and their mixtures, then ask one suffix correction to transfer to both.

### WC35 · Evidential conjugators
- **Mechanism:** Parameterize updates as a common content operator conjugated by how the evidence was obtained: direct trial, deduced consequence, or repeated report. Learn cancellation laws so repeated copies can alter confidence without reenacting the content write.
- **Why it might be new:** Evidential source changes the *kind of learning operation*, not just its scale or priority. Bayesian evidence fusion, idempotent learning operators and provenance tags are near neighbors.
- **First test + retention:** Teach a small relation model new facts with duplicate hearsay plus one contradictory direct trial, withholding duplicate IDs. Compare source-weighted SGD and explicit provenance deduplication at equal state. Check old directly verified facts and independently replicated facts with identical wording.

### WC36 · Referents with movable spatial loci
- **Mechanism:** Give an agent a transient relational coordinate frame for references such as “that subgoal's teacher,” but consolidate how to remap the frame, not the individual referent. A new task teaches a frame-changing operation that prior policies can use.
- **Why it might be new:** The learner retains *motions of bindings* across tasks, rather than names or task-conditioned slots. Object files, equivariant representations and role-filler binding are close.
- **First test + retention:** Use a small grid with roles assigned in arbitrary visit order and mirrors that swap inferred roles. Teach a remapping from a few examples; compare relational graphs and coordinate augmentation. Retest old relational commands on unseen layouts, including old commands nested under the new frame change.

## Law and procedure

### WC37 · Teach the holding, not the disposition
- **Mechanism:** On each adjudicated case, write the smallest learned feature interaction that separates it from incompatible earlier cases. Keep alternative explanations as nonbinding “dicta” that can predict, but cannot resolve future conflicts by themselves.
- **Why it might be new:** Case memory has two distinct inference powers for explanations from the same data. Case-based reasoning and exception lists are close; unseen distinctions must outperform matched nearest cases.
- **First test + retention:** Stream 2D rules where identical dispositions rest on two different conjunctions; later reverse one conjunction. Compare nearest cases and rule-list revision, then test boundary cases combining facts from the changed and unchanged holdings.

### WC38 · Appellate remedies as a label alphabet
- **Mechanism:** Give the learner structured feedback that distinguishes “wrong interpretation, rerun your procedure,” “right interpretation, wrong action,” and “sound result for a bad reason.” Train different local updates for each remedy without supplying the correct result.
- **Why it might be new:** A feedback type specifies which *operation on learning* is admissible, rather than just crediting a component or adding a preference score. Trace credit, hindsight correction and process rewards are close.
- **First test + retention:** In a tiny packing DSL, inject parser, heuristic and executor errors; send only a remedy category. Compare TextGrad-style feedback and scalar preference at equal bits. Test new error combinations plus old packing classes that share the affected stages.

### WC39 · Severability as elastic skill compilation
- **Mechanism:** Compile a learned policy together with a small family of *well-formed residual policies* generated by excising specific clauses. Future evidence can select a residual without claiming that removing a clause undoes the entire old gradient.
- **Why it might be new:** A write installs its own partial validity semantics, including how to reconnect the remaining pieces. Unlearning and program repair are close; this is neither an inverse update nor ordinary independent adapter removal.
- **First test + retention:** Train a few rule DAGs with both cyclic dependencies through state and valid shortened paths, then invalidate one clause. Compare dependency pruning, rule replacement and per-clause adapters. Without re-solving from scratch, retest old cases whose derivations crossed the clause but whose correct outcomes are unchanged.

### WC40 · Standing to modify a mechanism
- **Mechanism:** Before a new event can change a shared rule, infer whether the evidence would have changed if that particular rule had changed. It receives standing only on mechanisms it can discriminate; collect one low-cost intervention when two mechanism effects are aliased.
- **Why it might be new:** Access to a write is a learned *relation between evidence and mechanism*, not a global trust weight. Active causal diagnosis, probe-before-write and influence functions are close; the bet is that standing learned in one domain can adjudicate evidence in another.
- **First test + retention:** Use two agents with different product prices and sensor calibrations in a tiny market simulator. Transfer which observations license a price vs. sensor write, compare intervention-matched active diagnosis, and retest old prices and calibrated sensors after the unannounced confounded change.

### WC41 · Reliance damages
- **Mechanism:** When a shared primitive changes intentionally, compensate consumers by injecting an equivalent capability elsewhere in their dependency chains, rather than preserving obsolete upstream outputs or retraining all consumers. Learn which compensation permits old callers to keep their choices.
- **Why it might be new:** Retention can be measured and repaired at a consumer's *decision*, even when its old inputs must legitimately disappear. Backward compatibility and counterfactual repair are close; the proposed relocation acts downstream of the changed primitive.
- **First test + retention:** Change units and rounding in a shared price tool; some downstream choice rules depended on an old rounding boundary. Compare upstream wrappers and endpoint fine-tuning. Check held-out old purchasing choices that should remain valid and current calculations that must use the new rule.

### WC42 · Binding facts and open issues
- **Mechanism:** Decompose feedback into findings about reusable latent facts and rulings about how those facts map to a particular action. A confirmed finding can settle a later application without transferring the old action label; a rejected ruling leaves the finding intact.
- **Why it might be new:** A single supervision event can release future labeling budget for a learned subissue without fixing a whole skill or explaining its reasoning. Partial labels, disentangled dynamics and reusable subgoals are near.
- **First test + retention:** Stream small games reusing hidden movement constraints and switching victory rules; a teacher can certify either constraint or ruling at the same cost. Compare multitask partial labeling. Retest old games and old movement constraints in never-before-seen victory-rule combinations.

### WC43 · Burden-shifting updates
- **Mechanism:** A write produces a short witness and a declared locus of uncertainty. Later writers can narrow their search by treating the witnessed part as established, but can invert the burden by supplying a cheap counter-witness that forces only the relevant portion open again.
- **Why it might be new:** The write can change *who must furnish what evidence* on future updates; this differs from a static proof obligation or sequential accept/reject gate. Proof-carrying code, CEGIS and Bayesian sequential tests are close.
- **First test + retention:** Teach unknown inequalities in a constraint agent, then provide a counter-witness to one derived boundary. Compare fixed proof checks and CEGIS at equal query budget. Retest old entailed inequalities and old points near the reopened boundary that remain legal.

### WC44 · Rules of evidence for update composition
- **Mechanism:** Assign an edit a provenance *expression*: add alternative sources, multiply sources that are jointly required, and make repeated root evidence idempotent. Identical gradient vectors learned from different paths can then compose differently; revising a root disables only update terms that no longer have support.
- **Why it might be new:** The update algebra is provenance-sensitive even for behaviorally indistinguishable edits. Provenance semirings and influence propagation are close; unlike evidential conjugators (WC35), this operates on chains of already-learned edits.
- **First test + retention:** Make two chains of two symbolic updates with identical endpoint functions, one using independent evidence and one duplicating a root report. Introduce a correction to that root, compare semiring-backed write composition versus lineage-keyed replay, and retest independently acquired old behavior and duplicate-derived behaviors still supported by a separate source.

### WC45 · Prospective overruling
- **Mechanism:** Separate a rule's applicability clock from the decision's creation clock. A new write learns a narrow *transition rule* for old commitments and new applications of one model, rather than retaining the earlier model for all dated queries.
- **Why it might be new:** The persistent object is a migration policy for commitments that cross a regime boundary, not a dated rule or prompt-addressable checkpoint. Temporal QA and schema migration are close.
- **First test + retention:** Change a booking policy with old confirmed and tentative bookings under different migration clauses. Compare a time-indexed rule cache plus a handwritten cutoff. Test old commitments carrying forward, fresh cases under the new rule and cases whose old booking facts never changed.

### WC46 · Amicus updates
- **Mechanism:** Give another skill no access to the disputed examples, but permit it to submit the *experiment it wishes the learner would run*. The receiving skill runs comparisons and updates itself; the amicus gets credit only for distinctions that transfer to other learning disputes.
- **Why it might be new:** Skills exchange experimental designs that reshape each other's update opportunities, not their outputs, gradients or lessons. Active teaching and causal query planning are close; distinctively, another learned skill originates the question without reading the case.
- **First test + retention:** In a rule learner deciding whether color or position matters, let a previously learned counting skill recommend interventions using only a compact confusion summary. Compare random, mutual-information and self-proposed experiments. Check old counting and old unconfounded rule applications.

### WC47 · Equity through remedy, not rule replacement
- **Mechanism:** Learn an exception as a short *remedial action* after the standard rule fires, chosen to undo its local adverse side effect without altering the main output. Reuse the remedy wherever the same side effect is observed.
- **Why it might be new:** What generalizes is mitigation of a side effect caused by an old skill, not an input exception or an alternate rule. Residual RL and constrained policies are close; transfer should follow effects rather than the original exception's surface context.
- **First test + retention:** In a toy assignment agent, learn to reallocate unused slots after the base scheduler creates an orphan request. Compare input-keyed exceptions and a residual policy. Check held-out ordinary schedules and old schedules with different orphan mechanisms.

### WC48 · Chain of title for writable capabilities
- **Mechanism:** Split permission to use a capability from permission to *delegate a future write* on it. Delegation is itself a learnable operation that carries enumerated invariants to successors across source-model handoffs.
- **Why it might be new:** Learning authority can be transferred and recomposed independently of capability transfer. Object capabilities, proof-carrying edits and adapter ownership are near; the test is whether invariants bind after delegation without source snapshots.
- **First test + retention:** Let two toy learners hand implementation responsibility for two shared parsers to a third learner, then ask it for a cross-parser extension. Compare hard ownership and regression-only updates. Retest old use, delegation outside scope, and whether old valid parses survive a subsequent handoff.

## Sports and games

### WC49 · Curling writes into the path
- **Mechanism:** Learn a temporary modification of the environment only where a future action is expected to travel, rather than modifying that future policy. With a world model, write a short-lived, path-indexed perturbation to simulated transitions and train the agent to use or ignore the altered corridor.
- **Why it might be new:** A reusable skill can reside in a *prepared trajectory corridor* rather than the acting agent. Stigmergy, environment design and shaping are close; the corridor changes transitions, not reward or the actor's observations.
- **First test + retention:** In a tabletop simulator, let a sweeper change friction in four cells before a frozen striker acts. Compare conditioned policies and pre-action tool setup; after new target placements, check old trajectories with no sweeping and with previously learned sweeps.

### WC50 · Fosbury writes change the optimization chart
- **Mechanism:** When progress stalls, learn a coordinate transformation on an existing behavior's progress variables. Use a few task successes to choose a chart, then update from progress measured in that chart even where the old chart's signal is reversed.
- **Why it might be new:** The object exported by a successful outlier is a reusable *change of learning coordinates*, not a high-reward trajectory or a new base policy. Meta-learned rewards, curriculum and archive methods are close.
- **First test + retention:** In a 2D obstacle course, a successful detour initially moves away from the goal in the usual distance metric. Extract a reusable chart from one solution, then transfer to held-out detours; compare demonstrations and learned shaping. Check old direct routes for new stalls and excess path cost.

### WC51 · Climbing beta as load cones
- **Mechanism:** Store a skill step as a range of wrenches or transition forces that make it feasible, not as a waypoint or commanded movement. Compose learned load cones at shared support states and revise a cone from failed transfers.
- **Why it might be new:** Continual learning takes place in a space of admissible support relationships, which can be reused after the actuator or geometry changes. Affordances, contact planning and successor features are near.
- **First test + retention:** Use a 2D point climber where holds afford directional reaction forces. Transfer from two layouts to a rearranged wall with identical local cones; compare waypoint library and goal-conditioned policy. After adding a sloped hold, check old routes including unseen permutations of old holds.

### WC52 · Off-ball actions for learnability
- **Mechanism:** Train an auxiliary player to change what the rest of the team can learn from a shared reward without changing what they see or how they update. It runs interference during a short setup phase, then the team learns under the new interaction pattern.
- **Why it might be new:** An agent's action is a learning intervention on another agent *through the game*, not a message or a direct teacher probe. Experimental design and teammate shaping are close; the distinctive target is fewer aliased credit assignments at matched team reward.
- **First test + retention:** In a two-on-one passing grid, learn a screen that makes reward distinguish timing errors from receiver-selection errors. Compare fixed screens, random moves and reward-maximizing help. Remove the auxiliary after training and test old solo passing and previously learned passing routes.

### WC53 · A deductions grammar
- **Mechanism:** Factor failure feedback into local deductions that each score a transition between reusable primitives. When a scoring rubric changes, learn a mapping from behavior to the new deductions and recompose old primitives without relearning their execution.
- **Why it might be new:** What is editable is a reusable vector of *fault semantics* whose effect depends on neighbors, rather than one reward head per task. Reward machines, successor features and process supervision are close.
- **First test + retention:** Use a 5-move acrobatics simulator with deductions for particular landings and their follow-throughs. With equal labels, compare decomposed credits with successor features and scalar rewards after a rubric change. Retest old routine execution and old deductions on held-out sequences under the old rubric.

### WC54 · Draft-breaking lessons
- **Mechanism:** Learn a recovery operator from the paired difference between trajectories executed in another policy's protective wake and trajectories run alone. Later, attach the operator only where a different leader's protection disappears.
- **Why it might be new:** The content is a measured skill dependency on someone else's presence and an executable remedy, not the successful cooperative strategy. Robust MARL, residual control and policy distillation are close.
- **First test + retention:** In a simple cycling simulator, pair the same start with and without a lead rider. Train a wake-loss operator and compare residual RL and generic disturbance augmentation. After changing the lead rider, verify old drafting, old solo pacing and recovery under a novel headwind.

### WC55 · Change ends before learning
- **Mechanism:** Make a learner's write a two-leg operation: play under one orientation, switch sides or exchange roles, and update from the paired component that does not switch with the nuisance. Keep the side-specific remainder as an explicit nuisance model rather than throw it away.
- **Why it might be new:** A deliberately exchanged *experience pair*, not an augmented copy of one observation, is the unit of learning. Cross-over designs, domain generalization and active diagnosis are close; the learner chooses which reversal merits a charged second leg.
- **First test + retention:** In a tiny tennis simulator, court ends alter power and only one player's timing changed. Compare online paired reversal with mirrored augmentation and random extra trials; score first learning of the timing change and old shots from each end with unseen wind.

### WC56 · Compulsory figures as executable standards
- **Mechanism:** Old skills export small procedures that generate *different legal performances* of the same old requirement. New learning may change which performance satisfies a standard; measure the closest legal performance, then update the standard if its generator can no longer express valid alternatives.
- **Why it might be new:** A retention witness is an editable set of feasible behaviors, not a frozen prediction target. Behavioral cloning with multimodal teachers and specs are close; the generator is run against a new downstream constraint.
- **First test + retention:** Teach a glider to draw compliant curves with several legal radii, then restrict one actuator. Compare fixed-trajectory distillation and reward-only adaptation. Probe old figure legality, old comfort constraints and new geometry without allowing a degenerate single repeated trajectory.

### WC57 · Match-play concessions
- **Mechanism:** A learner can offer a claimed performance bound and let a teacher concede or contest it. Only the first contest produces a detailed example; align updates with the *difference between claimed and contestable regions* instead of treating conceded items as labeled positives.
- **Why it might be new:** A bounds-and-challenge protocol uses almost-free messages to change the kind of later supervision; a concession is not a check of exact behavior. Selective classification and active learning are close.
- **First test + retention:** In a continuous putt simulator, ask whether a claimed distance band is acceptable; receive one counterexample only when contested. Compare uncertainty queries and binary labels at equal teacher effort. Retest long- and short-putt accuracy on old surfaces after learning a new slope.

### WC58 · Relay handoffs transfer update responses
- **Mechanism:** Hand off a skill by sending a few perturbation/response pairs describing *how it should change* when conditions vary. The receiver fits its own learning rule to those response pairs rather than importing weights, optimizer moments or old trajectory data.
- **Why it might be new:** Transfer targets the local input-to-update response in behavior space, which different architectures can realize differently. Learned optimizers, policy distillation and SM25 optimizer inheritance are close; the handoff can succeed without sharing any optimizer coordinates.
- **First test + retention:** Hand off a lane-following task from a linear controller to a tiny MLP using three induced slope changes. Compare matched trajectory transfer and fresh adaptation. After adapting to a fourth slope, measure old lanes and response to an old perturbation on held-out starts.

### WC59 · League cycles as compressed learning state
- **Mechanism:** Continually infer a minimal directed-cycle decomposition of which strategies improve against which opponents. New play updates a cycle, letting the learner recompute robust mixtures without keeping or retraining every historical opponent.
- **Why it might be new:** The unit retained is an intransitive relation between skills, not an archive member or a mean payoff. PSRO, Nash averaging and games decomposition are close; a sparse cycle must predict an unplayed historical matchup.
- **First test + retention:** Stream small payoff matrices that extend rock–paper–scissors with hidden subcycles. Compare cycle updates to reservoir leagues and low-rank payoff completion. Test exploitability versus withheld old strategies and old cross-cycle mixtures after the newest strategy arrives.

### WC60 · Handicaps that train the missing move
- **Mechanism:** Give a learner a small number of oracle substitutions per episode. Periodically remove one substitution to identify the smallest unassisted subproblem that still fails; use the resulting dropout pattern to pick which local edit to learn, then retire the handicap once the edit works.
- **Why it might be new:** The supervision object is a measured obstacle to removing assistance, not the assisted trajectory, uncertainty or raw teacher advantage. DAgger, intervention-based teaching and curriculum are close.
- **First test + retention:** In a synthetic obstacle-course game, allow two oracle moves per episode. Train on where interventions cease being necessary; compare with random and oracle-advantage interventions at equal calls. Remove handicaps and check old courses, new bottlenecks and old skills composed with the new move.
