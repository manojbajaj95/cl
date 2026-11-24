# CPU retrieval-depth gate

Use the same checkpoint, 16 families, source/held-out split, solve/write menus, hidden oracles, weak smoke feedback, and stochastic decoder as the [original precheck](protocol.md). Reuse its frozen k=1 policies. For each k in {2, 4, 8}, score stacks of k relevant notes about the same bug family. Distinct provenance labels represent repeated evidence for the same underlying rule, not independent rules. Rotate label order and the one changed slot deterministically, balanced over families. Verify equal full-prompt token counts across all arms; all notes take the same slot format.

| Arm | Defective notes | Sound notes | Filler notes |
| --- | ---: | ---: | ---: |
| All sound | 0 | k | 0 |
| One bad, rest sound | 1 | k−1 | 0 |
| All bad | k | 0 | 0 |
| All filler | 0 | 0 | k |
| One bad, rest filler | 1 | 0 | k−1 |
| One filler, rest sound | 0 | k−1 | 1 |

**Funding gate: local per-defect effect in a mostly sound pool.** With one changed slot and the other k−1 notes sound, let `p1` and `p0` be new-helper defect risks with bad and filler in that slot. Estimate `τ_eff(k) = (p1 − p0)/(1 − p0)` and `k·τ_eff(k)`. The filler slot avoids counting the loss of a correct note as transmission. The normalized risk contrast is a net effect; its independent-hazard interpretation is conditional on the background assumption from the original precheck. The CPU result kills the proposal if all pointwise paired 95% upper confidence bounds for `k·τ_eff(k)` are below 0.5. Stage 1 is worth funding only if at least one interval includes a value at or above 0.5. This is a headroom screen, not evidence that `R` crosses 1.

**Dose fit and controls.** In the filler background, model the defect-free fraction as `(1 − p_j)/(1 − p_0) = (1 − τ(k))^j` for j in {0, 1, k}; fit the slope through zero by unweighted least squares on the log survivor ratio. Report the fitted per-defect `τ(k)`, direct one-bad filler-background contrast, saturation deviation at k, and all-sound / mixed / all-bad risks. Report planted-signature risks to distinguish the inherited bug from other errors. Match a no-note temperature separately at each k to the one-bad mostly-sound policy on source tasks only and report it as a diagnostic, not a substitute for the same-length causal contrast.

Use exact stochastic marginalization, paired family bootstrap with the same 10,000 draws at each k, and refit nuisance temperatures and dose slopes per draw. No prompt or endpoint selection based on observed outcomes. The test is conditional on this model, the deliberately repeated rule, and the constrained coding stream.
