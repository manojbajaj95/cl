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
