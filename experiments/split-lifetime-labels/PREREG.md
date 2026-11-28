# CV16 preregistration — when should a process label expire?

## Selection (Nov 28)

Consider eligible individual research cards in main's Survived review and
Queued sections and check the reviewer-verdicts branch for omitted candidates.
Exclude existing papers or pilot outcomes, pending gates, novelty-only triage,
improvements (ledger grading rule), process items, and server-side MCP SkillEvo
(declined). Rank explicit survivor grades first, then cheapest decisive test
(prefer finite CPU enumeration to fitting a learner or calling a model).
CV16 in [PR #411](https://github.com/manojbajaj95/cl/pull/411) is a grade-3
primitive with no pilot. Its exact finite arithmetic assay requires no learned
policy or learned checker, unlike the other explicitly promoted continual-verifier
cards. The archived reviewer-verdicts branch adds no omitted eligible survivor.
This tests the label maintenance primitive, not downstream language-model learning.

## Frozen protocol

- Use NumPy PCG64 seeds 0–31, independent streams of 16 arithmetic boards
  (12 released to the upgraded solver; 4 unchanged). Each board has states
  0–23 and an independently drawn uniform goal. A candidate step adds
  one of +1, +3, −2, +25; declared step validity is just whether the destination
  stays on the board. Label every candidate from every state (including
  the goal) with validity, and each legal candidate with signed progress:
  bounded reachability within 4 further moves from its destination minus
  reachability within 5 moves from its source. The base continuation solver
  uses +1, +3, −2; it stops successfully at the goal.
- Independently draw a residue class mod 3 per board and shuffle row order
  once per board, shared across arms. Release A adds a solver-only move +6
  from that class; secondary release B instead adds −5, using the same paired
  boards and seeds. The legal candidate grammar does not change. The
  unchanged boards receive neither move; both budget and retention are
  measured on the labeled store itself.
- Use the base reachability cache and fixed row order in all arms. A guarded
  row stores a three-bit mask for whether either of its progress terms, if
  previously false, can reach the source of a first new move with time left
  under the old solver. The mask need not tell whether that move succeeds.
  Do not use fresh truth or changed-label identities to schedule work.
- Compare **split** (carry legality, refresh only flagged progress) to
  **whole** (same guard, queue and v2 cache, but refresh the coherent
  joint row including an independent legality recheck); to **PAV recompute**
  (shared memoized v2 reachability and preserved independent validity,
  checking every legal row on upgraded boards, no row support masks);
  and **unguided carry** (validity and progress remain separate but frozen).
  Whole and PAV recompute may continue serving v1 labels until v2 work
  finishes; this avoids handicapping them with forced abstention.
  All recomputing arms can reuse v1 true reachability cells and share fresh
  reachability cells across rows of a board. None can inspect v2 oracle labels.
  A separate exhaustive v2 labeling oracle is the positive control.
- Equal caps per upgraded board: 48, **96 (primary)**, 192, 384 primitive
  operations. Charge 1 per row guard lookup, 1 per whole-label validity
  attempt, and 1 per attempted continuation action (including blocked
  actions); arithmetic, indexing, base compilation and hashing are not
  charged. Report wall time separately, not as a calibration of those units.
  Do not publish a row until both terms finish within budget. Report
  packed extra mask payload (one byte per candidate, Python overhead
  excluded), validity work, number of changed labels, and queue precision.

## Decision

Primary endpoint is exact joint-row accuracy over all upgraded-board rows,
in pp, at 96 operations/board, release A. The independently checked testbed
must have at least 1 pp stale-carry error there and the unrestricted versions
of the three refresh arms must return exact oracle labels on every row.
Require exact retention on all unchanged boards and on all invalid steps,
and separately report retention on unchanged valid detours and old progress
ordering (groupwise weak ordering on unchanged boards).

Promotion requires a >2 pp lift over **both** whole-label invalidation and
PAV recompute at the primary cap (lower confidence bound >2 pp) and exact
retention. **Kill** the tested primitive if either comparison's upper bound
is below 2 pp when harness and retention checks pass; if neither decision
holds, report inconclusive, not equivalence. Report seed-level paired t
intervals, 97.5% per comparison for a Bonferroni simultaneous 95% family
over the two primary contrasts. Other budgets and release B are descriptive
and cannot overturn the primary gate. No seed replacement or early stopping.
