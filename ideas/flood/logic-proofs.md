# Flood: continual learning from formal logic, proofs and verification

Raw, unfiltered ideas (64). Angle: what would continual learning look like if a learner's knowledge were a growing theory, each update a theory change, and retention something you can check (or prove) instead of measure on a held-out set? Nothing is pre-killed. Every entry is *ambitious but doable* unless marked **Moonshot**. Near neighbors are named where I know them; the reviewer judges overlap.

Screened against `reviews/idea-ledger.md` and `reviews/flood-triage.md` (PR #6). Where an idea touches a killed or ranked one it says so: sparse-write certificates (killed), composition contracts (killed), certified retention 2610.40740, P8/P25 certified contracts and abstract interpretation (rated 3), P9 effect types, P7 typed residual, P17 linker, N1 round-trip consolidation, L1 checkpoints, SM1 seed log, D3 hypothetical fine-tuning, physics #31 sheaf cohomology, #21 kinetic proofreading, memory-loop Lyapunov (killed), self-QA replay (killed), lesson capacity law (held).

Format: **mechanism**, *why it might be new / neighbors*, **cheapest first test** with a **retention check** (old tasks still work). Lesson/memory tests carry the ledger's same-length-filler and temperature-matched arms by default.

## A. Proof theory as consolidation

**LP1. Cut-elimination consolidation.** A skill first lives as a chain-of-lemma trace (each intermediate lemma is a "cut"). Consolidation trains the model to emit the conclusion directly (the cut-free proof) while a re-expansion loss keeps every eliminated lemma recoverable on request. Retention criterion: cut *admissibility* — the shortcut never replaces the ability to justify. *New:* implicit-CoT internalisation (Deng et al. 2023/2024) drops the steps; here the dropped lemmas are kept as an on-demand inverse, so later tasks that reuse a lemma can still cite it. **Test:** GPT-2 small, 4-digit multiplication then 3-step word problems that reuse partial products; stage-wise CoT removal with vs. without the re-expansion loss. Measure direct accuracy, lemma re-expansion accuracy, and transfer to task 2. **Retention:** task-1 direct accuracy after task 2 vs. plain implicit-CoT and vs. replay at equal tokens.

**LP2. Craig-interpolant task interfaces.** For tasks A and B with a partly shared input signature, learn an interpolant layer I that may only read features of the shared symbols; task-specific heads may not read each other's private features. All interference has to pass through I, which is small and can be regularised hard. *New:* Craig interpolation as the architecture rule for what may be shared between tasks; neighbors are shared/private CL splits (e.g. adversarial continual learning 2003.09553), which pick the split by learning, not by signature. **Test:** synthetic rule tasks over 20 variables with 5 shared; interpolant net vs. shared-private net vs. joint MLP at equal parameters. **Retention:** A's accuracy after training B.

**LP3. Proof-net merging of skills.** Represent two fine-tunes as proof nets (graphs of the rules each trace uses, from aligned reasoning traces); merge = graph union, and conflicts show up as two rules with the same premises and different conclusions. Only conflicting rule-nodes are resolved; the rest merge without loss. *New:* merge defined on proof structure rather than weights (TIES, DARE) or behaviour (L3 diff merge). **Moonshot-ish**; cheapest version uses synthetic rule systems. **Test:** two rule systems sharing 70% of rules; train separate models, merge via proof-net union (distil the union rule set) vs. TIES vs. data mixing. **Retention:** each source system's accuracy after merge.

**LP4. Harmony loss (introduction/elimination round trip).** For every concept the model learns to *produce* (introduction), also train a matching *use* (elimination); Dummett's harmony says elim∘intro is the identity. Consolidation regulariser: a concept's representation must survive intro→elim round trip; drift that breaks the round trip is penalised even without old labels. *Neighbors:* cycle consistency, S4 round-trip fixed points; new is the proof-theoretic pairing per concept as a label-free retention signal. **Test:** 20 synthetic concepts (define-then-apply tasks), sequential training with/without harmony loss vs. EWC. **Retention:** old concept application accuracy.

**LP5. Normalisation as sleep.** During a sleep phase, the model rewrites its own reasoning traces into normal form (β-reduce detours, remove repeated subproofs), then trains on the normal forms. Proof normalisation is confluent, so traces from different tasks that prove the same thing converge to one target, shrinking interference. *New:* confluence of rewriting as the reason consolidation does not conflict. **Test:** synthetic lambda-calculus or arithmetic-expression evaluation with redundant traces; sleep-on-normal-forms vs. sleep-on-raw-traces at equal tokens. **Retention:** old-task accuracy after 5 tasks.

**LP6. Definitional extensions as compression.** When a pattern recurs, introduce a new token defined by a definition (its embedding trained so that the token and its unfolding give identical continuations). Later learning uses the short symbol; eliminability (you can always unfold) is checked as a retention test. *Neighbors:* gist tokens, AutoCompressor, learned macros (P23 macro compilation); new is the unfold-equivalence check as the contract that keeps old meanings fixed while new ones are built on them. **Test:** GPT-2, 3 stages of tasks each defined in terms of the previous stage's concepts. **Retention:** unfold-equivalence KL and stage-1 accuracy after stage 3, vs. no definitions and vs. soft prompts.

**LP7. Conservative-extension learning.** A new theory is a conservative extension if it proves nothing new in the old language. Train new skills only through new vocabulary (fresh tokens / fresh adapter keys) and enforce conservativity: KL on old-language inputs = 0, checked on a mined probe set. Everything new is stated in new symbols. *New:* conservativity as a hard spec of CL, with new tokens as the *only* channel for new knowledge; neighbors are prompt tuning per task and vocabulary expansion. **Test:** GPT-2, 5 tasks, each introducing new tokens; KL on old-language text vs. LoRA and vs. LwF. **Retention:** old-task accuracy and old-language perplexity.

**LP8. Proof-irrelevance consolidation.** Many different derivations of the same fact (multiple CoT paths) collapse into one memory of the fact (propositional truncation), freeing the capacity spent on path diversity, while one canonical path is kept for justification. *New:* treats path-memorisation as the forgettable part of learning. **Test:** train on 5 paths per fact vs. 1 canonical vs. truncated (fact + 1 path); measure capacity used (LoRA rank needed) and later-task learning. **Retention:** fact accuracy after next tasks.

## B. Belief revision and theory change

**LP9. AGM postulates as training losses.** Turn success, inclusion, vacuity, consistency, extensionality and recovery into measurable losses over probe propositions, and train an editor/learner to satisfy them across a stream. Recovery (contract then re-add gives back the original) yields an undo for free. *Neighbors:* papers evaluating LLM editing against AGM (e.g. Hase et al. 2023 belief-revision analyses); new is training on all postulates as the CL objective. **Test:** GPT-2 + CounterFact-style stream of 200 edits and retractions; AGM-loss editor vs. MEMIT. **Retention:** unrelated-fact accuracy and recovery accuracy after retractions.

**LP10. Learned epistemic entrenchment.** Each stored belief gets an entrenchment score (Gärdenfors) derived from how many other beliefs depend on it; contradicting data removes the least-entrenched beliefs first. Implemented as per-fact learning-rate scaling from a derivation graph. *New:* entrenchment computed from logical dependency, not Fisher information. **Test:** synthetic knowledge base with rules; contradicting updates; entrenchment-scaled edits vs. EWC vs. uniform. **Retention:** fraction of non-contradicted beliefs preserved and ripple consistency (RippleEdits-style).

**LP11. Belnap four-valued memory.** Each query answer is T, F, Both or Neither. Contradicting updates don't overwrite: they move a fact to Both, which flags the conflict for later resolution; Neither marks never-learned. Paraconsistent, so one conflict doesn't contaminate the rest. *New:* separating "conflicting" from "unknown" as a learned output state in CL; neighbors are abstention and calibration, which merge the two. **Test:** fact stream with 20% changed facts; 4-valued head vs. standard overwrite vs. calibrated abstain. **Retention:** old-version recall and conflict detection rate.

**LP12. Truth-maintenance system for weights.** Each fact edit stores its justification (which edits/data it was derived from). Retracting a premise automatically retracts its dependent edits (dependency-directed backtracking at the rank-1-edit level). *Neighbors:* JTMS (Doyle 1979), RippleEdits, MQuAKE; new is justifications as a weight-level edit DAG. **Test:** GPT-2-XL, 100 premises + 200 derived-fact edits, retract 20 premises; TMS retraction vs. retrain-from-scratch vs. MEMIT reverse edits. **Retention:** surviving facts' accuracy.

**LP13. Unsat-core minimal forgetting.** When new data contradicts the model, extract the model's beliefs on related propositions, find the minimal unsatisfiable core with the new fact, and unlearn only the core. *Neighbors:* BeliefBank (Kassner 2021), ConCoRD (Mitchell 2022) do consistency at inference; new is unsat-core-scoped forgetting per update. **Test:** synthetic entailment KB, contradicting stream; core-unlearning vs. full-edit vs. fine-tune. **Retention:** non-core belief accuracy.

**LP14. MaxSAT sleep.** Periodic sleep: query the model on a probe set of propositions with known logical relations, solve weighted MaxSAT (weights = model confidence) for the most consistent assignment, fine-tune toward it. Consolidation driven by consistency, not replay. *Neighbor:* ConCoRD; new as a CL consolidation phase. **Test:** 5-task fact stream on GPT-2 with implication links; MaxSAT sleep vs. replay at equal tokens. **Retention:** old-fact accuracy plus consistency rate.

**LP15. Weakest-precondition lesson narrowing.** When an agent lesson fails, compute (or have the model propose) the weakest precondition under which the lesson would have held and *narrow* the lesson's guard instead of deleting it. Lessons specialise rather than die, so old successes keep working. *Neighbors:* ILP specialisation, ExpeL insight edits. **Test:** G1 router (PR #14), rotated-rule regime switch; narrowing vs. delete vs. rewrite. **Retention:** old-regime success after narrowing.

**LP16. Hoare-triple lessons.** Store agent lessons as {P} action {Q}; plans compose by the sequence rule and are checked before execution; a failed postcondition revises P or Q only. *Neighbors:* STRIPS/PDDL operator learning by LLMs, Voyager skills. **Test:** ALFWorld subset or text gridworld; Hoare lessons vs. text lessons. **Retention:** earlier task families after new families.

## C. Verification of updates

**LP17. Proof-carrying updates with certificate debt.** Every update ships with a cheap-to-check certificate (IBP/CROWN bound on an old task's margin over input regions). Certificates are stored, and every later update must keep all stored certificates valid (projected if not). The certificate store is the memory. *Neighbors:* certified retention 2610.40740, P8; new piece is accumulating certificates as persistent objects that later updates must respect. **Test:** small MLP, 5 tasks with region certificates; projection to keep certificates vs. EWC vs. OGD. **Retention:** certified fraction and empirical accuracy on old tasks.

**LP18. Counterexample-guided continual learning (CEGCL).** After each update, a verifier (MILP/SMT on small nets, fuzzing on large) searches for inputs violating old specs; counterexamples become the replay set. No stored data. *Neighbors:* CEGIS, A-CEGIS 2609.02892, adversarial replay; new is verifier-generated replay as a data-free CL method. **Test:** small ReLU nets on 4 synthetic spec'd tasks; CEGCL vs. stored replay at equal examples vs. generative replay. **Retention:** spec satisfaction and old accuracy.

**LP19. Abstract-region replay.** Store zonotopes of old inputs with output bounds instead of examples; replay propagates regions through the current net and penalises bound violations. *Neighbor:* P25 abstract interpretation; new is regions as the replay currency with a bytes-vs-retention curve. **Test:** split-MNIST with 50 zonotopes per task vs. 50 examples. **Retention:** old-task accuracy per stored byte.

**LP20. Mined invariants as retention spec (Daikon for networks).** Mine likely invariants over old-task activations and outputs (monotonicity, x_i ≥ x_j, parity, sign patterns) and enforce them during new learning; a violated invariant is a label-free forgetting alarm. *Neighbors:* property inference for DNNs (Gopinath 2019), neural activation patterns; new is invariants as both the regulariser and the monitor. **Test:** 5-task MLP stream; invariant regulariser vs. replay at equal bytes; alarm AUC for forgetting. **Retention:** old accuracy.

**LP21. Refinement-type outputs.** Each old task is summarised by a refinement type {y | φ(x, y)} checkable by SMT (e.g. output is sorted, sums match). New learning must keep outputs inhabiting the types; types mined from old behaviour. *New:* types replace labels as what is remembered. **Test:** small transformer, sort then reverse then dedupe tasks; type-check loss vs. replay. **Retention:** old-task exact match.

**LP22. Bounded-equivalence capacity release.** When a region of the network (a head, an MLP block, an adapter) is proven equivalent to an extracted program on a bounded input domain (SMT), delete it and call the program; freed capacity takes the next task. *Neighbors:* N1 round trip, neurosymbolic distillation; new is the equivalence proof as the license to free weights. **Test:** small MLP computing 4-bit add; extract, prove, prune, reuse capacity for 4-bit multiply. **Retention:** add accuracy (via program) and multiply accuracy.

**LP23. Interpolant fault localisation.** When an old property fails after an update, compute an interpolant between pre- and post-update abstractions to localise the neurons responsible; repair only those. *Neighbors:* Arachne, DNN fault localisation; new is interpolation over two model versions. **Test:** small nets, planted regression; localised repair vs. full fine-tune. **Retention:** new and old accuracy after repair.

**LP24. Gradual verification frontier.** Weights split into verified (certified properties, frozen) and unverified (plastic). New learning goes to unverified parts; properties certified over time move the frontier, so the model hardens like gradual typing. *Neighbor:* PackNet/HAT freeze; new is freezing triggered by a verified property, not by task end. **Test:** MLP stream; frontier vs. task-end freezing. **Retention:** old accuracy at equal capacity.

**LP25. Bisimulation retention for agents.** Measure and regularise forgetting as bisimulation distance between old and new policies up to depth k on old environments (behaviour trees, not accuracy). *Neighbors:* bisimulation metrics in RL (Ferns 2004, DBC). **Test:** gridworld agents over 4 tasks; bisimulation regulariser vs. policy distillation. **Retention:** old-task return.

**LP26. Assume-guarantee skill modules.** Each module states what it assumes about its inputs and guarantees about its outputs; a new module only re-verifies contracts it touches, so retention holds modulo contracts. *Neighbors:* P9 effect types, killed composition contracts (that was about labelling hybrids; this is about re-verification scope). **Test:** modular net for 3 composed tasks; add a 4th; contract check vs. full re-test cost. **Retention:** old compositions' accuracy.

**LP27. Proof-of-retention audits.** A fine-tuned model proves to a third party (zero-knowledge, or cheaply-checkable sampling proofs) that it retained capabilities on a hidden test set. Turns retention into something a learner can be paid for. **Moonshot** (zkML is slow). **Test:** tiny MLP with a zk-SNARK library; time to prove 100-example retention.

## D. Logic-shaped memory

**LP28. Unification-addressed memory.** Retrieval by most general unifier instead of embedding similarity: stored patterns with variables match queries exactly, and substitution generalises. *New:* unification as a memory address for neural agents; neighbors are Prolog-style neural theorem provers (Rocktäschel 2017). **Test:** symbolic rewriting tasks; unify-retrieval vs. dense retrieval. **Retention:** old rules' hit rate as memory grows to 1,000 entries.

**LP29. Anti-unification episodic consolidation.** Pairs of episodes are generalised to their least general generalisation (Plotkin); lessons form a lattice, and specific episodes stay instances, so nothing specific is lost. *Neighbors:* ExpeL, DreamCoder abstraction. **Test:** agent router logs; LGG lessons vs. LLM-written lessons. **Retention:** old-episode success.

**LP30. ⊥-token consistency maintenance.** Facts stored as edits; rules as edits that compose; a trainable ⊥ token is predicted when the model's closure on a probe set derives a contradiction. Edits are accepted only if ⊥ is not derivable. *Neighbor:* B6 edge-addressable weights. **Test:** GPT-2 with 100 facts + 10 rules, contradictory edits; ⊥ gate vs. no gate. **Retention:** non-contradicted fact accuracy.

**LP31. Logical-form-addressed weights.** Autoformalise each training fact into a canonical logical form; edits keyed by the alpha-normalised form, so paraphrases hit the same slot and contradictions collide at the same address with opposite polarity. *Neighbors:* B6, SERAC. **Test:** CounterFact paraphrase edits; LF-keyed codebook vs. GRACE. **Retention:** unrelated-fact accuracy and paraphrase generalisation.

**LP32. Herbrand-universe replay.** Data-free replay: enumerate ground terms of the old task's signature up to depth k, label them with the current model *before* the update, replay after. Structure-complete coverage at small depth. *Neighbor:* LwF with synthetic inputs. **Test:** arithmetic / list tasks; Herbrand replay vs. random-input LwF vs. stored replay. **Retention:** old-task accuracy.

**LP33. Relevance-logic locality.** An update from data x may change outputs only on inputs sharing variables with x (relevance logic's variable-sharing principle). Locality defined logically, not by embedding distance. **Test:** synthetic propositional tasks; relevance-masked update vs. MEMIT locality. **Retention:** unrelated-variable query accuracy.

**LP34. Linear-logic capacity typing.** Weight subspaces are linear resources: used by one task unless promoted with "!" (shareable) after passing a stability test. A type checker forbids two tasks writing the same non-! subspace. *Neighbors:* PackNet/HAT; new is promotion/dereliction as the rule for sharing. **Test:** MLP with 8 subspaces, 6 tasks; typed vs. HAT. **Retention:** old accuracy and capacity used.

**LP35. Datalog fixpoint memory.** Lessons are Datalog facts and rules; the agent's memory is the least fixpoint, recomputed incrementally (semi-naive evaluation) on each write; retractions use DRed. Weights only learn to query. *Neighbor:* neurosymbolic KB agents. **Test:** text-world with entity relations; Datalog memory vs. text memory. **Retention:** old-query accuracy after updates.

**LP36. Tableau conflict detection in lesson stores.** Autoformalise lessons; a semantic tableau finds closed branches (inconsistency) and the minimal conflicting set triggers targeted revision. *Neighbor:* physics #31 sheaf cohomology. **Test:** 60 agent lessons with planted conflicts; tableau vs. pairwise NLI. **Retention:** task success with revised store.

**LP37. Knowledge-compilation round trip.** Compile the model's beliefs on a domain into a d-DNNF circuit (exact conditioning queries), update on the circuit, distil back. *Neighbor:* N1 round trip; new is a tractable logical circuit as the intermediate. **Test:** small belief domain (50 propositions); circuit update vs. direct fine-tune. **Retention:** unrelated belief accuracy.

**LP38. Typed holes as learning targets.** Agent code memory holds typed holes; learning fills holes, keeping partial programs valid (Hazel-style live programming). *Neighbor:* N4 `...` frontier. **Test:** NOOA testbed, hole-filling vs. full rewrite. **Retention:** old method tests pass.

## E. Proofs as the memory of agents and provers

**LP39. Re-derivability memory.** Store a lesson only if the current model *cannot* re-derive it (checked by verifier). Memory shrinks as the model improves; when the model degrades, re-derivation fails, which is a forgetting alarm and triggers storage. *New:* memory criterion = non-derivability under current model; neighbors are learned compression and SM1 logs. **Test:** Lean mini-theorems or arithmetic facts; store-if-not-derivable vs. store-all vs. store-random at equal memory. **Retention:** old theorem success after a fine-tune that degrades the model.

**LP40. Redundancy-proof garbage collection.** Delete a lesson when the verifier confirms it is derivable from others, and keep the derivation as a compact proof of redundancy so it can be restored if the base changes. *Neighbor:* reachability GC (P33). **Test:** lesson store over a model upgrade; GC vs. no GC. **Retention:** success after upgrade.

**LP41. Monotone theorem set.** For prover LLMs: a CL rule that the set of kernel-checked theorems must never shrink; the learner's own verified proofs are exact replay. *Neighbor:* killed self-QA replay (unverified); here verification is exact. **Test:** small prover on miniF2F-like synthetic; expert iteration with vs. without monotone constraint. **Retention:** theorem loss count.

**LP42. Proof-sketch memory.** Store lessons as sketches (Draft-Sketch-Prove); details re-filled at use time. Memory = minimal sketch the current model can complete. *Neighbor:* DSP (Jiang 2022). **Test:** sketches vs. full proofs at equal bytes. **Retention:** success on old theorems after new domain training.

**LP43. Proof-repair transport across library versions.** When a library changes (mathlib bump, API change), learn the old-proof→repaired-proof transformation as a delta that transports skills across environment versions. *Neighbors:* PUMPKIN PATCH (Ringer), Baldur. **Test:** synthetic DSL with renamed/re-signatured lemmas. **Retention:** old-version proof success.

**LP44. Lemma-citation replay.** Replay only the lemmas a new task's proofs cite, ordered by the proof dependency graph. *New:* citations as the replay selector. **Test:** sequential rule tasks; citation replay vs. random replay at equal budget. **Retention:** old-task accuracy.

**LP45. Shared-lemma interference predictor.** Forgetting of A after B predicted by overlap of lemmas their proofs use. Gate on target variance first (ledger rule). **Test:** 20 task pairs; Spearman of overlap vs. measured forgetting vs. gradient cosine.

**LP46. Lean-axiom agent memory.** Agent lessons become axioms over an environment model; lessons provable from other axioms are dropped; unprovable but observed ones stay; contradicted ones are revised. Memory = minimal axiom set. **Test:** gridworld facts formalised; axiom memory vs. text lessons. **Retention:** old-room success.

**LP47. Proof-carrying lessons in fleets.** Agents share a lesson with a checkable trace; receivers verify before adopting, blocking contamination. *Neighbors:* physics #21 proofreading, E32 metered lessons. **Test:** fleet of 10 agents with 20% bad lessons; proof-gated vs. vote-gated sharing. **Retention:** old-task success across fleet.

**LP48. Kernel-feedback self-distillation.** OPSD where the teacher's privileged info is exact verifier state (error messages, goal states). *Improvement*. **Test:** Qwen 1.5B on synthetic Lean-like checker. **Retention:** old domain accuracy.

**LP49. Tactic-goal routing.** Route memory and adapters by the exact goal state rather than embedding. **Test:** prover with per-goal-shape adapters vs. one LoRA. **Retention:** old goal-shape success.

**LP50. Rule-granular adapters.** One adapter per inference rule (found by aligning traces to proof steps); tasks are compositions of rules, new tasks add only new rules. *Neighbors:* LoraHub, modular skills. **Test:** synthetic rule systems. **Retention:** old compositions after new rules.

## F. Temporal logic and model checking for agents

**LP51. LTL constitution that accumulates.** User-written LTL specs over agent traces compile into automata monitors that become a permanent loss term for all future updates. Specs accumulate; they're checked, not prompted. *Neighbors:* constitutional AI (text), LTL-constrained RL. **Test:** gridworld agent, 5 specs added over time; monitor loss vs. text constitution. **Retention:** spec violation rate on old specs.

**LP52. Growing shields.** Safety shields (Alshiekh 2018) persist across tasks and grow by automata learning (L*); new tasks are learned inside the shield. *Neighbor:* shielded RL. **Test:** 4 gridworld tasks. **Retention:** old-task safety violations and return.

**LP53. Automata extraction-reinsertion cycle.** Extract a DFA from the model's behaviour on a task (L* with the model as oracle), store the DFA, re-insert by training on DFA-generated strings when the task decays. *Neighbor:* N1. **Test:** Tomita grammars on a small RNN/transformer. **Retention:** grammar accuracy vs. stored replay at equal bytes.

**LP54. Reward-machine library.** Growing library of reward machines composed by product construction. *Neighbors:* Icarte reward machines, LTL transfer (Vaezipoor 2021). *Improvement*. **Test:** office gridworld. **Retention:** old-task return.

**LP55. BMC-gated harness edits.** Before accepting a harness edit, bounded model checking over an abstraction of the harness state machine confirms old traces are still accepted. *Improvement* in a saturated area. **Test:** harness testbed. **Retention:** old task pass rate.

**LP56. Ranking functions for self-improvement loops.** A learned well-founded measure that each self-modification must decrease, guaranteeing termination and ruling out rewrite attractors. *Neighbor:* killed memory-loop Lyapunov *predictor*; here the measure is an enforced constraint. **Test:** synthetic memory-loop policies. **Retention:** old-task performance at loop termination.

**LP57. Inductive-invariant writes.** Synthesise an inductive invariant (Houdini/ICE learning) of the agent's memory update loop from logs, e.g. "every lesson is consistent with all logged successes"; enforce writes that preserve it. **Test:** router lessons. **Retention:** old-regime success.

## G. Moonshots and crazy

**LP58. Löb-consistent self-model.** A provability head predicts "I can do X"; updates must keep it calibrated (if it asserts Prov(X), it does X). Label-free forgetting detection. **Test:** GPT-2 with self-prediction head over 5 tasks. **Retention:** old accuracy plus self-prediction calibration.

**LP59. Dynamic epistemic update operator.** Train [learn Y]X queries: will I still believe X after learning Y? *Neighbor:* D3 hypothetical fine-tuning. **Test:** predict post-update beliefs on 200 edits. **Retention:** prediction accuracy of which old facts break.

**LP60. Univalent task transport.** Isomorphic tasks are identified and skills are transported along the isomorphism (HoTT univalence). **Moonshot**. **Test:** permuted-label tasks with known isos. **Retention:** old-task accuracy.

**LP61. Parametric (free-theorem) skills.** Train skills to be parametric in task-irrelevant features, so new tasks varying only those features cannot interfere. *Neighbor:* equivariant nets. **Test:** permutation-equivariant variants. **Retention:** old accuracy.

**LP62. Random-SAT capacity phase.** Each task adds weight constraints; forgetting onset at a critical constraint density α_c. Risk: ledger capacity-law kill. **Test:** perceptron with sequential tasks; locate α_c. **Retention:** curve itself.

**LP63. Skolemised plans as skills.** Existential goals become Skolem functions stored as callable skills. **Test:** text planning. **Retention:** old goal success.

**LP64. Sequent-calculus curriculum.** Order tasks topologically by proof dependency and replay only cited lemmas. Overlaps LP44 as a schedule. **Test:** rule tasks. **Retention:** old accuracy.
