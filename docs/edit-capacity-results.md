# Sequential model-edit capacity pilot: KILL for GPU escalation

Unedited key covariance predicted collapse more accurately on average than the first-10% weight-norm control, but the improvement was not statistically clear: **mean absolute log-count error 0.220 vs. 0.407**, paired difference **−0.187 (95% CI −0.410 to +0.025)**. The mean advantage transferred to both held-out batch sizes, but neither size nor the pooled estimate cleared zero. The [locked decision rule](edit-capacity-protocol.md) therefore says not to spend GPU time. This is not evidence that the norm control won.

| Held-out batch size | Capacity error | Norm error | Capacity − norm (paired bootstrap 95% CI) |
| --- | ---: | ---: | ---: |
| 8 | 0.249 | 0.420 | −0.171 [−0.409, +0.055] |
| 32 | 0.192 | 0.394 | −0.202 [−0.428, +0.043] |
| Pooled | 0.220 | 0.407 | −0.187 [−0.410, +0.025] |

The six test streams are the bootstrap units (10,000 resamples); both batch-size results for a stream stay paired. In edit-count units, pooled MAE was **147 vs. 222 edits**. All 15 runs had observed collapses and passed the preregistered initial-edit check (96.9–100% efficacy at 32 edits).

## Forecasts and outcomes

GPT-2 small, CounterFact, CPU two-site MEMIT adaptation. Calibration at batch size 16 collapsed at 768, 736, and 704 edits, giving capacity multiplier 6.658 and log relative weight-norm threshold 0.592. Only the calibration fits used observed collapse labels. The norm slope for each test run used its first 192 edits only; each capacity forecast used only unedited activations and the frozen calibration multiplier. Collapse here means two successive checkpoints with at least 2× perplexity on held-out original CounterFact completions. Counts below are rounded to whole edits.

| Stream | Pre-edit covariance (both sizes) | Observed, size 8 | Norm, size 8 | Observed, size 32 | Norm, size 32 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 3 | 728 | 736 | 433 | 640 | 427 |
| 4 | 772 | 576 | 439 | 576 | 434 |
| 5 | 722 | 992 | 390 | 768 | 393 |
| 6 | 726 | 544 | 429 | 480 | 424 |
| 7 | 733 | 512 | 425 | 608 | 420 |
| 8 | 719 | 576 | 402 | 672 | 402 |

## What this does and does not show

- The rank varied little. As an exploratory check, just predicting the calibration median (736 edits) scored **0.216** pooled log error, slightly better than covariance. The win on point estimates over the norm control does not establish that covariance adds predictive information. The capacity forecast also cannot track batch-size effects on a fixed stream (up to 224 edits here).
- The norm control consistently predicted too early. It operationalizes the near-exponential growth account in [Norm Anchors](https://arxiv.org/abs/2602.02543) as a shared threshold plus a prefix log-linear extrapolation; the paper itself does not benchmark this forecast. A run-specific threshold cannot be learned from early norms alone without collapse labels.
- The alphaXiv check found prior evidence of abrupt collapse, edited-weight norm feedback, and drift of dominant weight singular directions ([Norm Anchors](https://arxiv.org/abs/2602.02543), [REVIVE](https://arxiv.org/abs/2601.11042)). [RoSE](https://arxiv.org/abs/2603.15518) uses covariance to explain same-subject generalization failures, not to forecast a sequential edit count. The search did not identify the exact pre-edit covariance forecast; that is not proof of novelty.
- This is a stress test with one model, one dataset, a fixed factual probe, a smaller-than-published moment weight, and fewer value-optimization steps than canonical MEMIT. It assumes the incoming stream is known in advance. It does not test GPT-2-XL, GPT-J, zsRE, or general-language collapse.

[Reproduction steps](../pilots/README.md) · [Per-run traces](../pilots/results/edit-capacity/)
