# Reversible training: making forgetting optional by running learning backward

Parent: the ledger's kills of the **Landauer erasure budget** (counting erased bits says nothing about accessibility) and of **return-point adapters** (saved states make exactness a save/restore stack), plus the flood seeds that already name the obvious moves: *reversible optimizer and selective rewind* and the *Crooks irreversibility meter* ([PR #44](https://github.com/manojbajaj95/cl/pull/44), `ideas/flood/physics-math.md`), *undo log of opcodes* and *time-reversal symmetric training* ([PR #42](https://github.com/manojbajaj95/cl/pull/42)), *seed-log autobiography with bisect, blame and exact undo* ([PR #36](https://github.com/manojbajaj95/cl/pull/36)) and *reversible training instruction* ([PR #114](https://github.com/manojbajaj95/cl/pull/114)). Prior art on exact unlearning by subtraction or sufficient statistics ([2505.12239](https://arxiv.org/abs/2505.12239), [2610.07197](https://arxiv.org/abs/2610.07197)), recorded-trajectory deletion ([2508.12220](https://arxiv.org/abs/2508.12220)), LoRA rollback by routing ([2603.11239](https://arxiv.org/abs/2603.11239)), Lie-bracket order prediction ([2606.24993](https://arxiv.org/abs/2606.24993), [2611.20087](https://arxiv.org/abs/2611.20087)) and symplectic learning units ([2603.01768](https://arxiv.org/abs/2603.01768)) is taken as given. Bit-exact reversible SGD is Maclaurin et al. 2015 (hyperparameter gradients), not ours.

**Node question.** Not "can a model state be restored" (true by construction, killed) and not "is this edit equivalent to that one" (the edit-equivalence cluster). The question is about the *learning program*: if every training step is an invertible computation, information is never destroyed, so forgetting is a choice about what to erase and when. What does that choice cost (tape, data, compute), which undo operations are cheap, and can the preserved information be turned into retention that is accessible without rewinding?

**Short answer from the CPU probe below.** (1) Exact reversal is real and cheap in tape: fixed-point heavy-ball SGD rewinds A→B→C back to θ_A **bit for bit in 10/10 worlds**, and the entropy-optimal remainder tape costs log₂(1/β) bits per parameter-step (0.152 at β = 0.9), the same as one fp32 (w, v) checkpoint every **421 steps, independent of model size**. (2) The tape is not the bill. Reversal recomputes gradients, so it needs every minibatch: the batch-index tape alone (259,200 bits) is 16× the remainder tape, and the data itself must be kept. Today's reversible training makes forgetting optional only for a learner that never deletes its data. (3) Undo is a stack. Removing B while keeping C exactly costs 2|C| + |B| steps (reverse C, reverse B, replay C); task-vector negation lands barely closer to the counterfactual θ_AC than doing nothing (relative distance 2.02 vs 2.04) while wrecking C (loss 0.43 vs 0.003); out-of-order gradient ascent on B's logged batches diverges (losses ~10³). (4) Reversibility buys recoverability, not retention. Undoing B exactly gives θ_AC, whose A loss is 0.286 against 0.0095 at θ_A, because C also overwrites A. And at matched effective step, a 70× lower erasure rate (β 0.5 → 0.99) leaves A loss after B at 0.565 / 0.567 / 0.533: how *much* the optimizer erases does not set what is retained, which re-confirms the Landauer kill from the reversible side.

So the open frontier is three problems: **reverse without data**, **undo out of order**, and **make preserved information accessible without rewinding**. The ideas below are sorted by which of these they attack, plus a group that changes what "a training step" is.

## Root cause: invertibility moves the forgetting decision, it does not remove it

1. **An invertible step preserves information but needs its inputs to run backward.** The inverse of θ' = θ − ηg(θ, x) must recompute g at the restored θ, so x is part of the inverse. Reversible SGD therefore converts weight-forgetting into a data-retention obligation. Any "data-free" reversal must replace x with something that regenerates the gradient (a gradient oracle, a generator, or a parameterization where the step is invertible without x).
2. **Inverse maps of contracting dynamics expand.** Forward SGD near a minimum contracts; the exact inverse expands at the same Lyapunov rate. Approximate reversal (lossy tape, proxy gradients, float noise) therefore drifts exponentially. Exactness is binary; a usable approximate reversal needs dynamics near isometry.
3. **Composition is ordered.** B then C is the word C∘B; removing B needs C∘B∘C⁻¹… conjugation, which costs C twice. Cheap out-of-order undo needs segments that commute or a cheap transport of B's effect through C.
4. **Old-task retention is a property of the current state, not of the trajectory.** A tape makes θ_A reachable, not θ_now competent at A. Turning reachability into retention needs computation at inference (rewind, or reversible borrow-and-return) or a training rule that keeps old competence in a register the new task never writes.

### CPU probe ([`tree/probes/reversible_training_probe.py`](probes/reversible_training_probe.py), numpy, ~2 CPU-s)

Host: 2-24-1 tanh MLP (120 params), MSE. Tasks A, B, C: three random tanh teachers on the same inputs (strong interference); A and B get 400 steps, C 100 steps, batch 32, lr 0.05. Optimizer: heavy-ball SGD on int64 fixed point (scale 2²⁴) with β = 9/10: v ← ⌊9v/10⌋ − g, w ← w + ⌊v/20⌋, remainder (9v mod 10) to a tape; reversal recomputes g at the restored w. 10 worlds.

**R1 exact rewind.** C and B run backward from θ_ABC reach θ_A and its velocity bit for bit in 10/10 worlds. Tape for 900 steps: remainders 358,768 bits naive (log₂10 per param-step), 16,416 bits entropy-optimal (log₂(10/9)), batch indices 259,200 bits; one fp32 (w, v) checkpoint 7,680 bits.

**R2 selective undo of B keeping C** (target θ_AC = A then C on the same streams; distance ‖w − θ_AC‖/‖θ_AC − θ_A‖; reference θ_A: L_A 0.0095; θ_AB: L_A 0.638, L_B 0.0013):

| Arm | L_A | L_B | L_C | dist | Cost |
|---|---|---|---|---|---|
| keep (do nothing) | 0.288 | 0.378 | 0.003 | 2.04 | 0 |
| out-of-order gradient ascent on B batches (clipped, no momentum) | 1.7·10³ | 1.8·10³ | 1.7·10³ | 30.0 | \|B\| steps, B data |
| task-vector negation θ − (θ_AB − θ_A) | 0.258 | 1.222 | 0.426 | 2.02 | θ_A, θ_AB stored |
| exact reverse C, reverse B, replay C | 0.286 | 0.379 | 0.003 | **0.000** | 2\|C\| + \|B\| steps, B + C data, tape |

**R3 friction sweep** (float SGD, matched lr/(1−β) = 0.5): A loss after A→B is 0.565 (β 0.5, 1.0 bit/param-step of erasure), 0.567 (β 0.9, 0.152 bits), 0.533 (β 0.99, 0.014 bits, but A was learned less: L_A after A 0.006 vs 0.001).

Caveats: one tiny host, interference so strong that C erases B functionally (L_B for keep ≈ exact), so R2 says nothing about cases where B survives C; ascent is the naive version.

## Ideas

Each idea: mechanism, why it is new against the ledger and prior art, the cheapest first test, and the old-task retention check. **P** = primitive (a new object or operation), **I** = improvement of an existing method. The same-budget control is named in the test.

### A. Reverse without the data (garbage-free learning)

**1. Catalytic learning: borrow the old task's weights as workspace and return them bit-exact (P).**
*Mechanism.* Catalytic-space computation (a full memory that may be used only if returned to its exact initial contents) applied to CL. The old network's trunk W_A is the catalytic tape; a small clean register R (head, low-rank slot) is the only durable write. Learning B: reversibly transform W_A by a sequence of invertible, data-conditioned couplings (W ← W + f(R, x)), train R against the transformed trunk, then uncompute the couplings in reverse. At inference on B, rerun the couplings forward (they depend only on R and a fixed seed, not on data), predict, run them back.
*Novelty.* Every rollback idea in the ledger keeps either a saved state or the data. Here old weights are bit-identical at all times outside an inference call by construction, and the scientific question is the new one: how much B competence fits in |R| bits when the borrowed W_A is the compute substrate. No CL work uses catalytic computation.
*Cheapest test.* Probe host: A trained, then B with R = output layer (25 params) + 8 coupling seeds, vs control "train only the head on frozen W_A" (same |R|) and vs "fine-tune all" (same steps).
*Retention check.* θ_A hash identical after every B step; L_A at θ_A unchanged by construction, so the measured quantity is L_B at matched |R| against the frozen-trunk control. Kill if no gain over frozen trunk.

**2. Compute–copy–uncompute training (Bennett for SGD) (P).**
*Mechanism.* Train task B in a scratch copy with exact reversible SGD, copy a compressed result (a k-bit quantized low-rank delta, or a distilled head) into the durable weights with a CNOT-style XOR/additive write, then run the scratch training backward to consume its own tape. Net garbage zero; the durable state changes only by the copied bits.
*Novelty.* The undo log (PR #42) keeps the log; this consumes it. Interference becomes an explicit, measurable channel (the copy), so "how many bits of B can enter without moving A" is a defined quantity rather than a Landauer count.
*Cheapest test.* Copy rank-1/2/4 deltas of B's scratch solution; plot L_B vs copied bits. Control: train a rank-matched LoRA directly on B for the same steps.
*Retention check.* L_A after copy vs after rank-matched LoRA; a win must hold A while matching L_B.

**3. Gradient-oracle reversal (P).**
*Mechanism.* While training B, fit a small oracle ĝ_B(θ) (e.g. a linear map on a sketch of θ, or a generator of B-like inputs) so the reverse pass recomputes gradients without B data. Pair with the exact remainder tape.
*Novelty.* Turns root cause 1 into an object: reversal fidelity as a function of oracle fidelity. Recorded-trajectory deletion (2508.12220) keeps data/checkpoints.
*Cheapest test.* Probe: replace B's gradient in R1's reverse pass with a generator-sampled batch; measure ‖θ_rev − θ_A‖ vs oracle size. Control: storing a checkpoint at θ_A with the oracle's bit budget.
*Retention check.* L_A at the approximately reversed state vs the matched-bits checkpoint and vs keep.

**4. Near-isometric optimizers for approximate reversal (I→P).**
*Mechanism.* Exact inverses of contracting maps expand (root cause 2). Use dynamics close to volume-preserving (β → 1 with a tiny explicit dissipator, symplectic leapfrog with a learned energy) so lossy reversal (low-precision tape, proxy gradients from idea 3) has a small backward Lyapunov exponent.
*Novelty.* CHLU (2603.01768) builds symplectic units for forward modelling; nobody treats the backward Lyapunov exponent of the *optimizer* as the quantity that decides whether forgetting is reversible without full storage.
*Cheapest test.* Measure reversal error growth per step for β ∈ {0.5, 0.9, 0.99, leapfrog} with k-bit truncated tape. Control: plain SGD at the same final L_B.
*Retention check.* L_A after approximate reversal at each β; report the β that minimizes it at fixed tape bits.

**5. Counter-based data tape (I).**
*Mechanism.* Replace the batch-index tape (R1: 16× the remainder tape) by a counter-based PRNG keyed on (seed, step); with streaming data, index the stream by hash. Reversal then needs O(1) index bits.
*Novelty.* Small, but it is the dominant measured cost and unaddressed in the flood seeds.
*Cheapest test.* Rerun R1 with Philox indices; tape bits drop to remainders only.
*Retention check.* Bit-exact rewind still reaches θ_A (same check as R1).

**6. Predictive remainder coding and a tape scaling law (I).**
*Mechanism.* Remainders are deterministic given full-precision v, but low bits of v are near-uniform. Fit a context model p(r | low bits of v, sign g) and arithmetic-code the tape; measure bits/param-step vs model width, β and lr.
*Novelty.* Gives the first scaling law for the price of "optional forgetting". R1 says the floor is log₂(1/β) independent of width, so the claim to test is that real tapes come in below that floor through structure.
*Cheapest test.* Coded size vs log₂(d/n) bound on the probe at widths 8–128.
*Retention check.* Decoded tape still rewinds bit-exactly to θ_A.

**7. Pebbled rewind of the training timeline (I).**
*Mechanism.* Bennett's pebble game: checkpoint hierarchically and re-run segments so any step is reachable with O(T^ε) storage and O(T^{1+ε}) compute; mix with the remainder tape inside segments.
*Novelty.* Pebbling is used for backprop memory, not for making a CL learner's past reachable; it gives the storage–compute frontier for "forgetting horizon".
*Cheapest test.* Simulate the bit/compute cost of rewinding to any of K task boundaries for tape-only, checkpoint-only and pebbled schedules.
*Retention check.* L_A at the reached θ_A for each schedule (exact for all; the result is the cost frontier).

### B. Undo out of order

**8. Trajectory transport of an undo vector (P).**
*Mechanism.* Removing B from A→B→C exactly is conjugation (cost 2|C| + |B|). Approximate it by transporting B's displacement through C's recorded steps with Jacobian–vector products: δ_C = ∏(I − ηH_t)·(θ_AB − θ_A), then θ ← θ_ABC − δ_C. Cost one JVP per C step, no B data.
*Novelty.* Negation (the strongest cheap control, which R2 shows misses badly) ignores that C moved the frame. Lie-bracket papers predict order effects; none transport an undo through a recorded path.
*Cheapest test.* Add the transported arm to R2. Controls: negation and exact conjugation.
*Retention check.* L_A and L_C at the transported state vs both controls; distance to θ_AC.

**9. Commuting-segment training (P).**
*Mechanism.* Constrain each task's updates so segments commute up to O(η³): project B and C gradients so their BCH bracket term [g_B, g_C] is cancelled by a small counter-step logged at each boundary. Undo of any segment is then its own inverse applied anywhere.
*Novelty.* Uses the bracket as a *training constraint that buys O(1) out-of-order undo*, not as an order predictor (2606.24993, 2611.20087). Differs from group-restricted updates (PR #42) because the group is not fixed in advance.
*Cheapest test.* Probe: bracket-cancelled A→B→C, then reverse B out of order with its tape; distance to θ_AC vs R2's exact arm.
*Retention check.* L_A, L_C after out-of-order undo vs exact conjugation and vs plain training at equal steps.

**10. Remainder-mismatch conflict detector (P).**
*Mechanism.* Running B's reverse steps out of order with B's remainder tape fails the divisibility check ((v + g)·d + r ≡ 0 mod n) wherever the state differs from what B left. The failure map is a free per-parameter, per-step test of "C touched what B wrote".
*Novelty.* A conflict detector that falls out of exact arithmetic, with no extra storage. Caveat: it fires with probability (n−1)/n on any difference, so it detects change, not harm; the test is whether its *spatial* map predicts interference.
*Cheapest test.* Correlate failure density per unit with the drop in L_B attributable to that unit (ablation).
*Retention check.* Use the map to freeze or protect high-conflict units during C; L_A, L_B vs random freezing of equal size.

**11. Write-dependency DAG with additive couplings (P).**
*Mechanism.* Parameterize weights as a stack of additive coupling writes w ← w + f_k(earlier writes), where each task's write may condition only on writes it names. Undo cost of task B = its descendant set; any task with no descendants is removable in O(1), exactly, out of order.
*Novelty.* Makes forgetting optional per task by architecture, not by stored states; the research object is the DAG density that a learner needs to keep competence.
*Cheapest test.* Three tasks; compare a chain DAG, a star DAG (each write conditions only on the root) and full fine-tuning on L at equal steps.
*Retention check.* After removing B in the star DAG, L_A and L_C vs their values before B was learned.

**12. Taint tracking of training information flow (P).**
*Mechanism.* Information-flow taint (security) for SGD: each parameter carries a bitmask of tasks whose gradients wrote into it since the last exact checkpoint; masks propagate through the forward pass into gradients. Undo scope of task B is its taint set.
*Novelty.* A new forgetting-dynamics observable: how fast one task taints the whole network (taint percolation time), comparable across optimizers and architectures.
*Cheapest test.* Measure taint coverage vs steps for SGD, Adam, and the DAG of idea 11.
*Retention check.* Restore only B-tainted params (from tape) while keeping the rest; L_A, L_C vs full conjugation.

**13. Training rebase (P).**
*Mechanism.* git rebase for learning: rewind branch B to the fork, replay it on top of branch C, with conflict regions from idea 10. Exact when the tape is complete, approximate with idea 8.
*Novelty.* The seed-log autobiography (PR #36) gives bisect, blame and undo; rebase (moving a whole branch onto another without merging weights) is not there and is different from weight merging.
*Cheapest test.* Two branches from θ_A; rebase B onto C vs weight averaging vs task-arithmetic merge at equal compute.
*Retention check.* L_A, L_B, L_C at the rebased state vs the merges.

**14. Single-batch exact excision (I).**
*Mechanism.* R1 shows the payoff of a tape over checkpoints is granularity, not depth (same bits as one checkpoint per 421 steps). Use it to excise one contaminated or mislabelled minibatch at step t exactly: rewind to t, replay from t+1 skipping it.
*Novelty.* Exact unlearning papers delete samples by subtraction or retraining from a checkpoint; this is exact at single-step granularity with cost T − t steps and no checkpoint.
*Cheapest test.* Insert one adversarial batch in task A; excise it at the end of C. Control: retraining from the nearest checkpoint at equal bits (stride 421).
*Retention check.* L_A, L_C after excision vs the checkpoint control.

### C. Make preserved information accessible without rewinding

**15. Garbage attribution (P, aimed at the Landauer kill).**
*Mechanism.* Instead of counting erased bits, ask which task's information they carry: zero or randomize slices of the remainder tape and measure the error in θ_A after reversal, per task and per layer. The map says where SGD dumps task-A information while learning B.
*Novelty.* The ledger killed counting; this measures accessibility-relevant content of the erased stream, which is the gap the kill named.
*Cheapest test.* Probe: perturb tape slices from B's segment by layer; report ΔL_A after rewind.
*Retention check.* Protect the top-attributed layer during B (lower lr there); L_A after B vs protecting a random layer.

**16. Where-to-dissipate allocation (P).**
*Mechanism.* R3: how much the optimizer erases does not set retention. Test where: run nearly frictionless (β → 1) reversible dynamics everywhere, with a single explicit dissipation channel whose direction is chosen (low old-task curvature, random, or high curvature).
*Novelty.* Converts the Landauer framing into an allocation question with a falsifier: if dissipation direction does not matter either, the thermodynamic route to CL retention is dead.
*Cheapest test.* Probe host, three dissipation directions at equal dissipated energy.
*Retention check.* L_A after B for each direction vs plain SGD at equal steps.

**17. Inference-time rewind depth as a latent (P, with the save/restore warning).**
*Mechanism.* Predict for each input how far to rewind (lazy, computed only for that input with idea 7's pebbles) and evaluate at that state.
*Novelty.* Over the killed return-point adapters, the claim is not exactness but that a learned rewind-depth predictor matches a mixture of K stored checkpoints at a fraction of the bits. Kill if it does not beat that matched-bits control.
*Cheapest test.* Rewind-depth classifier on mixed A/B/C inputs vs K checkpoints with a task classifier, at equal stored bits.
*Retention check.* Accuracy on A inputs at the selected depth vs the checkpoint mixture.

**18. Reversible thermostat (I).**
*Mechanism.* Nosé–Hoover-style deterministic, reversible noise (counter-based PRNG plus an auxiliary heat variable) so stochastic exploration is reversible; sample the basin around θ_A during B without losing the way back.
*Novelty.* SGLD/SGD noise is the main source of irreversibility in practice; making it reversible lets a CL learner explore and still rewind.
*Cheapest test.* Rewind exactness and final L_B with thermostat vs plain noisy SGD.
*Retention check.* L_A at the rewound point and the spread of L_A over the explored basin.

**19. Invertible learned optimizer (P).**
*Mechanism.* Meta-learn an update rule as an additive coupling network u = f(g, state), so each step is invertible with no tape beyond the coupling inputs; meta-objective: low interference at fixed invertibility.
*Novelty.* Learned optimizers are not invertible; enforcing it makes undo free while learning which updates interfere less.
*Cheapest test.* Meta-train on 2-task sequences of the probe family; test on new triples.
*Retention check.* L_A after B under the learned invertible rule vs Adam and vs EWC at equal steps.

### D. Change what a training step is

**20. Learning by permutation (P).**
*Mechanism.* Weights are a fixed multiset; a step only swaps positions (sort-based, accept a swap if it lowers the minibatch loss). Each step is a permutation, so nothing is erased; forgetting is impossible information-theoretically and becomes a question of accessibility only.
*Novelty.* Isolates the claim that forgetting is erasure: if a permutation learner still forgets A in function, CL forgetting is about accessibility, not information loss, with no optimizer details in the way.
*Cheapest test.* Probe host with weights drawn once, trained by greedy swaps on A then B.
*Retention check.* L_A after B; and reversibility by inverse swap list.

**21. Second-order reversible cellular-automaton learner (P).**
*Mechanism.* State (weights, activations) evolves by a local second-order rule s_{t+1} = F(s_t) − s_{t−1} (Fredkin's construction), which is reversible for any F; learning signals enter as boundary inputs. Old states are recovered by running the rule backward.
*Novelty.* Reversible by form for any local learning rule, no tape. The question is whether any F learns at all.
*Cheapest test.* 1-D CA learner on a 2-task toy classification; does it learn, and does backward evolution recover task-A accuracy?
*Retention check.* Task-A accuracy at the current state and after backward evolution to the A boundary.

**22. Tape as error-correcting code (P).**
*Mechanism.* The tape plus a replay is a redundant description of θ. If a few weights are corrupted or overwritten, rewinding and replaying detects the mismatch (divisibility failures) and reconstructs them: a self-healing learner.
*Novelty.* Reframes the tape as parity against forgetting from damage (pruning, quantization, bit flips) rather than as undo.
*Cheapest test.* Corrupt 5% of θ_ABC; reconstruct via rewind-and-replay; compare with storing parity at equal bits.
*Retention check.* L_A, L_B, L_C after reconstruction vs corrupted state.

**23. Uncomputed scaffolds (P).**
*Mechanism.* Learn an auxiliary task S (a scaffold that helps C) in scratch weights, learn C with S present, then uncompute S's training exactly while keeping C. Tests whether help from a temporary skill can be kept after the skill is gone.
*Novelty.* Curriculum and auxiliary-task work keeps the auxiliary or forgets it by drift; exact uncomputation separates "C needed S during training" from "C needs S at test".
*Cheapest test.* S = a related teacher; measure L_C after uncomputing S vs never-learned-S at equal steps.
*Retention check.* L_A throughout, and L_S after uncompute (should equal pre-S).

## Ranked deeper sub-questions

1. **Catalytic learning (ideas 1, 2).** How much new-task competence fits in a clean register of |R| bits when an old network is borrowed and returned bit-exact, against a frozen-trunk head at the same |R|? This is the only route here where old-task retention is exact without stored data or states, so it decides whether "optional forgetting" can be free.
2. **Data-free reversal (ideas 3, 4).** What is the backward Lyapunov exponent of practical optimizers, and can near-isometric dynamics plus a gradient oracle reverse a task with error below a matched-bits checkpoint? R1 shows the data, not the tape, is today's bill.
3. **Cheap out-of-order undo (ideas 8, 9, 10).** Does trajectory transport or bracket-cancelled training beat negation (which R2 shows lands no closer than doing nothing) at < 2|C| steps? Run on a host where B survives C, which the probe lacked.
4. **Where, not how much (ideas 15, 16).** Does the location of erasure predict retention when its amount does not (R3)? A negative answer closes the thermodynamic route.
5. **Permutation learner (idea 20).** Does a learner that cannot erase still forget in function? This separates information loss from accessibility loss for the whole node.
