# Learning Economics 2: What a Price Does to the Learner

Child of [root-learning-economics.md](root-learning-economics.md) (depth 1) · 27 candidate primitives · Ideas only; no experiments run

**Why this node exists.** The reviewer's triage of the root ([PR #324](https://github.com/manojbajaj95/cl/pull/324), [flood-triage row 442](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md#L442)) promoted two cards to score 3 and called the rest market-design transplants: **LE01**, buy the lesson that ends the supplier's monopoly, and **LE13**, price permitted learning paths instead of datasets. It also set the bar for any child: *these cards change who supplies the learner, not what the learner does, so each must show a learning or retention effect, not only feasible trades.* This node takes that as its thesis. Every card names a quantity measured **inside the learner** (which representation it ends with, which old cases survive, how many ordinary examples a substitute teacher needs, how much order matters) and states how the economic object changes that quantity. A card whose only output is a price, a surplus or a feasible contract is not here.

**The two learning facts this node is built on.**
1. *A general lesson and a set of narrow exceptions leave different learners.* Rule-then-exception and exception-then-rule curricula produce different representations, and rare exceptions can be learned, overregularized away and recovered ([Curriculum unlearning in humans and neural networks, 2611.04565](https://arxiv.org/abs/2611.04565); [The Dynamics of Quasiregular Neural Learning, 2609.26018](https://arxiv.org/abs/2609.26018)). So LE01's buyout does not only end a rent: it decides whether the learner ends with a rule that substitutes can extend, and whether old exceptions survive that rule.
2. *Order changes the endpoint, and the endpoint difference is forgetting.* For tasks A then B versus B then A, forgetting of A is almost exactly the gap in A's loss between the two orders (Spearman 0.96–1.00 on split MNIST/Fashion/CIFAR), set to leading order by the Lie bracket of the two gradient fields ([Does Learning Order Explain Forgetting?, 2611.20087](https://arxiv.org/abs/2611.20087)). So LE13's path price is not cosmetic: two paths with the same set of lessons can differ exactly in retention.

**Constraint inherited from the tree.** LE13 needs "the same learner state". The reviewer notes this is close to top-10 #2, the Nerode quotient of edits ([flood-top10](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-top10.md)). Two results from that line bind every path card below: [PR #104](https://github.com/manojbajaj95/cl/pull/104) shows function-identical states (uv with (u,v)=(1,1) vs (2,½)) diverge after one gradient step, so equivalence cannot be read off current outputs; [PR #108](https://github.com/manojbajaj95/cl/pull/108) predicts classes merge only at singular steps. A path price that certifies "same state" from outputs alone is wrong in the first case and must say so.

## What this node is not

The [idea ledger](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md) was read first. Not proposed again here: ordinary replay or data valuation relabeled as a market; token-bucket or plasticity budgets; static Shapley or influence credit with no learner-state effect; curriculum search alone; meters that only report. Cards that collapse to a known baseline say which one, and the baseline is a required arm. The root's market-design cards LE02–LE12 and LE14–LE32 are cited only where a card here gives them a learning effect.

**Literature check.** Searches (alphaXiv and arXiv/Hugging Face paper search, November 2026) covered machine teaching and teaching dimension, strategic and withholding teachers, data and information pricing, durable-goods / Coasian dynamics for information goods, distillation markets, temporal data valuation, order-dependent forgetting, curriculum and rule/exception learning, and multi-teacher distillation. Each card names the closest mechanism found and the specific gap; "none found" means none in those searches, not a proof of absence.

**Shared first-test protocol (adds to the root's).** Keep the root's protocol: exact enumeration of the smallest separating game, then an ordinary CPU learner; fixed opportunity streams and private seller types across arms; sellers best-respond; matched funds, labels, compute, rights; a central buyer with equal information, rights and commitment as a required rival. Add three learner-side readouts that every card reports **before** any price:
- **Rule share**: fraction of held-out new-task inputs the learner gets right that were never in any purchased lot (generalization from the general lesson).
- **Substitute sample cost**: ordinary examples from a fresh, interchangeable seller needed to reach the target error from the post-lesson state (the learner-side meaning of "the monopoly ended").
- **Order gap**: old-task loss difference between the purchased order and its reverse (or the cheapest reorder), at the same lesson set.

Default learners, all CPU: (i) a rule-plus-exception-table learner (exact); (ii) logistic regression on fixed features; (iii) a one-hidden-layer MLP on a quasiregular task (a dominant rule with rare exceptions, as in 2609.26018); (iv) a two-layer uv factorized linear model to reproduce PR #104's gauge case.

**Old-task check for all cards.** As in the root: pretrain on at least two ordinary old tasks, one rare; introduce the new task; score a fixed held-out old-task mix through normal prediction, with no task IDs or routing, before, during and after the transition and after any switch to a substitute seller. Report per-task retention and the worst drop against a predeclared no-new-learning floor. Here the old mix must also contain **old exceptions to the rule the new lesson installs**, because that is where a general lesson does its damage.

**Two exact fixtures used below.**
- **F-order (for LE13 cards).** Scalar learner w, start w=0. Lesson A: w ← w+1. Lesson B: w ← w/2 (a decay/shrink step). Old-task loss (w−1)². New task passes if w ≥ 0.5. Order A→B ends at w=0.5 (old loss 0.25); B→A ends at w=1 (old loss 0). Both orders buy the same set {A,B} and both pass the new task, so any set-based price treats them as the same purchase, yet only one retains. This is the smallest case where a path price has a retention meaning.
- **F-rule (for LE01 cards).** Inputs x∈{0,…,7}, a rule-plus-exception learner, an old task y=[x≥4] with one rare old exception, and a new task whose rule the incumbent can teach in one general lesson or as per-point exceptions. Entrants sell only ordinary labeled points. The readouts are rule share, substitute sample cost and survival of the old exception after entrants train. The same task run through logistic regression and the MLP shows whether the rule lesson overwrites the old exception in shared weights, which the exact learner hides.

## A · LE01 made into a learning claim: what must a monopoly-ending lesson do to the learner?

### LE2-01 · Contract on the substitute's sample cost, not on delivery of the lesson
- **Mechanism:** The buyout pays out only when a seller drawn at random from the entrant pool, using ordinary examples, brings the learner to target error within k examples from the post-lesson state. The object bought is a measured drop in substitute sample cost: a property of the learner, not of the data.
- **Learning effect claimed:** The incumbent is paid to leave a representation that is extensible by others. This should change the learner from exception memorization to rule acquisition, which rule share and substitute sample cost measure.
- **Nearest prior / gap:** [Iterative Machine Teaching (1705.10470)](https://arxiv.org/abs/1705.10470) and [Nonparametric IMT (2306.03007)](https://arxiv.org/abs/2306.03007) minimize the teacher's own steps to a target; [Patent Buyouts (Kremer 1998)](https://academic.oup.com/qje/article-abstract/113/4/1137/1916997) prices the end of a monopoly by auction, without any learner. No contract found whose trigger is another teacher's sample cost on the bought learner.
- **Cheapest first test:** F-rule, exact. Compare per-label purchase, prepaid curriculum, Kremer-style buyout with a delivery trigger, and this substitute-cost trigger at equal spend. Kill if the delivery-triggered buyout produces the same rule share and substitute cost: then the trigger is decoration.
- **Old-task retention:** Score the old exception after the entrant's k examples, not at payout; a buyout that passes on substitute cost but loses the old exception counts as failed.

### LE2-02 · Escrow the old exceptions a general lesson will overwrite
- **Mechanism:** Part of the buyout is held back and released only if a predeclared set of old exceptions (held out, not shown to the incumbent) survive the rule lesson *and* the entrants' continuation. The incumbent must teach the rule *with its exceptions intact*, for example by teaching rule-then-exception, which quasiregular dynamics favor.
- **Learning effect claimed:** Under a plain buyout the cheapest general lesson overregularizes; with the escrow, the incumbent's best response changes the curriculum to one that keeps rare old cases. Measured as exception survival at equal new-task error.
- **Nearest prior / gap:** [Quasiregular dynamics (2609.26018)](https://arxiv.org/abs/2609.26018) shows rare exceptions are learned, overregularized and recovered; [Curriculum unlearning (2611.04565)](https://arxiv.org/abs/2611.04565) gives the rule-before-exception explanation; [Owned Edits (2611.15917)](https://arxiv.org/abs/2611.15917) stores private exceptions as gated, withdrawable weight edits. None ties a teacher's payment to exception survival under someone else's continuation.
- **Cheapest first test:** MLP on a quasiregular task, CPU. The strategic teacher picks among rule-only, exception-first and rule-then-exception curricula at fixed cost. Compare escrow vs no escrow vs a central buyer who mandates rule-then-exception. Kill if the mandated curriculum matches escrow at equal spend with no information advantage, then the escrow adds nothing a buyer could not specify.
- **Old-task retention:** This *is* the retention card; also report the U-shaped dip during training, not just the endpoint.

### LE2-03 · Measure dependency directly: the teacher-substitution gap
- **Mechanism:** Define a learner-side dependency index: loss after continuing with N incumbent examples minus loss after continuing with N entrant examples of the same task, from the same state. Buyout eligibility, price and timing are set from this index, not from market shares.
- **Learning effect claimed:** Turns "monopoly" into a measurable property of the learner (its state is tuned to one teacher's convention). Predicts that dependency grows with per-label purchases and falls after a rule lesson.
- **Nearest prior / gap:** [What Can Firms Do in the Face of Model Distillation? (2610.38088)](https://arxiv.org/abs/2610.38088) models competition among firms whose outputs are distilled, not the student's dependence on one teacher; multi-teacher on-policy distillation ([2610.02179](https://arxiv.org/abs/2610.02179)) measures capability transfer per teacher. No dependency index found used as a contract variable.
- **Cheapest first test:** Logistic regression where the incumbent labels with a private convention (a feature rotation or a label-noise pattern) and entrants do not. Track the index across 0–20 incumbent purchases and after a rule lesson. Kill if the index tracks just the count of incumbent labels (then it is a proxy, not a state property).
- **Old-task retention:** Compute the index on old tasks too: a high old-task index means switching suppliers will cost old competence.

### LE2-04 · Buy out the incumbent's convention, not its knowledge
- **Mechanism:** When dependency comes from a labeling convention (class order, tokenization, rationale format) rather than content, buy a *translation lesson* that maps the convention to an open one, and stop. The learner keeps the knowledge and loses the lock-in.
- **Learning effect claimed:** Separates two things the root conflates: what the learner knows and in what coordinates. Predicts a large drop in substitute sample cost at small lesson size, with no change in task accuracy.
- **Nearest prior / gap:** Root LE20 (buy compatibility once and make it open) is a market object; [Functional compatibility as a determinant of persistent learning (2608.22462)](https://arxiv.org/abs/2608.22462) relates whether learning persists to the compatibility of new and old functions. The gap is a priced lesson whose only target is the coordinate system and whose success is measured by substitute cost.
- **Cheapest first test:** Same convention toy as LE2-03; arms: full buyout, translation lesson only, per-label, re-pretraining in the open convention at equal compute. Kill if the translation lesson needs as many examples as relabeling the whole set.
- **Old-task retention:** Old-task predictions under the old convention must stay valid after translation, through normal prediction.

### LE2-05 · Durable-lesson commitment: a buyer who promises never to buy exceptions after date T
- **Mechanism:** Coase's logic says a seller of a durable good who can sell again tomorrow cannot hold today's price. Here the buyer commits to a date after which it will buy no narrow lessons from anyone; the incumbent's best response is to teach the rule before T.
- **Learning effect claimed:** The commitment shifts *when* the general lesson arrives in the learner's history. Since rule timing changes representation (simplicity bias, 2611.04565), this is a curriculum change made by a commitment, measured by rule share and exception survival.
- **Nearest prior / gap:** [Coasian Dynamics for information goods (2507.13137)](https://arxiv.org/abs/2507.13137) finds a folk-theorem payoff interval for durable information goods with zero marginal cost; [Coase 1972](https://doi.org/10.1086/466709) gives the base result. They model buyer valuation, not a learner whose value depends on the order received.
- **Cheapest first test:** Enumerate a three-date game with F-rule; compare no commitment, commitment to T, and central buyer choosing the date. Kill if learner outcomes are identical across commitment dates (then order does not matter in this learner and the card reduces to pricing).
- **Old-task retention:** Measure old-exception survival at each candidate T; early rule lessons may overwrite more.

### LE2-06 · Pay for the rule's half-life under substitute data
- **Mechanism:** The incumbent's rule decays as entrants' noisy or drifting data trains the learner. Pay a per-period fee proportional to rule share remaining after each entrant batch, for a fixed horizon. The incumbent is paid for robustness of the rule, not for installing it.
- **Learning effect claimed:** Incentivizes rules that resist erosion, such as wider-margin solutions or taught invariances, measured as rule half-life under fixed entrant streams.
- **Nearest prior / gap:** Root LE14 guarantees fast teaching does not cut pay; [Learning Dynamics of Continual Learning (2609.33620)](https://arxiv.org/abs/2609.33620) links attribution, forgetting and plasticity loss. Neither pays a supplier for persistence of its contribution under others' training.
- **Cheapest first test:** Logistic regression with entrant label noise 10–30%; incumbent chooses margin. Compare half-life pay vs one-off payment vs a central buyer imposing margin. Kill if half-life pay equals one-off pay with a margin clause.
- **Old-task retention:** Track old tasks during the same entrant stream; a robust new rule that erodes old rules is a failure.

### LE2-07 · A royalty on lessons that build on the rule
- **Mechanism:** The incumbent keeps a small share of every later entrant sale whose measured learning gain depends on the incumbent's lesson (gain with lesson minus gain without, on the same learner). This aligns the incumbent with teaching the most extensible rule rather than the most valuable self-contained one.
- **Learning effect claimed:** Shifts the incumbent's chosen lesson toward ones that increase later learning rates; measure the learning-rate gain of entrant data over the horizon.
- **Nearest prior / gap:** Root LE06 gives a supplier a claim on data a lesson makes possible; [Capturing the Temporal Dependence of Training Data Influence (2412.09538)](https://arxiv.org/abs/2412.09538) and [Data Shapley in One Training Run (2406.11011)](https://arxiv.org/abs/2406.11011) attribute credit to data in a training order. The gap is a payment rule whose base is the *counterfactual learning rate of later data*, which a learner measures cheaply in an exact toy.
- **Cheapest first test:** Enumerate two candidate lessons (narrow but high-value now, general but low-value now) in F-rule; compare flat buyout vs royalty. Kill if the royalty selects the same lesson as a one-off price equal to the royalty's expected value.
- **Old-task retention:** Royalty base must also subtract old-task loss caused by the building lessons, or it pays for forgetting.

### LE2-08 · Self-continuation as the end of dependency
- **Mechanism:** The strongest monopoly-ending lesson lets the learner generate its own next training data (self-labeling or self-distillation) at accuracy above the entrants'. The buyout target becomes the learner's own pseudo-label accuracy on unlabeled new-task inputs.
- **Learning effect claimed:** Replaces "interchangeable sellers" with "no seller needed"; measured by how far self-training from the post-lesson state goes without any purchase, and by drift.
- **Nearest prior / gap:** Multi-teacher on-policy distillation ([MOPD 2606.30406](https://arxiv.org/abs/2606.30406), [Replay with MT-OPD 2611.02746](https://arxiv.org/abs/2611.02746)) uses fixed teachers; self-training is old. None prices a lesson by the self-training it enables or checks self-training drift against old tasks.
- **Cheapest first test:** Logistic regression with pseudo-labels after each lesson type; compare rule lesson, exception lessons and no lesson at equal spend. Kill if self-training gain is the same after any lesson that reaches the same new-task accuracy.
- **Old-task retention:** Self-training is known to drift; score old tasks throughout the unsupervised continuation.

### LE2-09 · When is selling the rule better for the learner than for the market?
- **Mechanism:** An audit card, not a mechanism. Compare (a) the central buyer's welfare-optimal curriculum, (b) the equilibrium under LE01-style buyout, and (c) the learner-optimal curriculum (max retention plus new-task accuracy at a cost cap). Find instances where the market's best rule lesson is not the learner's best.
- **Learning effect claimed:** Identifies whether buyouts select for lessons that are cheap to continue (good for markets) at the cost of lessons that are retention-friendly (good for the learner).
- **Nearest prior / gap:** [Selling Training Data (2611.29971)](https://arxiv.org/abs/2611.29971) studies seller strategy with a learning buyer; it optimizes revenue, not learner retention.
- **Cheapest first test:** Exhaustive enumeration over all three- and four-lesson curricula in F-rule. Kill the entire LE01 line if (a), (b) and (c) always coincide.
- **Old-task retention:** Built into objective (c).

## B · LE13 made into a learning claim: what does a path price say about the learner?

### LE2-10 · Price the class of the state reached, with retention in the class definition
- **Mechanism:** Two histories are in the same price class only if they agree on (i) the new task, (ii) the held-out old mix, and (iii) the response to every permitted next lesson. Price caps are computed over classes, not lesson sets.
- **Learning effect claimed:** F-order shows the effect: A→B and B→A agree on (i) but not (ii). A class-based price separates them; a set-based price cannot. The buyer is steered toward the retaining order.
- **Nearest prior / gap:** [Query-Based Data Pricing (Koutris et al. 2012)](https://dl.acm.org/doi/10.1145/2213556.2213582) prices by derivability; [Arbitrage-free Data Pricing (2606.10451)](https://arxiv.org/abs/2606.10451) handles bundles of versioned products with Bayesian buyer value, order-free. Top-10 #2 (Nerode quotient) defines (iii) for edits but not as a price object. Gap: retention-aware class pricing.
- **Cheapest first test:** F-order plus a 4-lesson extension, exact. Compute set prices, shortest-path prices, and class prices; count arbitrage opportunities each misses. Kill if adding (ii) never changes classes in any small instance.
- **Old-task retention:** Defined in the class.

### LE2-11 · Order-arbitrage refund that teaches sellers to sell retaining orders
- **Mechanism:** If the buyer later finds a reordering of the same lessons that reaches a weakly better class (same new task, less old loss) at the same price, the seller owes a refund equal to the old-loss gap priced at a posted rate. Sellers therefore recommend and sequence lessons in the retaining order.
- **Learning effect claimed:** Moves the order choice from the buyer, who rarely knows the bracket, to the seller who designs lessons. Measured by order gap at equilibrium.
- **Nearest prior / gap:** [Lie bracket and forgetting (2611.20087)](https://arxiv.org/abs/2611.20087) predicts forgetting from order without old data; [Curriculum Learning as Transport (2609.09099)](https://arxiv.org/abs/2609.09099) optimizes order. Neither puts order responsibility on a strategic seller.
- **Cheapest first test:** F-order with two competing sellers each owning one lesson; compare no refund, refund, and a central buyer choosing order. Kill if the refund equals the central buyer's choice only because the seller knows nothing the buyer doesn't.
- **Old-task retention:** Refund base is old loss.

### LE2-12 · Charge each edge its bracket: a retention-indexed price per lesson pair
- **Mechanism:** Sell low-bracket lesson pairs (order-insensitive) as bundles and high-bracket pairs only as sequences with a declared order. Bracket estimated from the stored gradient and top Hessian eigenpairs at the end of each lesson, as in 2611.20087.
- **Learning effect claimed:** Product structure tracks the learner's actual order sensitivity: bundles only where order does not matter for retention.
- **Nearest prior / gap:** Arbitrage-free pricing (2606.10451) assumes combinable purchases; order-insensitive in effect. [Dynamic Shapley Computation (2605.20620)](https://arxiv.org/abs/2605.20620) updates values as data changes, not as order changes.
- **Cheapest first test:** MLP on two Split-MNIST-style tasks at small scale on CPU; estimate the bracket per pair; compare bundled vs sequenced pricing on realized old-task loss. Kill if the bracket fails to rank pairs by order gap (Spearman < 0.5).
- **Old-task retention:** Order gap on old tasks is the target variable.

### LE2-13 · Price the return trip: lesson price includes the cost of restoring old tasks
- **Mechanism:** Every lesson is quoted together with the cheapest permitted repair path (a few old-task examples or a repair lesson) that restores the old mix to floor. The buyer compares round-trip costs, not one-way prices.
- **Learning effect claimed:** Encourages lessons that leave the learner easy to repair, not merely accurate; measured as repair cost.
- **Nearest prior / gap:** Replay buys old data; LE23 unbundles old data. Gap: the repair path is a priced object attached to the lesson, and lessons compete on it.
- **Cheapest first test:** Logistic regression with two candidate new-task lessons of equal accuracy but different repair costs. Kill if repair cost is constant across lessons.
- **Old-task retention:** Restoring old tasks is the deliverable.

### LE2-14 · Paths with rights: the state × rights product graph
- **Mechanism:** Each edge has a rights label (train, replay, inherit, sublicense). A path's rights are the intersection along it. Price caps are shortest paths in the product of learner classes and rights.
- **Learning effect claimed:** A path whose last edge forbids replay makes the learner unable to repair old tasks later; the price must reflect the lost repair path. Measured by retention after a later forced transition.
- **Nearest prior / gap:** Provenance semirings ([Green, Karvounarakis, Tannen 2007](https://dl.acm.org/doi/10.1145/1265530.1265535)) track annotations through queries; root LE08 sells separate rights. Gap: rights constrain future *learning moves*, so rights and learner state jointly determine value.
- **Cheapest first test:** F-order with B licensed "no replay"; then a third lesson that requires replay to avoid forgetting. Kill if rights never change shortest paths in small instances.
- **Old-task retention:** Measured after the later forced transition.

### LE2-15 · The gauge clause: refuse to certify equivalence from outputs
- **Mechanism:** A path-pricing rule declares two states equivalent only after a probe continuation (a fixed short lesson sequence) yields matching behavior, not from current outputs. The seller pays for the probe.
- **Learning effect claimed:** PR #104's uv example ((1,1) vs (2,½)) shows function-identical states diverge after one gradient step; pricing them the same misprices future learning. The probe exposes this.
- **Nearest prior / gap:** Top-10 #2 and PR #104 define the issue for edits; none uses it as a pricing condition.
- **Cheapest first test:** uv model exact; compare output-based and probe-based equivalence for path pricing. Kill if the probe misses gauge divergence at probe lengths ≤ 3.
- **Old-task retention:** The probe must include old-task examples.

### LE2-16 · Path options: buy the rest of a path only if the first lesson didn't generalize
- **Mechanism:** The buyer buys lesson 1 plus an option on lessons 2..n at a pre-agreed strike; exercises only if the learner is not already in the target class after lesson 1.
- **Learning effect claimed:** Learners that generalize fast stop buying. Measured by lessons consumed per target class, and avoided overtraining that might cost old tasks.
- **Nearest prior / gap:** [Pricing Pandora's Boxes (2607.23359)](https://arxiv.org/abs/2607.23359) prices sequential information acquisition; [Pricing Access to Dynamic Information Services (2510.09859)](https://arxiv.org/abs/2510.09859). Neither has a learner whose state after one purchase changes the value of the rest.
- **Cheapest first test:** F-rule with a fast and a slow learner type; compare bundle, per-lesson and option. Kill if exercise rates do not differ by learner type.
- **Old-task retention:** Less training should mean less forgetting; measure whether it does.

### LE2-17 · Cap a bulk price at the learner-specific teaching dimension
- **Mechanism:** Bulk price capped at the cost of the shortest teaching sequence for *this* learner's update rule from its current state, computed by any seller. Sellers who sell padding beyond the teaching dimension cannot charge for it.
- **Learning effect claimed:** Cuts superfluous examples that cause interference; measured by old-task drop at matched new-task accuracy.
- **Nearest prior / gap:** IMT (1705.10470) computes efficient sequences for a passive student; [Machine Teaching of Active Sequential Learners (1809.02869)](https://arxiv.org/abs/1809.02869). Gap: the teaching dimension as a market price cap.
- **Cheapest first test:** Logistic regression; compare sellers who pad vs capped sellers. Kill if padding never increases old-task loss.
- **Old-task retention:** Old-task drop is the readout.

### LE2-18 · Class-only prices: forbid charging for the buyer's private learning speed
- **Mechanism:** A seller who observes the buyer's progress can price-discriminate: quote a slow learner a cheap, short lesson it cannot fully use, and a fast learner a long, expensive one it does not need. The rule allows prices to depend only on the declared learner class (LE2-10), never on observed learning speed.
- **Learning effect claimed:** Under discrimination, lesson *content* tracks the seller's surplus, so slow learners end with partial rules and fast learners are overtrained (more interference). Class-only pricing should equalize rule share and old-task loss across learner types at matched spend.
- **Nearest prior / gap:** [When Trade Produces Knowledge (2607.18509)](https://arxiv.org/abs/2607.18509) studies dynamic pricing where both sides learn about value; root LE14 protects the teacher from fast-learning cuts. Neither measures what discrimination does to the learner's representation or retention.
- **Cheapest first test:** Enumerate F-rule with two private learner types (one-step and three-step rule acquisition) and a seller who sees progress after each purchase. Compare discriminating, class-only and central-buyer prices. Kill if both learner types end with the same rule share and old-task loss under all three.
- **Old-task retention:** Report old-exception survival per learner type; overtraining the fast type is the predicted failure.

### LE2-19 · Granularity as a priced choice: sell the new task split or whole
- **Mechanism:** A seller can sell the new task as one lesson or as k sub-lessons; the price schedule prices granularity explicitly, since granularity changes forgetting.
- **Learning effect claimed:** Measured old-task forgetting under each granularity at the equilibrium price.
- **Nearest prior / gap:** [Task Granularity and Forgetting (2606.08013)](https://arxiv.org/abs/2606.08013) measures the effect; no pricing.
- **Cheapest first test:** MLP, CPU; compare granularity at equal total examples. Kill if granularity has no effect on forgetting in the toy.
- **Old-task retention:** Directly measured.

### LE2-20 · Selling forgetting-safe orders requires the seller to see old data, which the buyer may not grant
- **Mechanism:** A seller can only design retaining orders if it can estimate the bracket against the buyer's old tasks. The buyer sells the seller a compressed old-task summary (gradient and Hessian top eigenpairs, as in 2611.20087) instead of old data.
- **Learning effect claimed:** Retention improves with the summary at no transfer of old data.
- **Nearest prior / gap:** 2611.20087 uses the summary for early warning, not as a tradable good.
- **Cheapest first test:** Split-MNIST-style CPU; compare seller with summary, without, and with full old data. Kill if summary gives no retention gain over no summary.
- **Old-task retention:** Directly measured.

## C · Joining LE01 and LE13: monopoly is a property of the path graph

### LE2-21 · The buyout is an edge in the path graph
- **Mechanism:** Represent LE01's general lesson as one edge in LE13's teaching graph: the edge after which entrant-only paths reach the target class. Its price cap is the cheapest entrant-continuable path through it, and its floor is the incumbent's continuation rent along the per-label path.
- **Learning effect claimed:** The two score-3 cards become one object: a buyout is worth paying only if the learner's class after it has short entrant continuations, which is substitute sample cost (LE2-01) read as path length.
- **Nearest prior / gap:** Kremer buyouts price the end of a monopoly with no learner; query and arbitrage-free pricing (Koutris et al.; 2606.10451) price derivable bundles with no monopoly. No combined object found.
- **Cheapest first test:** Write F-rule as an explicit graph over learner classes; compute cap and floor; check whether the buyout interval is empty for the rule-plus-exception learner but not for logistic regression. Kill if the cap always equals per-label cost (the edge carries no learning value).
- **Old-task retention:** Classes include the old mix, so a cheap entrant continuation that drops the old exception lands in a different class and does not count.

### LE2-22 · Allow a seller switch only between retention-equivalent continuations
- **Mechanism:** The buyer may move from incumbent to entrant mid-path only if the entrant's continuation and the incumbent's would end in the same class, old mix included. The switch is a constraint in the graph, checked on the learner with a short probe (LE2-15), not a contract term.
- **Learning effect claimed:** Blocks the predicted failure of competitive entry: entrants who are cheaper because they ignore the old exceptions. Measures forgetting caused by switching, separately from forgetting caused by the new task.
- **Nearest prior / gap:** Root LE10 replaces a restrictive source by buying the same input elsewhere; it assumes same input means same learning. [Multi-teacher on-policy distillation (2610.02179)](https://arxiv.org/abs/2610.02179) shows teachers transfer different capabilities. Gap: retention as the switching condition.
- **Cheapest first test:** F-rule with two entrants, one whose labels match the incumbent's on the new task but contradict the old exception. Count allowed switches and old loss with and without the rule. Kill if every switch preserves retention in the toy.
- **Old-task retention:** The defining condition; also report the switch-induced share of total forgetting.

### LE2-23 · Price the plasticity a rule lesson spends
- **Mechanism:** A general lesson compresses representations (simplicity bias with compression, 2611.04565) and may lower the learner's ability to learn the next unrelated task. The quote for a rule lesson includes the expected extra examples a later task will need from the post-lesson state.
- **Learning effect claimed:** Separates two goods a buyout bundles: extensibility *within* the rule's domain (cheap entrants) and plasticity *outside* it (expensive later tasks). Predicts a measurable trade-off between rule share and third-task learning speed.
- **Nearest prior / gap:** [Pretraining Curricula Enable Selective Fine-tuning (2607.04846)](https://arxiv.org/abs/2607.04846) shows curricula shape later fine-tuning; [Learning Dynamics of Continual Learning (2609.33620)](https://arxiv.org/abs/2609.33620) connects plasticity loss to training data. Neither prices the later learning cost to the lesson that caused it.
- **Cheapest first test:** One-hidden-layer MLP: old tasks, then rule lesson or exception lessons of equal new-task accuracy, then an unrelated third task; count third-task examples to target. Kill if third-task cost does not differ by lesson type.
- **Old-task retention:** Score the old mix after the third task as well; a compressed representation may protect or expose it.

### LE2-24 · A reachability covenant against path-dependent lock-in
- **Mechanism:** An incumbent can create a monopoly without any contract by steering the learner into states from which only its own lessons are short (its convention, its features). The covenant caps the entrant distance, the length of the cheapest entrant-only path to target, from every state the incumbent's lessons reach; exceeding it voids the incumbent's per-lesson price.
- **Learning effect claimed:** Makes lock-in a measurable learner property (entrant distance along the path) and predicts the incumbent shifts to lessons that keep the learner in open coordinates.
- **Nearest prior / gap:** Root LE21 ends exclusivity on refused supply, a legal trigger. [Computational Arbitrage in AI Model Markets (2603.22404)](https://arxiv.org/abs/2603.22404) studies arbitrage across model providers, not reachability of learner states. None found that contracts on distance in a learner's state graph.
- **Cheapest first test:** Logistic regression where the incumbent can teach in a private feature rotation; compute entrant distance after each lesson; compare covenant vs none vs LE2-04 translation buyout. Kill if entrant distance stays flat under all incumbent strategies.
- **Old-task retention:** Old tasks must remain within the covenant's distance too, so the incumbent cannot lock in the old mix.

### LE2-25 · Price an exiting supplier's unlearning path by the damage it does
- **Mechanism:** When a supplier withdraws and its contribution must be unlearned, the learner traverses a reverse path. Quote at entry the expected old-task damage of that reverse path, so suppliers whose lessons are entangled with the old mix pay more for the right to withdraw later.
- **Learning effect claimed:** Prices entanglement. Predicts suppliers prefer lessons that are separable from old knowledge when withdrawal is priced, measured by old-task loss after unlearning.
- **Nearest prior / gap:** [Machine Unlearning (SISA, 1912.03817)](https://arxiv.org/abs/1912.03817) makes withdrawal cheap by sharding; [Owned Edits (2611.15917)](https://arxiv.org/abs/2611.15917) makes exceptions withdrawable by construction; root LE07 returns use rights. None prices the collateral old-task damage of withdrawal back to the supplier's choice of lesson.
- **Cheapest first test:** F-order and logistic regression: two suppliers, one with an entangled lesson (shares weights with the old task), one separable; unlearn by retraining without each. Compare entry choices with and without the withdrawal quote. Kill if both lessons cause equal collateral damage.
- **Old-task retention:** Collateral old-task loss after withdrawal is the measured quantity.

### LE2-26 · Adversarial acceptance: pay a rival to find where the bought rule fails
- **Mechanism:** A buyout's acceptance test is run by a second seller paid per input on which the post-buyout learner, after entrant continuation, fails the new rule or an old exception. The incumbent's payout falls with each found failure.
- **Learning effect claimed:** Finds failures that a fixed held-out set misses (rare exceptions the incumbent knows about and the buyer does not), so the incumbent's best lesson covers them. Measured as residual failure rate on a large hidden test set.
- **Nearest prior / gap:** Root LE03 auctions the right to be second as a supply slot; [Teaching and Learning under Deductive Errors (2605.13384)](https://arxiv.org/abs/2605.13384) studies teaching when learners infer wrongly. No acceptance test found that pays a rival to search the learner for failures.
- **Cheapest first test:** F-rule with an incumbent who knows a rare old exception; arms: fixed held-out acceptance, adversarial acceptance with search budget 1–4 queries, central buyer with full knowledge. Kill if adversarial acceptance never lowers residual failure versus a held-out set of the same query count.
- **Old-task retention:** The rival is paid for old-exception failures too, so retention is part of acceptance.

### LE2-27 · Planner-equivalence audit for the whole node
- **Mechanism:** For every card above, compute the central buyer's learner outcome (rule share, substitute cost, order gap, old-task loss) with the same information, rights, transfers and commitment. A card survives only where the market outcome differs *because of* private information held by sellers.
- **Learning effect claimed:** Separates two claims a market card can make: that prices move learning (anyone can do that with a mandate) and that prices extract seller knowledge that moves learning (only markets can).
- **Nearest prior / gap:** The root's shared protocol requires a central-buyer comparator; [Unifying Data Values via Sequential Decision-Making (2502.04554)](https://arxiv.org/abs/2502.04554) frames data selection as a planner problem. This card turns the comparator into a kill rule per card.
- **Cheapest first test:** Run all exact fixtures with the planner given the sellers' private types. Kill any card whose market outcome equals the informed planner's and differs from the uninformed planner's only by information the buyer could cheaply acquire.
- **Old-task retention:** The planner's objective includes the old-mix floor, so a card cannot win by forgetting.

## Ranked deeper questions

1. **Does paying for a monopoly-ending lesson change what the learner ends up representing?** (LE2-01, 02, 05, 09, 21) Find the smallest F-rule instance where substitute-cost-triggered buyout, delivery-triggered buyout and per-label purchase leave different rule shares and exception survival at equal spend.
2. **What is the weakest learner-state equivalence a path price can use without mispricing retention?** (LE2-10, 14, 15) Build on top-10 #2 and PR #104; show a case where output equivalence, class equivalence with retention, and Nerode equivalence give different prices.
3. **Can a strategic seller be made responsible for order-induced forgetting?** (LE2-11, 12, 20) Find the smallest instance where a refund or bracket pricing reduces the order gap below what a buyer without the seller's information could achieve.
4. **When does the cheapest continuable rule cost the learner plasticity or rare old cases?** (LE2-06, 22, 23) Show whether the market selects for lessons that are cheap to continue at the expense of retention.
