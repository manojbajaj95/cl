# Self-QA replay does not clear the matched-question gate

**Decision: stop escalation.** Three held-out runs showed no retention
advantage over same-question teacher answers or verified generated prose at
equal replay tokens. This is a negative stop/go result, not an equivalence
claim or a test of natural-language, larger-scale or adaptive replay.

## Held-out results

Final accuracy (%) on unseen question forms for old facts. New accuracy
is for the most recent batch, also evaluated using unseen forms.

| Replay | Old 501 | Old 502 | Old 503 | Mean old | Mean new |
| --- | ---: | ---: | ---: | ---: | ---: |
| None | 73.26 | 55.21 | 42.36 | 56.94 | 88.66 |
| Self-QA | 85.76 | 81.94 | 76.39 | 81.37 | 81.13 |
| Same-question teacher | 85.07 | 85.07 | 78.12 | 82.75 | 76.62 |
| Style-matched teacher | 84.72 | 81.25 | 79.17 | 81.71 | 75.58 |
| Verified generated prose | 87.85 | 82.64 | 76.39 | 82.29 | 92.82 |
| Unfiltered generated prose | 84.38 | 80.90 | 78.12 | 81.13 | 92.59 |

Paired differences in percentage points (self-QA minus control).
Intervals are Student-t over three seed differences, not over individual
questions. New accuracy also misses the non-regression threshold against
verified prose; one seed accounts for most of that gap.

| Control | Old deltas by seed | Mean old delta [95% CI] | Mean new delta [95% CI] |
| --- | --- | --- | --- |
| Same-question teacher | +0.69, −3.12, −1.74 | −1.39 [−6.19, +3.41] | +4.51 [−9.04, +18.07] |
| Style-matched teacher | +1.04, +0.69, −2.78 | −0.35 [−5.59, +4.90] | +5.56 [−17.12, +28.23] |
| Verified generated prose | −2.08, −0.69, 0.00 | −0.93 [−3.56, +1.71] | −11.69 [−53.95, +30.57] |
| Unfiltered generated prose | +1.39, +1.04, −1.74 | +0.23 [−4.02, +4.49] | −11.46 [−53.51, +30.59] |

## Audit

- Every seed began at 100% old accuracy and lost at least 26.7 points with
  no replay. Both generation families covered 138/144, 144/144 and 144/144
  old facts in common. All three manipulation checks passed.
- Each arm saw 96,768 new next-token targets. Replay arms additionally saw
  4,032 next-token targets on identical fact schedules, with no masked or
  padded targets. The model sampled 576 attempts per replay family per seed.
- The canonical teacher's answer tokens differed from the self-answer on
  72/138, 109/144 and 62/144 questions. The style-matched teacher preserved
  the exact per-field, per-form style counts and differed on 81/138, 95/144
  and 85/144. Both used exactly the self-QA question prefix and fact value.
- Replay and evaluation use templated forms and known synthetic facts.
  The paired teacher controls isolate wording chosen by the model, not the
  benefit of choosing questions, fact coverage, or rehearsal timing.

## Reproduce

With Python 3.10 on CPU (tested with NumPy 2.2.6 and Torch 2.6.0+cpu):

```sh
python -m pip install numpy==2.2.6
python -m pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cpu
python -m unittest -v test_self_quiz_pilot
python self_quiz_pilot.py --split test > self-quiz.jsonl
python summarize_self_quiz.py < self-quiz.jsonl
```

See the [protocol](self-quiz-protocol.md) for the frozen gate.
