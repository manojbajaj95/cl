# Anomaly batch 1: what the killed pilots actually measured

Bottom-up pass over raw per-seed / per-unit data of PRs #12/#19 (rare event), #13 (effect-class),
#14 (G1), #25 (fleet Q2), with cross-checks against #17, #22, #23, #24. Every number below was
recomputed here from the pilots' checked-in data or a rerun of their unchanged code at more seeds;
scripts and outputs are in this directory. Ranked by how much each should change what the loop
does next.

| # | Anomaly | Above seed noise? | Novelty vs 2026 prior art | Recommendation |
|---|---|---|---|---|
| A3 | Memory lessons in G1/Q2 act as a temperature knob; "lesson effect" is sharpening x start | Exact (no sampling); 2 independent policy sets | Medium: "sharpening" known for RL, not shown for in-context lessons as the whole effect | Pilot (CPU, minutes) |
| A1 | Natural-frequency replay makes rare-old retention *worse* than no replay; the rare-event world has a built-in label conflict | 20 seeds, CIs ~0.3 pp wide | Low: replay-increases-forgetting is proven (2506.04377) | Ledger note; retire this world |
| A2 | Effect-class replay at weight 4 bifurcates: adoption collapses on 5/10 seeds, not on the others | 10 seeds, bimodal | Low | Cheap 30-seed check only if reviewer wants it |

---

## A3. A memory lesson is (almost) a temperature change; its value is a property of the start, not the lesson

**Data.** G1 (PR #14, `offline.npz["policy"]`, 30 lessons) and Q2 (PR #25, `truth.npz["new"]`, 40
lessons, different model) store the constrained policy table for every lesson, so per-start success
can be computed exactly by enumerating all 27 action paths
([task_by_lesson.py](a3/task_by_lesson.py), [temperature_control.py](a3/temperature_control.py)).
Lesson effect = success(lesson, start) - success(no lesson, start), 12 starts.

| | G1 | Q2 |
|---|---:|---:|
| Share of effect variance: lesson main effect | **1.2%** | **0.8%** |
| Share: start main effect | 72.1% | 86.1% |
| Share: lesson x start interaction | 26.7% | 13.1% |
| Rank-1 share of the interaction | 92.6% | 81.3% |
| Rank-1 lesson loading vs lesson's entropy change, r | **0.997** | **0.992** |
| Rank-1 start loading vs no-lesson success at that start, r | -0.973 | -0.965 |
| Best single temperature on the no-lesson policy reproduces per-start lesson effects, R^2 | **0.953** | **0.951** |
| ... interaction part only, R^2 | 0.908 | 0.776 |
| Fitted temperature, median [min, max] | 0.745 [0.58, 1.50] | 0.735 [0.57, 1.04] |
| Lessons whose effect changes sign across starts | 30/30 | 40/40 |

Mean effect by start (pp), G1: starts 0/3/6/9 (no-lesson success ~0.72) **+11.6 to +15.5**; the other
eight starts (success 0.05-0.18) **-1.3 to -9.6**. Q2 is the same pattern (+14.0 to +18.4 vs -1.5 to
-10.6). Every lesson sharpens the base policy; sharpening helps where the base mode is right and hurts
where it is wrong.

**Why Q2/G1 truth was "unreliable".** Split-half reliability of lesson ranking over all 462 6-vs-6
start splits depends on how many high-success starts each half gets
([balance_check.txt](a3/results/balance_check.txt)):

| \|high-start imbalance\| between halves | G1 mean r [min, max] | Q2 mean r [min, max] |
|---:|---:|---:|
| 0 | 0.75 [0.36, 0.93] | 0.51 [0.12, 0.85] |
| 2 | -0.46 [-0.59, -0.27] | -0.32 [-0.57, 0.14] |
| 4 | -0.82 [-0.84, -0.80] | -0.75 [-0.79, -0.69] |

So the reliability gate was not measuring noise: it measured the start mix. G1's rollout truth
(50 rollouts/lesson) adds sampling noise on top: across-lesson variance of fresh success is 0.0015 vs
binomial noise 0.0046, split-half -0.06 (recomputed from `fresh.npz`). The first-order
(performance-difference) expansion, base visitation x per-cell policy change x base Q, explains
98.7% / 99.1% of per-start effects, so the per-(step, code) policy change is the stable object; the
scalar "lesson effect" is not.

**Not explained by the pilots' hypotheses.** Q2 asked whether new-model likelihood gain predicts which
lesson still helps; G1 asked whether off-policy estimators rank lessons. Both assume a lesson has a
value. Here the lesson identity carries ~1% of the effect variance, and >90% of what is left is one
scalar per lesson (how much it sharpens).

**Mechanism hypothesis (H-A3).** A short in-context lesson mostly rescales the logits of a small
model's existing preferences (an inverse-temperature shift) rather than changing which action it
prefers. Value then factorizes as `effect(l, s) ~ beta(l) * h(s)` with `h(s)` the sign/size of the
base mode's correctness on the states reachable from `s`. Content-specific help exists only in the
small residual.

**Closest prior art (alphaXiv).**
- [2611.03930](https://arxiv.org/abs/2611.03930) Task-conditioned memory utility: memory value depends
  on the memory-task pair and individual labels are unstable. It attributes this to answer-bearing
  content; it has no temperature or confidence-matched control.
- [2610.33029](https://arxiv.org/abs/2610.33029) Lessons from Luck: lessons carry chance outcomes into
  the next decision. About lesson content, not a confidence channel.
- [2610.01509](https://arxiv.org/abs/2610.01509) Sharpening Tax, [2611.03146](https://arxiv.org/abs/2611.03146)
  Controlling Sharpening, [2611.01059](https://arxiv.org/abs/2611.01059) Temperature, Not Knowledge:
  the sharpening view is established for RL post-training and self-training, measured on weights.
  I found no paper that decomposes in-context memory/lesson effects against a temperature-matched
  no-memory control.
- Gap: "memory helps" claims in agent CL would need to beat a temperature-matched no-memory arm.

**Strongest control.** Temperature-matched no-lesson policy: for each lesson, pick T so that the
no-lesson policy's mean entropy (fit on source starts only) equals the lesson policy's; no access to
held-out outcomes. Content claims must beat this arm, not "no lesson".

**Smallest falsifying test (CPU, both models from PR #25, about 1 h).** Same router, but rotate the
rule so the no-lesson mode is wrong at codes with remainder 0 and right elsewhere (a rule change after
"upgrade"). Write 40 lessons as in Q2 (20 failure-distilled, 20 stratified), of which half state the
changed rule. Fit T on 6 source starts by entropy matching, evaluate the other 6 exactly.
- Prediction if H-A3 holds: temperature control R^2 >= 0.80 on held-out per-start effects for the
  non-rule lessons, and even rule-stating lessons lose most of their effect on held-out starts.
- **Kill line:** kill H-A3 if the temperature control's held-out R^2 on per-start lesson effects is
  below 0.50 for the pooled 40 lessons, or if rule-stating lessons beat their temperature-matched
  controls by >= 5 pp held-out success with a lesson-bootstrap 95% CI above 0. Also kill if the
  lesson main effect share exceeds 25% of effect variance.
- Gate before reading the result: report split-half reliability only on halves balanced in
  high/low-success starts; otherwise the gate measures the start mix (table above).

**If it survives**, the claim is that the in-context memory literature's "lesson value" is mostly a
confidence effect, with a cheap test (temperature-matched arm) every memory paper can run. That is a
methods result, the kind that gets an ICLR paper if it holds on a real agent benchmark.

---

## A1. In the rare-event world, replay makes rare forgetting worse, and coverage could never help

**Data.** Unchanged PR #19 pilot (vendored as [a1/pilot_pr19.py](a1/pilot_pr19.py)) with replay split
by old status and the new-task loss masked by status, 20 paired seeds (421-440)
([a1/squeeze.py](a1/squeeze.py), [results](a1/results/squeeze.json)). Old-rare = X-jam recovery.

| Arm (same replay budget) | old rare % | old common % | new common % | new jam % |
|---|---:|---:|---:|---:|
| no replay | 9.24 [8.90, 9.59] | 92.40 | 96.78 | 92.68 |
| MOPD, natural frequency (pilot arm) | 3.41 [2.74, 4.08] | 96.20 | 95.03 | 91.14 |
| MOPD, X-normal states only | 7.14 [6.84, 7.45] | 94.78 | 96.98 | 91.81 |
| MOPD, X-busy states only | 0.29 [0.28, 0.31] | 99.57 | 90.19 | 88.45 |
| no replay, Y-busy new loss masked | 0.06 [0.05, 0.06] | 100.0 | 48.78 | 99.92 |
| MOPD, half X-busy half X-jam | 55.31 [50.31, 60.31] | 98.21 | 86.04 | **19.77** |

Paired vs no replay: natural MOPD -5.83 pp old rare [-6.37, -5.30]; X-busy replay -8.95 [-9.29, -8.61].
These intervals are ~20x narrower than the effects.

**What it shows.** Labels are `X: 1 iff jam`, `Y: 1 iff busy` on one shared adapter. Centered feature
cosines: X-jam vs Y-jam **+0.86**, X-busy vs Y-busy +0.71, X-jam vs Y-busy -0.66. So the old rare state
and the new rare state share a direction with opposite labels. Replaying X-busy (label 0) pushes the
same way as Y-jam training. The 9% that "no replay" keeps comes only from Y-busy training (masking it
drops old rare to 0.06%). Anchoring the jam directly recovers 55% but costs 73 pp of new jam. This
is a single-readout Pareto conflict built into the world. More rare coverage (the PR #12 and PR #19
hypothesis) could only move along that front. That is why splitting never won and why seed variance
dominated arm variance in the PR #19 Q1 rerun.

**Mechanism hypothesis.** Retrieval-induced forgetting in parameter space: replay of the frequent
sibling of a rare state, with the opposite label and shared features, actively unlearns the rare
state when the new task already pulls that way.

**Closest prior art.** [2506.04377](https://arxiv.org/abs/2506.04377) *Replay Can Provably Increase
Forgetting*: in linear models, replaying some samples of a task increases forgetting of its unreplayed
samples. The authors name the retrieval-induced-forgetting analogy. Also
[2610.08718](https://arxiv.org/abs/2610.08718) (spurious forgetting) for the readout-level view.

**Strongest control.** Same replay budget spent on X-normal (orthogonal-ish features, -2.1 pp) vs
X-busy (aligned features, -8.95 pp): the feature-alignment ordering is the test.

**Smallest falsifying test (already run).** If the harm were a budget/coverage effect, X-busy-only and
X-normal-only replay would tie. **Kill line:** |X-busy - X-normal| < 2 pp. Observed 6.85 pp. It
survives, but it is prior art.

**Recommendation.** Not a paper. Ledger note: retire the PR #12 world for rare-retention questions.
Any successor world must have rare-old and new behaviors that are jointly satisfiable at matched
capacity (check: an oracle multi-task fit reaches >= 90% on both). Otherwise coverage methods are
tested on an infeasible front.

---

## A2. Effect-class replay at high weight bifurcates by seed

**Data.** PR #13 code unchanged except 10 seeds instead of 3 ([patch](a2/ten_seed.patch),
[results](a2/results/effect_class_10seeds.json)). Old-prompt new-API adoption:

| Arm | mean | sd | min | seeds with adoption < 0.95 |
|---|---:|---:|---:|---:|
| effect:4 | 0.906 | 0.131 | 0.592 | **5/10** (0.82, 0.87, 0.93, 0.59, 0.86) |
| reward:4 | 0.987 | 0.040 | 0.874 | 1/10 |
| effect:1, reward:1 | 1.000 | 0.000 | 1.000 | 0/10 |
| token:0.25 / 1 / 4 | 0.668 / 0.534 / 0.425 | 0.02-0.05 | | 10/10 (monotone in weight) |

The PR #13 verdict replicates at 10 seeds: effect - reward hypervolume -0.0028 [-0.0044, -0.0012],
now significant. Effect - token +0.0090 [+0.0065, +0.0114].

**Not explained.** Token-KL degrades smoothly with weight. Effect-class at weight 4 is either
untouched (5 seeds at 0.97-1.00) or collapses (0.59-0.93). That is a bifurcation, not a smooth
trade-off.

**Mechanism hypothesis.** The effect weight `teacher_count / student_count` (at most 4 with 4 samples)
times replay weight 4 gives up to 16x reinforcement of student samples whose execution signature
matches the *pre-migration* teacher. Once a seed's student emits one old-API call with the teacher's
signature, the large weight self-reinforces it (rich-get-richer).

**Closest prior art.** Importance-weight variance in off-policy distillation; OPD forgetting analyses
([2610.25651](https://arxiv.org/abs/2610.25651), [2607.01763](https://arxiv.org/abs/2607.01763)).
Nothing specific to effect classes, but also little novelty.

**Strongest control / smallest falsifying test.** 30 seeds of effect:4 with the ratio clipped at 1
(same expected weight scale via renormalization). **Kill line:** if clipped effect:4 still collapses
on >= 20% of seeds, the ratio is not the cause; if unclipped collapse rate across 30 seeds is < 20%,
the bifurcation was small-sample noise. CPU cost ~3 min. Low priority: even if it survives, it
explains a failure of an already-killed method.

---

## Checked and rejected (did not exceed noise or already explained)

- **Edit-capacity batch-size reversal (PR #22).** Batch-8 minus batch-32 collapse point by stream:
  +96, 0, +224, +64, -96, -96 edits. The mean is +32 and the sign is inconsistent across six streams,
  one run each. This is noise at this n.
- **Polya-urn early saturation (PR #17).** Utility-eviction gain saturates by step 200 (0.351 to
  0.343 at 1000). This is real but already the reason the comparator gate killed the predictor
  (rho = 1.000).
- **PR #23 exposure moves P(yes) +19.75 pp but greedy endorsements are 5/320; PR #24 functional damage
  98.8% concentrated while raw weight damage is not (r = -0.07).** Both are "continuous signal moves
  without crossing the argmax margin". The ledger already records this pattern (control margin);
  covered by [2608.20794](https://arxiv.org/abs/2608.20794) for factual recall. No new mechanism.
- **Cross-pilot "candidate spread is real but the score does not rank it" (PRs #9, #11, #19, #21,
  #22).** In each case the stated reason holds (comparator or constant baseline). A3 is the one place
  where the reason was structural rather than noise.

## Reproduce

```sh
python -m venv ~/venv && . ~/venv/bin/activate
pip install torch==2.7.1 --index-url https://download.pytorch.org/whl/cpu
pip install transformers==4.52.4 numpy==2.2.6 scipy==1.15.3
# A3 (seconds)
git show pr14:pilots/g1-offline-ab/offline.npz > /path/g1.npz
git show pr25:pilots/q2-upgrade-lessons/truth.npz > /path/q2.npz
python anomalies/a3/task_by_lesson.py --g1 /path/g1.npz --q2 /path/q2.npz --output anomalies/a3/results/task_by_lesson.json
python anomalies/a3/temperature_control.py /path/g1.npz /path/q2.npz anomalies/a3/results/temperature_control.json
# A1 (~25 s features + ~10 min)
cd anomalies/a1 && python pilot_pr19.py --threads 8 --cache /path/features.pt --features-only
python squeeze.py --cache /path/features.pt --seeds 20 --output results/squeeze.json
# A2: apply a2/ten_seed.patch to PR #13's pilots/effect_class_distill/pilot.py and run as in its REPORT
```
