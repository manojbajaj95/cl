# Glued reply fragments: compose incompatible specialists and park shared coordinates without observation

**Status:** Ideas only; no experiments, code, or GPU work. **Parent:** [Covering replies](covering-replies.md) ([PR #211](https://github.com/manojbajaj95/cl/pull/211)), cards 02 and 08. **Review seeds:** The [PR #211 flood-triage row](https://github.com/manojbajaj95/cl/blob/0a3fc72668fc1f4cd6fd73dc5cb8886514765787/reviews/flood-triage.md#L322) gives both cards score 3: (1) extract entry, intermediate, and exit obligations from fragments of incompatible specialist replies, unify their holes, and synthesize one observation-free ordering whose cross-fragment guarantees cover every hidden history; (2) park a shared coordinate in a neutral state safe for every history, apply the useful change, then clear the park, without reading which history held it. **Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/f3dbc1cf3d7dc26e99fc657d0f2d19079e521dd6/reviews/idea-ledger.md).

## What would make this a continual-learning primitive?

The parent expands the action set with a monolithic covering reply `r* ∈ L` instead of buying a splitting observation. This node asks whether a blind editor can build that covering reply **compositionally** out of two finer mechanisms: **fragment gluing** (harvesting sub-steps from mutually incompatible specialist replies and unifying their entry/middle/exit obligations into one observation-free sequence) and **universal parking** (moving a shared coordinate into one history-independent intermediate state that decouples the edit while keeping live service above floor, then clearing the park).

For a frozen public transcript, let `H` be all compatible, reachable hidden histories, `S = {S₁, …, S_m}` a set of specialist replies where each `Sᵢ` covers some proper subset of `H` but none covers all of `H`, and `L` the lawful fragment and state-transition language. Every intermediate tick `t = 0, …, T` of an executed sequence must satisfy hard ordinary-A and disjoint rare-C retention floors for **every** `h ∈ H`, and the commit state `t = T` must meet the B utility target over the declared continuation scope.

Two discipline rules bind every card below:
1. **No covert history dispatch.** Neither a glued sequence nor a park-and-clear script may branch on hidden state, clip conditionally on a history-varying statistic, or pass hidden history across a seam between fragments.
2. **A universal park is not a save/restore stack.** Saving a history-specific pre-park value in an auxiliary buffer and restoring it on clear is exact save/restore (killed in the [Idea ledger](https://github.com/manojbajaj95/cl/blob/f3dbc1cf3d7dc26e99fc657d0f2d19079e521dd6/reviews/idea-ledger.md) under return-point adapters), not a CL primitive. Both the park value `s_park` and the clear target `s_clear` must be determined purely by public state and the B target, and live service/capacity must be certified **at the park state itself**, not only at commit.

**Prior-art floor.** [Pacti][pacti] already composes assume–guarantee contracts; [conformant planning][conformant] already searches observation-free action sequences across belief states; [SyGuS][sygus] and [CEG repair][repair] synthesize programs against specifications; [shared replies (PR #173)][shared], [teaching bundles (PR #179)][teaching], and [monolithic covering replies (#200#08)][group] construct whole replies without splitting. For parking, [make-before-break (PR #157)][make], [Net2Net][net2net], transactional updates, [escrowed handshakes (PR #199, card 2)][handshake], [barrier certificates][barrier], and [optimizer resets][optreset] already protect transitions or decouple state. The candidate primitive is not generic contract composition, conformant planning, or extra-width blue-green staging. It is (a) **extracting history-free, hole-unifiable fragments from incompatible whole specialists after deletion** to cover a group that no specialist and no cheap monolith covers, and (b) **using a fixed-width, history-independent live maintenance state** on an active shared coordinate to make an otherwise un-orderable blind edit admissible. Anything that only speeds up search or ties the best stacked baseline is an improvement (`I`), not a conditional primitive (`P`).

**Common test rules.** Freeze legal reads, fragment language `L`, width/capacity bounds, A/C floors (including rare slices), B target, continuation horizon, and tariffs before running. Check ordinary A and disjoint rare C independently of the construction's witnesses at **every intermediate tick**, at commit, and after a held-out continuation. Compare fragment gluing against whole-specialist selection, #200#08 monolithic reply synthesis, Pacti contract composition, exact conformant planning, query-to-split (#190#09), and their strongest lawful stack. Compare universal parking against #157 make-before-break (charging spare width), per-history migration (charging split bits), transactional lock/stall (charging stall regret), #199#2 escrowed handshakes, and global optimizer resets. Charge fragment extraction, unification, proof checking, rejected candidates, park-state service loss, and fallback equally. Include both an **un-unifiable fragment negative** and a **no-safe-park negative**. Remember the ledger's kills: output matching at commit does not certify update/slot retention (effect-class distillation), and a geometry score is not a plasticity reserve. All tests below are proposals.

### Paper fixture 1: gluing fragments of incompatible specialists by trading slack

Consider a 4-coordinate live host `(x₁, x₂, x₃, x₄)` starting at `(1, 1, 1, 0)` with hard per-tick capacity `x₁ + x₂ + x₃ + x₄ ≤ 3`. Ordinary A is unchanged; new task B requires `x₄ = 1` at commit. Three compatible hidden histories `h₁, h₂, h₃` share this public state, with protected rare slices requiring at **every tick**:
- `h₁`: `x₁ + x₄ ≥ 1/2`
- `h₂`: `x₂ + x₄ ≥ 1/2`
- `h₃`: `x₃ + x₄ ≥ 1/2`

The incumbent specialist menu is `Sᵢ = [drop(xᵢ, 1); raise(x₄, 1)]` for `i ∈ {1, 2, 3}`. Each specialist covers two histories (`S₁` passes `{h₂, h₃}` but violates `h₁` at tick 1 with `x₁ + x₄ = 0 < 1/2`), so `{h₁, h₂, h₃}` is a 3-obstruction with no covering specialist. Now decompose specialists into parameterized fragments `drop(xᵢ, α)` (entry: `xᵢ + x₄ − α ≥ 1/2` for active `hᵢ`; exit: `free_cap ≥ α`) and `raise(x₄, β)` (entry: `free_cap ≥ β`; exit: raises every `xᵢ + x₄` by `+β`). Unifying `α = β = 1/2` and gluing fragments from `S₁` and `S₂` yields:
1. `drop(x₁, 1/2)` → `(1/2, 1, 1, 0)` (sum `5/2 ≤ 3`; `x₁+x₄ = 1/2`, `x₂+x₄ = 1`, `x₃+x₄ = 1`).
2. `raise(x₄, 1/2)` → `(1/2, 1, 1, 1/2)` (sum `3 ≤ 3`; all `xᵢ+x₄ ≥ 1`).
3. `drop(x₂, 1/2)` → `(1/2, 1/2, 1, 1/2)` (sum `5/2 ≤ 3`; all `xᵢ+x₄ ≥ 1`).
4. `raise(x₄, 1/2)` → `(1/2, 1/2, 1, 1)` (sum `3 ≤ 3`; all `xᵢ+x₄ ≥ 3/2`, `x₄ = 1` meets B).

One observation-free glued sequence covers all three histories at every tick (and also covers a fourth history requiring `x₁ ≥ 1/2`, which `[drop(x₁, 1/2); raise(x₄, 1/2); drop(x₁, 1/2); raise(x₄, 1/2)]` would violate). **Negative control:** raise the floor from `1/2` to `1` (zero initial slack); no `α > 0` is admissible at tick 1 and `free_cap = 0` blocks `raise`, so the fragment obligations cannot unify.

### Paper fixture 2: a universally safe park without reading history or saving state

Consider a fixed-width live host `(s, w, u)` starting at `(1, 0, 0)`, where `s ∈ [0, 1]` is an active shared coupling gate, `w ∈ [0, 1]` is the edited weight, and `u ∈ [0, 1]` is a compensatory offset. The lawful language allows one single-coordinate atomic update per tick. New task B requires `(s, w, u) = (1, 1, 1)` at commit. At **every served tick**:
- Ordinary A requires `1/2 + (1/2)·s ≥ 1/2` (holds for all `s ∈ [0, 1]`, with zero surplus at `s = 0`).
- Hidden history `h₁` has protected `C₁` requiring `1 − 2·s·(w − u) ≥ 0`.
- Hidden history `h₂` has protected `C₂` requiring `1 + 2·s·(w − u) ≥ 0`.

At `s = 1`, neither direct move is safe: `w ← 1` gives `(1, 1, 0)`, failing `C₁` (`1 − 2 = −1 < 0`); `u ← 1` gives `(1, 0, 1)`, failing `C₂` (`1 − 2 = −1 < 0`). No direct ordering of `{w, u}` covers `{h₁, h₂}`. Now apply the history-blind park–edit–clear triad:
1. **Park:** `s ← 0` → `(0, 0, 0)` (`A = 1/2 ≥ 1/2`, `C₁ = 1`, `C₂ = 1`).
2. **Edit 1:** `w ← 1` → `(0, 1, 0)` (`A = 1/2`, `C₁ = 1`, `C₂ = 1`).
3. **Edit 2:** `u ← 1` → `(0, 1, 1)` (`A = 1/2`, `C₁ = 1`, `C₂ = 1`).
4. **Clear park:** `s ← 1` → `(1, 1, 1)` (`A = 1`, `C₁ = 1`, `C₂ = 1`, B met).

No history is read, no backup buffer is allocated, and service clears all floors at every tick including the park. **Negative control:** tighten A's hard floor to `7/8` (forcing `s ≥ 3/4` at every tick). At `s = 3/4`, `w ← 1` gives `C₁ = 1 − 3/2 = −1/2 < 0` and `u ← 1` gives `C₂ = −1/2 < 0`; no universally safe park exists.

## Idea cards

### Glue fragments of incompatible specialist replies without hidden-state dispatch

#### 01. Compile incompatible specialists into a typed fragment library with entry/middle/exit obligations (P; parent 02)
- **Mechanism:** Before deleting histories, slice each rejected specialist reply into atomic fragments, exporting for each fragment a history-free triple of checked predicates: entry precondition, per-tick intermediate invariant, and exit postcondition over public coordinates and parameter holes. After deletion, unify holes across fragments drawn from *different* specialists and synthesize one observation-free sequence discharging every history in `H`.
- **Novelty vs nearest prior art:** [Pacti][pacti] composes pre-authored assume–guarantee contracts; [SyGuS][sygus] and [#200#08][group] synthesize monolithic replies. The candidate primitive is harvesting composable, deletion-safe fragments *out of mutually incompatible whole specialists* so a cell with no surviving specialist is still covered without observation.
- **Cheapest first test:** Fixture 1 plus the fourth `x₁ ≥ 1/2` history and the zero-slack (`floor = 1`) negative; compare whole-specialist choice, #200#08 monolithic synthesis, Pacti composition, exact conformant planning, and query-to-split at matched total work.
- **Old-task retention check:** Evaluate independent A and every `Cᵢ` at each intermediate tick and after a held-out continuation; reject any glued sequence verified only at commit.

#### 02. Interleave parameterized fragments to trade transient slack across specialists (P)
- **Mechanism:** Rather than concatenating complete specialist phases, interleave parameterized fragments `(f₁(α), g(β), f₂(α), g(β))` so an early partial step from specialist 1 frees just enough capacity for a shared fragment `g` to raise the margin that specialist 2's fragment needs, alternating until B is met.
- **Novelty vs nearest prior art:** [Conformant planning][conformant] searches unparameterized action graphs; [safe-order families (PR #195)][orders] certify permutations of fixed batches. Here hole unification creates a *new interleaved micro-schedule* out of incompatible specialists that no fixed-granularity permutation can form.
- **Cheapest first test:** Fixture 1 under tight capacity (`sum ≤ 3`) where no 2-step concatenation of fragments works, plus the `floor = 1` impossible control; compare against fixed-granularity fragment concatenation, monolithic synthesis, and conformant planning.
- **Old-task retention check:** Check A and all `Cᵢ` after every micro-step and under an unexpected continuation injected mid-interleaving; any single-tick dip below floor fails the arm.

#### 03. Unify fragment holes with relational seam invariants instead of concrete constants (P)
- **Mechanism:** Keep fragment step-size holes `(α, β)` symbolic and link them across seams by a checked relational invariant (e.g., `α ≤ β + slack_min`), exporting one glued skeleton that instantiates to held-out B target magnitudes without re-extracting fragments or re-checking deleted histories.
- **Novelty vs nearest prior art:** #211#06 keeps an inner reply envelope for one monolithic template, and Pacti checks fixed interfaces. A *cross-fragment seam relation* carries reusable parameterization across incompatible specialists' sub-steps.
- **Cheapest first test:** Fixture 1 across a held-out sweep of B targets `x₄ ∈ [0.6, 1.0]` and initial slacks; compare the relational skeleton against per-target re-synthesis, equal-byte cached concrete sequences, and static Pacti contracts.
- **Old-task retention check:** Test extremal and interior `(α, β)` instantiations on A and a rare C slice sensitive to `α − β`; include an out-of-range B target that must be refused.

#### 04. Emit a minimal un-unifiable seam core when fragment gluing fails (P)
- **Mechanism:** When no hole assignment or ordering glues the fragment library across `H`, return a minimal *seam obstruction*: the smallest subset of histories and fragment interfaces whose entry/middle/exit obligations contradict, distinguishing "slice finer" from "insert a park" from "buy a split" from "impossible in `L`".
- **Novelty vs nearest prior art:** [SyGuS unrealizability][unreal] and #211#03 refute a whole template at once. A seam core localizes *which interface mismatch* blocks composition, directly routing the editor to the cheapest structural remedy.
- **Cheapest first test:** Fixture 1 across three regimes: 2-cycle unifiable (`floor = 1/2`), 3-cycle sliceable (`floor = 3/4`), and impossible (`floor = 1`); compare seam-guided routing against generic UNSAT cores, #211#03 whole-template refutation, and query-first splitting.
- **Old-task retention check:** Check A and every `Cᵢ` along whichever remedy the seam core triggers (finer slice, park, or split), and plant a stale seam core after `L` expands to verify expiry.

#### 05. Certify obligation-modulo commutation between incompatible specialist fragments (P)
- **Mechanism:** Prove that two fragments `f_A, f_B` from incompatible specialists commute *modulo all protected A/C predicates across `H`* (even when they do not commute on raw weights), allowing a blind composer to reorder them to satisfy a downstream fragment's entry condition.
- **Novelty vs nearest prior art:** Partial-order reduction and #195#13 swap classes certify safe orderings of fixed updates. Certifying commutation *only up to retention-obligation equivalence* unlocks reorderings that raw-state commutation forbids.
- **Cheapest first test:** A 3-coordinate toy where `f_A; f_B` and `f_B; f_A` differ on an unprotected coordinate but agree on A/C, and only one order enables a shared B fragment; compare against raw-weight commutation, #195 swap classes, and exhaustive conformant planning.
- **Old-task retention check:** Plant a rare C slice that actually reads the supposedly unprotected coordinate and verify the commutation certifier rejects the swap.

#### 06. Glue weight-edit and optimizer-slot fragments across incompatible specialists (P)
- **Mechanism:** Decompose specialists that touch both weights `w` and optimizer slots `(m, v)` into separate weight and slot fragments, then glue a slot-conditioning fragment from specialist 2 ahead of a weight fragment from specialist 1 so the composed step lands safely for every hidden slot history.
- **Novelty vs nearest prior art:** [Slot splices (PR #185)][splice] transplant slots and [protective orders (PR #207)][protective] reorder batches; neither harvests and glues mixed weight/slot sub-steps from incompatible full replies.
- **Cheapest first test:** A 2-step momentum host where specialist 1's weight step is safe across hidden histories only after specialist 2's momentum-damping fragment; compare against monolithic joint synthesis, [full slot reset][optreset], #185 splices, and a slot-free SGD negative.
- **Old-task retention check:** Check A and rare C both at commit and after a 5-step held-out momentum continuation (matching the ledger's rule that commit outputs alone do not certify slot safety).

#### 07. Enforce seam non-interference so glued fragments cannot form a covert split (P)
- **Mechanism:** Type every fragment with a read/write effect manifest and check *across every glue seam* that no earlier fragment encodes a hidden-history difference into a shared state (norm, clip threshold, active gate) that a later fragment branches on or scales by; reject disguised splits or charge them as observations.
- **Novelty vs nearest prior art:** [Information-flow typing][flow] and #211#05 check monolithic replies. Gluing creates a two-step covert channel: two fragments that each look blind on a fixed state can leak history across their seam via conditional clipping.
- **Cheapest first test:** Construct two individually valid fragments whose composition clips conditionally on hidden history; compare seam-flow typing against per-fragment typing, dynamic read logging, and a licensed queried split.
- **Old-task retention check:** Swap hidden histories in shadow at the seam and check A/C; reject any sequence whose retention depends on history-conditioned clipping.

#### 08. Amortize harvested fragments across new obstructions in a canonical obligation algebra (P)
- **Mechanism:** Normalize extracted fragment entry/middle/exit clauses into a canonical, cell-independent vocabulary so fragments harvested from earlier cells' rejected specialists can be glued to cover a *new* cell where no previously synthesized whole reply applies.
- **Novelty vs nearest prior art:** #211#10 amortizes whole covering replies across overlapping cores, and [correction classes (PR #169)][classes] reuse whole witnesses. Amortizing *fragments* covers novel combinations of obligations without re-running specialist extraction.
- **Cheapest first test:** A 4-cell stream with rotating protected `C₁…C₄` constraints where no whole reply repeats, but 6 canonical fragments cover every cell; compare against #211#10 whole-reply caching, fresh monolithic synthesis, and Pacti library search at equal bytes.
- **Old-task retention check:** Add a 5th cell with a cross-coordinate C constraint outside the canonical vocabulary and confirm the composer refuses to glue rather than over-generalizing.

#### 09. Require anytime (prefix-interruptible) exit contracts on every glued sequence (P)
- **Mechanism:** Certify that if execution is interrupted after any prefix `f₁; …; f_j` of a glued sequence, every history in `H` remains above its hard A/C floors and admits a bounded history-blind completion, with zero rollback buffer.
- **Novelty vs nearest prior art:** Transactional rollback depends on saved state (violating the ledger's no-save-stack rule); #195#07 hands off partial batch orders. Anytime gluing guarantees safe live service at every fragment seam inside the live host alone.
- **Cheapest first test:** Interrupt Fixture 1 after ticks 1, 2, and 3 and inject a held-out continuation; compare anytime-glued sequences against commit-only glued sequences, rollback-buffered transactions (charged for backup bytes), and conformant planning.
- **Old-task retention check:** Score A and every `Cᵢ` immediately at each interruption point and after the held-out continuation, including a rare C slice sensitive to partial `x₄`.

#### 10. Cap gluing search depth by the minimum obligation-cycle cut size (I)
- **Mechanism:** Build the directed conflict graph among specialist obligations over `H` and use its minimum cycle cut size to cap fragment-gluing length before switching to monolithic synthesis or a split query.
- **Novelty vs nearest prior art:** Iterative-deepening conformant planning and #211#04 actuation ladders cap search by generic step count. Using obligation-cycle cut size is an audit/heuristic improvement for deciding when fragment gluing pays off.
- **Cheapest first test:** Enumerate 3- and 4-history fixtures with conflict-cycle lengths 2, 3, and 4; compare cycle-cut capping against iterative deepening, #211#04 ladder, and exact joint search.
- **Old-task retention check:** Hold identical per-tick A/C floors across all depth policies; a cap that misses a valid gluing must fall back to a certified split or refusal, never an unverified reply.

### Park a shared coordinate in a universally safe intermediate state, edit, and clear the park

#### 11. Synthesize a history-blind park–edit–clear triad with certified park-state service (P; parent 08)
- **Mechanism:** When a shared coordinate `s` couples with opposite signs to an edit across hidden histories, execute one blind 3-phase script: (1) move `s` to a fixed, history-independent `s_park` where every `h ∈ H` clears its hard A/C floors and decouples from the edit; (2) apply the B edit; (3) move `s` to its public commit value `s_clear` without reading which history held `s`.
- **Novelty vs nearest prior art:** [#157 make-before-break][make] allocates a duplicate route; [#199#2 escrowed handshakes][handshake] coordinate two branches; transactional updates lock/buffer; ledger's return-point adapters save old state. Here `s_park` is a *single history-independent live state* at fixed width with certified service during the park.
- **Cheapest first test:** Fixture 2 plus the `A ≥ 7/8` no-park negative; compare against #157 make-before-break (charging spare route), per-history migration (charging split query), transactional stall, #199#2, and conformant planning.
- **Old-task retention check:** Serve A and both `C₁, C₂` at `(0, 0, 0)` and mid-edit `(0, 1, 0)`, then after commit and a held-out continuation; disqualify scripts that pass only at commit.

#### 12. Park via fixed-width algebraic decoupling instead of spare capacity (P)
- **Mechanism:** Park an active multiplicative gate (e.g., a layer-norm scale, attention gate, or residual weight) at a zero-coupling value so the edited branch cannot perturb protected readouts while a parallel live path carries A/C above floor, then restore the gate once compensating weights align — using zero extra width.
- **Novelty vs nearest prior art:** [Net2Net][net2net] and #157 add spare units/routes; [OGD][ogd]/[GPM][gpm] project gradients into a static nullspace. Algebraic decoupling temporarily zeroes a coupling factor at fixed width to traverse a region that static subspace projection cannot cross.
- **Cheapest first test:** A fixed-width 2-branch toy MLP with a shared gate `s` and a frozen residual carrying A above floor at `s = 0`, plus a weak-residual negative; compare against OGD/GPM, #157 (width-charged), and direct edit + repair.
- **Old-task retention check:** Check A and a rare C slice on held-out inputs during `s = 0` and after `s ← 1`, verifying the residual truly holds the floor rather than masking a silent drop.

#### 13. Certify park-state survivability under bounded concurrent continuations (P)
- **Mechanism:** Certify that `s_park` remains a valid, safe serving state even if up to `L` unannounced public inputs or minor updates arrive between parking and clearing, rather than assuming an atomic uninterruptible critical section.
- **Novelty vs nearest prior art:** Transactional locks halt concurrent work; [split-timed deadlines (PR #180)][deadlines] lease proofs over update horizons. Certifying a *live park basin* against bounded concurrent continuations avoids stall regret while keeping safety blind to hidden history.
- **Cheapest first test:** Fixture 2 with 1–3 unannounced public continuation steps inserted between `w ← 1` and `u ← 1`, plus an adversarial continuation that exits the safe park basin; compare against lock/stall transactions (charging stall regret) and naive parks.
- **Old-task retention check:** Evaluate A and all `Cᵢ` after each interleaved continuation step while parked and after the delayed clear; confirm out-of-basin continuations trigger refusal before parking.

#### 14. Enforce a no-escrow-leak type rule separating universal parks from save/restore stacks (P)
- **Mechanism:** Require a proof that `s_clear` depends solely on public state and the B target (constant across `H`) and that no auxiliary coordinate stores a history-specific copy of pre-park `s` to be read back on clear.
- **Novelty vs nearest prior art:** Return-point adapters (ledger kill) and blue-green swaps save old state in a side buffer; #211#05 checks no-read on monolithic replies. This audit specifically blocks a park–clear script from smuggling a disguised save/restore stack across the edit.
- **Cheapest first test:** Pair a true universal park (`s_clear = 1` for all `h`) with a disguised save-stack that copies `s(h)` into a slack coordinate before parking; zero the slack coordinate at the park tick in shadow and test both arms.
- **Old-task retention check:** Verify A and every `Cᵢ` after clear under shadow pre-park perturbations of `s`; a genuine universal park still passes, while the disguised save-stack fails.

#### 15. Emit a two-part park impossibility witness: no safe park vs unsafe clear (P)
- **Mechanism:** When no park–edit–clear triad exists, return a typed witness separating (a) *no safe park* (no `s` simultaneously clears all A/C floors and decouples the edit) from (b) *unsafe clear* (a safe park exists, but no history-blind `s_clear` meets both B and all `Cᵢ` at commit).
- **Novelty vs nearest prior art:** #211#03 refutes a template monolithically and [barrier certificates][barrier] prove generic reach-avoid infeasibility. Splitting park vs clear infeasibility tells the editor whether relaxing park-tick service (if lawful) suffices or whether commit-time obligations force a split.
- **Cheapest first test:** Fixture 2 across three variants: feasible (`A ≥ 1/2`), no-safe-park (`A ≥ 7/8`), and safe-park/unsafe-clear (incompatible final `s_clear` requirements); compare typed routing against generic UNSAT and query-first baselines.
- **Old-task retention check:** Confirm every branch of the typed router preserves A and all `Cᵢ` at every tick, including a planted rare C slice that breaks only at clear.

#### 16. Park a shared optimizer slot without resetting unrelated weights or slots (P)
- **Mechanism:** Temporarily drive a single shared optimizer slot (e.g., momentum coordinate `m_s` carrying opposite-signed hidden histories) into a neutral zero-coupling zone via a short truthful sequence or bounded slot-park move, apply the weight edit, then restore operating momentum blindly — leaving unrelated slots intact.
- **Novelty vs nearest prior art:** [Optimizer resets][optreset] wipe momentum globally; [#197#15][protective] shapes momentum one-way for a known shift; [#212#14][handshakes] rotates paired branch slots. Targeted, temporary *single-slot parking* avoids both the hidden-history crash and global-reset B slowdown.
- **Cheapest first test:** A 2-coordinate momentum host with opposite-signed hidden `m_s` across histories; compare targeted slot park–edit–clear against full momentum reset, #197 order shields, direct editing, and a slot-free SGD negative.
- **Old-task retention check:** Score A, rare C, and B gain over a 10-step post-clear continuation (matching PR #197's horizon) to catch delayed slot-mediated relapse.

#### 17. Pre-train a certified maintenance-mode park into an active coordinate (P)
- **Mechanism:** During truthful training of old tasks A and C, regularize a designated shared coordinate `s` so a fixed `s_park` always keeps A and C above their hard floors, pre-installing a cheap universal park before future B edits are known.
- **Novelty vs nearest prior art:** #211#11–19 shape optimizer slots to cap Helly arity; [neutral groups (PR #183)][neutral] maintain output-exact reroutes; continual backprop recycles dead units. Pre-training a *certified live maintenance mode* on an active coordinate trades small training-time overhead for cheap future blind decoupling.
- **Cheapest first test:** Train a small MLP on A and C with vs without a maintenance-mode floor at `s = 0` (matched width and normal-mode accuracy), then issue held-out conflicting B edits; compare against unshaped training, #183 neutral groups, and OGD.
- **Old-task retention check:** Evaluate A and a held-out rare C slice at both `s = 1` and `s = 0` before, during, and after held-out B edits; charge the full training overhead of maintaining the park.

#### 18. Stagger rolling parks across coupled coordinates when joint parking breaks service (P)
- **Mechanism:** When parking two shared coordinates `(s₁, s₂)` together breaches A's service floor, park `s₁` while `s₂` carries A, execute the `s₁`-decoupled edit half, clear `s₁`, then park `s₂` while `s₁` carries A, execute the second half, and clear `s₂` — a history-blind rolling maintenance window at fixed width.
- **Novelty vs nearest prior art:** [Cancelling cycles (PR #210, card 06)][cycles] borrows margin across phases of a periodic orbit; #157 uses a spare route. Rolling parks use *existing active coordinates* as mutual temporary carriers for a one-shot blind edit without periodic cycles or extra width.
- **Cheapest first test:** A 2-gate extension of Fixture 2 where A requires `s₁ + s₂ ≥ 1` (blocking `(0, 0)` while allowing `(0, 1)` and `(1, 0)`), plus a `s₁ + s₂ ≥ 3/2` negative; compare against single-park (infeasible), #157 (width-charged), and conformant planning.
- **Old-task retention check:** Verify A and every `Cᵢ` at `(0, 1)`, mid-edit 1, `(1, 1)`, `(1, 0)`, mid-edit 2, and final commit, plus a held-out continuation.

### Combine glued fragments and universal parks, and test where both lose

#### 19. Insert a universal park as a typed seam between un-unifiable specialist fragments (P)
- **Mechanism:** When specialist fragment `f₁`'s exit condition cannot directly unify with specialist fragment `f₂`'s entry condition across `H`, insert a certified park–clear seam `(park(s); f₂; clear(s))` that bridges the interface mismatch without reading hidden history or re-synthesizing `f₁, f₂`.
- **Novelty vs nearest prior art:** Neither #211#02 (fragment gluing) nor #211#08 (single-edit park) alone resolves a cell where fragments are incompatible *and* their direct seam fails; Pacti and conformant planning do not treat a universal park as a reusable seam connector over deleted-history fragments.
- **Cheapest first test:** Combine Fixtures 1 and 2 so `f₁; f₂` fails unification directly (exit of `f₁` violates entry of `f₂` on `h₂`), while inserting `park(s)` at the seam covers all histories; compare against gluing alone, park alone, their naive stack, and exact conformant planning.
- **Old-task retention check:** Check A and every `Cᵢ` at every fragment boundary and during the park seam, plus a negative where the park seam itself breaches a rare C slice.

#### 20. Glue specialist parking fragments into a compound history-blind park (P)
- **Mechanism:** When incompatible specialists each contain a safe local parking step for their own history's coordinate, extract those parking fragments and glue them into one compound park covering the union of histories, without executing any specialist's full per-history migration.
- **Novelty vs nearest prior art:** Per-history migration queries the history first; #211#08 synthesizes a single park from scratch. Gluing *specialist parking fragments* composes local transition safety into a joint blind park across coordinates.
- **Cheapest first test:** Two histories where specialist 1 safely parks `s₁` and specialist 2 safely parks `s₂`, while neither specialist's full edit covers the other; compare glued compound parking against fresh park synthesis and query-to-split at matched verification cost.
- **Old-task retention check:** Check A and all `Cᵢ` at the compound park and after clearing both coordinates, including an adversarial case where parking both simultaneously violates A (must be refused).

#### 21. Carry drift-margin certificates on glued/parked scripts across bounded host updates (P)
- **Mechanism:** Export a verified glued or parked script together with explicit per-seam and per-park numerical margins `(ε_entry, ε_park, ε_exit)` so that after an unrelated host update of norm `≤ δ`, the same script is re-admitted by a cheap public margin check rather than re-synthesized.
- **Novelty vs nearest prior art:** #211#21 ties expiry to a training invariant and [#190#03][licenses] compiles price regions. Carrying *per-seam and per-park drift margins* lets a multi-step blind composition survive bounded host drift without reopening deleted histories.
- **Cheapest first test:** Perturb Fixtures 1 and 2 by unrelated updates inside and just outside `δ`; compare margin-checked reuse against fresh gluing/park synthesis and cached-script re-verification at matched bytes.
- **Old-task retention check:** Plant a rare C slice whose drift sensitivity exceeds the public bound and confirm the certificate invalidates before admitting an unsafe reuse.

#### 22. Falsification audit: map where fragment gluing and universal parks lose to monoliths, splits, or make-before-break (I)
- **Mechanism:** On a fully enumerated grid of small multi-history edit worlds, compare (a) fragment gluing, (b) universal park–edit–clear, (c) park-as-seam gluing, (d) #200#08 monolithic reply synthesis, (e) #157 make-before-break, (f) #190#09 query-to-split, and (g) exact conformant planning — charging extraction, unification, park-state service loss, proof checking, and fallback equally.
- **Novelty vs nearest prior art:** #211#22 audits covering replies vs splits; this audit specifically tests whether *fragment decomposition* and *fixed-width parking* earn a real Pareto win over monolithic synthesis + make-before-break + conformant planning once all intermediate-tick and extraction costs are counted.
- **Cheapest first test:** A factorial paper/CPU grid varying initial slack (zero vs partial), coupling sign symmetry (opposite vs aligned), park service floor (low vs tight), and query tariff (cheap vs expensive), including both un-unifiable and no-safe-park negatives.
- **Old-task retention check:** Admit only arms meeting identical per-tick A and rare-C floors and B commit utility; report park-state service loss, false admissions, and refusals separately.

## Ranked deeper questions

1. **Can gluing fragments of incompatible specialists beat both monolithic covering-reply synthesis (#200#08) and exact conformant planning once extraction and per-tick seam verification are charged?** Start with 01, 02, 04, and 22. A real win requires either solving cells where monolithic synthesis times out or fails at matched cost, or amortizing harvested fragments (08) across rotating obstructions where no whole reply repeats.
2. **Does a fixed-width universal park genuinely decouple opposite-signed hidden histories without sneaking in a save/restore stack or paying hidden stall/service costs?** Start with 11, 12, 14, and 15. Compare directly against #157 make-before-break (charged for extra width) and per-history migration (charged for split bits), enforcing live A/C floors at the park state and under bounded concurrent continuations (13).
3. **Do fragment gluing and universal parking interact super-additively when a park serves as the seam between un-unifiable specialist fragments?** Start with 19 and 20 against the best equal-budget stack of gluing alone, parking alone, and conformant planning. Count a joint win only when the park-seam unlocks a cover neither mechanism reaches alone without violating a rare C slice.
4. **Can a pre-trained maintenance-mode park (17) or targeted optimizer-slot park (16) survive realistic nonlinear training dynamics without hurting normal-mode B plasticity?** Test against unshaped training, #183 neutral groups, OGD/GPM, and full optimizer resets at matched width, normal-mode A/C accuracy, and post-clear B gain over a multi-step continuation.

**Verdict:** Keep fragment gluing as a conditional primitive only if harvesting typed entry/middle/exit fragments from *incompatible* specialists covers deleted-history obstructions more cheaply or more broadly than monolithic synthesis, Pacti composition, and conformant planning, with zero covert history dispatch across seams. Keep universal parking only if a fixed-width, history-independent live maintenance state decouples blind edits while clearing all A/C floors *during the park* and beating width-charged make-before-break, save/restore stacks, and split-guided migration. Fixtures 1 and 2 make both claims concrete and falsifiable, not established.

[sygus]: https://doi.org/10.1109/FMCAD.2013.6679385
[repair]: https://arxiv.org/abs/2301.11342
[shared]: https://github.com/manojbajaj95/cl/pull/173
[teaching]: https://github.com/manojbajaj95/cl/pull/179
[conformant]: https://arxiv.org/abs/1401.3468
[ogd]: https://arxiv.org/abs/1910.07104
[pacti]: https://arxiv.org/abs/2303.17751
[unreal]: https://arxiv.org/abs/1905.05800
[flow]: https://doi.org/10.1109/JSAC.2002.806121
[make]: https://github.com/manojbajaj95/cl/pull/157
[barrier]: https://doi.org/10.1109/TAC.2007.902736
[splice]: https://github.com/manojbajaj95/cl/pull/185
[gpm]: https://arxiv.org/abs/2103.09762
[net2net]: https://arxiv.org/abs/1511.05641
[optreset]: https://arxiv.org/abs/2306.17833
[group]: group-obstructions.md
[orders]: https://github.com/manojbajaj95/cl/pull/195
[protective]: https://github.com/manojbajaj95/cl/pull/207
[classes]: https://github.com/manojbajaj95/cl/pull/169
[handshake]: https://github.com/manojbajaj95/cl/pull/199
[deadlines]: https://github.com/manojbajaj95/cl/pull/180
[neutral]: https://github.com/manojbajaj95/cl/pull/183
[cycles]: https://github.com/manojbajaj95/cl/pull/210
[handshakes]: https://github.com/manojbajaj95/cl/pull/212
[licenses]: https://github.com/manojbajaj95/cl/pull/190
