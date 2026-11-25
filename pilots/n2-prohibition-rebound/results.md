# N2 pilot results

**KILL.** Text rebound: -1.83 [-6.67, 3.00] pp. Positive rewrite minus logit mask at wave 6: 29.67 [15.00, 46.17] pp.

The text rise did not meet the 5 pp gate. The rewrite–mask interval excluded zero.

200 repeated wave-1 probes per wave and seed; seeds 17, 29, 43. Values are percent [paired 95% CI].

| Wave | Prompt tokens (all arms) | Text | Positive rewrite | Logit mask | Verifier violations | No-rule baseline | Verifier unresolved |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 149–156 | 73.33 [58.17, 86.33] | 32.50 [16.67, 49.83] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 31.17 [24.67, 38.17] | 66.33 [49.83, 81.00] |
| 2 | 221–228 | 71.83 [54.67, 86.83] | 29.33 [15.83, 44.50] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 35.17 [27.50, 43.33] | 65.33 [46.33, 82.33] |
| 3 | 294–301 | 74.67 [61.50, 86.17] | 29.83 [15.67, 45.83] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 35.00 [27.83, 42.67] | 66.67 [51.67, 80.17] |
| 4 | 368–375 | 68.67 [51.33, 84.33] | 25.33 [12.33, 40.67] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 32.67 [24.83, 41.00] | 61.83 [43.33, 79.00] |
| 5 | 444–451 | 71.00 [53.50, 86.50] | 29.33 [14.83, 45.83] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 34.50 [26.67, 42.50] | 64.67 [45.50, 82.17] |
| 6 | 521–528 | 71.50 [57.83, 83.67] | 29.67 [15.00, 46.17] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 38.00 [29.33, 46.67] | 63.33 [47.50, 77.67] |

The length-matched no-rule baseline picked the habitual tool on fewer than half the probes at every wave. This limits the result: the probes did not reliably elicit the would-be forbidden behavior without a rule. The text arm's high violation rate is an absolute failure of the negative instructions, not evidence of an increase with accumulation.

The verifier rejects rather than executes a forbidden proposal; its unresolved rate is the cost of running out of its two draws. The logit mask's zero violations are guaranteed in this two-tool interface. The pilot only measures routing under one accumulation order and does not test the attention mechanism or separate competition from other effects of a longer prompt.

## Reviewer rerun: baseline-screened probes

**KILL and close N2.** Text rebound: -0.17 [-1.67, 1.33] pp (paired 95% CI; gate: +5 pp).

200 fixed probes per wave and seed; seeds 17, 29, 43. Probes per queue: amber 20, birch 20, cobalt 20, delta 20, elm 20, flint 20, granite 20, harbor 20, ivory 20, jade 20.

Every selected probe had exact no-rule forbidden-tool probability ≥70% at every wave. Values are percent [paired 95% CI]; the exact model probability is averaged across the selected probes.

| Wave | Text violations | No-rule sampled forbidden calls | No-rule exact probability |
|---:|---:|---:|---:|
| 1 | 98.50 [96.50, 99.83] | 96.50 [94.00, 98.67] | 95.50 [94.20, 96.66] |
| 2 | 98.67 [96.50, 100.00] | 97.67 [95.50, 99.50] | 97.28 [96.50, 98.02] |
| 3 | 98.83 [96.83, 100.00] | 97.67 [95.67, 99.33] | 97.53 [96.66, 98.28] |
| 4 | 98.67 [96.50, 100.00] | 97.33 [95.33, 99.00] | 96.40 [95.19, 97.45] |
| 5 | 98.50 [96.33, 100.00] | 98.33 [96.50, 99.67] | 97.94 [97.25, 98.55] |
| 6 | 98.33 [96.17, 99.83] | 98.83 [97.67, 99.83] | 98.87 [98.39, 99.26] |

Interpretation is conditional on the screened cohort and one memory order. The baseline was used only for selection, and no text-rule scores were used to choose probes. This rerun did not compare rewrite, mask, or verifier.

The smallest exact no-rule probability among selected probes at any wave was 72.15%. But the text arm already violated 98.50% of probes at wave 1, leaving only 1.50 pp of possible increase. This closes N2 under the reviewer's decision rule; it does not rule out accumulation effects in settings where the initial prohibitions are effective enough to leave more headroom.
