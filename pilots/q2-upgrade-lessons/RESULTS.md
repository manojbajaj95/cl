# Fleet Q2: KILL this pilot at the truth-reliability gate

## Truth reliability (checked first)

| Split-half measure across the 40 lessons | Estimate | Paired bootstrap 95% CI |
| --- | ---: | ---: |
| Spearman–Brown corrected | −0.041 | [−1.171, 0.509] |
| Raw Spearman rho | −0.020 | [−0.369, 0.342] |

**Stop:** corrected reliability was below 0.70; even the upper end of its
95% interval was below 0.70. The Spearman–Brown transform is reported
without clipping; it can fall below −1 for negative raw correlations.
Intervals resample lesson pairs 4,000 times while keeping the starting
codes fixed. See [per-lesson results](results.json).

The new model's no-lesson held-out success was **31.07%**. Exact full-split
lesson effects ranged from **+0.61 to +5.68 percentage points** (median
+1.84 pp), but **9/40** effects changed sign between the two halves.
All 40 average effects were positive on this particular set of six
starts, so it did not exhibit even one observed nonpositive lesson effect.
The two halves of three starts each did not support a stable ranking.

## What ran and what did not

- Qwen2.5-0.5B-Instruct → Qwen2.5-1.5B-Instruct, Q4_K_M, CPU, on the
  three-decision G1 router. The 40 frozen lesson entries comprise 20
  distilled notes from failures among 300 old-model episodes and 20
  stratified G1 notes. There were 38 distinct note texts.
- We enumerated all 27 action paths under each policy at each held-out
  starting code. The failed gate is disagreement over which starts
  define truth, not Monte Carlo variance from finite rollouts. Starts
  were disjoint from the writing/probe pool; later states can overlap.
- **Not measured:** no 60-episode probes, plain likelihood-gain
  rankings, source zero-shot baseline, old-model likelihood control,
  judge, pruning check or replication were collected after the stop.
  The two predictive thresholds (rho ≥ 0.50 and margin ≥ 0.15 over
  source zero-shot) were not evaluated. This kills this pilot, not the
  likelihood-gain hypothesis.

Compared with [PR #15's frozen protocol](PROTOCOL.md), exact truth replaces
the 200 paired rollouts and reliability is measured across held-out starts
rather than repeated draws. The planned predictor is ticket-specified
unweighted log-probability gain on actual successful logged actions, not
the original visitation-weighted probability lift. Source starts and the
next-token policy otherwise follow the frozen router design. A future
test would need more independently varying source and validation tasks:
additional rollouts on these same starts cannot change their exact truth
or its disagreement. Even on a richer test, predictor and truth share
new-model likelihoods; disjoint starts and full path enumeration reduce,
but do not remove, that dependence.
