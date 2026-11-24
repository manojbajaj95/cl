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

The result supports conditional reconstruction and cheap retained outputs in a controlled case, not safe admission or a novel CL result.

## Follow-up: held-out release chains

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python weight-space/pilot/witnesses.py --fit 48
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python weight-space/pilot/witnesses.py --fit 120
```

Ten validation chains (seeds 0–9) and 20 held-out chains (20–39) use disjoint original digits and different noise/capacity schedules. Within each chain, a replacement MLP continues training across four releases independently of installed patches; intermediate releases also have controlled hidden-unit masks. Each install rebuilds patches from the original capsule, not from the previous patched model, and needs no legacy model. Trunk training uses 480 private originals, the candidate pool has 160 public originals, and audit/label evaluation use neither pool. The learned router, ridge compiler, and random 48-row audit per skill are common to all methods, making this a comparison of **fit-witness selection**, not an open-set routing or audit-selection experiment. The held-out lineages share one digits partition and are repeated simulation draws, not independent datasets or real vendor releases.

The primary comparator is uniform int8 replay. The variants select diverse points in normalized feature/pixel space, high source-specialist margin where the bare model or sibling predicts a different class, both together, or both with round-robin balancing by the source's predicted class. Plain replay stores as many full-precision rows as fit under the same byte ceiling (13 or 34 rows per skill); the residual budget is less than one extra row per skill. Budgets include uint16 fit/audit indices, stored fit logits/scales, and uint8 audit labels for two skills. Public inputs, the fixed router, and target patch weights are shared costs and excluded. Label refit is a privileged diagnostic with the full 480 labeled training rows and the same model capacity, not a cost-matched competitor.

**Primary endpoint:** fraction of harmful accepted releases at exactly 65% coverage (52/80), ranked by worst agreement with source specialists and the bare target on clean inputs. Harm is the previously defined >2-point clean or >5-point per-skill regression. Ranking with all releases available measures separability, not an online deployment policy. For an online-style check, freeze each method's audit threshold at the validation 65% quantile and report realized test coverage/risk. Percentile intervals use 4,000 paired bootstraps over whole seed chains; rows within a chain are not resampled independently. Intervals are descriptive, unadjusted for the exploratory follow-up comparisons.

**120 fit rows per skill:**

| Method | Stored bytes | Harm at 65% coverage, 95% CI | Harm difference vs. random, paired 95% CI (pp) | Frozen coverage / harm | Mean skill accuracy |
|---|---:|---:|---:|---:|---:|
| Random int8 | 3,176 | 88.5% [76.9, 98.1] | — | 62.5% / 90.0% | 79.8% |
| Plain FP32 replay | 3,144 | 100.0% [100.0, 100.0] | +11.5 [+1.9, +23.1] | 67.5% / 100.0% | 62.9% |
| Diversity | 3,176 | 75.0% [57.7, 88.5] | −13.5 [−34.6, +3.8] | 55.0% / 72.7% | 81.0% |
| Contrast | 3,176 | 98.1% [94.2, 100.0] | +9.6 [0.0, +21.2] | 62.5% / 98.0% | 76.0% |
| Hybrid | 3,176 | 88.5% [76.9, 98.1] | 0.0 [−15.4, +15.4] | 71.2% / 89.5% | 79.5% |
| Balanced hybrid | 3,176 | 75.0% [59.6, 90.4] | −13.5 [−30.8, +1.9] | 70.0% / 76.8% | 80.9% |
| Label refit | Oracle | 11.5% [3.8, 19.2] | −76.9 [−90.4, −63.5] | 61.3% / 10.2% | 86.0% |

At 48 rows (1,448 bytes), balanced hybrid raised mean skill accuracy by **4.81 pp [3.78, 5.95]**, but its admitted harm was **96.2% vs. 100.0%**, a paired difference of **−3.8 pp [−11.5, 0.0]**. At 120 rows diversity improved mean skill accuracy by **1.14 pp [0.59, 1.74]**, but was no better than the balanced variant on the primary endpoint. Clean accuracy was 83.5% for every method at both budgets. The full-label diagnostic shows that the task is not intrinsically impossible under the head capacity; the smaller capsule often cannot reconstruct enough of the distribution. **No variant met the 30% relative harmful-admission reduction gate or produced a clear primary-endpoint win.** The improvements in average accuracy do not warrant scaling.

## Procedural pivot: revised rules in new weight coordinates

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python weight-space/pilot/procedures.py
```

Twenty seeded chains draw affine finite-state primitives on seven states and compose them into a named macro. Public anchors map logical states into changing widths and bases. A pseudoinverse compiles each transition into matrices executed in the target representation, without the source. A release revises one primitive and rederives its dependent macro; a later release revokes another primitive and removes the macro. Enumerate every supported length-2–4 sequence from every state. The same compiler receives either rule coefficients (two bytes per primitive), two outputs at fixed anchor states interpreted with the affine prior (two bytes), or a two-output lookup defaulting to identity on unknown states. All share the grammar schema, name IDs, macro, and anchors; the raw payload comparison excludes those fixed costs.

| Release | Rule compiler | Two-demo affine induction | Two-demo lookup |
|---|---:|---:|---:|
| Initial | 100.0% | 100.0% | 17.5% |
| Revision | 100.0% | 100.0% | 17.6% |
| Revocation | 100.0% | 100.0% | 25.0% |
| Collapsed anchors | Abstained 20/20 | Abstained 20/20 | Abstained 20/20 |

These are exact exhaustive checks per generated grammar, not a learning result. With the affine prior, the demonstration baseline is analytically equivalent: the outputs from states 0 and 1 uniquely determine the offset and multiplier. The low-rank anchor collapse invalidates the full-state readout, so the compiler rejects rather than claiming preservation. This pivot demonstrates an exact operational property, but **not a novel advantage**; beating only the lookup control would be misleading.
