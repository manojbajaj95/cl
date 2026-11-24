# Idea flood: databases, version control and distributed systems

Proposer angle: treat a continually learning model or agent as a **stateful system** (a database, a repository, a replicated service) and import the operations those fields invented to change state safely while still serving reads. Raw and unfiltered by design; the reviewer grades.

Read before writing: `reviews/idea-ledger.md` and `reviews/flood-triage.md` ([PR #6](https://github.com/manojbajaj95/cl/pull/6)). Deliberately **not** re-proposed here: prompt-addressable checkpoints (L1), the seed log (SM1), round-trip consolidation (N1), CRDT model merging (2605.19373, MELD 2608.16357), three-way merge / bisect / blame / COW (programs-weights P11–P16), reachability GC (P33 / N3), schema migrations (CL-bench B1), task-vector transport across bases. Where an idea below sits next to one of these, the near neighbour is named.

Format per idea: **Mechanism** · **Why it might be new** (near neighbours) · **Cheapest first test** (always with a retention check: old tasks still work).

Default testbed unless stated ("the toy"): a small MLP or 2-layer transformer trained on a stream of 5 synthetic tasks (permuted/rotated modular arithmetic or the G1 rule router), CPU, 3 seeds; **retention** = accuracy on tasks 1..k-1 after learning task k, compared with sequential fine-tuning, replay at equal budget and EWC.

---

## A. Transactions and concurrency control

### SD1 ACID learning transactions with rollback-on-constraint
- **Mechanism:** Each update batch is a transaction `BEGIN; Δθ; CHECK constraints; COMMIT|ABORT`. Constraints are declared once ("task-2 accuracy ≥ 0.9", "refusal rate on probe set unchanged") and checked on a cheap probe set before commit; aborted transactions are not discarded but *split* (binary search over the batch) to find the minimal subset that commits — a learned analogue of partial commit.
- **Why new:** Gated updates exist (A-GEM rejects gradients that hurt memory), but declarative constraints + abort + automatic batch splitting to the maximal committable subset is a DB primitive, not a projection. Near: GEM/A-GEM, safe policy improvement.
- **First test:** Toy stream with one adversarial conflicting task. Arms: SFT, A-GEM, SD1 (split-to-commit). Retention on declared tasks must stay ≥ constraint; measure how much new-task accuracy the split recovers vs full abort.

### SD2 MVCC weights: readers never see a half-learned model
- **Mechanism:** Keep version vectors per parameter block (`θ_b@t`). Learning writes new versions; each inference request takes a *snapshot timestamp* and reads a consistent cut. Garbage-collect versions no live snapshot needs. The CL twist: a request can pin an *old* snapshot per block (e.g. the old attention, the new MLP) — mixed-version reads become a search space for retention.
- **Why new:** Checkpoint ensembles exist; per-block multi-version reads with snapshot isolation semantics, and the finding of which mixed cuts preserve old tasks, is a new object (a version lattice over blocks). Near: L1 (one tag for the whole model), model soups.
- **First test:** Train toy through 5 tasks keeping per-layer versions. Exhaustively score all mixed cuts (layers × versions) on old + new tasks; does some cut dominate both final and best-checkpoint on the Pareto front? Retention is the old-task axis of that front.

### SD3 Write-skew detection between two lessons
- **Mechanism:** Two updates each preserve an invariant alone, but jointly violate it (classic snapshot-isolation write skew). Detect by evaluating invariants on Δ₁, Δ₂, and Δ₁+Δ₂; when only the sum fails, record a *conflict edge* and serialize them (apply one, re-derive the other on top).
- **Why new:** Pairwise interference measures exist (gradient cosine), but "each fine, together broken" is a specific anomaly class with a specific fix (serialization). Near: merge interference audits (ledger kill: coded merge interference) — this is about the anomaly, not group testing.
- **First test:** Generate 20 LoRA updates on toy; count write-skew triples; compare retention of averaging vs SD3 serialization on the skewed pairs only.

### SD4 Optimistic concurrency for parallel learners
- **Mechanism:** N workers fine-tune from the same base on different tasks; at commit each validates that the blocks it *read* (high-sensitivity params for its task, via Fisher) were not changed by an earlier committer; if they were, it rebases (re-runs a few steps on the new base) instead of merging.
- **Why new:** Model merging merges blindly; OCC's read-set validation decides *when* merging is safe vs a rebase is needed. Near: TIES/DARE, async SGD staleness.
- **First test:** 4 parallel toy tasks. Arms: average, TIES, OCC-rebase at equal total steps. Retention = all 4 tasks after final commit.

### SD5 Two-phase locking on features
- **Mechanism:** An SAE (or simple dictionary) over activations gives "rows". A learner must acquire a shared lock to read a feature and exclusive lock to change it; growing phase then shrinking phase. Updates that would write a feature locked shared by a still-active old skill are blocked or queued.
- **Why new:** Parameter-isolation methods (PackNet/HAT) freeze params; this locks *features*, with locks released when a skill is retired, giving a lifecycle. Near: PackNet, HAT, SAE-based editing.
- **First test:** Toy with dictionary features; implement lock check as a projection that removes components along locked feature write-directions. Retention vs OGD at equal compute.

### SD6 Deadlock graph for skill dependencies
- **Mechanism:** When skill A's update needs to change features B depends on and vice versa, the wait-for graph has a cycle; resolve by choosing a victim (cheapest to re-learn, by measured relearn cost) to roll back and re-acquire later.
- **Why new:** Gives a principled tie-breaker for mutual interference: retrain the cheaper-to-relearn skill. Near: savings-based replay.
- **First test:** Two mutually interfering toy tasks; compare "victim = cheaper relearn" vs random victim vs joint training; retention measured after victim relearning at equal total steps.

### SD7 Isolation levels as a learning hyperparameter
- **Mechanism:** Expose READ UNCOMMITTED (inference sees in-flight updates), READ COMMITTED, SNAPSHOT, SERIALIZABLE for an online-learning agent. Measure which anomalies (dirty reads = acting on half-learned lesson; non-repeatable reads = same query different answer within an episode) hurt task success.
- **Why new:** Online agents learning mid-episode is common; nobody classifies the failure modes as isolation anomalies. Might give a taxonomy primitive.
- **First test:** Agent toy where memory/lesson writes happen mid-episode; run the 4 isolation levels; count anomalies and episode success; retention = earlier-episode tasks.

### SD8 Sagas: compensating updates instead of rollback
- **Mechanism:** A long learning job is a saga of steps; each step registers a *compensating update* (e.g. a learned anti-LoRA computed when the step commits, while data is still at hand). If later steps fail, apply compensations in reverse rather than restoring a checkpoint — keeping unrelated later learning.
- **Why new:** Anti-updates exist (learning primitives D5), but registering the compensation *at write time* with the saga ordering is new. Near: D5 anti-updates, unlearning.
- **First test:** Stream of 5 tasks where task 3 is later declared "bad". Compare checkpoint restore (loses 4,5), unlearning after the fact, and saga compensation; retention on 1,2,4,5.

### SD9 Idempotency keys for experience
- **Mechanism:** Each experience carries a content hash; the learner guarantees an experience applied twice has the effect of once (store the per-key update and subtract/skip on duplicate). Replay then never over-weights duplicates; agents retrying the same episode don't drift.
- **Why new:** Dedup of datasets exists; idempotent *updates* at the learner level, applied online, is a learner property. Near: O1 idempotent learning operators (learning primitives) — this is the systems-key version, keyed not algebraic.
- **First test:** Stream with 30% duplicated batches; SFT vs dedup-before vs idempotency-key ledger; retention and calibration of old tasks.

### SD10 Exactly-once lesson delivery across a fleet
- **Mechanism:** Fleet agents share lessons via a log with offsets; each agent commits its consumer offset atomically with its memory write, so a crash never double-applies or loses a lesson.
- **Why new:** Probably an engineering primitive; included because fleet-memory papers ignore delivery semantics and duplicates may cause measurable emphasis inflation (cf. econ E4).
- **First test:** Simulate crashes in a lesson-sharing fleet; at-least-once vs exactly-once; measure duplicated-lesson emphasis and old-task success.

## B. Logs, recovery and storage engines

### SD11 Write-ahead log of gradients with redo/undo
- **Mechanism:** Log every applied update (compressed: top-k or low-rank) before applying. Recovery = redo from last checkpoint; forgetting surgery = undo specific log records while redoing everything after with a *correction* (ARIES-style compensation log records).
- **Why new:** SM1 is the seed log for regeneration; ARIES adds undo of a middle record with redo of later records, which is the hard CL case. Near: SM1, exact unlearning via SISA.
- **First test:** Toy 5-task stream, log low-rank updates; undo task 3 records + redo 4,5; compare with SISA retrain cost and with naive subtraction; retention on 1,2,4,5 and task-3 removal.

### SD12 LSM-tree memory: memtable in context, SSTables in weights
- **Mechanism:** New facts go to an in-context memtable; when full, flush to a small immutable adapter (SSTable level 0); periodically compact level-k adapters into level-k+1 (merge-distill), with tombstones for deleted facts. Reads check memtable → L0 → L1... with Bloom filters (SD13) to skip levels.
- **Why new:** Context-to-weights consolidation exists one way (ENGRAM, Cortex); the leveled, size-tiered compaction schedule with tombstones and read-path is the LSM primitive, and write amplification becomes a measurable forgetting cost. Near: ENGRAM 2611.09472, Cortex 2610.20399.
- **First test:** Stream of 1000 synthetic facts; LSM (3 levels of LoRA) vs single growing LoRA vs RAG; measure write amplification (distill steps per fact), recall of early facts (retention), update/delete correctness.

### SD13 Bloom filters over adapters for "do I know this?"
- **Mechanism:** Each adapter/skill gets a tiny learned membership filter over input embeddings (false positives allowed, no false negatives on its training set). Router consults filters; an adapter is loaded only on hit; adding a skill never retrains the others' filters.
- **Why new:** Learned routers are retrained as experts are added and drift; per-adapter one-sided-error filters are append-only. Near: MoE routing, LoRA hubs, learned Bloom filters (Kraska).
- **First test:** 20 toy task adapters added sequentially; filter routing vs learned router retrained each time; retention = routing accuracy on early tasks.

### SD14 Compaction with tombstones as the forgetting operator
- **Mechanism:** Deletion is a tombstone record (a negative example set); forgetting happens only at compaction, where the merge-distill sees tombstones and the live data. Defers unlearning cost and batches it.
- **Why new:** Unlearning literature is per-request; batched tombstone compaction is an amortization primitive. Near: SISA.
- **First test:** 100 deletion requests over a fact stream; immediate unlearning vs batched-at-compaction; total compute, residual leakage, retention of non-deleted facts.

### SD15 B-tree indexed experts
- **Mechanism:** Experts are keys in a balanced tree over an embedding order; inserting a skill splits a node (two children inherit parent adapter + fine-tune); routing is O(log n) comparisons. Splits are local: other leaves untouched.
- **Why new:** Hierarchical MoE exists; split-on-insert with a balancing invariant ties capacity growth to data. Near: hierarchical MoE, book-style nested skills (killed as retrieval; this is weights).
- **First test:** 32 toy tasks inserted; B-tree experts vs flat MoE grown; retention of early tasks and routing cost.

### SD16 Checkpoint + delta-chain storage with cheap point-in-time recovery
- **Mechanism:** Store rare full checkpoints and low-rank deltas; recovery to any time = base + Σ deltas. Main question: does the low-rank chain accumulate errors (drift) and does periodic "rebasing" bound it.
- **Why new:** Mostly engineering; included as the substrate for L1/SD11 tests. Near: L1.
- **First test:** Reconstruct the toy's checkpoint at t=k from deltas at rank r; retention = reconstructed model's old-task accuracy vs true checkpoint.

### SD17 Buffer pool for knowledge: page-in adapters by working set
- **Mechanism:** Fixed GPU budget of K adapters; others paged to disk; eviction by LRU-K over recent task hits. Prediction: the forgetting curve of a paged system is the miss-rate curve, so classical cache theory (working-set model) predicts forgetting under capacity.
- **Why new:** Gives an analytical forgetting law from Denning's working-set theory. Near: S-LoRA serving.
- **First test:** Simulated task-request traces with locality; compare predicted vs measured old-task accuracy with K adapters.

### SD18 Torn-write detection in weights
- **Mechanism:** A partially applied update (preempted job, merged mid-training) leaves a "torn" model. Store per-block checksums of function (outputs on canary inputs) so a torn state is detected and repaired by redo.
- **Why new:** Canary-based functional checksums of blocks; partial-update states are common in practice and untested for retention.
- **First test:** Apply 50% of blocks of a task-update; measure retention damage vs full or none; canary detection rate.

## C. Version control beyond merge/bisect

### SD19 Patch theory (Darcs/Pijul) for weight updates
- **Mechanism:** Treat updates as patches with commutation rules: patch A and B commute if applying in either order yields same function on probe sets; non-commuting patches carry a dependency. Then any subset of commuting patches can be cherry-picked; history is a set not a sequence.
- **Why new:** Ledger has "rebasing by measured noncommutation" (harness #7, scored 3); patch-theoretic *dependency inference* that lets you remove patch 3 while keeping its dependents rewritten is the new piece. Near: harness node #7, O2 commutative operators.
- **First test:** 10 LoRA patches on toy; measure pairwise commutation; remove one patch and its dependents vs naive subtraction; retention of the remaining tasks.

### SD20 `git rerere` for interference
- **Mechanism:** Record how a merge conflict between two skills was resolved (the fine-tune steps that repaired it); when a structurally similar conflict recurs (similar gradient-conflict signature), replay the recorded resolution as an initialization.
- **Why new:** Conflict-resolution reuse, keyed by conflict signature. Near: meta-learning, learned optimizers.
- **First test:** Families of conflicting toy task pairs; rerere init vs fresh repair; steps to repair and retention.

### SD21 Semantic merge driver: merge by behavior, not parameters
- **Mechanism:** A merge is defined on the behavior of two branches: sample disagreement inputs, let a referee (verifier or the base) pick, distill into one model. A "conflict" is an input where both branches are confident and disagree; conflicts are surfaced like git conflict markers for a human or verifier.
- **Why new:** Distillation-based merging exists; explicit conflict surfacing as a first-class output is the VC primitive. Near: knowledge distillation merges, MELD.
- **First test:** Two toy branches with overlapping contradictory tasks; count conflicts, resolve by verifier; retention on both branches' non-conflicting tasks vs TIES.

### SD22 Sparse checkout of a model
- **Mechanism:** Fine-tune only on a "checkout" of blocks relevant to a task path (by attribution), with the rest frozen; commit writes only those blocks. Repeated sparse checkouts create a per-block history; conflicts only arise when checkouts overlap.
- **Why new:** Close to sparse fine-tuning; novelty is the per-block history and overlap-based conflict prediction. Near: sparse memory finetuning (ledger: covered).
- **First test:** Predict forgetting from checkout overlap; retention vs full fine-tune.

### SD23 Signed commits: provenance-carrying updates
- **Mechanism:** Every update carries a signature over its data hash and a "behavioral receipt" (probe-set diff). A model can later answer "which commit taught me this?" by matching its current behavior diff to receipts.
- **Why new:** Training-data attribution is a separate field; receipts recorded at commit time make attribution a lookup. Near: TRAK, influence functions.
- **First test:** Toy 20 updates with receipts; attribution accuracy by receipt matching vs TRAK; retention irrelevant here except that receipts must survive later updates (measure decay).

### SD24 Submodules: skills pinned at a version inside a moving model
- **Mechanism:** A skill adapter is pinned to the base version it was trained on; when the base updates, the adapter is run against a *frozen copy of the old base's relevant layers* (a submodule) until it is re-trained. Version skew handled by keeping old dependency.
- **Why new:** Contrasts with transporting adapters (covered). Keeping old dependency slices is cheap if slices are small.
- **First test:** Base drifts over 3 updates; adapter with pinned slice vs transported vs naive; retention of adapter task.

### SD25 Git hooks for learning: pre-commit tests
- **Mechanism:** Learners run a regression test suite per commit; failures reject or trigger fix-up commits. The interesting part: auto-generate the test suite from the model's own old outputs (golden files), with flakiness tracking.
- **Why new:** Like SD1 but test-suite generation from self-goldens with flaky-test detection (stochastic outputs). Near: verifier-measured retention audit (PR #2).
- **First test:** Golden-file suite on toy; pre-commit rejection + fix-up vs plain SFT; retention.

### SD26 Monorepo vs polyrepo of skills
- **Mechanism:** Compare one model (monorepo) vs many small specialists (polyrepo) with an explicit dependency manager (which specialist calls which). Measure "diamond dependency" breakage when a shared lower skill updates.
- **Why new:** Phenomenon study; diamond dependency hell in skill graphs may be a new measurable forgetting route.
- **First test:** Skill graph with shared sub-skill; update it; count downstream breaks in both architectures.

### SD27 Blame-driven replay
- **Mechanism:** For each old-task failure after an update, compute which recent commit caused it (cheap: revert-one tests); replay only data from the blamed commit's victims.
- **Why new:** Blame is covered as tooling (P11–P16); using blame to target replay is the CL step. Near: P11–P16.
- **First test:** Blame-targeted replay vs uniform replay at equal budget; retention.

### SD28 Feature flags over learned behavior
- **Mechanism:** Every new skill is trained behind a flag token; the flag defaults off; behavior is gradually rolled out (flag on for 1%, 10%...) by mixing; old behavior remains retrievable by flag off forever because training includes flag-off = old outputs.
- **Why new:** Close to L1 (tags) but per-skill and gradual rollout with canary metrics. Near: L1, conditional training tokens.
- **First test:** Toy: train task-2 behind flag, measure flag-off retention of task-1 vs untagged training.

## D. Replication, consensus and distributed systems

### SD29 Raft for fleet memory: a replicated lesson log with leader election
- **Mechanism:** Fleet agents propose lessons; a lesson enters shared memory only when a quorum of agents (who replay it on their own tasks) accept. Leaders rotate; partitions don't fork memory.
- **Why new:** Shared memory papers use voting/reputation; consensus with replay-based acceptance is different. Near: ledger kills on social choice / median-of-means (shared-memory governance).
- **First test:** Fleet of 5 with 1 poisoned agent; quorum-replay acceptance vs majority vote vs none; retention of fleet's old tasks.

### SD30 Vector clocks for lessons to detect concurrent contradictions
- **Mechanism:** Each lesson carries a vector clock of what the writer had seen. Two lessons are concurrent if neither clock dominates; concurrent contradictory lessons are flagged; causal ones mean the later supersedes.
- **Why new:** Staleness handling exists; causality-aware supersession (later-in-causal-order wins, concurrent = conflict) is a clean rule. Near: memory staleness papers (saturated).
- **First test:** Simulated fleet with drift; vector-clock supersession vs timestamp-latest vs keep-all; task success on current and old regimes.

### SD31 Gossip-learned weights with anti-entropy via Merkle trees
- **Mechanism:** Agents with personal adapters exchange Merkle hashes of per-block functional fingerprints; only differing blocks are exchanged and merged. Divergence is located cheaply.
- **Why new:** Gossip learning exists; Merkle localization of *functional* differences is new-ish. Near: gossip learning, federated.
- **First test:** 8 agents, different tasks; Merkle-gossip vs full-average; communication and retention of each agent's own task.

### SD32 Chain replication for distillation
- **Mechanism:** Knowledge flows head → tail through a chain of student models; reads come from the tail (most consolidated) and writes enter at the head. Each link distills only what it confirms; the tail is the stable consolidated memory.
- **Why new:** Multi-timescale consolidation exists (fast/slow weights); the chain with acknowledgments gives strong consistency for reads. Near: CLS theory, fast/slow learners.
- **First test:** 3-link chain on toy stream; tail retention vs single fast learner vs EMA teacher.

### SD33 CAP theorem for continual learners
- **Mechanism:** A learner partitioned from its data (offline) must choose: stay Available (serve stale) or Consistent (refuse until synced). Formalize Consistency = behaves as if trained on all data so far; derive impossibility; test PACELC tradeoffs (latency vs consistency) for online agents.
- **Why new:** A theory framing; might give a no-free-lunch for online CL. Moonshot-ish.
- **First test:** Simulated partitioned agents; measure accuracy-staleness tradeoff curves.

### SD34 Quorum reads across checkpoints
- **Mechanism:** Answer a query by reading from R of N past checkpoints and returning the majority; tune R/W like Dynamo. Writes go to W checkpoints (train W replicas on the update). R+W>N guarantees the newest write is seen; R+W≤N gives older behavior back.
- **Why new:** Ensembles exist; R/W quorum semantics give a knob between plasticity and stability with a guarantee. Near: checkpoint ensembles, SD2.
- **First test:** N=5 replicas on toy; sweep R,W; retention and new-task accuracy.

### SD35 Leases on knowledge: time-bounded beliefs
- **Mechanism:** Every learned fact has a lease; without renewal (re-confirmation by data), it expires to "uncertain". Renewal is cheap evidence; expiry is the forgetting.
- **Why new:** TTL in memory exists; leases tied to *confirmation* rather than age. Near: memory TTL, staleness (saturated).
- **First test:** Fact stream with changes; lease vs TTL vs none; accuracy on changed and unchanged facts.

### SD36 Byzantine-tolerant self-consistency within one model
- **Mechanism:** Treat attention heads or experts as replicas; a memory is reliable only if 2f+1 replicas agree. Training targets redundancy so f can be corrupted by later fine-tuning without losing the memory.
- **Why new:** Redundancy as an explicit fault-tolerance target with measurable f. Near: dropout redundancy, coded memory (killed at proposal as covered).
- **First test:** Train with redundancy objective; later fine-tune corrupting random heads; retention vs baseline.

### SD37 Linearizable learning: one global order of updates across agents
- **Mechanism:** Enforce that all agents observe the same order of lesson updates; compare with causal-only and eventual consistency for fleet task success.
- **Why new:** Consistency models as an experimental variable in multi-agent CL.
- **First test:** Fleet sim; three consistency models; success and retention.

### SD38 Consistent hashing of skills over experts
- **Mechanism:** Map tasks to experts by consistent hashing over task embeddings; adding an expert only moves 1/n of tasks, so forgetting from re-routing is bounded.
- **Why new:** Bounded re-routing on growth; MoE re-routing on expansion causes forgetting. Near: MoE expansion.
- **First test:** Add experts over time; consistent hashing vs learned router; retention.

### SD39 Erasure-coded knowledge across adapters
- **Mechanism:** Store k skills in n adapters such that any k adapters reconstruct all skills (Reed-Solomon over low-rank deltas). Losing adapters (or overwriting them) loses no skill.
- **Why new:** Coded fragments killed for memory text; here coding over weight deltas. Near: physics #43 Chinese remainder storage.
- **First test:** k=4 skills, n=6 coded adapters on toy; drop 2; retention.

## E. Query processing, indexing and views

### SD40 Materialized views: precomputed frequent reasoning
- **Mechanism:** Frequent multi-step reasoning chains are materialized into a direct mapping (a small adapter); the view is kept consistent by incremental view maintenance when base facts change: only the affected view rows are updated.
- **Why new:** Distilling chains into direct answers is known; incremental maintenance when base facts change (the ripple-effect editing problem) as view maintenance is the new primitive. Near: ripple-effects editing benchmark, MQuAKE.
- **First test:** Synthetic KB with 2-hop queries; edit base facts; IVM-style updates of 2-hop answers vs re-distilling vs editing only base; retention on unaffected queries.

### SD41 Query optimizer over memory: choose context vs weights vs tool per query
- **Mechanism:** A cost-based optimizer estimates cost and accuracy of retrieving from context, weights, or tool for each query, with statistics updated online; plans are cached.
- **Why new:** Routers exist; cost-based planning with cardinality-like statistics for memory sources. Near: adaptive RAG.
- **First test:** Mixed queries; optimizer vs always-RAG vs always-weights; accuracy, cost, retention when weights update.

### SD42 Secondary indexes in weights
- **Mechanism:** Same knowledge stored with two access paths (forward fact and reverse) as an explicit index; index maintenance happens on every write; tests the reversal curse as a missing index.
- **Why new:** Reversal curse fixes augment data; treating it as index maintenance with write-time cost makes CL edits update both paths. Near: reversal curse papers.
- **First test:** Edit facts with and without index maintenance; reverse-query accuracy and retention.

### SD43 Foreign keys and referential integrity across facts
- **Mechanism:** Declared relationships (person → employer) enforce that deleting/editing one fact cascades or blocks; edits violating integrity are rejected.
- **Why new:** Knowledge editing consistency exists; declarative cascades are a DB primitive. Near: MQuAKE, ripple effects.
- **First test:** Synthetic KB; edits with cascade vs plain ROME; consistency and retention.

### SD44 Triggers: learned "on event do update"
- **Mechanism:** The model maintains triggers: when certain input patterns appear, a stored update fires (an adapter merges in). Triggers persist; rules become event-driven.
- **Why new:** Conditional computation; triggers as persistent event-update rules.
- **First test:** Toy; triggers vs static adapters; retention.

### SD45 Column store for skills
- **Mechanism:** Decompose updates by "column" (feature dimension) instead of by "row" (example); learn new tasks by adding columns. Old tasks read old columns only.
- **Why new:** Progressive nets add columns; this is column-wise storage of features with projection reads. Near: progressive nets.
- **First test:** Retention vs progressive nets at equal params.

### SD46 Bitemporal knowledge: valid time vs transaction time
- **Mechanism:** Each fact has valid time (when true in the world) and transaction time (when learned). The model answers "what did you believe on date X about date Y". Training includes both time tokens.
- **Why new:** Temporal LMs model valid time; bitemporal adds belief history, enabling correction without destroying history. Near: TempLAMA, L1.
- **First test:** Synthetic facts with corrections; bitemporal queries accuracy; retention of old belief queries.

### SD47 Time-travel queries `AS OF`
- **Mechanism:** Like SD46 but for skills: "do this task AS OF version 3". Training retains a version-conditioned head.
- **Why new:** Overlaps L1 heavily; included as the SQL surface.
- **First test:** Compare against L1 if implemented.

### SD48 Cardinality estimation for forgetting
- **Mechanism:** Predict how many old examples an update will break using sketches (HyperLogLog over activation buckets touched by the update).
- **Why new:** Forgetting predictors are gradient-based; sketch-based prediction is cheap. Near: GEM/OGD predictors (ledger F1 kill).
- **First test:** Correlation of sketch prediction with measured forgetting vs gradient cosine.

## F. Stream processing and data systems

### SD49 Watermarks for delayed labels in online learning
- **Mechanism:** Updates wait until a watermark says late labels are unlikely; late data triggers retraction and correction updates.
- **Why new:** Ledger killed delay-compensated gating as covered; watermark + retraction updates may still tie. Near: ledger kill.
- **First test:** Delayed-label stream; watermark vs immediate; retention.

### SD50 Change data capture from the world into the model
- **Mechanism:** Subscribe to world changes (diff of documents) and only train on the diff, with ordering guaranteed.
- **Why new:** Diff-based updates of knowledge; similar to continual pretraining on diffs.
- **First test:** Wiki-like diffs; train on diff vs full doc; retention.

### SD51 Backpressure for learning
- **Mechanism:** If the consolidation queue grows faster than consolidation, the agent throttles intake (asks fewer questions, defers), preventing overload-driven forgetting.
- **Why new:** Learning rate scheduling is internal; backpressure couples to intake. Near: curriculum pacing.
- **First test:** Bursty stream; with/without backpressure; retention.

### SD52 Event sourcing + projections for agent memory
- **Mechanism:** Store only events; memory "views" are projections recomputed by a new projector when the model upgrades. Upgrading the model = re-projecting history.
- **Why new:** Close to SM1 (log regenerates weights) but for agent memory; projections are versioned.
- **First test:** Upgrade reader model; re-project vs keep old memory; success on old tasks.

## G. Weirder imports

### SD53 Cache coherence (MESI) between context and weights
- **Mechanism:** A fact may live in context (cache) and weights (memory); states Modified/Exclusive/Shared/Invalid; when context modifies a fact, weights copy is invalidated (a mask or a suppression vector) until written back. Prevents double-dosing (ledger survivor: context × weights interactions).
- **Why new:** Directly addresses the context-vs-weights interaction survivor with coherence states. Near: KAFT, double dosing.
- **First test:** Facts in both; contradicting context; MESI invalidation vs nothing; accuracy and retention.

### SD54 Read-copy-update (RCU) learning
- **Mechanism:** Readers use old weights while writer prepares new copy; old copy freed after grace period when all in-flight episodes finished. Applied to agents mid-episode.
- **Why new:** Similar to SD2/SD7; specific to episode boundaries.
- **First test:** Combine with SD7.

### SD55 Speculative learning with rollback
- **Mechanism:** Apply an update speculatively, keep serving, verify later; rollback if verification fails, with dependent updates squashed (like CPU speculation).
- **Why new:** D1/D2 deferred commitment adjacent; speculation squash of dependents is the extra. Near: D1, D2.
- **First test:** Toy with delayed verification; retention vs waiting.

### SD56 Garbage collection by generational hypothesis
- **Mechanism:** Most new memories die young; keep a nursery (fast weights) collected often and promote survivors to tenured (slow weights) less often.
- **Why new:** Fast/slow weights are similar; generational collection with promotion threshold by survival count. Near: CLS.
- **First test:** Retention vs fast/slow baseline.

### SD57 Vacuum: reclaim capacity from dead skills
- **Mechanism:** Identify parameters serving only retired tasks and reinitialize them (vacuum), restoring plasticity.
- **Why new:** Plasticity resets exist (ReDo); retire-aware vacuum. Near: ReDo, NOOA #22.
- **First test:** Plasticity and retention of non-retired tasks.

### SD58 Write amplification as the forgetting metric
- **Mechanism:** Define forgetting cost as total parameter change per new fact; minimize write amplification as a training objective.
- **Why new:** Metric-level idea; ties to SD12.
- **First test:** Correlate write amplification with forgetting across methods.

### SD59 Distributed snapshots (Chandy-Lamport) of multi-agent learning state
- **Mechanism:** Take a consistent snapshot of a fleet's memories and in-flight lessons for rollback.
- **Why new:** Engineering; enables fleet-level rollback experiments.
- **First test:** Fleet with poisoned lesson; snapshot rollback vs per-agent checkpoints.

### SD60 Schema-on-read for memories
- **Mechanism:** Store raw episodes; interpret them with a schema decided at read time by the current model (unlike consolidated lessons with fixed schema).
- **Why new:** Similar to raw experience replay with re-reading; may tie RAG. Near: ExpeL, raw trajectory retrieval.
- **First test:** Upgrade model; raw schema-on-read vs pre-written lessons; success.

### SD61 Two-phase commit across model and memory
- **Mechanism:** An update that touches both weights and external memory must commit both or neither; prevents inconsistent states (memory says X, weights say Y).
- **Why new:** Joint consistency of weights + memory. Near: SD53.
- **First test:** Crash injection; consistency rate and retention.

### SD62 Shadow traffic for updates
- **Mechanism:** New model runs on mirrored traffic without serving; divergence on old-task traffic blocks promotion.
- **Why new:** Standard deployment practice; using shadow divergence statistics as a training signal (penalize divergence on mirrored old traffic) is the CL step.
- **First test:** Shadow-divergence regularizer vs replay; retention.
