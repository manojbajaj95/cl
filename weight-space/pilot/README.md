# Source-free upgrade pilots (CPU)

Run from the repository root with Python 3.10+:

```sh
python -m pip install -r weight-space/pilot/requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python weight-space/pilot/rebase.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python weight-space/pilot/routed.py
```

The dependencies are NumPy and scikit-learn; the bundled 8×8 digits dataset needs no download. Both scripts default to seeds 0–9; pass `--seeds 0` for a smoke run. Tested with Python 3.10.12 and the versions in the requirements file. The scripts include numeric checks for gauge invariance/additive removal and exact off-branch invariance when a routed patch is disabled, respectively.

## Setup

Each split uses disjoint original images before deriving clean, 90°-rotated and inverted views: 1,000 source training, 64 fit, 96 audit, and 637 labeled test. The only true labels in migration are in the privileged refit reference; the evaluation uses all methods' same hidden test splits. We regard probe images/transformation names as public resources (not private source training images); their bytes and the router are **not** included in the payload figure below. This is a toy study with correlated synthetic domains and repeated splits, not independent model release chains. The three target types are a gauge-equivalent permutation/positive rescaling of the source MLP, an independently trained MLP with noisy clean inputs, and that independent MLP with only four surviving hidden units. They are separate target stress cases, not three dependent releases.

## Pilot 1: static patches collide

The source learns two additive head updates in succession. Store each patch's centered logit effects on its positive fit probes and declare zero on other domains. At an upgrade, solve a ridge fit from the target features and sum the new patches without input-dependent routing. Positive-only fitting ignores unrelated inputs; a feature bridge fits target→source activations and then applies the source patch. Neither is a complete reproduction of a published migration system. `refit` can use the original labels and the same static head family. Accuracy percentages below are means over 10 seeds.

| Release | Method | Clean | Rotated | Inverted | Harmful / 10 | Admitted / 10 |
|---|---|---:|---:|---:|---:|---:|
| Gauge | Base only | 92.3 | 10.5 | 0.5 | 10 | — |
| Gauge | Static contract | 73.2 | 60.1 | 28.6 | 10 | 0 |
| Gauge | Labeled refit | 74.3 | 68.7 | 38.5 | 10 | — |
| Independent | Raw copy | 14.0 | 9.0 | 8.4 | 10 | 0 |
| Independent | Feature bridge | 5.4 | 20.0 | 28.7 | 10 | 0 |
| Independent | Positive-only | 2.6 | 24.8 | 29.8 | 10 | 0 |
| Independent | Static contract | 69.1 | 33.3 | 6.4 | 10 | 0 |
| Independent | Labeled refit | 66.3 | 66.9 | 16.2 | 10 | — |
| Bottleneck | Static contract | 5.1 | 12.3 | 17.5 | 10 | 0 |

Source clean / rotated / inverted was 89.5 / 54.3 / 0.8 with only patch A and 73.2 / 60.1 / 28.6 with both. A gauge change reproduces the source static scores exactly (numerical tolerance); its bad clean result is an installation problem, not migration. Even privileged refit cannot meet retention using this final-head parameterization and these constraints. The audit rejects all attempted migrations: zero bad admits here is **not** evidence of useful deployment. It requires ≥95% clean agreement with the bare target, per-skill agreement with the source specialist no more than 8 points below the source static installation, and ≥90% agreement with that skill's standalone target patch.

## Pivot: a routed, compact response capsule

Keep a fixed input router trained on **known view IDs**, not digit labels, on the 64 public fit examples per view. It sees no domain ID at inference. It falls back to the target base if maximum probability is below 0.90 or it predicts clean. Recompile each residual head on its own fit slice from saved source-specialist logits. `replay` keeps full-precision logits; `capsule` uses one symmetric int8 scale per task, using **644 bytes per task** for 64×10 fit scores and a float32 scale, versus 2,560 bytes for float32 values (the unquantized NumPy control uses float64 in memory). This excludes audit outputs, inputs, installed patch weights, and routing state; it is not a constant-total-budget system. Disabling A with the router frozen does not change outputs when any other branch is selected; that is a structural property, not proof that routing selects the right scope.

| Release | Method | Clean | Rotated | Inverted | Harmful / 10 | Admitted / 10 | Harmful admits |
|---|---|---:|---:|---:|---:|---:|---:|
| Gauge | Capsule | 92.3 | 86.0 | 85.8 | 7 | 10 | 7 |
| Independent | Base only | 91.8 | 12.8 | 0.2 | 10 | 0 | 0 |
| Independent | Routed raw copy | 91.8 | 11.1 | 6.5 | 10 | 0 | 0 |
| Independent | Routed replay | 91.8 | 80.8 | 79.9 | 10 | 3 | 3 |
| Independent | Capsule | 91.8 | 80.8 | 79.9 | 10 | 3 | 3 |
| Independent | Labeled routed refit | 91.8 | 90.3 | 90.3 | 1 | 10 | 1 |
| Bottleneck | Capsule | 21.2 | 32.1 | 35.4 | 10 | 0 | 0 |

Source routed performance was 92.3 / 89.8 / 91.0. The pivot recovered much of both skills with no mean clean cost, and int8 matched unquantized means to the printed precision. The provisional audit (≥95% clean agreement and ≥80% agreement with each specialist) nevertheless admitted 3/10 independent targets, **all harmful** by the gold metric. In both pilots harmful means >2 percentage points below the bare target on clean or >5 points below the respective source install on any registered skill. Known routing was 100.0 / 99.2 / 100.0%, with no inverted test predictions changing when A was revoked, but applying a patch to **10.1%** of unregistered rotated-inverted inputs exposed an overlap failure; upside-down inputs triggered 0.0%. Neither support case is an open-set guarantee.

The result supports conditional reconstruction and cheap retained outputs in a controlled case, not safe admission or a novel CL result. The decisive next test is counterfactual witness selection against random saved logits under equal total budgets, on genuinely ambiguous and unseen release/task combinations.
