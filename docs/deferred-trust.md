# Deferred trust: revising a stream without replay

A learner that no longer has the stream cannot generally replay it under a
new source-trust policy. This pilot asks whether it can maintain **joint
responses to trust changes** during training, with a fixed number of
parameter vectors, and later tell when the approximation is unreliable.
Multipliers apply to every example carrying the named source ID; their
values are revealed only after the stream. The reference is chronological
SGD from the same initialization, not a converged batch fit.

See the [frozen protocol](deferred-trust-protocol.md). Radius 0.5 queries
downweight or upweight sources by half; radius 1 queries include both
zeroing and doubling weights. A revision is an off-center readout; it
does not re-center or mutate the live learner.

## Results and decision

**Keep the self-audit as a narrow result; do not scale yet.** Higher-order
state can help in a partly coupled stream, but no candidate beat the
strongest control on dense streams or on digits. Results below are for
parameter reconstruction (lower RMSE is better), not accuracy.

| First held-out split | Dense Taylor | Affinity Taylor | Sketched Taylor | Affinity shadows | Joint shadows |
| --- | ---: | ---: | ---: | ---: | ---: |
| Paired | 1.054 | 1.054 | 1.054 | 0.859 | 0.859 |
| Bridged | 0.934 | 2.289 | 1.623 | 2.488 | 1.795 |
| Dense | 0.062 | 1.414 | 1.711 | 1.453 | 2.007 |
| Digits | 0.055 | 0.980 | 1.204 | 0.999 | 1.460 |

*Units: mean parameter RMSE × 1,000 at radius 0.5, 24 paired streams
per family. Dense Taylor has a larger memory budget.*

1. **H1: killed as a general compression win.** The sketch recovered all
   12 interaction pairs with 13 rows on every paired stream, and matched
   dense Taylor with 97 vs. 325 live parameter vectors (65,088 vs. 187,200
   bytes including the probe directions at dimension 72). But simple
   input-affinity gating also matched dense Taylor on this fixture.
   Under weak feature bridges, sketching beat affinity by **29.1%**
   (paired 95% CI 23.6–33.9%) but was **73.8% worse** than dense Taylor.
   This exact sparse recovery does not establish a superior learning
   algorithm.
2. **H2: keep only under weak coupling.** Joint shadows passed the
   original axis and ridge comparisons on paired streams but tied the
   post-hoc affinity-shadow control there. On bridged streams they beat
   the strongest derivative-free control by **27.8%** (22.5–32.4%),
   dropping to **12.4%** (6.7–17.4%) vs. the best derivative-free
   control at radius 1. Dense and digits results falsify transfer.
3. **H3: passed the narrower fallback test.** Against a no-pair Taylor
   learner, the data-free guard reduced RMSE by **60.7%** (57.8–63.3%)
   on paired streams and **36.7%** (33.2–39.9%) with bridges. It met the
   5% regression bound against that same baseline in dense and digits,
   falling back in 44 of 48 streams across those two families. It still
   lost to affinity Taylor on both and did not reliably beat axis
   shadows after source rekeying (0.7% reduction; −3.0–4.6%).

At radius 0.5, differences in mean clean log loss vs the chronological
oracle were smaller than 0.00005 for the sketch/shadow methods in each
family, with no consistent advantage over controls. The better
parameter match is not evidence of a better classifier. In the paired
split, median sketch and dense-jet training times were 39 and 69 ms per
stream on one CPU thread; affinity Taylor took 37 ms. These timings
exclude query decoding and do not equate FLOP budgets. The added
affinity-shadow control spends 73 live model vectors plus 24 fingerprint
vectors, not the same number of SGD updates as a 97-model shadow bank.

**Next gate:** replay a timestamped, real-provenance stream (for example,
WILDS iWildCam camera IDs, with fixed image embeddings), choose sources
by event count rather than measured interaction rank, and hold out both
time windows and trust edits. Require at least 20% lower revision RMSE
than tuned equal-byte affinity, shadow and reservoir controls, with no
clean-holdout loss regression. If it fails that CPU-scale test, stop this
direction rather than buying GPU time.

## Mechanism

Let `w(a)` denote the final model with trust multipliers `a`, and let
`J_i`, `D_i` and `H_ij` be its first, diagonal second and off-diagonal
second derivatives at `a=1`. Readout for `a=1+q` is
`w(1) + Σ_i q_i J_i + ½ Σ_i q_i² D_i + Σ_{i<j} q_i q_j H_ij`.

**Directional sketch.** With training example `(x,y,s)` (source `s`),
logistic error `f = sigmoid(w·x)-y`, and rate `η`, each update is
`w ← w−η a_s f x`. At unit trust define `v_i = x·J_i`. Differentiating
the *update*, not the final test loss, gives the cross derivative update

```text
H_ij ← H_ij − η x [ f' (x·H_ij) + f'' v_i v_j + f' (1[i=s] v_j + 1[j=s] v_i) ]
```

For a fixed direction `z`, maintain `B_z = Σ_{i<j} z_i z_j H_ij`.
The linear transport term is the same across all pairs, so transport
commutes with projection. The two projected forcing terms are
`f'' [(z·v)² − Σ_i z_i² v_i²]/2` and
`f' [z_s (z·v) − z_s² v_s]`. This is an exact sketch of the Taylor
coefficients, without ever storing the dense pair table. With `K`
sources, `d` parameters and `M` sketches, persistent state is
`O((K+M)d + MK)`, versus `O(K²d)` for the dense jet.
The per-example work for this rank-one logistic update is
`O((K+M)d + MK)`; this is not a scaling claim for general neural
optimization. Query-time code materializes the `M × (K choose 2)` probe
matrix transiently; the training loop does not.

**Identifiability.** The rows of the probe matrix are
`Φ_z,ij = z_i z_j`. For independent Gaussian `z`, the matrix is full
spark almost surely: for any set of at most `M` distinct monomials there
exist evaluation points with independent evaluation vectors (otherwise
some nonzero linear combination of those monomials vanishes everywhere).
The associated determinant is a nonzero polynomial, so it is nonzero
almost surely. If the active rows of `H` have support size and rank
`s`, the span of `ΦH` is exactly that of the active columns of `Φ`.
When `M ≥ s+1` this span identifies the support by standard
[rank-aware MUSIC](https://doi.org/10.1109/tit.2011.2173722).
With `M=s` any full-rank candidate support of size `s` could explain
the same sketch. If `H` is unrestricted and `M < (K choose 2)`,
directions in the kernel of `Φ` can change query answers while
leaving the sketch unchanged. The sharp result concerns local
derivatives, not exact reconstruction of finite revisions.

**Mixed shadows.** Run probes as live policy variants rather than
differentiating the update. Single-source pairs of shadows fit the
first and diagonal second terms. All-source signed pairs estimate
mixed terms via the even finite difference after removing the diagonal
contribution. Decode with MUSIC or a matched-probe ridge control.
These differences have higher-order contamination and need independent
probes; in dense coupling, a sparse decoder can be worse than dropping
all mixed terms. The source-affinity shadow control instead pairs
sources using their first inputs and initializes each joint shadow
from the older source's already-trained single shadow.

**Data-free self-audit.** Split the Gaussian measurements into fit,
selection and confirmation sets. Confirm against a no-pair prediction
before using the decoded correction; otherwise use the exact diagonal
jet. For a **fixed** estimate from the fit/selection rows, a fresh probe's
expected squared residual equals `||H−Ĥ||_F²`: distinct off-diagonal
monomials are orthogonal with unit second moment. For uniform
fixed-size edits with independent random signs and radius `r`, expected
squared **pair-term** error is that same Frobenius error times
`r⁴ k(k−1)/(K(K−1))` for `k` edited sources. This is an average over
random queries; confirmation residuals are noisy, and neither guarantee
holds for arbitrary targeted edits or for higher-order Taylor error.

## Closest work and what this does not claim

- [Interaction-Aware Influence Functions](https://arxiv.org/abs/2605.15675)
  already show benefits of pairwise group attribution by expanding a
  target around a fitted model. [Source](https://arxiv.org/abs/2405.12186)
  already uses approximate unrolled differentiation to account for
  training dynamics. We do not claim novelty in pair terms or
  differentiating a trajectory.
- [Datamodels](https://arxiv.org/abs/2202.00622) already predict
  training-subset counterfactuals from model ensembles.
  [Datamodel Matching](https://arxiv.org/abs/2410.23232) applies prediction
  surrogates to approximate unlearning. Mixed shadows are a streaming
  instance of that general idea, not a priority claim over it.
- The unverified novelty candidate is the **combination** of exact
  streaming measurements of joint weight response, a rank condition
  specific to that response, and a replay-free test of whether decoding
  is warranted. MUSIC and random-projection validation are not new.
  This pilot is not evidence of a publication-level discovery, certified
  deletion, a better classifier, or transfer to a neural optimizer.

## Reproduce

```sh
python -m pip install numpy==2.2.6 scipy==1.15.3 scikit-learn==1.7.2
OPENBLAS_NUM_THREADS=1 python -m unittest -v
OPENBLAS_NUM_THREADS=1 python deferred_trust.py --split test > /tmp/trust-test.jsonl
OPENBLAS_NUM_THREADS=1 python deferred_trust.py --split audit > /tmp/trust-audit.jsonl
python summarize_deferred_trust.py /tmp/trust-test.jsonl
python summarize_deferred_trust.py /tmp/trust-audit.jsonl
```

The harness loads generated examples to give every method the same
chronology and score exact reruns. The sketch and shadow update rules
consume only the current example plus their own state; query functions
do not use historical labels. Digits is a real image dataset but has
randomly assigned source IDs and simulated corruption. Its bootstrap
measures variation over assignments and splits, not over new datasets.
