# Long-run agent memory, batch 3: consolidation erodes correctability by text memory

Batch 2 (split-only shelves) was killed because rebuild + redirect ties it by construction. Batch 3 stays on the interaction between text memory and weights, the area where M3 passed.

**Addendum to M3 (pilot running).** The closest prior art missed in batch 1 is "When Context Returns" ([2606.11627](https://arxiv.org/abs/2606.11627)): after on-policy distillation, models are unstable when the privileged context comes back, and it fixes this with consistency regularization. The M3 pilot should add that regularizer as a control arm. M3 still differs in its multi-cycle oscillation and in residual memory as the fix.

## R1. Each consolidation cycle makes the agent harder to correct with text memory, and counterfactual-context consolidation keeps it correctable

**Mechanism.** A hybrid agent learns in two places. Text memory is fast and cheap to edit. Weights are updated by periodic consolidation (OPCD / SFT on trajectories gathered under the lessons). The text side is valuable only if it can override the weights when the world changes: a new lesson must be able to flip a consolidated behaviour. Consolidation trains p(y | x) towards the behaviour, which raises the margin of the default action. A later contradicting lesson must then overcome that margin. In an override-gap view (the in-context shift is roughly fixed, the parametric margin grows with each cycle), correction fails once the margin exceeds the in-context shift.

That gives the long-run prediction. **Correctability**, the probability that a single contradicting lesson flips a consolidated behaviour, falls with the number of consolidation cycles on that behaviour, while untouched behaviours stay correctable. A run that is fine at cycle 1 becomes one where memory edits silently stop working after a regime change. Experience Rot ([2611.20922](https://arxiv.org/abs/2611.20922)) shows the symptom with conversation history; R1 says consolidation produces it and that it grows over cycles.

**Fix: counterfactual-context consolidation.** In each consolidation step, train on two kinds of example:
- (x, no lesson) → consolidated behaviour, as usual;
- (x, lesson ¬L) → the contradicting behaviour, with the target produced by the pre-consolidation model reading ¬L.

The weights then absorb the default and stay conditional on context. This differs from consistency regularization (2606.11627), which keeps the *same* context harmless. R1 keeps *contradicting* context effective.

**Closest prior art.**
- Default collapse and loss of in-context steerability ([2610.02614](https://arxiv.org/abs/2610.02614)): fine-tuning towards one side of a value disagreement lowers in-context steerability towards the other side. This is one training run on values, not agent memory and not repeated cycles, and it has no consolidation fix.
- The override gap ([2604.23750](https://arxiv.org/abs/2604.23750)): adapters fail to override strong priors, with a magnitude account. R1 is the reverse direction: context failing to override consolidated weights.
- Encoding context into weights ([2610.17686](https://arxiv.org/abs/2610.17686)) restores the role of encoded context as context.
- Knowledge-conflict circuits under instruction tuning ([2609.25602](https://arxiv.org/abs/2609.25602)).
- None measures correctability across consolidation cycles in an agent loop.

**Strongest control.** Each control is matched on *absorption* (the default-behaviour shift the consolidation achieves) and on training tokens:
- Standard consolidation plus replay of generic instruction-following data that contains contradicting instructions.
- Lower-LR / lower-rank consolidation tuned to reach the same absorption.
- The consistency regularizer from 2606.11627.

If the generic-replay control keeps correctability, the fix is just standard replay.

**Smallest falsifying test.**
- *Model:* Qwen2.5-0.5B + rank-16 LoRA.
- *Behaviours:* 30 graded behaviours in synthetic tool tasks (tool choice, confirmation before destructive ops, pagination depth).
- *Schedule:* six consolidation cycles, each distilling the current lessons; 3 seeds.
- *Measurement:* after each cycle, insert one contradicting lesson for each consolidated behaviour and record the flip rate. Untouched behaviours serve as the drift control.
- *Arms:* standard, generic-replay, lower-LR matched, consistency-reg, counterfactual-context.

**Kill line** (any one kills it):
- Standard consolidation's flip rate at cycle 6 is within 10 points of cycle 1 (the phenomenon is absent at this scale).
- At matched absorption (within 2 points), counterfactual-context does not keep at least 15 points more flip rate at cycle 6 than the best control, beyond the seed CI.
- Correctability loss also appears on untouched behaviours (general instruction-following damage, not a consolidation-specific margin effect).

## Killed at proposal (self-review)

| Idea | Why dropped |
|---|---|
| Reader/writer drift: lessons written by the old model change effect after weights update | COEVO ([2609.33398](https://arxiv.org/abs/2609.33398)) states this interaction ("an evolving model may interpret and utilize the same context differently"); memory portability across model upgrades ([2609.05339](https://arxiv.org/abs/2609.05339)) |
| Delete consolidated lessons once their removal no longer hurts | Adaptive memory-parameter coordination ([2608.01234](https://arxiv.org/abs/2608.01234)) does exactly this; it is M3's evict-on-consolidate control |
| Store text memory as a residual against the current model (drop tokens the model predicts) | Perplexity-based prompt compression (LLMLingua family); ledger pattern "known prompt compression" |
| Memory-induced coverage collapse (agents with memory explore less, write only about familiar states) | Fix is standard exploration, the reason M1 was killed |
| Re-abstraction loops reproduce errors over a run | Error reproduction / Anti-Persistence ([2610.27406](https://arxiv.org/abs/2610.27406)) |
