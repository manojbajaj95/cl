# Non-neural learners: Synonymous mutability coding and flow-borne writes

Child of [Continual Learning from Non-Neural Learners](root-non-neural-learners.md) ([PR #338]) · 26 idea cards · Ideas only; CPU tests proposed, none run

The [reviewer's score-3 entries][triage] on [PR #6] were **NNL01**, compiling confirmed and uncertain clauses into equally functional but differently mutable forms, and **NNL07**, carrying a write signal through the same flow that serves inference. Neither changed the reviewer's top 10. NNL01 overlaps with the gauge-orbit channel in [PR #53], but the blind editor, not a metadata reader, acts on the difference. NNL07 asks whether *where and when a conserved pulse arrives* matters more than local traffic volume. We take the parent's 95:5 rare-task assay, not dormant experts or replay, as a test. The [idea ledger][ledger] rules out counting exact restore, simple replay ties, or a new name for an existing method as progress.

## Two exact witnesses, not continual-learning results

**NNL01: same function, different write hazard.** Let a three-bit clause's output be majority and let the editor flip one uniformly selected bit. Both `000` and `001` decode to zero. From `000`, no one-step proposal changes the output; from `001`, two of three proposals do. The separation lasts only as long as the relevant neighborhood does: if both proposals are blindly committed, the two-step exit probability starting from `000` is 2/3. In a general fixture with read function $f$ and fixed proposal kernel $K$, compare the *distribution of decoded proposals* from $x$ and $y$ with $f(x)=f(y)$, not just the odds of any change. If $K$ has the same total transition probability from every synonym to each decoded class ([strong lumpability][Lumpability]), recoding cannot change this one-step distribution; the whole decoded chain is then the same without additional state-dependent acceptance. The majority example is ordinary redundancy; it proves neither novelty nor an advantage over a freeze mask.

**NNL07: same edge traffic, different write location.** Take two parallel two-hop lanes with unit traffic on each edge at each tick. Release one pulse unit into the left or right lane entrance at tick zero. In a one-hop-per-tick conserved transport model, the corresponding second edge, and only that edge, gets a crossing at tick one. For a capacity update proportional to pulse crossings with slack budget, the second-edge increments swap; an updater given only local flow and identical local starting state cannot tell the cases apart. A message-passing updater given the source and flow can reproduce this exactly. The witness isolates missing information in the flux-only baseline, not an advantage over a strong router.

## Shared CPU-first contract

- **Stream and retention.** Use A and rare B at 95:5, then C and D with no B refresh, then a held-out A/B return. B must be learned before the split into arms. A/B tests are read-only: never use their labels or their test traffic for updates. Interleave held-out checks after installation and during C/D, not just at the end. Report A and B separately (worst slice as well as rate), C/D adaptation latency at matched retention, and retention at matched C/D adaptation. Use observable inputs, no task IDs or future confirmation. Confirmation comes from past training evidence; include a false-confirmation condition.
- **Blind edits, not blind accounting.** For NNL01 fix the edit operation, proposal draw and acceptance budget across synonymous arms. Start with uniform coordinate flips; distinguish uniform proposals from post-selection writes. Check exact equivalence across the entire bounded read domain before and after a *recoding*, and count invalid proposals as wasted work, not protection. Include a tunable explicit freeze mask or EWC where a differentiable baseline exists; also include an adaptive per-clause edit-rate table, unequal-error-protection coding, uncoded uniform edits, random synonyms, and hot/cold assignments shuffled against confirmation. A mask is allowed to thaw with the same evidence. Charge the decoder/compiler, rewrite work, confirmation state, persistent bits and peak scratch; no cheap hidden codebook.
- **Advection, not an outcome broadcast.** For NNL07 use a finite graph; traffic determines the split of packets across outgoing edges, with one hop of delay per tick unless stated otherwise. Account for every pulse unit as in transit, arrived at a designated sink, or explicitly dissipated; do not copy it at branches. Conductance receives feedback only from local pulse passage (including the paired normalization budget if used). Use a shared prompt-free input and feedback interface; all arms get the same release observations. Compare against [flux reinforcement][Tero] with no advection, a source-aware equal-byte Hebbian routing table, a gradient-trained router, and shuffled pulse-to-edge/time assignments with budgets and relevant marginals conserved. Also test a non-advected diffusion or replayed-path arm where it could explain the gain. Count messages, rounding residuals, conductance/trace state, solver steps and feedback delay. Report realized traffic and initial matched-flow interventions; don't assume traffic stays matched after a write changes the graph.

## Literature check

Targeted web searches covered neutral genotype-to-phenotype search, unequal protection and local update codes, semantics-preserving program transformations, and adaptive routing with or without transport. The linked original papers or their publisher abstracts establish the comparisons below. [Toussaint & Igel][Neutrality] already show that neutral encodings change the offspring distribution without a phenotype change; [Rothlauf & Goldberg][Redundancy] study synonymously redundant representations, and [The Evolvability of Programmable Hardware][Hardware] finds functionally identical circuits with different mutational robustness. This rules out claiming that choosing a more robust synonym is new by itself. [Kramar & Alim][Hierarchy] already use a transported softening signal to write a tube-diameter hierarchy; [Alim et al.][Propagation] already model a flow-borne signal that changes the flow carrying it. The candidate gaps are about continual allocation of editability and old-route service under bounded writes, not priority claims about either mechanism.

## A · NNL01: Compile the blind editor's behavior

### SM01 · Reassign protection without changing the clause — IMPROVEMENT
- **Mechanism:** Recode a clause from a boundary synonym to an interior synonym when independent observations confirm it; thaw it by the inverse type of move when fresh counterevidence arrives. This is an adaptive protection policy, not a new error-correcting code.
- **Nearest prior / gap:** [Unequal Error Protection][UEP] protects selected digits; [Neutrality] changes search distributions via neutral state. The question is whether reallocating protection online inside one fixed decoder is cheaper than changing explicit policies.
- **Cheapest first test:** Enumerate three-bit majority blocks, then shift which block needs revision without announcing it. Compare with adaptive unequal protection and a mask; reject if recoding does not move the adaptation/retention frontier.
- **Old-task retention:** Score unchanged A clauses and a confirmed rare B clause after C and D, including while a falsely confirmed C clause thaws.

### SM02 · Directional synonym write — PRIMITIVE CANDIDATE
- **Mechanism:** Choose among synonyms of the same current action with equal total escape rates but different *destinations* of escapes. Install a directed next-write preference without making the incumbent more or less fragile overall.
- **Nearest prior / gap:** [Phenotypic Exploration][Exploration] already describes structured offspring distributions. The candidate operation is an addressed change of one clause's outgoing edit odds under a frozen shared kernel, with collateral odds held fixed.
- **Cheapest first test:** Exhaust tiny ternary-output codebooks for twins with equal Hamming-neighbor escape counts and opposite next-action biases. Then compare corrective samples-to-adoption against a cached directional edit table.
- **Old-task retention:** Verify B when it shares input support with the edited clause and A when neither correction should fire; test both intended and wrong future directions.

### SM03 · Switch coherent bundles, not single bits — PRIMITIVE CANDIDATE
- **Mechanism:** Choose a synonym whose one-edit neighbors change two linked clauses together but leave a third fixed. Write a permitted pattern of co-edits rather than independent edit rates.
- **Nearest prior / gap:** [Phenotypic Exploration][Exploration] already adapts mutation correlations. Test whether a writer can prescribe one useful correlation, independent of others, at lower cost than a block editor.
- **Cheapest first test:** Search a six-bit decoder for joint-edit and independent-edit synonyms with matched per-clause marginals. Compare against explicit grouped edits and a covariance table.
- **Old-task retention:** Track A/B cases that observe one clause at a time and cases that depend on their agreement during partial C/D rollouts.

### SM04 · Prefix-selective coldness — IMPROVEMENT
- **Mechanism:** Select synonyms using the probability of *first exit by edit horizon* rather than one-step neutrality. Two identical launch hazards can conceal different paths through the neutral region.
- **Nearest prior / gap:** [Lumpability] explains when aggregated transitions lose dependence on the carrier state. This is a horizon-aware policy for choosing that state, not a new Markov reduction.
- **Cheapest first test:** Find two synonyms with identical one-step decoded distributions but different three-step survival by exact enumeration. Compare to a timer-controlled edit mask with the same feedback and state budget.
- **Old-task retention:** Count the first A or B error during a burst of edits, including errors that would be missed by scoring only after C/D.

### SM05 · Moving protection on a fixed-size substrate — IMPROVEMENT
- **Mechanism:** Pack multiple clauses into one fixed-width word. Change representatives to move some protection from a previously volatile clause to B without changing any decoded answers or increasing word size.
- **Nearest prior / gap:** [Unequal Error Protection][UEP] already allocates redundancy unevenly. The test is the cost and losses of *retargeting roles* inside a shared codebook rather than switching codes.
- **Cheapest first test:** Enumerate two-bit payloads in six-bit words; find the nondominated hazard vectors across synonyms. Compare to an explicit role permutation plus the best static unequal-protection code.
- **Old-task retention:** Report A's lost protection as well as B's gain; require both to serve correctly through C/D before calling the trade worthwhile.

### SM06 · Semantic coldness across editor swaps — IMPROVEMENT
- **Mechanism:** Choose a representative that minimizes the worst old-output hazard over two ordinary editors, such as a token swap and a literal substitution. It must still admit useful new-task edits.
- **Nearest prior / gap:** [Genetic Programming with Proof Search][GP Proof] maintains semantics under specified transformations. Here semantics-preserving compilation is used to shape the response to two *non*-preserving editors.
- **Cheapest first test:** Exhaust bounded Boolean expressions and evaluate both kernels exactly; swap the editor midstream. Compare with separately tuned masks and an editor-agnostic protection code.
- **Old-task retention:** Measure old A/B corner cases immediately after the swap and over the first ten C updates, not after selecting a new compiler.

### SM07 · Compile a cap on semantic blast radius — PRIMITIVE CANDIDATE
- **Mechanism:** Route high-impact clauses through equivalent shared or factored subexpressions so one blind edit may modify nearby decisions but is unlikely to affect two old service slices at once.
- **Nearest prior / gap:** [Semantic GP][Semantic GP] studies the locality of mutations; [egg] represents equivalent programs. The gap is selecting an equivalent program by a *joint* old-service tail constraint, at matched marginal error and adaptation.
- **Cheapest first test:** Enumerate hand-sized Boolean DAGs and count edits affecting both old slices. Compare to subtree isolation, equal-width duplication, and selection by average semantic locality.
- **Old-task retention:** Record worst A and B errors per proposal and the probability both fail on the same committed edit during C/D.

### SM08 · A cheapness bound for thawing — IMPROVEMENT
- **Mechanism:** Compile confirmed clauses into low-exit states only when a short function-preserving path leads back to an editable boundary. Bound neutral steps required to reopen write access.
- **Nearest prior / gap:** [Locally Updatable Codes][LULDC] already trade update cost against correction. This is an online policy over *same-payload* transitions under a constrained editor.
- **Cheapest first test:** Breadth-first search synonym graphs for cold states with and without short neutral exits. Give a thawing mask the same confirmation events and compare correction latency, including installation cost.
- **Old-task retention:** During a real A correction, score unchanged A anchors and rare B at every intermediate step, including failed thaw attempts.

### SM09 · Spend write tolerance on likely colliding tasks — PRIMITIVE CANDIDATE
- **Mechanism:** Estimate which clauses C's blind edit stream touches from ordinary proposals. Recode protected A/B so edits affecting those functions intersect the active C neighborhood less often, not merely so their global hazards fall.
- **Nearest prior / gap:** [EWC] penalizes changes to important parameters. The candidate is a semantics-preserving rearrangement that changes conditional interference *before* optimization, without supplying importance to the blind editor.
- **Cheapest first test:** Use two C objectives with identical global edit volume but opposite accepted neighborhoods. Compare to proposal-matched EWC or an interference-aware explicit per-clause rate table, including the cost of learning where proposals land.
- **Old-task retention:** Score A and B during both C objectives and a D objective with reversed overlap; report whether protecting one old slice displaced damage to the other.

### SM10 · Two bounded writers with different legal edits — PRIMITIVE CANDIDATE
- **Mechanism:** A synonymous write makes a clause cold to one fixed editor but hot to another while both read the same function, allowing cheap correction by one maintenance process without a policy check by the other.
- **Nearest prior / gap:** [Neutrality] gives state-dependent exploration and [WOM Codes][WOM] constrain permissible rewrites. The gap is separately tuning the effects of two already deployed editors; this is update reliability, not access control.
- **Cheapest first test:** Give one editor adjacent swaps and one bit flips; search equal-width exact twins for opposite hazards. Compare to two explicit masks and a representation with separate write regions.
- **Old-task retention:** During interleaved C maintenance, ensure B survives the high-volume editor; during an authorized-by-protocol A correction score unaffected A and B against the same deadlines.

### SM11 · Distinguish neutral drift from live counterevidence — IMPROVEMENT
- **Mechanism:** Recenter a neutral code only if the stream has not supplied enough evidence to revise it. A fresh correction must be able to exploit boundary states instead of having every neutral change undone.
- **Nearest prior / gap:** [Unequal Error Protection][UEP] addresses correction of channel errors; the proposed policy decides whether to recenter when the same edit process also serves learning.
- **Cheapest first test:** Alternate bursts of corrupt feedback with sustained genuine reversals in a small online rule learner. Compare to periodic hard scrubbing plus a change detector and a same-byte adaptive risk table.
- **Old-task retention:** Test early A/B decay during noise, and retain rare B while a superficially similar A rule legitimately reverses.

### SM12 · Let proof reuse pay for recoding — IMPROVEMENT
- **Mechanism:** Keep a bounded repertoire of exact rewrites. Reuse rewrite derivations across a family of clauses when selecting low-hazard syntax, rather than solving each synonym search anew.
- **Nearest prior / gap:** [egg] already shares equivalences efficiently, and [GP Proof] derives semantics-preserving transforms. The target is amortized scoring by edit hazard, not a new equivalence engine.
- **Cheapest first test:** Give an e-graph extractor a small clause family and equal wall-clock budgets for hazard search versus adaptive masks. Charge the shared rewrite/equivalence engine and reject if it only wins when startup is free.
- **Old-task retention:** Test unseen A/B inputs authorized by the same finite semantics, including a rare B clause that does not reuse the common rewrite.

### SM13 · Survive an ordinary canonicalizer — IMPROVEMENT
- **Mechanism:** Constrain compilation to synonyms that remain distinguishable to the mutation kernel after the storage/runtime's real normalization pass. If normalization collapses a class to one representative, there is no carrier there.
- **Nearest prior / gap:** [Wasm-Mutate][Wasm] builds equivalent rewrites for diversification. The criterion here is post-normalization retention of useful edit geometry, not diversity itself.
- **Cheapest first test:** Use sorted and constant-folded Boolean rules, with serialization round trips. Compare before/after decoded proposal distributions and give a serialized explicit mask the same bytes and normalization cost.
- **Old-task retention:** Score C/D interference with A and rare B after every checkpoint reload, with matching checks for arms that never reload.

### SM14 · Abstain when rare behavior falls outside the proof — IMPROVEMENT
- **Mechanism:** Restrict deployment to synonym rewrites proven on the entire supported finite interface; when only sampled equivalence is available, identify which contractual old behavior makes recoding unsafe and abstain.
- **Nearest prior / gap:** [GP Proof] proves semantics-preserving changes. This card tests the practical coverage cost of insisting on proof for *editability* changes, not the novelty of verification.
- **Cheapest first test:** On a tiny rule language plant rare A/B disagreements hidden from the compiler's sampled queries. Compare finite checking against sample-only and adversarial-probe compilation under the same checker budget.
- **Old-task retention:** Score the deliberately undersampled B cases immediately after recoding (before C), then again after C/D; report abstentions and new-task progress.

### SM15 · Persistent protection through independent editors — PRIMITIVE CANDIDATE
- **Mechanism:** Compile a *set* of equivalent representatives closed under the most common edits of each of two writers, instead of selecting a single locally robust center. Rare escape edges still permit correction.
- **Nearest prior / gap:** [Programmable Hardware][Hardware] already shows neutral networks with varying robustness. The candidate object is a low-leakage subgraph designed for *compositions* of fixed editors, rather than passive robustness under one kernel.
- **Cheapest first test:** Enumerate two edit graphs on the same codebook and minimize worst two-editor escape probability. Compare with the best single-editor center, replay-free scrubbing, and a combined mask.
- **Old-task retention:** Measure cumulative A and B first-exit risk under alternating and bursty C/D editors at equal useful edits, not just the launch hazard.

### SM16 · Let a clause keep one protected consequence — PRIMITIVE CANDIDATE
- **Mechanism:** Pick synonyms whose likely edits change the clause on an explicitly revisable portion of the input space while leaving a protected implication valid. Store the scope of safe revision in mutation geometry instead of in an edit guard.
- **Nearest prior / gap:** [Semantic GP] already considers semantics of mutations. The candidate is a clause-local compile operation specifying the *scope of future semantic change* at fixed launch semantics, not merely smaller average semantic steps.
- **Cheapest first test:** For three-input Boolean rules, enumerate equivalence classes and conditional edit distributions for two declared regions. Compare against constrained mutation with an equally sized scope guard.
- **Old-task retention:** In C and D, report errors on A's declared invariant and B's untouched region separately from legitimate changes in the revisable region.

## B · NNL07: Let inference traffic carry the write

### FA01 · Pulse destination is not local edge use — IMPROVEMENT
- **Mechanism:** Infer which of two equally used downstream edges should change by transporting an event pulse from its release location through live traffic. Conductance changes at crossings, not at release.
- **Nearest prior / gap:** [Hierarchy] already uses this transport mechanism. The gap is whether source/destination information beats a source-aware routing table for sequential task service, not whether advection works.
- **Cheapest first test:** Extend the equal-flux two-lane witness with a shared junction and release locations that swap after C. Give the table the release location and compare equal-work performance, including pulse-shuffled controls.
- **Old-task retention:** Measure rare B's route score on the branch sharing the junction with C, and A throughput on the other branch after C and D.

### FA02 · Carry delayed feedback on actual return flow — PRIMITIVE CANDIDATE
- **Mechanism:** Release a pulse at outcome arrival; allow updates only on edges traversed by the real return traffic. No path is retained for later replay. Measure where asymmetric returns cause miscredit rather than assuming they retrace the forward leg.
- **Nearest prior / gap:** [Eligibility Traces][Traces] credit recent forward events; [Q-routing][Q-routing] learns from downstream delay estimates. The candidate is an outcome-dependent write address defined by live return transport.
- **Cheapest first test:** Compare one symmetric and one asymmetric six-node graph, scoring both correct and spurious edge writes against matched traces, a stored path, and a source-aware table.
- **Old-task retention:** Force the most convenient C return path to overlap B's forward path; count B latency breaches and A delivery failures during adaptation.

### FA03 · Temporal routing at equal edge totals — PRIMITIVE CANDIDATE
- **Mechanism:** Use flow order across ticks to steer a finite pulse into one of two write regions. The two schedules use each edge equally often, but they offer different time-respecting paths from the release point.
- **Nearest prior / gap:** [Propagation] already explains a flow-borne traveling front; [Heat Kernel] diffuses mass through a graph. The candidate is an addressed write distinguished by path order under matched edge counts and fixed local read rules.
- **Cheapest first test:** Enumerate two three-tick schedules on parallel two-hop paths, keeping the release and on/off counts of each edge fixed. Compare to diffusion, a delay-aware table, and schedule shuffles that preserve those counts.
- **Old-task retention:** Hold B visits out during the write window; test B's delivery on the unselected branch while A and C compete at the junction.

### FA04 · Write strengthening or weakening from signed pulses — IMPROVEMENT
- **Mechanism:** Advect separate nonnegative good/bad outcome masses. Local conductance responds to their difference, with each sign independently conserved until sink or specified dissipation. Track both masses so zero net change does not conflate contradictory feedback with no feedback.
- **Nearest prior / gap:** [Ant Colony System][ACS] deposits tour-level reinforcement and evaporates pheromone; [Tero] uses flux alone. The test is whether local mixtures of transported signed feedback can outperform a matched per-route signed outcome table.
- **Cheapest first test:** Use a fork with equal traffic but an unreliable C branch and delayed outcomes. Match sign totals and test the mass-shuffled and last-path baselines.
- **Old-task retention:** Route rare B through the junction with a narrow service deadline; report whether negative C pulses wrongly weaken B and whether A loses headroom.

### FA05 · Locally budgeted conductance transfer — IMPROVEMENT
- **Mechanism:** On arrival, a pulse can enlarge an edge only by reallocating local conductance at the junction; no global renormalizer can invisibly subsidize a new route. Compare fixed share floors with no floors.
- **Nearest prior / gap:** [Hierarchy] already grows some tubes at others' expense; [Backpressure] allocates service from local queue state. The gap is a measured service/learning tradeoff under identical local budgets, not the existence of competition.
- **Cheapest first test:** Compete two old routes and a new shortcut at one four-way junction. Compare to backpressure plus the same minimum-service rule and to global normalization charged for its messages.
- **Old-task retention:** Include B with zero refresh during C/D and a bursty A. Count per-route deadline failures, including harm displaced to neighbors by the local budget.

### FA06 · Correct only where the pulse can reach before a deadline — IMPROVEMENT
- **Mechanism:** Sink a pulse after a fixed lifetime. This bounds the write region by the traffic's *time-respecting* reachable set, not by a fixed graph radius.
- **Nearest prior / gap:** [Directed Diffusion] uses local gradients and reinforcement for delivery; [Propagation] gives flow-dependent front speed. The candidate advantage is a cheap write-scope control that responds to actual live delays.
- **Cheapest first test:** Compare one fast distant branch and one slow near branch. Test against hop limits, time-limited diffusion, and a table with matched timestamps and latency observations.
- **Old-task retention:** Test A on the slow near branch and B off the fast branch at multiple pulse lifetimes; score both false containment and failure to adapt C in time.

### FA07 · Select a read-neutral but write-distinct flow decomposition — PRIMITIVE CANDIDATE
- **Mechanism:** Where routing has multiple feasible flows with the same output deliveries and matched service costs, choose among them to change where a future pulse will pass. This applies NNL01's synonymous write to NNL07's transport.
- **Nearest prior / gap:** [Neutrality] changes future exploration without altering present output; [Hierarchy] couples transport and memory. The candidate is a read-neutral control of *where a future update lands*, not flow balancing alone.
- **Cheapest first test:** Enumerate admissible flows on symmetric diamond routes and compile two decompositions with identical delivery and latency. Compare against an explicit pulse-routing table, both component baselines stacked, and random service-equivalent decompositions.
- **Old-task retention:** Verify A/B read equivalence at installation with no feedback; then test B's downstream recovery-free service after C and D pulses select the other path.

### FA08 · Learn a bounded write overlap from two sources — PRIMITIVE CANDIDATE
- **Mechanism:** Carry two separately conserved pulse masses; allow a conductance update proportional to the lesser of their coincident arrivals at an edge. Neither source alone has a write effect. The edge needs no global route list.
- **Nearest prior / gap:** [Propagation] studies a transported signal; [Traces] accumulate temporal evidence. The candidate write operator conditions on the intersection of two realized transport paths, not on a pooled sum or two source flags.
- **Cheapest first test:** Use equal per-source traffic and pulse totals on a shared corridor versus disjoint corridors with matched arrival times. Compare to additive updates, diffusion with the same coincidence rule, and an explicit per-edge two-source trace table.
- **Old-task retention:** Keep A and B serving on corridors reached by just one source; check for B damage when C/D pulses overlap near but not on its route.

### FA09 · Service failure from self-reinforcing write transport — IMPROVEMENT
- **Mechanism:** Cap the conversion of local pulse mass to conductance when successive releases concentrate on one route. Preserve pulse transport; limit write gain rather than adding a protected expert or a second router.
- **Nearest prior / gap:** [Propagation] already models positive feedback between signal and flow; [Braess] shows that a favorable local change can worsen network service. The proposed cap is useful only if it fixes a feedback-specific failure not handled by load control.
- **Cheapest first test:** Toggle a shortcut, freeze versus recompute flow between pulses, and compare capped and uncapped gains to backpressure and flux reinforcement at equal C delivery.
- **Old-task retention:** Measure A/B latency tails when C creates a dominant shortcut; kill the intervention if the failure occurs equally with frozen flow or the cap just slows all learning.

### FA10 · Write survives source position shifts without storing source IDs — PRIMITIVE CANDIDATE
- **Mechanism:** Train with release nodes that vary across events but are useful precisely when current traffic carries their mass into a shared useful corridor. Consolidation is overlap of actual delivery paths, not identity of release nodes.
- **Nearest prior / gap:** [Directed Diffusion] reinforces successful sensor-data paths; [Physical Coupled Learning][Coupled] uses local responses to free/clamped states. The gap is reuse of conductance across unseen release positions without storing per-source state or needing a clamped phase.
- **Cheapest first test:** Train with two release nodes, test a third that shares the corridor and a fourth equally close that does not. Compare to a topology-aware table, distance diffusion, and gradient routing under the same feedback graph.
- **Old-task retention:** Hold A's standard source nodes and B's unrelated rare corridor fixed through C/D source changes; report whether generalization was bought by narrowing either old route.

## Ranked deeper questions

1. **Is synonymous editing more than implementing an adaptive edit-rate table?** Start with SM02/SM03 on exact finite codebooks; match launch function and marginal hazard, then manipulate destination or co-edit odds only. Separate the existence proof from SM01's online stream. Compare an equally expressive explicit kernel and unequal-protection code with all representation and update costs; if they tie, call the compiler a representation choice, not a new learning primitive.
2. **Does causal transport order matter after matching the information available to the router?** Start with FA01/FA03. Match initial edge traffic, release schedule and total pulse mass; disturb only which time-respecting paths reach the destination. Then match the table/router's source, timing and query access and run the rare-B hiatus. Kill the advection advantage if traces or diffusion plus a table recover the same retention/adaptation frontier.
3. **Can past confirmation pay for coldness without locking in the wrong rule?** Combine SM04, SM08 and SM11. Sweep false confirmation and the duration of the B hiatus. Rank by worst-prefix A/B service at matched C/D adoption and count the cost of thawing. If a thawable explicit mask or scrubbing policy matches both, drop the more elaborate recoding.
4. **Can a serving network choose where it will learn next without changing what it serves now?** Start with FA07, then test the FA08 interaction. Require matching launch outputs and costs, then compare against the best synonym-only and advection-only controls *stacked*. If flow-equivalent twins need spare routing capacity that a small table can spend more effectively, do not claim a hybrid primitive.

[PR #6]: https://github.com/manojbajaj95/cl/pull/6
[PR #53]: https://github.com/manojbajaj95/cl/pull/53
[PR #338]: https://github.com/manojbajaj95/cl/pull/338
[ledger]: https://github.com/manojbajaj95/cl/blob/f340fc1877cdc2eb490aa747a6e510a9ea5e8c79/reviews/idea-ledger.md
[triage]: https://github.com/manojbajaj95/cl/blob/f340fc1877cdc2eb490aa747a6e510a9ea5e8c79/reviews/flood-triage.md#L459
[ACS]: https://faculty.washington.edu/paymana/swarm/dorigo97-itec.pdf
[Backpressure]: https://ieeexplore.ieee.org/document/182479
[Braess]: https://doi.org/10.1209/0295-5075/115/28004
[Coupled]: https://arxiv.org/abs/2011.03861
[Directed Diffusion]: https://www.isi.edu/websites/scadds/projects/diffusion.html
[egg]: https://arxiv.org/abs/2004.03082
[EWC]: https://arxiv.org/abs/1612.00796
[Exploration]: https://argmin.lis.tu-berlin.de/papers/03-toussaint-FOGA.pdf
[GP Proof]: https://pmc.ncbi.nlm.nih.gov/articles/PMC6044322/
[Hardware]: https://doi.org/10.1098/rsif.2010.0212
[Heat Kernel]: https://www.pnas.org/doi/10.1073/pnas.0708838104
[Hierarchy]: https://www.pnas.org/doi/10.1073/pnas.2007815118
[LULDC]: https://doi.org/10.1007/978-3-642-54242-8_21
[Lumpability]: https://people.nmsu.edu/jtian/publications/2006-3.pdf
[Neutrality]: https://doi.org/10.1023/A:1024906105255
[Propagation]: https://www.pnas.org/doi/10.1073/pnas.1618114114
[Q-routing]: https://publications.ri.cmu.edu/storage/publications/pub_files/pub1/littman_m_1993_1/littman_m_1993_1.pdf
[Redundancy]: https://doi.org/10.1162/106365603322519288
[Semantic GP]: https://doi.org/10.1007/s10710-013-9210-0
[Tero]: https://doi.org/10.1016/j.jtbi.2006.07.015
[Traces]: https://people.cs.umass.edu/~barto/courses/cs687/Chapter%207.pdf
[UEP]: https://doi.org/10.1109/TIT.1967.1054054
[Wasm]: https://doi.org/10.1016/j.cose.2024.103731
[WOM]: https://doi.org/10.1016/S0019-9958(82)90344-8
