# Flood: NOOA-style agents (object-oriented agents), raw ideas

Source: NOOA (arXiv 2607.20709): agent = Python object; fields = durable model-visible state; `...` methods completed by an LLM loop; docstrings = prompts; return annotations = validated contracts; live objects passed by reference; optional ACT-R memory with typed references to live state. Unfiltered on purpose; the reviewer ranks. Each: mechanism, why new, cheapest first test. Deeper cards N1–N4 are in `ideas/nooa/batch-1.md`.

1. **Round-trip consolidation (code → weights → code).** Distil an agent-written helper's I/O into a LoRA, then have the tuned model rewrite the helper without seeing the old source. New: consolidation papers (ENGRAM, Cortex) go one way; the claim here is that the return trip *improves* the program. Test: 12 string/grid families, overfit helpers, compare against equal-compute "rewrite and generalize this helper".

2. **Inheritance-shaped adapters.** Each class owns a LoRA residual; a subclass's adapter is the sum along its MRO; the agent's own subclass tree is the weight-sharing topology. New: OO-Harness evolves class trees for code only; TreeLoRA builds trees from gradients, not semantics. Test: 0.5B, 8 typed method families in 3 waves vs TreeLoRA and a random tree of the same shape.

3. **Reachability forgetting.** Prune memories unreachable from live fields and the current library (mark-and-sweep through `kind:key` references) instead of ACT-R decay. New: no memory system uses reachability as the forgetting criterion. Test: synthetic world with heavy-tailed object lifetimes; success vs store size against decay and self-pruning.

4. **`...` frontier after a model upgrade.** Code written by the old model caps the new one; revert a chosen subset of methods to `...`. New: inverse of tools-under-API-drift; here the model drifts. Test: 0.5B writes 20 helpers, 1.5B runs; mixed frontier vs all-code / all-`...` / rewrite-all.

5. **Refactoring as weight surgery.** When the agent extracts a superclass from two classes, merge their LoRA residuals into a parent residual plus two small children (SVD of the shared part). New: makes code refactors and adapter merges one operation, with code structure deciding what merges. Test: does post-refactor merged model retain both tasks better than TIES/DARE merge at equal params.

6. **Type-signature hashing as task identity for weight CL.** Route continual LoRA updates by a canonical hash of each `...` method's signature + return schema; no task IDs, no learned router. New: typed contracts give free, exact task boundaries that ordinary CL lacks. Test: 6 methods, sequential LoRA; signature-routed vs learned router vs single adapter.

7. **Contract-directed generative replay.** Before a weight update, sample inputs from each old method's argument types (Pydantic), have the current model answer, keep only outputs that validate, replay them. New: self-synthesized rehearsal without a seed buffer, where the type system supplies the input distribution and the filter. Test: forgetting of 4 old methods vs SSR and vs random-prompt replay.

8. **Validator rejections as continual RL reward.** Every return-validation failure in deployment is a free negative reward; corrected retries are free positives. Continual RL on weights from validator traffic alone. New: deployment-time learning from contract signals without any task reward. Test: 0.5B, 3 typed tasks, GRPO on validator-only reward; does task accuracy rise or does it reward-hack to minimal valid outputs.

9. **Contract tightening as curriculum.** The agent progressively tightens its own return types (Field ranges, Literals, invariants) as it learns; tighter types reshape the action space for later learning. New: curriculum by the agent narrowing its own output space. Test: compare learning curves with fixed loose types vs self-tightened vs oracle-tight.

10. **Docstring–behaviour drift as a forgetting alarm.** After self-edits, regenerate each method's docstring from traces and diff it against the stored docstring; divergence predicts harness-level forgetting. New: uses the agent's self-description as a self-model whose fidelity is measurable. Test: correlate docstring diff with measured regression across 50 self-edits (variance gate first).

11. **Self-model compression via `doc()`.** The agent's `doc()` (signatures + visible state) is its context-visible self-model. Learn to compress it (which methods to expose) per task stream; exposure becomes a learned memory. New: continual learning over the agent's own API surface, not its memories. Test: exposure policy learned on wave 1 vs full exposure on wave 2 at equal tokens.

12. **Escape analysis as a write gate.** REPL locals die at method return; only values written to `self` persist. Train (or prompt) the model to decide escape, and measure which escapes predicted later reuse. New: a write gate defined by the language's own scoping rather than a separate memory tool. Test: log escapes in ARC-like runs; does an escape-prediction rule beat "store everything" at matched size.

13. **Live-reference memory vs snapshot memory under drift.** Memories that dereference live state at recall never go stale on values but can go stale on meaning (the object changed type). Measure "semantic staleness" that references cannot fix. New: isolates the failure mode left once value staleness is solved by construction. Test: world where object types mutate; reference memories vs snapshot vs both.

14. **Class-level vs instance-level memory.** Store a lesson on the class (shared by all instances) or the instance; let the agent decide and learn the policy from transfer outcomes. New: an OO scoping axis for lesson generality that no memory system names. Test: fleet of instances on related tasks; class-scoped vs instance-scoped vs learned.

15. **Method resolution order as retrieval order.** When a subclass and parent both hold memories, retrieval walks the MRO: specific before general, with `super()` to escalate. New: retrieval precedence derived from program structure, not embeddings. Test: tasks with exceptions-to-rules; MRO retrieval vs embedding top-k.

16. **Multiple inheritance as skill composition with conflict detection.** A new class inheriting from two skill classes surfaces method conflicts (diamond problem) explicitly; resolve them with the model and keep the resolution as memory. New: interference between skills becomes a compile-time event. Test: count conflicts and post-composition accuracy vs composing text skills.

17. **Executable world-model inheritance across games.** ARC-AGI-3 agents persist world-model classes; new games subclass the closest old world model instead of starting fresh. New: transfer of executable dynamics via inheritance, measured in actions-to-first-level. Test: 10 grid games; subclass-from-nearest vs from-scratch vs text notes.

18. **Popperian memory.** Every memory is stored as a predicate that predicts an observation; it is continuously checked against live observations and retired only when falsified, with the falsifying observation stored. New: retirement is localized to the belief that broke, not global decay. Test: nonstationary grid world; drift localization time vs falsification-gated self-evolution (2611.14326).

19. **Counterexample objects.** When a method's output is wrong, the agent stores the input object itself (by reference) as a counterexample attached to the method; future calls see nearest counterexamples. New: memories are concrete live inputs, not text. Test: vs text error notes at matched tokens, with filler and temperature arms.

20. **Trace-coverage EWC for code.** Weight each line of the agent's source by how many successful traced calls executed it; penalize self-edits to high-coverage lines in proposal scoring. New: Fisher-style importance in program space. Test: 100 self-edits; regressions vs unconstrained editing and vs a regression-test gate.

21. **Program-space plasticity loss.** Track how many methods are still edited over a long self-evolution run; test whether agent libraries lose plasticity (ossify) like networks do, and whether "re-ellipsising" (resetting bodies to `...`) restores it like resets do. New: plasticity loss studied in the code substrate. Test: 1,000 self-edit steps on a drifting task; edit acceptance rate over time with and without periodic resets.

22. **Dormant-method resets.** Analogue of ReDo for code: methods never called for N tasks are reset to `...` so the model reimplements them fresh when next needed. New: dormant-neuron recycling applied to agent methods. Test: library size and success under drift vs never-reset and random reset.

23. **Garbage-collection pauses as sleep.** Run consolidation exactly when the memory heap crosses a size threshold (like GC), not after each task; measure whether event-triggered consolidation beats fixed schedules. New: consolidation timing driven by memory pressure. Test: three schedules at equal consolidation calls.

24. **Weak references for doubtful memories.** Memories the agent is unsure of are held via weak references: they survive only while some strong memory or live object points to them. New: confidence expressed as reference strength, so doubtful memories die automatically with their context. Test: world with corrupted observations; weakref vs confidence-threshold pruning.

25. **Copy-on-write agents for safe self-modification.** Fork the agent object copy-on-write when it proposes a self-edit; both run on the next tasks until one diverges, then the loser is collected. New: self-evolution as process forking with shared state pages. Test: success and compute vs a validation gate on held-out tasks (HK1 control).

26. **Agent pickling as a checkpoint for continual learning.** Serialize the whole agent (state + code + memory) at each task boundary; learn which pickle to restore under drift. New: snapshots of agent objects as a model pool. Test: recurring-regime stream; restore-best-pickle vs keep-evolving vs time-travel baseline (note: ledger killed time-travel memory; this must beat it).

27. **Types as compressed lessons.** Instead of writing a text lesson, the agent edits a type (adds a Literal, a validator). A typed constraint is enforced, not read, so it cannot be ignored or mistaken for temperature. New: lesson effect via the action space rather than the context, sidestepping the A3 lessons-as-temperature finding. Test: same 20 lessons as text vs as type edits; temperature-matched arm.

28. **Signature evolution as representation learning.** Let the agent add/remove fields of its argument and return types across tasks; measure whether evolved schemas transfer to new tasks (a learned ontology). New: representation learning in the type system. Test: schema learned on 5 tasks reused on 3 held-out vs hand-written schema vs no schema.

29. **Pass-by-reference as attention over the heap.** Train the model (LoRA) to choose which live objects to dereference into context per step; the "what to look at" policy is learned continually. New: continual learning of a dereference policy rather than retrieval. Test: tasks with large live state; learned dereference vs full render vs embedding retrieval at equal tokens.

30. **Asyncio scheduling as continual credit assignment.** Concurrent sub-agent calls produce partial results at different times; credit each sub-agent's memory writes by its effect on the awaited result. New: credit assignment from the program's own control flow. Test: multi-worker tasks; per-worker credit vs equal credit for memory curation.

31. **Exception handlers as learned recovery.** The agent writes `try/except` handlers around failing calls; handlers accumulate as recovery memory with type-specific dispatch. New: failure recovery stored in exception types, matched by the language. Test: drift stream with new failure types; handler library vs text recovery notes.

32. **Tracing graphs as replay buffers.** NOOA traces follow the nested call tree; replay sub-trees (a single method call with its inputs) instead of whole episodes for weight CL. New: replay granularity set by program structure. Test: forgetting under method-level vs episode-level replay at equal tokens.

33. **Mutation testing of memories.** Mutate a memory (flip a value, delete a field) and measure behaviour change on archived calls; memories whose mutation changes nothing are dead weight. New: memory utility from mutation testing, not leave-one-out on outcomes. Test: correlation of mutation sensitivity with LOO utility; cost at equal calls.

34. **Liskov memory for subclass specialists.** A subclass's memories must not break parent behaviour on parent-typed calls (behavioural subtyping); check by running parent-call archive through the subclass. New: an interference test indexed by type hierarchy. Test: rate of parent regressions with vs without the check.

35. **Agents as dataclasses: diffable learning.** Since all state is typed fields, continual learning is a sequence of typed diffs; learn a model of which diff types help (field adds, list appends, method edits). New: a grammar of agent state changes as the unit of analysis. Test: predict next-task success from diff type counts (variance gate).

36. **Ellipsis density as an exploration knob.** Fraction of `...` methods sets how much the agent improvises vs follows code; anneal it like temperature over a task stream. New: exploration control in program structure rather than sampling. Test: same stream with fixed vs annealed ellipsis density; compare with temperature annealing.

37. **Self-written unit tests as memory.** Instead of lessons, the agent stores tests for its own methods; tests constrain future edits and also act as few-shot examples. New: tests as a dual-use memory (spec + demonstration). Test: tests-as-context vs lessons vs examples at matched tokens.

38. **Cross-agent method import (`from other_agent import method`).** Agents in a fleet import each other's methods by signature; imported methods carry the source agent's memory references. New: transfer by import with typed compatibility checks. Test: fleet of 4; import vs shared text memory vs no sharing.

39. **Monkey-patching the harness at test time.** The agent patches its own context builder for one task and auto-reverts; patches that help are promoted. New: reversible harness changes scoped by Python context managers. Test: patch-and-revert vs permanent edits under drift.

40. **Model-written metaclasses.** Let the agent write metaclasses that transform how its future methods are compiled (e.g., auto-add retries, caching). New: the agent learns at the level of how methods are built, a second-order harness. Test: does a metaclass learned on family A help family B vs direct method edits.
