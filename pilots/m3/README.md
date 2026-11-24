# M3: Does consolidation cause growing oscillation?

The single-pass context-reintroduction result is covered by
[When Context Returns](https://arxiv.org/abs/2606.11627v2). This pilot tests
repeated consolidation with a feedback loop, plus the reviewer's R1
correctability probe. It does not test a new intervention.

## Protocol

- **Ten lessons.** Review versus release in ten synthetic queues, with a
  queue-specific threshold on a 0–99 review score. On uniform scores the
  intended review rates are 85%, 75%, 65%, 60%, 55%, 45%, 40%, 35%, 25%, and
  15%. The ordinary prompt states a default threshold of 50. A privileged
  prompt appends the active queue override.
- **Three consolidations per arm.** At each cycle copy the current model's
  privileged distribution on 40 queue/score examples with rank-16 LoRA on
  Qwen2.5-0.5B-Instruct (Q and V projections, final 12 blocks). Fit two AdamW
  passes at 0.001 with a fresh optimizer and carried-over weights, using the
  context-free student's reverse KL to the frozen contextual teacher. Both
  actions are single tokens; normalize over `Yes` and `No` and compute the
  complete binary KL rather than drawing action rollouts.
- **Arms.** Keep the notes versus keep plus No-Context Anchoring (NCA). NCA
  adds the paper's equation 7, `0.5 × KL(stopgrad(p(no note)) || p(note))`,
  on the same student prompts and steps. Both arms start from the same
  checkpoint, initialization and training examples for each of five seeds.
  Evict branches from keep after cycle 1: delete all ten notes, freeze the
  cycle-1 adapter (there are no remaining lessons to consolidate), and deploy
  it without context. This checks retained calibration without further
  writes, not robustness to interference from new lessons.
- **Feedback.** Start with the nominal threshold. For each arm and lesson,
  use separate feedback probes after every nonfinal cycle to replace the
  context note with threshold
  `clip(nominal + round(100 × (observed review rate − target)), 0, 100)`.
  This is target-centered proportional feedback with unit gain, not a
  learned lesson writer. Training scores, feedback scores and report scores
  have disjoint residues modulo 3; reports also use a different prompt
  template from training. Estimate the review rate by averaging the
  restricted probability of “Yes” within each side of the nominal cutoff
  and weighting the two sides by their uniform-score masses. A perfect
  nominal policy has zero aggregate calibration error on the probes.
- **M3 endpoint.** Score adapted models with the active note (“both”) and
  without it (“weights”), plus frozen base with the nominal note
  (“context”) and without it. Positive signed error means going past the
  nominal target in the intended direction. A growing oscillation requires
  two successive target crossings, absolute error greater than 3 percentage
  points (pp) at every cycle, and at least 1 pp of amplitude growth each
  time. Kill if there is no growing oscillation across cycles or if NCA
  removes it. An increase in MAE without sign changes does not pass.
- **R1 endpoint.** Replace the active note at inference only with the
  opposite cutoff (`100 − nominal`). On three fixed disagreement probes
  per lesson, a flip occurs when the weights-only argmax picks the original
  action and the contradicted argmax picks its opposite. Report the raw
  rate among eligible probes and the weights-only gain in original-action
  probability versus base (“absorption”). For change from cycle 1, match
  eligible probes within the same seed/queue/score and require absorption to
  differ by no more than 10 pp. Kill unless the upper endpoint of the
  matched final-minus-first 95% CI is at most −15 pp. If the decline is
  distinguishable from zero, examine whether 0.00025 LR and NCA preserve
  flips; NCA is already included in the main run.
- **Uncertainty.** Paired 95% percentile bootstrap over whole seeds
  (10,000 replicates), holding the lesson panel fixed. Also report the
  seed × lesson crossed bootstrap for oscillation incidence. This small
  synthetic panel does not establish generalization across models or lesson
  families.

## Reproduce

From the repository root, using Python 3.10+ on CPU:

```sh
python -m pip install 'torch==2.7.1+cpu' 'transformers==4.53.3' 'peft==0.16.0' \
  --extra-index-url https://download.pytorch.org/whl/cpu
python -m unittest discover -s pilots/m3 -v
python pilots/m3/run.py --output m3-traces.jsonl
python pilots/m3/run.py --low-lr --output m3-low-lr.jsonl
python pilots/m3/summarize.py m3-traces.jsonl m3-low-lr.jsonl
```

The runner pins the model revision; `--model-dir` can point to a local copy
of that revision. The output file must not already exist.
