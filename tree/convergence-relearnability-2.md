# Convergence: First-Order-Invisible Relearning Patches

Child of [Convergence: Relearnability as Memory](convergence-relearnability.md) ([PR #336]) · 28 idea cards · Ideas only; no training runs

The [reviewer’s score-3 entries][triage] on [PR #6] were **CR01**, a finite-response patch with zero tangent, and **CR20**, sequential evidence with no informative singleton. The reviewer put the parent’s third question ahead of the rest: rule out shortcut readers before building correction interfaces around either idea. [PR #114] lost its hidden-channel claim because raw logits decoded the bits; [PR #123] adds the one-step shortcut check. This child asks what a writer can install that those readers miss, whether another edit leaves it usable, and when a conventional memory is cheaper. It does not propose retrying the affine fork or the killed approaches in the [idea ledger][ledger].

## Two exact witnesses, and what they do not prove

**Finite but tangent-invisible (CR01).** Use $f_{u,z}(x)=ux+zu^2x^2$ with $u=0$ and $z\in\{-1,+1\}$. Both states return zero for every $x$; the parameter Jacobian is $(x,0)$ everywhere on that read surface. Give both the ordinary squared-loss example $(1,1)$; one simultaneous SGD step of size $\eta$ takes both to $u=\eta$, leaving $z$ unchanged. The held-out response at $x=-1$ is $-\eta+z\eta^2$; the linearized response is $-\eta$ in both arms. A directional second derivative recovers $z$, and an exact virtual step followed by one forward evaluation ties the actual step. The example proves separation from first order, **not** from those readers or direct access to $z$.

**Two ordinary updates (CR20).** On input $(a,b,t)$ use $f_{u,v,z}=au+bv+t z u v$ with $u=v=0$ and $z\in\{-1,+1\}$. Feed $L=((1,0,0),1)$ and $R=((0,1,0),1)$ to the same squared-loss SGD. At launch both states have output zero and Jacobian $(a,b,0)$ on every input. Either singleton endpoint agrees on *all* inputs across $z$. After both updates, in either order, the held-out output on $(0,0,1)$ is $z\eta^2$. Repeating just $L$ or $R$ does not unlock it. This is a product, not proof of noncommutative learning: a joint batch summed on the same loss scale gives the same result, and an off-diagonal Hessian query reads $z$. Under uniform $z$ the legal labels are independent of the bit, so a recipient with no correlated state cannot beat chance, even after both steps. The two observations permit the read; they are not themselves Shamir shares.

These are query-only separation fixtures, not examples of successful continual learning. Exact equality follows algebraically; no optimization was run. In any variant where the old examples already have zero update and there is no other update state, there is nothing for vanilla SGD to read. Use real residuals after C, ordinary corrections, or ordinary label noise; never inject a private trigger or payload in the evidence.

## Shared CPU-first contract

- **Name the read surface and budget.** Freeze old queries $Q$ (including feedback inputs and held-out targets), the alphabet of legal ordinary batches $E$, the optimizer and its state, and permitted prefix length. Match launch outputs, per-example parameter gradients, and $J_Q\Delta\theta$; match exact single-batch endpoints for CR20, over *every* legal singleton in finite fixtures. If mixed batches are legal, they count as singletons too. If they are not, report the mixed batch separately as a shortcut at equivalent examples and work. Match optimizer state or reset it; log exposure to residual labels, intermediate gradients, parameters and activations separately. Agreement of sampled readers is not a proof of indistinguishability.
- **Keep the shortcuts stronger than the claim.** Give readers the same feedback, depth-appropriate endpoints or counterfactuals, and budget. Use raw logits, margin/temperature, first gradients and linearization; then sweep step size and equivalent parameterizations, and offer directional Hessians (including mixed directions), pooled and shuffled batches, and exact virtual steps where access permits. An exact simulator of the same update has identical outputs, so no claim of exclusivity against that simulator is possible. Charge state bytes, peak workspace, ordinary observations, forward/backward calls and write/install work. Give replay, compact stored answers, replay with La-MAML, and an ordinary state reader the same accounting, not artificially restricted access.
- **Separate history from generally being easy to train.** Plant an old distinction during A, with B a rare and unrelated old task, then learn C with a different writer. Return with new A evidence that was unseen during installation. Pair with an A-naive but matched recipient, an equally difficult fresh task, scrambled old labels, and a carrier erased with all budgets preserved. For planted distinctions randomize the payload per world independently of held-out evidence. If the evidence or generic plasticity explains the improvement, call it transfer or realignment, not memory.
- **Keep serving old tasks while reading.** In every card retain ordinary A/B slices separate from the relearning target, including old jobs due before the cue; record per-task floors before install, after install, after C, and at every prefix on the live learner. Also score C at equal progress to detect rollback. Count unrecovered targets, failures at deadlines, and the worst old slice; don't average away a prefix violation or rescue it by picking a fork in hindsight.

## Literature check

Targeted Hugging Face Papers searches included higher-order tangent/influence, gradient projection in continual learning, noncommutative optimization, fast adaptation, and relearning. The comparisons in the cards were checked against the linked original arXiv abstracts (via Hugging Face or arXiv) or historical publication records (Crossref). [NTK] establishes the first-order comparison; [Tangent Hierarchy] and [Wide Linearity] already explain higher-order departures, and [Differential Influence] already estimates data influence beyond simple linear approximations. [MAML], [La-MAML] and [ANML] already optimize future adaptation or interference. [Spurious Forgetting] and [Benign Relearning] already show that a loss of performance can be reversible without a new memory primitive. The gaps below are narrow design hypotheses, not priority claims.

## A · CR01: Write into a finite response, not a tangent

### IP01 · An independently addressed curvature write — PRIMITIVE CANDIDATE
- **Mechanism:** Install a coefficient on each of two quadratic response terms. The same enabled parameter moves on both ordinary corrections, but different held-out input features select different curvature coefficients. Write one without changing the other.
- **Nearest prior / gap:** [Tangent Hierarchy] models higher-order training dynamics. Here the object to control is an addressed finite response that can be rewritten independently with identical launch outputs and gradients.
- **Cheapest first test:** Solve the constraints in a two-feature polynomial head. Test every binary write and both write orders; then fit a scalar and a per-coordinate LR baseline over three rates. If they reproduce both signed response changes or Hessian read wins at equal access, narrow the claim to addressability.
- **Old-task retention:** Keep the untouched correction’s held-out response, legacy boundary cases on its support, and rare B correct at every prefix.

### IP02 · A correction with a prescribed blind step size — PRIMITIVE CANDIDATE
- **Mechanism:** Tie response terms to vanish at launch and beyond the selected operational points where the polynomial has roots. In the fixture use $z\,u^2(u-h)$: the same correction must produce opposite effects at steps on either side of $h$ and no effect at $h$.
- **Nearest prior / gap:** [SGD Regularization] explains finite-rate effects using modified dynamics. The proposed write specifies a selective response zero and sign change under a fixed shared optimizer, not an optimal learning rate.
- **Cheapest first test:** Enumerate rational rates around $h$ with mixed target signs. Hold out one rate per side; reject a fit that an LR schedule or matched MAML initialization can reproduce without moving an untargeted head.
- **Old-task retention:** A deadline-critical old slice with small margin must stay above its floor at all rates, including the fastest, not just at the designed zero.

### IP03 · A writer whose first separating derivative is chosen — PRIMITIVE CANDIDATE
- **Mechanism:** Choose the first observable derivative order $d$ by installing a local factor that vanishes to order $d-1$ along legal updates. Compare a monomial with a bounded smooth alternative so the dial need not require extreme step sizes.
- **Nearest prior / gap:** [Tangent Hierarchy] orders corrections; [Wide Linearity] relates Hessian scaling to effective linearity. Neither result makes a writable order useful. The hypothesis is that order can be chosen independently of useful signal under finite precision.
- **Cheapest first test:** For $d=2,3,4$, compare analytic jets, held-out response at calibrated step sizes, and fixed-point roundoff at equal bytes with a compact stored value. Stop if higher order only reduces signal or if rescaling the carrier leaks to lower-order readers.
- **Old-task retention:** Preserve an ordinary low-margin A slice and rare B under the largest legal step required to resolve each order.

### IP04 · A patch that distinguishes paired directions but not their marginals — PRIMITIVE CANDIDATE
- **Mechanism:** Set the diagonal curvature terms equal and vary only a mixed term. Permit ordinary composite minibatches to couple two update directions; write a signed cross-effect on one held-out old subgroup.
- **Nearest prior / gap:** [Differential Influence] approximates nonlinear data influence. The proposed actuator writes a specific mixed interaction while leaving each marginal response intact, not a new estimator of joint influence.
- **Cheapest first test:** Use two orthogonal features and enumerate four signed batch pairs. Compare with independent scalar patches, a joint batch baseline and mixed Hessian polarization. Demote any read claim if the latter wins; require sign extrapolation to unseen batch pairs for the write claim.
- **Old-task retention:** Each individually valid correction must still repair its ordinary old subgroup; a rare unrelated subgroup sharing one direction must stay intact after the composite batch.

### IP05 · A response write with an explicit gauge quotient — PRIMITIVE CANDIDATE
- **Mechanism:** Canonicalize equivalent factorized hosts *before* installing the patch; record the optimizer’s transformation convention. Define the written object by the response pattern that survives canonical relabeling, not by a coefficient norm.
- **Nearest prior / gap:** [Git Re-Basin] aligns permutation-equivalent models for merging; [Net2Net] preserves the function while changing the network. Ask whether a patch can survive quotienting without collapsing to an ordinary effective LR difference.
- **Cheapest first test:** Use a two-unit homogeneous model with permutation and positive rescaling. Compare raw SGD, canonicalized SGD, and tuned per-unit step sizes on a grid; reject if all apparent memory follows unequal effective update scale.
- **Old-task retention:** Preserve the same low-margin A and B slices in every tested representative, both before the write and after ordinary corrections.

### IP06 · A correction that bends back before the next deadline — PRIMITIVE CANDIDATE
- **Mechanism:** Install a factor with a prescribed transient response on the first update and a return to baseline at the endpoint of another ordinary update, without undoing the learning in the other heads.
- **Nearest prior / gap:** [Trajectory Distillation] matches multi-step expert trajectories using synthetic data. Here the data are ordinary and unchanged; the write changes one observable path while leaving the terminal behavior and neighboring outcomes fixed.
- **Cheapest first test:** Solve a small polynomial using the two endpoints of repeated squared-loss updates; hold out a second example path with similar update magnitudes. Compare to an ordinary temporary head and a two-step extension of [Meta-SGD] with learned per-coordinate rates at matched bytes.
- **Old-task retention:** The excursion must not cross the floor of an A job due between updates, even if the final checkpoint restores it; check B throughout.

### IP07 · A locality mask that covers reachable update paths — PRIMITIVE CANDIDATE
- **Mechanism:** Factor the patch by the allowed displacement of the feedback as well as the query feature. Off-scope feedback should have no effect even when its launch gradients overlap the target on the old read surface.
- **Nearest prior / gap:** [Learning Where] learns which weights to change; [OGD] projects to preserve output to first order. The proposed mask bounds which *finite response* an ordinary correction can change, including when first-order scopes coincide.
- **Cheapest first test:** Enumerate on- and off-scope corrections in a four-query nonlinear host, including near-boundary perturbations. Compare learned gradient masks and OGD plus a line search with the same veto budget.
- **Old-task retention:** Hold out near-boundary legacy corrections where locality matters and an out-of-scope old subgroup using the same feature; a false veto counts as retention loss.

## B · CR20: Move the first useful read beyond any singleton

### IP08 · An ordered read outside the pooled gradient span — PRIMITIVE CANDIDATE
- **Mechanism:** Use $f=au+b(v+cuw)+t z v w$ with public $c\ne0$ and $u=v=w=0$. The same $L,R$ as above leave $w=0$ after either singleton, $RL$, or any weighted pooled SGD step. After $L$, however, the $R$ loss gradient moves $w$ to $c\eta^2$; the target on $(0,0,1)$ reads $zc\eta^3$. The extra direction is created by the first update, not an order tag.
- **Nearest prior / gap:** [Conditional Invariance] uses noncommutativity to direct transfer toward a target domain. Here the distinction is a writable, history-dependent response absent at singleton endpoints; order sensitivity itself is not new.
- **Cheapest first test:** Enumerate $L,R,LR,RL$ and legal pooled steps, with a sweep over pooled step size and weighting. Include a reader of the intermediate gradient and any exact virtual two-step read; if rescaling or reweighting matches the read and control outputs, the ordered claim fails.
- **Old-task retention:** Score legacy slices that routinely see the reverse order and those due between the two cues; the wrong order must not silently erase ordinary service.

### IP09 · A threshold in distinct observations rather than step count — PRIMITIVE CANDIDATE
- **Mechanism:** Couple $k$ ordinary feedback coordinates via a product or elementary symmetric polynomial. Repetition of the same coordinate cannot substitute for seeing enough distinct evidence.
- **Nearest prior / gap:** [Shamir] gives a well-defined threshold reconstruction scheme. Here the observations are independent of the history payload; the candidate is a threshold over legal *learning transitions*, not secret sharing or security.
- **Cheapest first test:** For three channels, enumerate all prefixes of length three, plus admissible pooled batches and repeated labels with matched total magnitude. Match an explicit counter and same-byte answer store; stop if the implicit threshold has no cost or retention advantage.
- **Old-task retention:** B’s routine repeated examples must continue to improve B without spuriously unlocking A; check urgent old tasks with fewer than $k$ distinct cues available.

### IP10 · Error-tolerant composition without decoding a singleton — PRIMITIVE CANDIDATE
- **Mechanism:** Build several redundant two-observation paths to the same update; aggregate their signed response contributions so one corrupted ordinary observation cannot flip a majority and no single legal observation can reveal the payload.
- **Nearest prior / gap:** [Shamir] and ordinary redundancy motivate threshold and fault tolerance. The gap is error tolerance on the distribution of ordinary feedback and with unchanged singleton responses, rather than distributing encoded labels.
- **Cheapest first test:** Enumerate substitutions and deletions in a six-observation binary world, with two disjoint observations per path. Compare equally redundant replay, majority-gated cached answers and an endpoint reader under the same corrupted streams.
- **Old-task retention:** Check a rare old task whose errors correlate with a corrupt cue and report systematic two-path failures separately from the single-error guarantee.

### IP11 · A switchback detector for stale evidence — PRIMITIVE CANDIDATE
- **Mechanism:** Install a pair interaction that cancels when two ordinary corrections are inconsistent with the current revision; a reversed correction first drains the old displacement and cannot use it as the first half of a fresh read.
- **Nearest prior / gap:** [Automated CL] learns context-dependent self-updates; [Backpropamine] gates plasticity through learned modulation. The narrower operation is a revision-specific cancellation observable only on composed ordinary updates without a version tag at serve time.
- **Cheapest first test:** Enumerate $L,R$ with both residual signs across two revisions of a tiny task. Compare a versioned two-slot cache and a learned update rule at the same bytes; vary magnitudes so cancellation at a single calibrated point is insufficient.
- **Old-task retention:** Include still-valid old corrections with the same surface form as stale ones, and check their held-out targets and B before and after cancellation.

### IP12 · A response that composes across missing time — PRIMITIVE CANDIDATE
- **Mechanism:** Tie the first partial write to a mode that the typical intervening updates cannot move, but that the second ordinary correction accesses. Treat intermittent unrelated learning as part of the read path, not a pause.
- **Nearest prior / gap:** [ANML] trains for resistance to interference; [Backpropamine] learns how to modulate plastic changes. Here the preserved object is a partial composed read with no useful singleton output, rather than a mastered answer.
- **Cheapest first test:** In a three-head host interleave 0, 1, 4 or 16 C updates between $L$ and $R$, including C directions with deliberately shared support. Compare replay, ANML and an explicit pending-cue buffer of equal total bytes.
- **Old-task retention:** A and rare B must continue working throughout the gap, and C’s gain must remain after the second cue.

### IP13 · A counterexample generator for false singleton blindness — IMPROVEMENT
- **Mechanism:** Enumerate or search legal batches by residual sign, composition and weight, maximizing endpoint distinguishability. Return the smallest ordinary singleton that invalidates a composed-read claim.
- **Nearest prior / gap:** [Angluin] uses distinguishing counterexamples to learn automata. The proposed improvement is a shortcut audit for update interfaces, with a specified legal batch grammar and work budget rather than unrestricted parameter probes.
- **Cheapest first test:** Plant a product channel and a version with one mixed-batch loophole. Compare exact enumeration and fixed-budget randomized held-out batches on time to detect leakage. Report uncovered legal batches for any search-only claim.
- **Old-task retention:** Run discovered counterexamples as legal live updates and score old A/B; label a leak that requires violating the contract separately from one that works in normal service.

### IP14 · A lower bound on the prefix that can read — IMPROVEMENT
- **Mechanism:** Prove equivalence to depth $k$ by propagating the equalities preserved by each legal update; retain the shortest distinguishing prefix at depth $k+1$ as a witness. Quotient out states with the same future observable traces within the horizon.
- **Nearest prior / gap:** [Angluin] already formalizes finite-state language identification via queries and counterexamples. What could help here is tractable depth certification with derivative/end-point readers included and an ordinary-feedback grammar, not trace equivalence itself.
- **Cheapest first test:** Exhaustively enumerate quantized two-coordinate SGD states and compare partition refinement with brute-force prefixes, checking both produce the same minimum read depth. If the certificate costs more than enumeration at the same coverage, don't build on it.
- **Old-task retention:** Include old answers due at each intermediate depth as observations so a candidate cannot appear equivalent by omitting deadline-sensitive outputs.

## C · Install and preserve the distinction across independent edits

### IP15 · Net growth that adds response degrees of freedom — PRIMITIVE CANDIDATE
- **Mechanism:** Duplicate a nonlinear branch with cancelling values and first derivatives at the cut, then adjust its residual curvature while holding the host and the shared optimizer fixed. Test a normal install without changing task routing.
- **Nearest prior / gap:** [Net2Net] and [Composable Expansions] preserve function under growth. The extra requirement is preserving launch tangents while changing just one finite response, with an independent editor allowed afterward.
- **Cheapest first test:** Split a two-unit MLP with a tied cancellation, install a patch, then learn C in the enlarged shared model. Compare function-preserving growth plus La-MAML and equally large untied expansion.
- **Old-task retention:** Check that untouched old feedback still lands correctly on both sides of growth, including rare B cases whose activations lie near a hidden-unit boundary.

### IP16 · A response anchor rather than a function anchor — IMPROVEMENT
- **Mechanism:** Replace some of the anchors in output regularization with exact, target-blind response differences after ordinary feedback on disposable measurement forks. Fit C while keeping a fixed mixture of no-feedback and response anchors.
- **Nearest prior / gap:** [Functional Regularisation] stores an approximate posterior over old outputs; [La-MAML] optimizes post-update performance. The improvement to test is whether a response-anchor budget preserves old feedback options better than these alternatives, not whether a larger regularizer works.
- **Cheapest first test:** On a three-task CPU stream compare output-only anchors, gradient projection and replay plus La-MAML at matched stored bytes and editor work; score held-out response families rather than the anchors themselves.
- **Old-task retention:** Old items due without any feedback and ordinary post-feedback A/B both count; if any falls below its floor to improve response coverage, reject.

### IP17 · A patch translation validated on the difference, not either learner — PRIMITIVE CANDIDATE
- **Mechanism:** Translate the *contrast* between a source’s patched and unpatched responses into a recipient, without cloning either source endpoint. Constrain the recipient’s launch function and protect its existing unrelated correction responses.
- **Nearest prior / gap:** [Distillation] transfers output predictions and [Task Arithmetic] transfers parameter deltas. The proposed transfer object is the difference between two ordinary-update effects, identified across incompatible parameterizations.
- **Cheapest first test:** Translate a quadratic source into a small smooth MLP with different widths. Fit on a few ordinary directions and hold out rates, directions and recipients; compare distillation on exact source endpoints and ordinary delta alignment at the same budget.
- **Old-task retention:** Retain recipient-private legacy tasks, shared old A, and old responses that were already better in the recipient than in the donor.

### IP18 · Transport through a pruner using return behavior — IMPROVEMENT
- **Mechanism:** Choose channels to keep by their contribution to post-feedback separations, then re-encode the separations in a fixed sparse recipient. Do not restore deleted weights or a saved dense teacher at read time.
- **Nearest prior / gap:** [Lottery Tickets] finds sparse trainable subnetworks; [Pruning Spaces] describes useful subnetwork architectures. The target here is retention of a particular writable response contrast after pruning, not generic trainability or static accuracy.
- **Cheapest first test:** Enumerate equal-density masks in a tiny redundant MLP. Compare response-selected masks with magnitude pruning, rewound tickets, and compressed replay at the same storage and write cost, then apply held-out corrections after C.
- **Old-task retention:** Protect rare old channels that are dormant on the fit queries but needed at a normal legacy deadline; no dense recovery fallback for free.

### IP19 · A three-writer collision ledger for responses — PRIMITIVE CANDIDATE
- **Mechanism:** Let two writers independently preserve different response coordinates and give a third writer only their scoped, bounded claims. Admit a joint edit only if independent prefixes and composed probes still work, returning the smallest conflicting prefix otherwise.
- **Nearest prior / gap:** [GEM] and [PCGrad] detect or mitigate local gradient interference. The candidate conflict is invisible at launch and on individual singleton checks, yet attributable to a specific later legal prefix rather than a gradient cosine.
- **Cheapest first test:** Enumerate two patch writers and a third C writer in a four-channel host; plant a collision activated only in one paired order. Compare full joint refitting and GEM at the same total audit and update cost.
- **Old-task retention:** Retain each writer’s ordinary A/B service and its undisputed read prefixes independently; rejecting a merge cannot erase the live learner.

### IP20 · Keep the write through a changed optimizer, not its momentum — PRIMITIVE CANDIDATE
- **Mechanism:** Define the carrier by a sign or ordering of held-out responses across a disclosed family of optimizers with reset state and matched update magnitudes. Install the host factor without embedding optimizer state as an answer store.
- **Nearest prior / gap:** [MAML] optimizes for an adaptation rule and [Automated CL] learns the rule itself. The gap is a writable selective response invariant to a family of *external*, replaceable optimizers, not transfer of a trained optimizer.
- **Cheapest first test:** Compare SGD, reset momentum and a diagonal preconditioner with matched first displacement on a small quadratic head, then test a new preconditioner. Use copied optimizer moments and optimized initialization as storage-matched controls.
- **Old-task retention:** Report the weakest optimizer on A/B and reversal corrections, not just average portability; never reset away the branch’s new C competence.

### IP21 · Surgical removal of the response factor — PRIMITIVE CANDIDATE
- **Mechanism:** Overwrite just the degrees of freedom that encode a designated read by learning. Try to make every allowed read prefix equivalent to a never-written state without erasing static competence or other response coordinates.
- **Nearest prior / gap:** [Benign Relearning] uses later optimization to test whether apparent erasure was superficial. The proposed operation erases a designed, addressable response channel while keeping distinct legal neighboring reads.
- **Cheapest first test:** Write two independent bits, remove one without reverting the checkpoint, and enumerate legal one- and two-update prefixes. Compare resetting a dedicated state byte and output-only erasure; score the masked bit at chance with uniform assignments.
- **Old-task retention:** Retain ordinary A/B and the unrevoked bit’s old response. The erased bit cannot be a task due now; this is not a claim of universal deletion outside the declared read protocol.

## D · Find the regimes where a patch is worth keeping

### IP22 · An access-aware shortcut frontier — IMPROVEMENT
- **Mechanism:** Produce a cost frontier over read permissions: black-box logits, optimization endpoints, directional derivatives, then internal-state inspection. Record the first reader that matches the live learner rather than reporting one aggregate chance score.
- **Nearest prior / gap:** [Differential Influence] provides an efficient approximation to influence; [Tangent Hierarchy] supplies higher-order probes. The improvement is measuring the smallest *sufficient* read budget for the claimed memory in an exact comparison with updates.
- **Cheapest first test:** Map the two exact fixtures plus a planted logits leak; predict which reader should succeed before enumerating. Include matched-work exact endpoints and a direct byte read; a channel justified only by withholding access must be labeled as such.
- **Old-task retention:** Evaluate all usable readers on ordinary A/B outputs at the same endpoint and deadline; a read on a destructive fork cannot pass as live service.

### IP23 · Equal-byte compression for partially unlocked memories — PRIMITIVE CANDIDATE
- **Mechanism:** Share one low-dimensional factor across multiple task responses whose ordinary cues arrive at different times. Store direct answers for deadline-critical slices and let the shared factor cover only those reconstructible on time.
- **Nearest prior / gap:** [Trajectory Distillation] compresses training into synthetic examples and [Spurious Forgetting] separates alignment from retained knowledge. The claim is a favorable storage–deadline tradeoff under unchanged ordinary evidence, not compression just by waiting.
- **Cheapest first test:** Enumerate allocations of bytes and recurring cue schedules in an eight-task toy world; compare low-rank answer heads, compressed replay and factorized MAML, including the no-cue regime. Price the writer and the direct-answer fallback.
- **Old-task retention:** Any rare B query whose cue misses the deadline needs its direct path; compare missed deadlines and worst-slice performance, not steady-state mean alone.

### IP24 · Use a byte of precision where it changes the read threshold — IMPROVEMENT
- **Mechanism:** Quantize launch-equivalent states using a budget assigned to the smallest separating finite response at operating step sizes. Equalize the no-update quantization error across arms.
- **Nearest prior / gap:** [Wide Linearity] connects the size of Hessian contributions to effective linearity; [Function-Space Regularization] measures changes in functions rather than parameters. Here the error criterion is a calibrated, post-update decision under real numeric limits.
- **Cheapest first test:** Exhaustively allocate 1–8 bits per coordinate on a tiny polynomial with noisy residuals, then test held-out rates. Compare magnitude-based precision, output calibration and direct bit storage. Drop the patch if serializing it costs more than storing and using its decoded effect.
- **Old-task retention:** Check low-margin A/B across rounding seeds and read prefixes. Count quantization that hides the payload merely by degrading all old tasks as failure.

### IP25 · A causal receipt for where the saved examples came from — IMPROVEMENT
- **Mechanism:** Exchange the response factor between function- and tangent-matched twins, with native, swapped and sham swaps, and test whether savings follow the factor rather than the history of the host.
- **Nearest prior / gap:** [Spurious Forgetting] attributes some early degradation to alignment; [ANML] seeks representations resistant to interference. This is an identification test for an installed, selective carrier rather than another relearning curve or generic robustness metric.
- **Cheapest first test:** Register separate held-out targets for old A, fresh A-like work and shuffled A. Swap before and after C; include sham swaps that preserve norms and curvature magnitudes but scramble the response assignment. If savings do not follow the assignment selectively, don't credit the carrier.
- **Old-task retention:** Verify that the act of swapping leaves both donors’ normal A/B service and independent correction rights intact.

### IP26 · A negative control with the same entire response table — IMPROVEMENT
- **Mechanism:** Hide a history bit in auxiliary parameters while making every permitted query and prefix transition observationally equivalent across bit values. Use it to detect leakage through seeds, checkpoint choices, gauge or undeclared readers.
- **Nearest prior / gap:** [Angluin] formalizes when observations distinguish hypotheses; [Git Re-Basin] supplies concrete equivalences in weight space. The gap is a reusable null for judging any claimed read-by-learning benchmark.
- **Cheapest first test:** Attach a disconnected bit (and a separate permutation-only host twin), hash the enumerated read traces, then try the same decoder suite as on planted positives. An above-chance decoder reveals leaked state, not learning.
- **Old-task retention:** Both null arms must pass identical A/B and C service trajectories, including output precision and metric denominators; a failing null is a fixture defect.

### IP27 · Learn to stop carrying a read when the environment supplies it — PRIMITIVE CANDIDATE
- **Mechanism:** Mark a response coordinate as reclaimable only after matched naive recipients can recover it from the actual ordinary evidence within its deadline. Reassign the factor to a different old target and recheck the former target after independent edits.
- **Nearest prior / gap:** [Spurious Forgetting] and [Benign Relearning] show that easy recovery is possible. The candidate is a reclaim operation measured against online evidence supply, not an assumption that quickly recoverable targets never needed memory.
- **Cheapest first test:** Change cue frequency twice in a binary stream. Compare fixed replay, a cache with empirical eviction, and oracle deadlines at matched bytes. Include a downturn after reclaim to test whether a declared free coordinate was really reusable.
- **Old-task retention:** Keep an old target whose only cue disappears and another with no slack before its deadline; a necessary fallback counts against recovered capacity.

### IP28 · A response family that pays for a shared writer — PRIMITIVE CANDIDATE
- **Mechanism:** Train a reusable installer that maps a small observed correction family to a silent response patch, then use it across held-out task families without per-task meta-training. Count the installer and its training, amortized over explicitly stated numbers of installations.
- **Nearest prior / gap:** [MAML] amortizes adaptation by meta-learning an initialization; [Automated CL] meta-learns continual update algorithms. The candidate contract is a transferable writer of selected higher-order responses with fixed launch outputs and tangents, not a learned general-purpose optimizer.
- **Cheapest first test:** Use a few small nonlinear regression families with held-out structure, not just seeds. Plot total bytes and CPU work to the same old recovery floor against hand-written factors, direct storage and La-MAML; report the first actual crossover or none.
- **Old-task retention:** Each installation must leave its host’s rare B and unrelated old corrections usable, and later installations cannot spend this guarantee to improve amortized cost.

## Ranked deeper questions

1. **What is the strongest reader the patch actually beats?** Start at IP01, IP08, IP13 and IP22. Check exact launch outputs, gradients and all legal singletons, then compare against step-size/gauge controls, directional Hessians, pooled batches at equal examples and work, and exact virtual endpoints. Require both orders, naive and shuffled-label controls, and live A/B after C. If a simple reader ties, name the restricted access class or abandon exclusivity; an exact same-access simulator always ties. Do not return to the parent’s transplant and composition work until this gate is understood.
2. **Can independent writing survive C without buying a replay system in disguise?** Start at IP15–IP20 and use IP25 to attribute savings to the written factor. Require held-out ordinary feedback, cheap selective rewrites and same-budget replay plus La-MAML. A win must survive one independent new task with the original service deadlines, not merely a shared training objective.
3. **Is the value in ordered learning or in ordinary integration of observations?** Start at IP08–IP14. Match pooled loss scale, examples, optimizer reset and deadlines; compare a counter, a static feature, and direct caching. Count all singleton and intermediate access, including mixed batches where legal. If order adds no capability above those controls, keep the cheaper integration mechanism.
4. **Where is the cost crossover once immediate service is priced?** Start at IP23–IP24 and IP27–IP28. Sweep cue reliability, bit precision, state size and number of deployments. Charge direct fallbacks, peak forks and pretraining; start with exact enumeration, and stop if every feasible policy is dominated by compressed answers or replay at the same prefix floors.

[PR #6]: https://github.com/manojbajaj95/cl/pull/6
[PR #114]: https://github.com/manojbajaj95/cl/pull/114
[PR #123]: https://github.com/manojbajaj95/cl/pull/123
[PR #336]: https://github.com/manojbajaj95/cl/pull/336
[triage]: https://github.com/manojbajaj95/cl/blob/577170e3752b3ef31ee1c331a2b28540a7f8150f/reviews/flood-triage.md#L456
[ledger]: https://github.com/manojbajaj95/cl/blob/577170e3752b3ef31ee1c331a2b28540a7f8150f/reviews/idea-ledger.md
[NTK]: https://arxiv.org/abs/1806.07572
[Tangent Hierarchy]: https://arxiv.org/abs/1909.08156
[Wide Linearity]: https://arxiv.org/abs/2010.01092
[Differential Influence]: https://arxiv.org/abs/2508.14648
[SGD Regularization]: https://arxiv.org/abs/2101.12176
[MAML]: https://arxiv.org/abs/1703.03400
[Meta-SGD]: https://arxiv.org/abs/1707.09835
[La-MAML]: https://arxiv.org/abs/2002.09571
[ANML]: https://arxiv.org/abs/1910.01705
[Git Re-Basin]: https://arxiv.org/abs/2209.04836
[Net2Net]: https://arxiv.org/abs/1511.05641
[Trajectory Distillation]: https://arxiv.org/abs/2203.11932
[Learning Where]: https://arxiv.org/abs/2110.14402
[OGD]: https://arxiv.org/abs/1910.07104
[Conditional Invariance]: https://arxiv.org/abs/2402.11682
[Shamir]: https://doi.org/10.1145/359168.359176
[Angluin]: https://doi.org/10.1016/0890-5401(87)90052-6
[Backpropamine]: https://arxiv.org/abs/2002.10585
[Automated CL]: https://arxiv.org/abs/2312.00276
[Composable Expansions]: https://arxiv.org/abs/2308.06103
[Functional Regularisation]: https://arxiv.org/abs/1901.11356
[Distillation]: https://arxiv.org/abs/1503.02531
[Task Arithmetic]: https://arxiv.org/abs/2212.04089
[Lottery Tickets]: https://arxiv.org/abs/1803.03635
[Pruning Spaces]: https://arxiv.org/abs/2304.09453
[GEM]: https://arxiv.org/abs/1706.08840
[PCGrad]: https://arxiv.org/abs/2001.06782
[Benign Relearning]: https://arxiv.org/abs/2406.13356
[Spurious Forgetting]: https://arxiv.org/abs/2501.13453
[Function-Space Regularization]: https://arxiv.org/abs/1805.08289
