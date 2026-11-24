# Description-built partners

**Status:** Ideas only. No experiments, probe code or GPU; two hand-checked paper witnesses. **Parent:** [Cancelling release counterweights](cancelling-counterweights.md) ([PR #208](https://github.com/manojbajaj95/cl/pull/208)), card 02. **Review seed:** [flood triage row 319](https://github.com/manojbajaj95/cl/blob/78c09a6263dafb1cad2c8afd9c6f53cca97c819c/reviews/flood-triage.md#L319), the one score-3 idea for PR #208: *compile a partner address that shaping never saw.* Learn a map from a public reader/slot description to the signed contribution it needs. Register a new counterpart at a fresh physical address by neutrally reallocating that address's own local survivors. Join it with a previously shaped address without any historical edge list, under fixed capacity. The reviewer's controls are a memoized edge table at equal bytes, #198#06 interface matching, exact repair, re-shaping on the new pair, a matching-description address whose hidden reader differs, and A/C retention.

**Can a learner turn a description of an address it has never touched into a working, neutral counterweight for an address it shaped earlier, with no stored pairing table and no extra capacity?** If so, compatibility stops being a remembered fact about specific pairs and becomes a compiled property of descriptions. Every component already exists somewhere. Hypernetworks emit weights from descriptions ([Text-to-LoRA 2506.06105](https://arxiv.org/abs/2506.06105), [Universal Hypernetworks 2604.02215](https://arxiv.org/abs/2604.02215), [Internalizer 2610.11715](https://arxiv.org/abs/2610.11715), [MOSAIC](https://www.alphaxiv.org/abs/2611.mosaic-continual-lora-merging)). [Zero-shot tokenizer transfer 2405.07883](https://arxiv.org/abs/2405.07883) predicts embeddings for tokens it never saw. Weight-space metanetworks transfer across architectures ([Transferable Graph Metanetworks 2610.00420](https://arxiv.org/abs/2610.00420), [NeuMeta 2410.11878](https://arxiv.org/abs/2410.11878)). [Net2Net](https://arxiv.org/abs/1511.05641) and [Neuron Merging 2010.13160](https://arxiv.org/abs/2010.13160) make function-preserving width changes. [Consistent hashing](https://dl.acm.org/doi/10.1145/258533.258660) and [rendezvous hashing](https://doi.org/10.1109/90.663936) let new nodes join without a global table. The candidate is narrower: an **edit-local registration** that spends a fresh address's own spare capacity to create a signed residual, so that a *later* joint release with an old address becomes legal where no singleton release is. The descriptor map supplies the sign and shape; the registration has to be neutral, local and capacity-neutral.

## What would count?

- **Compiled, not recalled.** Pairing information must reach a fresh address only through its public description and the learned map. Charge every map parameter, descriptor byte, cache entry and proof as bytes. Witness W2 sets the floor: a table for an arbitrary perfect matching on `2N` addresses needs `log₂((2N−1)!!)` bits (21.0 bits at N=8, 146.3 at N=32, 839.8 at N=128). A map of B bits can realize at most `2^B` matchings. So the claim is only possible on compatibility relations of low description complexity, and an edge shuffle with fixed marginals *must* break the map while leaving the table's cost unchanged. A map that survives the shuffle is reading something other than the description.
- **Local registration that is not mere donation.** Witness W1 shows that in an open additive head, registering a counterweight at fresh address *j* by using *j*'s spare unit equals simply donating that spare unit to absorb the old partner's residual directly. The idea counts only under a declared **edit-locality contract**: an edit at address *j* may rewrite only units at *j*, and a release may write only to the declared global survivors. Report every result under both the local and the open editor, and claim value only where the open editor's direct donation is illegal or more expensive.
- **The description has to determine the reader.** Two addresses with identical public descriptions but different hidden readers on the protected domain must get the same predicted contribution, so at least one is wrong. Every test includes such decoys and scores the refusal path. A registration that publishes on a decoy is a retention failure, not a miss.
- **Fixed capacity, real use.** No new units, no wider precision, no growth of the survivor pool. The registration consumes spare units at *j* that would otherwise be idle; price them at their best alternative use (a direct write, a donation, a reserve). Use both vacated addresses after the joint release for genuine new writes, and score target utility.
- **Beat the strongest stack.** Controls are the reviewer's list plus the components above: a memoized edge table at equal bytes, a hypernetwork that predicts the full new-address weights (no neutral registration), consistent/rendezvous hashing over descriptors, #198#06 interface equations, exact joint repair given the descriptor, re-shaping on the new pair, and direct spare-unit donation when legal. Score paired success, refusals, bytes, proof/search cost and failed attempts.
- **Retention.** A is the legacy tasks; C is every accepted write plus downstream readers, including the fresh address's original readers. Registration must be exactly neutral on the declared A/C domain at deployed precision, checked again after the joint release and after both vacated addresses are spent. The [idea ledger](https://github.com/manojbajaj95/cl/blob/78c09a6263dafb1cad2c8afd9c6f53cca97c819c/reviews/idea-ledger.md) rules out a readiness/Gramian score as the map's target, gauge-only memory that a rebalance erases, results true by construction, and gains that equal-budget replay or save/restore ties. Its hypernetwork-CL entries also mean that "a hypernetwork emits adapters" is not itself new.

### Witness W1: registration is donation unless edits are local

Additive protected head on `x ∈ [0,1]³` with coefficient vectors over `(x₁, x₂, x₃)`. A global survivor `s` can carry any combination of `x₁, x₂` but not `x₃`. A previously shaped address `a` contributes `x₁ + x₃` (its `p + r`, with `r = x₃`). A fresh address *j* has a releasable slot `b` contributing `x₂` (its `q`), whose unit features span `{x₂, x₃}`, and one dormant local spare unit `s_b` that reads `x₃`, with coefficient bound `|w| ≤ 1` and current weight `0`.

- **Open editor** (a release may write any survivor): `a` releases alone by sending `x₁` to `s` and `x₃` to `s_b`. No counterweight is needed, and compiling one only re-labels the donation.
- **Local editor** (a release writes only to `s`; an edit at *j* touches only `b` and `s_b`): `a` cannot release alone, because `s` cannot hold `x₃`. Registration at *j* is a local, neutral edit: `b → x₂ − x₃`, `s_b → +x₃`, and the total is unchanged. The joint release of `a` and `b` then removes `(x₁ + x₃) + (x₂ − x₃) = x₁ + x₂`, which `s` absorbs. Both addresses are vacated, and *j*'s spare capacity has served `a` without a non-local write. `a` alone is still impossible after registration. `b` alone is possible only by undoing the registration (`s_b → 0`), another local edit.

These coefficient identities were checked mechanically. The witness fixes the object: the counterweight is a *capacity bridge across an edit-locality boundary*. The descriptor map's job is to predict `r = x₃` from *j*'s public description before anyone has paired *j* with `a`. Without a locality contract, the whole idea collapses to spare-unit donation.

### Witness W2: a pairing-free map needs a low-complexity compatibility relation

Counting perfect matchings, a stored table that supports an arbitrary partner assignment on `2N` addresses needs `log₂((2N−1)!!)` bits. Any map with B bits of parameters plus descriptors realizes at most `2^B` assignments. "No stored pairing table" is therefore a statement about the *relation*, not the learner. The compatibility of `(a, j)` has to be computable from their descriptions by a short program, as in W1 where *j*'s description exposes that `b` reads `x₃`. This gives the decisive control for free: re-pair addresses at random with marginals and timing fixed. The table pays the same bytes and keeps working. The map's paired success must fall to the hidden-reader decoy floor, or the map is leaking an ID.

## Idea cards

### Compile the counterpart

#### 01. Signed-contribution map from reader descriptions
- **Mechanism:** Train `g(desc_j) → r̂_j`, the signed residual that address *j* must carry to cancel some shaped partner's `r`, from (description, solved residual) pairs on shaped addresses. At first contact, run the W1 local registration with `r̂_j` and verify neutrality before publishing.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Text-to-LoRA and zero-shot tokenizer transfer emit weights for unseen inputs but never under a neutrality constraint, and never to set up a later joint release. The new object is a description-conditioned, function-preserving registration.
- **Cheapest first test:** A linear additive head with 64 addresses, whose descriptions are the reader feature sets plus noise. Withhold a bank of 16 addresses entirely. Compare against a hypernetwork that emits full weights, exact joint repair given the descriptor, and an equal-byte edge table. Run under both local and open editors.
- **Old-task retention check:** Exact old-head coefficients on all protected inputs after registration, after the joint release and after the vacated addresses are spent. The bank's original readers are exercised before and after.

#### 02. Registration as a two-unit neutral move
- **Mechanism:** Restrict registration to the minimal local move from W1: put `−r̂` on the releasable slot and `+r̂` on one local spare. This makes the registration auditable as a single rank-one neutral transfer inside *j*.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Net2Net and Neuron Merging preserve function while *changing width*. This preserves function at *fixed* width to create a releasable signed imbalance.
- **Cheapest first test:** Enumerate small integer heads and find every address where the two-unit move is legal. Compare the release coverage it buys with an unrestricted local neutral search at the same spare budget.
- **Old-task retention check:** A bit-exact neutrality check of the two-unit move at deployed precision, including the saturation boundary of the spare's coefficient bound.

#### 03. Refuse on underdetermined descriptions
- **Mechanism:** Pair `g` with a learned *determinacy test*. The description must pin the reader's action on the protected domain to within the decision margin. Otherwise refuse and fall back to exact repair.
- **Novelty vs nearest prior art — IMPROVEMENT:** Selective prediction and abstention exist. The added value is a refusal calibrated to a *neutrality* loss, not to prediction error.
- **Cheapest first test:** Plant hidden-reader decoys with identical descriptions at 10/30/50% rates. Measure published-but-wrong registrations, refusal rate, and service against always-repair.
- **Old-task retention check:** No published registration may change any A/C output, and refused registrations leave *j* untouched.

#### 04. Edge-shuffle falsifier as a built-in gate
- **Mechanism:** Deploy the map only if its paired success on a randomly re-paired twin history (same marginals and timing) falls to the decoy floor, and certify this once per family.
- **Novelty vs nearest prior art — AUDIT:** W2 makes it necessary. No hypernetwork paper reports it, because none claims pairing-free compatibility.
- **Cheapest first test:** Build the twin histories from card 01's world. Report the gap between true and shuffled paired success for the map and for the table. Only the map should collapse.
- **Old-task retention check:** Run the shuffled-history map with publication on, and confirm that every wrong registration is caught by the neutrality check before it reaches A/C.

#### 05. Description-complexity curve
- **Mechanism:** Vary the Kolmogorov-style complexity of the compatibility relation (descriptor-determined → partly random → fully random) and measure where the map's bytes cross the table's.
- **Novelty vs nearest prior art — IMPROVEMENT:** Learned index structures ([Kraska et al. 2018](https://arxiv.org/abs/1712.01208)) chart the same break-even for key lookup. Here the value is a fixed-capacity *write* that has to be neutral, not a lookup.
- **Cheapest first test:** Mix a descriptor rule with a fraction ρ of random exceptions. Compare map + exception table against a pure table at equal bytes, sweeping ρ.
- **Old-task retention check:** The exceptions are handled by the table. Check that exception addresses never receive a map-built registration.

### Make locality the resource

#### 06. Locality-bridged capacity
- **Mechanism:** Treat the counterweight as the only legal way for *j*'s spare to serve `a` under edit locality (W1). Learn which shaped addresses are *bridgeable* from a description of *j*'s spare features.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Parent card 08 routes unsigned sums across a shared pool. Here the bridge crosses an edit-locality boundary that no single release can cross, and a learned map finds it at first contact.
- **Cheapest first test:** Run W1 at scale: 32 shaped addresses with distinct `r`, and 16 fresh addresses whose spares read different subsets. Compare against the open-editor donation optimum, which is an upper bound and not a competitor, and against local exact search.
- **Old-task retention check:** Recheck A/C after each bridge and confirm that no spare consumed by a bridge was serving an accepted write.

#### 07. Price the spare at its best alternative use
- **Mechanism:** Register only when the release enabled by the bridge beats *j*'s best local use of the same spare (a direct write for an incoming task, or a held reserve).
- **Novelty vs nearest prior art — IMPROVEMENT:** Opportunity-cost pricing is standard. It is required here so that the map's gains are not just idle capacity being counted as free.
- **Cheapest first test:** Stream writes that compete for *j*'s spare. Compare register-on-contact, never-register and exact offline value.
- **Old-task retention check:** Run A/C and the competing writes' targets after each choice.

#### 08. Locality contracts that come from real hardware or sharding
- **Mechanism:** Use a locality contract the deployment actually has, such as tensor-parallel shards, per-expert ownership in an MoE, or per-adapter write permissions. Ask whether description-built partners relieve cross-shard release cost.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Expert-parallel and shard-local training exist. Using shard ownership as an edit contract that makes signed residuals worth having is not reported.
- **Cheapest first test:** A toy two-shard MLP in which each shard's editor writes only its own units and the global survivor is a shared bias head. Count releases that need cross-shard communication with and without registrations.
- **Old-task retention check:** Old outputs stay unchanged across both shards after each registration and joint release.

#### 09. One fresh address bridging several old ones
- **Mechanism:** *j* has k spares. Learn a description map that outputs a k-sparse set of signed residuals, so that *j* can later join any of several shaped partners, one at a time.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Parent card 21 shares one opening between two finishes. Here one registration exposes several mutually exclusive joins built from one description.
- **Cheapest first test:** Vary k from 1 to 3 and measure join coverage per spare against k independent single registrations and against exact repair.
- **Old-task retention check:** Check every exposed join's release path on A/C, as well as the state after one join pins *j*.

#### 10. Counterweight under a nonlinear reader
- **Mechanism:** Replace the additive head with a ReLU readout. Registration has to cancel across the protected cell arrangement (parent card 04), and the map predicts a piecewise residual.
- **Novelty vs nearest prior art — IMPROVEMENT:** APRNN ([2304.03496](https://arxiv.org/abs/2304.03496)) repairs finite cells. The map is the new part, and only if it generalizes across cells.
- **Cheapest first test:** One-dimensional segmented nets, with a decoy carrying a narrow extra hinge between probes. Compare against full piecewise-linear repair.
- **Old-task retention check:** Verify every protected cell and the planted hinge after the registration and after the release.

### Learn the map honestly

#### 11. Train the map only from solved neutral moves
- **Mechanism:** Supervise `g` on residuals produced by exact neutral solves, never on observed pairings, so the map cannot memorize IDs.
- **Novelty vs nearest prior art — AUDIT:** This addresses the leak W2 predicts. Hypernetworks trained on (task, adapter) pairs can memorize task identity.
- **Cheapest first test:** Train two maps, one on solves and one on pair labels. Compare their gap on the shuffle falsifier (card 04).
- **Old-task retention check:** Only verified registrations publish, and A/C is checked as in card 01.

#### 12. Equivariant descriptors
- **Mechanism:** Encode descriptions with permutation- and rescaling-equivariant metanetworks, so that relabelled or rebalanced addresses get the transported residual (parent card 03).
- **Novelty vs nearest prior art — IMPROVEMENT:** Neural functionals and graph metanetworks (2610.00420) already handle symmetry. This is a transfer audit against the ledger's Noether kill.
- **Cheapest first test:** Rebalance a host function-preservingly. Compare equivariant and plain maps on registration accuracy at the moved addresses.
- **Old-task retention check:** Re-verify neutrality on the rebalanced host before and after registration.

#### 13. Map distillation from exact repair traces
- **Mechanism:** Distil the exact joint-repair solver's outputs on shaped pairs into `g`, then measure what the map recovers on new banks per byte and per unit of solver time.
- **Novelty vs nearest prior art — IMPROVEMENT:** This is amortized optimization ([survey 2202.00665](https://arxiv.org/abs/2202.00665)). It is novel only if amortization beats proof-sharing exact repair at equal service.
- **Cheapest first test:** Use solver-time break-even curves. Include a world where exact repair is cheap; the map should lose there.
- **Old-task retention check:** The same A/C checks as for exact repair, on every published registration.

#### 14. Online map updates without a history buffer
- **Mechanism:** Update `g` from each verified registration and discard the pair, so no edge list builds up even during training.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Online hypernetwork CL (MOSAIC, 2610.15677) stores task-conditioned adapters. Here the stored object is only the compiler.
- **Cheapest first test:** Stream 200 registrations and compare against a map retrained on a growing buffer and against an equal-byte table that evicts old entries.
- **Old-task retention check:** A map update must not change any already-published registration. Re-verify old registrations after each update.

#### 15. Descriptor bytes as the bottleneck
- **Mechanism:** Learn the shortest public descriptor that still determines the residual, an information bottleneck on what the fresh address has to announce.
- **Novelty vs nearest prior art — IMPROVEMENT:** This is an application of the information bottleneck. It is useful because it makes the W2 byte accounting concrete.
- **Cheapest first test:** Sweep descriptor length and plot paired success against total bytes (descriptor + map) next to the table.
- **Old-task retention check:** At each length, decoys must still be refused (card 03).

### Stress and retention

#### 16. Stale descriptors after a true acquisition
- **Mechanism:** When a later task adds a reader at *j*, *j*'s description changes. Invalidate only the registrations whose residual depended on the changed part (parent card 07).
- **Novelty vs nearest prior art — IMPROVEMENT:** Version-keyed invalidation is standard. The test is whether description-level dependencies cut recertification cost.
- **Cheapest first test:** Add a reader that separates one previously registered pair and leaves another unchanged. Compare against whole-bank recertification.
- **Old-task retention check:** Run legacy tasks and the new reader after the attempted release, and confirm the stale pair is refused.

#### 17. Adversarial descriptions
- **Mechanism:** An address announces a description that makes the map build a registration that is neutral at the cut but harmful downstream, and the map has to refuse.
- **Novelty vs nearest prior art — AUDIT:** This parallels backdoor and poison audits. Neutrality verification is the defence, and the map must never bypass it.
- **Cheapest first test:** Plant descriptions that differ from the true reader only off the protected probes. Measure false publishes with and without full-domain verification.
- **Old-task retention check:** Full-domain A/C on every published registration, including off-probe inputs.

#### 18. Quantized registration
- **Mechanism:** Compile `±r̂` at deployed precision, so that the two-unit move cancels bit-exactly (parent card 09).
- **Novelty vs nearest prior art — AUDIT:** This checks whether apparent transfer depends on extra bits.
- **Cheapest first test:** int8 blocks with a saturation decoy. Compare real-valued registration rounded afterwards against operand-aware registration.
- **Old-task retention check:** Bit-exact old outputs at boundary inputs.

#### 19. Registration that does no harm when no partner ever comes
- **Mechanism:** If no shaped partner ever joins *j*, the registration has to be cheaply reversible, or worth more than its idle cost, under the same locality.
- **Novelty vs nearest prior art — IMPROVEMENT:** Parent card 15 covers retiring options. This card prices speculative registrations.
- **Cheapest first test:** Vary the arrival probability of a partner. Compare register-on-contact, register-on-demand, and exact repair at join time.
- **Old-task retention check:** Undo is a local neutral edit; check A/C after the undo.

#### 20. Rival hidden readers behind one description
- **Mechanism:** Two populations share descriptions but differ in hidden readers at a base rate π. Learn the π-dependent threshold at which registering beats refusing.
- **Novelty vs nearest prior art — IMPROVEMENT:** This is a decision-theoretic extension of card 03.
- **Cheapest first test:** Sweep π. Compare against oracle-reader registration and always-repair.
- **Old-task retention check:** Every wrong-reader registration has to be caught before publication, so no A/C change ever reaches deployment.

### Compete with the stack

#### 21. Map + table hybrid at equal bytes
- **Mechanism:** Let the map cover the low-complexity part of the relation and a small table cover the exceptions (card 05), and ask whether the hybrid beats the best pure method at every ρ.
- **Novelty vs nearest prior art — IMPROVEMENT:** Hybrid learned indexes exist. The test is whether the hybrid helps neutral writes.
- **Cheapest first test:** The card 05 sweep with the hybrid added.
- **Old-task retention check:** As in cards 01 and 05.

#### 22. Description-built partners plus a shared opening
- **Mechanism:** Combine with parent card 21. A fresh address registered from its description becomes one of the two finishes of an already-published opening.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** The claim holds only if a first-contact registration supplies a finish the opening could not have prepared. That is an interaction the stacked baselines cannot reproduce.
- **Cheapest first test:** Run the parent's paper witness with `b₁` replaced by an address that was never seen during shaping. Compare against a paid wider menu and exact online replanning.
- **Old-task retention check:** B₁ stays live throughout, and A/C is checked on both branches and on the refusal path.

## Ranked deeper questions

1. **Does a description-conditioned registration beat an equal-byte edge table and exact repair *under an explicit edit-locality contract*, while collapsing on shuffled histories?** Start with cards 01, 04, 06 and 11 on W1-style worlds. Require a paired-service win at matched bytes, a collapse under the shuffle falsifier, and correct refusals on decoys. If the open-editor donation is legal and ties, report the locality observation only.
2. **What locality contracts exist in real models that make signed residuals worth having?** Start with cards 08 and 07. Shard or expert ownership and per-adapter permissions are candidates. If no realistic contract forbids direct donation, the primitive has no deployment and stays a toy feasibility result.
3. **Where is the break-even between compiling and memoizing?** Use cards 05, 15 and 21 to trace bytes against relation complexity. A map is worth keeping only in the region W2 allows, and the curve should show that region directly rather than through averages.
4. **Do nonlinear readers keep the description → residual map low-complexity?** Use cards 10, 12 and 18. If piecewise readers make the residual a high-complexity function of the description, the map degenerates to a table and the novelty claim ends.

**Verdict:** Keep the idea as a falsifiable PRIMITIVE CANDIDATE with two preconditions taken from the witnesses. There must be an edit-locality contract under which direct spare donation is illegal (W1), and a low-complexity compatibility relation that a shuffle can break (W2). Without both, a description-built partner is either spare-unit donation or a compressed edge table, and the reviewer's equal-byte memoized table plus exact repair should tie it.
