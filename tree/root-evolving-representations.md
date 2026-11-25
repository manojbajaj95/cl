# Root: Evolving representations

Root node (depth 0) · 32 candidate primitives · Ideas only; no experiments run

**Thesis.** A lifelong learner should be able to change the things it computes *with*: what counts as one symbol, which variables exist, what an edge carries, and which operations its internal language can express. The hard case is not adding a component. It is moving old skills onto a changed execution substrate, deleting the old substrate, and learning something there that would have been expensive or inexpressible before.

**Boundary.** The [reviewer ledger][ledger] already killed frozen-backbone skill embeddings as prompt-pool CL plus Toolken, and flags replay, append-and-retrieve, and exact restore as cheap explanations. The [flood triage][triage] also separates [Interface-change][interface]'s normalization and growth controls from [Self-invented vocabulary][coinage]'s public coinage and construction induction. This root is about replacing computation, not adding names. No card is about optimizer state, plasticity budgets, audit or meter design, inference-time weight edits, weightless substitutes, or teams of agents. A split must permit genuinely different successors; a merge must remove something; a rewrite must move old computation, not just rename it. The proposer sees only the arriving stream and the current model. Task boundaries below are for the evaluator, not a task-ID input to the learner.

**First-test contract.** Each CPU sketch stages A → B → C: fit A, induce and apply the rewrite from B, then learn a fresh C using the rewritten object. Score A immediately after the rewrite and after C, on raw inputs held out from the proposer; score B again after C. Old behavior means the old task's public semantics, not old hidden vectors or token IDs. Require exact agreement where the fixture is finite and deterministic, or specify a tolerance before fitting; task metrics are per-family, not averages that hide a broken family. No original object, frozen old head, or extra labelled replay for the candidate. Equalize total stored bits (including conversion tables, learned rules and residuals), examples and allowed search; count rewrite work and steady-state steps separately. Use the card's named control plus a fixed structure and an append-and-freeze ceiling where meaningful. Handwritten rewrites can establish feasibility in the cheapest fixture but not learnability: run the same fixture with decoys and require the learner to select or synthesize the rewrite from B before counting it as a result.

**Literature check.** AlphaXiv searches covered dynamic architecture, token retirement, continual representation learning and library refactoring. The strongest collisions were checked in the primary texts: [Lossless Vocabulary Reduction, §3][lossless] already transports a text distribution to a sub-vocabulary at inference; [In-Place Tokenizer Expansion, §2][inplace] holds old merges fixed and appends new ones; [FlowGenesis][flow] and [SoftModel][soft] already grow live structure; [MoRe][more] already aligns, reuses and expands identifiable modules; [Representational Empowerment][empower] already edits a world model in place; [Programmatic Skill Networks, §2.5][psn] already substitutes calls, merges and synthesizes common abstractions online. The cards below claim narrower differences against these and the cited comparators, not priority. If a matched implementation of the prior art produces the same object and benefit, drop the card.

## I. Rewrite the alphabet

### ER01 · Compile a token out of the model, not out of the sampler

- **Mechanism:** A retirement operator maps both the old emission machine and its live state to a smaller one over the new alphabet. Merge distinct partial parses only when their conditional laws over *all* future bytes (including stop) agree; otherwise the unresolved distinction stays in the new state and is charged. Delete the old token row and old transition path.
- **Literature delta:** [Lossless Vocabulary Reduction][lossless] induces the sub-vocabulary sequence distribution using the original LM. The claim here is that a learned quotient can materialize that law as a smaller successor that runs without the original LM; not that the law can be mapped.
- **Cheapest first test:** Learn a rational weighted automaton over `a, b, ab`; stop using `ab` in B, learn an `aba` transition in C. Compare exact reduction, minimization and their stack. Include a decoy whose parses agree on the next byte but disagree two bytes later.
- **Old-task retention:** Compare every old state’s byte-prefix mass and stop probability for the fixture's bounded horizon, both after deletion and after learning C.

### ER02 · Turn a spelling class into a composable token operator

- **Mechanism:** Replace the rows for an inflected family by a stem and a learned *executable* spelling transform. Transform composition becomes available as an operation in the model; overlapping transformations can demand a new composition rule rather than another surface row. Retire the old rows from both input and output.
- **Literature delta:** [The Functionalizer][functionalizer] already reversibly factors orthographic variation; [Self-invented vocabulary, card 15][coinage] proposes productive affixes from interventions. The narrower candidate replaces the model's spelling operations with a learned *composition law* that predicts unseen orderings of already learned transformations.
- **Cheapest first test:** Use a 24-word invented grammar with one suffix that changes consonants only under negation and a second transform that removes that trigger. Retire surface rows in B; predict a held-out composition order on new stems in C. Compare lossless formatting factors, productive affix induction plus a small transducer, and continued BPE.
- **Old-task retention:** Exact spelling and interpretation on held-out old stems, including the forms that do *not* alternate and old compositions whose ordering matters.

### ER03 · Change alphabets halfway through a symbol

- **Mechanism:** A boundary-state translation migrates a running stream from lexer/decoder pair A to pair B *inside* an unfinished symbol. Its live object is a distribution over the unread suffix and destination states, not just the emitted bytes. No replay of the consumed prefix and no old lexer or decoder calls after handoff.
- **Literature delta:** [Segmental BabyLMs][segmental] learn over alternative segmentations; [Lossless Vocabulary Reduction][lossless] supplies the textual law. The extra operation is destructive migration of an in-flight decoder with delayed parse commitments, bounded state and no reprocessing.
- **Cheapest first test:** Switch on each character of a branching `ab/ac` grammar, then learn a token sharing the `a` prefix. Compare restart-on-boundary, exact reduction with the old machine kept and a compiled product transducer. A pair of histories with the same printed prefix but opposite suffix mass is the negative.
- **Old-task retention:** Match completion and stopping distributions conditional on each old mid-symbol state, not just on a clean new request.

### ER04 · Trade a flat vocabulary for a constrained product alphabet

- **Mechanism:** Replace a flat symbol by two typed factors and a legality relation. Split or fuse axes in a later rewrite when new combinations emerge. A factorized logit consists of two additive terms plus only the interactions the learner cannot yet remove; compute the partition function over legal pairs, not all pairs.
- **Literature delta:** [Adaptive softmax][softmax] partitions a fixed target vocabulary; [Vocabulary Expansion and Initialization][expansion] and [Interface-change][interface] already deal with the old softmax changing. The candidate is a mutable factorization that deletes rows and creates novel legal symbols by changing a factor or compatibility relation, not normalizer matching.
- **Cheapest first test:** Fit a 4 × 4 alphabet with three illegal pairs and one exceptional interaction; discover factors from B and expose new legal pairs in C. Compare a static masked factor head, adaptive softmax and a flat head at matched bits; independent factors should fail on the exception.
- **Old-task retention:** Match old conditional probabilities in contexts whose legality set did not change; in expanded contexts match the normalized distribution conditional on the original legal alternatives.

### ER05 · Give a token an internal address space

- **Mechanism:** Promote spans into variable-length symbols with typed address ports. Old position-sensitive instructions migrate to offset arithmetic on the ports: composing two spans adds offset lengths; selected internal anchors remain routable without expanding every byte.
- **Literature delta:** [Byte Latent Transformer][blt] already groups bytes into dynamic patches; [Interface-change, card 3][interface] proposes tokens that memoize computation. Here the changing patch structure must transport *addressable operations* through offset ports, not emulate a span's cached final output.
- **Cheapest first test:** Ask for quoted-field lengths and the byte before a separator in synthetic records. Merge variable-length fields in B; learn nested fields in C. Compare BLT-style patching with a local decoder and a conventional span-index data structure at equal memory and touches.
- **Old-task retention:** Return exact bytes and offsets for old records with repeated separators and length ties, including a query spanning two new tokens.

### ER06 · Learn which grammar owns a token boundary

- **Mechanism:** A lexicon entry belongs to a scope entered and left by a learned transducer, not to a global vocabulary or a document-level language ID. A scope may hand a half-built lexical unit across its boundary as a typed continuation; identical spellings in separately owned scopes need not share an embedding or action. Rewrite and retire duplicated local entries.
- **Literature delta:** [Modular Tokenizers][modtok] already assigns language-specific tokenizers; [Dynamic Tokenization][dynamic] can retrofit embeddings for changing tokenizers. The candidate requires growing *composable ownership and handoff* rules within one sequence and migrating old boundary computation.
- **Cheapest first test:** Use mixed code/prose with a nested interpolation and adversarial identical delimiters; derive one handoff from B and reuse it at a previously unseen nesting depth in C. Compare language routing plus a fixed lexer stack, including a stack granted the same grammar rules.
- **Old-task retention:** Recover old spans and execute old code/prose disambiguation at both sides of a handoff; count errors on escaped delimiters separately.

### ER07 · Learn a token with unbounded arguments

- **Mechanism:** A gapped lexical unit is an executable constructor with typed, length-variable holes. It replaces the wrapper symbols around its arguments, while repeated holes share one binding, not a fixed subword embedding. Introduce a hole equality only where the learned constructor keeps the old argument semantics.
- **Literature delta:** [Split Trees][split] alter segmentation, [Stitch][stitch] abstracts arguments from programs, and [Self-invented vocabulary, card 16][coinage] opens slots in fixed expressions. Here a symbol can bind *multiple nonadjacent uses of the same unbounded argument* on the input stream and replace the wrapper's old computation, not just accept a new operand.
- **Cheapest first test:** In a bracket-and-copy grammar discover the equivalent of `tag(x)…close(x)` from B; apply it to longer, unseen nested arguments in C. Compare Stitch followed by a fixed tokenizer and a byte model with copy, both under the same execution budget.
- **Old-task retention:** Exact expansion and parsing on old held-out nested strings, including a mismatched tag pair that a naive macro would wrongly accept.

### ER08 · Replace literal names with binding instructions

- **Mechanism:** Turn repeated identifiers into `bind`, `refer` and `rebind` symbols with scope-relative operands. Rewrite the model's existing reference consumers to use lexical distance or binding identity, not surface equality. Name spelling is retained only at the public rendering boundary; delete per-name learned rows.
- **Literature delta:** [De Bruijn indices][debruijn] already solve representation of bound variables; [Dynamic Tokenization][dynamic] changes input embeddings. The testable claim is discovery of which names actually bind (versus are literal) from a task stream, and lifetime migration of their consumers without a hand-supplied binding grammar.
- **Cheapest first test:** Learn commands with nested variable shadowing plus literal room names. B introduces alpha-renamed commands; C introduces a new shadowing operator. Compare a static binding compiler, byte model and move-to-slots without scopes; train and charge the grammar search.
- **Old-task retention:** Resolve held-out references with shadowing, and ensure that replacing an old literal room name still changes the answer.

## II. Rewrite the latent state

### ER09 · Transplant a coordinate axis

- **Mechanism:** Replace a joint latent index by a product of two independently composable axes and a sparse table of irreducible interactions. Rewrite existing decoders in those coordinates and eliminate the original index; later swap one axis for a strictly richer one without refitting the other.
- **Literature delta:** [MoRe][more] identifies and reuses fundamental modules, while [Continual Nonlinear Independent Representations][ica] addresses identifiable factors under changing environments. Here a previously executable joint latent type is actually retired; the delta is concurrent transport of consumers and expansion into previously nonexistent combinations.
- **Cheapest first test:** Start with a joint 2 × 3 latent table, one interaction and two heads. Expose new recombinations in B, a third value on one axis in C. Compare fixed identifiable factors, lookup expansion and joint refactor with no portable residual.
- **Old-task retention:** Both heads must keep old conditional answers on withheld triples, especially the genuine interaction that pure independence discards.

### ER10 · Replace global coordinates with a learned atlas

- **Mechanism:** Replace global axes with local charts linked by learned changes of frame. Rewrite old computations at these interfaces and split or glue charts as new views arrive. Coordinate re-expression around a loop must agree; transport of a physical state around a loop need not, and uses separate operators so that a real rotation is not erased.
- **Literature delta:** [Gauge-equivariant CNNs][gauge] already transport features between local frames; [Motion Equivariant ConvLSTM][motion] uses moving gauges. The claimed object is a learned, mutable chart cover with destructive chart split/join that maintains existing functions through the overlap maps.
- **Cheapest first test:** Fit three toy cameras that overlap only pairwise; B forces a new chart split, C adds a fourth camera. Compare learned global alignment, a fixed gauge network and an atlas with oracle seams. Include an inconsistent overlap cycle.
- **Old-task retention:** Reproduce old local bearings and all previously supported multi-camera compositions, including traversing an overlap in both directions.

### ER11 · Split a state by the effect of an action

- **Mechanism:** Refine a learned state equivalence class only along the action that breaks it. A new action-indexed fiber stores the lost distinction for that action; old actions still consume the quotient. Permit recombination of the fiber with a different base state without creating a fully split copy of the world model.
- **Literature delta:** [MDP model minimization][mdp] already partitions states by transition and reward equivalence; [Representational Empowerment][empower] already edits transition tables and refactors concepts by intervention gain. The claim is a *partially refined type* with executable action fibers that can be moved across base states, not discovery of the usual refined partition.
- **Cheapest first test:** Two aliased rooms have the same navigation but different reset outcomes. Learn the reset fiber in B; reuse it with a new navigation graph in C. Compare full partition refinement, an action-conditioned factored model and their equal-size stack.
- **Old-task retention:** Check old navigation rollouts from both reset outcomes over every old action sequence of length ≤ 4, not merely the original starts.

### ER12 · Add order without giving up the bag

- **Mechanism:** Change a latent bag into a bag plus antisymmetric pair counts on just the pairs whose order starts to matter. An old bag reader is compiled into the symmetric part; adding a new order-dependent reader does not allocate a full positional sequence. Drop pair coordinates that become equivalent under the newly learned relations.
- **Literature delta:** [Deep Sets][deepsets] establishes invariant set aggregation; [Order Matters][order] studies learning orders for set/sequence prediction. The proposed edit changes the symmetry of a *live* type in selected directions and migrates old consumers, rather than choosing an ordered encoder from the start.
- **Cheapest first test:** A sums a bag; B distinguishes `ab` from `ba`; C distinguishes just `bc` from `cb`. Compare an always-ordered model, bag plus sparse order bits and the corresponding full pair-count encoding. Include long inputs where pair counts are not enough to reconstruct order.
- **Old-task retention:** Check all old bag answers under every permutation of the old examples, not only the order seen in training.

### ER13 · Promote a relation to an object

- **Mechanism:** Reify a relation (such as a contact) as a latent object with identity, attributes and its own update rule. Redirect old pairwise queries and writes through that object, using a learned rule for ambiguous writes; retire the pairwise parameter table.
- **Literature delta:** [Neural Module Networks][nmn] compose modules over object/relation tasks; [relational lenses][lens] already provide bidirectional view updates. The proposed operation learns *when a relation needs enduring identity* and changes the model's currently executable update semantics with no supplied target schema.
- **Cheapest first test:** Repeated contacts in a toy graph gain independent ages in B and share a reset operation in C. Compare an oracle relational schema, a learned link-state tensor and a standard lens with the same learned mapping.
- **Old-task retention:** After old-style add/remove/query traces, return the same adjacency and counts for parallel edges and missing pairs.

### ER14 · Turn a confound into something the model can intervene on

- **Mechanism:** Split a variable fitted from passive data into an endogenous source and an external selector when new interventions distinguish them. Replace the old predictor with the new causal factorization; its passive branch integrates out the selector rather than consulting a frozen observational head.
- **Literature delta:** [Causal Representation Learning][causalrep] motivates latent causal variables, and [Causal Abstractions][causalabs] tests intervention-preserving relations. The claim is a lifecycle edit that derives a *new writable causal port*, with the old marginal realized by the new factorization after deleting the old variable.
- **Cheapest first test:** Fit two observationally equivalent binary models on A. Break the tie with one intervention family in B, then test an untrained cross-intervention in C. Compare fixed causal structure search with online refit at matched data; with no distinguishing intervention the learner must not infer a unique split.
- **Old-task retention:** Reproduce the full passive joint table on old mixtures, including a rare cell where the two marginals can otherwise appear to tie.

### ER15 · Grow a tree representation into a space with loops

- **Mechanism:** Store path-dependent state as a spanning tree plus independent cycle coordinates. When the stream exposes a new loop, add the necessary coordinate and rebase path operators; when an edge disappears, move retained cycle coordinates to a new basis rather than rebuilding old paths.
- **Literature delta:** Cycle bases and Hodge decomposition already factor fixed graphs; [Graph Neural Networks][gnn] learn graph functions. The difference to test is a changing latent *topology and basis* with shared executable path operators, not using cycle features on one known graph.
- **Cheapest first test:** Learn travel costs on a tree, then observe a loop with nonzero signed circulation and replace one tree edge. Compare online cycle maintenance plus the same decoder, a fixed-tree embedding and a graph model. The zero-circulation case should need no added coordinate.
- **Old-task retention:** Match costs of old surviving directed paths, reversed paths and their concatenations both before and after changing the spanning tree.

### ER16 · Merge quantized codes but keep a reusable residual operation

- **Mechanism:** Merge two latent codes into a common code plus a typed residual direction. Old linear readers become sums of code and residual contributions. A later split can assign that *same learned residual operation* to another parent rather than restoring either retired code.
- **Literature delta:** [VQ-VAE][vq] learns a discrete codebook; product and residual quantization already compose discrete codes. The only prospective delta is mutable code typing with consumer transport and transferable residuals that survive repeated deletion of old code entries.
- **Cheapest first test:** Compress two displaced clusters used by two different readers, then move the same displacement to a third cluster. Compare online residual quantization with the same learned reader migration and a static product quantizer. Include a nonlinear reader that does not admit the residual split.
- **Old-task retention:** Exhaustively compare old reader outputs on projected points around both deleted codes, especially across the old decision boundary.

## III. Rewrite the execution graph

### ER17 · Give a noncommuting pair a shared circuit

- **Mechanism:** Replace duplicated branches for `AB` and `BA` by one canonical branch and a reusable commutator edge. The second order reads the canonical composition plus the signed correction. Share or delete that correction only when the learner finds a lower-dimensional rule for it.
- **Literature delta:** [Network Morphism][morph] already preserves functions during graph edits; [egg][egg] already rewrites algebraic terms. The candidate is a *learned correction edge that introduces a reusable family of order-sensitive circuits*. Factoring `BA − AB` once is not a result if ordinary shared `A, B` or algebraic optimization ties it.
- **Cheapest first test:** Fit small linear blocks whose order differences are rank one; induce the correction port from B and predict a held-out three-block composition in C. Compare weight sharing plus algebraic simplification, and include full-rank commutators as a failure case.
- **Old-task retention:** Check both old orders on basis and held-out mixture inputs after deleting the old branch and after C.

### ER18 · Turn learned depth into an extensible loop

- **Mechanism:** Replace an untied stack by one transition on `(latent, phase)`. Fit a compact phase evolution that reproduces the old layer effects; delete the stack. New tasks learn stopping or continuation *in that loop* rather than adding layers or treating phase as an index into saved weights.
- **Literature delta:** [Recurrent Depth][recurrent] and [Universal Transformers][ut] start with tied recurrence; [Library of Layers][layers] starts with a reusable block library. The delta is inferring a recurrent factorization from an incumbent untied model and carrying its already learned depth-dependent skills into that loop.
- **Cheapest first test:** Three independently fitted linear stages implement rotating shear; learn a two-coordinate phase and one step family from B, then learn four- and five-step compositions in C. Compare an always-recurrent model and phase lookup/conventional recurrent distillation. Reject a phase table as large as the stack.
- **Old-task retention:** Match old end outputs and an old public early-exit task at its original stopping point on unseen inputs.

### ER19 · Make edge width depend on the value's type

- **Mechanism:** Replace a dense edge by a sum of narrow, type-selected payloads with separately shaped consumers. Learn a partition of reachable inputs on which a narrow transport suffices; allocate a wider payload only for a new type that needs it. Old consumers are moved onto the narrow payloads, not redirected to a saved dense edge.
- **Literature delta:** [Net2Net][net2net] and [Network Morphism][morph] alter layer shape; [Dynamic Expandable Networks][den] already split or expand capacity. Here the learner changes a shared edge's *value type and shape* and can later refine the type itself, not just route to another module.
- **Cheapest first test:** Two interleaved domains use rank-one projections along distinct axes; a third needs rank two. Rewrite a rank-two trunk to ragged ports and learn the third domain. Compare fixed-rank shared projections and a matched routed mixture, including the cost of deriving the type.
- **Old-task retention:** Both old projection tasks must work on held-out inputs near and across the learned type boundary, without an oracle route.

### ER20 · Move a computation across a clock boundary

- **Mechanism:** Move a computation and its state between stages of a persistent graph. An edge's learned delay is part of its type. Transport the in-flight values and swap the locations of computation and storage while preserving outputs at each *public* tick; the new graph can make use of an input that arrived after the old stage ran.
- **Literature delta:** [Classical circuit retiming][retiming] already redistributes registers without changing behavior; [SoftModel][soft] adds cyclic computation. The claim is that a stream-discovered delayed factorization permits joint retiming and an additional learned computation without a second pipeline. Ordinary retiming plus a new stage is the control, not the contribution.
- **Cheapest first test:** A two-stage streaming linear predictor learns a late-arriving feature in B; search small stage relocations and compare retiming plus a late fusion head at matched bits and latency. Retire the old intermediate buffer before C alternates both modes.
- **Old-task retention:** Compare exact output timestamps and values after a switch at every reachable pipe occupancy, including the first and last ticks.

### ER21 · Fuse live dynamical modules through one realization

- **Mechanism:** Replace independently trained recurrent modules by a joint state realization plus old readout maps. Compute a many-to-one map on the *current states* before deleting both originals, and assign future tasks ports on that shared state. No historical input sequence is required at migration.
- **Literature delta:** [Ho–Kalman][hokalman] already constructs minimal linear realizations, and [Structured State Spaces][s4] parameterizes a shared recurrence. The candidate must beat minimal realization plus online refit by giving the next task a reusable state interface discovered during repeated migrations; simply finding a smaller linear realization is known.
- **Cheapest first test:** Fit two small linear filters that accidentally learn the same hidden pole. Fuse with their states nonzero; next teach a third filter that shares the pole but uses a new input. Compare classical minimal realization, independently fitted filters and the same-budget stack.
- **Old-task retention:** Feed adversarial suffixes after unequal prefixes and require both old output streams to match, including the first read after fusion. A duplicated but *independently driven* pole is the negative.

### ER22 · Replace serial execution with a learned segment algebra

- **Mechanism:** Find a compact, closed segment representation and a learned associative combination. Replace a step-by-step graph with a scan of summaries that can be reused at new lengths or segmentations. Preserve prefix outputs by making the summaries composable at every possible cut, not just whole sequences.
- **Literature delta:** [Mamba][mamba] uses a selective scan; [ScanWeaver][scan] lowers affine recurrences to associative scans. This candidate changes the live graph by discovering a useful summary type for a previously unfactorized operation; if ordinary scan lowering already finds it under matched information, stop.
- **Cheapest first test:** Discover stable transition summaries for sequences of small saturating integer functions and use them on longer C inputs. Baselines: an exhaustive transition-table monoid, hand-lowered scan and unchanged serial execution. Charge the representation needed to encode each distinct function.
- **Old-task retention:** Compare every old prefix read across every parenthesization in the finite fixture, including inputs that hit saturation.

### ER23 · Tie a graph into symmetry orbits, then grow an exception

- **Mechanism:** Infer transformations under which currently distinct kernels implement the same operation. Collapse their parameter tensors into one orbit kernel and explicit symmetry actions; later refine selected orbits into suborbits when a new task breaks the symmetry. Delete old copies rather than masking them.
- **Literature delta:** [Learned weight-sharing symmetries][symmetry] and [Approximate Equivariance][approx] already learn or relax symmetry. The lifecycle claim is about destructive orbit collapse and *selective re-expansion* with previously deployed readouts moved to the same kernel.
- **Cheapest first test:** Begin with independent kernels for all four grid rotations, learn the invariant action in B and one direction-specific exception in C. Compare learned soft tying, a fixed equivariant layer and an equivalent orbit-plus-residual stack; count the physical parameters and tensor accesses.
- **Old-task retention:** Keep all old kernels' input–output maps, including mixtures of rotations and old tasks that were never rotation-invariant.

### ER24 · Change a dense update into an event machine

- **Mechanism:** Replace dense recomputation by a learned state-transition interface with typed events such as add, delete and threshold crossing. Internal operators consume those events and store just enough current state to produce exact public values. A C task can learn a new event transition without expanding the original dense input path.
- **Literature delta:** [Delta Networks][delta] already exploit temporal sparsity in recurrent updates; the proposed rewrite lets new *semantic event types* alter active graph topology and old consumers continue on the new event interface. Merely thresholding dense deltas is known.
- **Cheapest first test:** Start with a small weighted sum followed by ReLU, learn insert/remove events in B, then one group-move event in C. Compare a generic incremental evaluator given the same operators and a conventional delta network. Charge all retained accumulators and event conversion.
- **Old-task retention:** Reproduce old readouts after every event, particularly when insert and delete cancel or one event crosses the old ReLU threshold.

## IV. Rewrite the executable language

The learner here is a small program-inducing model with an internal language. These are changes to that model's own grammar, interpreter or calling convention, not additions to an agent's retrieval store.

### ER25 · Lift a hidden dependency into a lexical argument

- **Mechanism:** Promote a value read through a hidden environment dependency to a typed argument; change both the learned callee and its callers. Old uses pass the value they previously captured. C can compose the same operation with a novel provider that the old program could not name.
- **Literature delta:** Closure conversion and parameter extraction are known, and [Leroy][leroy] already synthesizes reusable imperative abstractions. The candidate is learning, from arriving tasks, which *semantic dependency* to promote even when the callers obtain it through different computations. Syntactic capture lifting alone is a control.
- **Cheapest first test:** Two old programs convert measurements with implicit scales obtained in different ways. B varies scale independently; C supplies a third scale provider and composes both routines. Compare closure conversion, Stitch and a static explicit-argument DSL with matched search.
- **Old-task retention:** Run old programs with held-out scale and aliasing cases; require the same values and side effects after discarding the captured versions.

### ER26 · Split one return value into a correlated bundle

- **Mechanism:** Give a learned primitive a multi-port result with a joint relationship among the ports. Transport old consumers to projections of this result. C can combine ports without the independent re-evaluation that previously broke their coupling; retire the separately evaluated routines.
- **Literature delta:** [Stitch][stitch] and [PSN][psn] already discover common subroutines and merge callers. The delta is invention and adoption of a *joint result type with a coupling*, not deduplicating identical code that happens to return a tuple.
- **Cheapest first test:** In a finite stochastic DSL, two old routines sample different projections of one latent draw. B identifies their coupling; C needs both together. Compare product outputs, typed anti-unification, and common-subroutine extraction with shared-seed threading.
- **Old-task retention:** Preserve the individual distributions and the independence of historically separate calls. Sharing one draw across all calls fails even if the new paired task passes.

### ER27 · Invent a relation that can be executed in different directions

- **Mechanism:** Replace two asymmetric procedures by an executable relation with learned admissible input/output modes. Retire the old procedure definitions; old callers fix the same arguments as before. A new caller can bind a different set and obtain a finite set of completions, not an arbitrarily chosen inverse.
- **Literature delta:** [Bidirectional Program Search][bidirectional] uses forward and inverse execution in synthesis; functional-to-relational compilation and [lenses][lens] are established. The claim is induction of the *shared relation and its modes* from separate old programs plus B, not automatically reversing a given DSL primitive.
- **Cheapest first test:** Learn two procedures on modular arithmetic with non-injective operations; synthesize and induce a missing mode from B; in C solve congruence queries binding a new pair of arguments. Compare enumeration over old procedures, a general relational interpreter with the same search, and relational compilation plus mode inference.
- **Old-task retention:** Match all old deterministic results and failures, including non-unique inverse cases that the old policy resolved by a stated tie rule.

### ER28 · Learn a reduction law, then make it part of the language

- **Mechanism:** Promote a recurring equality between *existing learned operations* to an executable reduction rule in the model's grammar. Its guard is a typed argument pattern, and existing programs are rewritten through it; retire obsolete productions when the guarded reductions cover them. Next-stage synthesis enumerates reduced programs directly.
- **Literature delta:** [Equality-saturation theory exploration][ruler] already learns rewrite rules, and [DreamCoder][dream] already grows a synthesis grammar. The difference to test is whether rewriting the lifelong learner's production grammar and already executable artifacts together buys a real search gain over rule inference plus library learning.
- **Cheapest first test:** Induce one conditional identity for finite bitvector programs, delete a redundant production on the supported types, and solve deeper C tasks. Compare equality saturation plus library learning with the same candidate equations and search; include a near-identity that fails at a boundary value.
- **Old-task retention:** Run every old program on the exhaustively enumerable old types, including the boundary case and any guard-false caller.

### ER29 · Turn a return into a continuation

- **Mechanism:** Allow a learned instruction to yield a reusable continuation instead of only a final value. Rewrite the old caller to exhaust the continuation, but allow C callers to interleave two live continuations or compose one with a newly learned instruction. The old implementation is removed.
- **Literature delta:** [Continuation-passing style][cps] already makes control flow explicit; [PSN][psn] refactors executable skills online. The candidate's delta is discovering the suspension points and minimal resumable state from a stream, so that two formerly opaque learned computations can cooperate at an internal boundary.
- **Cheapest first test:** Two finite parsers currently return a final answer. B introduces a paired stream that needs alternating prefixes; C interleaves with a third parser. Compare an off-the-shelf coroutine conversion given identical suspension points, plus a direct joint parser and CPS search at the same budget.
- **Old-task retention:** Run old parsers to completion on held-out accepted and rejected strings; verify the same output order and error position without the old interpreter entry points.

### ER30 · Change the meaning of an effect independently of its callers

- **Mechanism:** Extract a repeatedly learned state-change pattern into a named effect with a typed handler. Replace direct state mutation in older routines by the effect, and migrate their prior handler behavior to a common implementation. C learns a different handler that can be scoped inside a new program without copying the routines.
- **Literature delta:** [Algebraic effect handlers][handlers] already supply this execution model; [Leroy][leroy] abstracts imperative programs. The conjecture is that a learner can infer the *effect boundary and semantic equivalence of different concrete updates* and make the new handler available as a learned operation, not merely apply a known effect system.
- **Cheapest first test:** Two tiny programs update a counter and a ledger via dissimilar code. B makes the updates reversible under a shared handler; C composes them under nested scoping. Compare effect inference with ordinary library abstraction and an oracle handler language, at matched program-search work.
- **Old-task retention:** Exhaustively match old traces and final state with the default handler, including exceptions and nested calls.

### ER31 · Fuse two interpreters by learning what they can share

- **Mechanism:** Replace independent programs that walk the same input with a product interpreter. A learned sharing rule identifies which intermediate computations can run once while each program keeps only its irreducible local state. Extend that product with another interpretation instead of re-running the input or storing it.
- **Literature delta:** [Deforestation][fusion] and product constructions already share traversals; [PSN][psn] already extracts common subskills. This card needs a *semantic shared-state factorization* of interacting walkers learned from B, not simply zipping two loops with syntactically identical bodies.
- **Cheapest first test:** Fuse two finite text recognizers with different state layouts but a common quote-state machine, then add a third recognizer in C. Compare ordinary automaton product plus minimization, and deforestation over equivalent implementations at equal state and synthesis budget.
- **Old-task retention:** Match the arrival time and content of both old output streams on every short input including escapes; shared state must not leak a recognizer's private mode.

### ER32 · Make a rewrite reusable as a typed architecture operation

- **Mechanism:** When the learner derives two successful concrete migrations, abstract the migrations themselves into a typed rewrite operator: it introduces the new representation, transforms incident operators, and lowers unsupported cases without the old graph. Apply it to a new graph with the same boundary *structure* but different parameters and arity.
- **Literature delta:** [Network Morphism][morph] supplies reusable transformations; [Circuit Condensation][condensation] shrinks a learned behavior's circuit; [Stitch][stitch] abstracts terms. The delta is abstraction over *live model-migration programs*, including the state map and the rewrites of consumers, learned during the lifetime instead of supplied as a fixed edit menu.
- **Cheapest first test:** Let the model solve two toy port factorizations end to end, then induce a migration operator and run it on a held-out three-port graph. Compare a fixed morphism menu, anti-unification of transformation traces, and unrestricted direct migration. Require an instance where anti-unifying just the final graphs gives the wrong live state.
- **Old-task retention:** After the inferred migration and a new C fit, compare outputs on old calls beginning from each reachable in-flight state, not only from initialization.

## Ranked deeper questions

1. **What is the smallest state that can survive true retirement?** Start with ER01/03. Is continuation equivalence sufficient for practical migration once conditioning includes an unfinished output, and how does the smallest successor scale with ambiguous prefixes? Derive both a strict separation from inference-only reduction and a family that provably requires keeping the old distinctions. If the exact composed and minimized machine always ties, there is no new compiler primitive here.
2. **When does factoring a learned distinction buy future expressivity rather than bookkeeping?** Start with ER09/11/14. Construct two worlds with the same old behavior, one where a distinction transfers across bases and one where it does not. Ask what B evidence suffices to learn the reusable factor and whether it buys a C sample or representation advantage over full partition refinement plus shared factors.
3. **Can one architecture remember several histories after its physical computation changes?** Start with ER18/20/21. Separate matching maps from zero state, matching every live state, and learning efficiently after transport. Seek a strict frontier over classical realization plus incremental refit, not a function-preserving initialization result.
4. **Can the learner invent an edit it can later reuse?** Start with ER25/28/32. Compare a typed state-and-caller migration operator with a fixed library of graph morphisms plus an abstraction learner. Generalization must cross a new arity or representation type while excluding a well-typed counterexample; speedup on repetitions of the original rewrite does not count.
5. **Can the alphabet and the executable model evolve on different clocks?** Start with ER04/07/26. Alternate changes to spelling, binding and computation; ask whether independently valid rewrites commute on old semantics or whether only joint migration fits the lifetime budget. Compare the best independent token and graph rewrite stack, and include a no-interaction case where it ought to tie.

[ledger]: https://github.com/manojbajaj95/cl/blob/6a91cc5e9e1c63f45f3336bb02e550b9a625387e/reviews/idea-ledger.md
[triage]: https://github.com/manojbajaj95/cl/blob/6a91cc5e9e1c63f45f3336bb02e550b9a625387e/reviews/flood-triage.md
[interface]: https://github.com/manojbajaj95/cl/pull/115
[coinage]: https://github.com/manojbajaj95/cl/pull/128
[lossless]: https://arxiv.org/abs/2510.08102
[inplace]: https://arxiv.org/abs/2607.15232
[flow]: https://arxiv.org/abs/2610.35108
[soft]: https://arxiv.org/abs/2608.16409
[more]: https://arxiv.org/abs/2605.14364
[empower]: https://arxiv.org/abs/2609.02322
[psn]: https://arxiv.org/abs/2601.03509
[functionalizer]: https://arxiv.org/abs/2609.15991
[segmental]: https://arxiv.org/abs/2609.01151
[softmax]: https://proceedings.mlr.press/v70/grave17a.html
[blt]: https://arxiv.org/abs/2412.09871
[modtok]: https://arxiv.org/abs/2609.15528
[dynamic]: https://arxiv.org/abs/2411.18553
[split]: https://arxiv.org/abs/2605.22705
[stitch]: https://arxiv.org/abs/2211.16605
[ica]: https://arxiv.org/abs/2408.05788
[gauge]: https://arxiv.org/abs/1902.04615
[motion]: https://arxiv.org/abs/2610.28771
[deepsets]: https://arxiv.org/abs/1703.06114
[order]: https://arxiv.org/abs/1511.06391
[nmn]: https://arxiv.org/abs/1511.02799
[causalrep]: https://arxiv.org/abs/2102.11107
[causalabs]: https://arxiv.org/abs/2106.02997
[gnn]: https://arxiv.org/abs/1810.00826
[vq]: https://arxiv.org/abs/1711.00937
[morph]: https://arxiv.org/abs/1603.01670
[egg]: https://arxiv.org/abs/2004.03082
[ut]: https://arxiv.org/abs/1807.03819
[recurrent]: https://arxiv.org/abs/2502.05171
[net2net]: https://arxiv.org/abs/1511.05641
[den]: https://arxiv.org/abs/1708.01547
[s4]: https://arxiv.org/abs/2111.00396
[mamba]: https://arxiv.org/abs/2312.00752
[scan]: https://arxiv.org/abs/2606.00601
[symmetry]: https://arxiv.org/abs/2412.04594
[approx]: https://arxiv.org/abs/2409.11772
[leroy]: https://arxiv.org/abs/2410.06438
[bidirectional]: https://arxiv.org/abs/2110.11536
[ruler]: https://arxiv.org/abs/2609.14527
[dream]: https://arxiv.org/abs/2006.08381
[debruijn]: https://doi.org/10.1016/1385-7258(72)90034-0
[mdp]: https://doi.org/10.1016/S0004-3702(02)00376-4
[lens]: https://doi.org/10.1145/1142351.1142399
[retiming]: https://doi.org/10.1007/BF01759032
[hokalman]: https://doi.org/10.1524/auto.1966.14.112.545
[delta]: https://proceedings.mlr.press/v70/neil17a.html
[cps]: https://doi.org/10.1145/155090.155113
[handlers]: https://doi.org/10.1007/978-3-642-00590-9_7
[fusion]: https://doi.org/10.1145/224164.224221
[expansion]: https://arxiv.org/abs/2407.05841
[layers]: https://arxiv.org/abs/2611.03526
[condensation]: https://arxiv.org/abs/2608.27254
