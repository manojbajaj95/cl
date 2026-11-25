# Root: A LoRA-Writing Learner

Root node (depth 0) · 32 candidate primitives · Ideas only; no experiments run

**Thesis.** A neural **Learner** writes actual low-rank factors `B, A` into a separate, frozen Executor: `W_eff = W + BA`. A skill file, demonstrations, or experience can teach the Learner what to write, but the Executor should not have to reread the file to use the skill. What would make the weights a better programming medium, rather than just a shorter prompt? Give each latent skill an operation that a static file-to-adapter compiler cannot already do: defer a binding, admit a local revision, record only what can be known, or grow into two routable skills when one steering direction stops serving both uses.

**Scope.** The [idea ledger](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md) requires a new object or operation and retention in the first test. The [weight-programming flood](https://github.com/manojbajaj95/cl/blob/devin/1795538334-programs-weights-flood/ideas/flood/programs-weights.md) and its [triage](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md) already cover IRs, linkers, ABIs, and weight macros. This is not the killed WSP repair, residual-skill bits, coded merge audits, prompt-addressable checkpoints, or another edit-site selector ([model-guided edits](https://github.com/manojbajaj95/cl/blob/devin/1795538570-model-guided-edits/tree/model-guided-edits.md)). It does not rely on the Executor rewriting itself. Cards posit candidate primitives, not confirmed novelty; if an equal-cost ordinary adapter, router, or text policy reproduces the result, that is a negative result.

## Literature check

Used Hugging Face Papers search to locate papers and checked the linked arXiv and ACL Anthology abstracts for mechanisms. These comparisons are an abstract-level screen, not a claim to have read every full paper or established priority.

| Already available | What this root has to add |
|---|---|
| [HyperNetworks](https://arxiv.org/abs/1609.09106) generate another network's weights; [shared hypernetwork adapters](https://arxiv.org/abs/2106.04489) condition on task and layer. [HyperTuning](https://arxiv.org/abs/2211.12485) produces soft prefixes or LoRA parameters for frozen T5 from few-shot examples; [HypeLoRA](https://arxiv.org/abs/2603.19278) generates LoRA factors with a shared hypernetwork. | Generating factors with a network, even without backprop at deployment, is not the proposal's novelty. |
| [Text-to-LoRA](https://arxiv.org/abs/2506.06105) generates an adapter from a task description in one pass and tests unseen tasks; [Drag-and-Drop LLMs](https://arxiv.org/abs/2506.16406) generates weights from a handful of unlabeled prompts via a hyper-convolutional decoder. | “Write what a skill file does into weights” has direct precedents. Test what can be changed, composed or learned *after* the adapter has been installed, not only zero-shot generation. |
| [Doc-to-LoRA](https://arxiv.org/abs/2602.15902) amortizes context distillation into a forward pass; [Internalizer](https://arxiv.org/abs/2610.11715) uses a largely shared hypernetwork trunk and small model-specific interfaces. [Hypernetwork knowledge injection](https://arxiv.org/abs/2607.19604) trains a writer for a fixed fact-bearing LoRA. [The Override Gap](https://arxiv.org/abs/2604.23750) studies conflicts with pretrained priors, and [Doc-to-LoRA Analysis](https://arxiv.org/abs/2611.30825) reports wrong-fact and multi-document interference. | Don't assume document compression implies selective activation, correct exceptions, or safe accumulation. Neither a stronger delta nor another portable writer is the proposed operation. |
| [Learning by Distilling Context](https://arxiv.org/abs/2209.15189) internalizes prompted performance by fine-tuning; [GenPI](https://arxiv.org/abs/2411.15927) also learns to regenerate prompts and rationales; [OPCD](https://arxiv.org/abs/2602.12275) distills context using student trajectories. [From LoRA to Language](https://arxiv.org/abs/2611.09454) recovers parts of skill documents more successfully by running the adapter than by reading its weights. | Compare against per-skill distillation, not just the unadapted base. Recovering a prose description is not a new primitive; behavioral agreement may still leave revision semantics unidentified. |
| [MEND](https://arxiv.org/abs/2110.11309) transforms a fact edit's decomposed fine-tuning gradient into a local update. [Task arithmetic](https://arxiv.org/abs/2212.04089) edits behavior with vector sums and differences; [LoraHub](https://arxiv.org/abs/2307.13269) fits combinations of library modules; [Arrow](https://arxiv.org/abs/2405.11157) routes inputs to pre-existing LoRAs. [LoRA Superposition](https://arxiv.org/abs/2610.30691) sums same-task deltas across contributing backbones, but the leave-one-backbone-out result is near zero. | Compare against learned point edits, existing-span composition, and routing. Equal tensor shape is not evidence a skill ports to an unseen host. |
| [Self-WSP](https://arxiv.org/abs/2611.28833) self-edits, sometimes matched by random search; [self-rewriting](https://arxiv.org/abs/2611.21885) uses model reasoning and white-box inspection; [SelfWrite](https://arxiv.org/abs/2611.29513) writes programs constructing low-rank edits and selects via a hidden gate. [WSP writes ICL](https://arxiv.org/abs/2611.26841) often transcribes ICL residual shifts into weights, with wording sensitivity. [Controlled WSP repair](https://arxiv.org/abs/2611.25613) finds fixed numerical projections can match interactive selection in some cases. | A neural writer must earn its keep against analytic edits and budget-matched search. Neither gradient-free edits nor a text model writing an edit program is a new object here. |
| [DEN](https://arxiv.org/abs/1708.01547) already duplicates and timestamps units to avoid semantic drift. [CN-DPM](https://arxiv.org/abs/2001.00689) grows an expert mixture without task IDs; [SEMA](https://arxiv.org/abs/2403.18886) grows adapters on representation shift; [DIMoE-Adapters](https://arxiv.org/abs/2605.07494) evolves its pool from expert optimization dynamics; [CDSP-MoE](https://arxiv.org/abs/2512.20291) uses gradient conflict to prune shared topology into experts. | A negative cosine, a new expert, or copying the parent is not enough. Test an observable distinction between a one-direction continuation and a warranted split, and whether the resulting children preserve or improve a specific property. |
| [O-LoRA](https://arxiv.org/abs/2310.14152) separates task subspaces; [InfLoRA](https://arxiv.org/abs/2404.00228) designs update subspaces to reduce interference; [LLaVA-MoLE](https://arxiv.org/abs/2401.16160) uses sparse LoRA experts against data conflict; [MoSEs](https://arxiv.org/abs/2511.06237) selectively expands and recombines subexperts; [MoRAM](https://arxiv.org/abs/2506.21035) grows reusable self-activating rank-one memories. [Progressive Nets](https://arxiv.org/abs/1606.04671) and [PackNet](https://arxiv.org/abs/1711.05769) provide strong grow/freeze and partition controls; [PCGrad](https://arxiv.org/abs/2001.06782) tries to resolve conflicts without growing capacity. | Growth must beat sharing, isolation, recombination, and the same expansion with another birth rule. Charge the router and the inherited parent, not just child rank. |
| [SAPT](https://aclanthology.org/2024.acl-long.625/) aligns learning and selection of parameter-efficient blocks through shared attention. [Graph Coloring for Multi-Task Learning](https://arxiv.org/abs/2509.16959) groups batches by gradient compatibility without requiring separate skills. [Skill1](https://arxiv.org/abs/2605.06130) co-evolves agent skill selection, utilization, and distillation under shared rewards. | Pooling or grouping evidence is a baseline, not evidence that a single live skill can become two separately callable policies. |

**Shared CPU-first protocol.** Use tiny frozen linear or two-layer nonlinear Executors, finite-state tasks, and a small neural factor writer. An enumerated or closed-form fixture can first falsify the claimed separation; if it survives, ask whether the neural Learner can infer the write on held-out skills and orders. Compare at equal supervision, write attempts, live bytes (including shared parent, routing and source state), inference compute, and deployment inputs. Compare source-file steering, same-rank per-skill distillation, an ordinary factor writer, and the closest named control where relevant. Price offline writer training separately. Compare products `BA` or intervention effects, never raw factor cosine: `BA = (BQ)(Q⁻¹A)` for invertible `Q`. Charge explicit runtime metadata or probes; do not smuggle the skill file, future outcome, or oracle task ID into the input.

**Old-task check on every card.** Establish the normal A/B behavior first (including one rare slice), introduce C, then D, then return to A/B. Evaluate hidden held-out original requests through the same live interface, no oracle routing or adapter bypass, immediately after each change and on later returns. Report each task and worst drop against a preregistered no-change tolerance, together with new-skill learning; doing nothing cannot win on retention alone. Each card adds a behavioral slice to that common check.

## A · What can be written when the specification is incomplete?

### LL01 · Compile a question into the skill
- **Mechanism:** When two plausible readings imply different writes, emit one low-rank policy that does their common work but itself asks a discriminating question on the first request where they diverge. The interaction result binds future factors; the original file is no longer needed.
- **Nearest prior / gap:** Text-to-LoRA emits a point adapter; active learning selects a label query. The proposed object is a persistent, partially usable adapter with a specific unresolved choice that its Executor can surface.
- **Cheapest first test:** Use two incompatible rounding rules with identical demonstrations and a small action vocabulary containing ordinary answers and one clarification. Compare always-ask and uncertainty-triggered existing writers at equal question count; hold out request orders.
- **Old-task retention:** Check old rounding and formatting requests, especially ones sharing the ambiguous inputs but already carrying sufficient context.

### LL02 · Freeze the rule, defer its parameter
- **Mechanism:** Write the rule's factors once with a single replaceable inner coordinate `BA = U M V`; bind a later semantic parameter by writing only `M`. Its meaning must survive an intervening unrelated update, not merely a first successful binding.
- **Nearest prior / gap:** HyperTuning regenerates task parameters and flood P35 proposes weight macros. The distinction is a late-binding operation over a *live* skill: late information cannot rewrite the rule, and the old symbol can be rebound after another write.
- **Cheapest first test:** Learn unit conversion with a rate revealed only after installation. Freeze the surrounding factors, change the rate twice with an intervening skill, and compare full regeneration plus a same-size scalar conditioner.
- **Old-task retention:** Recheck fixed conversion rules and requests that explicitly supply their own rate.

### LL03 · Write the exception before its default exists
- **Mechanism:** Install a low-rank exception whose behavior shadows any later default in its scope, irrespective of installation order. The writer receives the current factors and writes no extra prompt instruction.
- **Nearest prior / gap:** The Override Gap measures overriding a known pretrained prior. Here the default is not known or installed when the exception is authored; ordered runtime exception dispatch is the control.
- **Cheapest first test:** Enumerate a tiny category lattice, writing a singleton exception before or after several defaults, including unseen default values. Compare additive adapters and ordinary ordered dispatch at identical information.
- **Old-task retention:** Check all established exceptions and contexts to which the later default should not apply.

### LL04 · Give a latent rule a live caller
- **Mechanism:** The skill write makes an internal action conditional on the result of a regular Executor subcall, not on a value snapshotted from the file or its demonstrations. Later changing that subcall's implementation updates the caller's behavior without rewriting the caller.
- **Nearest prior / gap:** The flood's weight-space linker connects named residual directions. Test the narrower property of dynamic behavioral binding: downstream calls follow a replacement supplier with no edit to the calling factors.
- **Cheapest first test:** Fit two small sorting policies that consume an intermediate comparator; replace the comparator with a held-out ranking. Compare explicit function composition and a joint distilled policy.
- **Old-task retention:** Check the original sort mode and unrelated users of the replaced comparator.

### LL05 · Write a skill that defers to new evidence
- **Mechanism:** Generate factors that cease their own steering on exactly the portion of an episode where an observable event discharges the skill's requirement. Do not uninstall the adapter or use a global timer.
- **Nearest prior / gap:** DnD installs task adapters and OPCD distills trajectories; a learned gate can already suppress an adapter. The hypothesis is that the writer can compile a reusable *within-episode discharge condition* into the update, not just choose whether to load it.
- **Cheapest first test:** In a finite-state form-filling game, generate “ask once until verified”; interleave verified and unverified forms and withhold some event orders. Compare a hand-coded discharge gate and context distillation.
- **Old-task retention:** Check the old rule to keep asking on missing verification and an ordinary task where repeated confirmation is required.

### LL06 · Write a contrastive scope, not two behaviors
- **Mechanism:** Encode which *relation* between two observable states licenses an effect. Examples specify “change the reply when the owner changes,” not a lookup table for owners; the writer must make the same update respond to unseen pairs.
- **Nearest prior / gap:** WSP-writes-ICL often installs a residual offset keyed to familiar formats. The gap is holding the two state marginals fixed while generalizing a relational scope; ordinary context distillation with the same pair supervision may tie.
- **Cheapest first test:** Train on pairs of two-bit records with an owner relation; withhold fresh combinations and swap pairings at fixed marginals. Compare a plain writer and a relational-feature adapter.
- **Old-task retention:** Test old pairwise comparisons and unrelated owner changes that must not trigger this skill.

### LL07 · Make a write commute with an observable transformation
- **Mechanism:** The Learner accepts a desired effect and a transformation of inputs/outputs, and emits a write that respects the transformation at the behavioral level. One learned effect can then steer rearranged requests, not just familiar serializations.
- **Nearest prior / gap:** Text-to-LoRA tests unseen task generalization and WSP-writes-ICL reports wording fragility. Ordinary equivariance is not new; the candidate object is a generated edit parameterized by a transformation, with equivariance of the *increment* rather than a new equivariant Executor.
- **Cheapest first test:** Generate field-selection skills for record permutations on a frozen non-equivariant MLP. Hold out permutations and compare a canonicalization wrapper and augmented distillation at equal data.
- **Old-task retention:** Check old order-sensitive field positions; the new invariant skill must not erase behavior that legitimately depends on order.

### LL08 · Train the writer to leave a missing distinction missing
- **Mechanism:** Emit factors that implement the identified part of a skill but leave the disputed effect at the base policy. Store only a compact alternative identifier for later adjudication; don't silently pick the most familiar reading.
- **Nearest prior / gap:** Doc-to-LoRA can confuse facts and HyperTuning writes a point adapter. Standard abstention is a baseline; the claim is partial compilation with an identifiable untreated slice despite useful changes elsewhere.
- **Cheapest first test:** Describe a policy with one deliberately underspecified case. Shuffle the hidden true convention independently of all observed evidence; compare ordinary distillation and a masked explicit policy.
- **Old-task retention:** Check old defaults on the untreated slice and both known exceptions learned before the new partial skill.

## B · Revise installed skills without reconstructing their source

### LL09 · Compile an edit port for a counterfactual field
- **Mechanism:** When the original skill is written, expose a small factor coordinate for “replace rule X” whose meaning is defined by comparing original and amended policies on paired interventions. The port is part of the write interface, not a human-readable recovery of the source.
- **Nearest prior / gap:** MEND learns a point editor after the fact; From LoRA to Language recovers parts of a skill document. Test whether a writer can prospectively install a handle that makes later edits separable even when two rules happened to give the same answers.
- **Cheapest first test:** Generate two tiny decision procedures with an accidentally redundant condition; later replace just that condition and introduce combinations that break the redundancy. Compare against a pooled editor and independent factor slots at equal bytes.
- **Old-task retention:** Check unchanged conditions and all previously legal conjunctions, not only the edited column.

### LL10 · Substitute a witness while keeping the rule
- **Mechanism:** In a skill that can execute the same recommendation by two paths, the Learner rewrites which path the Executor uses, without changing the recommendation. Later failures of the former path should not break the skill.
- **Nearest prior / gap:** GenPI can elicit reasons for an internalized prompt; changing generated explanations does not establish a changed execution dependency. Test an intervention on the actual supplier, against ordinary auxiliary supervision of path choice.
- **Cheapest first test:** Give a toy agent two equal-valued sensors with different later outages. Ask the writer to substitute one as evidence, then intervene on sensors separately; compare distillation on action and path traces.
- **Old-task retention:** Check ordinary decisions with inconsistent sensor readings and old tasks whose evidence should still depend on the original sensor.

### LL11 · Swap a default with a previously exceptional action
- **Mechanism:** Compile one repair that changes which behavior is the fallback while preserving a named carve-out for the former default, without reconstructing the remaining exception map.
- **Nearest prior / gap:** Task arithmetic can negate/add a direction, while The Override Gap boosts a contradictory response. This operation changes the *priority* relationship between two already installed behaviors; an explicit decision list is the strong control.
- **Cheapest first test:** A 16-state policy has a fallback and three mutually overlapping exceptions. Swap the fallback with one exception using one narrow revision and test unused overlaps against matched distillation and explicit lists.
- **Old-task retention:** Score unchanged exceptions, particularly old cases satisfying two predicates.

### LL12 · Write only the part the user can still cancel
- **Mechanism:** A skill's output contract declares an action that may be undone before commitment but not after. The writer produces two phase-specific residuals whose effect switches on an observable commitment receipt.
- **Nearest prior / gap:** OPCD can imitate successful trajectories and ordinary transactions implement cancellation. The new hypothesis is authoring a cancellation boundary into factors from paired traces, without teaching the whole skill again or saving an old model.
- **Cheapest first test:** Use a tiny booking automaton with identical first actions and differing commitment times; introduce a late cancellation reason never seen with some ordinary requests. Compare a transaction wrapper and on-policy distillation.
- **Old-task retention:** Check ordinary completions and old cases whose original irreversible commit must stand.

### LL13 · Make a correction survive a change in upstream confidence
- **Mechanism:** Install a correction relative to the *current* confidence gap supplied by the Executor, rather than adding a fixed logit amount. Train the writer to preserve specified regions where stronger new upstream evidence should still win.
- **Nearest prior / gap:** The Override Gap uses conflict-aware boosting and the ledger's MX1 treats correctability at matched margin. Test a rescaling-resistant rule for how much evidence can overturn the edit after the upstream producer changes, not another layer or boost choice.
- **Cheapest first test:** In a two-head classifier, randomly change upstream calibration after writing. Compare magnitude-matched selective boosting, a hand-coded gap rule, and full recalibration.
- **Old-task retention:** Check both originally decisive and borderline examples where the old confidence ordering still matters.

### LL14 · Split the right to use a skill from the right to change it
- **Mechanism:** A shared factor supplies a skill to two callers, but only one caller's corrections may update a shared semantic clause; the other's observations can write only into a private residual. Test whether this asymmetric influence can be learned from prior revision examples.
- **Nearest prior / gap:** Arrow separates which adapter a request uses; PackNet separates which parameters can change. The candidate is two independently specifiable interfaces for *one live behavior*: execution dependency and correction authority.
- **Cheapest first test:** Two workflows call the same unit normalizer; present equally plausible contrary amendments from the designated and undesignated caller. Compare equal-size fixed write masks and separately distilled skills.
- **Old-task retention:** Check unchanged callers and original private exceptions after both accepted and refused edits.

### LL15 · Unlearn a premise but preserve what has independent support
- **Mechanism:** Write a skill with two interchangeable evidentiary supports, then retract one support without erasing decisions that have the other. The surviving policy uses live support rather than storing a duplicate skill.
- **Nearest prior / gap:** Negating task vectors is a coarse deletion, and exact unlearning reruns a counterfactual training history. Here the object is a partially retractable behavior with explicit alternative supports; a symbolic support graph is a required control.
- **Cheapest first test:** Teach a small classifier from two independently overlapping policy sources. Retract one and compare subtraction, equal-byte support tracking, and retraining on the surviving source.
- **Old-task retention:** Check older decisions supported by both sources, surviving-exclusive cases, and unrelated old skills.

### LL16 · Edit a skill's response to being edited
- **Mechanism:** For a fixed current behavior, author a new edit policy that distinguishes future amendments from corrections of observations. The writer can change which evidence changes future factors without changing the prescribed action today.
- **Nearest prior / gap:** MEND learns updates and the self-modifying-architecture root explores learning rules. This card asks for an independently replaceable amendment rule on one generated LoRA, evaluated against a sidecar with the same evidence and bytes.
- **Cheapest first test:** Generate two identical small policies; switch which of two observed event classes may amend one. Feed identical future events and compare fixed learning-rate or fixed-mask updates and a symbolic amendment rule.
- **Old-task retention:** Check equality before any amendment, then check old regimes unaffected by authorized amendments and all old behavior after unauthorized ones.

## C · Auto-growing skills: when one steering direction should become two

Begin with **one** skill, not a library of oracle-labeled tasks. An incoming episode provides evidence about the edit it wants, but at serve time only the ordinary observed prefix, or a charged diagnostic, can choose a branch. A negative gradient cosine alone neither proves incompatibility nor tells the Executor which skill to use. The split tests need four controls: a stronger single skill at the same total rank, sharing with gradient surgery, a same-budget grow/freeze or task-free mixture, and an oracle branch label only as an upper bound. Require no split on matched noise and check the pre-split behavior **through the resulting children**, not via a hidden frozen parent.

### LL17 · Birth certificate for two steering directions
- **Mechanism:** Accumulate a finite witness that no legal shared write can meet both improvement floors at a fixed retention and rank budget, plus two feasible branch writes and an observable routing cue. Hand the witness to the Learner to write both children. Lack of a witness leaves one skill, not a forced split.
- **Nearest prior / gap:** DEN splits to avoid drift, SEMA grows on representation shift, DIMoE evolves via optimization dynamics, and CDSP-MoE uses conflict structurally. This candidate requires a *matched-budget shared infeasibility plus callable feasibility* witness, not a drift or conflict threshold.
- **Cheapest first test:** On a frozen two-layer model, enumerate one quantized rank-two delta versus two rank-one deltas plus a charged cue. Alternate separable requests demanding opposite effects, cases with a feasible common update, and noisy labels. Match overall bytes and observations with CN-DPM-style growth and PCGrad.
- **Old-task retention:** Exercise the original unsplit skill on common and rare inputs now routed through either child, including unconflicted calls near the cue boundary.

### LL18 · Give the two children one inherited promise
- **Mechanism:** Emit a shared parent update and two disjoint deviations. Impose agreement on one intentionally held-in-common ordinary subroutine; subsequent corrections may move the children apart elsewhere but must still be served once to both on that subroutine.
- **Nearest prior / gap:** DEN duplicates units, Progressive Nets use lateral transfer, MoSEs shares recombined subexperts. Test *one teachable inheritance*: a later correction to the shared promise takes effect in both children without revisiting their private rules.
- **Cheapest first test:** Split a formatter into two incompatible retry styles, then change one formatting convention neither child has seen. Compare two clones, a parent-plus-residual parameterization without inheritance supervision, and MoSEs-style recombination.
- **Old-task retention:** Check old formatting and each original retry case after both the split and the shared correction.

### LL19 · Delay splitting until an observable separator exists
- **Mechanism:** Keep opposing feedback as provisional evidence, but propose a single boundary-disambiguating question or observation. Only write children when that observation predicts which branch to run before the irreversible action. Otherwise retain one conservative behavior.
- **Nearest prior / gap:** CN-DPM grows from a task-free stream, and Graph Coloring separates optimization-compatible tasks. Neither abstract establishes birth conditional on buying a *pre-action* separator for different desired behaviors of the same observed input; compare a mixture with active queries.
- **Cheapest first test:** Use two streams with identical input and gradient statistics. In one, one cheap yes/no question separates goals; in the other, outcome labels appear only afterward. Match question budget and measure starts that can be served correctly.
- **Old-task retention:** Test no-question old requests, older explicit preferences, and old users whose prefixes match the ambiguous cases.

### LL20 · Fork only the conflicting phase
- **Mechanism:** Write two residuals that take different actions during an observed conflict window and then produce the same downstream handoff state. A request can take separate paths without becoming two whole skills.
- **Nearest prior / gap:** MoRAM grows rank-one experts and LLaVA-MoLE specializes sparse experts. A phase-local split with an explicit reconvergence target differs from allocating a new expert for the entire trajectory; compare a shared-suffix MoE with the same phases.
- **Cheapest first test:** In a toy form workflow, draft procedures diverge but both must hand the same normalized state to an unchanged submitter. Train on few paths and hold out prefix/suffix combinations.
- **Old-task retention:** Run old procedures that enter through different branches and old suffix consumers of the normalized state.

### LL21 · Inherit only one side of a LoRA factorization
- **Mechanism:** A split can fork the observable trigger (input factor) while sharing what changes (output factor), or fork what changes while keeping the trigger common. The writer chooses the cheaper split by testing interventions on inputs and feedback, not by comparing raw factor orientations.
- **Nearest prior / gap:** HypeLoRA studies fixed factors and MoRAM treats rank-one factors as key/value associations. The proposed operation diagnoses which side must fork in a live, multiply used skill and transmits future fixes to the still-shared side.
- **Cheapest first test:** Generate matched streams where only input conditions change, only action directions change, or both change. Use known intervention signatures on `BA`; compare always-fork-both and a fixed dictionary with the same bytes.
- **Old-task retention:** Check old triggers and old output directions separately after the first post-split correction.

### LL22 · Fork a skill's learning before forking its answers
- **Mechanism:** Keep a single serving adapter when two branches still agree on current actions, but allocate separate low-rank amendment coordinates once their *responses to the same future feedback* are observably different. Close the split if the predicted difference fails an intervention.
- **Nearest prior / gap:** DEN reacts to semantic drift; PCGrad reduces present training conflict. The gap is a branch justified by incompatible revision rules even at zero serving disagreement, not by a new task or current error.
- **Cheapest first test:** Use two controllers with identical current actions but distinct rules for which feedback is reliable. Compare a single meta-updater, early clone, and outcome-triggered clone under balanced future feedback events.
- **Old-task retention:** Check current behavior through both amendment routes and revisit the original policies after a feedback sequence only one branch should obey.

### LL23 · End a split without forgetting how to split again
- **Mechanism:** When the children become behaviorally and developmentally compatible, merge their live factors but retain only the tiny *separating witness* that originally justified them. Recreate children from fresh evidence and the witness, never by restoring child deltas.
- **Nearest prior / gap:** Task arithmetic and LoraHub merge current adapters; DEN timestamps splits, and DIMoE reduces redundant capacity. The gap is reuse of the reason for a past split after its policy factors are discarded, explicitly not the killed prompt-addressable checkpoint.
- **Cheapest first test:** Run incompatible → compatible → differently incompatible cycles with a stable observable separator. Charge witness bits and fresh observations; compare fresh SEMA-style growth, storing the children, and always remaining split.
- **Old-task retention:** Check old requests on every cycle, especially during the merged period and when the next split assigns some requests differently.

### LL24 · Transfer a split, not either child
- **Mechanism:** Learn a relationship between the two branches of a particular skill (for example, the upstream cue and how it changes downstream authority), then use it to split another still-unified skill while writing both new adapters from that skill's evidence.
- **Nearest prior / gap:** Task arithmetic transfers analogies as deltas and LoRA Superposition combines existing weights. The candidate is transfer of the *decision to separate and what must stay shared*, not transporting child tensors, task vectors, or model coordinates.
- **Cheapest first test:** Teach a distinction between advisory and binding outcomes in one toy workflow; provide scant evidence in a new workflow with remapped actions and unrelated factor directions. Compare a pretrained task-free router and analogical task arithmetic; shuffle learned separation cues at fixed marginals.
- **Old-task retention:** Run the source children and unchanged calls in the receiving skill before and after the inferred split.

## D · Teach the Learner to write better skills

### LL25 · Learn from a successfully refused write
- **Mechanism:** When an attempted edit changes an unrelated output and is refused, train the writer on the *difference between the requested effect and the effect that caused refusal*. The next write must retain the first effect while omitting the second; a refusal need not discard all useful supervision.
- **Nearest prior / gap:** SelfWrite's hidden gate rejects candidates and MEND trains for localized edits; [SPACE-LoRA](https://arxiv.org/abs/2609.34453) suppresses new responses on sensitive old directions. The proposed training datum is a labeled partial success from one refused write, tested for transfer to a new skill with remapped input features.
- **Cheapest first test:** Simulate bad edits whose useful and harmful effects are independently varied. Compare scalar rejection, MEND-style locality supervision, and an analytic projection with the same labeled interventions and trials.
- **Old-task retention:** Recheck the old behavior implicated by the refusal and a hidden related slice never used to label it.

### LL26 · Learn to write a cheaper next correction
- **Mechanism:** Produce today’s requested adapter under two simulated future amendments. Distill into the writer the placement that makes both amendments possible by touching fewer factor coordinates, without making either amendment now.
- **Nearest prior / gap:** MEND optimizes immediate locality, [DUET](https://arxiv.org/abs/2611.29269) constrains updates to preserve old and new losses, and the repository studies relearnability. This card targets *rewritability at fixed behavior*: train a compiler over alternative factorizations with different costs under a fixed write interface, not arbitrary gauge rotations that are free to undo.
- **Cheapest first test:** Freeze permitted write ports of a tiny model and enumerate behavioral ties now with different costs for later changes. Compare spare rank, standard meta-initialization, and per-amendment refit under the same edit budget.
- **Old-task retention:** Test both amendments in either order and include original behavior that never called the edited port.

### LL27 · Learn from pairs that agree now but disagree after an edit
- **Mechanism:** Construct writer training pairs with identical skill rollouts but different response to a labeled amendment. Update the Learner to reproduce the amendment contrast, not to reproduce arbitrary coordinates of the teacher adapter.
- **Nearest prior / gap:** Text-to-LoRA reconstructs adapters and OPCD matches behavior on trajectories. The candidate supervision is agreement on a *counterfactual write response*, distinct from predicting another ordinary task output.
- **Cheapest first test:** Meta-train on boolean policies with syntactically different, observationally equivalent source rules; hold out amendments that expose the distinction. Compare adapter reconstruction and joint distillation that receive the same amendment traces.
- **Old-task retention:** After the amendment, recheck all original cases where the two rule readings should still agree.

### LL28 · Teach direction from the timing of a correction
- **Mechanism:** Train the writer with pairs in which the same feedback arrives at different causal points in a workflow. Emit distinct low-rank writes so that feedback changes the preceding decision it actually concerns rather than every decision associated with a similar final outcome.
- **Nearest prior / gap:** OPCD uses student trajectories; WSP-writes-ICL converts examples into offsets. Causal credit assignment itself is known. Test whether the *time of intervention* is sufficient supervision to transfer a local write across unseen paths without a layer or task label.
- **Cheapest first test:** A two-choice automaton returns identical terminal errors, but at different controlled times. Match timestamps and interventions for an eligibility-trace control and a trajectory-conditioned writer; swap timings to check the claimed dependence.
- **Old-task retention:** Check the original action in the other phase and variants of old workflows that interleave the two phases.

### LL29 · Compile behavior from positive and negative permissions
- **Mechanism:** The writer learns a correspondence between “must do” and “must not do” descriptions of the same default policy. A small forbidden-action set constrains what to write even when no positive example demonstrates the permitted action.
- **Nearest prior / gap:** Text-to-LoRA maps descriptions to adapters, and ordinary constrained policy learning uses forbidden actions. The question is whether learning paired permissible and forbidden specifications lets a writer perform a held-out change with strictly less supervision than both controls, not whether a model can learn prohibitions.
- **Cheapest first test:** Meta-train on action tables expressed as either permissions or prohibitions; evaluate new action sets under same prompt length. Compare explicit masks and a point writer trained with equal mixed-format data.
- **Old-task retention:** Recheck old permitted actions and genuine old prohibitions that overlap the new action vocabulary.

### LL30 · Learn from two sources that request the same effect for different reasons
- **Mechanism:** Train the Learner to separate the *shared effect* from which source authorizes it by withholding one source at a time. At serve time the write implements the shared effect only when an observable authority remains valid.
- **Nearest prior / gap:** Shared hypernetwork adapters condition on task; MEND handles edits pointwise. Unlike LL15's retraction operation, this is a training signal for learning authorization from missing sources, benchmarked against symbolic provenance and pairwise distillation.
- **Cheapest first test:** Generate synthetic policy documents with overlapping permissions and matched marginal authority rates. Hold out source combinations and invalidate one source midstream; use a source-shuffle and a sidecar with the exact same evidence.
- **Old-task retention:** Check old agreements as well as old rules authorized by a different standing source.

### LL31 · Teach a skill write by omission from an otherwise identical episode
- **Mechanism:** Pair two teaching trajectories differing only because an opportunity to exercise the skill was removed in one. The writer emits a factor update sensitive to the opportunity, not merely to the action emphasized in the successful episode.
- **Nearest prior / gap:** Drag-and-Drop LLMs reads unlabeled prompt batches and WSP-writes-ICL measures activation shifts. Neither a negative example nor an activation contrast is new; the hypothesis is that controlled *availability* rather than labeled desired action identifies what to write on a new opportunity structure.
- **Cheapest first test:** Remove one affordance from a toy routing game while preserving the visible goal and other choices. Compare action-labeled demonstrations, ordinary paired distillation, and opportunity labels with no matched episode.
- **Old-task retention:** Check old paths using the same affordance for a different goal and paths where it was already absent.

### LL32 · Ask the writer to predict when its own teacher is insufficient
- **Mechanism:** Train the Learner to output either factors or a minimal missing *kind of evidence* such as an old-boundary test, a positive example, or an observed cue. Train on pairs where adding the right evidence changes which edits are admissible while adding an equally informative-looking but irrelevant example does not.
- **Nearest prior / gap:** MEND learns a point update and ordinary active learning requests labels. The candidate is a query over the *interface for writing a skill*, not a confidence score or general “need more data” refusal. LL01 asks during execution; this one chooses what evidence unlocks a write before installation.
- **Cheapest first test:** In a simulated sequence of 2-bit policies, vary which evidence source makes two candidate writes distinguishable. Compare active label selection and a fixed evidence checklist at equal query and annotation costs.
- **Old-task retention:** Check old behavior after both writes and refusals, including requests that motivated the held-out boundary test.

## Ranked deeper questions

1. **When should one live steering skill split into two (LL17–LL24)?** Can a Learner identify both the absence of a useful shared write and the presence of a serve-time separator without task labels, at lower total cost than trying both architectures? Start with an exact finite witness, then hold out conflict streams and make the writer infer it. If equal-budget single-skill sharing or task-free mixture growth ties, or if the cue exists only after action, do not count the split as a win.
2. **Can the Learner preserve the meaning of a future edit, not just today's behavior (LL02, LL09, LL16, LL26–LL27)?** Find two presently indistinguishable skills with different lawful later changes. Ask whether the writer can produce an edit interface that generalizes to unseen amendment families at lower cost than retaining the original file, separate factor slots, or a conventional editor.
3. **What is the smallest useful partial write under incomplete instructions (LL01, LL03, LL05, LL08, LL32)?** Determine whether a generated adapter can do the identified work, leave the unidentifiable part untouched, and acquire exactly the missing evidence. A file with an explicit fallback or question is the baseline; no gain at matched interaction and retention means this should stay in text.
4. **Does the medium earn its cost after the first write?** In a matched stream, account for total source storage, writer training and inference, serving tokens, write attempts, and failed edits. Compare the best primitive against text skills, per-skill distillation, a static text/prompt-to-LoRA writer, and a routed library. Look for a regime with repeated revisions or growth in which one operation improves adaptation *and* preserves normal old-task service; otherwise factor generation is mostly a deployment trade-off.
