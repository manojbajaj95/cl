# Learner–world co-evolution (depth 6): the world's guards as long-term memory & outage-proof dual-layer retention

Child node (depth 6) of [PR #368](https://github.com/manojbajaj95/cl/pull/368) (`L6W25` + `L6W19`) · 26 bold candidate primitives · Ideas only; no experiments run

**Parent triage.** In `reviews/flood-triage.md` (latest row, PR #368 / `tree/learner-world-coevolution-6.md`), two score-3 primitives were kept:
1. **`L6W25` — use the world's guards as long-term memory (primary focus of this node):** instead of keeping every old safety skill active in weights or replay buffers, keep external world guards alive and hold each skill internally only as a lightweight 1-step wakeable trace—splitting continual-learning retention across the *environment* and a *wakeable internal pointer* so continual-learning memory literally includes the world.
2. **`L6W19` — cap deployed prevention below the guard-removal threshold while keeping full mastery one step away:** hold expressed prevention below $p_{\text{crit}}$ while `L5W03` keeps 100% prevention one gradient step away, waking immediately on exogenous guard loss.

**Safety boundary (from reviewer triage & round 101 `CAX4`).** Leaving harmful failures un-prevented to keep external guards alive is **strictly restricted to synthetic benchmarks with harmless failures** (e.g., benign formatting/style rules). In any real-world deployment, external world-memory is kept alive via *transparent, independently verified delegation* (`CAX4`, `L7W16`, `L7W18`) or consented dry-run heartbeats—never by degrading existing prevention or manufacturing real harm.

**Why `L6W25` is a fresh continual-learning primitive (Extended Mind / Co-Evolutionary Memory Hierarchy).** Every standard continual-learning memory mechanism—experience replay, episodic buffers, RAG, even hardware memory hierarchies (`Miro`, `2308.06053`)—treats memory as a *passive, static internal store*. `L6W25` introduces an *extended-mind* continual-learning architecture where **the environment's living guards (validators, tools, human checklists, institutional workflows) serve as a volatile, co-evolving L3 memory tier**, paired with a wakeable 1-step internal trace (L2) and active plastic weights (L1). Unlike RAM or RAG, this external memory *decays under disuse*, *mutates asynchronously when the world changes*, *survives base-model swaps intact*, and *can be actively written to* via stigmergic tool/rule compilation!

**Shared literature boundary checked (alphaXiv).**
- *Extended mind, agent memory & environment-grounded memory:* [Memory-Centric Continual Learning for AI Agents](https://arxiv.org/abs/2610.29357), [Grounding Agent Memory: Environment-Probing Curation](https://arxiv.org/abs/2609.11060) (probes the environment to curate an *internal* memory store; `L6W25` treats the *environment's own guards* as the persistent memory tier), [Use and Disuse: Intent-Structured Experience Consolidation](https://arxiv.org/abs/2610.12124) (models use/disuse decay of *internal* memory; here disuse decays *external world guards*), [AutoMem: Automated Learning of Memory as a Cognitive Skill](https://arxiv.org/abs/2607.01224), [When Continual Learning Moves to Memory](https://arxiv.org/abs/2604.27003), [Forget to Improve: Budget-Curated Memory](https://arxiv.org/abs/2606.25115), [Memory as Belief](https://arxiv.org/abs/2610.25119), and [Probing Stability-Plasticity Tradeoffs in Agent Memory](https://arxiv.org/abs/2609.30558).
- *Equal-byte replay, memory hierarchies & dual-memory CL:* [Miro: Continual Learning over Memory Hierarchy](https://arxiv.org/abs/2308.06053) (tiers samples across RAM/flash; `L6W25` extends the hierarchy *outside the device* into living external guards + 1-step wake traces), [FOREVER: Forgetting Curve-Inspired Replay](https://arxiv.org/abs/2601.03938), [CAMR: Compatibility-Aware Memory Replay](https://arxiv.org/abs/2610.36734), [Drift and Dependence: Layer-wise Replay Bounds](https://arxiv.org/abs/2608.11690), [Information-Theoretic Dual Memory System](https://arxiv.org/abs/2501.07382), [Engram Neuron Inspired Adaptive Memorization](https://arxiv.org/abs/2610.14940), and [Complementary Learning Systems](https://arxiv.org/abs/2201.12604).
- *Learning to Defer & transparent delegation:* [Intelligent AI Delegation](https://arxiv.org/abs/2602.11865), [Too Much of the Same: Algorithmic to Human Bias in L2D](https://arxiv.org/abs/2608.28050), [Babysitting AI Agents: Delegation Failures](https://arxiv.org/abs/2610.34748), [Learning to Defer under Expert Drift](https://arxiv.org/abs/2611.26440), and [Learning When Human Decisions Matter](https://arxiv.org/abs/2611.05814).

**Shared falsification rule (from `reviews/flood-triage.md`).** Every `L6W25` world-memory primitive must beat *replay at equal bytes*, EWC, always-on mastery, and `L6W19` alone in a world where external guards decay at known rates, jointly measuring *retention of 20 skills after wake* and *capacity left for new tasks*. Every `L6W19` primitive must beat `L5W10` alone, `L5W03` alone, their independent union, `CAX4` handoff, Learning-to-Defer, and always-admit in a *strictly synthetic world with harmless failures and outside guard outages*.

---

## Section A · The World's Guards as Long-Term Memory (`L7W01`–`L7W16`, leaning hardest on `L6W25`)

### L7W01 · Three-tier Co-Evolutionary Memory Hierarchy (L1 Weights / L2 1-Step Trace / L3 Living World-Guard)
- **Mechanism:** Formalize continual-learning retention as a 3-tier memory architecture with explicit promotion/demotion transitions: **L1 Active Weights** (zero latency, maximum plasticity tax), **L2 1-Step Wakeable Trace** (`L5W03`, 1-step swap-in latency, tiny tangent-space tax), and **L3 Living External World-Guard** (zero internal weight tax, *volatile under disuse*). Demote stabilized skills from L1$\to$L2+L3 when external guards are verified healthy; promote L3$\to$L2$\to$L1 automatically when external guard readiness drops.
- **Nearest prior / gap:** [Miro](https://arxiv.org/abs/2308.06053) and [Complementary Learning Systems](https://arxiv.org/abs/2201.12604) tier *internal* memory (fast/slow weights or RAM/flash). Extending the memory hierarchy *across the agent–environment boundary* into living external guards is the foundational primitive of `L6W25`.
- **Cheapest first test:** 20-skill continual stream + 20 new tasks $C_1 \dots C_{20}$ with heterogeneous guard decay rates and 3 exogenous guard outages. Compare equal-byte replay (`FOREVER`/`Miro`), EWC, always-on mastery, `L6W19` alone, and 3-tier hierarchy `L7W01`. Kill if equal-byte replay or EWC matches 20-skill post-wake retention and task-20 plasticity.
- **Old-task retention:** Jointly verify 20-skill retention after forced guard outages and free capacity / learning speed on $C_1 \dots C_{20}$.

### L7W02 · DRAM-style refresh scheduling for volatile world-memory
- **Mechanism:** Unlike SSD or RAG storage, living external guards behave like **DRAM capacitors**: their readiness $g_t(F)$ leaks exponentially under disuse (`2610.12124`, `2609.38459`). Measure each external guard's empirical decay half-life $T_{1/2}(F)$ and schedule minimal-cost *safe refresh cycles* (transparent `CAX4` delegations or consented benign dry-run checks—zero real harm!) just before $T_{1/2}(F)$ elapses, sustaining L3 world-memory indefinitely at the information-theoretic minimum refresh bandwidth.
- **Nearest prior / gap:** [FOREVER](https://arxiv.org/abs/2601.03938) uses forgetting curves to schedule *internal* weight replay; `L7W02` uses forgetting curves to schedule *external world-guard refresh* so the environment never garbage-collects offloaded skills.
- **Cheapest first test:** 20-guard world with heterogeneous exponential decay half-lives $T_{1/2} \in [10, 200]$ steps under a fixed total refresh budget. Compare uniform refresh, no refresh (equal-byte internal replay instead), EWC, and half-life-scheduled `L7W02`. Kill if equal-byte internal replay or uniform refresh retains more of the 20 skills at equal total internal + refresh cost.
- **Old-task retention:** Verify all 20 L3 guards stay above readiness floor with minimal refresh bandwidth, leaving L1 weights free for $C_1 \dots C_{20}$.

### L7W03 · World-memory page faults & 1-step demand paging
- **Mechanism:** Treat an external guard's unexpected disappearance as a **hardware page fault**: during normal operation, 20 skills are "paged out" to L3 external guards (zero active weight tax), while L2 holds their 1-step wake pointers. The instant a page fault occurs (guard outage or miss), the learner executes a 1-step demand swap-in from L2$\to$L1—restoring $F$ inside weights on demand without stalling or erasing active tasks $C_1 \dots C_{20}$!
- **Nearest prior / gap:** Turns `L5W03` from a standalone regularizer into a *demand-paging swap mechanism* for an externalized continual-learning memory system.
- **Cheapest first test:** 20-skill world where 4 random external guards suffer sudden exogenous page faults during training of $C_{10}$ and $C_{18}$. Compare equal-byte replay, EWC, always-on mastery, `L6W19` alone, and demand-paging `L7W03`. Kill if equal-byte replay (requiring multi-step re-training on page fault) matches 1-step swap-in recovery and $C$-retention.
- **Old-task retention:** Verify 1-step swap-in restores all 4 faulted skills immediately while preserving $C_1 \dots C_{20}$ and the other 16 paged-out skills.

### L7W04 · Pointer-vs-payload split (storing complex evolving rules in the world, tiny wake pointers in weights)
- **Mechanism:** Why can `L6W25` beat equal-byte replay? Replay must store the full *data payload* of every old skill (high byte cost per skill). In `L7W04`, the external world guard holds the rich, high-entropy *operational payload* (complex multi-condition compliance rules, domain heuristics, human judgment), while L2 stores only a tiny *compressed wake pointer* (a low-rank gradient direction + 1-shot trigger key)—achieving strictly higher retention-per-internal-byte as skill complexity grows!
- **Nearest prior / gap:** Directly challenges [Drift and Dependence](https://arxiv.org/abs/2608.11690) and [Forget to Improve](https://arxiv.org/abs/2606.25115), which bound continual-learning capacity assuming the payload itself must live in internal bytes.
- **Cheapest first test:** Sweep skill complexity (decision-boundary description length from 10 bytes to 10 KB per skill across 20 skills) at a fixed internal byte budget. Compare equal-byte replay (`CAMR`/`FOREVER`), EWC, always-on mastery, and pointer-vs-payload `L7W04`. Kill if equal-byte replay matches `L7W04` even on high-description-length skills.
- **Old-task retention:** Verify retention advantage scales *positively* with skill description length while leaving L1 plasticity untouched.

### L7W05 · Cache coherence for mutating world-memory (syncing L2 wake pointers when L3 guards evolve)
- **Mechanism:** A replay buffer never changes on disk; *living external guards constantly evolve* (teams tighten policies, update linters, shift thresholds, `2611.26440`). If an L3 guard mutates while its L2 wake pointer stays frozen, a page fault swaps in a *stale, obsolete* version of $F$! Run an asynchronous *cache-coherence protocol*: periodically diff L3's live verdicts against L2's virtual 1-step wake boundary on benign probes; on mismatch, invalidate and refresh the L2 pointer—giving continual learners *up-to-date* external memory without re-training L1 weights!
- **Nearest prior / gap:** [Memory as Belief](https://arxiv.org/abs/2610.25119) updates internal belief memory; `L7W05` solves *coherence between an internal wake pointer and a living, independently mutating external guard*.
- **Cheapest first test:** 20-skill world where 6 external guards mutate their decision boundary mid-stream before 3 of them suffer an outage. Compare incoherent `L6W25`, equal-byte replay (frozen old examples!), EWC (frozen old weights!), and cache-coherent `L7W05`. Kill if incoherent `L6W25` or replay matches post-wake accuracy on the *mutated* rules.
- **Old-task retention:** Verify 1-step wake-up restores the *current* mutated rule (beating frozen replay and EWC by design!), with intact $C_1 \dots C_{20}$.

### L7W06 · World-memory garbage-collection protocol (distinguishing intentional rule retirement from accidental atrophy)
- **Mechanism:** When an external guard goes dark, there are two opposite causes: (i) **intentional garbage collection** (the organization deliberately deprecated an obsolete rule—so the learner should *free* its L2 pointer too!), vs. (ii) **accidental bit-rot / outage** (the rule is still needed—so the learner must immediately page L2$\to$L1!). Require a lightweight *tombstone vs. decay discriminator* (explicit deprecation metadata or counterfactual hazard probe) before paging in, preventing zombie skills from clogging L1/L2.
- **Nearest prior / gap:** Closes a major blind spot of `L6W25`: treating every disappeared guard as an outage turns external memory into a memory leak.
- **Cheapest first test:** 20-skill stream where 5 guards are intentionally deprecated (rules become obsolete) and 5 suffer accidental outages. Compare naive `L6W25` (wakes all 10), equal-byte replay, EWC, and GC-aware `L7W06`. Kill if naive `L6W25` retains equal new-task capacity without distinguishing deprecations from outages.
- **Old-task retention:** Verify all 5 accidental outages wake in 1 step, all 5 deprecated rules are cleanly freed, and $C_1 \dots C_{20}$ gain reclaimed capacity.

### L7W07 · Active stigmergic write-out (compiling learned skills *out* of weights into external guards)
- **Mechanism:** Push `L6W25` from *read-only* use of pre-existing guards to *read-write extended memory*: when the learner acquires a crisp, high-rank prevention rule $F$ that consumes precious L1 weight capacity, **compile $F$ out of weights into an external deterministic artifact** (a unit test, schema validator, regex/AST lint, or structured checklist deployed in the environment), verify it passes, and then *evict $F$ from L1 weights* down to a tiny L2 trace! The learner literally **writes its own long-term continual memory into the world**.
- **Nearest prior / gap:** Harness continual learning and [Grounding Agent Memory](https://arxiv.org/abs/2609.11060) create tools or prompt memories, but don't couple *external artifact compilation* to *deliberate internal weight eviction + 1-step L2 fallback* for plasticity reclamation.
- **Cheapest first test:** 20-skill stream where 12 skills are cleanly distillable into deterministic external guards and 8 are fuzzy/neural-only, under a tight parameter cap. Compare always-in-weights EWC, equal-byte replay, passive `L6W25` (no write-out), and stigmergic write-out `L7W07`. Kill if passive `L6W25` or equal-byte replay matches task-20 plasticity when skills start without pre-existing external guards.
- **Old-task retention:** Verify 100% retention on all 12 externalized skills + 8 neural skills, with dramatically freed L1 capacity for $C_1 \dots C_{20}$.

### L7W08 · RAID-1 external memory striping (fault-tolerant offloading across uncorrelated guards)
- **Mechanism:** Offloading a critical skill to a single external guard creates a single point of failure. Stripe high-criticality L3 memories across **two uncorrelated external media** (e.g., an automated CI/tool check *plus* an independent periodic human review) alongside the L2 wake trace: if one external guard suffers an exogenous outage, the second catches $F$ while L2 quietly swaps in—achieving zero-escape fault-tolerant external memory without locking L1 weights.
- **Nearest prior / gap:** Brings storage-system redundancy (RAID-1) to extended-mind continual learning, neutralizing correlated-outage criticism of `L6W25`.
- **Cheapest first test:** 20-skill world with independent per-guard outage probability $p = 0.1$ per epoch. Compare single-guard `L6W25`, equal-byte replay, always-on mastery, and RAID-1 striped `L7W08`. Kill if single-guard `L6W25` achieves equal zero-escape safety during outage detection lag.
- **Old-task retention:** Verify zero unguarded escapes even under stochastic guard outages, with zero L1 weight locking.

### L7W09 · World-aware metamemory placement (`AutoMem` over L1 Weights vs. L3 World vs. L4 Replay)
- **Mechanism:** Extend Stanford's [AutoMem](https://arxiv.org/abs/2607.01224) (learning *how* to manage internal memory) into a **co-evolutionary metamemory controller**: for every skill $F$, learn the optimal tier placement—L1 active weights, L2+L3 world-memory, or L4 cold replay—from four features: `(subspace rank cost, external guard half-life T_1/2, refresh cost, outage latency tolerance)`. Keep cheap-rank/fast-decay skills in L1, keep high-rank/long-half-life skills in L3 world-memory, and keep high-latency-tolerance skills in L4 cold replay.
- **Nearest prior / gap:** [AutoMem](https://arxiv.org/abs/2607.01224) and [Information-Theoretic Dual Memory](https://arxiv.org/abs/2501.07382) optimize purely internal placement; `L7W09` learns the optimal *internal-vs-external* memory split.
- **Cheapest first test:** Heterogeneous 20-skill world spanning wide ranges of rank, half-life $T_{1/2}$, and refresh cost. Compare all-L1 EWC, all-L4 equal-byte replay, all-L3 `L6W25`, and learned metamemory `L7W09`. Kill if any single-tier policy matches `L7W09` on joint 20-skill retention + task-20 plasticity + refresh cost.
- **Old-task retention:** Verify strictly dominant retention–plasticity–cost frontier across heterogeneous skills.

### L7W10 · Anti-bias refresh diversity (preventing human world-memory corruption)
- **Mechanism:** [Too Much of the Same](https://arxiv.org/abs/2608.28050) proves that routing narrow, repetitive examples to human experts *systematically biases* their judgment—meaning naive DRAM refresh pulses (`L7W02`) can *corrupt* human-backed L3 world-memory! Select safe refresh delegations via *boundary-covering diversity sampling* (maximizing coverage over $F$'s distinct sub-modes) so human external guards stay calibrated across the entire $F$ manifold rather than overfitting to one cliché trigger.
- **Nearest prior / gap:** Connects L2D human-bias findings (`2608.28050`) directly to the integrity of `L6W25`'s external memory tier.
- **Cheapest first test:** Human-guard simulator where repeated narrow triggers induce mode-blindness (guard loses recall on unseen sub-modes of $F$). Compare narrow-trigger `L7W02`, equal-byte replay, and diversity-refreshed `L7W10`. Kill if narrow-trigger refresh preserves full-manifold human guard recall equally well.
- **Old-task retention:** Verify uniform guard recall across all sub-modes of $F$ over 100 steps, with intact $C_1 \dots C_{20}$.

### L7W11 · Multi-agent shared world-memory refcounting (preventing Agent A from erasing Agent B's memory)
- **Mechanism:** In real organizations, multiple continual learners share the *same* external world guards. If Agent A decides to internalize skill $F$ into its weights and stops delegating, the shared external guard $G$ atrophies and dies—silently **erasing Agent B's L3 long-term memory**! Maintain a lightweight *shared-guard reference count / lease registry* across co-deployed agents: no agent may suppress refresh traffic to a shared guard $G$ while another agent holds an L3 memory lease on $G$.
- **Nearest prior / gap:** Exposes a multi-agent *memory-aliasing hazard* unique to environment-as-memory (`L6W25`) that never occurs in isolated replay buffers.
- **Cheapest first test:** 2-agent coupled world sharing 10 external guards where Agent A greedily internalizes 5 skills while Agent B relies on them as L3 memory. Compare uncoordinated `L6W25`, equal-byte replay, and refcounted `L7W11`. Kill if Agent B suffers zero memory loss without refcounting.
- **Old-task retention:** Verify zero cross-agent memory erasure, intact 10-skill coverage for both agents, and preserved plasticity.

### L7W12 · Environment-probing memory inventory (bootstrapping L3 pointers in a new workspace)
- **Mechanism:** When a continual learner is deployed into an unfamiliar codebase or enterprise workflow, it doesn't start with a map of existing external guards. Extend Microsoft's [Grounding Agent Memory](https://arxiv.org/abs/2609.11060) with a *safe passive inventory pass*: probe existing CI gates, schema validators, static analyzers, and review checklists to build an initial **L3 World-Memory Map** (which invariants the environment already enforces!), immediately preventing the learner from wasting L1 weights re-memorizing rules the world already holds.
- **Nearest prior / gap:** `2609.11060` probes the environment to populate an *internal* memory store; `L7W12` probes the environment to *avoid* duplicating knowledge that already lives in L3 external guards.
- **Cheapest first test:** Cold-start deployment in a 20-rule environment where 12 rules are already enforced by existing external validators (unknown to the learner initially). Compare blind always-learn EWC, equal-byte replay, and inventory-bootstrapped `L7W12`. Kill if blind always-learn achieves equal plasticity on the 8 *unguarded* rules + $C_1 \dots C_{15}$.
- **Old-task retention:** Verify zero wasted weight capacity on the 12 pre-guarded rules, 100% L1 focus on the 8 unguarded rules + new tasks.

### L7W13 · Engram-factored wake dictionary (packing 50+ L2 wake pointers into 1-task tangent budget)
- **Mechanism:** The scaling bottleneck of `L6W25` is L2: keeping $K=50$ independent 1-step wake traces (`L5W03`) eventually crowds the tangent space (`L6W18`). Inspired by [Engram Neuron Adaptive Memorization](https://arxiv.org/abs/2610.14940), factor the $K$ wake directions into a *shared low-rank wake dictionary* $D \in \mathbb{R}^{d \times r}$ ($r \ll K$) plus sparse per-skill index coefficients $c_F$, testing whether 50 world-offloaded skills can stay 1-step wakeable at the plasticity and byte cost of a single task!
- **Nearest prior / gap:** Solves the `L6W18` tangent-space saturation wall so `L6W25` scales far beyond $K=20$ skills without crushing L1 plasticity.
- **Cheapest first test:** Sweep $K \in \{10, 20, 50\}$ offloaded skills on a fixed-width MLP at equal internal bytes. Compare unfactored `L6W25`, equal-byte replay (`FOREVER`), EWC, and engram-factored `L7W13`. Kill if unfactored `L6W25` or equal-byte replay matches 50-skill 1-step wake accuracy and task-20 plasticity.
- **Old-task retention:** Verify 50-skill 1-step wake recovery remains $\ge 95\%$ while L1 new-task speed stays flat vs. $K$.

### L7W14 · SLA-tiered wake latency (L2 hot 1-step vs. L4 cold multi-step external memory)
- **Mechanism:** Not every externalized skill needs a 1-step wake trace in L2! Partition L3 world-memories by *outage SLA*: skills whose external guard outage causes immediate risk get a hot **L2 1-step trace**; skills with a relaxed SLA (e.g., async nightly batch audits) get **zero L2 tangent-space footprint**, falling back to a tiny L4 cold synthetic sketch (multi-step recovery on outage). This multiplies effective L3 capacity without paying L2 overhead on slow-SLA skills.
- **Nearest prior / gap:** Sharpens `L6W25` by recognizing that L2 wake traces are a scarce resource that should only back *real-time* external guards.
- **Cheapest first test:** 30-skill world (10 real-time SLA, 20 relaxed async SLA) under a tight L2 tangent budget. Compare all-L2 `L6W25`, equal-byte replay, EWC, and SLA-tiered `L7W14`. Kill if all-L2 `L6W25` matches $C$-plasticity without SLA tiering.
- **Old-task retention:** Verify 1-step wake on all 10 real-time outages, within-SLA recovery on async outages, and strictly higher $C$-plasticity.

### L7W15 · Equal-bytes phase-boundary audit (World-Memory vs. Replay across decay rate $\lambda$ & skill count $K$)
- **Mechanism:** Construct the exact empirical phase diagram separating where `L6W25` beats internal replay from where replay wins: sweep `(guard decay rate λ, skill count K, skill description length B)` at **strictly equal total internal bytes** (comparing L2 pointers + refresh metadata against `FOREVER`/`CAMR`/`Miro` replay buffers). Explicitly report the break-even curve $\lambda^*(K, B)$ where world-memory ceases to dominate!
- **Nearest prior / gap:** Directly operationalizes row 510's core scientific gate ("replay at equal bytes, a world where guards decay at known rates, retention of 20 skills after wake and capacity left for new tasks").
- **Cheapest first test:** Grid sweep $K \in \{5, 10, 20, 40\} \times \lambda \in \{0.001, 0.01, 0.05, 0.2\}$ on a fixed-byte MLP benchmark. Kill `L6W25` outright if equal-byte replay dominates across all realistic $(\lambda, K)$ cells.
- **Old-task retention:** Jointly plot 20-skill post-wake retention, new-task learning speed, and total refresh bandwidth across the grid.

### L7W16 · Safe CAX4 delegation as the production refresh mechanism (zero-harm world-memory)
- **Mechanism:** Directly resolves the reviewer's safety flag: in real deployments, *never* leave harmful failures un-prevented to keep L3 guards alive! Maintain L3 world-memory exclusively via **transparent, consented `CAX4` delegation** (explicitly handing off pre-agreed, bounded decision slices or benign verification checkpoints to external guards/experts with full visibility and capacity checks, cf. [Intelligent AI Delegation](https://arxiv.org/abs/2602.11865)), keeping external memory warm at **zero manufactured harm**.
- **Nearest prior / gap:** Decouples `L6W25` (world-as-long-term-memory) cleanly from unsafe competence caps, proving environment-as-memory is safe for real production systems.
- **Cheapest first test:** Coupled world with capacity-limited human/tool guards and real harm costs. Compare unsafe `L5W10` capping, standard Learning-to-Defer (which does not refresh dormant guards), equal-byte replay, and transparent-delegation world-memory `L7W16`. Kill if standard Learning-to-Defer keeps all 20 guards alive equally well without scheduled refresh delegation.
- **Old-task retention:** Verify zero manufactured harm, 20-skill L3 guard survival + 1-step L2 wake readiness, and high $C_1 \dots C_{20}$ plasticity.

---

## Section B · Safe, Outage-Proof Dual-Layer Guarding (`L7W17`–`L7W20`, refining `L6W19` under the safety boundary)

### L7W17 · Synthetic harmless-world ablation: competence cap + 1-step wake vs. transparent `CAX4` delegation
- **Mechanism:** Isolate `L6W19`'s exact scientific hypothesis in a **strictly synthetic world with harmless failures** (e.g., harmless formatting/style rules where a miss costs 1 minor edit, never real harm): test whether holding expressed prevention just below $p_{\text{crit}}$ + 1-step L2 wake strictly beats transparent `CAX4` delegation and Learning-to-Defer when the external guard has a sharp removal cliff and random exogenous outages.
- **Nearest prior / gap:** Directly answers row 510's gating question ("ranked question 1 must beat learning to defer before `L6W19` runs") while strictly respecting the synthetic-harmless-worlds safety boundary.
- **Cheapest first test:** Synthetic harmless-lint world with sharp guard cliff ($p_{\text{crit}} = 0.95$) and 2 exogenous outages over 100 steps. Compare `L5W10` alone, `L5W03` alone, independent `L5W10 + L5W03`, `CAX4` transparent handoff, Learning-to-Defer, always-admit, and `L6W19`. Kill `L6W19` permanently if `CAX4` handoff or Learning-to-Defer matches it on cumulative cost, guard survival, and post-outage wake recovery.
- **Old-task retention:** Jointly measure synthetic cost, guard survival, 1-step $F$-recovery on outage, and $C$-plasticity.

### L7W18 · Zero-harm detected-trigger delegation + 1-step autonomous failover (safe replacement for `L6W19`)
- **Mechanism:** Can we get 100% of `L6W19`'s benefit with **zero un-prevented failures**? Instead of letting $(1 - p_F^*)$ failures slip through uncaught, *detect* 100% of $F$-triggers, transparently delegate fraction $(1 - p_F^*)$ of *flagged* cases to the external guard *before* execution (`CAX4` pre-execution gate), and keep full 1-step autonomous execution in L2 (`L5W03`) so an exogenous guard outage flips instantaneously from "flag-and-delegate" to "handle autonomously"—zero leaked failures, alive external guard, instant outage immunity!
- **Nearest prior / gap:** Transforms `L6W19` from a synthetic-only curiosity into a **production-safe dual-layer primitive** that never leaves a failure un-prevented.
- **Cheapest first test:** World with real failure harm and exogenous guard outages. Compare unsafe `L6W19` (synthetic baseline), standard L2D, `CAX4` without L2 failover, always-admit, and detected-delegation + 1-step failover `L7W18`. Kill if standard L2D or `CAX4` without L2 recovers equally fast when the external guard crashes.
- **Old-task retention:** Verify zero leaked failures in both normal and outage phases, alive guard, and intact $C$ + $A/B$.

### L7W19 · Passive SLA-timeout outage sensor (sub-step trigger for L2 wake-up)
- **Mechanism:** Both `L6W19` and `L6W25` assume the learner *knows immediately* when an external guard dies for an outside reason. In practice, silent tool failures or unresponsive review queues can lag for hours! Attach a zero-overhead *passive SLA-timeout / response-distribution sensor* to every L3 delegation channel: the first missed heartbeat or abnormal timeout immediately fires the 1-step L2 wake-up *before* a single unguarded failure escapes.
- **Nearest prior / gap:** Closes the detection-latency gap between exogenous guard loss and 1-step L2 activation.
- **Cheapest first test:** Outage simulator with silent guard crashes (no explicit crash notification). Compare reactive-after-incident `L6W19`, fixed polling, and passive SLA-timeout `L7W19`. Kill if reactive-after-incident `L6W19` suffers equal zero-escape harm.
- **Old-task retention:** Verify zero false-alarm wake-ups during normal jitter, 1-step pre-escape wake on silent crash, and intact $C$ + $A/B$.

### L7W20 · Hysteretic re-offload handshake after exogenous outages
- **Mechanism:** After `L6W19`/`L7W18` wakes L2$\to$L1 during an exogenous guard outage, handing control back to the external guard on the first flickering recovery signal causes repeated page-fault thrashing. Require a *verified 2-check restoration handshake* before demoting L1 back to L2+L3, keeping the learner safely in charge through noisy infrastructure recoveries.
- **Nearest prior / gap:** Prevents L1$\leftrightarrow$L3 thrashing during real-world flapping outages (`2610.34748`).
- **Cheapest first test:** Flapping-outage simulator (guard recovers briefly for 2 steps then crashes again for 20 steps). Compare instant-demote `L6W19`, permanent-pin (never demotes), and hysteretic-handshake `L7W20`. Kill if instant-demote `L6W19` avoids thrashing and $C$-disruption equally well.
- **Old-task retention:** Verify zero unguarded escapes during flapping recovery and full plasticity restoration once the guard truly stabilizes.

---

## Section C · Joint `L6W25 × L6W19` Primitives: Co-Evolutionary Memory Operating System (`L7W21`–`L7W26`)

### L7W21 · Guard-decay pre-emptive paging (swap-in *before* the external guard dies)
- **Mechanism:** Combine `L6W25` (world-memory) with `L6W19` (1-step wake): instead of waiting for a hard page fault ($g_t = 0$), track each external guard's continuous readiness $g_t(F)$. When $g_t(F)$ crosses a warning watermark ($g_t < 0.5$) and refresh fails to revive it, *pre-emptively page* L2$\to$L1 in advance—eliminating even the 1-step outage exposure window!
- **Nearest prior / gap:** Analogous to predictive OS page pre-fetching, applied to decaying external world-memory.
- **Cheapest first test:** Gradual-decay + sudden-drop mixed outage world across 20 skills. Compare reactive page-fault `L7W03`, `L6W19` alone, equal-byte replay, and pre-emptive paging `L7W21`. Kill if reactive `L7W03` achieves equal zero-escape safety on gradually dying guards.
- **Old-task retention:** Verify zero unguarded escapes during gradual guard death, zero premature paging on healthy guards, and intact $C_1 \dots C_{20}$.

### L7W22 · Mass-outage L1 swap-slot triage (budgeted demand paging under correlated shocks)
- **Mechanism:** Suppose a broad organizational outage takes down 8 L3 external guards simultaneously, while L1 weights only have spare interference-free capacity to absorb 3 skills in 1 step without crushing active task $C$. Rank the 8 simultaneous page faults by `Criticality(F) × Wake_Fidelity(F) / C_Interference(F)`: swap the top 3 into L1 via L2 1-step wake, put the next 3 into transparent pre-execution abstention (`CAX4`), and queue the remaining 2 until guards recover.
- **Nearest prior / gap:** Solves the correlated-failure mode of world-as-memory (`L6W25`) when multiple external memory banks fail together.
- **Cheapest first test:** 20-skill world hit by a correlated 8-guard outage during training of high-value task $C_{15}$. Compare wake-all `L6W25`, equal-byte replay, EWC, and swap-triaged `L7W22`. Kill if wake-all `L6W25` preserves $C_{15}$ equally well during an 8-guard shock.
- **Old-task retention:** Verify $C_{15}$ stays above floor, top-criticality skills wake in 1 step, abstention prevents silent harm on the rest, and $A/B$ hold.

### L7W23 · World-memory break-even law (thermodynamic accounting of internal plasticity vs. external refresh)
- **Mechanism:** Formalize the exact net benefit of offloading skill $F$ to L3 world-memory:
  $$\Delta U_{\text{world}}(F) = \underbrace{\text{PlasticitySaved}(V_F) + \text{BytesSaved}(F)}_{\text{internal gain}} - \underbrace{\Big(\frac{c_{\text{refresh}}(F)}{T_{1/2}(F)} + c_{\text{L2}}(F) + \lambda_{\text{outage}}(F)\,c_{\text{wake}}(F)\Big)}_{\text{external maintenance + wake cost}}.$$
  Use $\Delta U_{\text{world}}(F) > 0$ as a principled, domain-independent rule deciding which skills belong in world-memory vs. equal-byte replay vs. L1 weights!
- **Nearest prior / gap:** Turns `L6W25` from a metaphor into a *falsifiable quantitative capacity law* directly comparable to information-theoretic replay bounds (`2608.11690`).
- **Cheapest first test:** Synthetic 20-skill world sweeping $T_{1/2}$, $c_{\text{refresh}}$, and $\lambda_{\text{outage}}$ to test whether $\Delta U_{\text{world}}(F) > 0$ accurately predicts when `L6W25` beats equal-byte replay (`FOREVER`/`Miro`). Kill if the analytical break-even sign fails to predict empirical winners across $>80\%$ of regimes.
- **Old-task retention:** Verify the law selects the highest-utility memory tier per skill, beating uniform replay and uniform world-memory.

### L7W24 · Zero-migration-cost model upgrades via persistent L3 world-memory
- **Mechanism:** A radical payoff of `L6W25`: when you upgrade the learner from base model $\theta_{\text{old}}$ to a completely new architecture $\theta_{\text{new}}$ (e.g. a new model family or full weight reset), EWC Fishers, adapters, and weight consolidation are **100% wiped out**—yet **L3 external world-guards persist untouched in the environment!** $\theta_{\text{new}}$ automatically inherits all 20 world-offloaded skills on day 1, needing only a cheap L2 pointer alignment pass (no full 20-skill re-training!).
- **Nearest prior / gap:** Connects this learner–world co-evolution branch back to the repo's earlier model-upgrade line—showing that *externalized world-memory is natively architecture-invariant across model generations!*
- **Cheapest first test:** 20-skill continual stream with a full architecture swap (MLP $\to$ wider ResNet/Transformer) at step $t=50$. Compare EWC (wiped!), replay-retrain (high re-training compute!), and world-memory inheritance `L7W24` (instant L3 continuity + fast L2 pointer init). Kill if equal-compute replay re-training matches day-1 post-upgrade safety and new-task speed.
- **Old-task retention:** Verify 100% day-1 retention of all 20 skills across a full model swap, with immediate forward plasticity on $C_{11} \dots C_{20}$.

### L7W25 · Immutable invariant checksums against adversarial world-memory poisoning
- **Mechanism:** Storing long-term memory in external world-guards (`L6W25`) introduces a unique security threat: if an adversary or buggy deploy silently corrupts an external guard, cache-coherence sync (`L7W05`) would *overwrite* L2 with a poisoned wake pointer! Protect every L3$\to$L2 sync with a tiny, immutable *core-invariant checksum* (a few hard-coded or cryptographically signed red-line test cases): accept benign policy updates from L3, but quarantine any L3 drift that violates core red-line invariants.
- **Nearest prior / gap:** Hardens extended-mind continual learning against external memory poisoning without reverting to static frozen weights.
- **Cheapest first test:** 20-skill world where 3 external guards undergo benign policy evolution and 2 undergo adversarial corruption mid-stream. Compare unguarded `L7W05`, frozen replay, and checksum-guarded `L7W25`. Kill if unguarded `L7W05` avoids internalizing the 2 poisoned rules equally well.
- **Old-task retention:** Verify the 3 benign guard evolutions sync cleanly while both adversarial corruptions are rejected and safely handled.

### L7W26 · 20-Skill Co-Evolutionary Memory Hierarchy Benchmark (World-Memory vs. Equal-Bytes Replay)
- **Mechanism:** A compact, CPU-runnable benchmark strictly in a **synthetic harmless domain** testing 20 operational skills + 20 forward tasks $C_1 \dots C_{20}$ with: (i) known guard decay half-lives $T_{1/2}$, (ii) exogenous guard outages, (iii) mid-stream guard policy mutations, and (iv) a mid-stream base-model architecture swap. Directly pits `L7W01` + `L7W02` + `L7W05` + `L7W13` + `L7W16` against equal-byte replay (`FOREVER`/`CAMR`/`Miro`), EWC, always-on mastery, Learning-to-Defer, `CAX4`, and `L6W19` alone.
- **Nearest prior / gap:** Directly operationalizes every control and metric required by row 510 in one clean falsification suite.
- **Cheapest first test:** Run the full control ladder on a fixed-byte MLP benchmark over 20 skills and 20 forward tasks. Kill the `L6W25` world-memory line if equal-byte replay matches 20-skill post-wake retention, mutated-rule accuracy, and task-20 plasticity across all decay regimes.
- **Old-task retention:** Jointly measure 20-skill post-wake retention, task-20 learning speed, mutated-rule fidelity, refresh cost, and post-swap day-1 retention.

---

## Ranked deeper questions

1. **Does World-as-Long-Term-Memory (`L6W25` via `L7W01` + `L7W02` + `L7W13` + `L7W16`) strictly beat replay at equal bytes (`FOREVER`/`CAMR`/`Miro`), EWC, and always-on mastery on 20-skill post-wake retention AND remaining new-task plasticity?**
   *Cheapest falsification:* Run the equal-bytes phase-boundary grid (`L7W15`: $K \in \{5, 10, 20, 40\} \times$ decay rate $\lambda$) on a CPU MLP benchmark. If equal-byte replay matches or beats `L6W25` on both 20-skill post-wake retention and task-20 plasticity across realistic decay rates, the environment-as-memory line closes.

2. **Can zero-harm detected-trigger delegation + 1-step autonomous failover (`L7W18` / `L7W16` / `CAX4`) match or beat `L6W19`'s competence cap in synthetic harmless worlds—eliminating any need to ever leave failures un-prevented?**
   *Cheapest falsification:* Run the synthetic harmless-lint cliff-plus-outage benchmark (`L7W17` vs. `L7W18` vs. Learning-to-Defer vs. `CAX4` without L2). If `L7W18` (zero leaked failures) matches `L6W19` on guard survival, plasticity, and outage recovery, unsafe competence caps can be permanently retired in favor of safe delegation + 1-step failover.

3. **When external world-memory *mutates* over time (policy updates / schema drift), does cache-coherent world-memory (`L7W05`) + active stigmergic write-out (`L7W07`) beat frozen internal replay and EWC by design?**
   *Cheapest falsification:* Run the 20-skill mutating-guard stream (`L7W05`, 6 mutated guards + 3 outages). Measure post-wake accuracy on the *current* world rules; this tests whether living external memory provides a qualitative advantage (tracking world evolution automatically) that no static internal replay buffer can match.

4. **Does persistent L3 world-memory (`L7W24`) provide a strict zero-migration-cost retention advantage across full base-model architecture swaps?**
   *Cheapest falsification:* Swap the model architecture at step $t=50$ in the 20-skill stream (`L7W24`), comparing day-1 retention and re-training compute against EWC and equal-byte replay. If replay re-training matches day-1 safety and new-task speed at comparable compute, the cross-generation world-memory advantage closes.
