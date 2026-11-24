# Functional syndromes: MEMIT MLP pilot

**Verdict: kill the fixed MEMIT-key syndrome.** On GPT-2-XL with 1,000 CounterFact edits, the most damaged 10% held **18.9% (95% CI 18.3–19.7%)** and **19.1% (18.4–19.9%)** of raw damage energy across two WikiText-2 runs, far below the 80% gate. Restricting the analysis to the 263 cases where MEMIT actually flipped the model's answer preference gave essentially the same result. At equal storage, the sparse decoder did not reliably improve on either baseline.

The proposed code measures damage to an edit's response to a fixed MLP input. It is not weight ECC: [Repair Brain Damage](https://arxiv.org/abs/2602.00076) constrains network weights to correct sparse hardware/computation faults, and [SANAI](https://arxiv.org/abs/2611.02042) embeds keyed parity for weight bit flips. Here an ordinary optimizer update can change all weights legitimately, and the pilot asks whether its effects happen to concentrate on a small fraction of edit keys.

## Results

All brackets are 95% bootstrap CIs. Full precision and per-layer estimates are in [results.json](results.json).

| Metric | Training seed 302 | Training seed 303 |
| --- | ---: | ---: |
| Raw damage energy in top 10% | 18.9% [18.3, 19.7] | 19.1% [18.4, 19.9] |
| Raw damage energy in top 10%, among 263 edit-induced wins | 19.3% [18.2, 20.3] | 19.4% [18.3, 20.3] |
| Edit-normalized damage energy in top 10% | 46.7% [24.9, 62.9] | 48.3% [25.1, 64.9] |
| Edit-direction projected energy in top 10% | 51.4% [48.0, 54.9] | 47.9% [44.8, 51.0] |
| Opposite-to-edit projected energy in top 10% | 79.6% [75.1, 83.6] | 69.9% [65.6, 73.8] |
| Positive functional drop energy in top 10% | 98.8% [98.0, 99.3] | 98.7% [97.8, 99.3] |
| Pearson correlation: raw damage norm vs. functional drop | −0.069 [−0.125, −0.016] | −0.070 [−0.124, −0.020] |
| Rewrite preference after fine-tuning | 46.0% [42.9, 49.4] | 45.8% [42.7, 49.0] |
| Net preference decrease from post-edit | 1.5 pp [0.2, 2.8] | 1.7 pp [0.4, 2.9] |
| Mean edited-target probability decrease | 0.19 pp [0.10, 0.29] | 0.25 pp [0.17, 0.35] |
| Retained preference wins among the 263 edits that flipped the answer | 88.6% [84.8, 92.4] | 89.7% [85.6, 93.5] |
| Reserved WikiText next-token NLL, pre → post | 5.232 → 4.722 | 4.868 → 4.550 |

The base model preferred the edited answer for 21.7% [19.2, 24.4] of the cases; MEMIT raised that to 47.5% [44.5, 50.7] before training. Mean edited-target probability rose from 0.29% to 3.34%. The highly concentrated behavioral drops don't rescue this sketch: the coded readout observes the raw linear response, and its norm is weakly negatively correlated with the behavioral drop. The one-sided edit-direction diagnostic uses fact-specific edit responses that the tested decoder does not store.

| Top-100 raw-damage recovery, 16 MB each | Seed 302 | Seed 303 |
| --- | ---: | ---: |
| Syndrome recall = precision | 11.05% [9.85, 12.20] | 11.20% [10.20, 12.60] |
| Dense least-squares recall = precision | 11.55% [10.40, 12.75] | 11.25% [10.00, 12.50] |
| Replay coverage recall = precision | 10.50% [9.10, 12.00] | 10.45% [9.15, 11.90] |
| Paired recall difference, syndrome − dense | −0.50 pp [−2.15, 1.30] | −0.05 pp [−1.60, 1.75] |
| Paired recall difference, syndrome − replay | +0.55 pp [−1.15, 2.30] | +0.75 pp [−0.95, 2.50] |

Both truth and prediction sets have size 100, so the recall percentages also give the number of true positives per attempt. The primary gate failed, so no repair training was run. The verdict applies to this CPU-adapted MEMIT recipe, this edit batch, and one shift objective with two training streams; it does not rule out other readouts, full MEMIT, or other types of shifts. The main model run took 1,921 seconds and peaked at 22,334,316 kB RSS on eight CPU threads.

## Decision protocol

For each of 1,000 CounterFact edits, use its original MEMIT key at each of GPT-2-XL layers 13–17, and read the subsequent training perturbation on that fixed key. The primary damage score is `D_i = Σ_l ||(W_l,post-FT − W_l,post-edit) k_il||²`, not a last-layer activation difference. **Kill if the most damaged 10% hold less than 80% of total damage energy.** Passing this gate is necessary but not sufficient: the coded decoder must find more of those 100 facts than both an equally sized replay buffer and a dense sketch with least-squares decoding before advancing.

## Method

- Draw 1,000 cases with NumPy seed 301, excluding repeated (subject, relation) pairs. The edit algorithm follows [MEMIT](https://github.com/kmeng01/memit): optimize an intervention at the last subject token in layer 17, then distribute the remaining target residual across successive MLP projections using the published Wikipedia uncentered second moments and regularization weight 20,000. CPU simplifications: canonical rewrite prompt only (no generated context ensemble), batched latent optimization with two Adam steps (rather than up to 19), and the subject KL prompt. Report rewrite efficacy rather than assuming all writes succeeded.
- Fine-tune only the five edited projection matrices (51.2M parameters) with AdamW (learning rate `2e-5`, zero weight decay), on next-token prediction from WikiText-2 raw train. Independent paragraph shuffles (302 and 303), 100 updates of two 32-token sequences each, from the identical edited checkpoint. The loss diagnostic uses two reserved batches per shuffle and is not a WikiText validation-split benchmark.
- Rewrite efficacy is whether the canonical prompt assigns higher geometric-mean token probability to the edited answer than the original answer. Functional damage is the before-minus-after edited-answer geometric-mean token probability. For functional concentration use its positive part squared (ignore improvements). Also report key-space concentration within initially successful new edits, after normalizing by `Σ_l ||ΔW_l,edit k_il||²`, and projected onto the concatenated edit response, with and without limiting to opposite-direction components. Percentile 95% CIs resample fact indices within a run; they are conditional on this model/edit batch and do not represent independent training runs.
- At each layer, store 100 Gaussian linear mixtures of input keys (`q_jl = Σ_i C_ji k_il`, shared code matrix across layers) and their reference post-edit reads. Later read `ΔW_l q_jl` by subtraction. Simultaneous orthogonal matching pursuit uses the common support across all layers and output coordinates. Minimum-norm dense least squares receives **the same** Gaussian observations. The replay support baseline can only directly re-edit the 100 uniformly sampled facts whose original pairs it stored. Its reported score is coverage of the damaged set (assuming perfect re-edit of covered facts); the diagnostic does not measure post-repair behavior.
- Every method has 100 × 5 × (6,400 + 1,600) × 4 = **16,000,000 bytes** of float32 payload: input key plus desired value (replay), or mixed key plus reference output (both sketches). All have shared, external fact IDs; draw matrices/indices are reproduced from seeds, so there is no stored matrix or per-fact keybook in the decoder. Seed/header metadata is excluded for all methods. The offline runs compute the subtraction equivalently using the saved weight difference, but still charge the reference output in the sketch payload. Reconstruction does not read the oracle raw keys or per-fact damage; the raw keys are used to form the checks, and the damage only scores predictions. Report precision, recall, and recall differences with percentile bootstrap CIs over 20 paired code/replay draws per training seed, conditional on that seed's damage.

## Reproduce

Use Python 3.10 and a CPU environment with roughly 31 GiB RAM. Downloads and run artifacts stay outside git.

```bash
PILOT="$PWD/pilots/functional_syndromes"
DATA="$HOME/.functional-syndromes-data"
python -m pip install -r "$PILOT/requirements.txt"
mkdir -p "$DATA"/{gpt2-xl,stats}

gpt2_rev=15ea56dee5df4983c59b2538573817e1667135e2
wiki_rev=b08601e04326c79dfdd32d625aee71d232d685c3
for f in config.json tokenizer.json vocab.json merges.txt model.safetensors; do
  curl -fL "https://huggingface.co/gpt2-xl/resolve/$gpt2_rev/$f" -o "$DATA/gpt2-xl/$f"
done
curl -fL https://rome.baulab.info/data/dsets/counterfact.json -o "$DATA/counterfact.json"
curl -fL "https://huggingface.co/datasets/Salesforce/wikitext/resolve/$wiki_rev/wikitext-2-raw-v1/train-00000-of-00001.parquet" \
  -o "$DATA/wikitext-2-train.parquet"
for i in {13..17}; do
  f="transformer.h.$i.mlp.c_proj_float32_mom2_100000.npz"
  curl -fL "https://rome.baulab.info/data/stats/gpt2-xl/wikipedia_stats/$f" -o "$DATA/stats/$f"
done
(cd "$DATA" && sha256sum -c "$PILOT/inputs.sha256")

python "$PILOT/run_pilot.py" --data "$DATA" --output "$DATA/xl" \
  --n 1000 --batch 48 --z-steps 2 --train-steps 100 --train-seeds 302 303
OPENBLAS_NUM_THREADS=4 python "$PILOT/analyze.py" "$DATA/xl"/seed-*.npz --draws 20
python -m unittest discover -s "$PILOT" -v
```
