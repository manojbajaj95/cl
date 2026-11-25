# NOOA-style agents: continual-learning proposer batch 1

Source: NVIDIA Object-Oriented Agents (NOOA, arXiv 2607.20709, github.com/NVIDIA-NeMo/labs-OO-Agents). An agent is a Python object: fields are durable model-visible state, methods are actions, a method whose body is `...` is completed at runtime by an LLM loop (CodeAct or Predict), docstrings are prompts, return annotations are validated contracts, arguments are passed by reference as live objects, and an optional memory store (ACT-R activation, decay pruning, typed `kind:key` references to live state) persists across tasks. ARC-AGI-3 agents persisted ~4.4k lines of executable world-model code across 25 games.

What NOOA uniquely exposes for continual learning: (1) a machine-checkable boundary between knowledge held in **code** and knowledge held in **weights** (the `...` frontier), (2) an **agent-authored class hierarchy**, (3) a **reference graph** from memories to live objects, (4) typed contracts on every model-implemented call.

Pitched as ambitious-but-doable bets: each has a cheap first pilot, the simple baseline that would tie it, and a kill line.

Screened against the idea ledger (PR #6). Not repeated: Agent Toolbox / tools-vs-lessons under drift (narrowed survivor pending; N4 is about the model changing, not the API), composition contracts, skill re-shelving, HK1–HK8 harness gates/fork-and-route, HW1, circuit decompilation, Cortex/ENGRAM-style consolidation as stated, self-pruning. Methods rule applies to every arm: length-matched filler and source-fit entropy-matched temperature arms wherever context or lessons are compared; seed CIs; target variance must exceed seed variance before any predictor is tested.

| Card | One line | First pilot | Kill line |
|---|---|---|---|
| N1 Round-trip consolidation | Distil an agent-written helper into weights, then decompile it back into code: the decompiled program generalizes beyond the original | CPU/1 GPU-h, Qwen2.5-Coder-1.5B LoRA, 12 string/grid-transform families | Decompiled program ≤ equal-compute "rewrite and generalize this helper" + 3 pp held-out |
| N2 Inheritance-shaped adapters | The agent's own subclass tree is the LoRA sharing topology for its `...` methods | CPU, Qwen2.5-0.5B, 8 typed method families over 3 waves | ≤ TreeLoRA gradient-similarity tree and a random tree of equal shape |
| N3 Reachability forgetting | Prune memories unreachable from live state/code (GC) instead of by activation decay | CPU, synthetic NOOA world, no training | Success-vs-store-size curve within CI of ACT-R decay and of size-matched self-pruning |
| N4 The `...` frontier after a model upgrade | Code written by an old model caps a new model; reverting selected methods to `...` recovers it, and the frontier choice transfers | OpenRouter + local 0.5B→1.5B, 20 methods | Best mixed frontier ≤ max(all-code, all-`...`) + 2 pp |

---

## N1 Round-trip consolidation: weights as a denoiser for agent code

**Bet.** Agents in NOOA write deterministic helpers that overfit what they have seen (ARC world-model `encode` functions, parsers). Consolidation work (ENGRAM 2611.09472, Cortex 2610.20399) moves experience into weights and stops there. The new claim is about the **return trip**: if a helper's I/O behaviour is distilled into a LoRA on the agent's own model and then the tuned model is asked to re-write the helper from scratch (no access to the old source), the decompiled program generalizes better than the original, because passing through weights replaces the helper's hard-coded case splits with the model's smoother prior. If true, an agent can improve its own library by consolidation alone, without new environment data: a complementary-learning-systems loop in which code is the hippocampus and weights the neocortex, and knowledge comes back out improved.

**Why it is not tied by construction.** The obvious tie is "ask the model to generalize the helper" with the same compute. The round trip only wins if gradient descent on the helper's I/O finds structure that reading the source does not. That is not settled by linear algebra; it could fail.

**Pilot.** 12 transformation families (string rewriting, small grid ops) each with a seen split (helper written from 10 examples, typically overfit) and a held-out split of variants. Model Qwen2.5-Coder-1.5B, LoRA rank 8 trained only on the helper's I/O on its seen inputs plus helper-generated inputs sampled from the argument type. Arms, all at matched generation and token budget:
1. original helper;
2. same model, untuned, prompted with the helper source to "rewrite and generalize";
3. same as 2 with k self-refinement rounds on the seen examples (matches the round trip's extra compute);
4. LoRA trained on the same number of **ground-truth environment** examples (upper bound for "more data");
5. round trip: LoRA trained on helper I/O only, then decompile (tuned model writes the function from I/O examples, never sees the old source);
6. round trip with a shuffled-label LoRA (filler control for the training step).

**Gate.** Original helpers must fail ≥30% of held-out variants; else no headroom.

**Kill.** Arm 5 ≤ max(arm 2, arm 3) + 3 pp held-out accuracy (3 seeds, paired bootstrap), or arm 6 within CI of arm 5.

**If it works.** Iterate the loop (code→weights→code) for several cycles and measure library size, held-out accuracy, and forgetting of old families in the LoRA; scale to ARC-AGI-3 world-model helpers.

**Compute.** ~1 GPU-h or ~8 CPU-h for the first pilot.

---

## N2 Inheritance-shaped adapters: let the agent design its own weight-sharing topology

**Bet.** In NOOA a new task is naturally a new subclass: it inherits methods, overrides some, calls `super()`. OO-Harness (2610.28380) already evolves such hierarchies for harness code. The new step is to make the class tree the **weight** topology: each class owns a LoRA residual, a subclass's effective adapter is the sum along its MRO, and the training data for a residual are the calls to that class's own `...` methods. The agent's code decisions (what to override, what to inherit) then decide what is shared and what is private in weights. The claim: an agent-authored tree, which encodes semantic knowledge of which behaviours are the same, beats data-driven trees (TreeLoRA 2506.10355, gradient similarity) on old-task retention at equal parameters, and new subclasses learn faster from fewer calls.

**Pilot.** Qwen2.5-0.5B, 8 typed method families (e.g. ticket triage variants with Literal labels whose meanings partly shift by subclass) arriving in 3 waves; an LLM writes the class tree from the method signatures and docstrings only. Arms at equal total LoRA parameters: flat single LoRA; one LoRA per task; TreeLoRA tree; random tree with the same shape as the agent's; agent tree; agent tree with permuted leaf assignments.

**Gate.** Per-task LoRA vs flat must differ in retention by more than seed spread; else the topology cannot matter.

**Kill.** Agent tree ≤ TreeLoRA or ≤ random same-shape tree on average retention and on few-shot learning of wave-3 classes (3 seeds).

**If it works.** Let the agent refactor the hierarchy mid-stream (extract a superclass) and test whether merging the corresponding residuals is lossless; that would make refactoring a weight-space operation.

**Compute.** ~6 CPU-h.

---

## N3 Reachability forgetting: garbage-collect memory instead of decaying it

**Bet.** NOOA memories can hold typed references (`kind:key`) into live agent state, and agents persist executable world-model code. That gives a reference graph: from the agent's live fields and its current library, which memories can any code path or live object reach? The proposal: forgetting by **reachability** (mark-and-sweep from live roots, through memory-to-memory associations and references), not by ACT-R activation decay (NOOA's default) or LLM self-pruning (2610.25561). The claim is that reachability keeps rarely-used but still-relevant memories (a rule about an object that still exists, unread for 500 steps) that decay drops, and drops frequently-read memories about objects that no longer exist, which decay keeps. Dependency-aware revision (2611.02912) updates dependents of a changed fact; it does not use reachability as the forgetting criterion.

**Why not tied by construction.** In a world where object lifetime and memory usefulness are uncorrelated, GC has no advantage; the pilot world makes this a measured property, not an assumption. Long-tail reuse (a rule needed again after a long gap) is exactly where decay and GC disagree.

**Pilot.** Synthetic NOOA world: 200 objects with lifetimes drawn from a heavy-tailed distribution, rules about objects and about object classes, queries whose answer depends on a rule; Qwen2.5-1.5B reads injected memories (4 per turn, as in NOOA). Arms at matched store size: no pruning (upper bound), recency, ACT-R decay, LLM self-pruning, reachability GC, reachability GC with randomly rewired references (control). Filler and temperature arms per the methods rule.

**Gate.** Disagreement between decay and GC pruning sets ≥20% of memories at the target size.

**Kill.** GC's success-vs-store-size curve within CI of ACT-R decay and of self-pruning at every size, or rewired-reference GC within CI of GC.

**Compute.** CPU, inference only, ~4 h.

---

## N4 The `...` frontier after a model upgrade

**Bet.** A NOOA agent mixes deterministic methods (often written by the model itself) with `...` methods completed by the model. When the model is upgraded, code written by the old model freezes the old model's competence: a hand-rolled parser written by a weak model is worse than what the strong model would do live. The claim: after an upgrade, reverting a selected subset of self-written methods back to `...` recovers capability that neither keeping all code nor reverting everything does; and the best frontier is predictable from per-method traces on archived calls (cheap), so an agent can re-draw its own code/weights boundary at every model change. This is the inverse of the Toolbox drift card (the API changes there; the model changes here) and of Q2 lesson obsolescence, which died because lesson effects were tiny; code effects should be large enough to pass the truth gate.

**Pilot.** 20 methods across 4 task families; an old model (Qwen2.5-0.5B local, or a small OpenRouter free model) writes deterministic bodies for each from 10 examples; new model Qwen2.5-1.5B or Nemotron. Arms: all old code; all `...` on new model; new model rewrites all code; mixed frontier chosen by per-method A/B on 50 archived calls; random frontier of the same size.

**Gate (truth).** Per-method code-vs-`...` effect split-half reliability ≥0.7 on archived calls.

**Kill.** Chosen mixed frontier ≤ max(all-code, all-`...`, rewrite-all) + 2 pp on fresh calls, or random same-size frontier within CI.

**If it works.** Learn a frontier predictor from method signatures and trace features that transfers across model pairs; this is the agent-level analogue of choosing which layers to freeze.

**Compute.** CPU plus ≤50 OpenRouter requests.

---

## Prior art checked (alphaXiv, 2026-11-24)

2607.20709 NOOA; 2610.28380 OO-Harness (evolved subclass harnesses + router); 2610.18784 CarryOn (object-oriented context); 2608.19013 Harness Continual Learning; 2611.19461 Program Distillation (LLM→program, one-way); 2611.09472 ENGRAM and 2610.20399 Cortex (experience→weights, one-way); 2506.10355 TreeLoRA; 2610.25561 self-pruning memory; 2611.02912 dependency-aware memory revision; 2611.14326 falsification-gated self-evolution; 2610.21283 / 2608.25927 code world models.
