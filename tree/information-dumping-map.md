# Information-dumping map: where SGD loses access to old tasks

**Parent:** [Reversible training](reversible-training.md) ([PR #131](https://github.com/manojbajaj95/cl/pull/131)), especially ideas 15 (garbage attribution) and 16 (where to dissipate). **Status:** research ideas; no new experimental results. Proposed first tests are CPU-scale.

**Question.** When a learner goes from A to B, where along the update does a distinction needed for A stop being usable, and can we choose a different direction to discard without slowing B? The parent found similar A loss after B despite a roughly 70-fold change in the idealized remainder-tape rate. That does not show that discarded information is irrelevant, or that a remainder bit is a unit of skill. It makes **where** and **what can still be read** better questions than how many bits are erased.

## Map: follow an old-task distinction, not weight drift

Start from paired A-trained states whose A behaviors differ by a known amount, then train both on the *same* B minibatches and randomness. Use either real A variants or, for calibration only, a planted perturbation with known response. Rank channels by their effect on A behavior, not by the norm of the parameter change or by whether they decode an arbitrary history label. At three cuts—before the B step, after the optimizer-state update, and after the weight update—ask what a fixed-budget reader can recover from the available state. Report both recoverability under the named reader and retention by the live model. Neither implies the other.

| Where to look | Intervention and signature | Alternative to rule out |
|---|---|---|
| **Live weights: B overwrites or masks A** | Track paired A outputs, gradients and exact one-step responses through B. Test whether an equal-budget fixed readout can recover the missing A behavior from frozen B features. | A has no compatible solution with B under the allowed inputs; ordinary old/new tangent-kernel interference explains the drop; recovery is just relearning from labels. |
| **Trajectory: a direction contracts or turns away from the A readout** | For full optimizer state $s=(w,v)$, estimate perturbation transport by paired finite differences or step Jacobian products $D F_{t-1}\cdots D F_0$. Read the surviving difference through the held-out A output Jacobian. Track state separation and A-output separation separately. | A direction can lose A readout overlap without shrinking; another can shrink without affecting A. Singular values depend on coordinates and on how $w$ and $v$ are scaled. |
| **Optimizer slots: the next update loses a distinction the forward pass did not need** | Reset or swap velocity between matched weights, then run the same B future. Inspect A behavior after the next update and later, and measure what the slot swap does to B. | Zeroing momentum changes effective step size; a slot trace may predict future dynamics without affecting old-task service. |
| **Arithmetic: rounding, clipping, or reset makes an actual many-to-one write** | In fixed point, find two admissible inputs with the same post-operation state and different A consequences. Compare a high-precision or exact-with-side-state branch, then ablate just the side state. | An invertible but contracting real-valued map can hide A at finite resolution; ordinary gradient interference can occur even when no residue is erased. No collision observed is not proof of invertibility. |
| **External state: tape or inputs make A recoverable only with help** | Compare terminal state alone, state with B batch access, state with tape, and state with both. Contrast a tape with a same-byte checkpoint or A sketch. | The B batch log is side information, not discarded A payload; exact rewind with all inputs is by construction. A failure of one reader is not a proof of absence. |

Use a shared-input conflict case to stress the assay, but measure simultaneous retention on a compatible A/B pair (e.g. shared features plus distinct, observable input contexts, with no supplied task ID) and include an untouched old task C. Report the offline joint-fit ceiling. In an intentionally incompatible cell, report recoverability separately rather than treating failure to fit both labels for one input as an optimizer defect.

### A tape-damage assay that does not confuse bad decoding with lost skill

1. **Calibrate exact rewind.** Reuse the parent's [fixed-point heavy-ball host](probes/reversible_training_probe.py), with identical B batches and deterministic gradients. Check recovery of both weights and velocity; add a zero-damage and a no-training control. Start with a diagonal quadratic (known fast and slow modes), then use a compatible tanh MLP pair and a deliberately interfering pair. Use a high-precision twin to separate finite-resolution loss from contraction or masking.
2. **Damage local windows in two distinct ways.** First test real many-to-one events, holding the immediate post-operation state fixed. For the parent's update, if $q=\lfloor nv/d\rfloor$, a valid remainder for that quotient satisfies $0\le r<d$ and $dq+r$ divisible by $n$. There may be no alternative. If a different valid preimage exists, verify it maps to the same post-step state. The two preimages in this host differ in velocity, not in the weights at that cut: a local forward read cannot show an A-logit difference. Test a declared alternate update on those slots, or measure past A behavior on earlier cuts of consistent trajectories that actually converge to the common post-step state. If no valid earlier prefix is available, stop at the local slot fork. Separately inject a continuous perturbation in the inverse momentum update and propagate with the real-valued inverse; label this a **sensitivity assay**, not an admissible tape edit or recovered bits. Do not bypass the exact decoder's divisibility check and interpret the resulting errors as attribution.
3. **Measure selectivity, not how broken rewind got.** For each layer/time/direction bin report valid-fork coverage, equal-norm injected state error (for the sensitivity arm), resulting state error, and A/B/C function error at a common reference cut where those functions are measured. Match dose, time-to-cut, and inverse amplification (e.g. via finite-difference calibration or stratification); compare random and weight/velocity-magnitude controls, same-A pairs, and function-preserving alignment/rebalancing where supported. Test joint damage to adjacent windows before summing scores. For an information claim, test what tape adds on held-out histories over terminal state and permitted B inputs under a fixed reader budget—not just how hard the inverse fails. Treat old-data/Jacobian use as an oracle unless it is available to the proposed training rule.
4. **Close the causal loop forward.** Pick a channel on development streams. Turn its damping, quantization or reset up in one arm and down in another, routing the displaced budget to a matched alternative; never change two mechanisms silently. Test whether the predicted A effect follows the destination on new streams at comparable B performance, not simply whether corrupted rewind hurts A. Include ordinary SGD and static old-curvature/gradient projection, tune equally, and match update norms where possible. Start with a schedule of orthogonal projectors $P_t$ frozen before each held-out rollout, and set $v'=(I-\lambda P_t)v-g_B$ for $0<\lambda<1$. Damping is then a contraction with a real-valued inverse, not an exact erasure. Record damping-only kinetic-energy removal $\tfrac12(2\lambda-\lambda^2)\lVert P_t v\rVert^2$ before applying the gradient. This is bookkeeping, not thermodynamic heat or a bit rate. Sweep doses and compare matched removal and B acquisition; if those cannot both be matched, report the tradeoff rather than equating the arms.

**Decision rule.** Predicting inverse sensitivity alone does not identify a sink. A strong positive is a direction-by-intervention effect on live A retention, held out and beyond curvature, update size and inverse gain, with comparable B learning. A map that only improves reconstruction belongs in rewind engineering; a map that predicts but cannot change retention is a diagnostic.

## Prior-art boundaries and test contract

The [idea ledger](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md) rejects the scalar Landauer budget, Noether storage without finite-step/rebalance controls, exact save/restore, and sparse functional syndromes without sparsity. The plasticity-reserve Gramian did not beat simple predictors; do not substitute a Gramian score for a forward intervention. [Function-matched twins (PR #123)](https://github.com/manojbajaj95/cl/pull/123) and [differential fork registers (PR #114)](https://github.com/manojbajaj95/cl/pull/114) require same-input logits, initial gradients and exact one-update endpoints as shortcut controls for any claimed multi-step-only trace. Match launch margins when comparing which examples or skills fail first. Do not assume tasks or remainders are sparse.

Nearest anchors: [Maclaurin et al.](https://arxiv.org/abs/1502.03492) already reverse momentum with a residue tape; [EWC](https://arxiv.org/abs/1612.00796), [Synaptic Intelligence](https://arxiv.org/abs/1703.04200), [orthogonal gradient descent](https://arxiv.org/abs/1910.07104) and [constrained full fine-tuning](https://arxiv.org/abs/2504.07097) already protect important directions or constrain updates; [NTK overlap](https://arxiv.org/abs/2010.04003) already explains linearized task interference; [error feedback](https://arxiv.org/abs/1901.09847) already carries compression residuals; [benign relearning](https://arxiv.org/abs/2406.13356) already shows recovery can coexist with apparent forgetting. The proposed differences below are hypotheses, not exhaustive prior-art clearance.

Every test below uses fresh A and C examples and records live loss or accuracy before and after B, at common update counts and at matched B acquisition (report misses). Record average and worst-old-task scores and the lowest transient retention. Rewind/repair scores are a separate diagnostic; when repair is the mechanism, also score normal service *after* the deployed repair without going back to an A checkpoint. Charge all side information, training/read FLOPs and oracle data access. Use paired streams, inspect variation across independent stream seeds, and keep development, A retention and B acquisition splits separate. **P** = proposed primitive (a reusable object/operation); **I** = improvement (the mechanism may be useful but does not on its own establish a new primitive).

## Idea pool

### A. Locate where the distinction went

#### 1. Admissible collision atlas (P)

**Mechanism:** Index true alternative preimages of optimizer writes by the change they cause in old predictions across a local fork. **Novelty rationale:** Maclaurin records the original preimage; this asks whether an alternative legal preimage would lose selectively different old behavior, not whether a decoder crashes. **Cheapest first test:** Enumerate the parent quotient buckets in a two-mode fixed-point model; compare with same-gain continuous inverse perturbations and same-A forks. **Old-task retention check:** In a compatible A/B MLP, keep higher precision only in implicated buckets during B; compare live A/C with uniform precision at equal bytes and matched B.

#### 2. Inverse-amplification knockoff tape (P)

**Mechanism:** Pair each damaged window with a different window calibrated to give the same backward state error but different predicted A-output error. **Novelty rationale:** Separates task selectivity from conditioning, which scalar erased-bit counts and naive zeroed-tape ablations cannot. **Cheapest first test:** Calibrate doses in a diagonal quadratic; hold out nonlinear MLP streams where the knockoff should tie on state error but not A-function error. **Old-task retention check:** Protect the selective window's channel versus the knockoff channel forward; compare live A/C at matched B.

#### 3. First-loss cut for an old distinction (P)

**Mechanism:** Instrument each substep with paired A-distinction reads and swaps, then bypass the first suspected bottleneck alone. **Novelty rationale:** NTK overlap predicts function drift from an update; it does not locate which transition drops a distinction from the accessible optimizer state. **Cheapest first test:** In an MLP, plant a weight-channel effect and a velocity effect on different pairs, recover the planted cut, then repeat on ordinary A training with step-size-matched slot resets as control. **Old-task retention check:** Bypass only the identified substep for A-sensitive directions; compare held-out A/C to a sham bypass and compare B latency.

#### 4. Weight/slot/tape substitution matrix (P)

**Mechanism:** Measure a factorial grid of intact/swapped weights and slots, with and without tape and replay inputs, to identify redundant and complementary carriers. Use exact reversal only on consistent triples; on hybrids, test forward behavior or bounded readers. **Novelty rationale:** Relearning and rewind each measure one read path; the matrix asks which channels can replace one another without storing a whole checkpoint. **Cheapest first test:** Swap states between aligned MLP pairs with matched A-adjacent outputs; compare to independent same-history swaps and simple logits/one-update readers. **Old-task retention check:** Restore only one budgeted carrier after B, then test normal A/C service before and after more B; compare with an equal-byte snapshot delta.

#### 5. Transported old-output footprint (P)

**Mechanism:** Push old-sensitive state perturbations through short B windows and pull held-out old-output probes back through the same windows; track when these directions rotate away from each other. **Novelty rationale:** A causal time-varying read/write map, not the killed static plasticity-reserve Gramian or a launch NTK score. **Cheapest first test:** In a tanh MLP, rank equal-norm interventions by transported readout, frozen NTK, Fisher and exact short rollout at the same compute; test across unseen B orders. **Old-task retention check:** Reroute B damping away from the top-ranked transported modes; test live A/C over B and after a delayed recurrence.

#### 6. Tape-only conditional read (P)

**Mechanism:** Fit a fixed reader for old A output residuals from a tape sketch conditional on the terminal state and B batch transcript; test incremental prediction when exact inverse is out of budget. **Novelty rationale:** A read-budget test for accessible A payload, not tape entropy or a history-label classifier. **Cheapest first test:** Across held-out toy histories, compare terminal/B-only, true, within-dose shuffled tape, and equal-byte checkpoint sketches; include the twins shortcut baseline. **Old-task retention check:** Use the read to repair the live model under a fixed update budget and check A/C and B on new data versus replay-based repair.

### B. Choose directions to discard

#### 7. Rotating friction valve (P)

**Mechanism:** Rotate the damped velocity subspace as B progresses, routing dissipation into directions whose transported A readout is weak. **Novelty rationale:** Keep the B gradient unchanged at the damping substep; test dynamic contraction placement beyond static OGD or freezing. **Cheapest first test:** Use a rotating quadratic for calibration and a tanh MLP for the claim; compare transported, instantaneous-curvature, randomized and fixed valves over matched damping-dose/B-progress curves. **Old-task retention check:** Compare live A/C at common B progress and check for delayed A loss after the valve returns to uniform damping.

#### 8. Take turns discarding across old tasks (P)

**Mechanism:** Maintain per-task retention budgets and alternate damping destinations according to which old task has slack; the writable direction changes with current readout, not fixed task ownership. **Novelty rationale:** A controller for the discarded component rather than average Fisher importance or replay frequency. **Cheapest first test:** Fit two old toy skills with uneven overlap, then compare time-sharing to damping defined by average Fisher, worst-task replay and a fixed mixture with the same mean damping. **Old-task retention check:** Require better worst-task A/C without transient floor violations at matched B; an average-only gain fails.

#### 9. Momentum shadow channel (P)

**Mechanism:** Split velocity into live and shadow components; put an old-sensitive component in a bounded shadow register and feed it back only where it alters subsequent harmful B writes. **Novelty rationale:** A protected optimizer-state pathway, not a frozen forward adapter or just saving the whole momentum vector. **Cheapest first test:** In a small MLP compare against same-byte EMA momentum, error feedback, and a same-rank forward adapter; swap shadows while holding live weights fixed. **Old-task retention check:** Measure live A/C after B and following a long B continuation, with no shadow read at inference; match B progress.

#### 10. Writable-subspace exchange (P)

**Mechanism:** When a direction scheduled for coarse rounding becomes A-sensitive, apply a reversible block rotation in velocity space that exchanges it with a currently redundant direction before rounding; convert back before the weight update. **Novelty rationale:** Exchange what physical precision can destroy rather than constrain the full gradient or store roundoff. **Cheapest first test:** Two-block fixed-point SGD with shifting redundancy; compare to equal-byte static mixed precision, error feedback and random rotations; charge rotations. **Old-task retention check:** Measure live A/C on shifted inputs at equal B and bytes; verify the advantage disappears when both blocks use high precision if rounding is the mechanism.

#### 11. Old-null today, readable tomorrow (P)

**Mechanism:** Exempt directions with zero immediate A-output effect from damping only if they feed back into A under a short B rollout. **Novelty rationale:** Dynamic-only protection must beat frozen NTK, initial gradients and exact one-step response, not rediscover a first-order shortcut. **Cheapest first test:** Use matched MLP copies, compare two-to-four-step selection to rank/compute-matched repeated OGD and one-step selection; verify held-out multi-step gain. **Old-task retention check:** Compare live A/C curves through the rest of B and after shared mixing, not just at the selection horizon.

#### 12. State-dependent minimum-loss reset (I)

**Mechanism:** If a slot budget forces periodic hard resets, pick the component to zero from short counterfactuals; charge the fork and optionally distill a cheaper selector only if the oracle has headroom. **Novelty rationale:** A drop policy for irreversible optimizer writes, not a new consolidation loss; must beat generic readiness and gradient-magnitude criteria. **Cheapest first test:** Scan a few rank-matched velocity resets on a CPU MLP; compare direct replay and random/curvature reset at the same budget. **Old-task retention check:** Track live A/C after repeated resets at equal B acquisition, including the worst drop immediately after any reset.

### C. Use a measured sink for bounded repair

#### 13. Old-task parity across exits (P)

**Mechanism:** Encode a bounded old-output correction in a small parity sketch across two channels only where the map predicts complementary, rather than shared, losses. **Novelty rationale:** Targets independence of mapped channel failures, not the ledger's killed assumption that forgotten facts are sparse. **Cheapest first test:** On a two-block MLP, damage channels alone and together; compare dense random sketches, separate uncoded sketches and same-byte replay. **Old-task retention check:** After a single failure, deploy the decoded correction and compare live A/C at matched B; joint failures are a separate measured limit.

#### 14. Residue-to-repair compiler (P)

**Mechanism:** Decode selected optimizer residues into low-rank corrective weights without rewinding; learn the decoder across training histories, then use it only when the mapped damage signature appears. **Novelty rationale:** A bounded tape-to-function operation, not an undo stack, raw error feedback, or assuming any residual encodes a skill. **Cheapest first test:** Fit a linear decoder first on toy A→B histories; compare shuffled-tape, terminal-only, replay and stored-weight-delta decoders at equal bytes and training access. **Old-task retention check:** Apply the correction only to the B model; test held-out A/C plus B before and after further B updates.

#### 15. Damage-indexed replay (I)

**Mechanism:** Choose A examples by their ability to repair measured loss at a particular sink, not by how much A loss they already show. **Novelty rationale:** Must add signal beyond GradMatch and direct loss/margin prioritization; replay itself is not new. **Cheapest first test:** In a toy classifier match examples on A margin and gradient norm, pick different groups according to a slot/rounding intervention, and compare to same-count GradMatch and uniform replay. **Old-task retention check:** Require a gain on disjoint A examples, with C and B guardrails, and a rank reversal when the destination changes.

#### 16. Cross-task borrow-back (P)

**Mechanism:** If the map shows that a partly inaccessible A distinction survives in a B-used feature, fit a tiny readout from that feature into the A output while leaving the shared feature intact. **Novelty rationale:** A sink-localized reuse operation must beat an unconstrained readout of the same size, not just demonstrate benign relearning. **Cheapest first test:** In a compatible two-context MLP, swap equal-norm feature blocks and test whether only the nominated block transfers A predictive value; compare with PCA and random blocks. **Old-task retention check:** Fit with a fixed A calibration budget, test ordinary mixed A/B/C inputs without task ID, and count the readout cost.

#### 17. Catch-and-release quantization error (P)

**Mechanism:** Store the component of quantization error predicted to remain harmful after B, and release it selectively into a later update where it no longer conflicts with B. **Novelty rationale:** Relative to full/low-rank error feedback, the distinguishing claim is a timing-by-direction interaction, not a smaller buffer alone (the functional sigma-delta kill). **Cheapest first test:** Quantized two-task MLP, cross mapped/random capture with mapped/immediate release; compare same-byte error feedback and dense feedback as a ceiling. **Old-task retention check:** Compare live A/C both before and after release and after B continues; delayed recovery cannot mask a retention floor violation.

#### 18. Local escape from an overwrite basin (P)

**Mechanism:** Use the map to pick a minimal group of neighboring optimizer operations to bypass or reparameterize, then resume B from the edited live state, not a rewound A model. **Novelty rationale:** Target a measured interaction between operations rather than selective task undo or adding the negative task vector. **Cheapest first test:** In a toy MLP, test a two-operation repair after a short B block against each operation alone, additive repair, and budget-matched replay; stop if no interaction survives. **Old-task retention check:** After resumed B, require persistent held-out A/C gains at equal B, not a one-checkpoint recovery.

### D. Test whether the map transfers or fails

#### 19. Map an equivalence class, not a neuron (P)

**Mechanism:** Express candidate sinks by their effects on probe outputs and transport those effects across equivalent parameterizations. **Novelty rationale:** This is a coordinate-invariant intervention target, not a Noether invariant used as a memory register. **Cheapest first test:** Rebalance a ReLU MLP; use a transformed optimizer for an equivalence sanity check, then ordinary SGD as the deliberately non-equivariant arm. Compare to layerwise and Fisher ranking. **Old-task retention check:** Check whether the transported intervention protects live A/C in held-out rebalances at equal B, and distinguish failed transfer from changed SGD dynamics.

#### 20. Map without stored A examples (P)

**Mechanism:** Keep a bounded sketch of A-output responses before B; use it to rank later candidate dissipation maps on public anchors, without retaining old training inputs. **Novelty rationale:** A derivative of the sink map is deployed and tested for transfer; teacher distillation or Fisher sketches alone are occupied. **Cheapest first test:** Toy teachers with anchor coverage varied; compare a random feature sketch, equal-byte Fisher and logits-only distillation on the same anchors, with an old-data oracle ceiling. **Old-task retention check:** Evaluate A/C on fresh examples including locations far from anchors, and ensure B acquisition is not sacrificed.

#### 21. Forecast map expiration (P)

**Mechanism:** Treat a dissipation map as valid only until a new update changes its predicted direction ordering; use cheap changes in transported probes to trigger remapping. **Novelty rationale:** The monitored object is the stability of a specific intervention ranking, not a replay deadline or an abstract Gramian capacity threshold. **Cheapest first test:** On an A→B→D stream with smooth and abrupt D shifts, compare trigger, periodic refresh and direct loss alarms at equal probe/refresh compute; test held-out rank reversals. **Old-task retention check:** Keep A/C service across both new tasks at comparable B/D acquisition, including stale-map failures between refreshes.

#### 22. Sequence-sensitive joint sink (P)

**Mechanism:** Use a factorial ledger of paired window interventions to identify damage that occurs only when two individually harmless writes run in one order. **Novelty rationale:** Order noncommutativity is known; the new target is a localized loss of A observability that licenses moving just one dissipation event, not reordering all of B. **Cheapest first test:** Four single/joint intervention arms in both orders in a toy MLP versus matched direct order rollouts and additive scores. **Old-task retention check:** Move one event to the predicted safer window; check live A/C through training with the B examples and order otherwise unchanged.

#### 23. Cross-optimizer map translation (P)

**Mechanism:** Translate a sink's old-output effect into an intervention on a different optimizer's state, e.g. heavy-ball velocity damping into directional Adam first-moment attenuation. **Novelty rationale:** A portable causal target, not a claim that optimizer choice changes forgetting or that raw tape coordinates should transfer. **Cheapest first test:** Fit the map on heavy-ball runs; compare transferred, random, independently fit and Fisher directions in Adam at the same effective weight-update scale. **Old-task retention check:** Assess live A/C at matched B progress in both optimizers; a transfer that needs the same data/compute as full refitting is not a portability win.

#### 24. Loss that no allowable valve can avoid (P)

**Mechanism:** Construct an oracle frontier over permitted damping destinations and look for a witness direction where all B-improving writes necessarily damage A under the declared budget and local model. **Novelty rationale:** Neither a universal forgetting lower bound nor a scalar capacity predictor; a falsifiable diagnostic for when routing should give way to changing representations or adding storage. **Cheapest first test:** Enumerate rank-one valves in a low-dimensional quadratic, then challenge locally predicted infeasibility in a tiny compatible MLP with longer direct rollouts and replay at the same budget. **Old-task retention check:** Check the live A/C versus B frontier, including a positive control where the oracle must find a retention-preserving arm; keep joint-fit ceiling separate from the local budget.

## Ranked deeper sub-questions

1. **Does the location of dissipation causally set old-task retention?** Start with cards 1, 2 and 7: exact local preimages or gain-matched defects nominate channels; the rotating valve tests those nominations forward. Does this beat static curvature and old-gradient projection at matched B acquisition and damping dose on held-out compatible streams? If not, the parent's proposed allocation mechanism has not cleared its cheapest test.
2. **When is skill actually discarded rather than hidden?** Use cards 3, 4 and 6 to ask what tape adds given terminal state and B inputs, and whether the apparent loss survives forward, gradient and one-update shortcut reads. Distinguish exact local collisions from shrinkage and from bounded-reader failure.
3. **How far does a map generalize before it must be rebuilt?** Cards 5, 19, 21 and 23 separate a moving optimizer-specific sink from a transferable functional target by varying time, parameterization, B order and optimizer. An expensive map that must be rebuilt every update has little value unless a cheap predictor beats remapping.
4. **Can measured side information buy more live service per byte than replay?** Cards 13, 14 and 17 test whether routed or stored residue can help deploy a joint A/B model without rewind, against checkpoint deltas, error feedback and same-byte old examples. A win in inverse reconstruction alone does not count.
5. **What lies outside the scope of direction selection?** Use card 24 to identify cases where even an oracle valve has no headroom under the permitted update and state budget. Separate incompatible objectives, insufficient model capacity, and compatible tasks where the local representation or dynamics need to change.
