# Rare-event distillation: kill this pilot

Weighted splitting found **10.4× as many old jam tails** as ordinary
MOPD replay, but didn't turn that coverage into a retention win at the fixed
budget. Post-shift old recovery was **10.7%** ([2.7%, 18.7%] 95% CI) with splitting
and **17.2%** ([-16.7%, 51.0%]) with prompt upsampling, the best control by point
estimate. The paired difference was **−6.5 pp** ([-40.5, +27.6] pp).
Splitting did beat ordinary MOPD on old recovery, but lost **1.06 pp** of old
common behavior ([-1.66, −0.47] pp), independently failing the retention gate.

## Held-out results

Expected action success, % (95% seed (t)-CI, three paired streams). X and Y
are the old and new domains. Intervals are not clipped to [0, 100]; the wide
intervals are part of the result, not evidence of equivalence.

| Arm | X recovery | X common | Y non-jam | Y jam |
| --- | ---: | ---: | ---: | ---: |
| Before shift | 99.4 [99.2, 99.6] | 100.0 [100.0, 100.0] | 48.8 [48.8, 48.8] | 0.4 [0.2, 0.6] |
| No replay (diagnostic) | 9.5 [8.1, 10.9] | 92.3 [91.9, 92.7] | 96.8 [96.4, 97.3] | 92.9 [92.2, 93.6] |
| MOPD-style | 3.1 [1.5, 4.7] | 96.3 [95.6, 96.9] | 94.9 [93.4, 96.4] | 92.3 [88.6, 96.1] |
| MOPD-style, tilted objective | 9.0 [3.1, 14.9] | 95.5 [95.3, 95.7] | 95.1 [94.3, 95.8] | 87.7 [82.3, 93.0] |
| Uniform prefix replay | 8.2 [−4.0, 20.4] | 96.0 [94.4, 97.5] | 93.3 [90.8, 95.9] | 89.6 [80.0, 99.3] |
| Prompt upsampling | 17.2 [−16.7, 51.0] | 94.9 [89.0, 100.8] | 94.3 [88.3, 100.3] | 77.8 [39.1, 116.5] |
| **Weighted splitting** | **10.7 [2.7, 18.7]** | **95.2 [94.4, 96.0]** | **95.9 [94.4, 97.3]** | **85.7 [80.3, 91.2]** |
| Direct terminal replay | 9.6 [6.5, 12.8] | 95.4 [94.9, 95.9] | 95.4 [93.9, 96.9] | 87.3 [81.8, 92.7] |

| Splitting minus control | X recovery, pp (95% CI) | X common, pp (95% CI) |
| --- | ---: | ---: |
| MOPD-style | +7.62 [+0.89, +14.34] | −1.06 [−1.66, −0.47] |
| MOPD-style, tilted objective | +1.66 [−8.20, +11.53] | −0.31 [−0.89, +0.27] |
| Uniform prefix replay | +2.48 [−7.07, +12.02] | −0.76 [−2.65, +1.13] |
| Prompt upsampling | −6.48 [−40.52, +27.55] | +0.31 [−6.15, +6.78] |
| Direct terminal replay | +1.06 [−5.47, +7.59] | −0.18 [−0.93, +0.58] |

## Budget and interpretation

Each replay arm used 4,096 old tails and 4,096 old teacher-token positions per
seed, alongside the identical 16,384 new training trajectories/label positions.
The old fit saw 811 jams in 786,432 trajectories across the three seeds, or
**1.03 per 1,000**. Unit of a tail is one terminal continuation; both fresh and
reused prefixes count as a rollout even if fewer live tool calls were needed.

| Replay arm | Old jam tails by seed | Distinct jam states by seed | Live root draws per seed | Live tool transitions per seed |
| --- | ---: | ---: | ---: | ---: |
| MOPD-style (either) | 5 / 1 / 6 | 5 / 1 / 6 | 4,096 | 4,096 |
| Uniform prefix replay | 5 / 6 / 3 | 5 / 5 / 3 | 1,338–1,367 | 2,718–2,755 |
| Prompt upsampling | 4 / 7 / 4 | 4 / 6 / 4 | 4,096 | 4,096 |
| Weighted splitting | 47 / 37 / 41 | 26 / 19 / 20 | 2,048 | 4,096 |
| Direct terminal replay | 2,049 / 2,048 / 2,049 | 43 / 40 / 41 | 2,048 | 2,048 |

Splitting did not beat ordinary sampling with the same tilted objective or
direct rehearsal of recorded jams. The win over plain MOPD does not isolate
branching: it shrank and became inconclusive when MOPD used the same objective.
No GPU follow-up for this variant. Revisit only with a reason why branching
should add useful recovery states unavailable to direct replay.

This is a synthetic, two-decision environment with an oracle risk flag and known
transition kernel. Only 896 parameters in a rank-one update of the constrained
C/D logits were trained on the 494M-parameter Qwen backbone, and the routing
action and backbone remained frozen. It tests prefix sampling under controlled
interference, not free-form generation or backbone fine-tuning. The
[MOPD baseline](https://arxiv.org/abs/2611.02746) uses the previous student as
teacher with token KL only; the [ReOPD-inspired baseline](https://arxiv.org/abs/2607.04763)
uses uniform, not the paper's step-decaying, prefix depth. Neither is a full
paper reproduction. See the [frozen protocol](protocol.md) and
[seed data and exact intervals](results.json).

## Reproduce

From the repository root on Linux with Python 3.10:

```bash
python -m pip install torch==2.7.1+cpu --index-url https://download.pytorch.org/whl/cpu
python -m pip install transformers==4.52.4 numpy==2.2.6 scipy==1.15.3
mkdir -p "$HOME/.cache/cl-rare-event"
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 python -m unittest discover -s experiments/rare_event -v
HF_HUB_DISABLE_XET=1 python experiments/rare_event/pilot.py --threads 8 \
  --cache "$HOME/.cache/cl-rare-event/features.pt" \
  --output "$HOME/.cache/cl-rare-event/results.json"
```

The full run took 44.5 s wall time on an 8-vCPU Intel Xeon VM, including 32.4 s
for frozen features (checkpoint already downloaded), with 3.2 GiB peak RSS.
The runner pins the checkpoint revision and records its own source hash.
