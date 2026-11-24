# P3 · Memory-write distractibility

**Verdict: KILL.** At 210 paired episodes per arm, a bad off-target lesson did
not increase bad writes versus the clean control (−1.90 percentage points,
95% CI [−5.24, +1.43]). The write-vs-solve-failure gap was −2.86 pp vs
length-matched filler [−7.62, +1.43], not the predicted positive gap.

## Replication

Same real-unit conversion tasks, wrong target lesson, no verifier, and numeric
judge as the [PR #4](https://github.com/manojbajaj95/cl/pull/4) cohort that went
from 12/32 to 17/28 bad writes. The clean cohort has no **bad** off-target lesson
(three correct ones); distractor corrupts one, and filler replaces that slot
with exactly token-matched neutral prose.

| Arm | Solve accuracy (Wilson 95% CI) | Bad writes (Wilson 95% CI) |
| --- | ---: | ---: |
| Clean | 0/210 · 0.00% [0.00, 1.80] | 99/210 · 47.14% [40.50, 53.88] |
| Distractor | 2/210 · 0.95% [0.26, 3.41] | 95/210 · 45.24% [38.65, 52.00] |
| Length-matched filler | 7/210 · 3.33% [1.62, 6.72] | 96/210 · 45.71% [39.11, 52.47] |

| Paired contrast (pp; 95% CI) | Δ bad writes | Δ solve failures | Δ bad writes − Δ solve failures |
| --- | ---: | ---: | ---: |
| Distractor − clean | −1.90 [−5.24, +1.43] | −0.95 [−2.38, 0.00] | −0.95 [−4.29, +2.38] |
| Filler − clean | −1.43 [−5.24, +2.38] | −3.33 [−5.71, −1.43] | +1.90 [−2.38, +6.19] |
| **Distractor − filler** | −0.48 [−4.29, +3.33] | +2.38 [0.00, +4.76] | **−2.86 [−7.62, +1.43]** |

## Writer intervention

All writers used the same 210 distractor-arm action trajectories (solve
accuracy 2/210). The mask beat baseline, trace-only, and the instruction,
but that benefit does not rescue the failed distractibility replication.

| Writer | Bad writes (Wilson 95% CI) | Mask minus writer (pp; paired 95% CI) | Mean input tokens |
| --- | ---: | ---: | ---: |
| Baseline | 95/210 · 45.24% [38.65, 52.00] | −10.95 [−15.24, −6.67] | 183.14 |
| Action-log-prob mask | 72/210 · 34.29% [28.20, 40.94] | — | 129.18 |
| Action trace only | 110/210 · 52.38% [45.64, 59.03] | −18.10 [−24.29, −11.90] | 89.45 |
| “Write only about the task” (baseline token count) | 113/210 · 53.81% [47.06, 60.42] | −19.52 [−23.81, −15.24] | 183.14 |

The mask retained 1.27 of four lessons on average and kept the corrupted
off-target lesson in 18/210 episodes. The instruction matches the baseline
token budget; this comparison does not isolate attribution-based selection
from other ways of shortening the context.

These results apply to Qwen2.5-1.5B-Instruct Q4_K_M and the fixed six-task
conversion suite. Solve accuracy was near floor, and the numeric write judge
measures factor recovery, not downstream usefulness of memories.

[Protocol and reproduction](PROTOCOL.md) · [Summary JSON](results.json) · [Paired episode log](episodes.jsonl)
