# Non-neural learners: Same service, different next write

Child of [Synonymous mutability coding and flow-borne writes](non-neural-learners-2.md) ([PR #339]) · 26 idea cards · Ideas only; no experiments run

The [PR #6 reviewer][triage] kept two cards from #339 at score 3: **SM02**, choosing the destination of a blind edit at fixed escape probability, and **FA07**, choosing the site of a future flow-borne write at fixed current deliveries and service cost. This node asks which future writes can be independently addressed, how much that costs, and when an explicit controller wins. It does not revisit the majority-code protection schedule, make a claim about saving or restoring snapshots, or retest the coincident-pulse gate outside the comparison to CR20 suggested in the review. See the [idea ledger][ledger].

## Two exact witnesses and their limits

**Fixed escape, opposite destination.** On three bits, decode `001,010` to $V$, `101,110` to $W$, and all other states to $U$. Flip one uniformly sampled coordinate. At `000` and `111` the read is $U$ and the escape probability is $2/3$. Conditional on escape, the destination is $V$ from `000` and $W$ from `111`. The fixed editor does not read a mode; the decoder and edit kernel are unchanged. An explicit row over $U,V,W$ reproduces the effect exactly, and this fixture says nothing about acceptance, two-step behavior, or memory efficiency.

**Same edge loads, different writable edge.** A diamond has two equal-latency lanes, each capable of serving one unit per tick, with no spare lane. Two addressable streams $i,j$ share the same endpoints. Match each stream's deliveries, latency and service cost, and every edge's aggregate load by swapping which stream takes which lane. A unit pulse released into $i$ follows $i$'s actual forwarded packets; it then crosses a different downstream edge under the swap. Conservation requires delivering or sinking the unit, not copying it. This is read-neutral for the specified service interface, not for anyone who sees per-stream paths. A selector with the same stream key and path access can send the pulse to the same edge; charge those bits and operations symmetrically. A single unlabeled flow with a pulse splitter depending only on identical aggregate edge loads cannot give this effect.

## Shared CPU-first contract

- **Separate a proposal from a commit.** For an exact reference fixture let $f$ be the full finite read, $K$ the unchanged proposal kernel, $p_x(v)=\Pr_{x'\sim K(x,\cdot)}[f(x')=v]$, and $h_x=1-p_x(f(x))$. Match $f$ and $h_x$ across matched-hazard arms; compare the *conditional* destination row $p_x(v)/h_x$ for $v\ne f(x)$ when $h_x>0$. Separately count rejected/invalid proposals and report the analogous committed hazard and row. A tie under strong lumpability ([Lumpability]) means the bit-level difference has no one-step direction to use, not that a weak reader failed.
- **Keep the strong alternatives.** For directional edits, give a fully destination-aware explicit transition kernel the same confirmation evidence, candidate support, feedback and work; also compare a scalar edit-rate table, unequal protection, random synonyms at matched hazard, and a false-confirmation arm. If the desired transition is legally unreachable, don't count a shortcut that writes it directly. When an explicit controller can reproduce the full kernel, test cost and access, not exclusivity.
- **Show read neutrality before measuring a pulse.** For flow arms match demands, per-stream delivery and deadlines, service cost, and available capacity/slack. Where the card claims it, match aggregate edge loads at each tick too. Keep a pulse ledger (issued, in transit, sunk or specified loss). Include synonym-only and advection-only arms stacked, a source/timing/query-matched explicit table and message-passing router, and random service-equivalent twins at equal spare capacity. Any per-flow tag, path bookkeeping or reconfiguration transient counts; there is no hidden routing oracle. If a matching table beats the transport implementation, say so.
- **Keep serving old tasks.** Unless specified otherwise, train frequent A and rare B in a 95:5 mix, then learn C and D during a B training hiatus. Score held-out A and B immediately before and after a neutral write, through C/D, and on return, without offering test labels or routing traffic to the updater. Report per-task and worst-prefix service, adaptation cost at matched retention, and adoption after misleading early evidence. Charge persistent bytes, peak scratch, compiler/solver steps, queries and transmitted bits, not just stored clauses or edges.

## Literature check

Targeted web searches checked original papers and publisher abstracts on genotype–phenotype neighborhoods, mutational bias, probabilistic aggregation, and equivalent flows. [Ancel & Fontana][RNA] and [Toussaint & Igel][Neutrality] already connect neutrality to the distribution of accessible variation; [Schaper & Louis][Arrival] already show that which mutations arrive can steer adaptation. Fixed-hazard destination choice is a constrained use of existing neutral geometry, not a new discovery of directional mutation. [Ahuja et al.][Network Flows] give path and cycle formulations; [Räcke][Oblivious] already constructs path distributions to control aggregate congestion; [Reitblatt et al.][Consistent Updates] already address consistency during network changes. [Kramar & Alim][Hierarchy] already write a flow-borne memory. The gap under test is continual control of a *future write* across operationally indistinguishable current service states, with the strongest direction-aware and path-aware controls. The comparisons below are design hypotheses, not priority claims.

## A · SM02: Address a next destination, not a rate

### DS01 · Write a full destination row — PRIMITIVE CANDIDATE
- **Mechanism:** Specify a target probability vector over three or more next answers; choose a synonym from the fixed-hazard fiber that realizes the row. Width and the blind editor stay fixed.
- **Nearest prior / gap:** [Phenotypic Exploration][Exploration] describes general offspring distributions. Test compiled control over multiple odds, rather than selecting between two pre-existing modes.
- **Cheapest first test:** Enumerate attainable rows for a small Boolean decoder. Ask for three non-collinear rows and bound the error for both the best synonym and an equally compact explicit kernel.
- **Old-task retention:** A's protected outputs and the rare B row must continue working through C/D row changes, including when the requested row is infeasible and the compiler abstains.

### DS02 · Direction changes sign under a role exchange — PRIMITIVE CANDIDATE
- **Mechanism:** Use a labeled symmetry of a fixed decoder to remap an installed destination preference when two roles exchange, without re-estimating its magnitude or changing the incumbent.
- **Nearest prior / gap:** [Gray Codes] arrange states with prespecified small edits; [Neutrality] permits differing exploration. The candidate operation is predictable conjugation of an edit distribution under a role exchange at constant hazard.
- **Cheapest first test:** Exhaust a factored codebook with a swap of two output roles that fixes the incumbent. Compare reuse of the swap to an explicit kernel with the same column permutation; check exact equivariance on held-out roles.
- **Old-task retention:** Score unchanged A and rare B roles after a C swap and a D swap back; require that only the two intended future destination odds move.

### DS03 · Keep direction after ordinary acceptance — IMPROVEMENT
- **Mechanism:** Choose a synonym by its induced *accepted* destination distribution on a bounded set of ordinary feedback conditions, subject to fixed proposed and committed hazards where feasible.
- **Nearest prior / gap:** [Hastings] separates proposals from acceptance to shape realized transitions. Here the acceptor is fixed by the task; the question is whether recoding alone retains an intended direction across losses.
- **Cheapest first test:** On a finite bandit, vary which legal proposals pass a common acceptance threshold, with a strict equal-query comparison to an explicit proposal controller. Reject if the gain vanishes after matching accepted hazard.
- **Old-task retention:** Monitor A/B errors even when early C rewards point to the wrong destination and D reverses the reward ordering.

### DS04 · Transfer only directional evidence across tasks — IMPROVEMENT
- **Mechanism:** Infer which destination should become easy from a recurring pattern of prerequisites, then install a synonym in a different clause with the same destination schema. Transfer the preference, not the source clause's answer, confidence or write rate.
- **Nearest prior / gap:** [Successor Features] transfer predictions built from shared features. This asks whether encoding the transferred policy as a fixed-hazard destination bias has any advantage over storing that same policy explicitly.
- **Cheapest first test:** Train a tiny contextual bandit on two prerequisite sequences; hold the current answer fixed and transfer to a third sequence with the same next-target rule. Compare to a posterior-matched kernel and random matched-hazard synonyms.
- **Old-task retention:** Score A and B both when the prerequisite structure transfers correctly and when C spuriously resembles a B prefix but needs a different next target.

### DS05 · Buy a cheap escape back from a wrong direction — PRIMITIVE CANDIDATE
- **Mechanism:** Select which *microstate* an accepted edit reaches within the chosen destination. Prefer a landing state that makes a later ordinary correction back possible, at matched first-step output odds.
- **Nearest prior / gap:** [Testing Equivalence][Bisimulation] distinguishes states by future observations. The candidate write steers the recoverability of a particular accepted transition rather than caching and restoring the incumbent.
- **Cheapest first test:** Enumerate finite chains with matched first-step decoded rows but unequal conditional return probabilities; count further ordinary observations and attempts needed for a correction. Compare to an explicit two-step kernel and equal-byte snapshot restore as a control.
- **Old-task retention:** While recovering from wrong C evidence, keep unrelated A and rare B serving; a restored snapshot must also keep useful D progress to count as a tie.

### DS06 · Set direction at two levels of answer detail — PRIMITIVE CANDIDATE
- **Mechanism:** Match the next-edit odds for the coarse outcome class, but choose which fine-grained outcome is reachable within it. A separate coarse service view should not need more volatility to get fine control.
- **Nearest prior / gap:** [Lumpability] describes when aggregation preserves transition structure. The operation exploits a discrepancy between a coarse destination row and a finer inspected row, rather than proposing a new aggregation method.
- **Cheapest first test:** Find synonym pairs in a two-level rule table with equal hazards and equal coarse destination rows but distinct fine rows. Compare to an explicit hierarchical kernel with a shared coarse table.
- **Old-task retention:** Score the full A/B interface, not just the coarse metric used for matching next edits; count errors on rare B refinements during C/D.

### DS07 · Preserve the option after a neutral proposal — PRIMITIVE CANDIDATE
- **Mechanism:** Require not just a matched launch hazard but a high chance that the chosen *direction* survives one or more ordinary neutral proposals, without a maintenance rewrite.
- **Nearest prior / gap:** [RNA] studies neutral-network accessibility, and [Lumpability] gives the aggregate-chain null. Unlike a prefix-survival card, condition on continued service and measure whether the preferred destination, not the incumbent, persisted.
- **Cheapest first test:** Match launch rows for two carrier states; enumerate the destination row after a forced neutral step. Benchmark an explicit latched destination selector at the same total bytes.
- **Old-task retention:** Report A/B service and direction persistence separately through C/D; an arm that preserves service by silently losing its selected correction is not successful.

### DS08 · Measure the bits carried by a directional write — IMPROVEMENT
- **Mechanism:** Let an installer choose from a matched-hazard class given a desired next target. Estimate how much of that choice is communicated to the next decoded destination, conditional on an ordinary escape; charge failed proposals too.
- **Nearest prior / gap:** [Shannon] supplies the channel-capacity calculation. The benchmark restricts input symbols to service-equivalent carriers and charges the cost of using the actual edit channel, not just mutual information per success.
- **Cheapest first test:** Compute a capacity upper bound from enumerated rows, then price the best explicit quantized row selector at the same delivered information per attempt.
- **Old-task retention:** Hold the A/B read functions fixed while cycling desired C/D destinations; show any coding gain doesn't spend B's service margin.

### DS09 · Bound direction when edit flow must balance — IMPROVEMENT
- **Mechanism:** Compile several directional rows together subject to the edge symmetry of an undirected blind edit graph. For sets of microstates at stationarity under symmetric flips, count equal directed cross-class flux in both directions; don't infer a net cycle from one selected representative.
- **Nearest prior / gap:** [Reversible Chains] treats transition weights as electrical conductances. Apply that balance as a feasibility screen when a continual compiler claims directed changes in several read classes at once.
- **Cheapest first test:** Enumerate degree-constrained cubes for a requested three-class cycle, comparing stationary flux with flux from regularly reinstalled representatives. Charge reinstalls and compare to an explicit nonreversible editor.
- **Old-task retention:** Score A and B during the reinstallation budget sweep; reject gains that vanish when A/B receive equal service time.

### DS10 · Pack many independent next-write choices — PRIMITIVE CANDIDATE
- **Mechanism:** Encode different directional preferences at multiple service addresses under one decoder. An install at one address must preserve the other address's full destination row, not just its read or escape rate.
- **Nearest prior / gap:** [Exact Synthesis] handles complex synthesis constraints. The object here is a decoder with independently writable *future transition rows*; independence is a property to verify rather than a promise from the storage layout.
- **Cheapest first test:** For two ternary clauses, search for all four combinations of two target directions, then exhaust both orders of one-address replacement. Compare against storing two row indices and against permitting hidden coupling.
- **Old-task retention:** Use rare B as the unchanged address during C/D updates to A's revisable slice; score B's old answers and independently test its next write.

### DS11 · Compile under incomplete kernel knowledge — IMPROVEMENT
- **Mechanism:** Query the installed editor in scratch, estimate uncertainty in competing destination rows, and commit only a choice whose directional advantage is certified at matched hazard on fresh proposals.
- **Nearest prior / gap:** [Arrival] characterizes biases in accessible mutants when arrival probabilities differ. This asks how much black-box sampling is required to deploy a directional preference, rather than claiming a new sampling estimator.
- **Cheapest first test:** Hide a small editor's coordinate weights, then share proposal samples with a Bayesian explicit kernel selector. Compare correct destination choices, tie/abstain rate and consumed queries.
- **Old-task retention:** Score A/B while the writer abstains and when a falsely confirmed C direction is deployed with a low sample budget.

### DS12 · Control where an aborted edit would have gone — PRIMITIVE CANDIDATE
- **Mechanism:** Compile equal committed rows on A's normal feedback but different rejected-proposal destinations. After an independently induced D change to ordinary feedback, see whether the formerly rejected directions give earlier valid corrections.
- **Nearest prior / gap:** [Hastings] gives the proposal/acceptance decomposition; [Phenotypic Exploration][Exploration] biases proposals. The candidate carrier is the otherwise unserved part of the proposal row, with both actual service and committed directions matched at install.
- **Cheapest first test:** Enumerate a ternary editor and fixed A/D acceptors; hold launch proposal hazard and the A-committed row fixed. Compare to a stored explicit proposal row and a D controller with the same advance feedback.
- **Old-task retention:** Test A and rare B under A's feedback while installing the latent preference, then during D while the previously rejected destinations become available.

### DS13 · Compose synonym compilers without silent row erasure — PRIMITIVE CANDIDATE
- **Mechanism:** Give two independent writers different future-row constraints at one service address, such as controlling $V:W$ odds and odds of a third destination. Accept a composition only if both constraints survive in either order at matched hazard.
- **Nearest prior / gap:** [Exact Synthesis] can solve conjunctions of constraints and [Neutrality] provides variable search distributions. Test separately installed directional writes without a central compile from the original constraints each time.
- **Cheapest first test:** On a four-destination codebook, enumerate the intersection of two row constraints. Compare standalone composition to a full recompilation and a dense row controller with identical access to both requests.
- **Old-task retention:** Check A/B between the two installations and after C/D, not at the final feasible combination alone; record lost directional preferences separately.

## B · FA07: Address a future write without moving the service frontier

### FW01 · Enumerate reachable future write sites in a service fiber — PRIMITIVE CANDIDATE
- **Mechanism:** Map each service-equivalent flow decomposition to its pulse-crossing vector; use the resulting feasible set as the writable address space. Exclude any site reachable only by increasing current service cost.
- **Nearest prior / gap:** [Network Flows] constructs feasible path/cycle decompositions. The candidate object is the image of that constrained set under the *future local write operator*, not the flow set itself.
- **Cheapest first test:** Enumerate integral flow decompositions on two connected diamonds and compute the exact set of pulse sinks and edge crossings. Compare its rank and installation cost to an explicit edge-addressed selector.
- **Old-task retention:** Require both A and B deliveries and path latency to hold on each selected decomposition; then test retention after learning C/D at each reachable write site.

### FW02 · Route labeled credit at fixed aggregate load — PRIMITIVE CANDIDATE
- **Mechanism:** Reassign commodity labels to saturated paths while keeping the multiset of used paths fixed. Test whether local forwarding can carry a later pulse associated with an outcome on one commodity without storing its path centrally.
- **Nearest prior / gap:** [Oblivious] chooses source-destination path distributions to manage congestion; [Hierarchy] carries signal with flow. This tests whether equal load is compatible with cheaper commodity-specific write addresses in a shared service.
- **Cheapest first test:** Extend the diamond to three commodities and exhaust assignments at capacity. Compare exact per-tick edge loads and charge tags against a selector that can store a path index.
- **Old-task retention:** Withhold rare B updates after C starts on the shared service; measure B's per-stream latency rather than declaring retention from equal aggregate throughput.

### FW03 · Set a probabilistic write address with service-optimal mixtures — IMPROVEMENT
- **Mechanism:** Time-share among decompositions that each meet current service constraints, with mixtures chosen for future pulse-destination odds. Do not use a mixed marginal to excuse a service violation in one component.
- **Nearest prior / gap:** [Optimal Transport] defines feasible plans and cost/regularization objectives. The extra objective is the induced distribution of future writes, at exact primary service cost and with service constraints on each component.
- **Cheapest first test:** Solve a tiny linear mixture over feasible schedules with fixed pulse release times sampled independently of the mixture. Compare to an explicit randomized address table and to entropy tie-breaking.
- **Old-task retention:** Report A/B worst-tick service during mixed routing and through C/D writes; a mean-only gain does not pass.

### FW04 · Keep a write choice valid for burst tails — IMPROVEMENT
- **Mechanism:** Select a flow synonym only if it agrees with the incumbent on latency tails under a fixed library of admissible burst traces, not just on nominal load. Evaluate whether any directional work remains after this stricter equivalence.
- **Nearest prior / gap:** [Oblivious] already targets worst-case congestion across demands. The test is how much pulse-direction control survives a service-equivalence constraint stronger than equal mean throughput.
- **Cheapest first test:** Enumerate small queues and burst schedules; match the full per-stream deadline outcomes for each trace and compare to an explicit selector plus ordinary robust routing.
- **Old-task retention:** Score A and rare B deadlines on held-out correlated bursts before and after C/D; count twins that were rejected for mistreating B.

### FW05 · Reserve the same slack, choose distinct write sites — PRIMITIVE CANDIDATE
- **Mechanism:** Constrain two decompositions to identical per-edge slack under normal and predeclared failure scenarios. Use only the remaining label or path choices to steer where a future write lands.
- **Nearest prior / gap:** [Oblivious] controls congestion through path choices; [Network Flows] formulates residual capacity. The candidate uses feasible degrees of freedom *after* capacity insurance is fixed, not spare capacity as a hidden write channel.
- **Cheapest first test:** Enumerate a six-node network with one disabled edge scenario and two feasible failover paths. Give the table all failover information and compare attainable targets at equal reserved capacity.
- **Old-task retention:** In C/D, fail one edge and verify A and rare B deadlines through failover with no B rehearsal visits; charge the recovery interval.

### FW06 · Write mode persists under consumer-independent traffic — PRIMITIVE CANDIDATE
- **Mechanism:** Pick a decomposition by the path pattern shared across a library of demand changes. The chosen future address must survive ordinary unrelated traffic without reselecting a decomposition on every query.
- **Nearest prior / gap:** [Oblivious] routes with bounded congestion across demands. The property here is stable *writing address* despite variable demands, at matched service trace, not a route's predictable congestion.
- **Cheapest first test:** On a small capacitated network, release the same probe pulse before and after adding an unrelated stream. Match both arms' current service and compare to a table keyed on the same observable demand.
- **Old-task retention:** Include a rare B arrival coinciding with a burst of unrelated C traffic, then a D demand shift; require neither pulse steering nor traffic matching to sacrifice B.

### FW07 · Service-equivalent transition, not just endpoints — IMPROVEMENT
- **Mechanism:** Change decompositions while packets are in flight. Require the intermediate execution to maintain old-service deadlines and the intended pulse address, or account for a bounded quiescence interval.
- **Nearest prior / gap:** [Consistent Updates] supplies per-packet consistency for reconfiguration. This test asks whether enforcing consistency for both service packets and incoming write pulses consumes the apparent transport advantage.
- **Cheapest first test:** Switch lanes on a two-tick diamond mid-flight; enumerate switch orders and pulse arrival times. Compare version tagging or draining against a fixed forwarder with explicit write routing.
- **Old-task retention:** Count A/B deadline misses and wrong C/D writes during the transition; no credit for correct endpoints with unserved in-flight B jobs.

### FW08 · Preserve flow timing as well as totals — PRIMITIVE CANDIDATE
- **Mechanism:** Choose a commodity assignment on a time-expanded network where every physical edge has the same load each tick and every commodity has the same delivery times, but a tagged pulse follows different edge-time cells.
- **Nearest prior / gap:** [Dynamic Flows] constructs flows with transit times. The proposed degree of freedom is the identity of a writable edge-time cell *after* observed service timings and congestion have been fixed, not faster signal propagation.
- **Cheapest first test:** Exhaust a two-lane, three-tick flow with same-tick demands and unequal path transit times internally paired to equal end-to-end time. Compare to a time-indexed explicit kernel and non-advected broadcast.
- **Old-task retention:** Test rare B's scheduled delivery at every prefix during C/D, including when two pulse arrivals contend for one write opportunity.

### FW09 · Use a neutral circulation only if its cost is real — IMPROVEMENT
- **Mechanism:** Allow a circulation to carry a pulse without source-to-sink delivery, but require an equal-cost circulation in the control and charge all reserved bandwidth and solver work. Reject it if operational traffic does not already support the loop.
- **Nearest prior / gap:** [Network Flows] explicitly decomposes circulations. The question is whether a real cost-matched service circulation offers a write route cheaper than directly allocating a message path.
- **Cheapest first test:** Compare alternate equal-length cycles on a graph with mandatory circulating traffic and on the same graph without it. Count the loop budget and give an explicit transport table equal message allowances.
- **Old-task retention:** Check A/B delivery under both traffic regimes and during D, so a stealth draw on B's bandwidth cannot appear as memory.

### FW10 · Jointly steer a write and its conservation debit — PRIMITIVE CANDIDATE
- **Mechanism:** With fixed total conductance, use a local rule that pairs each pulse ingress at a junction with a particular debit edge. Choose a read-neutral decomposition whose pulse reaches the same target edge through a different ingress, paying from a different edge without reading task identity.
- **Nearest prior / gap:** [Hierarchy] reallocates diameter among tubes. The candidate is independent control of benefit and collateral debit using decompositions at fixed service, not simply a capped update.
- **Cheapest first test:** Use an equal-cost diamond with both lanes feeding the target junction. Match positive pulse arrivals at the target and vary which ingress pays. Compare against a signed explicit table under the same cap and balance.
- **Old-task retention:** Measure A/B headroom and B's deadline under a fixed short burst after C/D; report the total debit and where it landed.

### FW11 · Test whether compact forwarding beats explicit addresses as the graph grows — IMPROVEMENT
- **Mechanism:** Generate a family of service-equivalent route permutations from shared local forwarding rules instead of a separate stored write path per shift. Charge the codebook and each local message, not only final bytes.
- **Nearest prior / gap:** [Oblivious] compresses routing structure through hierarchical decompositions. The proposed benefit is amortized representation of *future write addresses* in existing service state; the table may use the same hierarchy.
- **Cheapest first test:** Enumerate chains of two, four and eight diamonds; compare best shared forwarding rule, hierarchical message-passing router, and compressed address table over an identical target sequence.
- **Old-task retention:** Put one old B service at a distant diamond and one A at a shared junction; measure locality of collateral failure as the graph grows through C/D.

### FW12 · Quantization as a limit on write addressing — IMPROVEMENT
- **Mechanism:** Select a flow synonym by its realizable pulse-crossing counts under integer packets. Reject fractional plans whose apparent directional control disappears after rounding under equal service and conservation.
- **Nearest prior / gap:** [Oblivious] allows randomized path selections for congestion; [Dynamic Flows] represents time-constrained flows. This is a feasibility screen for packet-limited directional writes, not a new rounding method.
- **Cheapest first test:** Compare exact integer solutions to relaxed ones on a three-way junction at one, two and four available pulse units. Compare residual-address error with an explicit packet dispatcher and charge any additional packets.
- **Old-task retention:** Prioritize B deadline and A throughput in the integer constraints. Score C/D adaptation at matched old-task retention and packet budgets, not just fractional cost optimality.

### FW13 · Cross fixed-hazard direction with read-neutral transport — PRIMITIVE CANDIDATE
- **Mechanism:** Use an ordinary accepted edit's *destination*, not its occurrence, to supply the feedback label carried by a pulse. A flow synonym controls which downstream cell sees that label. Hold launch service, committed hazard and issued pulse mass fixed so direction and write site are independently manipulable.
- **Nearest prior / gap:** [Exploration] changes destination odds and [Hierarchy] transports a write signal. The proposed interaction is learning a label-by-site mapping that remains selectively writable in a joint carrier, not an improvement merely from applying both methods in succession.
- **Cheapest first test:** Cross two fixed-hazard directional synonyms with two saturated flow twins. Compare to synonym-only plus advection-only stacked with the same full label/site inputs, a joint explicit kernel and a message-passing router. Discard the hybrid if the stacked system reproduces both target writes and interference at equal cost.
- **Old-task retention:** Put rare B on overlapping service but on neither intended write cell. Score A/B after each of the four interventions and after D while matching C adoption.

## Ranked deeper questions

1. **How many independent next destinations can be set at fixed hazard before an explicit kernel is cheaper?** Start with DS01 and DS10. Enumerate attainable rows and one-address rewrites, include the DS09 balance check, and measure actual accepted rows under DS03. Match legal support and all costs. If the dense or compressed kernel ties, keep the feasibility result and drop the proposed representation advantage.
2. **Can the learner move a future write under exact current service without relying on hidden addressing or spare capacity?** Start with FW01, FW02 and FW08. Match per-stream outcomes, timing and slack before every pulse, intervene on the decomposition, then cross-check the trace using the source-aware table and message-passing router. If no twins survive the matched-service test or the router ties, stop at the separation fixture.
3. **Can either choice survive an ordinary but misleading stream?** Cross DS05/DS07 and FW06/FW07 with false confirmation, bursty C/D updates and the rare-B hiatus. Plot worst-prefix A/B service against successful redirection and total installation work. Do not accept gains that require pausing service or restoring it in hindsight.
4. **Does joint compilation buy an interaction, or just encode an explicit label-by-site table?** Test FW13's four-way crossing only after each constituent passes its own strong control. Match the stacked baselines' bytes, tags and information and keep the B hiatus. A clean interaction in a fixture is insufficient if the joint table or stacked baselines match the end-to-end frontier.

[PR #339]: https://github.com/manojbajaj95/cl/pull/339
[ledger]: https://github.com/manojbajaj95/cl/blob/3b5cd7ffac6cf9134fa896f3b6a1103bb3850fa1/reviews/idea-ledger.md
[triage]: https://github.com/manojbajaj95/cl/blob/3b5cd7ffac6cf9134fa896f3b6a1103bb3850fa1/reviews/flood-triage.md#L461
[Arrival]: https://doi.org/10.1371/journal.pone.0086635
[Bisimulation]: https://www.sciencedirect.com/science/article/pii/S0890540117301864
[Consistent Updates]: https://doi.org/10.1145/2342356.2342427
[Dynamic Flows]: https://doi.org/10.1287/opre.6.3.419
[Exact Synthesis]: https://si2.epfl.ch/demichel/publications/archive/2017/IWLS2017_Paper23_eTesta.pdf
[Exploration]: https://argmin.lis.tu-berlin.de/papers/03-toussaint-FOGA.pdf
[Gray Codes]: https://doi.org/10.1137/s0036144595295272
[Hastings]: https://academic.oup.com/biomet/article-abstract/57/1/97/284580
[Hierarchy]: https://www.pnas.org/doi/10.1073/pnas.2007815118
[Lumpability]: https://people.nmsu.edu/jtian/publications/2006-3.pdf
[Network Flows]: https://hdl.handle.net/1721.1/49424
[Neutrality]: https://doi.org/10.1023/A:1024906105255
[Oblivious]: https://doi.org/10.1145/1374376.1374415
[Optimal Transport]: https://optimaltransport.github.io/pdf/ComputationalOT.pdf
[Reversible Chains]: https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch3.S6.html
[RNA]: https://doi.org/10.1002/1097-010X(20001015)288:3%3C242::AID-JEZ5%3E3.0.CO;2-O
[Shannon]: https://doi.org/10.1002/j.1538-7305.1948.tb01338.x
[Successor Features]: https://arxiv.org/abs/2110.09196
