# N1: layer-local lesson KV

**Verdict: KILL.** The mask retained **82.84%** of full-visibility held-out gain (95% CI **[79.35%, 85.94%]**), below the required **90%**. It reduced held-out harm **37.43%** relative to the training-gain-matched global bias **[21.99%, 50.43%]**, and beat the entropy-matched no-lesson arm's on-target gain by **1.7493 nats** **[1.5084, 1.9873]**. Neither offsets the failed retention gate. Exact station retrieval at the same recall retained all gain with zero off-target harm in this keyed task.

## Results

Correct-valve log-probability gain and harm (nats), with paired 95% bootstrap intervals:

| Arm | On-target gain | Off-target harm | Mask − arm gain | Mask − arm harm |
|---|---:|---:|---:|---:|
| Full visibility | 1.7187 [1.4996, 1.9355] | 1.3365 [1.2228, 1.4588] | −0.2950 [−0.3645, −0.2327] | −0.8060 [−0.9689, −0.6453] |
| **Layer mask** | **1.4237 [1.2313, 1.6150]** | **0.5305 [0.4486, 0.6186]** | — | — |
| Matched global bias | 1.1820 [1.0118, 1.3569] | 0.8479 [0.7288, 0.9814] | +0.2417 [0.1898, 0.2958] | −0.3174 [−0.4813, −0.1663] |
| Retrieval gating | 1.7187 [1.4996, 1.9355] | 0.0000 [0.0000, 0.0000] | −0.2950 [−0.3645, −0.2327] | +0.5305 [0.4486, 0.6186] |
| Narrow rewrite | 1.8527 [1.6164, 2.0883] | 1.3780 [1.3231, 1.4348] | −0.4290 [−0.5138, −0.3532] | −0.8475 [−0.9500, −0.7393] |
| No lesson, temperature matched | −0.3255 [−0.3760, −0.2747] | 0.0027 [0.0016, 0.0040] | +1.7493 [1.5084, 1.9873] | +0.5278 [0.4453, 0.6165] |

| Arm − no-lesson temperature | On-target gain | Off-target harm |
|---|---:|---:|
| Full visibility | +2.0442 [1.7743, 2.3117] | +1.3337 [1.2201, 1.4561] |
| Layer mask | +1.7493 [1.5084, 1.9873] | +0.5278 [0.4453, 0.6165] |
| Matched global bias | +1.5075 [1.2900, 1.7269] | +0.8451 [0.7263, 0.9783] |
| Retrieval gating | +2.0442 [1.7743, 2.3117] | −0.0027 [−0.0040, −0.0016] |
| Narrow rewrite | +2.1783 [1.8913, 2.4638] | +1.3753 [1.3198, 1.4324] |

The layer mask removed at least one block for 117/120 lessons. Mean absolute per-lesson training gain mismatch was 0.0033 nats (mask 1.4919; global bias 1.4952). The gain match did not remain exact on unseen phrasings: the mask gained 0.2417 nats more than the bias, with no held-out retuning. Mean per-lesson Spearman correlation of single-block help across splits was 0.847.

Source-only T = 0.828 (untempered entropy 0.5201, matched to full-visibility entropy 0.4240 nats). CPU wall time: 21m 57s. Per-seed values, masks and full-precision CIs are in [results.json](results.json).

## Protocol

- Same frozen CPU Qwen2.5-0.5B-Instruct as [M2](../m2_salience/RESULTS.md), rather than the 1.5B in the [proposal](https://github.com/manojbajaj95/cl/pull/18). Test 40 one-lesson station-valve tasks in each of three seeds (101, 202, 303); valve assignments and unrelated station probes vary by seed. Each lesson gives its station's recommendation and suggests that valve is safe generally. On-target probes need the recommendation; off-target probes ask about another station and explicitly supply a conflicting correct local instruction.
- Three on-target and three off-target prompt phrasings per lesson are used for training, and three different phrasings of each type are held out. Scores are the correct valve's log probability among A/B/C. **Gain** is mean on-target change relative to the no-note context. **Harm** is mean off-target log-prob loss, clipped at zero per probe so improvements cannot cancel interference.
- **Layer mask:** keep the lesson's prefix KV fixed and place a hard attention mask on its key positions at selected layers, for all suffix queries and heads. Group 24 layers into six consecutive blocks. Rank single-block removals by training harm; greedily accept those preserving at least 90% of training full-visibility gain and reducing harm, checking joint effects when combining removals. Keep at least one block visible. For nonpositive training gain, keep full visibility.
- **Matched global bias:** use the same prefix KV and one uniform scalar across all layers. Per lesson, choose the closest training gain to the mask's from a grid of seven biases (−10, −5, −2, −1, 0, +1, +2); refine with up to four interpolation steps when the grid brackets the target gain. No held-out labels are used to choose the mask or bias. **Retrieval:** expose the lesson only when its literal station name occurs in the question. It has the same 100% on-target recall as the nonempty layer mask; in this keyed world it is an intentionally strong gate. **Narrow rewrite:** explicitly limit the recommendation to its own station and forbid reuse elsewhere.
- **No-lesson temperature:** fit a single T matching full-visibility mean predictive entropy on 240 source queries (40 disjoint station identities × six train phrasings) only. Freeze it for evaluation and pair every arm's gains and harms against this baseline.
- CIs: 10,000 paired bootstrap draws resampling seeds and then lessons within seeds. Compare the mask with the global bias at matched training help, report held-out help and harm against all controls, and apply the gate: ≥90% of full held-out gain, ≥30% relative held-out harm reduction against matched global bias, and more held-out on-target gain than the entropy-matched no-lesson policy. Per-lesson Spearman correlation between training and held-out single-block help is an additional transfer diagnostic from the proposal.

## Reproduce

Use the environment from [M2](../m2_salience/RESULTS.md). From the repository root:

```sh
SECONDS=0  # Bash elapsed time
python -m pilots.n1_layer_local_kv.pilot --threads 8 --output raw-n1.json
python -m pilots.n1_layer_local_kv.report raw-n1.json --wall-seconds "$SECONDS" --output n1-results.json
```
