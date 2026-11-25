# Immunology and development idea flood

64 unranked, speculative continual-learning cards for models and agents. The biology supplies analogies; all proposed mechanisms and tests are computational. "Novelty bet" identifies the reusable object or operation, not verified priority. Each card is ambitious but has a CPU-sized first test; none has been run.

**Shared test contract.** On an A→B→… stream, take a read-only score on fixed, held-out A probes just after learning A and again after each subsequent wave. Report the per-task change and worst old-task delta alongside the named new-learning result. No task labels at inference unless they are part of the task; label such an arm an oracle otherwise. Use the same persistent bytes, examples, model calls, or compute for the closest control where possible; count the added state and calls on both sides. Use separate training and retention probes. For any later text-memory version, add same-length filler and a temperature-matched no-memory arm.

**Scope.** Skimmed the [idea ledger](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md), [flood triage](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md), and the [neuro-bio flood](https://github.com/manojbajaj95/cl/blob/devin/1795538372-neuro-bio-idea-flood/ideas/flood/neuro-bio.md). These cards are not variants of prompt-addressable checkpoints, round-trip consolidation, or seed-log reconstruction. Nearby mechanisms are named where useful for review.

## I. Evidence that authorizes a write

### ID01 · Cross-presented edits

- **Mechanism:** A trainer makes a private update from an episode; two independently implemented frozen readers render its effect as before/after predicate pairs. Future consumers see only the effect pairs and bind them to their own executable writes, without reading the episode or accepting the producer's patch.
- **Novelty bet:** Learn from observed changes in another learner's behavior, with a separate presentation interface that strips its implementation. Near: behavioral distillation and probe-before-write; the object is a translated intervention, not a teacher output.
- **First test:** A lookup agent teaches a DFA learner an exception via effect pairs. Introduce a sender-only nuisance bit and compare sample efficiency to output-only distillation and direct rule transfer at the same query budget. Recheck the DFA's old acceptance and rejection languages.

### ID02 · Split witness join

- **Mechanism:** Store an unlabeled observation and a separately generated outcome as half-witnesses with a shared event key. A writer commits only the change identified by their join; use conflict among multiple valid pairings as a signal to collect more evidence, not to choose one by confidence.
- **Novelty bet:** Address learning by an identity join between evidence sources that are individually consistent with several different writes. Near: delayed-label buffers; the buffer here can expose unresolved pairings even after both sources have arrived.
- **First test:** Interleave two partially observed bandits, with batched reward reports that occasionally alias. Compare exact partial-witness joins to equal-byte FIFO matching and confidence gating; measure wrong arm reassignments and recheck old contexts with the original reward map.

### ID03 · Three-role write licenses

- **Mechanism:** A proposal names a reader, a writer, and a downstream dependent. The dependent returns a minimal contract it needs preserved; the writer emits a change keyed to that contract, and the reader tests it. Compose licenses by intersecting contracts, not by voting.
- **Novelty bet:** A write permission is a consumable, dependent-issued object that changes the update itself. Near: effect types and design-by-contract; the dependent learns which invariant warrants a license.
- **First test:** In a three-tool spreadsheet simulator, change an input representation while two consumers disagree on what can vary. Compare against propose-then-rollback and a fixed assertion set at equal tests. Recheck old formulas using each consumer independently.

### ID04 · Linked recognition across effects

- **Mechanism:** Let one learner recognize a trustworthy episode and endorse an otherwise unrecognized local effect only if both behaviors are causally tied to the same controlled event. Persist the link's witness, not the episode's global trust score.
- **Novelty bet:** Trust transfers along an experimentally linked edge, not to every feature or lesson co-occurring with a trusted cue. Near: causal provenance and semi-supervised co-training.
- **First test:** In a key-value tool toy, one observer recognizes a schema transition and another learns its value-normalization rule. Hold out counterexamples where adjacent events co-occur but are not linked. Compare to per-source trust and co-occurrence; recheck legacy schema queries.

### ID05 · Missing-self invariants

- **Mechanism:** Attach a benign sentinel operation to each component's interface. A monitor learns where that operation is obligatorily reachable and opens a localized diagnostic only when a formerly present sentinel disappears, even if task outputs still look normal.
- **Novelty bet:** Absence of an expected *reachable behavior* becomes a learning signal rather than treating evidence as increased loss or novelty. Near: canary tests; learn the region where absence is informative, not a universal trigger.
- **First test:** Use interchangeable parsers whose output labels initially agree but whose normalization helper occasionally disappears. Compare learned conditional sentinel checks to fixed canaries and output residuals, then recheck old valid and invalid inputs after repairs.

### ID06 · Partial-agonist edit spectrum

- **Mechanism:** For one write recognizer, train probes that selectively open evidence collection, staging, or commitment without opening the other steps; interventions on recognized features map the writer's reachable states.
- **Novelty bet:** A write recognizer has a vector of dissociable effects, not a scalar relevance threshold or a sequential extra verifier. Near: multistage gating and physics #21; diagnostic partial activation, not added delay, is the proposed operator.
- **First test:** On synthetic intent changes, hold out cue combinations in which one cue should cause probing and another should cause staging but neither should commit. Compare gate-state prediction and bad writes to a width-matched scalar gate; recheck old intents and their ambiguity cases.

### ID07 · Coincidence receptive fields

- **Mechanism:** A learner keeps two independently clocked event channels and can learn a write address as a pattern of lead/lag across them. Once the pattern is found, the address selects a specific operation rather than merely raising a global step size.
- **Novelty bet:** A learned relative-time receptive field addresses future updates; unlike phase-coded credit (NB10), it discovers a relation among external streams, not a code assigned to internal computations.
- **First test:** Make identical event marginals identify opposite rule changes when their order reverses. Compare lag-selective writes to windowed classifiers and equal-state timestamp lookup on unseen rates; recheck old contexts where events remain unpaired.

### ID08 · Scope by joint occupancy

- **Mechanism:** Bind a proposed edit to two or more weak cues only when they coexist at a single inferred entity or graph node. Store the binding relation so similar cues scattered across different entities do not invoke the edit.
- **Novelty bet:** A memory address is a variable-bound tuple with a joint-occupancy condition, not a concatenated similarity key. Near: unification and conjunctive retrieval; treat the relation itself as what online feedback writes.
- **First test:** Teach changing rules on a symbolic two-object manipulator and scramble cue ownership at evaluation. Compare with equal-size embedding retrieval and a hand-built conjunctive router. Recheck previously learned object-relation rules after each addition.

## II. Repertoires that keep learning

### ID09 · Fork responders at the fault line

- **Mechanism:** When one responder works on old contexts but fails on a narrow new seam, split the *difference of its responses* into child increments. Learn where the increments diverge, with the parent left writable for effects shared by both.
- **Novelty bet:** Clone bookkeeping represents a local response contrast and routes shared evidence upstairs, not two snapshot experts. Near: hierarchical MoE and residual trees; distinguish specialization by counterfactual response divergence.
- **First test:** Stream punctuation-sensitive symbol transforms to a depth-2 decision DAG. Compare learned contrast forks with a node-split tree and two separate experts of equal size. Recheck old delimiter variants as well as the parent transform on untouched inputs.

### ID10 · Selection on the recognition boundary

- **Mechanism:** Mutate only false-positive and false-negative regions of a responder's match function; freeze the responder's payload. Exchange boundary fragments among responders whose payloads remain unrelated.
- **Novelty bet:** Recognition surfaces become transferable learning objects independently of updates, beyond evolving whole policies or recombining detectors from scratch (NB35). Near: rule-list evolution and hard-negative mining.
- **First test:** Learn sparse wildcard recognizers for a stream of command families with different actions but shared distractors. Compare boundary-fragment exchange to evolutionary whole-rule search and equal-budget hard negatives. Recheck old commands and old near misses.

### ID11 · Cross-reactivity atlas

- **Mechanism:** For each new evidence family, measure signed benefit and collateral loss of activating a small panel of old responders. Factor the resulting response matrix into axes used to choose future interventions before observing full labels.
- **Novelty bet:** An active response panel learns the geometry of task families through interventions, not prompt similarity or a synthetic old-data checksum. Near: steering tomography; the axis learned is cross-task *reuse*, not an edit location.
- **First test:** In a family of hidden linear rule mixtures, predict which old operators help a new mixture from three output probes. Compare against loss-ranked experts and random panel axes; recheck old single-rule and mixed-rule tasks after allocation.

### ID12 · Response-class switch

- **Mechanism:** Keep the learned recognizer and its stable identity while swapping the semantics of its response, e.g. from adding a correction to requesting clarification. Transfer what made the recognizer useful but re-learn how it reaches downstream components.
- **Novelty bet:** One memory can change the *kind* of operation it authorizes without redefining what it is about. Near: modular retrieval and effect types; test the payload migration, not only the presence of an indirection table.
- **First test:** In a command agent, change a known ambiguous-input family so acting becomes worse than asking. Compare intact recognition plus a learned kind switch to retrain-both and fixed action substitution. Recheck old command families and the changed family's unaffected recognition boundary.

### ID13 · Ecological shadow clones

- **Mechanism:** Maintain a small pool of dormant models selected to cover different *errors of the incumbent*, not different tasks. Update membership when two clones become redundant under interventions; let a clone become active on a previously unseen error intersection.
- **Novelty bet:** Capacity reserves coverage of counterfactual failures, not latent task IDs or diversity measured on ordinary predictions. Near: mixture-of-experts diversity and error-correcting ensembles.
- **First test:** Use weak Boolean learners whose blind spots overlap, then introduce a held-out conjunction of blind spots. Compare selected shadow members to disagreement and random reservoirs of equal size. Recheck each incumbent old concept once a clone is activated.

### ID14 · Evidence-barcoded lineage merge

- **Mechanism:** Tag a learned micro-operation with identities of minimal independent evidence witnesses. When two descendants transfer the operation, estimate duplicated support from shared witness ancestry before deciding whether it deserves stronger commitment.
- **Novelty bet:** Merge confidence can conserve independence across forks without merging histories or counting equivalent edit strings as independent. Near: convergent-edit promotion and common-information filters; the key operation is evidence subtraction across descendants.
- **First test:** Split a symbolic learner into three branches with overlapping observations, then merge learned rewriting rules. Compare calibration and wrong promotions to branch voting and exact edit deduplication. Recheck retained pre-fork rewrite rules and unaffected edge cases.

### ID15 · Breadth mosaic

- **Mechanism:** Partition responders by their measured coverage across *independent transformations* of a skill. When evidence is scarce, activate a mosaic whose blind spots are complementary under unseen transformation combinations, not the single best responder.
- **Novelty bet:** A reusable responder carries a cross-transformation coverage profile that composes with others' profiles. Near: portfolio ensembles; the distinguishing prediction is held-out combinatorial coverage at equal committee size.
- **First test:** Train small transducers on rotated, renamed, and reordered symbol rules. Compare coverage-set selection with top-score and prediction-disagreement committees, then recheck each earlier transform after the mosaic is updated.

### ID16 · Recognition-space inoculum

- **Mechanism:** After a correction, store the smallest distinguishable *family of update requests* that would have produced that same correction. Use those equivalence classes to interpret new requests, not to reject known bad content or rehearse earlier examples.
- **Novelty bet:** Continual learning changes the dictionary that parses future update requests. Near: edit idioms and receptor repertoires; not the ledger's killed memory inoculation or detector reuse.
- **First test:** Send a toy rule editor unseen paraphrase grammars requiring the same insert, guard, or change-scope effect. Compare learned equivalence classes to intent-classification features and edit replay; recheck older requests and the untouched behaviors those requests previously edited.

## III. Active tolerance and release

### ID17 · Recognition without action

- **Mechanism:** On a conflicting observation, learn a separate recognition trace while imposing zero output change under a measured intervention. If later evidence changes the decision, train from the recognized pattern without collecting the original examples again.
- **Novelty bet:** A system can acquire a usable recognizer under a do-not-act constraint, rather than postponing the entire write or superposing tentative payloads. Near: selective prediction and latent learning.
- **First test:** Show an MLP unlabelled exceptions before later providing either confirmation or disconfirmation. Compare recognition-only learning with a feature buffer and deferred training at equal bytes; recheck old decisions both while exceptions are silent and after confirmation.

### ID18 · Transfer the tolerance boundary, not the skill

- **Mechanism:** A learner exports pairs on which it must react differently and pairs on which it must react identically. A second learner uses these to infer which distinctions it can ignore while retaining its own outputs and choosing its own parameters.
- **Novelty bet:** Invariance alone can migrate as a partially specified object, without copying labels, actions, or task weights. Near: relational distillation and contrastive learning; transfer must help even when the recipients' label semantics disagree.
- **First test:** Give two tiny classifiers different label permutations and backgrounds. Teach one how nuisance swaps work, then transfer just boundary pairs and compare to matched contrastive augmentation and output distillation. Recheck the recipient's old classes and nuisance strata.

### ID19 · Tolerance by disagreement escrow

- **Mechanism:** When two perspectives disagree, let each attach a condition for what would settle the conflict. Store the two conditions as a joint query generator, and permit a write only where the returned evidence discriminates.
- **Novelty bet:** An unresolved disagreement can retain executable *settlement semantics* independent of either prediction, rather than persisting the losing hypothesis or increasing a confidence threshold. Near: active query by committee and CEGIS.
- **First test:** In a tile-rule agent, make hypotheses disagree on many tiles but differ in a transportable way on only one pair. Compare paired settlement queries to committee disagreement and fixed counterexamples at two queries per event. Recheck standing unrelated tile rules.

### ID20 · Local tolerance wakes the neighbors

- **Mechanism:** A specialized responder that explains away a discrepancy suppresses relearning the same mapping locally, but passes a scoped invitation to adjacent modules to test for a different cause. The invitation carries the explained portion and the residual.
- **Novelty bet:** A rejected local write can become a portable teaching input, rather than ending the update or routing the original observation unchanged. Near: hierarchical residual learning and ID25; this message is emitted by a tolerance decision, not an induction signal.
- **First test:** Couple two simulators with partly shared sensor errors. Train one to recognize a recurring benign shift, then add a simultaneous true shift in the other. Compare residual invitations to hierarchical residual fitting and routing on total loss; recheck old dynamics in both simulators.

### ID21 · Action-conditioned tolerance

- **Mechanism:** Learn which discrepancy disappears under a reversible action or view change. Suppress learning only for that action-defined equivalence class; release it when the formerly neutralizing operation stops working.
- **Novelty bet:** Tolerance records a runnable neutralization operation, not a static mask on examples or a negative replay item. Near: causal invariance and probe-before-write; tolerance can be revoked by a single failed neutralization.
- **First test:** In a gridworld, compare a reversible view offset and a real reward remapping with identical one-step losses. Match probe budgets against passive drift detection and a fixed neutralizer. Recheck reward behavior under old mechanics and multiple old views.

### ID22 · Clearance receipts

- **Mechanism:** Track why a transient learning request was resolved: a receipt carries the exact observations explained, the new exception introduced, and the event that invalidates closure. Dependent writers can discharge only their matching requests without touching other pending work.
- **Novelty bet:** Termination of one update becomes a typed effect on *other learners' pending evidence*, not deletion or decay of the skill. Near: truth maintenance and event-driven job deduplication; test closure when evidence is shared but obligations differ.
- **First test:** Simulate three learners issuing overlapping repairs across recurring API versions. Compare receipt-driven closure to per-event deduplication and recency decay; measure unnecessary reheating and recheck old API calls and unrelated open repairs.

### ID23 · Soluble decoys for evidence

- **Mechanism:** Before a discrepancy reaches any updater, allow a short-lived explanation object to bind it and predict which second observation should accompany it. Bound evidence becomes eligible for ordinary learning again as soon as the prediction fails.
- **Novelty bet:** An explanation temporarily holds a *specific teaching sample* out of circulation pending a falsifiable prediction, without changing action selection. Near: Bayesian explaining-away and pending-label queues.
- **First test:** Feed a context model bursts caused by nuisance noise or real changes; make their second events diverge. Compare expiring explanation bindings to robust loss and delayed-label-only controls at equal delay. Recheck preexisting mappings between bursts and after release.

### ID24 · Two-component breach tests

- **Mechanism:** Keep the permanent action policy and the permanent learning policy separate. Let a pair of incidents breach tolerance only if swapping which incident supplies the prediction and which supplies the feedback reverses the proposed write.
- **Novelty bet:** A cross-swapped causal contrast is a compositional update trigger, not an uncertainty threshold, negative example, or majority vote. Near: paired counterfactual testing and doubly robust diagnostics; the bet is that swapping adds information beyond each incident's score.
- **First test:** In a toy command agent, pair conflicting feedback from an actual spec change or from two different users with unchanged specs. Compare the swap test to a paired residual threshold at four evaluations. Recheck old user contexts and unchanged commands.

## IV. Inducing new computation

### ID25 · Portable organizers

- **Mechanism:** Learn a short signal sequence that makes several untrained neighbors form complementary roles. Transfer the organizer alone to an empty neighborhood and let a different local substrate realize the roles without receiving the original modules or their weights.
- **Novelty bet:** Transfer an elicitor of construction rather than a patch or a seed that reconstructs a prior self. Near: neural cellular automata, hypernetworks and SM15 ontogeny distillation; the claimed object is a substrate-independent input that induces complementary structure.
- **First test:** Learn signals that produce a parser and a counter in a three-node logic graph. Move the organizer to an unseen permutation of gate types; compare to a same-byte module recipe and trained hypernetwork. Recheck the original parser and counter after another role is induced nearby.

### ID26 · Competence as a learnable type

- **Mechanism:** A module learns which open-ended construction signals it can translate into useful local behavior. A construction signal may be delivered to a new module before either side has been trained on the requested behavior.
- **Novelty bet:** A learner writes a *type of request it can learn from*, independent of its current output capabilities. Near: typed interfaces, meta-learning and affordance discovery; the test is new signal–module pairings.
- **First test:** Train small transducers to respond to a subset of construction signals such as compose, repeat, and invert. Hold out signal–substrate pairs; compare competence lookup to a learned task router and fixed type tags, and recheck old transductions after new bindings.

### ID27 · Reciprocal interface induction

- **Mechanism:** Two neighboring modules adapt alternately by offering candidate latent interfaces, each written to reduce the other's learning cost while preserving its own previously tested input/output behavior. Settle on an interface only if both can exploit it.
- **Novelty bet:** An interface can be an equilibrium of local learning operations, not an ABI fixed up front (P19) or an alignment after training. Near: emergent communication and iterative co-training.
- **First test:** Add a shared subroutine to two small agents with different observation encodings. Compare interactive interface negotiation to centralized representation alignment and one-way distillation at matched data. Recheck the agents' old tasks without the shared subroutine.

### ID28 · Seam memory

- **Mechanism:** When two modules' decisions nearly agree but composition fails in a narrow region, fit a boundary module to the discrepancy on their intersection; store which values the seam reads on each side and allow it to migrate as either module changes.
- **Novelty bet:** Learn a function *on the seam between two capabilities*, together with a mechanism for transporting its support, rather than fine-tuning both or appending an ordinary expert. Near: domain decomposition and learned adapters.
- **First test:** Pair independently trained parsers with one shared delimiter whose meaning drifts. Compare a transported seam module to static adapters and end-to-end replay; recheck old parser-private inputs plus old well-formed compositions away from the seam.

### ID29 · Order-of-induction operator

- **Mechanism:** Find a shortest sequence of two existing teaching operators that yields a new behavior only in that order. Install the order as a one-use construction instruction that can recruit freshly instantiated modules.
- **Novelty bet:** Learn to use, rather than eliminate, noncommutation of *building operations*. Near: O2 commutative learning, curriculum learning and program synthesis; a held-out composition must depend on order even when both arms receive the same examples.
- **First test:** Build a tiny graph in which normalization can precede or follow specialization. Search two-step orders on two tasks; transfer order to a third and compare random or loss-greedy orders. Recheck the original normalization and specialization tasks.

### ID30 · Insertion by intercalation

- **Mechanism:** Present already competent endpoint modules with a novel unhandled intermediate case. Insert the shortest bridge consistent with endpoints' transition rules; teach the bridge from inside out without assigning new parameters to endpoint roles.
- **Novelty bet:** New functionality can interpolate between executable state transitions, unlike replay interpolation in input space or reconstructing a removed region (NB21). Near: option discovery and program synthesis from boundary conditions.
- **First test:** Insert a half-step protocol state between two trained handshake states and compare local bridge synthesis to a new option and ordinary fine-tuning. Recheck old direct handshakes as well as each endpoint's other transitions.

### ID31 · A learned default fate

- **Mechanism:** Give uncommitted modules a default function that expresses only when a local suppression signal is absent. Update the default from recurring gaps; older sites that already provide suppression are examined for leaks, not refit by default.
- **Novelty bet:** A learning system can change what *unassigned capacity does by default* while keeping the previous exceptions to default expression. Near: default rules and MoE background experts; the absence condition is attached to a location, not matched against the full input.
- **First test:** In a bounded graph of symbol transforms, learn a new background operation after adding holes in distinct contexts. Compare to an equal-size default expert and residual cascade. Recheck old occupied contexts and obsolete default behavior where it still has an explicit guard.

### ID32 · Bidirectional relay induction

- **Mechanism:** If two old modules can't exchange a new distinction directly, change a dormant intermediate module into a relay by asking each endpoint to train an opposite side of it. Keep only relays that carry a verifiable distinction in both directions.
- **Novelty bet:** Learning can recruit an intermediary through two-sided local teaching instead of authoring a link centrally or activating a prespecified bridge (NB07). Near: bidirectional representation alignment and adapter composition.
- **First test:** Give two tiny agents disjoint command vocabularies and a new handoff requiring agreement. Match bytes and examples versus one-way translators and centralized alignment. Recheck standalone command sets and older handoffs after a relay is installed.

## V. Lineage and changes of fate

### ID33 · Inheritance of tests, not weights

- **Mechanism:** When a module spawns a specialist, pass down the smallest set of operations that reveal when the parent's rule stops applying. The new module uses these to select useful data; it need not copy the parent's model or training data.
- **Novelty bet:** The hereditary unit is a failure-disclosing experiment that can be run against new descendants. Near: contract-directed replay and teacher experiment design; these tests choose acquisition data rather than replay parent outputs.
- **First test:** Give a tiny arithmetic learner's descendants tasks where carry behavior differs in subtle cases. Compare inherited experiment generators to fixed edge cases and ordinary active learning with the same query count. Recheck the parent's old arithmetic and previously promoted descendants.

### ID34 · Asymmetric division of learning roles

- **Mechanism:** Split a learner into a stable producer and an editable understudy. Give the understudy the producer's responsibility for resolving one kind of ambiguity, but not the producer's learned answer; it must derive its own answer through the producer's observable behavior.
- **Novelty bet:** Division distributes *who gets to answer which learning question*, not weights, an optimizer, or model-copy duties. Near: stable/plastic dual networks; only specific query rights move with the split.
- **First test:** Split a tiny intent learner's clarification role from execution, then switch clarification costs. Compare reallocated queries to full cloning and a fixed tool split at equal calls; recheck old execution and unaffected clarifications with both learners active.

### ID35 · The same phenotype, two heritable ways to build it

- **Mechanism:** Retain two different construction rules that realize one public behavior. When a constraint changes, keep patches to the construction rules that survive both the original and new constraint, rather than choosing which implementation has higher current fitness.
- **Novelty bet:** A skill can inherit a small set of interchangeable *implementability proofs*, not merely an ensemble of predictors or neutral parameter copies. Near: program equivalence, degeneracy and SM7 neutral drift.
- **First test:** Keep table-driven and algebraic implementations of an integer transform, then remove one operation and add a new input range. Compare adaptation against an ensemble and a single implementation plus repair search. Recheck old inputs after each constraint change.

### ID36 · Transdifferentiation map

- **Mechanism:** Convert an existing module to a different computational role by preserving an agreed latent distinction that the new role can exploit, then train only the changed read/write interfaces. Store a conversion contract applicable to other modules.
- **Novelty bet:** Role conversion is a transferable operation on the same module, not merely routing it differently, reallocating parameters, or transplanting old functionality (P27). Near: transfer learning and representation surgery.
- **First test:** Convert a tiny next-symbol predictor into a mismatch detector while preserving its internal delimiter distinction. Apply the learned map to a second predictor and compare against head replacement and full distillation. Recheck old modes that still use the original delimiter representation.

### ID37 · Fusion with dual jurisdiction

- **Mechanism:** Fuse two modules into a single learned state machine, but preserve both original update interfaces. When simultaneous writes disagree, require the fused machine to produce a small separating state that can host both old transitions.
- **Novelty bet:** Fusion creates one shared state with two independently meaningful update algebras, rather than averaging weights or composing outputs. Near: product automata and multitask learning; the question is whether a compact separating state suffices.
- **First test:** Merge two learned finite-state protocol trackers with one shared state and two conflicting transitions. Compare to product construction and multitask minimization by bytes and convergence; recheck both original transition languages after adding a joint event.

### ID38 · Fate mosaics that generalize from disagreement

- **Mechanism:** Apply a small update to a distributed subset of otherwise equivalent cells or modules. Treat downstream responses as a mosaic experiment that reveals whether the new behavior is module-autonomous or needs neighboring changes before extending it.
- **Novelty bet:** A mosaic is a probe for *context dependence of a write*, not a random search over edit locations. Near: patch canaries and sparse causal ablations; estimate an interaction with neighbor context rather than an edit's mean effect.
- **First test:** In a four-node message-passing toy, plant both local and neighbor-dependent new tasks. Infer required write neighborhoods from singleton and paired mosaics; compare to random canaries and update norms, then recheck every old node-local task.

### ID39 · Fate maps for destructive edits

- **Mechanism:** Keep a writable map of which downstream capabilities adopted each of a module's *roles*, not which weights or snapshots they came from. Before deleting a role, use the map to predict substitute paths and test them; update the map after each substitution.
- **Novelty bet:** A learned lineage map is indexed by acquired responsibilities, and can predict effects of a deletion no past run has seen. Near: provenance, causal tracing and NB08. The bet is useful prediction of substitutes, not a local pruning gate.
- **First test:** Grow a shared DAG of toy string functions, then remove an intermediate operation replicated by two different paths. Compare routing based on role descent to dependency-graph reachability and intervention-only search; recheck all old compositions that used the removed role.

### ID40 · Heterochronic handoff

- **Mechanism:** Replace a global training phase with per-module readiness signals. Learners jointly determine when each neighbor has a usable (not necessarily finished) skill and which parts of its output can already teach downstream.
- **Novelty bet:** A construction clock carries *what can teach what now*, rather than merely choosing a learning rate, ordering examples, or handing off the full module. Near: asynchronous curriculum and progressive networks.
- **First test:** Train a parser, counter, and router with independent shifts and delayed feedback. Compare readiness-conditioned partial supervision to fixed curricula and loss-triggered handoffs at equal updates. Recheck earlier roles and joint tasks after the slowest role matures.

## VI. Shape and mechanics of a growing learner

### ID41 · Convergent extension for computation graphs

- **Mechanism:** When several parallel modules redundantly handle part of an old computation, swap local neighbors pairwise to turn some of that width into sequential depth. Require each intermediate graph to preserve the exposed old interfaces.
- **Novelty bet:** Trade width for depth by local, behavior-preserving rearrangements over a stream, rather than growing an entire new topology or making a one-shot network morphism. Near: Net2Net and dynamic architecture search.
- **First test:** Teach parallel Boolean transforms, then introduce ones that require longer compositions. Compare local rearrangement to equal-parameter widening and Net2Net-style deepening. Recheck held-out compositions of the original transforms after every swap wave.

### ID42 · Interference tension edges

- **Mechanism:** Give each module boundary a tension estimated from how changing it redistributes error to neighbors. Let accumulated incompatible tensions relax by moving interfaces and sharing load, not by moving the modules' weights along the ordinary loss gradient.
- **Novelty bet:** Maintain a separate mechanical state over learned interfaces that can trigger *structural* relaxation before the next data wave. Near: interference gradients and NB06; use tension to change a boundary, not route update magnitude.
- **First test:** In a shallow linear network with coupled subproblems, track edits whose errors move across different cuts. Compare tension-driven cut moves with gradient-conflict routing and periodic random refactoring. Recheck old tasks whose interfaces are adjacent to and distant from the cut.

### ID43 · Buckle under conflicting roles

- **Mechanism:** Start with one smooth shared computation. Estimate the smallest symmetry-breaking deformation that would let two roles specialize in opposite directions without losing a shared mode; test the deformation and then grow a persistent branch only if it helps.
- **Novelty bet:** Add a new degree of freedom along a measured instability of the *shared mechanism*, not arbitrary duplication or thresholded loss growth. Near: neuron splitting and mode bifurcation.
- **First test:** Stream symmetric and then asymmetric regression targets through a tiny shared basis model. Compare estimated antisymmetric branch directions to random split directions and width growth, measuring adaptation per added parameter. Recheck both old symmetric inputs and prior asymmetric ones.

### ID44 · Compartment boundaries with direction

- **Mechanism:** Learn two distinct permeability masks across each module boundary: one for reading behavior and one for sending gradients or write messages. Allow new functionality to import old outputs without granting the reverse write channel.
- **Novelty bet:** A boundary stores direction-dependent read/write compatibility, not one task mask or a firewall on a whole module. Near: stop-gradient interfaces and NB04; learn which crossings should be asymmetric as the stream changes.
- **First test:** Pair two differentiable modules sharing a useful latent feature and a conflicting nuisance. Compare learned directional boundaries to fixed stop-gradient, symmetric masks, and OGD. Recheck both old functions on downstream and upstream inputs.

### ID45 · Adhesion by complementary obligations

- **Mechanism:** Let a component expose a learned description of what it needs from a neighbor and what it can supply. Connect only compatible descriptions and issue a short local test where both sides can try to falsify the match before adopting it.
- **Novelty bet:** Build reusable compatibility surfaces for decentralized architecture growth, not a central linker resolving fixed symbols (P17) or a MoE gate direct to an expert. Near: interface contracts and modular program synthesis.
- **First test:** Pool a dozen tiny programs with ambiguous names and hidden input assumptions. Fit obligation vectors from earlier successful pairings; test unseen pairings against embedding match and static types at the same probe budget. Recheck existing compositions after rewiring.

### ID46 · Prestressed learning scaffolds

- **Mechanism:** Install two opposing latent constraints with zero net effect on the currently tested computations. If a new role strains one constraint more than the other, the imbalance favors one of several viable shapes for incorporating that role.
- **Novelty bet:** Persist a preference for *how future structure deforms* without adding a current output or a named future task. Near: null-space adaptation and plasticity reserve; the claim concerns selecting a concrete structural transition, not predicting generic next-task gain.
- **First test:** Use two equal-performing sparse graph layouts with different reusable links; teach matched next tasks under symmetric or biased constraint pairs. Compare adaptation and edge changes to fixed topology preferences and equal-norm regularization. Recheck earlier graph functions throughout.

### ID47 · Fold to link

- **Mechanism:** Place modules on a learnable sheet with an adjacency budget. Local folds create transient contacts between distant modules, letting them test a joint operation; successful contacts can persist after unrelated parts unfold.
- **Novelty bet:** Search for compositions by rewriting the geometry that determines *which pairs can communicate*, rather than searching individual arbitrary edges. Near: neural graph rewiring and learned topologies; the claimed advantage is coherent reuse across nearby compositions.
- **First test:** Lay out a dozen small string operations and induce batches of pair compositions. Compare budgeted fold proposals to pairwise edge search and embedding nearest neighbors. Recheck old compositions whose long-range contacts share the same sheet.

### ID48 · Developmental handedness

- **Mechanism:** Preserve an orientation bit in the rules that construct local modules, and propagate orientation through verifiable transitions when topology changes. Interpret later writes relative to that orientation, not an arbitrary model or tool indexing convention.
- **Novelty bet:** Learned updates can have a portable handedness carried by local construction rules, distinct from rebasing weights or conditioning on a task tag. Near: equivariant networks and NB13 coordinate loops.
- **First test:** Train a local graph agent on clockwise controls, then change node numbering and introduce a reflected tool family. Compare orientation propagation to equivariant data augmentation and fixed canonical sorting. Recheck old clockwise and counterclockwise controls after each graph rewrite.

## VII. Repair and life-cycle transitions

### ID49 · Repair by uncommitting a fate

- **Mechanism:** Separate a module's hard role assignments from a small set of generic transformations. When no ordinary write fits new evidence, temporarily revoke the role assignments but keep the transformations and let them reassemble into different roles under old behavioral constraints.
- **Novelty bet:** Uncommit what a component *is allowed to become*, without wiping parameters, restoring a checkpoint, or regrowing the same missing tissue (NB21). Near: selective resets and network rewiring.
- **First test:** In a six-node transducer, remove a sensor modality and add a replacement with different output semantics. Compare role release to equal-budget resets and fine-tuning. Recheck earlier transductions on inputs that do not use the removed sensor.

### ID50 · Injury transfer, not lesson transfer

- **Mechanism:** Extract a minimal intervention that reproduces a failure in one module. Translate that intervention to another module's interface and use the recipient's own response to learn a repair before it experiences the original failure.
- **Novelty bet:** Transfer a *generator of local failure* rather than a solution, a warning, or a hard example. Near: fault injection and domain randomization; the generator is learned online and transports causal structure across different implementations.
- **First test:** Discover a brittle truncation in a table parser and transfer the intervention to a grammar parser with differently named tokens. Compare with example replay and random grammar perturbations at equal calls. Recheck legacy parsing languages and unaffected failures.

### ID51 · Regulate the shape, not the cells

- **Mechanism:** Specify an acquired behavior as a set of global relations over module outputs. After local interference, adjust modules using only residuals of those relations so a different distribution of local roles can recover the same global skill.
- **Novelty bet:** An acquired phenotype can be stored as relational constraints for compensation, without target activations, fixed task replay, or a sparse-damage syndrome. Near: distributed control and neural cellular automata.
- **First test:** Teach five agents to maintain an ordered allocation, then change one agent's feasible range. Compare constraint-residual repair to output imitation and same-byte relation replay; recheck old allocation commands on new start states and old cardinalities.

### ID52 · Metamorphosis with obligations in flight

- **Mechanism:** Make two agent architectures exchange only a minimal representation of pending promises and their resolution conditions. Complete a promise begun in the old architecture in the new one, even if the new architecture cannot replay the old path.
- **Novelty bet:** A learning system hands off *unfinished causal commitments*, not just state, memory, or recoverable checkpoints. Near: continuation-passing and state migration; the bet is that usable continuations can be learned from consequences rather than specified per architecture.
- **First test:** Change a planner from a stack to a DAG midstream with delayed requests and obsolete internal actions. Compare learned obligation transfer to serialized intermediate state and issue-list replay at equal bytes. Recheck old workflows and actual completion of pre-switch promises.

### ID53 · Scaffold for detachability

- **Mechanism:** During acquisition let temporary helper modules provide information, but train them to expose which parts of their help can be recomputed locally by the learner. Strip helpers that reveal a sufficient reconstruction, not merely helpers whose outputs are small.
- **Novelty bet:** A teaching scaffold plans its own deletion through reusable reconstruction hints. Near: privileged learning, distillation and curriculum fading; no improvement is attributed simply to who wrote the examples.
- **First test:** Teach a tiny pushdown recognizer with temporary parse hints. Compare reconstruction-aware hints with ordinary hint dropout and teacher distillation at equal supervision. Remove hints and recheck earlier languages as well as the new one.

### ID54 · Compensatory organ transfer

- **Mechanism:** Rather than repair a lost module in place, give a different existing module the ability to offer an alternate intermediate computation. Learn a way for consumers to transform their requests so the alternate yields the same task-level result.
- **Novelty bet:** Recover through a learned *substitution of roles*, without reconstructing the erased function or installing a backup copy. Near: degeneracy, fault tolerance and ID36; consumers change their request language while the replacement stays competent at its original role.
- **First test:** Remove a prefix counter from a transducer and let consumers derive the count from boundary events exposed by an existing tokenizer. Compare request rewriting to masked-module fine-tuning and backup storage. Recheck old prefix tasks and original tokenizer behavior.

### ID55 · Learn a scar's aftercare

- **Mechanism:** When an interface is repaired, store which later operations would reopen its failure, and a local rewrite that makes those operations compatible when they arrive. Use the repair to generate actionable data about future structural changes.
- **Novelty bet:** A repair creates a prospective *edit-to-edit translator*, not a frozen scar, prohibition, or old-weight penalty. Near: NB04 and P19; future proposals need not share the original interface representation.
- **First test:** Repair a pipeline whose two stages now disagree on units, then submit unseen edits that change interface scaling. Compare learned translators against fixed contracts plus rejection. Recheck old units and consumers after each accepted later edit.

### ID56 · Transitional function as a first-class skill

- **Mechanism:** Learn an intermediate procedure used only while two subsystems are at different stages of a change. Index the skill by the mismatch it resolves, and reuse it when a different pair of subsystems hits the same mismatch.
- **Novelty bet:** The lesson is a *bridge between nonstationary states*, not the old endpoint behavior, new endpoint behavior, or an API alias. Near: compatibility shims and ID30; here the bridge is intentionally temporary and should generalize across asynchronous transitions.
- **First test:** Update three symbolic tools at staggered times from push to pull semantics. Compare learned transitional procedures with static compatibility tables and ordinary re-planning; recheck both mixed-version and all-old workflows on held-out cases after later updates.

## VIII. Immune–developmental hybrids

### ID57 · Teach by developmental challenge

- **Mechanism:** When an agent observes a discrepancy, select a tiny daughter learner and expose it to simplified versions of the environment. If the daughter can grow the missing skill from a particular seed behavior, send only that behavior and its construction conditions back to the parent.
- **Novelty bet:** A discrepancy is diagnosed by *buildability in a controlled learner*, not by the parent's predicted gradient, sandboxed own update, or the daughter's final weights. Near: D3 hypothetical fine-tuning and artificial life.
- **First test:** Compare tiny learners grown from different partial lookup rules under paired easy/hard worlds, then transfer their construction conditions to a different parent. Compare to parent-only counterfactual editing and loss-greedy curricula. Recheck the parent's old mappings before and after transfer.

### ID58 · Immune privilege by role, not module

- **Mechanism:** Mark one output role as temporarily exempt from general write review while adjacent roles remain subject to it. Learn how to limit the exemption by measuring effects on downstream dependents; revoke it on observed leakage instead of on a fixed clock.
- **Novelty bet:** A protected developmental niche can be specified as a writable exclusion boundary over effects, not as a frozen module or generic staged deployment. Near: policy sandboxing and role-scoped write masks.
- **First test:** Teach a new formatter in a shared parser without blocking controlled changes to its temporary outputs. Compare effect-scoped privilege to whole-module isolation and a global write gate. Recheck old formats, including shared-prefix cases most likely to leak.

### ID59 · Re-open competence from a narrow alarm

- **Mechanism:** A module's old construction path can be reused for a new role only if a learned alarm reconstructs which competence was missing. Match alarm features to small operations that change what the module can *learn from*, before teaching the new function.
- **Novelty bet:** A detected mismatch becomes a portable constructor of learning affordances, not a reset, larger step size, or selection among fixed objectives. Near: ID26 and meta-learned curricula; the alarm should carry across contexts with different observable errors.
- **First test:** Make a previously one-token transducer learn a two-token rule after the stream switches. Compare alarm-selected construction of a lookback channel with fixed lookback and ordinary hyperparameter tuning at equal compute. Recheck the original one-token transformations.

### ID60 · Boundary cells certify growth

- **Mechanism:** Before committing a structural insertion, let boundary modules return local satisfiability conditions for the old functions they touch. Compose the conditions through changed edges to predict where additional probes are needed; no compensation is allowed to hide an unsatisfied condition.
- **Novelty bet:** Growth carries a distributed and composable body of proof obligations, not a single retention penalty or post-hoc global alarm. Near: P8 certified updates, P9 effect types and ID03; here the insertion can create new proof obligations for subsequent learning.
- **First test:** Insert local operations into a small typed functional DAG with paired insertion successes and cross-boundary failures. Compare adaptive local obligations to comprehensive old replay and static types at equal calls. Recheck each old composite behavior, especially those spanning multiple insertions.

### ID61 · Pass the ability to forbid along a lineage

- **Mechanism:** During role succession, the predecessor grants the successor power to reject a particular class of harmful writes to dependencies. Transfer the power only after the successor can identify novel counterexamples not seen by the predecessor; leave accepted writes unconstrained by this test.
- **Novelty bet:** Descendants inherit an experimentally qualified *veto operation*, rather than inheriting a frozen constraint, memory artifact, or complete verifier. Near: ID33 and proof-carrying updates; the inherited operation acts on third-party writes.
- **First test:** Replace a calendar toy's conflict-checking module and expose it to unseen interval encodings. Compare qualified veto transfer with copied rejection rules and an independent shared verifier at equal probes. Recheck old scheduling requests and safe calendar revisions.

### ID62 · Transfer the map of tolerable mutations

- **Mechanism:** Learn a graph whose edges are known behavior-preserving transitions between local implementations. Give a new learner the graph's move predicates, but not its states, so it can discover analogous moves that preserve *its own* old skills.
- **Novelty bet:** Port a grammar of empirically neutral structural operations, not a parameter alignment, fixed editing ISA, or null-space basis tied to one model. Near: SM7, P21 and ID41; test cross-substrate transfer of neutrality.
- **First test:** Find safe rewrites of arithmetic expression DAGs, then move the predicates to tiny finite-state transducers with different nodes and actions. Compare to generic neutral search and a ported fixed rewrite library. Recheck each recipient's fixed old-task panel after a sequence of rewrites.

### ID63 · Recover a suppressed distinction through tissue reorganization

- **Mechanism:** If two old consumers treat different inputs identically for different reasons, split the local representation along the difference in their invariance constraints. The split should let a new consumer learn the distinction without asking either old consumer to give up its invariance.
- **Novelty bet:** Expose a latent teaching axis by comparing two *reasons for ignoring it*, not by reserving a feature slot or detecting dense corruption. Near: disentanglement and gradient surgery; the separate constraint witnesses choose the new axis.
- **First test:** Train two output heads that ignore the same raw cue under distinct nuisance transforms. Learn a third head requiring that cue only in a new composition. Compare constraint-difference splitting to supervised feature expansion and projected gradients; recheck both old heads on independently held-out nuisance pairs.

### ID64 · Maintain a development grammar by rejecting bad organs

- **Mechanism:** Keep a grammar of local construction operations rather than an archive of successful architectures. When a new module works in isolation but disrupts old behavior after integration, identify a smallest failing *combination of grammar rules* and revise the grammar to propose different constructions next time.
- **Novelty bet:** Rejection is attributed to a transferable construction motif, not to a particular transplant, checkpoint, or failed weight vector. Near: P27, grammar-guided architecture search and CEGIS; the bet is zero-shot avoidance of the motif on a different host graph.
- **First test:** Grow toy mechanism graphs through six waves; introduce two rewrites each safe alone but harmful in combination on held-out hosts. Compare cross-host integration success to base grammar search and failure blacklists of equal size. Recheck the entire old behavior panel after each growth wave.
