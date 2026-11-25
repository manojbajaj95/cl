# Convergence: Relearnability as Memory

Convergence node for [PR #331], [PR #334], and [PR #335] · 32 idea cards · Ideas only; no training runs

**Question.** If two learners give exactly the same answer to every old query, can one ordinary round of old feedback make their answers differ? Yes. The research bet is stronger: can we preserve and reuse **the means to relearn**, rather than the answer, at lower total cost than keeping answers, examples, or a good initialization? This does not excuse failing a task that needs its answer *before* feedback arrives.

**Three independent lines.** In [PR #331], LE5-11/15 preserve a second teaching route through a first learner's successful update; LE5-25 supplies a matched fresh-task control for generic plasticity loss. In [PR #334], SD2-19 divides memory into distinctions that a legal cue can cheaply reteach and distinctions that must survive without it. In [PR #335], SMA13/31 separate serving edges from correction edges and put the scope of a correction in the update rule; its first ranked question asks for exact old-query agreement followed by ordinary old-feedback separation. See the [reviewer rows][triage] on [PR #6] and the revised [top-10 #5][top10], from [Inversions 03][inversions]: make savings a designed read head, not just a forgetting diagnostic. [PR #114] killed the linear fork's hidden-channel claim (raw logits already decoded its bits); [PR #123] adds a one-step shortcut check. A usable teaching route need not be hidden; a claimed *exclusive* training read does.

## Exact witness: same old function, different finite update

Use the old query space $X=\{-1,+1\}$ with old regression target $y=x$. Both learners use $f_{u,v}(x)=uvx$, with states $(0,1)$ and $(0,2)$. Their outputs are identical on every old input (indeed on every real input). Give each the same ordinary example $(+1,+1)$, loss $\tfrac12(f(x)-y)^2$, and one simultaneous SGD step with $\eta=1/4$. At the cut the gradient is $(-v,0)$, so the new pair is $(v/4,v)$. The new outputs on the **unseen** old input $-1$ are $-1/4$ and $-1$. No task ID, switch, different optimizer, or hidden feedback was used.

This is an identifiability witness, not evidence for a learned carrier: the first gradient and the tangent kernel already tell the states apart, and an effective step-size control ties it. An endpoint matched only on classification accuracy would be weaker than this fixture. If both learners interpolate every old feedback target and the ordinary loss gives zero gradient there, vanilla SGD on exactly that feedback cannot separate them; tests must state where residuals come from (e.g. an ordinary return after interference, noisy feedback, or corrections under the old interface).

## Shared CPU-first contract

- **Freeze the interface before seeing the target.** A state includes weights, optimizer, buffers and any learned update rule. Declare old queries $Q$, allowed ordinary feedback $E$, a fixed update rule and its state, and a deadline $k$. Compare both $f_s|_Q$ and the observable response $R_s(e,q)=f_{U_e(s)}(q)$ for a feedback prefix $e\in E^{\le k}$. One separating pair refutes equivalence under feedback; matching finitely sampled responses does not establish it for all legal prefixes. With no observable difference under the declared protocol, do not count stored parameter differences as retained memory.
- **Measure savings against the right nulls.** On paired streams, compare steps, ordinary examples, and wall-clock work to the same loss and retention floors; report non-completion separately. Match exact outputs on small finite worlds, otherwise match logits, margins, and starting losses on preregistered probes. Include a matched old-task-naive recipient given the identical feedback, a matched fresh task, shuffled labels of matched difficulty where meaningful, replay and MAML/La-MAML at equal budget, and the particular control named per card. Sweep step size and test gauges, optimizer reset, and direct same-byte storage. A scratch or naive learner tying after the cue means the cue taught the target, not that the learner retained it. Do not transfer labels, stored deltas, or observer-selected checkpoints for free.
- **Separate service from recovering service.** Pretrain ordinary A and B (B rare); return to A after learning C. Card-specific retention below is in addition to unchanged per-task A/B slices before C, after C, and through each feedback prefix, plus C at matched progress. Use no special probe as a serving cue, task ID, or restore. Score held-out old items disjoint from feedback, with a separate floor for jobs due before feedback and for untouched neighbors. Experimental forks are for measurement; any live forks, selection labels, shared decoder, offline search, stored state, peak state, and extra reads count in the budget.
- **For a hidden read, rule out shortcuts.** At matched access and work, give shortcut readers the raw outputs on the feedback and test inputs, first gradients (including the rule's actual update inputs), $J_Q\Delta\theta$, and, for a multistep claim, exact one-update endpoints. Compare with public or label-free forks only when the very same strings/observations go to the naive recipient. With identically retained states and identical legal inputs, no later continuation can recover the history distinction. Do not retry the failed affine fork, Gramian reserve, or self-generated QA replay from the [idea ledger][ledger] under new names.

## Literature check

The closest comparisons below come from targeted Hugging Face Papers searches and checks of original abstracts on Hugging Face/arXiv and the linked historical sources. They establish overlap and the remaining test, not claims of priority. Ebbinghaus's [savings paradigm][ebbinghaus] already measures memory by the cost of learning again. [Hinton and Plaut][hinton] proposed fast/slow weights to mitigate interference, not the first discovery of rapid reacquisition. [Spurious Forgetting] shows performance loss can be shallow task misalignment; [Benign Relearning] and [Syntax Relearning] show restoration from loosely related or structurally similar data. These are reasons to control cue leakage and ordinary realignment, not evidence for a deliberately writable channel. [MAML] and [La-MAML] already optimize post-update performance; [Automated CL] already meta-learns the update mechanism. [NTK] and [NTK Overlap] already explain differential response and interference to first order, and [Mode Connectivity] / [Git Re-Basin] already show how low-loss geometry can depend on representation. None of **savings**, **a good post-update loss**, **a different gradient**, or **a low-loss path** alone qualifies as a new primitive here.

## A. What the memory writer can install

### CR01 · A finite-response patch with zero tangent — PRIMITIVE
- **Mechanism:** Install a local nonlinear factor that changes the *finite-step* response to an ordinary correction, while preserving pre-feedback outputs and first derivatives at the operating point. Expose the patch as an independently writable second-order term, not a stored gradient.
- **Nearest prior / gap:** [NTK] gives the first-order response; [MAML] optimizes a finite step. The claim is a selective response edit with output **and tangent** fixed, not that curvature matters.
- **Cheapest first test:** Enumerate scalar polynomials $f(t)=t+ct^2$ at $t=0$, then fit one such factor in a two-output polynomial. Compare generic one-step meta-training and a scalar LR control with identical first derivatives and one allowed coefficient. Reject if either can change just the requested endpoint.
- **Old-task retention:** Preserve a second output and held-out old correction contexts, through the edit and through the altered finite update.

### CR02 · An answer-free substitute teacher — PRIMITIVE
- **Mechanism:** Persist a transform from naturally arriving evidence of source S into the update coordinates of unavailable source T. The transform is installed before either source reveals its target and must work after a polarity swap; it does not store T's target.
- **Nearest prior / gap:** [Synthetic Gradients] predicts backward signals locally; [Modular Solutions] learns composable model parts. Here an independently changing *evidence source* can substitute for another on unheard corrections, without predicting the answer in advance.
- **Cheapest first test:** Use two view-specific regression streams with one hidden signed permutation and draw a new target after fitting the transform. Compare an equally sized synthetic-gradient predictor, CCA bridge, and ordinary multitask feature sharing.
- **Old-task retention:** S and T's previous shared tasks and their view-private tasks must survive substitution; misaligned evidence must not rewrite the old private rule.

### CR03 · A write that changes who can teach, not what is read — PRIMITIVE
- **Mechanism:** Make a learned correction address replaceable independent of forward weights: two callers reading the same value can send conflicting corrections to distinct factors selected by provenance learned from past interactions.
- **Nearest prior / gap:** [Learning Where] learns gradient sparsity, and [Automated CL] learns an update rule. Build on SMA31 only if the correction address can be swapped independently between learners and still dispatch correctly on callers not seen at installation.
- **Cheapest first test:** In a two-caller table, swap only the address between output-equal learners before revealing a third caller that inherits one provenance pattern. Compare SMA31 in place, a fixed learned mask, and equal-state context-conditioned meta-updates.
- **Old-task retention:** Old queries must agree immediately; later both legitimate and invalid old corrections must leave the other caller's held-out examples intact.

### CR04 · A silent competitor that teaches only under disagreement — PRIMITIVE
- **Mechanism:** Factor the backward map into a shared vote and an antisymmetric vote. Agreement updates the shared feature; a naturally occurring disagreement enables a zero-forward antisymmetric component to receive evidence, so unrelated updates cannot erase its future use by averaging.
- **Nearest prior / gap:** [PCGrad] uses gradient disagreement to resolve interference; [Learning Where] selects weights. Here disagreement opens a separately persistent, zero-forward update port, rather than projecting away the conflicting component.
- **Cheapest first test:** Enumerate paired noisy corrections for two Boolean views, with the same individual marginals and different joint signs. Compare fixed projection, gradient-surgery on the same pair, and matched context-gated adapters; hold out new pairs.
- **Old-task retention:** Check rare old items requiring the shared vote and the old cases in which only one source provides evidence.

### CR05 · A response with fixed average but useful variation — PRIMITIVE
- **Mechanism:** Write a factor that preserves mean response on each old output over legal batches while deliberately correlating the response with which evidence arrived. Expose the conditional response, not noise magnitude, as the programmable quantity.
- **Nearest prior / gap:** [NTK Overlap] models first-order transfer, and [Dataset Distillation] changes examples to shape learning. Keep the ordinary batch distribution fixed; learn which response conditional on a public batch statistic can change without altering the mean.
- **Cheapest first test:** Enumerate all size-two batches of a parity toy with paired nuisance signs. Compare a matched update-covariance controller and independent random perturbations at the same covariance and old mean. Reject unless the batch-conditioned association transfers to unseen pairs.
- **Old-task retention:** Require per-batch old-task floors, not only mean retention; check the rare nuisance sign before and after feedback.

### CR06 · Store which parameter combinations are still learnable — PRIMITIVE
- **Mechanism:** Preserve an update interface over identifiable *combinations*, not a dormant head per target. Expose one correction coordinate only for each observable contrast; defer the null directions until independent evidence arrives.
- **Nearest prior / gap:** [Modular Solutions] factors reusable function parts and [Rate–Distortion] prices decoder side information. The bet is a factor that can accept new evidence for the unresolved combinations without reconstructing the complete old hypothesis.
- **Cheapest first test:** Two stages reveal different rank-one observations of three signed coefficients. Install the interface before drawing the coefficients. Compare incremental least squares with full sufficient statistics and exact same-budget coding plus an ordinary updater. Drop the storage claim if the sufficient statistics tie.
- **Old-task retention:** Old queries involving only prior identifiable contrasts stay correct through both stages, and deadline-critical null-direction queries use the separately retained fallback.

### CR07 · Teach a direction without committing its sign — PRIMITIVE
- **Mechanism:** Install a transferable basis-vector *handle* which specifies a joint response on several old queries but has no preferred coefficient. One signed ordinary label chooses polarity after transfer; old answers and pre-feedback preferences must not reveal it.
- **Nearest prior / gap:** [MAML] and [Learning Where] can learn low-dimensional adaptable subspaces. Require independent placement and reuse of one handle across backbones with no matching of entire parameter vectors, not just a low-rank warm start.
- **Cheapest first test:** Train small Boolean feature factorizations on disjoint tasks, install a common handle via public correspondences, and then draw a random sign. Compare a frozen feature with a new linear head, low-rank MAML and equal-bit basis storage; score both signs.
- **Old-task retention:** Include an old rare task sharing the handle's support whose sign must not be changed by the new correction.

### CR08 · A memory with no dependence on the learner's step units — PRIMITIVE
- **Mechanism:** Define a learned response as an ordered sequence of observable boundary crossings, not a learning-rate-specific vector. Compile an update port that guarantees the order across a declared step-size interval while leaving the serving function fixed at installation.
- **Nearest prior / gap:** [Learning to Learn] trains an optimizer and [Mode Connectivity] finds low-loss paths. The candidate promise is invariance of the *ordering* of old distinctions restored by ordinary updates, not linearly connected weights or tuning rates.
- **Cheapest first test:** Enumerate quantized SGD states for two old parity slices with different restoration thresholds. Compare LR schedules, normalized SGD and a same-size MAML initializer under held-out *fixed* rates. Certify by enumeration rather than fitting thresholds to the evaluator.
- **Old-task retention:** One deadline-critical legacy slice must never fall below its floor for any rate, including rates that delay the other crossing.

## B. Operations on correction interfaces

### CR09 · A transplant checked by responses rather than weights — PRIMITIVE
- **Mechanism:** Extract a partial map from ordinary feedback to query changes around a scope; synthesize an attachment that realizes that map inside an independently trained recipient. Transfer only the correction interface, without replacing its current predictions.
- **Nearest prior / gap:** [Git Re-Basin] aligns units of whole networks for merging; [Dataset Distillation] replaces training sets. The candidate operation should work when there is no whole-model alignment and the recipient cannot use the donor's data or outputs outside the scope.
- **Cheapest first test:** Fit factorized regressors with incompatible private heads and identical shared-task outputs. Match responses on some ordinary shared corrections, then test new ones against aligned merge plus refit and a distilled meta-initializer of equal size.
- **Old-task retention:** Recipient-private and donor-shared old tasks survive; a correction outside the transferred scope continues to use the recipient's original route.

### CR10 · A morphism that commutes with learning — PRIMITIVE
- **Mechanism:** For a live grow/split edit $M$, construct a feedback/update lifting rule such that updating after the edit agrees on old outputs with doing the same update before the edit and then migrating. Preserve specific old update sequences, not just the cut prediction.
- **Nearest prior / gap:** [Net2Net] and [Composable Expansions] preserve the forward function; [Learning Equivariance] derives constraints on learning dynamics from parameter transformations. The narrower obligation is a train-then-edit versus edit-then-train guarantee on specified finite feedback, including noninvertible cross-architecture edits, not a new symmetry principle.
- **Cheapest first test:** Widen a two-unit regressor and check every length-two old batch sequence. Compare Net2WiderNet with LR correction, tied clone training and an equal-size static supergraph; permit untied future learning outside the preserved scope.
- **Old-task retention:** Check old rare responses through two successive morphs, and unchanged immediate old queries when no feedback arrives.

### CR11 · An executable disagreement returned by merge — PRIMITIVE
- **Mechanism:** When two output-equal routes are merged, return the smallest *legal feedback prefix* that exposes an incompatible correction plus its scope, rather than a scalar merge score. A later edit can replay the witness to verify the disputed route without donor weights.
- **Nearest prior / gap:** [Git Re-Basin] aligns/merges predictors and the [repo's Nerode work][nerode] already supplies separating continuations. The candidate artifact is a scoped witness of a *specific failed join* that a later independent repair can reuse, not existence of a separating string.
- **Cheapest first test:** Enumerate merges of finite rule learners with held-out delayed corrections; give a repairer only witnesses from an earlier merge. Compare fresh counterexample search and retaining two routes at equal memory and verifier work.
- **Old-task retention:** Validate intact behavior of both donors' undisputed old corrections plus immediate old answers after recovery from the failed merge.

### CR12 · Join local correction contracts without joining learners — PRIMITIVE
- **Mechanism:** Glue partial response maps over overlapping scopes by agreeing on the induced changes on the overlap, then test whether the glued map is realizable by one ordinary learner. Reject a join with an incompatibility certificate instead of silently averaging conflicting responses.
- **Nearest prior / gap:** [Task Arithmetic] combines parameter deltas, and [Provable Repair] enforces prescribed output changes. The candidate operation implements reusable response-level composition with an explicit realizability failure, not fitting pooled targets.
- **Cheapest first test:** For a tiny bilinear model enumerate local response constraints with pairwise agreement but a globally infeasible triple. Compare pooled distillation, separate adapters and a joint solver with the same observations and solve budget.
- **Old-task retention:** Old queries outside the gluing overlap and each input contract's held-out in-scope corrections survive any accepted join.

### CR13 · Reject a correction without discarding its evidence — PRIMITIVE
- **Mechanism:** Split an arriving update into an immediately admissible response and an unresolved obligation, encoded as a constraint on a later response rather than a queued parameter delta. Re-solve that constraint after the learner changes coordinates.
- **Nearest prior / gap:** [Error Feedback] accumulates compression residuals; [Gradient Projection Memory] projects conflicting gradients. The bet is portability of the unresolved *effect* across an intervening representation change, not eventually applying rejected gradients.
- **Cheapest first test:** A two-output factorization rotates after one blocked correction; a second ordinary example later disambiguates its lawful scope. Compare gradient error feedback, matched raw-example replay and a stored constraint solved in old coordinates.
- **Old-task retention:** Keep the initially blocking old task correct at every prefix; check a rare held-out case requiring the deferred response once permitted.

### CR14 · Remove a teaching route by draining only its obligations — PRIMITIVE
- **Mechanism:** Retire an update route only when all feedback already issued against it has either been discharged or can be credited via a verified successor map. Keep no predictor copy; allow old value reads to live on a separate route.
- **Nearest prior / gap:** [Synthetic Gradients] decouples backward computation; SMA23 in [PR #335] routes pending corrections by provenance. The added operation is a reusable *retirement condition* under which an independent edit can erase the original route, not moving credit once.
- **Cheapest first test:** Exhaustively reorder delayed feedback over two successive edge changes in a finite learner. Compare a queue attached to archived modules and SMA23 plus a global callback registry with the same bytes and operations.
- **Old-task retention:** Score legacy episodes opened before retirement and completed afterward, including old aliases that receive feedback of opposite sign.

### CR15 · A correction join that promises locality across order — PRIMITIVE
- **Mechanism:** Package two update ports with a certificate that either order preserves an agreed old response outside a named interaction scope. Within scope, export a required order only if it is observable before the first divergent update.
- **Nearest prior / gap:** [PR #334] already covers ordinary commutativity and contingent continuations; [Certified CL] bounds changes in prior outputs. The test is reusable composition for **feedback response** despite different final weights, not a new commutativity theorem.
- **Cheapest first test:** Enumerate all legal two-batch permutations in two small independently trained graphs, then attempt an unseen third join. Compare pairwise commutativity checks over outputs plus exact re-verification, charged at the same work.
- **Old-task retention:** Check both old orderings on untouched probes, and refuse only the ambiguous order in the named legacy scope.

### CR16 · Replace an editor without replacing what learners can be taught — PRIMITIVE
- **Mechanism:** Compile one interface of ordinary feedback into a different optimizer's state and step semantics so that old finite responses stay within declared tolerances. Retain only the compile product, not an emulator calling the old editor.
- **Nearest prior / gap:** [Learning to Learn] learns optimizer policies; [NTK] can already match first-order updates. The candidate is optimizer substitution for existing corrections, including their response to subsequent steps and unseen legal batch compositions.
- **Cheapest first test:** Match a small sign-SGD learner to a constrained SGD recipient on single and two-step old sequences, with permission to fail translation on a conflicting sequence. Compare LR/per-parameter calibration, a learned optimizer and exact replay-based distillation.
- **Old-task retention:** Check unchanged old no-feedback behavior and held-out old updates requiring opposite signs and different batch orders.

## C. What ordinary evidence can unlock

### CR17 · A handoff with reversible retirement — PRIMITIVE
- **Mechanism:** Replace a served answer with a procedure plus a witness that every legal feedback prefix due by the deadline identifies it; permit retirement only while this witness remains valid. Before deleting, publish the cheapest falsifying prefix so another writer can downgrade the contract and keep a fallback.
- **Nearest prior / gap:** [Rate–Distortion] counts decoder side information and SD2-19 in [PR #334] already proposes the answer/procedure split. The new operation is a reusable revocation witness for the *supply* of future evidence after a different writer changes the world, not another static allocation.
- **Cheapest first test:** Enumerate dialect worlds in which a public cue disappears or is delayed, announced only when a later editor changes the supply contract. Compare re-solving the exact same-bit codec each time and a fixed compressed head with the same notice.
- **Old-task retention:** Verify deadline-critical dialect queries even when the cue disappears, and unaffected old commands on both sides of revocation.

### CR18 · A feedback receipt that cannot teach twice — PRIMITIVE
- **Mechanism:** Compile learnability from *independent observations*, not number of update calls. A single arriving observation of unknown truth appears in two modules' ordinary feedback; turn the two receipts into one reusable constraint with two destinations. Do not let duplicate delivery create a second bit of apparent evidence.
- **Nearest prior / gap:** [Nonparametric Machine Teaching] chooses useful training examples iteratively; [Functional Regularisation] stores inducing inputs for old functions. Idempotent receipts alone are standard; the bet is an evidence object that survives changes to the recipient's factorization and distinguishes reusable evidence from duplicate support.
- **Cheapest first test:** Route delayed binary noisy labels to two heads, with replayed receipts versus independently repeated labels. Compare exact deduplicated replay and a sufficient-statistic updater with equal state. Reject if the receipt does not improve re-routing under a head split.
- **Old-task retention:** Check a legacy rare category that sees mostly duplicated receipts and another for which independent observations must still accumulate.

### CR19 · Budgeted questions that buy a future update, not a label cache — PRIMITIVE
- **Mechanism:** Use old interactions to choose which *relationship between cues* to retain, minimizing the future cost of an independently delivered correction. Keep the short relation and discard the queried answers, so the next teacher can pick a novel target.
- **Nearest prior / gap:** [Nonparametric Machine Teaching] optimizes example choice for the current learner; [Dataset Distillation] synthesizes a small transferable training set. Reverse what is chosen: observations buy a relation that lets an ordinary, uncoordinated entrant later teach several possible targets.
- **Cheapest first test:** In a finite three-view world, query at most two legacy co-occurrences before the target is sampled. Compare active queries for current accuracy, distilled examples and same-byte storage of the best common feature; hold out an entrant/view pairing.
- **Old-task retention:** Old view-pair categories and the rare category whose label never returns must stay available after the late entrant updates.

### CR20 · Sequential evidence with no informative singleton — PRIMITIVE
- **Mechanism:** Write a teaching gate enabled only after two independent observations establish a relationship. Either single legal update preserves the entire old read surface; only the composed ordinary updates can teach the target. Store the update gate, not the two answers.
- **Nearest prior / gap:** [Dataset Trajectories] matches multi-step training paths, and [PR #123] gives a two-step witness already. A new candidate would be a composable, learned gate on held-out cue pairs, with both first gradients and every single-update endpoint matched.
- **Cheapest first test:** Use a two-factor polynomial learner with a predeclared pair of public cues and one held-out cue composition. Compare sequence-conditioned meta-learning, direct one-bit storage and a generic two-step counter; additionally try swapping cue order and duplicating either cue.
- **Old-task retention:** Check legacy single-cue commands and an untouched target after every prefix; the duplicated cue may not trigger a spurious switch.

### CR21 · A correction that intentionally forgets its teacher — PRIMITIVE
- **Mechanism:** Transfer a teaching right from a source only after the recipient can derive the same legal corrections from its own evidence. Replace the link by a bounded response checker that can revoke disagreement, without retaining the original teacher or labels as a fallback.
- **Nearest prior / gap:** [Distilling Knowledge Updates] propagates a change to related facts via a teacher. This is independence from the original labeler after handoff, tested on *new old-scope corrections*, not teacher imitation of already-revised outputs.
- **Cheapest first test:** Fit two finite agents observing different logs of the same event. Withdraw the teacher and draw fresh outcomes; compare static teacher distillation and a frozen two-view decoder with the same state and public log. Include events for which the recipient observes insufficient data.
- **Old-task retention:** Keep old jobs that demanded teacher-only information on their existing route or abstain under their original contract; score old jobs from both views when the teacher is absent.

### CR22 · An update source that must prove it is substitutable — PRIMITIVE
- **Mechanism:** Let substitute feedback act on an old interface only on scopes where a compact agreement proof can be generated from ordinary overlapping observations; do not rely on the source's declared task label. A conflicting overlap revokes that scope locally.
- **Nearest prior / gap:** [Provable Repair] certifies changes to neural outputs, and [Syntax Relearning] already finds structure that restores knowledge with different content. The extra object is a scoped substitution proof to be reused across later ordinary corrections, including structural lookalikes that should **not** substitute.
- **Cheapest first test:** Enumerate two source grammars sharing surface forms but differing in one namespace; test unseen strings after fitting the scoped gate. Compare a matched domain classifier, a fixed pooled adapter, and per-correction certification.
- **Old-task retention:** Check old commands with ambiguous forms and rare namespace-specific actions both before and after a formerly reliable scope is revoked.

### CR23 · A learnability witness that survives removal of one cue — PRIMITIVE
- **Mechanism:** Store a minimal set of *alternative evidence sequences* sufficient to re-open a particular teaching direction. Index each alternative by the actual cue dependencies, so an edit removing one observation type invalidates only the promises that need it.
- **Nearest prior / gap:** LE5-15 in [PR #331] preserves redundant parameter carriers; [Rate–Distortion] handles multiple different decoder observations. The claim is a reusable explanation of **which sequential evidence alternatives remain valid**, not redundancy or compression by itself.
- **Cheapest first test:** Enumerate three overlapping observation channels with one removal and one common cause affecting two channels. Compare exact multi-decoder allocation with full revalidation and matched duplicate features. Reject if the witness does not save checks or increase valid retirements.
- **Old-task retention:** Verify rare old queries whose two apparent alternatives actually share the removed dependency, and preserve unchanged old serving on unrelated channels.

### CR24 · A certificate of what no permitted lesson can restore — PRIMITIVE
- **Mechanism:** Return two target histories that agree under *every* permitted feedback prefix up to the deadline yet require conflicting old outputs. Attach one distinguishing observation obligation to the proposed edit so a later writer can invalidate only this lower-bound witness.
- **Nearest prior / gap:** [Rate–Distortion] and the confusability-graph bound SD2-20 in [PR #334] already give the converse. The primitive bet is repairable, composable **impossibility witnesses** for restricted update programs, not a new information bound.
- **Cheapest first test:** Enumerate a 16-state world where extending the deadline and dropping a sensor have different effects on the same alias pair. Compare incremental witness reuse against an exact confusability graph recomputed under the same budget and equal-byte target storage.
- **Old-task retention:** Evaluate blocked old decisions at their deadlines, plus old query families that become recoverable after the distinguishing observation is added.

## D. Keep a useful route through a changing stream

### CR25 · Allocate precision to future updates rather than current values — PRIMITIVE
- **Mechanism:** Store quantization refinements for distinctions between response maps, spending zero extra bits where serving and permitted continuations agree. Later packing rechecks a refinement against new correction scopes and may drop it independently of weight blocks.
- **Nearest prior / gap:** [Error Feedback] corrects compression errors along actual gradients, and [Rate–Distortion] already prices future decoders. The bet is an independently writable fine-precision component that matters only to reachable future learning, not quantization tuned for a metric.
- **Cheapest first test:** Enumerate two-bit versus three-bit factorizations with identical old functions, followed by two legal gradient steps after fixed unrelated training. Compare mixed precision chosen by weight norms, recent gradients or exact task-loss coding at the same bytes.
- **Old-task retention:** Check legacy low-margin items both before and after rounding; report whether keeping their behavior consumes all claimed response-only precision.

### CR26 · Copy only the correction directions that outlive the next edit — PRIMITIVE
- **Mechanism:** When C leaves old outputs unchanged but would erase an old teaching route, rewrite just the endangered response factor into a free part of the learner. Test the relocation after C, rather than reserving that part against all writes.
- **Nearest prior / gap:** [Gradient Projection Memory] and [Synaptic Intelligence] protect important directions or weights. LE5-15 in [PR #331] pre-installs redundancy; this proposes a triggered migration of a live correction response with no permanent duplicate.
- **Cheapest first test:** Train a width-three shared linear factorization; choose from a fixed set of small C edits with equal immediate loss. Trigger migration on a held-out loss of cross-response, and compare always-on protection, LE5-15 and matched replay. Drop it if a scale-matched gradient proxy suffices.
- **Old-task retention:** Score the rare old probe tied to the previous carrier, and a common old probe sharing the destination, after relocation and subsequent old feedback.

### CR27 · Refresh a route by a public lesson that cannot answer it — PRIMITIVE
- **Mechanism:** Periodically practice a target-blind transfer task that exercises a particular update interface while drawing independent temporary targets. The persistent object is the map learned from those refreshes; never train on the retired target or a proxy that identifies it.
- **Nearest prior / gap:** [Benign Relearning] and [Syntax Relearning] demonstrate recovery from related strings; [Continual Backprop] maintains general plasticity. The claim is preservation of a specific response-map factor without refreshing answers or generic capacity.
- **Cheapest first test:** Interleave two tiny view tasks and refresh only one transform using random signs, with A's target independent and fixed. Compare unrelated practice, structure-matched ordinary training, and equal-work random unit refresh. Run the same exercises on an A-naive model.
- **Old-task retention:** Check A and a rare old view-private rule between refreshes; restoration should not merely undo the latest C task.

### CR28 · A budget for when feedback is scarce, not when storage is scarce — PRIMITIVE
- **Mechanism:** Make an executable serving lease that redeems an available correction route while enough future observations remain; when supply falls, promote the fragile distinction from learnable to immediately available using only currently lawful feedback.
- **Nearest prior / gap:** [Rate–Distortion] models decoder-side information and successive refinement; SD2-19 in [PR #334] already asks what to store. The candidate is an online conversion triggered by evidence depletion rather than a scheduled change in bit rate or simple caching.
- **Cheapest first test:** Use an exact two-state supply process with random outages and delayed returns, matching peak bytes. Compare always-on compressed heads, optimal cache with reacquisition cost, and a full finite dynamic program as an oracle. No gain claim when an exact cache captures the same actions and ties.
- **Old-task retention:** Check urgent old queries just after outages, including a rare one with no second opportunity to collect evidence; count every missed deadline.

### CR29 · Versioned relearning that cannot wake a stale answer — PRIMITIVE
- **Mechanism:** Preserve the correction interface across target revisions but require the current version's ordinary evidence to bind its coefficient. Any pre-binding state must be answer-neutral for that scope or serve an explicitly valid fallback.
- **Nearest prior / gap:** [Distilling Knowledge Updates] propagates revised facts; [Spurious Forgetting] and [Benign Relearning] show readouts can recover old knowledge. The target is selective recovery of the present version through the *same route*, not easier restoration of whichever version dominates in the weights.
- **Cheapest first test:** Alternate a signed rule through three revisions and hold out the change at which the old answer repeats. Compare a stored version bit plus compressed heads, standard replay, and a frozen generic meta-initializer with the same public version signals.
- **Old-task retention:** Track untouched rare old rules through all revisions and check old queries that must distinguish latest from as-of-time requests.

### CR30 · Route capacity measured in independent recoverable writes — PRIMITIVE
- **Mechanism:** Expose a batch-write interface that makes independent distinctions recoverable from separate licensed feedback prefixes. Track collisions by whether reading one distinction irreversibly changes another's read, not by classifier accuracy or parameter rank.
- **Nearest prior / gap:** [Rate–Distortion] already models multiple decoders; the [top-10 read head][top10] already proposes a channel and [PR #114] falsifies its affine fork. The new claim is a constructive allocation of *live*, mutually non-destructive training reads after intervening learning, not a bigger affine or static fork.
- **Cheapest first test:** Enumerate a quantized nonlinear two-factor system under both read orders and one intervening C write. Compare two independent adapters, same-byte direct storage, and shortcut readers from the shared contract; eliminate the hidden-read claim if they tie.
- **Old-task retention:** Sentinel A/B service persists through both read orders on the live learner, not just when discarding diagnostic forks.

### CR31 · Break a relearning dependency cycle with one ordinary lesson — PRIMITIVE
- **Mechanism:** Represent dependencies between teaching routes as executable prerequisites. If restoring A needs B and restoring B needs A, store an alternative seed lesson interpreter at an edge that makes the cycle first teachable, rather than keeping both answers.
- **Nearest prior / gap:** [Modular Solutions] learns reusable function parts, and [Nonparametric Machine Teaching] sequences training examples. Dependency planning is old; the learnability claim is that an answer-neutral interpreter gives an independent teacher an admission step a matched planner plus replay cannot buy.
- **Cheapest first test:** Three Boolean rules with a circular feature dependency, including cases with and without a legal seed observation. Compare exact prerequisite planning with cached examples, a generic warm start, and a same-bit direct answer at the weakest edge.
- **Old-task retention:** Require two unrelated old rules and all pre-deadline old queries in the cycle to meet their respective floors throughout the restart.

### CR32 · Pay for an ability only when a later learner uses it — PRIMITIVE
- **Mechanism:** Compile an update interface with a detachable response factor and a matched control factor. A later independent trainer can test necessity by replacing just that factor in a diagnostic copy using the same feedback, and retain it in the live learner only if it saves old-task relearning selectively.
- **Nearest prior / gap:** [Influence Functions] trace predictions through training examples and [Synaptic Intelligence] attributes importance over a path. The candidate is an independently replaceable **unit of credit** for a future learning response, not retrospective attribution; LE5-25's fresh-C test is the generic-plasticity null.
- **Cheapest first test:** Fit two tiny graphs with an interchangeable candidate factor and placebo. Test blind replacement on held-out return streams; compare leave-one-out data attribution, an equally sized generic feature and ablation of a replay shard. Charge the diagnostic branch.
- **Old-task retention:** Check that replacing the factor cannot change immediate old answers and that retaining it helps subsequent rare B without sacrificing normal A or equally hard fresh C.

## Ranked deeper questions

1. **Can correction interfaces survive independent edits at lower cost than replay plus meta-initialization?** Start with CR01/CR09/CR10: require one finite separation with matched outputs, gradients and first-order response, then install and transplant the responsible factor before an independent editor learns C. Measure exact prefix responses and paired cost to the same old floors on feedback not seen at installation. Stop if an LR/gauge adjustment, ordinary replay or La-MAML ties at matched state, data and work. An exact separation alone proves only non-equivalence.
2. **When should memory buy a teaching route rather than an answer?** Combine CR17/CR24/CR28. First solve the tiny confusability-and-deadline problem exactly with the same feedback supply for every method, including the no-cue case. Then test whether small executable factors realize more of the computed rate–deadline frontier than compressed heads and an equally informed dynamic cache. Never trade away an immediate required old answer to claim a win.
3. **Can a read by learning reveal a designed distinction that simpler readers cannot?** Start at CR20/CR30, building on the negative affine result. Require shuffled-label and naive recipients to fail, all single-batch endpoints and first-order readers to tie at chance, and held-out composed reads to work after C without damages on either read order. If a public feature, stored answer or equal-budget shortcut ties, drop the exclusive-channel claim even if selective relearning remains useful.
4. **What survives as a primitive once old teachability is made compositional?** Test CR12/CR15/CR23 on a third independent writer who sees only the contract and ordinary observations. Can it reuse witnessed scopes to join or revoke interfaces more cheaply than fresh joint fitting plus verification, while preserving the same old feedback rights and immediate service? If not, prefer the simple optimizer and checks to new machinery.

[PR #6]: https://github.com/manojbajaj95/cl/pull/6
[PR #331]: https://github.com/manojbajaj95/cl/pull/331
[PR #334]: https://github.com/manojbajaj95/cl/pull/334
[PR #335]: https://github.com/manojbajaj95/cl/pull/335
[PR #114]: https://github.com/manojbajaj95/cl/pull/114
[PR #123]: https://github.com/manojbajaj95/cl/pull/123
[triage]: https://github.com/manojbajaj95/cl/blob/4c99a4b6fa616f5e753541ba7611a1836d8d6628/reviews/flood-triage.md#L449-L454
[top10]: https://github.com/manojbajaj95/cl/blob/4c99a4b6fa616f5e753541ba7611a1836d8d6628/reviews/flood-top10.md#L11
[ledger]: https://github.com/manojbajaj95/cl/blob/4c99a4b6fa616f5e753541ba7611a1836d8d6628/reviews/idea-ledger.md
[inversions]: https://github.com/manojbajaj95/cl/pull/72
[nerode]: https://github.com/manojbajaj95/cl/pull/104
[ebbinghaus]: https://doi.org/10.1371/journal.pone.0120644
[hinton]: https://www.cs.toronto.edu/~hinton/absps/fastweights87.pdf
[Spurious Forgetting]: https://arxiv.org/abs/2501.13453
[Benign Relearning]: https://arxiv.org/abs/2406.13356
[Syntax Relearning]: https://arxiv.org/abs/2602.03379
[MAML]: https://arxiv.org/abs/1703.03400
[La-MAML]: https://arxiv.org/abs/2002.09571
[Automated CL]: https://arxiv.org/abs/2312.00276
[NTK]: https://arxiv.org/abs/1806.07572
[NTK Overlap]: https://arxiv.org/abs/2010.04003
[Mode Connectivity]: https://arxiv.org/abs/1802.10026
[Git Re-Basin]: https://arxiv.org/abs/2209.04836
[Synthetic Gradients]: https://arxiv.org/abs/1608.05343
[Modular Solutions]: https://arxiv.org/abs/2312.15001
[Learning Where]: https://arxiv.org/abs/2110.14402
[Gradient Projection Memory]: https://arxiv.org/abs/2103.09762
[Dataset Distillation]: https://arxiv.org/abs/1811.10959
[Dataset Trajectories]: https://arxiv.org/abs/2203.11932
[Rate–Distortion]: https://arxiv.org/abs/0901.1705
[Learning to Learn]: https://arxiv.org/abs/1606.04474
[Net2Net]: https://arxiv.org/abs/1511.05641
[Composable Expansions]: https://arxiv.org/abs/2308.06103
[Learning Equivariance]: https://arxiv.org/abs/2512.21447
[PCGrad]: https://arxiv.org/abs/2001.06782
[Task Arithmetic]: https://arxiv.org/abs/2212.04089
[Provable Repair]: https://arxiv.org/abs/2304.03496
[Error Feedback]: https://arxiv.org/abs/1901.09847
[Certified CL]: https://arxiv.org/abs/2407.06697
[Nonparametric Machine Teaching]: https://arxiv.org/abs/2306.03007
[Functional Regularisation]: https://arxiv.org/abs/1901.11356
[Distilling Knowledge Updates]: https://arxiv.org/abs/2306.09306
[Synaptic Intelligence]: https://arxiv.org/abs/1703.04200
[Continual Backprop]: https://arxiv.org/abs/2306.13812
[Influence Functions]: https://arxiv.org/abs/1703.04730
