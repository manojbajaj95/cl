# Preregistration: does the body connection have headroom, and is its loss variance?

Written and committed before `mechanism.py` was run (2026-11-27). The PR #418
pilot (`results_pr418.json`, reproduced by `pilot.py`) found that a curvature-gated
body connection Γ with a generic random-Fourier basis loses to EB12, a
6-parameter affine action map that is itself a least-squares projection of the
same learned Γ. This test asks why, with two added arms and a ritual-budget sweep.

## Added arms
- **Γ-oracle**: exact state-dependent transport through the true simulator,
  `u_dst = inverse_dst(q, q̇, forward_src(q, q̇, u_src))`, at the observed (noisy) state.
  It is the best any learned connection can do.
- **EB12-oracle**: the least-squares affine map fitted to Γ-oracle on the source
  ritual states. It is the best any affine map can do.

## Sweep
Ritual budget N ∈ {300, 1200, 4800, 19200} at 1% sensor noise, and N ∈ {1200, 19200}
at 0% noise; families curved, contact, mixed; 16 paired seeds. Rituals are nested
(the first N of one 19,200-sample draw per body, separate RNG), so skill
demonstrations and evaluation episodes are identical across N and noise levels.
Paired gaps are mean ± SE over seeds; "> 2 SE" means gap / SE > 2.

## Kill bar (Γ is promoted as a transport primitive only if K1, K2 and K3 all pass)
- **K1 headroom.** Curved family, N = 1200, 1% noise: Γ-oracle beats learned EB12
  on held-out S5 return by > 2 SE and by ≥ 0.010. Fail: state-dependent transport
  has no room to beat the affine map here, whatever the estimator.
- **K2 estimator.** For some N in the 1% noise grid, gated Γ beats both EB12 and
  GAT-MLP by > 2 SE on curved and on contact.
- **K3 retention.** At that N, gated Γ's S1–S4 retention is ≥ 0.85 on curved and contact.

## Mechanism predictions (descriptive, not gates)
- **M1 variance.** If the loss is finite-sample variance, Γ_RFF − EB12 rises with N
  at 1% noise and is larger at 0% noise than at 1% for the same N.
- **M2 bias.** If Γ_RFF stays below EB12 at N = 19,200 with no noise while Γ-oracle
  beats EB12, the generic basis is biased, not under-sampled.
