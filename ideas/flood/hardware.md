# Hardware idea flood: 65 continual-learning cards

Hardware, analog, and neuromorphic computing as sources of *learning operations*, not just ways to run the same training faster. I checked [PR #6's idea ledger](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md) and [flood triage](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md) and skimmed sibling floods. The current leaders (prompt-addressable checkpoints, round-trip consolidation, self-readable seed log) are separate targets. These are novelty hypotheses, not priority claims or pilot results.

**Test convention:** Use a cheap simulator first, not custom silicon. A/B are sequential training regimes with disjoint held-out evaluation sets; unless noted, score B acquisition and held-out A before B, after B, and after any proposed recovery. Separate unchanged A skills from intentionally superseded rules on migration tests. Report old-task retention at comparable B performance, plus absolute old/new scores and any extra read or recovery work; old data used for training or calibration is counted, not taken from the evaluation set. Controls share stream, storage (including metadata), and relevant write/read or compute budgets as specified.

## Analog state is part of the learner

### H01. Conductance push-pull with a movable fulcrum
- **Mechanism:** Encode each adapter scalar as the difference of two conductances. Recenter both equally when one rail nears saturation; spend the recovered pulse headroom in the direction the incoming update needs, without changing the pre-write readout.
- **Novelty / tag:** **Primitive** — a zero-output physical operation changes the *reachable next writes*. Differential crossbars and SM7's neutral drift are neighbors; here the target is measured directional pulse feasibility at fixed readout.
- **First test / tie:** Simulate bounded conductance cells on alternating signed regression shifts; check held-out A after B. Compare to a balanced differential pair that spends the same recalibration pulses on symmetric resets.

### H02. Drift as an address
- **Mechanism:** Program two resistive copies with different drift exponents. Sample their difference at two times after the same reference pulse to recover a sum and an age-channel residual; use the residual as a distinct input to a frozen LM's adapter.
- **Novelty / tag:** **Primitive** — the time derivative is a readable channel, not a half-life policy. Near PCM drift compensation and temporal multiplexing.
- **First test / tie:** Fit two toy token maps in the temporal basis and retrieve held-out A under jitter after learning B. Compare with two quantized banks using the same cells and reads, with explicit time metadata counted.

### H03. Read-voltage-selective updates
- **Mechanism:** Fit task residuals in different response coefficients of a nonlinear crossbar; a low-amplitude drive reads the base map, while a higher drive and reference subtraction expose the additional coefficient. Program B by changing only the measured high-drive response.
- **Novelty / tag:** **Primitive** — one programmed substrate implements different forward operators by read waveform, not by a prompt or a software route. Near nonlinear selector devices and bit-slice reads.
- **First test / tie:** Simulate mildly coupled nonlinear cells for two character transductions; measure A under the low-drive mode after B. Compare to two bit-sliced linear banks at matched cells and conversions.

### H04. Plasticity only where write noise cancels
- **Mechanism:** Map a rank-one update into complementary crossbar tiles sharing a noisy supply; use measured common-mode pulse correlations to choose signs and pairing so bad pulses cancel in the old readout but new residuals add.
- **Novelty / tag:** **Improvement** — physical noise covariance becomes placement information; near common-mode rejection and robust weight mapping, rather than a new loss.
- **First test / tie:** Fit A then B with simulated correlated write noise on a linear adapter; evaluate held-out A on unseen noise draws. Compare to equally redundant random pairings with the same calibration reads.

### H05. Pulse-spectroscopy write masks
- **Mechanism:** Before writing, tap each tile with small bipolar pulses and measure its local programming derivative. Build the next adapter update in tiles whose derivative is large in the required direction and small on old readout-sensitive cells.
- **Novelty / tag:** **Improvement** — allocation uses an online measurement of the actual write operator, not an estimated Fisher or free-weight count. Near write-verify and gradient projection.
- **First test / tie:** Introduce asymmetric cell aging into a tiny digit head, learn a new rotation, and retest the old digits. Compare to magnitude-based masking given the same number of taps, pulse writes, and protected cells.

### H06. Program by quench, read by minor loop
- **Mechanism:** On a phase-change-inspired cell model, store a durable conductance and a metastable response to a small read sequence. Train the latter on a transient context; a quench either turns it into durable conductance or clears it, with acceptance decided on calibration examples.
- **Novelty / tag:** **Primitive** — a reversible local trial and an irreversible commit are different material transitions, not checkpoint loading. Near volatile/nonvolatile hybrid synapses.
- **First test / tie:** Emulate a bank on stable A plus recurring and one-off B facts; check A and previously committed facts after several rejected trials. Compare to a same-bit fast/slow digital weight pair with the same commit tests.

### H07. Read-disturb writes a usage map
- **Mechanism:** Intentionally use a tiny read perturbation in each selected coefficient. A second, low-disturbance scan estimates the per-row conductance displacement and feeds it to an adapter allocator, without logging per-query accesses.
- **Novelty / tag:** **Improvement** — read wear doubles as a local footprint of use. Near read-disturb mitigation and hardware access counters.
- **First test / tie:** Simulate skewed lookup traffic, then add new mappings; compare rare and common held-out A recall with equal bytes and scan work against saturating software counters.

### H08. Reference rows that learn the inverse read channel
- **Mechanism:** Reserve pilot-tone rows in every analog tile; fit their inversion jointly with the adapter using separate read and supervised-write errors. If hardware drifts between tasks, change the inverse readout while leaving stored conductances untouched.
- **Novelty / tag:** **Improvement** — learned per-array calibration separates hardware loss from learning loss. Near pilot-tone channel estimation and analog drift compensation.
- **First test / tie:** Apply piecewise ADC drift while fitting B in a random-feature head; test A under both old and new ADC settings. Compare with equal-read gain/offset calibration and the same B writes.

### H09. Dead cells as a frozen compute fabric
- **Mechanism:** Measure stuck-cell patterns and use their fixed random projections as features. Add new skills by programming the surrounding live columns to read or cancel those features; never require a stuck cell to store a requested value.
- **Novelty / tag:** **Primitive** — an accumulating physical defect map becomes an expanding fixed feature basis rather than an erasure index. Near defect-aware remapping and extreme learning machines.
- **First test / tie:** Kill cells between two synthetic token-mapping tasks; fit a readout and retest held-out A. Compare to masking those cells and spending equal live cells and operations on synthetic random features.

### H10. Elastic row voltage
- **Mechanism:** Keep shared analog weights fixed, but issue a learned input-voltage envelope per channel from a small adapter. State-dependent voltage changes select where nonlinear devices saturate, giving the learner a write over the operator's response surface.
- **Novelty / tag:** **Primitive** — plasticity acts on a control voltage and therefore on which nonlinearities are exposed, not a stored weight. Near IA³, gain modulation, and programmable analog computing.
- **First test / tie:** Fit B through voltage envelopes on a saturating random-feature block and retest A at the original and inferred envelopes. Compare to equal-parameter IA³ over the same fixed features and task cues.

### H11. Interference-routing through ballast
- **Mechanism:** Fit low-rank adapter updates in crossbar tiles with measured, location-dependent row voltage drops. Put B's coefficients in precise tiles; send a simultaneous balancing current through otherwise idle columns to suppress predicted distortion on A directions.
- **Novelty / tag:** **Improvement** — parasitic coupling becomes an active compensator shared between writes, rather than an error ignored by the CL rule. Near IR-drop compensation.
- **First test / tie:** Emulate a resistive grid for two overlapping regression tasks; retest A under simultaneous A/B loads. Compare to remapping-only placement with the same extra columns and calibration.

### H12. Learn to read the residue of resets
- **Mechanism:** A reset returns PCM-like cells to a narrow baseline but leaves a weak history-dependent signature. Fit a read-only projection to extract a context flag from that footprint, then use fresh cells to store B normally.
- **Novelty / tag:** **Primitive** — a soft-erased substrate becomes a state sensor, not a version archive; near analog remanence and reservoir readouts. The flag is deliberately constructed state, not arbitrary recovered private data.
- **First test / tie:** Simulate synthetic pulse-history residues on recurring benign tool configurations; track held-out A success after B and repeated resets. Compare to a digital context bit per bank using equal bits and reads.

### H13. Conductance gradient as a teaching bus
- **Mechanism:** After a forward read, inject a local error current in the opposite direction across the same array. Use the return current only to choose candidate write locations; a low-rank digital sidecar determines their magnitudes.
- **Novelty / tag:** **Improvement** — reverse electrical transport selects writable sites without forming an explicit full gradient. Near analog backpropagation and feedback alignment; spatial coupling may be beneficial only under a write budget.
- **First test / tie:** Compare reverse-current selection to matched random and gradient-magnitude selection on a two-task MLP with nonlinear tile noise; retest held-out A after B at equal pulse count.

## Neuromorphic substrate and online credit

### H14. Spike collisions open write apertures
- **Mechanism:** Encode feature events and delayed tool feedback on separate timestamp buses; coincident bursts briefly unmask a low-rank adapter block, but event magnitude has no effect outside the aperture.
- **Novelty / tag:** **Primitive** — a write aperture is an independently routed control event, not a scalar global learning rate; near STDP and three-factor learning.
- **First test / tie:** Train a tiny policy on two interleaved delayed-reward toy tools; retest A after B with changed feedback latency. Compare to matched eligibility magnitude gating with equal traces and writes.

### H15. Acknowledge-before-forgetting synapses
- **Mechanism:** Each in-flight agent episode acquires a short lease on the sparse adapter indices represented in its eligibility trace. A later episode can learn elsewhere immediately, but those indices cannot be recycled until the first outcome acknowledges or expires.
- **Novelty / tag:** **Primitive** — delayed credit creates temporary write ownership with explicit release; near event acknowledgments, e-prop, hazard pointers, and neuro-bio NB01's write escrow. The trace protects its location from recycling, rather than just marking where to write later.
- **First test / tie:** Simulate asynchronous bandit tools with long-tail feedback; learn B under outstanding A episodes, then rerun held-out A. Compare to fixed-window locking with equal trace memory, queued work, and mean residence time.

### H16. Negative eligibility paid by later abstention
- **Mechanism:** Keep signed local tags for an agent's skipped feasible tool branches as well as the executed choice. When a matched state later selects and validates a formerly skipped branch, route the reward difference into those tags, not into every feature from the old episode.
- **Novelty / tag:** **Primitive** — unexecuted choices leave redeemable traces rather than replay examples. Near counterfactual policy gradients, gradient IOUs, and eligibility traces; no payoff is assigned until matched outcomes arrive.
- **First test / tie:** Use a paired-context bandit whose rewards are only observed for tried arms; after new contexts, check held-out success on A. Compare to a same-size replay cache of executed outcomes with the same exploration draws.

### H17. Dendritic write veto without forward suppression
- **Mechanism:** Let branch outputs keep contributing to a frozen LM residual stream, but attach a separate nonlinear modulator to each branch's write path. Persistent predictable activations raise a local veto unless the verified error exceeds that branch's threshold.
- **Novelty / tag:** **Improvement** — separates learned write veto from inference routing; near apical dendritic gating and neuro-bio NB03's compartment veto, but uses accumulated local predictability instead of a counterfactual branch substitution.
- **First test / tie:** Teach two overlapping syntax maps to a tiny transformer; retest A while all branches remain readable. Compare to fixed activity-based freezing at the same write and parameter budgets.

### H18. Conditional dendritic carry
- **Mechanism:** Store a correction on an adapter branch that cannot affect the residual alone; it fires only when two separate local feature events arrive in a short window. Update the conjunction thresholds instead of rewriting either single-feature response.
- **Novelty / tag:** **Primitive** — a temporal AND carries the learned interaction separately from its constituent skills. Near multiplicative adapters and nonlinear dendrites.
- **First test / tie:** Train primitive A rules then B exceptions requiring feature pairs; retest A on isolated cues and near-miss pairs. Compare to a matched gated adapter using concatenated features with the same operations.

### H19. Refractory write barriers
- **Mechanism:** After writing an adapter row, mark it temporarily refractory to writes but not reads. If two corrections keep colliding, they must find other rows; the barrier depends on recent pulses, not age since task start.
- **Novelty / tag:** **Improvement** — a hard local inter-write interval may prevent cohorts from repeatedly erasing each other. Near refractory dynamics, gradient throttling, and per-parameter schedules.
- **First test / tie:** Alternate conflicting and independent minibatches in a sparse linear head; test A after B. Compare to random write drops with the same per-row expected pulse count.

### H20. Route error by spike latency, not by identity
- **Mechanism:** Give the correction signal several latency bins; adapters with traces nearest the arriving error update first, and the residual error moves to another bin only if a verifier says it remains.
- **Novelty / tag:** **Primitive** — bus latency encodes a mutable credit-ordering program across shared modules, not a context or task ID. Near rank-order coding and neuro-bio NB10's phase-locked credit packets; this sweeps a verified residual across ordered recipients rather than using phase as an address.
- **First test / tie:** Simulate an agent with syntactic and semantic tool failure classes, then add a third. After B, retest A including delayed responses. Compare to fixed stage order given the same verifier calls and traces.

### H21. Inhibitory shadow of a weight write
- **Mechanism:** Pair each plastic low-rank excitatory branch with a cheaper inhibitory branch trained on its unintended activation outside the intended event ensemble. Publish both together; inhibit the branch, not the base logits.
- **Novelty / tag:** **Improvement** — near lateral inhibition and functional antidotes; the shadow is specifically a jointly trained branch-local counter-current measured before publication.
- **First test / tie:** Insert B fact associations with false-cue overlap; retest old A and unrelated token predictions. Compare to a standard gated adapter of equal rank using the same unlabeled negative inputs.

### H22. Eligibility trace transplantation across calls
- **Mechanism:** At an agent's tool boundary, serialize a compressed trace of eligible local adapter features in the pending call. A later verifier returns a scalar reward plus the trace; a compatible worker can apply it without saving the originating activations or full transcript.
- **Novelty / tag:** **Primitive** — the transferable object is a bounded credit envelope, not a weight delta or a seed log. Near e-prop, actor-learner queues, neuro-bio NB01's write escrow, and forward-only credit-address books; the experiment tests if credit can cross the worker boundary without its originating forward pass.
- **First test / tie:** Train a two-worker toy planner through an added tool with delayed results; retest held-out A on both workers. Compare to equal-byte compressed trajectory replay with the same learner updates.

### H23. Microglue buses for incompatible features
- **Mechanism:** Give each adapter a few learned spike channels whose local receivers can change independently. When two tasks need the same observable cue in incompatible hidden coordinates, teach a bridge on coincident calibration events instead of changing either adapter.
- **Novelty / tag:** **Primitive** — communication learns without merging endpoints. Near event buses and the weight-space linker; the bus is an online temporal translator, not relocatable residual directions.
- **First test / tie:** Freeze A and B modules with permuted features; teach a short mixed-tool routine and retest A standalone. Compare to matched dense feature alignment with the same bridge size and calibration calls.

### H24. Associative recall only after spike silence
- **Mechanism:** Let the frozen model handle the early token stream. If no learned correction emits before a deadline, send one event to an expensive memory bank whose response can still replace the tentative action.
- **Novelty / tag:** **Improvement** — uses *absence of an adapter event* as the retrieval trigger; near early exits, ask-when-stuck, and event-driven sparse computation.
- **First test / tie:** Stream easy and exceptional toy tool calls through A/B; measure A answers and tail latency after B additions. Compare to confidence-threshold retrieval with equal memory lookups and total runtime budget.

### H25. Counterpropagating replay waves
- **Mechanism:** A live example sends forward local feature events, while short stored snapshots of old residual activity move backward through the module graph. Permit a new local write only in the timing window where the old wave has cleared that module.
- **Novelty / tag:** **Primitive** — a live/replay handshake protects mutually inconsistent local state without pausing the whole learner. Near activation replay and pipelined backpropagation.
- **First test / tie:** Run a four-block tiny transformer simulator on alternating token forms; retest A after B and count stalls. Compare to barrier-synchronized replay with identical old events, updates, and measured throughput budget.

### H26. Neuromodulator exchange between clocks
- **Mechanism:** Have a fast token learner emit low-bit error histograms and a slow episode verifier emit signed credit pulses. Cross them through an accumulator that only releases writes when the two sources agree in sign within a configurable timing window.
- **Novelty / tag:** **Primitive** — credit confirmation across time bases is an explicit write operation, not just averaging two losses. Near dual-timescale three-factor rules.
- **First test / tie:** Use a toy policy where early reward and final success disagree on B; retest A with delayed rewards. Compare to equal-buffer weighted error summation given the same pulse arrivals.

## Storage controllers that learn

### H27. Refresh by reference charge, not by replay
- **Mechanism:** Pair volatile adapter weights with local guard cells. Charge decay of the guard tells the controller how far to amplify a block before a DRAM-like read/restore; retain only calibration constants, not old examples or target outputs.
- **Novelty / tag:** **Improvement** — hardware-state refresh performs a data-free maintenance write, near variable-retention DRAM and hardware drift compensation, not scheduled training on old data.
- **First test / tie:** Fit successive linear residuals with simulated heterogeneous leak. Measure A after B and long idle periods against matched periodic refresh with the same reads and writes.

### H28. Uncorrectable-write exceptions
- **Mechanism:** Put ordinary ECC over quantized adapter words. New writes may update data bits but must submit the intended parity changes separately. A tile that instead produces a persistent unexpected syndrome raises a fault and routes execution temporarily through a small fallback head until the tile is scrubbed.
- **Novelty / tag:** **Primitive** — a learning write can trigger a machine-level exception separating interrupted programming from task interference. This uses exact word integrity, not the ledger's falsified behavioral sparse-recovery syndrome.
- **First test / tie:** Inject correlated torn B writes into a quantized toy LM head; measure new assimilation and old A held-out accuracy during and after the fault. Compare to matched checksums and reload retries with equal redundant bits and recovery time.

### H29. Retention leases under wear leveling
- **Mechanism:** Give an adapter placement a lease on the future pulse life of its current cells. As observed error rates approach the lease limit, migrate *currently stable weights* into less-worn cells and let new short-lived updates consume the old site.
- **Novelty / tag:** **Improvement** — near flash wear leveling and memory relocation. It schedules by physical write life plus old-read tolerance, not by chronological task importance.
- **First test / tie:** Simulate heterogeneous cell fatigue across a 10-regime token stream and retest A after B and late waves. Compare to uniform wear leveling given identical migration bandwidth, endurance, and spare cells.

### H30. Deallocate learning authority, not data
- **Mechanism:** On an obsolete dependency, issue a TRIM-like command to the agent's memory controller: future learning may no longer use that lesson as a teacher, but existing consumers may still read it until they receive fresh evidence. Later compact the now-undepended teacher entries.
- **Novelty / tag:** **Primitive** — independently revoke a lesson's permission to reproduce and its permission to be read. Near reachability GC and the ledger's self-contamination law; no need to delete immediately.
- **First test / tie:** Simulate a tool schema migration with a reused subrule and a changed teacher; measure A's unaffected held-out cases while learning B. Compare to equal-space immediate deletion or version marking with the same lookup budget.

### H31. Compaction commits only the joint read
- **Mechanism:** Append few-bit residual slices as they arrive. During compaction model their combined actual readout, including quantizer saturation, and fit one replacement tile; keep the old slices until the combined read passes held-out-from-fit calibration.
- **Novelty / tag:** **Improvement** — unlike chronological replay or additive adapter merge, compaction treats the analog read of the segment as the reference. Near log-structured stores and adapter distillation.
- **First test / tie:** Compact saturated residual slices on three toy token maps, including A then B; retest A following reclaim. Compare to simple merge-then-quantize using the same space, examples, and fitting steps.

### H32. Read amplification as learning pressure
- **Mechanism:** Run an agent's newest notes in a small lookup tier and older leaves in a bounded tree. If answering requires multiple leaves, train a directly executable macro on the verified combination and cache it as an additional read path; leave source leaves independently readable.
- **Novelty / tag:** **Improvement** — pressure comes from measured redundant reads, not frequency of a lesson alone. Near LSM read amplification and reasoning amortization; macros compose existing reads rather than memoizing answers.
- **First test / tie:** In a toy schema agent, add B compositions of A subskills; track held-out A and novel combinations at a fixed read and storage budget against caching the most frequent outcomes.

### H33. Behavioral write combining
- **Mechanism:** Accumulate updates in a controller buffer by the output signature they change, not the address they target. Before issuing pulses, solve for one sparse combined update that approximates their aggregate response at old anchors and new inputs.
- **Novelty / tag:** **Primitive** — a write-combine key is functional rather than spatial. Near optimizer microbatching and LSM compaction; it can combine updates originally computed in different adapter rows.
- **First test / tie:** Stream small rank-one edits for overlapping fact keys; measure A retention and B gain against equal-size coordinate accumulation at matched pulses and fitting FLOPs.

### H34. Cache coherence for learned assumptions
- **Mechanism:** Tag an agent's derived memory with the actual verified premises it read and monitor resolution traffic. If another worker updates a premise, issue an invalidation only to caches that consumed it; reads detect stale state with a version token until the next derivation.
- **Novelty / tag:** **Improvement** — nearest B32's dependency cache, now with consumer-specific invalidation under asynchronous multi-agent learning rather than global flush.
- **First test / tie:** Add a tool field while two tiny router workers update different premises; retest A on unaffected old workflows. Compare to periodic global refresh using the same invalidation messages and derivation-token budget.

### H35. Allocate cells by worst-case loss on power interruption
- **Mechanism:** Split an adapter update into independently executable chunks and order their publication so each prefix keeps old probes within tolerance. Power loss discards the staging suffix, not the partially learned learner.
- **Novelty / tag:** **Primitive** — a *prefix-safe update* can be interrupted without needing rollback. Near crash consistency and certified CL; certification covers intermediate visible writes, not just endpoints.
- **First test / tie:** Preempt a tiny MLP's B edit at random pulse boundaries; retest A at interruption and after completion. Compare to atomic double-buffer commits at equal peak bytes and physical writes.

### H36. Read-only snapshots of plasticity permissions
- **Mechanism:** Freeze a small bitmap of which adapter slots may receive learning during an episode while keeping the weights themselves live. If a new task transfers ownership mid-episode, later reward must reconcile against the old permissions before applying delayed updates.
- **Novelty / tag:** **Primitive** — snapshot *who can write where*, rather than past behavior or a past model. Near transaction snapshot isolation and H15; this allows recycling during the call and reconciles at commit instead of locking cells.
- **First test / tie:** Stream overlapping long and short tool episodes; retest old A under late feedback after B. Compare to last-writer-wins plus standard staleness caps with the same metadata and learner operations.

### H37. Cross-tier learning with exclusive writes
- **Mechanism:** After a pattern moves from fast context memory to a compiled adapter, only the active tier can assimilate new evidence for that pattern. Fast context keeps a read-inert repair stub until an error promotes it back to writable.
- **Novelty / tag:** **Improvement** — cache ownership rather than double dosing; near exclusive caches and interpreted-to-compiled patches. The transferred state is update authority, not the same lesson applied twice.
- **First test / tie:** Run recurring old tool rules then a mix of corrections and new B rules. Retest unchanged A workflows; compare to ordinary two-tier promotion with an equal token, storage, and write budget.

### H38. Spare rows that store replacement functions
- **Mechanism:** Instead of mirroring an entire vulnerable tile, train a small frozen spare tile to approximate its feature-conditioned residual directly. If later programming corrupts the live tile, route only the affected subdomain through its spare.
- **Novelty / tag:** **Improvement** — a spare row stores an approximate replacement *function*, not a data copy; near shadow models and functional redundancy. Unlike functional syndromes it does not infer sparse fact damage from coded probes.
- **First test / tie:** Inject contiguous tile failures after B training on a toy transducer; score held-out A across regions. Compare to equal-bit quantized mirrors with the same detection mask and fallback reads.

### H39. Hand off write debt, not experience logs
- **Mechanism:** A site out of pulse budget transfers a bounded escrow of unserved desired residuals and a domain constraint to another device or worker. The receiver settles debt on its own live feature basis rather than copying the first worker's optimizer state.
- **Novelty / tag:** **Primitive** — gradient IOU is the neighbor; this object is explicitly transferable across unlike writable substrates and payable by functional equivalence with a domain limit.
- **First test / tie:** Cut one of two adapter learners' simulated endurance midway through B; retest old A on both. Compare to same-byte replay and delta export given equal total writes and network traffic.

## Timing, reconfiguration and shared fabric

### H40. Clock gating as a learned decomposition
- **Mechanism:** Train a residual bank on heterogeneous update clocks; every event chooses only a small set of clocks to tick. Fit the clock-choice policy on future verified benefit so recurring motifs update slowly while transient discrepancies can trigger rapid writes elsewhere.
- **Novelty / tag:** **Improvement** — learns per-event clock enables rather than assigning all weights a fixed cadence. Near Clockwork RNN and multi-timescale optimizers.
- **First test / tie:** Sequentially add volatile B rules on top of stable A rules to a tiny policy; retest A after multiple B shifts. Compare to fixed per-bank clocks at equal pulse and controller-compute budgets.

### H41. A synchronizer for stale gradients
- **Mechanism:** If an adapter update crosses a token/episode clock boundary, sample its source activation signature on consecutive receiver ticks. Issue the write only if the direction still agrees with the stored signature; otherwise use the second tick to reproject onto currently valid features.
- **Novelty / tag:** **Improvement** — clock-domain metastability inspires a specific cross-clock update acceptance/reprojection rule. Near stale-gradient compensation.
- **First test / tie:** Asynchronous CPU workers with changing feature bases learn rotating rules; retest held-out A after B. Compare to age-weighted gradients with matched forwards, buffering, and writes.

### H42. Out-of-order learning with a reorder buffer
- **Mechanism:** Fit the next ready skill on a private bank before a slow previous episode returns. Commit only in dependency order; if the earlier result changes a needed interface, replay the later *update computation* against the new feature state.
- **Novelty / tag:** **Primitive** — lets learning execute speculatively while ordering it by prerequisites, not arrival or reward times. Near CPUs' reorder buffers and speculative optimization.
- **First test / tie:** Give a 3-tool toy agent variable verifier delays and a prerequisite graph; measure time to master B and retained A after conflicts. Compare to ordered fitting with equal workers, buffers, and update budget.

### H43. Learn a fence instruction
- **Mechanism:** Train a small policy to emit a fence event before publishing a memory write that another worker may consume. Rather than always blocking until all old writes settle, a fence synchronizes only its touched adapter pages and derived-cache entries.
- **Novelty / tag:** **Primitive** — the agent learns *where synchronization is needed for learning*, separately from what to remember. Near memory-order fences and dependency-aware transactions; H42 instead orders known prerequisites.
- **First test / tie:** Learn B schema updates in an agent with two concurrent consumers; retest held-out A on unchanged fields. Compare to fixed fences and globally ordered commits at equal stall time and controller compute.

### H44. Partial-reconfiguration sockets
- **Mechanism:** Hold a frozen residual-stream stub with stable shape and learned input/output contracts. Fit a new low-rank microcircuit into a small slot while neighboring slots remain live; only the stub may translate voltage or feature scales.
- **Novelty / tag:** **Improvement** — FPGA partial reconfiguration supplies locality and live continuation. Near P19's stable ABI and modular adapters; the distinctive test compares service interruption during learning.
- **First test / tie:** Swap a single middle-layer slot of a toy LM while adding B; run held-out A before, during, and after swap. Compare to whole-block swap using equal reserve bytes and update compute; record stall time.

### H45. Power-cut latent adapters
- **Mechanism:** Partition a model into adapter islands that can lose their fast state entirely between relevant requests. Jointly learn the route and a context-independent startup state from which an old skill can answer its first cold request.
- **Novelty / tag:** **Improvement** — power-gating exposes a specific cold-start retention objective beyond sparse activation; near MoE and recurrent-state reset.
- **First test / tie:** Train a recurrent toy language head on alternating symbol streams; cold-start before held-out A after B and measure first-answer accuracy. Compare to an equally sparse adapter with ordinary zero-state reset and matched startup operations.

### H46. Brownout read semantics
- **Mechanism:** Train a single quantized adapter to expose nested executable residuals as its bit-planes become readable. Allocate high bits using old task sensitivity while making new features useful at higher power; no path loads different weights.
- **Novelty / tag:** **Improvement** — near progressive quantization and anytime networks, with retention required across *all* power states after each write, not just on the full read.
- **First test / tie:** Use 2-, 4-, and 8-bit read modes on a toy classifier and retest A at each tier after B. Compare to matched uniform quantization-aware training given the same storage and read-energy schedule.

### H47. Feature races that emit evidence
- **Mechanism:** Launch two cheap learned approximations of a skill on parallel lanes with different feature orderings. The faster lane proposes the decision; the gap in finish times, calibrated from held-out-from-fit traces, decides when to train a correction or ask for verification.
- **Novelty / tag:** **Primitive** — runtime contention becomes a differential learning signal rather than using only output uncertainty. Near race logic, early exiting, and disagreement-based active learning.
- **First test / tie:** Introduce B cases where A's cheap classifier is wrong at high confidence; retest A after correction. Compare to equal-op disagreement and confidence controls with equal verifier calls.

### H48. Isolate write traffic by learned bandwidth tenancy
- **Mechanism:** Give clusters of agent memories separately metered read/write queues. A live stream can borrow service slots; if that delays a tenant's reads, repay by reserving later windows during which the borrower cannot write banks that tenant reads.
- **Novelty / tag:** **Improvement** — near quality-of-service scheduling and replay budgeting; optimizes memory interference through actual read/write service rather than loss weighting.
- **First test / tie:** Simulate bursty new-tool learning alongside old queries, score A accuracy including timeouts through B. Compare to fixed weighted fair queueing at equal maximum bandwidth and buffers.

### H49. Opposed routing on a reconfigurable interconnect
- **Mechanism:** Map forward residual routes and backward credit routes independently through a small switch fabric. If learning B would change a shared forward path that A needs, connect B's credit to a compensating block while leaving the forward topology intact.
- **Novelty / tag:** **Primitive** — independent, persistent credit wiring can be learned separately from feature transport. Near feedback alignment and P21's register machine; this changes the routing of local teaching signals, not forward instructions.
- **First test / tie:** Use a four-block toy controller with linked subtasks; retest A after learning B. Compare to fixed feedback alignment and ordinary gradient masking at equal switch state and update operations.

### H50. Branch-predict the next expendable write
- **Mechanism:** Train a tiny branch predictor on recent verified write outcomes to preposition a fresh adapter workspace. Mispredictions discard only untouched workspace reservations; successful predictions reduce time to learn without changing which update is accepted.
- **Novelty / tag:** **Improvement** — speculation applies to preparation for a learning operation, not selecting lessons. Near allocator prefetching and gradient IOUs.
- **First test / tie:** Replay a stream with abrupt tool changes and small workspace budgets; track delay to new mastery and held-out A after B. Compare to LRU-based workspace preallocation at equal reservation bytes and controller work.

### H51. Pipeline bubbles as consolidation slots
- **Mechanism:** During idle frontend stages, pass a few old activations locally through the free blocks and maintain their output behavior while the live stream is queued elsewhere. Give each block a right to decline if its version differs from the stored activation's contract.
- **Novelty / tag:** **Improvement** — uses measured idle compute and explicit activation compatibility instead of a global replay schedule. Near pipeline replay and distributed continual distillation.
- **First test / tie:** Run asynchronous token waves on a 4-block LM simulator; compare A retention after B with opportunistic replay vs fixed interval replay given equal updates, activation storage, and wall time.

### H52. Elastic depth under partial fault
- **Mechanism:** Provide a short physical bypass around each slow plastic stage. When a stage goes unavailable during a write, the rest of the model runs with the bypass; train both full-depth and bypass modes on normal requests over the stream.
- **Novelty / tag:** **Improvement** — near LayerDrop and dynamic inference depth; the target is service continuity during writes, not test-time compression.
- **First test / tie:** Simulate one blocked stage while fitting B; retest held-out A during blockage and afterward. Compare to matched stochastic layer dropping at equal extra compute and bypass capacity.

## Wave, reservoir and in-memory learning

### H53. A read key made from wavefront geometry
- **Mechanism:** Superpose grating-like projections of adapter coefficients on one simulated optical plate. Learn a small query-to-wavefront map; changes in angle read separate low-rank residuals, while the plate places new gratings to avoid crossing old ones within the measured angular bandwidth.
- **Novelty / tag:** **Primitive** — a learned key is a controllable optical mode that doubles as a placement constraint. Near angularly multiplexed holography and key-based weight superposition.
- **First test / tie:** Simulate finite-aperture interference for eight token-domain mappings; test A recall under unseen query and angle jitter after B. Compare to digital superposition of equal effective bits and equal read operations.

### H54. Holographic writes that tolerate lost fragments
- **Mechanism:** Distribute an adapter's low-rank factors across an aperture such that every contiguous subaperture can generate a lower-resolution version. Write new tasks into spare frequency bands instead of copying an old bank.
- **Novelty / tag:** **Improvement** — the failure target is graceful *spatial truncation*, unlike killed redundant lesson fragments or coded fact syndromes. Near holographic distributed storage and erasure coding.
- **First test / tie:** Block random contiguous regions after B in a Fourier simulator and retest A at several occlusion sizes. Compare to matched erasure-coded digital storage with equal redundancy, reads, and reconstruction latency.

### H55. Training by destructive interference at read boundaries
- **Mechanism:** Place B updates on a simulated interferometer. Optimize phase shifters to cancel B's optical contribution for old anchor inputs while adding it constructively for new inputs. Calibration measures output fields at designated boundary ports rather than recovered skill parameters.
- **Novelty / tag:** **Improvement** — near photonic mesh training and OGD; the distinctive claim is that coherent cancellation can enforce an old-input null without explicitly storing a gradient basis.
- **First test / tie:** Train a small phase-only mesh on A/B regression and retest A under phase noise. Compare to equal-parameter projected digital updates using the same anchors and training budget.

### H56. Photonic interference exposes a pairwise read primitive
- **Mechanism:** Retrieve two learned low-rank feature transforms as fields, read their summed intensity, and subtract the independently calibrated powers to expose a bilinear interaction. Add B interactions without retraining the stored unary transforms.
- **Novelty / tag:** **Primitive** — interaction is a selectable read operation, with pair identity independent of where the unary functions were learned. Near optical homodyne detection, bilinear pooling, and holographic composition.
- **First test / tie:** Fit A unary predictors and B pair exceptions using a wave simulator, then retest held-out unary A and unseen pairs. Compare with matched digital rank-limited bilinear pooling at the same parameters and per-pair cost.

### H57. Delay line as memory router
- **Mechanism:** Feed the version of an agent's event stream addressed to a memory row into a bank of delay lines. Learn only the taps and binding features: two observations separated by a characteristic delay bind to a skill even if the individual cue words or values change.
- **Novelty / tag:** **Primitive** — separation in event time becomes a reusable address feature, not a task ID or recency weight. Near tapped delay networks and reservoir computing.
- **First test / tie:** Teach two multi-step toy workflows sharing the same tool names but different event delays; retest A after a third B workflow and timing jitter. Compare with a temporal convolution of equal taps and memory.

### H58. Fit an inverse key to an untrainable reservoir
- **Mechanism:** Let a fixed delayed reservoir settle into a task-specific trajectory. Learn a small pre-input waveform to steer a generic query toward that trajectory; the readout remains shared and fixed, so acquiring a new task mostly writes a waveform.
- **Novelty / tag:** **Primitive** — the learned object is an inverse control input to a fixed physical dynamical memory. Near prompt tuning and driven reservoirs; test whether temporal control beats equal-size static prefix control.
- **First test / tie:** In an echo-state network with a shared readout, learn A then B sequence transforms and test old A with jitter. Compare to equal-byte static embeddings and equal recurrent operations.

### H59. Reservoir state contracts that survive a hardware swap
- **Mechanism:** Two dissimilar reservoirs agree to exchange short trajectories of measured anchor states rather than full hidden vectors. Train a receiver-side readout from those trajectories after replacement, while untouched readouts continue to run on the original reservoir.
- **Novelty / tag:** **Improvement** — P19 and task-vector transport are neighbors; this transfers a *time-domain interface* that tolerates different internal dynamics, not a moved weight delta.
- **First test / tie:** Swap recurrent topology for a new B skill and migrate one A skill; test both migrated and untouched held-out A. Compare to equal-byte single-state alignment with the same calibration trajectories and compute.

### H60. Bank-local gradient auctions
- **Mechanism:** Each memory bank evaluates a new example's local residual gain against its own old activation sketches, then returns just a quantized bid and intended pulse cost. A controller authorizes only the winning writes; no full gradient or old examples leave the bank.
- **Novelty / tag:** **Improvement** — near sparse routing, reservoir readout selection, and market proposals; the claim is comparable acquisition and retention under a hard off-bank traffic limit.
- **First test / tie:** Split a linear memory head into banks and train overlapping A/B edits. Retest old A and compare to top-gradient-byte and round-robin controls with the same pulse and off-bank byte budgets.

### H61. Rewrite the data's neighborhood instead of the weights
- **Mechanism:** When two shards of an agent's memory repeatedly contribute useful joint evidence, learn a new physical placement that colocates them near the same compute-in-memory matcher. Each local service forms joint keys before transmitting anything to the model.
- **Novelty / tag:** **Improvement** — near graph partitioning and processing-in-memory. Placement changes what conjunctions a fixed-FLOP reader can afford, not just their lookup latency.
- **First test / tie:** Run a sharded synthetic agent with compositional B queries and single-shard A queries. Retest A after relocation and compare to equal-bandwidth cached cross-shard routing given the same compute and migration bytes.

### H62. Differential sensing of disputed rules
- **Mechanism:** Put competing agent rules on the two inputs of a sense amplifier. For a query, the first read identifies only the favored rule; a second calibrated differential read estimates which input caused the conflict and can update that input independently after verification.
- **Novelty / tag:** **Improvement** — near comparator circuits and contrastive retrieval; conflict is a local read/write event without giving the LM both conflicting descriptions.
- **First test / tie:** Simulate tool rules with overlapping aliases; acquire B aliases and retest A including ambiguous held-out queries. Compare to scoring both full rules then updating the losing one, with matched bytes, verifier calls, and operations.

### H63. Noise correlation as learnable uncertainty wiring
- **Mechanism:** Couple stochastic bits across otherwise independent residual branches by programming their shared noise source. Verified failures update the coupling only: branches that fail together are sampled together, leaving each branch's mean local readout fixed.
- **Novelty / tag:** **Primitive** — learned uncertainty lives in the *joint sampling circuit* rather than mean weights or per-lesson temperatures. Near p-bits and correlated posterior sampling; not physics-math #20's noise-assisted recall.
- **First test / tie:** In a toy planner with correlated tool failures, learn a B correlation shift and retest A decision accuracy and calibration. Compare to matched independent noise and a low-rank digital sampler with the same state and samples.

### H64. Anneal the routing fabric without annealing skills
- **Mechanism:** Let a stochastic switch fabric sample combinations of frozen skills. Cool only switches whose coactivation has been verified useful for B, preserving all component weights and leaving unexplored switch combinations hot.
- **Novelty / tag:** **Improvement** — near simulated annealing and frozen-expert routing; selectively anneals the topology of compositions, not parameters or the model's decoding temperature.
- **First test / tie:** Teach a tiny planner two B composites over known A actions and retest A primitives and earlier composites. Compare to entropy-regularized routing with identical search samples and verifier calls.

### H65. The learning path as an impedance measurement
- **Mechanism:** Send a small swept perturbation into one endpoint of a trained module chain and record amplitude/phase at a few internal buses. When B needs a new branch, attach it at a port whose perturbation response predicts weak coupling into A-critical bands.
- **Novelty / tag:** **Primitive** — a learned module has a reusable *frequency-domain port description* for attachment, complementary to a type signature. Near system identification, steering tomography and guided edit-site selection; a frequency response is useful only if it predicts actual cross-task interference.
- **First test / tie:** Linearize a four-stage recurrent agent on a few A anchors, attach a B response, and retest held-out A. Compare to random site plus a data-aware local edit and to static Jacobian screening at equal perturbations and fitting work.
