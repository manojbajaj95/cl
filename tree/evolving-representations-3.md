# Evolving Representations 3: Retire a Token, Keep Its One Reader

Child of [evolving-representations-2.md](evolving-representations-2.md) (depth 2) · 27 cards (21 proposals + 6 audits and controls) · 4 ranked deeper questions · Ideas only; no GPU, no experiments run (one exact CPU fixture computed by enumeration)

**Why this node exists.** The reviewer's triage of [PR #328](https://github.com/manojbajaj95/cl/pull/328) ([flood-triage row 446](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md#L446)) kept #325's ER01/ER11 at score 3 and promoted two of #328's cards:
1. **ER2-16 · Retire a token globally but keep its one needed distinction as an action fiber.** When merging `ab` is future-equivalent on almost all text but breaks one downstream action (e.g. exact delimiter parsing), complete the retirement and store the lost cue as an ER11 fiber that only that action reads. Required controls: aborting the retirement, ER01 with a larger residual state, keeping `ab` as a special token, a sampler-side merge with an exception table at equal bytes, a cue needed by several actions, and old-text perplexity plus action-task retention.
2. **ER2-20 · Only allow a token merge that preserves every live fiber's cue.** A merge nearly lossless on text can erase the prefix cue an active action fiber reads, so merges must commute with the fiber read. Required controls: ER01 merges judged on text perplexity only, a merge checked on next-byte agreement, ER2-27's order-dependent witness automaton, freezing every token a fiber touches, and retention of the fiber's action task after the merge.

The reviewer also flagged ER2-23 (do byte-equivalent parse pairs stay equivalent in a trained model?) as the gate for every ER01 variant. It is not re-proposed here; every card below assumes it runs first and names what changes if it fails.

**Thesis.** Both promoted cards treat the retired token's lost distinction as something that still *exists* after retirement and only needs a new home. That is true only sometimes. Once `ab` leaves the alphabet, the input no longer says whether the bytes `a`,`b` arrived as one token or two. The distinction the breaking action read is then either (i) a function of the byte context, which a fiber can recompute, possibly with **delay**; or (ii) carried only by a side channel (who wrote the bytes, a non-canonical encoding, a control-token authority), which no amount of byte context restores. This node builds the two promoted cards around that split. Group A makes the retire-then-fiber round trip concrete, including where the fiber's input comes from. Group B makes "merges commute with fiber reads" checkable, and shows mutual-information preservation is not enough when the cue shifts in time. Group C fuses retirement and fiber placement into one operation, and Group D holds the audits and the exact fixture.

**Constraints inherited from the ledger and tree.** Read from [idea-ledger.md](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md) and the parent:
- **Present-output agreement is not future-training agreement** ([PR #104](https://github.com/manojbajaj95/cl/pull/104), [2608.15976][fiber]). A fiber that reproduces the act_3 output today can still diverge under C.
- **Merge cards must beat the stacked union of their parts' baselines** (ledger patterns). For the ER2-16 × ER2-20 cards in Group C, that stack is "exception table + freeze every fiber-touched token + global exact refinement".
- **Retention check in every first test**, and **no pilots on IMPROVEMENT cards**. Each card is labelled PRIMITIVE, IMPROVEMENT or AUDIT.
- **True by construction / ties a simple baseline** kills: in exact finite machines, the coarsest quotient that respects every reader is computed by partition refinement ([Paige–Tarjan][paigetarjan]; [2608.06386][endpoint]). Any card whose only claim lives in the exact finite case is a control, not a result.
- Not re-proposed: global 1-bit provenance flags (ER2-06), commuting batch retirement (ER2-07), fiber-to-base promotion (ER2-11), zero-sum split-merge budgets (ER2-18), merge-vs-split arbitrage (ER2-21), replay/append-and-retrieve shortcuts.

**Literature check (alphaXiv, November 2026; primary texts read where marked).**
- [When Is Forgetting Provenance Lawful? Endpoint Sufficiency and Behavioral Quotients (2608.06386)][endpoint] *(read)*: the exact finite-system answer to "when may a distinction be forgotten". The greatest endpoint-respecting bisimulation is the coarsest exact quotient, computed by partition refinement initialized from endpoint classes. Its worked witness has two occurrences with the same visible graph but different permissions for a boundary-touching rewrite. **This is the nearest prior for ER2-16 and ER2-20 in the exact case.** It refines the state globally, for every consumer; it has no reader-scoped fiber, no learned model and no deletion of a token from weights.
- [Output-decomposed Learning of Mealy Machines (2405.08647)][mealy] *(read)*: learns one smaller machine per projected output and reconstructs the whole system from the projections. This is the automata-learning ancestor of "each reader keeps its own quotient". It learns from scratch, with no continual edits or alphabet retirement.
- [Inference Equivalence and Quotient Coding (2611.21096)][quotientcode] *(read)*: the coarsest code that preserves every valid claim of a declared task. It is static and single-task, and adding a claim means recomputing the code.
- [Lossy Common Information in a Learnable Gray-Wyner Network (2601.21424)][graywyner] *(read)*: a learned common channel plus task-private channels. "Global quotient + private fiber" is a Gray–Wyner split, so Group A must beat a Gray–Wyner-style common/private codec trained at equal bits. Gray–Wyner is static, with no retirement of an existing symbol.
- [Same Bytes, Different Authority (2609.35932)][samebytes] *(read)*: a forged `<|im_start|>` sent as one reserved token gets 39–66 pp more attack success than the same bytes as subwords. The token ID carries authority beyond its bytes, which is exactly a side-channel cue of kind (ii).
- [Nameless Tokenization (2609.16984)][nameless] *(read)*: keeps control entries as reserved IDs with *no* surface string, so content cannot forge them. It is a tokenizer-level fix that keeps the token, the opposite of retiring it.
- [Pruned BPE (2608.00837)][prunedbpe] *(read)*: makes low-exposure tokens internal-only merge nodes and reallocates their visible slots. Tokenizer-side only, judged by encoded length, with no downstream-reader check.
- [Lossless Vocabulary Reduction (2510.08102)][lossless] *(read)*: an exact sub-vocabulary distribution that keeps the original model running. This is the sampler-side wrapper control.
- [TokDrift (2510.14972)][tokdrift] *(read)*: semantically identical code that tokenizes differently shifts code-LLM behaviour, and the effect originates in early embeddings. This is a natural real breaking action.
- [SELD (2611.12903)][seld] *(read)*: compressed contexts can lose the evidence for an answer while the answer stays the same. This is the context-compression twin of ER2-20's trap, where text perplexity is unchanged but the reader's cue is gone.
- *Commit Now, Pay Later* (alphaXiv, 2026; arXiv ID not resolved by search, so cited by title) *(abstract read)*: steering a streaming transducer to keep track of where output came from is decidable under bounded ambiguity with bounded lookahead, and RE-complete otherwise. "The only difficulty is timing: a choice must be made before the input that decides it is visible." That is the delayed-fiber problem in transducer form. The older exact notion of bounded delay for streaming string transducers is [2205.04287][sstdelay].
- Also checked, abstracts only: [Language Models over Canonical BPE (2506.07956)][canonical], [Broken Tokens? (2506.19004)][brokentokens] (models handle non-canonical encodings), [the partial token problem (2601.23223)][partialtoken], [KLOD locality-preserving edits (2608.27839)][klod], [AlphaEdit null-space edits (2410.02355)][alphaedit], [scalable partial-bisimulation minimization (1207.2462)][partialbisim], [minimization of streaming transducers (2605.11190)][sstmin], and [emergent retokenization symmetry (2606.15521)][retoksym].

**Exact CPU fixture F-delay (computed by enumeration for this node).** BPE over bytes `{a,b,c,d}` with merge ranks `bc` before `ab`. `abc` encodes as `a|bc` and `abd` as `ab|d`. Over every string of length 2–6, whether the bytes `ab` at position `i` were sent as the single token `ab` is **not** a function of the causal byte prefix `s[:i+2]` (lookahead 0 fails). It **is** a function of `s[:i+3]` (lookahead 1 holds). So the old token-level model got one byte of lookahead from the tokenizer for free. After `ab` is retired, a causal fiber that reproduces the old cue exactly must resolve it **one byte late**. Any reader that acts at the `b` position must either wait one step or accept a lossy cue. This turns "store the cue in a fiber" into a timing question, and it is the basis of A1, B9 and D1.

**Shared fixtures (from the parent, reused).** F-tok (automaton plus 2-layer GRU/Transformer over `{a,b,c,ab}`), F-fiber (tabular MDP with aliased base states), and F-dual (tokenized observations over `{a,b,ab}`, where retiring `ab` breaks `act_3` on 5% of prefixes). New here: **F-auth**, a toy chat template where the delimiter `<|t|>` exists both as a reserved token (authority = 1) and as byte-spelled user text (authority = 0), and a dispatcher action reads authority. Every test is staged **A → B → C** as in the parent: fit A, retire or merge on B, learn fresh C. Equalize stored bits, examples and search budget. Delete the retired token row before scoring, and use no task IDs at test time.

---

## A · ER2-16 deepened: Retire globally, keep the cue for one reader

### ER3-01 · Delayed fiber: resolve the retired cue one step late, and let the reader wait — PRIMITIVE
- **Mechanism:** After retiring `ab`, compute the minimal lookahead `d*` at which the old cue becomes a function of the byte prefix (F-delay: `d* = 1`). Then install a fiber that writes the cue at position `i+2+d*`. Pair it with a **reader delay contract**: act_3 is re-scheduled to read `d*` steps later, rather than retrained to guess earlier. The fiber's cost is `d*` steps of reader latency plus `log2(classes)` bits, never an extra token.
- **Novelty vs nearest prior art:** [The partial-token problem (2601.23223)][partialtoken] and token healing fix *generation* at a prompt boundary. [Canonical-BPE LMs (2506.07956)][canonical] enforce canonicality at sampling time. *Commit Now, Pay Later* shows bounded-lookahead provenance controllers exist for transducers. None of these moves a downstream **action's read time** to absorb the lookahead the tokenizer used to supply. Gap: retirement as an explicit trade of tokenizer lookahead for reader latency.
- **Cheapest first test:** F-delay with a 2-layer GRU over bytes (CPU). On B, retire `ab` in three ways: (a) a causal fiber at delay 0, trained to predict the old cue; (b) a delayed fiber with act_3 shifted by one step; (c) abort the retirement (control). Also run the reviewer's controls: a sampler-side merge with an exception table at equal bytes, and ER01 with a +1-bit residual state. **Kill:** if (a) matches (b) on act_3 exact-match. That would mean the GRU already recovers the cue causally through some other correlate, so delay is irrelevant.
- **Old-task retention:** act_3 exact-match on the 5% breaking prefixes, plus old-text bits/byte, immediately after retirement and after C. Also measure act_3 latency in steps.

### ER3-02 · Cue-source triage: refuse retirement when the cue lives only in a side channel — PRIMITIVE
- **Mechanism:** Before retiring a token, classify each breaking prefix by where the cue the reader needs lives: **(i) canonical**, a function of bytes within `d*` lookahead (fiber can recompute it); **(ii) non-canonical**, where the same bytes could arrive as `ab` or `a|b` and the choice was made upstream; **(iii) provenance**, where the token ID encodes who produced the bytes (F-auth). Retire only when every breaking prefix is (i), or when (ii)/(iii) have an explicit side-channel input to feed the fiber. The classifier is exact on the automaton and estimated by re-encoding probes on the network.
- **Novelty vs nearest prior art:** [Endpoint sufficiency (2608.06386)][endpoint] decides whether provenance may be forgotten **given** the observable history. Gap: it does not ask whether the observable history after token deletion still *contains* the cue, so it treats (ii) and (iii) as forgettable when they are actually unrecoverable. [Broken Tokens (2506.19004)][brokentokens] shows models tolerate non-canonical input, but does not route the cue anywhere.
- **Cheapest first test:** Mix F-dual (canonical cue) with F-auth (provenance cue) at a 1:1 ratio. Compare a triage-gated retirement against an ungated ER2-16 retirement and against keeping `ab` as a special token. **Kill:** if ungated ER2-16 matches triage on F-auth dispatcher accuracy. That would mean the network smuggles provenance through some other channel and triage is unneeded.
- **Old-task retention:** Dispatcher authority accuracy, act_3 exact-match, and old-text bits/byte after B and after C.

### ER3-03 · Authority fiber: delete a control token's embedding and keep one bit for the dispatcher only — PRIMITIVE
- **Mechanism:** Retire the reserved delimiter `<|t|>` so that its bytes always reach the model as plain text. Carry a 1-bit **authority fiber**, set by the serving stack (not by the content), that only the dispatcher/role head reads. It is masked from the text and tool heads. The model can no longer distinguish authentic and forged delimiters by token ID anywhere except in the one reader that needs the distinction.
- **Novelty vs nearest prior art:** [Same Bytes, Different Authority (2609.35932)][samebytes] measures how much authority the reserved ID carries. [Nameless Tokenization (2609.16984)][nameless] keeps the ID and removes its surface string. Both keep a model-wide token for authority. Gap: authority scoped to a single reader as a fiber, with the token deleted from the shared embedding. This is ER2-16 instantiated on the one case where the cue is provably kind (iii).
- **Cheapest first test:** F-auth with a 2-layer Transformer (CPU). Arms: (a) authority fiber read only by the dispatcher; (b) Nameless-style reserved ID without a surface string (strongest control); (c) a global 1-bit flag visible to all heads (ER2-06-like); (d) bytes only, with no authority signal. Metrics: forged-delimiter attack success, delimiter-bearing user text accuracy, clean turn parsing. **Kill:** if (b) or (c) matches (a) on both attack success and delimiter-text accuracy at equal bits.
- **Old-task retention:** Clean multi-turn parsing and text bits/byte after B. After C (a new tool-result role), test whether authority still holds for the old roles.

### ER3-04 · Tombstone projection: compile the retired row into a reader-only rank-1 fiber, data-free — PRIMITIVE
- **Mechanism:** Before deleting the `ab` embedding row `e_ab`, split it as `e_ab = e_a⊕b + r`, where the first term is the byte-path representation. Project the residual `r` onto the row space of act_3's readout. That projection is the **tombstone**: a rank-1 write the fiber injects only into act_3's input whenever the F-delay cue fires. No data is needed, and the text heads never see `r`.
- **Novelty vs nearest prior art:** ER2-05 adds a rank-1 transition bias globally. Self-completion transport (ER2-03) moves distribution mass for the text head. [KLOD (2608.27839)][klod] and [AlphaEdit (2410.02355)][alphaedit] protect non-target outputs during *knowledge* edits. Gap: an analytic, reader-scoped residual from a deleted vocabulary row, extracted from weights alone.
- **Cheapest first test:** F-dual with a 2-layer Transformer. Arms: (a) tombstone only, with zero gradient steps; (b) a learned fiber with equal parameters and 100 examples; (c) re-init plus equal-compute SFT. **Kill:** if (a) recovers less than half of (b)'s act_3 recovery. That would mean the cue is not linearly carried by the row residual.
- **Old-task retention:** act_3 on breaking prefixes and text bits/byte immediately after deletion and after C. A data-free method must not hurt text at all, so any text regression fails the card.

### ER3-05 · Ghost-row gradient sink: keep training signal for the retired token flowing into the fiber during C — IMPROVEMENT
- **Mechanism:** During C, compute the gradients that would have reached the deleted `e_ab` row by reconstructing the old token boundary from the delayed cue. Route them only into the act_3 fiber parameters. The fiber keeps learning the C-time drift of the old distinction without restoring the token.
- **Novelty vs nearest prior art:** [PR #104](https://github.com/manojbajaj95/cl/pull/104) and [2608.15976][fiber] show present-output fibers drift under future training. ER2-04 adds a training-span term at merge time only. Gap: a continuing gradient channel after deletion.
- **Cheapest first test:** IMPROVEMENT, so no pilot. Specify it as a variant of ER3-04 once ER3-04 passes. **Kill condition:** a frozen fiber matches the ghost-row fiber on act_3 after C.
- **Old-task retention:** act_3 after C versus right after B; text bits/byte after C.

### ER3-06 · Reader-keyed attention channel: implement the fiber as keys only one head can query — PRIMITIVE
- **Mechanism:** Implement the fiber neurally as an extra key/value slot per position, masked so that only the act_3 readout's attention queries can attend to it. Every other head and the LM head get a hard `-inf` mask. Old readers are therefore *provably* unchanged at inference: a structural guarantee rather than a regularizer.
- **Novelty vs nearest prior art:** Adapters and prefix-tuning add parameters visible to the whole forward pass. Side-tuning adds a parallel network. [Gray–Wyner networks (2601.21424)][graywyner] separate private channels at the codec level, not inside attention. Gap: a structural "who may read the cue" mask placed exactly where the retired token's information used to enter the residual stream.
- **Cheapest first test:** F-dual with a 2-layer Transformer. Arms: (a) masked key channel; (b) the same channel unmasked; (c) a Gray–Wyner common/private codec at equal bits (control); (d) keeping `ab`. **Kill:** if (b) matches (a) on text bits/byte. That would mean leakage to other heads is harmless and the mask is unnecessary.
- **Old-task retention:** Text bits/byte must be bit-identical to the retired-without-fiber model, which tests the guarantee. Also act_3 after B and after C.

### ER3-07 · Retirement receipt: the breaking-prefix set becomes the regression suite for every later edit — PRIMITIVE
- **Mechanism:** At retirement, store a **receipt**: the minimal set of prefix classes where retiring changed act_3, found by contrasting outputs with and without the token. Serve the fiber only on receipt classes. Every later merge (ER2-20) or C step must leave receipt behaviour within ε. The receipt is a few hundred bytes of witness prefixes, not replay data from A.
- **Novelty vs nearest prior art:** [SELD (2611.12903)][seld] detects evidence loss after compression, once. Model-editing locality sets ([2601.17343][editlocality]) are chosen by the evaluator, not produced by the edit. Gap: an edit that emits its own minimal witness set and makes it a standing obligation. Equalize against ledger-forbidden replay by budget: the receipt holds witness *prefixes* only, with no labels from A.
- **Cheapest first test:** F-dual: retire `ab`, then apply 5 later ER01 merges. Arms: (a) merges gated by the receipt; (b) merges gated by a random equal-size prefix set; (c) merges gated by text perplexity (the reviewer's ER2-20 control). **Kill:** if (b) matches (a) on act_3 retention.
- **Old-task retention:** act_3 exact-match on all breaking prefixes after the 5 merges and after C.

### ER3-08 · Reader-count escalation price: when a second action starts reading the fiber — IMPROVEMENT
- **Mechanism:** Charge each fiber per reader. When C introduces act_4 reading the same cue (the reviewer's "cue needed by several actions" control), compare `n_readers × fiber_cost` against the cost of reinstating `ab`. Reinstate when the fiber costs more. This specifies ER2-16's break-even point, unlike ER2-11, which promotes by drift.
- **Novelty vs nearest prior art:** ER2-11 promotes by stability; ER2-18 is a global budget. Gap: a per-reader price derived from the receipt.
- **Cheapest first test:** IMPROVEMENT, so no pilot. Specify it as the sweep `n_readers ∈ {1,2,4}` on F-dual. **Kill condition:** the crossover sits at `n_readers = 1`, meaning keeping the token always wins.
- **Old-task retention:** act_3 and act_4 exact-match plus text bits/byte at the crossover.

### ER3-09 · Reader-side absorption: delete the token and teach act_3 to recompute the cue from bytes — PRIMITIVE (as the strongest control)
- **Mechanism:** Add no state at all. Retire `ab` and fine-tune only act_3's readout to read the byte window `[i, i+2+d*]`, so it recomputes the cue itself. The distinction moves into the *reader's* function rather than the *state*. This works for kind (i) cues only.
- **Novelty vs nearest prior art:** This is the null hypothesis for ER2-16 that the reviewer's controls did not list. If a reader can recompute the cue, a fiber is redundant storage. Nearest prior: canonical-BPE re-tokenization inside the model ([2506.07956][canonical]).
- **Cheapest first test:** Pair F-dual and F-auth: compare absorption against ER3-01's delayed fiber at equal parameters. **Kill condition for the fiber family:** absorption matches the fiber on F-dual, but fails on F-auth. That outcome means fibers are only needed for kind (ii)/(iii) cues, which narrows ER2-16 to the provenance case.
- **Old-task retention:** act_3 after B and after C. Absorption touches only act_3, so text must be unchanged.

---

## B · ER2-20 deepened: Merges that commute with every live fiber read

### ER3-10 · Reader-initialized exact refinement as the mandatory baseline — AUDIT
- **Mechanism:** On the F-tok/F-dual automata, compute the coarsest partition of parse states that is stable under transitions, with the initial partition given by the **joint** classes of (next-byte law, every live fiber reader's output). This is [Paige–Tarjan][paigetarjan] / [partial bisimulation (1207.2462)][partialbisim] refinement seeded as in [endpoint sufficiency (2608.06386)][endpoint]. Every ER2-20 merge proposed by a neural method is compared against the exact answer.
- **Novelty vs nearest prior art:** None claimed. This card exists because the ledger kills "true by construction" claims. In the exact case, ER2-20 *is* refinement with a reader-seeded initial partition, so any ER3-1x card must show value beyond it: on networks, under C, or at scale.
- **Cheapest first test:** Run refinement on F-dual (CPU, milliseconds). Report how many of ER01's text-only merges the reader seed vetoes, and whether the vetoed set equals the receipt from ER3-07. **Kill (for B-group novelty):** if a neural model that is distilled to match the automaton gets every veto right with no fiber-aware machinery.
- **Old-task retention:** This is an exact audit, so retention is by definition. Report act_3 and next-byte agreement on all prefixes up to length 8.

### ER3-11 · Fiber-read Jacobian screen: veto a merge whose direction the reader is sensitive to — PRIMITIVE
- **Mechanism:** A merge of tokens `u, v` moves hidden states along `Δ = h_u − h_v`. Score each candidate by `‖J_reader · Δ‖`, where `J_reader` is the Jacobian of each live fiber reader. Veto when the score exceeds τ. This is a first-order, data-light check (one Jacobian per reader, many candidates) that runs before ER01's expensive future-equivalence test.
- **Novelty vs nearest prior art:** [KLOD (2608.27839)][klod] preserves non-target output distributions during knowledge edits using sampled KL. [AlphaEdit (2410.02355)][alphaedit] projects edits into a null space of preserved keys. Neither screens *vocabulary merges* against *action readers*. Gap: a reader-sensitivity veto for alphabet edits.
- **Cheapest first test:** F-dual with a 2-layer Transformer and 40 candidate merges. Arms: (a) Jacobian veto; (b) text-perplexity-only veto (the reviewer's control); (c) next-byte agreement veto (control); (d) freezing every token a fiber touches (control). Score the vetoes against ER3-10's exact veto set. **Kill:** if (c) or (d) matches (a)'s precision and recall on the vetoes.
- **Old-task retention:** act_3 exact-match after all accepted merges; text bits/byte; then both after C.

### ER3-12 · Null-space merge map: choose the merged embedding inside every reader's kernel — PRIMITIVE
- **Mechanism:** Do not just pick merge-or-not. When merging `u, v → w`, choose `e_w` by solving `min ‖text loss change‖` subject to `J_reader (e_w − e_u) = J_reader (e_w − e_v) = 0` for each live reader, i.e. a least-squares solve in the readers' joint null space. When no feasible `e_w` exists, the merge is vetoed, and the certificate is the infeasibility.
- **Novelty vs nearest prior art:** [AlphaEdit (2410.02355)][alphaedit] uses a null-space projection for fact edits. Merge-time embedding initialization in tokenizer transfer (ER2 parent references) averages rows. Gap: merged-row placement constrained by downstream readers, with infeasibility serving as the commute test.
- **Cheapest first test:** F-dual as in ER3-11. Arms: null-space `e_w`, mean `e_w`, frequency-weighted `e_w`, and ER3-11's binary veto. **Kill:** if the mean row plus the ER3-11 veto matches null-space placement on act_3 and text.
- **Old-task retention:** act_3 and text bits/byte after the merge and after C.

### ER3-13 · Redundant-cue joint veto: two merges that are each safe can be jointly fatal — PRIMITIVE (with exact witness)
- **Mechanism:** Build a witness where act_3's cue is carried *redundantly* by two tokens, `ab` and `bc`: each one alone determines the cue on the breaking prefixes. Retiring either token alone leaves the cue intact through the other. Retiring both erases it. So **per-merge ER2-20 checks are not compositional**. The proposed gate keeps a running *cue-carrier set* per reader and vetoes the merge that would empty it.
- **Novelty vs nearest prior art:** ER2-27 is an order-dependence witness for one merge and one split. ER2-07 batches commuting retirements for the text head. Group testing and redundancy-aware feature pruning are the nearest ML analogues. Gap: non-compositionality of reader-safety across sequential alphabet edits, and a carrier-set gate for it.
- **Cheapest first test:** Construct the witness automaton (exact, CPU), then train a 2-layer GRU on it. Arms: (a) carrier-set gate; (b) independent ER3-11 checks per merge; (c) re-checking the full set after each merge with an exact recompute (expensive control). **Kill:** if (b) already vetoes the second merge on the GRU, because the model does not use the redundancy.
- **Old-task retention:** act_3 after the first and second retirement and after C; text bits/byte.

### ER3-14 · Timing-preserving commute: a merge that keeps the cue's information but moves it in time still breaks the reader — PRIMITIVE
- **Mechanism:** ER2-20 asks whether the cue survives the merge. F-delay shows that the cue can survive while its *resolution time* shifts by `d*` steps. A reader that samples at a fixed offset then fails even though mutual information is preserved. The proposed check is a **(cue, resolution-time) pair**: a merge commutes with a fiber read only if the cue is recoverable at the reader's read step, or if ER3-01's delay contract is re-negotiated explicitly.
- **Novelty vs nearest prior art:** MI-based and probe-accuracy checks ignore timing. *Commit Now, Pay Later* and [bounded SST delay (2205.04287)][sstdelay] give exact delay notions for transducers, but not for continual merge gates. Gap: a timing invariant for reader-safe merges.
- **Cheapest first test:** On F-delay, use merges that shift the cue by 0 or 1 steps. Arms: (a) timing-aware gate; (b) MI-preserving gate (control); (c) next-byte agreement gate (control). **Kill:** if act_3 is learned with enough slack that it never reads at a fixed offset, so (b) matches (a).
- **Old-task retention:** act_3 exact-match and latency, and text bits/byte, after the merge and after C.

### ER3-15 · Reader interface contracts: each action publishes the partition it needs — PRIMITIVE
- **Mechanism:** Each fiber reader exports a small **interface**: the coarsest partition of fiber-input classes it distinguishes, found by refinement on its own receipt. Merges are checked against interfaces, not against readers' weights or data. Adding a reader during C only adds an interface, and nothing else must be rechecked. Interfaces compose by meet.
- **Novelty vs nearest prior art:** [Output-decomposed Mealy learning (2405.08647)][mealy] learns a projection per output, but in a single offline pass. [Quotient coding (2611.21096)][quotientcode] fixes the code for a declared task. Interface automata (de Alfaro–Henzinger) compose component interfaces for verification. Gap: interfaces as the stable API between a continually edited alphabet and its consumers, so merges can be checked without touching any reader.
- **Cheapest first test:** F-dual plus F-auth, 3 readers, 20 merges. Arms: (a) interface-checked merges; (b) full re-check against all readers per merge (ceiling); (c) text-only merges. Metrics: check cost and act accuracy. **Kill:** if interface checks miss any veto that (b) catches on more than 2% of merges.
- **Old-task retention:** Each reader's accuracy after the merges and after C, where C adds a new reader and interface.

### ER3-16 · Trap mining: search for merges that are invisible to text but maximal for a reader — AUDIT
- **Mechanism:** Run adversarial search over candidate merges, maximizing reader output change subject to text bits/byte change below 0.01. The mined traps form the red-team suite every B-group gate must pass. This is ER2-20's failure mode made into a benchmark.
- **Novelty vs nearest prior art:** [TokDrift (2510.14972)][tokdrift] finds tokenization-boundary rewrites that change code-LLM behaviour. [SELD (2611.12903)][seld] finds compressions that silently lose evidence. Neither searches over *vocabulary merges* against *action readers*.
- **Cheapest first test:** On F-dual plus a toy code grammar (delimiters `(`, `)`, `()` as a candidate token), mine the top 10 traps. Report how many of them ER3-11, ER3-13 and ER3-14 each catch. **Kill (for the audit):** if fewer than 2 traps exist with text change below 0.01. That would mean ER2-20's risk is hypothetical on these fixtures.
- **Old-task retention:** act and text after each trap merge; the trap list is the retention suite.

### ER3-17 · Fiber-priced merge ranking: rank merges by bits saved minus fiber bits needed — IMPROVEMENT
- **Mechanism:** Replace frequency-ranked pruning ([LiteToken (2602.04706)][litetoken], [Pruned BPE (2608.00837)][prunedbpe]) with `score = embedding_bits_saved − fiber_bits(receipt) − reader_latency_cost(d*)`. Greedily take positive merges.
- **Novelty vs nearest prior art:** LiteToken and Pruned BPE rank by exposure only. Gap: a reader-aware price. This adds cost accounting on top of ER3-01/ER3-07, so it is an improvement.
- **Cheapest first test:** IMPROVEMENT, so no pilot. **Kill condition:** the frequency ranking plus ER3-11's veto selects the same merge set.
- **Old-task retention:** All readers and text after the selected merges and after C.

### ER3-18 · Stale-fiber detector after C: the merge was safe at B, but C changes what the reader needs — PRIMITIVE
- **Mechanism:** ER2-20 checks merges against fibers *as they are at B*. Under C, a reader's interface (ER3-15) can refine, so a merge that was safe becomes unsafe retroactively. Re-derive each interface from the reader's current receipt every K steps of C. When an interface refines past an already-applied merge, raise an alarm and **unmerge** that one token by reinstating it from its tombstone (ER3-04).
- **Novelty vs nearest prior art:** [Incremental bisimulation (1207.2462)][partialbisim] maintains quotients under model updates, but only for exact systems. CEGAR loops (the parent's references) refine abstractions on counterexamples, not alphabets on reader drift. Gap: retroactive merge invalidation driven by the consumer's continual drift.
- **Cheapest first test:** F-dual, where C trains act_3 to use a finer cue. Arms: (a) detector plus unmerge; (b) no detector; (c) freezing all fiber-touched tokens forever (control). **Kill:** if (c) matches (a) on act_3 after C at equal vocabulary size.
- **Old-task retention:** act_3 on the old prefixes after C, plus text bits/byte.

---

## C · One operator: Retire-and-place as a single transaction

### ER3-19 · Expand–dual-read–contract retirement: a schema migration for vocabularies — PRIMITIVE
- **Mechanism:** Retire a token in three phases, borrowed from the database expand/contract (parallel-change) pattern. (1) **Expand:** install the fiber (ER3-01/04) while `ab` still exists. (2) **Dual-read:** run act_3 on both the token path and the fiber path, logging disagreements into the receipt. (3) **Contract:** delete `ab` only once disagreement stays below ε for N steps. Otherwise roll back. Retirement and fiber placement become one atomic edit that cannot leave act_3 without its cue.
- **Novelty vs nearest prior art:** ER2-16 retires first and repairs after. ESCD/DVLM-style distillation ([2609.34738][escd], [2609.33816][dvlm]) keeps a teacher alive throughout. Gap: a bounded shadow window with a hard commit rule, after which no old-token state remains.
- **Cheapest first test:** F-dual with a 2-layer Transformer. Arms: (a) expand/contract; (b) ER2-16 retire-then-fiber; (c) aborting the retirement; (d) keeping a teacher alive through C (ceiling). **Kill:** if (b) matches (a) on act_3 immediately after deletion. That would mean no transient breakage needs guarding.
- **Old-task retention:** act_3 and text through all three phases and after C, including the worst-case act_3 dip during the window.

### ER3-20 · Product of reader quotients: retire a token only where every factor agrees — PRIMITIVE
- **Mechanism:** Maintain the representation as a product `Q_text × Q_act3 × … × Q_actk` of per-reader quotients, each a coarsening of the byte-parse state. Retiring `ab` is a merge in `Q_text`. It is allowed in `Q_act_i` only where that factor agrees; otherwise the distinction survives *only* in that factor. ER2-16 (retire plus fiber) and ER2-20 (commute check) become one rule: an edit is applied per factor, and the fiber is whatever the factors still distinguish that `Q_text` does not.
- **Novelty vs nearest prior art:** [Output-decomposed Mealy learning (2405.08647)][mealy] learns factor machines per output projection, but offline. [Gray–Wyner (2601.21424)][graywyner] splits common/private bits statically. Gap: continual alphabet edits applied factorwise, with the fiber *derived* as the factor difference rather than designed.
- **Cheapest first test:** On the F-dual automaton, plus a GRU with one hidden block per factor. Compare against the stacked baseline (exception table + freeze fiber-touched tokens + ER3-10 global refinement), which is the ledger's merge-card bar. **Kill:** if the stacked baseline matches at equal state bits.
- **Old-task retention:** Every factor's reader and text after B and after C, where C adds a factor.

### ER3-21 · Quotient-then-fiber versus fiber-then-quotient: does the order of the two edits matter on networks? — PRIMITIVE
- **Mechanism:** ER2-27 builds an order-dependent witness automaton for ER01 and ER11. Here, test the order on the *transaction* level. Retire-then-fiber (ER2-16) leaves a window where the cue is gone. Fiber-then-retire (ER3-19) does not. The claim is that ER2-16 and ER2-20 together need fiber-first ordering whenever the cue is of kind (ii)/(iii), and are order-free for kind (i) with `d* ≤ reader slack`.
- **Novelty vs nearest prior art:** ER2-27 is exact and offline. Gap: a predicted order law tied to cue kind and delay, checked on trained networks under C.
- **Cheapest first test:** Cross the 3 cue kinds (F-dual, F-delay, F-auth) with 2 orders on a 2-layer GRU. **Kill:** if the order effect is below 1 pp act_3 for all three kinds.
- **Old-task retention:** act_3 and text after B and after C for each cell.

### ER3-22 · Fiber reuse as C-transfer: a new action reading the retired cue learns faster than one relearning from bytes — PRIMITIVE
- **Mechanism:** In C, introduce act_4, which needs the same distinction as act_3. Give act_4 read access to act_3's fiber, and compare against learning the cue from bytes. If the fiber transfers, a retired token's distinction becomes a reusable, addressable object, which is the "portable local distinction" ER11 promised.
- **Novelty vs nearest prior art:** ER2-10 materializes fibers lazily for one action. ER2-11 promotes widely read fibers to the base. Gap: sharing a fiber *across* actions without promotion, with transfer measured as C's learning speed.
- **Cheapest first test:** F-dual with an act_4 variant. Arms: (a) fiber shared; (b) act_4 from bytes; (c) `ab` kept as a token; (d) the fiber promoted to base (ER2-11 control). Metric: C steps to 95%. **Kill:** if (b) learns as fast as (a).
- **Old-task retention:** act_3 after act_4 shares its fiber (check for interference); text bits/byte.

### ER3-23 · Fiber superposition capacity: how many retired cues can one k-bit fiber carry for m readers? — PRIMITIVE
- **Mechanism:** Retire `n` tokens, each breaking a different reader. Store all `n` cues in one shared `k`-bit fiber using superposed (random-projection) codes, with each reader decoding its own cue. Measure the capacity curve `n_max(k, m)` and the interference between readers. If capacity grows faster than linearly in `k`, vocabulary retirement becomes cheap at scale.
- **Novelty vs nearest prior art:** Superposition studies measure feature packing in trained models. Gap: deliberate packing of *retired-token* cues for scoped readers, with a falsifiable capacity law.
- **Cheapest first test:** On a synthetic F-dual family with `n ∈ {2,4,8,16}` retired tokens and `k ∈ {2,4,8}`, use a CPU GRU. **Kill:** if `n_max ≤ k`, so that superposition gives nothing over one bit per cue.
- **Old-task retention:** Every reader's exact-match plus text after B and after C.

---

## D · Audits and boundary probes

### ER3-24 · Real-tokenizer delay audit: how much lookahead does retiring a GPT-2 merge cost? — AUDIT
- **Mechanism:** For the 200 lowest-exposure merges of a public BPE tokenizer (GPT-2 merges, which are CPU-loadable), compute `d*`, the bytes of lookahead after which "were these bytes one token?" is a function of the byte prefix, over a 10 MB text and code slice. The F-delay result shows `d* = 1` exists in toy BPE. This audit asks whether real retirements have bounded, small `d*`.
- **Novelty vs nearest prior art:** [Partial-token (2601.23223)][partialtoken] studies prompt-boundary effects. [Pruned BPE (2608.00837)][prunedbpe] studies visible-vocabulary allocation. Neither reports per-merge lookahead needed to recover token identity. This is the input to ER3-01, ER3-14 and ER3-17.
- **Cheapest first test:** Pure CPU counting with the merge list and a regex pre-tokenizer. **Kill (for ER3-01):** if median `d*` exceeds 8 bytes or is unbounded for more than 20% of merges.
- **Old-task retention:** Not applicable; this is a measurement audit. Report alongside the decode-identity check (re-encoding reproduces the original stream).

### ER3-25 · Canonical versus side-channel share: what fraction of breaking prefixes are fiber-recoverable? — AUDIT
- **Mechanism:** For the F-dual breaking set and for TokDrift-style code rewrites ([2510.14972][tokdrift]), label each break as kind (i), (ii) or (iii) using ER3-02's triage. This decides whether ER2-16 is mostly a byte-recomputation problem (ER3-09 wins) or a provenance problem (ER3-03 wins).
- **Novelty vs nearest prior art:** [Broken Tokens (2506.19004)][brokentokens] and [retokenization symmetry (2606.15521)][retoksym] measure model tolerance to non-canonical encodings, but not which downstream actions depend on the encoding.
- **Cheapest first test:** CPU labelling on the fixtures plus a 1k-snippet code slice with a small public tokenizer. **Kill (for the fiber family):** if more than 90% are kind (i) with `d* ≤ 2`, since then reader absorption suffices.
- **Old-task retention:** Not applicable (audit).

### ER3-26 · ER2-23 gate interaction: if trained parses are not byte-equivalent, does the fiber still help? — AUDIT
- **Mechanism:** The reviewer made ER2-23 (Neural Nerode Gap) the gate for every ER01 variant. Cross ER2-23's outcome with ER3-04/ER3-06: when trained representations of byte-equivalent parses diverge, retirement loses information even for text, and the fiber might be absorbing text drift rather than act_3's cue.
- **Novelty vs nearest prior art:** Not a new method. It is a validity check that prevents ER3 results from being explained by the ER2-23 gap.
- **Cheapest first test:** On F-tok, measure the per-prefix hidden distance between `ab` and `a|b` parses. Bin breaking prefixes by that gap, and report fiber gains per bin. **Kill (for the A group):** if fiber gains concentrate entirely in the high-gap bins, because then they repair the Nerode gap and not a reader-specific cue.
- **Old-task retention:** Text bits/byte per bin after B and after C.

### ER3-27 · Equal-bit Gray–Wyner control for every fiber card — AUDIT
- **Mechanism:** Train a common/private codec ([2601.21424][graywyner]) on the post-retirement state, with the private branch read only by act_3, at exactly the fiber's bits. This is the generic learned alternative to every hand-placed fiber in Groups A and C.
- **Novelty vs nearest prior art:** Not claimed; it is the strongest generic control. Fiber cards survive only if they beat it on retention after C, or on data cost, because the fiber is compiled from the tombstone or receipt rather than learned.
- **Cheapest first test:** Run it alongside ER3-04, ER3-06 and ER3-20 on F-dual. **Kill (for those cards):** if Gray–Wyner matches them at equal bits and equal examples.
- **Old-task retention:** act_3 and text after B and after C.

---

## Ranked deeper questions

1. **Is a retired token's distinction recoverable, delayed, or gone, and can that be decided before deleting the row?** ER3-02/24/25 sort breaks into byte-recoverable within `d*` (kind i) and side-channel only (kinds ii/iii). If kind (i) with small `d*` dominates real tokenizers, ER2-16 reduces to reader absorption (ER3-09) and fibers are only for provenance. If not, the fiber is the only safe retirement path. Every A-group card depends on this answer.
2. **Is reader-safety of merges compositional in time and across merges?** ER3-13 (redundant carriers) and ER3-14 (resolution time) are two ways a per-merge ER2-20 check can pass while the sequence fails. If neither shows up on trained networks, ER2-20 is a cheap local check. If either does, merge gates need running state: carrier sets, timing contracts and interfaces (ER3-15).
3. **Does anything here beat exact reader-seeded refinement plus a Gray–Wyner codec once C training is added?** ER3-10 and ER3-27 are the bars. The node's claim to primitives rests on C-time behaviour: tombstones and ghost gradients (ER3-04/05), stale-fiber unmerging (ER3-18), and fiber reuse (ER3-22). Offline exactness is already solved.
4. **Is a vocabulary a contract between a model and its readers?** If ER3-15's interfaces and ER3-19's expand/contract work, alphabet edits in a continual learner can be managed like API migrations: readers publish what they distinguish, and the alphabet may change freely inside that. ER3-03's authority fiber is the security instance: a model where "who wrote this delimiter" is visible only to the one head allowed to act on it.

---

[endpoint]: https://arxiv.org/abs/2608.06386
[mealy]: https://arxiv.org/abs/2405.08647
[quotientcode]: https://arxiv.org/abs/2611.21096
[graywyner]: https://arxiv.org/abs/2601.21424
[samebytes]: https://arxiv.org/abs/2609.35932
[nameless]: https://arxiv.org/abs/2609.16984
[prunedbpe]: https://arxiv.org/abs/2608.00837
[lossless]: https://arxiv.org/abs/2510.08102
[tokdrift]: https://arxiv.org/abs/2510.14972
[seld]: https://arxiv.org/abs/2611.12903
[sstdelay]: https://arxiv.org/abs/2205.04287
[canonical]: https://arxiv.org/abs/2506.07956
[brokentokens]: https://arxiv.org/abs/2506.19004
[partialtoken]: https://arxiv.org/abs/2601.23223
[klod]: https://arxiv.org/abs/2608.27839
[alphaedit]: https://arxiv.org/abs/2410.02355
[partialbisim]: https://arxiv.org/abs/1207.2462
[sstmin]: https://arxiv.org/abs/2605.11190
[retoksym]: https://arxiv.org/abs/2606.15521
[editlocality]: https://arxiv.org/abs/2601.17343
[litetoken]: https://arxiv.org/abs/2602.04706
[escd]: https://arxiv.org/abs/2609.34738
[dvlm]: https://arxiv.org/abs/2609.33816
[fiber]: https://arxiv.org/abs/2608.15976
[paigetarjan]: https://doi.org/10.1137/0216062
