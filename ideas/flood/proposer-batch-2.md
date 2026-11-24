# Flood batch 2 (merged-ideas proposer): 36 raw ideas, unfiltered

Same format: mechanism, why it's new, and the cheapest first test. These are deliberately wilder than batch 1.

1. **Memory as a second model that argues back.** A small "conscience" model trained only on past mistakes interjects whenever the main model's margin is small. *New:* memory is an adversarial voice, not something retrieved. *Test:* 0.5B conscience on a G1 failure log; the agent's accuracy with and without interjection.

2. **Gradient echoes.** Store the low-rank sketch of every past gradient. When a new gradient's projection onto an old sketch exceeds a threshold, replay that task's examples. *New:* replay is triggered by gradient collision, not by schedule. *Test:* M3 world; echo-triggered vs periodic replay.

3. **Weight-space immune memory.** Keep "antibody" directions: the updates that once fixed a regression. When a new update recreates the same damage pattern, apply the stored antibody. *New:* reusable repairs. *Test:* #24 with repeated shift tasks.

4. **Lessons that expire unless re-earned.** Each lesson's attention bias decays every step unless an outcome confirms it. *New:* memory as a leaky integrator of evidence. *Test:* M2 harness with decay vs a fixed bias.

5. **Counterfactual twin.** Fork the model before every update and run the twin without the update on live traffic for k steps; commit the update only if the original beats the twin. *New:* A/B testing inside the learner. *Test:* challenge world at a small scale.

6. **Context-to-weights phase transition.** Lessons move to weights when their follow index saturates, and are pulled back into context when it drops. *New:* bidirectional consolidation. *Test:* M3 world with a pull-back rule.

7. **Self-generated contradiction exams.** Before consolidating, the model writes contradicting directives for each lesson; if it can't be overridden by them, it refuses to consolidate. *New:* the model certifies its own editability. *Test:* M3 world, exam-gated consolidation.

8. **Attention-sink memory.** Store memories in the attention-sink position's key/value, so they are always visible at near-zero token cost. *New:* uses the sink as memory. *Test:* N1 harness; sink-KV memory vs prefix memory.

9. **Lessons as steering of the sampling temperature per token.** Instead of text, a lesson is a per-token temperature schedule. A3 says that is most of its effect anyway. *New:* takes the null result seriously and turns it into a mechanism. *Test:* G1 tables; learned temperature schedule vs text lesson.

10. **Swarm consolidation.** N agents each consolidate a different shard of lessons into LoRAs, and the LoRAs are merged by the agents' correctability-weighted votes. *New:* federated continual learning with editability weighting. *Test:* 4×0.5B LoRAs, merge vs single consolidation.

11. **Forgetting as compression.** Treat retention as an MDL problem: keep the lessons whose removal increases the total code length of the experience stream. *New:* a principled retirement criterion. *Test:* G1 lesson set, MDL vs LOO pruning.

12. **Mirror tasks.** For every new task, generate its "mirror", the inverse mapping, and train on both, so the network keeps capacity to un-learn it. *New:* symmetry-based plasticity preservation. *Test:* plasticity scripts with mirror augmentation.

13. **Dream-time adversarial lessons.** During sleep, the model writes the lesson most likely to mislead itself, then trains to resist it. *New:* self-inoculation. *Test:* challenge world.

14. **Margin ledger in the KV cache.** Store each past decision's margin next to its KV entry, and attend more to past entries that had a margin similar to the current one. *New:* margin-matched retrieval. *Test:* M2 harness, with a margin-similarity bias.

15. **Plasticity budget tokens.** Give the model an explicit "learning budget" input token that scales LoRA's effective rate per example; it learns when to learn. *New:* the learner controls its own write strength. *Test:* M3 world, budget token vs fixed LR.

16. **Memory with a gut feeling.** Store only a scalar "this went badly last time" per state cluster, and use it as an entropy boost. *New:* the cheapest possible memory, testing how much text lessons add. *Test:* G1, scalar memory vs lessons vs temperature.

17. **Lesson superposition.** Pack k lessons into one context by summing their embeddings at a single position, and let N1 masks decode them per layer. *New:* sub-token memory capacity. *Test:* A3, k = 1..8 superposed lessons.

18. **Evolving tokenizer for memory.** Add new tokens for recurring lesson phrases and train only their embeddings. *New:* vocabulary growth as continual learning. *Test:* G1 lessons; new tokens vs text.

19. **Weight-space git.** Every update is a commit, merges use task arithmetic, and conflicts are detected by functional-drop overlap. *New:* version control semantics for model weights, with functional conflict detection. *Test:* #24, two branch updates merged.

20. **Curiosity from overridability.** The agent explores states where its own follow index is high, i.e. where it is unsure enough to be corrected. *New:* exploration bonus from correctability. *Test:* G1 router exploration.

21. **Lessons with preconditions learned from margins.** Each lesson gets an automatically learned applicability region: the states where it flipped decisions correctly. *New:* learned guards on memory. *Test:* A3 tables.

22. **Inverse lessons.** Store what *not* to think, as negative attention biases on misleading memories. N2 showed prohibitions rebound, so these are applied in attention, not text. *New:* moves prohibition out of language. *Test:* M2 with negative biases.

23. **Population-coded memory.** The same lesson is stored in 5 paraphrases with different layer masks, and their agreement measures confidence. *New:* redundancy as an uncertainty estimate. *Test:* N1 harness.

24. **Temporal attention priors.** Learn an attention bias over memory age that the model adjusts by the task's measured drift rate. *New:* adaptive recency. *Test:* M2 harness with drift worlds.

25. **Lesson distillation into routing.** Train only the router of a small MoE on lessons, so lessons change which expert answers, not the experts themselves. *New:* routes as memory, and experts stay intact. *Test:* tiny MoE on synthetic tasks.

26. **Damage-aware learning rate.** Scale each step's LR by a live estimate of functional damage on 20 sentinel probes. *New:* closed-loop LR control from function. *Test:* #24 harness.

27. **Memory metabolism.** Each memory has an energy that is spent when it is used and refilled by outcome reward; memories at zero energy are consolidated or deleted. *New:* a unified lifecycle under one scalar. *Test:* G1 router.

28. **Cross-model lesson transfer by margin alignment.** Transfer a lesson from 0.5B to 1.5B by matching the margin shifts it induced, not its text. *New:* lessons as model-agnostic margin targets. *Test:* A3 worlds at both scales.

29. **Sleep debt.** Consolidation is triggered by the accumulated context-entropy budget the lessons consume. *New:* a homeostatic sleep trigger. *Test:* M3 world.

30. **Reversible LoRA.** Every consolidation LoRA is trained with an invertibility constraint, so it can be subtracted exactly later. *New:* exact retirement of parametric memories. *Test:* M3 world; subtract-and-measure vs retrain.

31. **Lesson attention temperature per layer.** Learn a separate attention temperature for memory tokens at each layer. This is a continuous version of N1 masks. *New:* soft layer-local visibility. *Test:* N1 harness.

32. **Fact-level forgetting forecasts as a service.** Before any fine-tune, publish a per-fact forecast of what will break, using margin + overridability + first-order bound. *New:* a pre-deployment forgetting report. *Test:* #24, forecast vs realized.

33. **Lessons as constraints in decoding.** Compile lessons into soft constraints applied in beam search only at small-margin steps. *New:* decode-time memory, gated by margin. *Test:* A3 world.

34. **Metamemory head.** Train a head to predict whether retrieving memory will help this state; it is trained on M2's per-state gains. *New:* learned retrieval gating. *Test:* M2 harness; head-gated vs always-on.

35. **Experience shuffling for order robustness.** At sleep, consolidate the same experiences in several random orders and average the LoRAs. *New:* order-averaged consolidation. *Test:* M3 world, comparator order distance.

36. **Lesson conflict as a training signal.** When two lessons conflict (B3's interference), generate a reconciling lesson and train on the resolved version. *New:* memory self-repair by synthesis. *Test:* B3 harness.
