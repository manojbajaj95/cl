# Cross-generation inheritance: what a new base model should inherit from an old fine-tune

**Status:** research ideas plus one small NumPy sanity probe; no GPU and no claims beyond the toy. **Parents:** the [idea ledger (PR #6)](https://github.com/manojbajaj95/cl/pull/6). **Siblings it must not duplicate:** [edit transfer (PR #76)](https://github.com/manojbajaj95/cl/pull/76) and [fleet memory (PR #15)](https://github.com/manojbajaj95/cl/pull/15). This branch of the tree concerns continual learning **across model generations**. It is not about edit equivalence, edit localization or moving a single weight delta between models.

## Root-cause hypothesis

A fine-tune is an adaptation **to an old world, written by an old learner**. When a new base model arrives, the fine-tune contains three things mixed together: (a) the skill the owner actually wanted; (b) the old base's beliefs about the world, which the skill was trained against and which the new base may have corrected; and (c) the old base's calibration, which belongs to no one. Plain distillation from the old fine-tune copies all three. Edit transport tries to move (a) as an object. The hypothesis of this node is that inheritance across generations is a **population and lineage process**: what should pass on is whatever survives re-derivation by a learner with a different prior in a changed world. That is the problem cultural evolution studies (transmission bottlenecks, ratchets, Rogers' paradox) and the choice evolution poses between Lamarckian inheritance (pass on acquired traits) and Darwinian/Baldwinian inheritance (pass on whatever made acquisition cheap).

The probe below shows the failure in its simplest form. When the old world is wrong somewhere, distilling from the old fine-tune transfers the skill but also brings back the old world as **fossils** that the new base had already corrected.

## Prior-art and repo screen

- **Data-free transfer to a new base already exists.** [TuneShift-KD](https://arxiv.org/abs/2603.24518) transfers specialized knowledge from a fine-tuned model to a new base without the original data. [Data-free on-policy distillation](https://arxiv.org/abs/2609.14193), [fine-tuning transfer / task-vector re-basing](https://arxiv.org/abs/2503.20110) ([also](https://arxiv.org/abs/2505.22697)), [LoRA-X](https://arxiv.org/abs/2501.16559) and [inverse value learning](https://arxiv.org/abs/2410.21027) cover adapter/delta/value transfer. Teacher-to-new-base imitation, generated probe sets and delta re-basing are baselines here, not contributions.
- **Cultural evolution of learners is active.** [Cultural accumulation in RL](https://arxiv.org/abs/2406.00392) shows generational ratchets for fixed-architecture agents. [Model collapse as cultural evolution](https://arxiv.org/abs/2605.23054), [iterated subliminal trait transfer](https://arxiv.org/abs/2609.25721) (traits persist over ten generations while their explicit expression declines), [Rogers' paradox and lossy transmission](https://arxiv.org/abs/2611.06022), [cultural evolution in neural emergent communication](https://arxiv.org/abs/2611.00006), [Lamarckian evolution and the Baldwin effect](https://arxiv.org/abs/2605.28703), [Selection is not learning](https://arxiv.org/abs/2610.22029), [Continual learning in transition](https://arxiv.org/abs/2608.06216) and [model lineage attestation](https://arxiv.org/abs/2601.11683) are the closest neighbours. No screen here establishes priority. Each card states the bet that would separate it from these papers.
- **Local exclusions.** PR #76 owns moving edits between models, including parallel transport along a training lineage, universal teaching sets, evidence instead of conclusions, subliminal channels and fleet-consensus edits. Fleet Q2/Q3 (PR #15) already predict which lessons go stale after an upgrade; they were falsified or blocked by unreliable truth targets, so "predict obsolescence" is not reopened. The ledger's killed patterns (memory inoculation, self-quizzing, save/restore, frozen prompt pools) do not become new by adding a generation index.

## Toy probe: fossils and anti-transfer

[`tree/probes/cross_generation_probe.py`](probes/cross_generation_probe.py) (NumPy, about 20 s on CPU, 8 seeds). An old base `B0` learns world `W0`. Its fine-tune `F0` learns skill `S` on region `Q`, mixed 1:1 with `B0`'s own labels as an anchor. A new base `B1` learns `W1`, which corrects `W0` on region `R` (overlapping `Q`). `B1` inherits from `F0` using only unlabeled generic inputs. Mean ± s.e.:

| arm | skill on Q | W1 fix kept on R\Q | fossil rate R\Q | untouched old tasks |
|---|---|---|---|---|
| F0 (old fine-tune) | 0.783 ± 0.004 | 0.032 ± 0.003 | 0.848 ± 0.005 | 0.846 ± 0.003 |
| B1 (no inheritance) | 0.188 ± 0.008 | 0.942 ± 0.002 | 0.030 ± 0.002 | 0.952 ± 0.001 |
| plain KD from F0 | 0.735 ± 0.004 | 0.032 ± 0.003 | 0.843 ± 0.006 | 0.846 ± 0.003 |
| delta KD (B1 + F0 − B0 logits) | 0.327 ± 0.019 | 0.659 ± 0.019 | 0.000 ± 0.000 | 0.061 ± 0.009 |
| disagreement-gated KD | 0.578 ± 0.010 | 0.759 ± 0.008 | 0.122 ± 0.008 | 0.848 ± 0.005 |
| oracle: fine-tune B1 on S data | 0.742 ± 0.006 | 0.670 ± 0.008 | 0.152 ± 0.008 | 0.772 ± 0.006 |

What the toy shows, and nothing more:
1. **Plain inheritance turns the new base into the old one.** KD recovers the skill (0.735), but `B1` keeps only 3% of its own corrections outside `Q`, and 84% of those inputs revert to the old world's answer.
2. **Naive delta arithmetic transfers in reverse.** Adding `F0 − B0` logits to `B1` scores 0.061 on untouched old tasks, below the 1/6 chance rate. The anchored fine-tune is less confident than `B0`, so the difference votes *against* `B0`'s top class wherever the two agree. Calibration is inherited along with the skill.
3. **A disagreement gate is a strong, cheap baseline, and it still leaves a gap.** Gating to `F0` only where `F0` and `B0` disagree keeps most fixes. It still loses about 16 pp of skill and 10 pp of untouched-old accuracy relative to the best arms. Every card below must beat this gate and plain KD, not just `B1`.
4. Even real skill data on `B1` costs 17 pp on its corrections. The target is not "as good as the old data" but a Pareto point no arm in the table reaches.

## Shared CPU test contract

- Use synthetic worlds, as in the probe: `W0 → W1 → W2 …` with controlled correction regions, and skills defined independently of the world, conditioned on it, or contradicting it. Architectures change across generations (width, depth, activation, seed) so that parameter coordinates are never shared. The successor never sees skill labels; it gets unlabeled generic inputs and whatever artifact the card allows, matched in bytes or queries across arms.
- Always report four numbers: inherited skill; the new base's corrections kept; fossil rate (old-world answers where the worlds differ); and **untouched old tasks**, meaning the successor's own pre-inheritance competence outside the skill region. Use paired seeds and at least 8 seeds. The controls are plain KD, delta KD, the disagreement gate, and an oracle fine-tune with skill data. A card passes a first screen only if it beats the gate on skill or fossils with no more than a 2 pp drop on untouched old tasks.
- For multi-generation cards, also report the trajectory of each number across at least 4 generations, so that "survives one hop" is never mistaken for "accumulates".

## Research ideas (22 cards)

### A. Fossils: separating the skill from the world it was trained against

#### 1. Inherit only what is invariant to the ancestor's world model

- **Mechanism:** Perturb `B0`'s world beliefs counterfactually by fine-tuning cheap copies `B0'` on synthetic world shifts. Re-apply the same fine-tune recipe to the copies using `F0`'s self-generated probe inputs, then keep the component of `F0`'s behavior that is stable across all `B0'`. The successor inherits that invariant component. Where the component depends on the world, `B1` relabels it under its own world.
- **Novelty bet — primitive candidate:** This treats a fine-tune as a function of its base's world beliefs and inherits only its world-invariant component, applying an IRM-style idea to ancestry instead of to environments. TuneShift-KD and delta re-basing both assume the skill is base-independent.
- **Cheapest test:** The probe with three skill types (independent, conditioned on world facts, contradicting the world). It succeeds if the fossil rate drops below the gate's at equal skill.
- **Old-task retention:** Untouched old-task accuracy and corrections kept on `R\Q` before and after inheritance, compared with the gate.

#### 2. Inherit decision flips, not logits

- **Mechanism:** Represent `F0`'s adaptation as the set of inputs where the fine-tune *changed the decision* relative to `B0` (an ordinal event), plus the new decision. Calibration and margin changes are discarded. `B1` is trained only on flipped inputs and anchored to itself elsewhere.
- **Novelty bet — improvement:** The probe shows that calibration drift makes logit deltas anti-transfer. Ordinal, flip-only inheritance is the minimal fix and serves as a falsifiable explanation of finding 2. If it ties the gate, the gate already captures it.
- **Cheapest test:** The probe, adding a sweep of the anchor temperature used to build `F0` so that its calibration shift varies independently of the skill.
- **Old-task retention:** Untouched old tasks must stay within 2 pp of `B1`. Report the result separately for inputs where `B0` and `B1` disagree.

#### 3. Fossil audits by triangulating three models

- **Mechanism:** For every candidate inherited behavior, check whether it agrees with `B0`, `B1` and `F0`. A behavior shared by `F0` and `B0` but contradicted by `B1` is a fossil candidate. Train a small classifier, using only generic inputs, to predict fossil versus skill from the three models' internal disagreement features, and use it as the gate.
- **Novelty bet — improvement:** The gate in the probe uses a hand threshold. The bet is that fossilness is *learnable from geometry*, transfers across skills, and therefore works for future upgrades without labels.
- **Cheapest test:** Train the audit on skills 1–3, test it on held-out skills 4–5 and on new world shifts.
- **Old-task retention:** Measure untouched old tasks on held-out skills, where the audit is out of distribution.

#### 4. Provisional inheritance with reconsolidation

- **Mechanism:** Inherited behaviors enter `B1` as a separate, decaying adapter. Each behavior is consolidated into the main weights only after `B1` re-derives it from its own later experience (self-consistency under new unlabeled data and any sparse feedback). Behaviors that are never re-derived decay.
- **Novelty bet — primitive candidate:** Inheritance becomes a *hypothesis the descendant must re-earn*, not a write. That matches memory reconsolidation and differs from the permanent inheritance used in every distillation baseline.
- **Cheapest test:** The probe plus a stream of sparse W1 feedback on `R`. Measure whether fossils decay faster than the skill.
- **Old-task retention:** Untouched old tasks at every consolidation step. Count a skill that is lost with no counter-evidence as a failure.

### B. Lamarckian versus Darwinian/Baldwinian inheritance

#### 5. A measured crossover between inheriting traits and inheriting learnability

- **Mechanism:** Run two lineages through a sequence of worlds and skills. The *Lamarckian* lineage passes `F0`'s behavior to each successor. The *Baldwinian* lineage passes only what made learning fast: an initialization offset, a learning-rate map, or a curriculum, but none of `F0`'s outputs. Vary the world-shift rate and the skill's dependence on the world.
- **Novelty bet — primitive candidate:** The prediction is that a crossover exists: Lamarck wins when worlds are stable, Baldwin wins when they drift. Its location should be predictable from a measurable quantity, the disagreement between `B0` and `B1` on generic inputs. [2605.28703](https://arxiv.org/abs/2605.28703) studies this for evolving agents, not for base-model succession with fine-tunes.
- **Cheapest test:** A 4-generation chain of the probe with shift rates {0, 0.1, 0.3, 0.6}. The card dies if one strategy wins everywhere.
- **Old-task retention:** Each successor's untouched old tasks and all earlier generations' skills, re-scored at the end.

#### 6. Inherit the developmental order, not the endpoint

- **Mechanism:** Use the ordering in which `F0`'s checkpoints changed behavior on generic inputs (which inputs moved first) as a curriculum for `B1`. `B1` then trains on its own self-labels plus the ancestor's *order*, never the ancestor's final outputs.
- **Novelty bet — primitive candidate:** This passes on development, not phenotype. The bet is that order carries the skill's structure but not the old world's answers, so fossils are avoided by construction.
- **Cheapest test:** The probe with saved `F0` checkpoints. Compare with a random order, a difficulty order computed from `B1`, and plain KD.
- **Old-task retention:** Untouched old tasks and corrections on `R\Q` after each curriculum stage.

#### 7. Baldwinian assimilation: learn plastically, then assimilate selectively

- **Mechanism:** `B1` first acquires inherited behaviors in a fast, discardable form: a scratch adapter, an in-context buffer, or a retrieval table of `F0` answers. It then assimilates into its weights only the behaviors that it can relearn cheaply from few examples, measured by its own learning speed. The rest stay in the discardable form or are dropped.
- **Novelty bet — primitive candidate:** The Baldwin effect used as a filter: ease of re-learning by the descendant signals that a behavior fits its prior, while fossils should be hard to learn because they contradict `B1`'s world.
- **Cheapest test:** The probe. Check whether per-input re-learning speed separates skill from fossils (AUROC) before building the full system.
- **Old-task retention:** Untouched old tasks after assimilation versus the gate, including the retrieval-table arm.

#### 8. Epigenetic plasticity marks

- **Mechanism:** Inherit only *where* the ancestor changed, as a per-region map of plasticity and regularization strength in input space, not what it changed to. The successor then gets a small skill feedback budget and spends plasticity where the ancestor needed it.
- **Novelty bet — primitive candidate:** This passes on a learning prior with zero answers, the purest Darwinian/epigenetic channel. The bet is that a feedback budget about 10× smaller suffices.
- **Cheapest test:** The probe with a budget of N skill labels for `B1`. Compare plasticity marks with uniform plasticity and with the oracle fine-tune.
- **Old-task retention:** Untouched old tasks, because concentrated plasticity should *protect* them. Fail if they drop more than in the uniform arm.

#### 9. Germline artifacts: train the old model to be a good ancestor

- **Mechanism:** During `F0`'s fine-tune, also train a separate small transmission artifact: probe generator, verifier and rationale set. Optimize it for how well *random unseen successor architectures* recover the skill from it alone. The weights act as soma; the artifact acts as germline.
- **Novelty bet — primitive candidate:** Heritability becomes an explicit training objective at the time of fine-tuning, a meta-learning problem over unknown future bases. Existing work transfers after the fact from whatever the old model happens to be.
- **Cheapest test:** Meta-train the artifact against 5 successor architectures, then test on 3 held-out architectures and a shifted world.
- **Old-task retention:** `F0`'s own skill and untouched tasks must not drop from the extra objective, and successor retention is measured as in the contract.

### C. Cultural transmission and iterated learning

#### 10. Iterated-learning bottleneck as a fossil filter

- **Mechanism:** Pass the skill through k rounds of narrow re-learning: each intermediate learner (different seed and architecture) sees only m generated examples from the previous one and labels new ones. Iterated learning amplifies what is learnable and drops what is idiosyncratic. The bet is that fossils are idiosyncratic to `B0` and get filtered out.
- **Novelty bet — primitive candidate:** This uses a transmission bottleneck deliberately as a denoiser *of the ancestor's world*, not only to produce compositional languages. The risk is that it also erodes the skill, as model collapse does ([2605.23054](https://arxiv.org/abs/2605.23054)).
- **Cheapest test:** The probe with k ∈ {1, 2, 4, 8} and m ∈ {64, 256}. Plot skill and fossil rate against k.
- **Old-task retention:** Final `B1` untouched old tasks, and whether the skill decays monotonically or plateaus.

#### 11. A cultural ratchet across changing bases

- **Mechanism:** Keep a lineage repository of skills, each paired with an executable check (a probe set plus a verifier). Every new base inherits only skills whose checks it can pass after cheap self-training, may add one innovation, and writes it back with a check. Over generations, measure whether total competence ratchets upward.
- **Novelty bet — primitive candidate:** [Cultural accumulation in RL](https://arxiv.org/abs/2406.00392) shows ratchets for a *fixed* architecture. The bet is that verified transmission ratchets even when every generation's prior and world differ, and that the verifier stops fossils from accumulating.
- **Cheapest test:** An 8-generation chain with one new skill per generation and world shifts. Compare with a no-check repository and with plain KD chains.
- **Old-task retention:** Every earlier skill, scored at every generation. The ratchet claim fails if early skills decay while late skills accumulate.

#### 12. Transmission fragility, measured before the upgrade

- **Mechanism:** Before deprecating `F0`, estimate each skill's *transmission fragility*: how much the skill drifts when re-learned by 3 cheap proxy successors. Spend the inheritance budget on fragile skills and let robust skills transmit through cheap channels.
- **Novelty bet — improvement:** This is a per-skill heritability estimate used for budget allocation. Fleet Q2/Q3 predicted obsolescence; this card predicts *transmission loss*, a different quantity.
- **Cheapest test:** Check whether the proxy fragility ranking predicts real fragility on `B1` (Spearman), then compare equal-budget allocation with fragility-weighted allocation.
- **Old-task retention:** Untouched old tasks under both allocations.

#### 13. Rogers' paradox control: adapting the social-learning rate to staleness

- **Mechanism:** Mix inherited targets with the successor's own learning (self-labels or sparse feedback) at a per-region rate set by measured staleness: disagreement between `B0` and `B1` and the age of the ancestor. Copy the ancestor where the world is stable and learn individually where it drifted.
- **Novelty bet — improvement:** [2611.06022](https://arxiv.org/abs/2611.06022) separates lossy transmission from staleness in theory. This card makes the social/individual mix a controllable variable in model succession.
- **Cheapest test:** Multi-generation probe chains with varying drift. Compare a fixed mixing rate with the staleness-adaptive rate.
- **Old-task retention:** Untouched old tasks and the lineage-wide fossil rate.

#### 14. Oblique transmission with conformist and prestige biases

- **Mechanism:** Inherit from several ancestors (fine-tunes from different past generations and bases), weighted by a conformist bias (majority of ancestors) and a prestige bias (ancestors whose world matches `B1`'s). Each ancestor's private fossils are outvoted.
- **Novelty bet — primitive candidate:** This is cross-generational, not cross-fleet. PR #76's fleet consensus averages edits within one generation. The bet is that older ancestors with *different* fossils triangulate the skill better than the single most recent one.
- **Cheapest test:** Three ancestors with different world errors, each sharing skill S. Compare inheriting from the newest ancestor, uniform, conformist and prestige weighting.
- **Old-task retention:** Untouched old tasks, plus skills held by only one ancestor (minority skills should not be voted away).

#### 15. Lore: transmitting a compiled symbolic program

- **Mechanism:** The ancestor emits the skill as a short program or rule list, induced from its behavior with a program synthesizer, together with its preconditions on world facts. The successor runs or compiles the lore and re-grounds the preconditions against its own world.
- **Novelty bet — primitive candidate:** Symbolic lore separates *what to do* from *what the world is like* through explicit preconditions, which makes fossils inspectable. The bet is that lore survives base changes better than distributions for compositional skills.
- **Cheapest test:** A rule-based skill on the probe's inputs (thresholds on features). Synthesize with decision lists and compare re-grounded lore with plain KD.
- **Old-task retention:** Untouched old tasks, and skill when preconditions mention corrected world facts.

### D. Selection, lineage and latent inheritance

#### 16. Darwinian selection over inheritance subsets

- **Mechanism:** Spawn several cheap successor candidates, each inheriting a different subset of the ancestor's skills or regions. Select by a fitness that combines skill checks with the successor's own untouched competence, recombine the winners, and iterate.
- **Novelty bet — primitive candidate:** *What to inherit* becomes a combinatorial search with interactions (inheriting A may break B). [Selection is not learning](https://arxiv.org/abs/2610.22029) separates selection from update; the bet is that interactions make greedy or independent inheritance suboptimal.
- **Cheapest test:** Probe variants with 6 skills, 2 of which interact through shared world regions. Compare greedy selection, all-at-once inheritance and evolutionary subset search.
- **Old-task retention:** Untouched old tasks are part of fitness, so also report them on a held-out probe set not used for selection.

#### 17. An inheritance-debt ledger

- **Mechanism:** Tag every inherited behavior with provenance (generation, ancestor, evidence). Track which ones have no current support (no data, no verifier, contradicted by the base) as *inheritance debt*, and schedule audits or retirement by debt age.
- **Novelty bet — improvement:** Lineage attestation ([2601.11683](https://arxiv.org/abs/2601.11683)) proves ancestry; this card uses ancestry as an operational signal for what to stop trusting. Unlike Fleet Q2/Q3, it needs no prediction of truth, only provenance and support counts.
- **Cheapest test:** A 6-generation chain. Compare debt-guided retirement with uniform retention and age-only retirement.
- **Old-task retention:** Every earlier skill. Count a supported skill retired as debt as a failure.

#### 18. Latent (recessive) inheritance and re-emergence

- **Mechanism:** Measure traits that are inherited but not expressed: after plain KD followed by a short `B1` correction fine-tune, does the fossil or skill re-emerge after further unrelated fine-tuning? Build a detector that flags latent inherited traits before they resurface.
- **Novelty bet — primitive candidate:** [2609.25721](https://arxiv.org/abs/2609.25721) reports persistence alongside declining expression. Treating *re-emergence under later continual learning* as a forgetting-safety problem across generations is new for this repo.
- **Cheapest test:** The probe: KD, then correction, then an unrelated task. Measure the fossil rate at each stage, and the detector's AUROC from hidden-unit probes.
- **Old-task retention:** Skill retention through the unrelated task, compared with a successor that never inherited.

#### 19. Niche construction: inheriting the environment, not the model

- **Mechanism:** The ancestor leaves a modified environment instead of passing on weights or behavior: a tool library, a retrieval cache keyed by inputs, or a feature extractor exposed as a tool. The successor learns to use the niche and may overwrite it.
- **Novelty bet — primitive candidate:** Inheritance moves out of the learner. The bet is that a niche-mediated skill transfers across arbitrary architecture changes at a fossil rate controlled by the successor's own gating of the tool.
- **Cheapest test:** The probe with `F0` exposed as a callable tool on `Q`. `B1` learns when to call it, at a matched query budget compared with KD.
- **Old-task retention:** Untouched old tasks with the tool available and with it removed (dependency risk).

### E. Recombination and inferred objectives

#### 20. Sexual recombination of two ancestral lines

- **Mechanism:** Two independent lineages hold different skills and different fossils. The offspring inherits from both through crossover of their generated teaching corpora (regions chosen by each parent's competence), with conflict resolution by the disagreement gate.
- **Novelty bet — primitive candidate:** This tests whether recombination dilutes each parent's private fossils, through segregation, while combining skills. It differs from model merging because the parents' coordinates never meet.
- **Cheapest test:** Two parents with skills S1 and S2 and disjoint world errors. Compare offspring by crossover, by union KD, and inheriting from one parent.
- **Old-task retention:** Untouched old tasks and both skills, plus interference between them.

#### 21. Inferring the ancestor's objective, then re-optimizing it

- **Mechanism:** From `(B0, F0)` pairs on generic inputs, infer the *objective* that turns `B0` into `F0`, as a reward or loss on outputs, separated into terms that depend on the world and terms that do not. Re-optimize only the world-independent objective on `B1`.
- **Novelty bet — improvement:** Inverse value learning ([2410.21027](https://arxiv.org/abs/2410.21027)) transfers a value model. The bet here is decomposing the inferred objective by world dependence, so the successor optimizes the owner's intent rather than the ancestor's beliefs.
- **Cheapest test:** The probe with a parametric loss family. Check objective identification accuracy, then compare successor skill and fossils with the gate.
- **Old-task retention:** Untouched old tasks after re-optimization; regularize to `B1` only if the contract's tolerance is exceeded.

#### 22. A retirement interview: self-identified uniqueness before deprecation

- **Mechanism:** Before deprecation, the ancestor and successor play an adversarial query game. The ancestor searches for inputs where it is confident and the successor differs, and the successor labels each found disagreement as *mine (world correction)* or *yours (skill)* using its own consistency checks. Only "yours" items are inherited.
- **Novelty bet — improvement:** This turns the gate into an active, two-sided negotiation that finds rare skill regions passive sampling misses. The risk is that it collapses to card 3 with active sampling.
- **Cheapest test:** The probe with `Q` made rare (1% of generic inputs). Compare query-matched passive gating with the interview.
- **Old-task retention:** Untouched old tasks and corrections on `R\Q`; "mine" errors show up directly as fossils.

## Ranked deeper sub-questions

1. **Can a successor inherit a skill while refusing its ancestor's world?** Start with cards 1, 2 and 7. The probe gives the bar: beat the disagreement gate on skill *and* fossil rate with no more than 2 pp loss on untouched old tasks. Next, check skills that are conditioned on corrected facts, where the right inherited behavior is the ancestor's *rule* applied to the new world. The node's root hypothesis dies if no card beats the gate on any skill type.
2. **Is there a predictable Lamarck–Baldwin crossover in model succession?** Cards 5 and 8. Sweep world drift across 4+ generations and test whether the crossover point is predictable from B0/B1 disagreement measured before inheritance. A predictable crossover is a reusable decision rule; if one strategy dominates everywhere, stop.
3. **Can verified transmission ratchet across changing architectures?** Cards 11 and 10. Require monotone total competence over 8 generations with no early-skill decay, compared with a no-check repository and plain KD chains. Collapse or saturation would itself be a useful negative result relative to [2406.00392](https://arxiv.org/abs/2406.00392).
4. **Do inherited traits hide and resurface?** Card 18 combined with card 17. Measure whether fossils suppressed by correction re-emerge under later unrelated continual learning, and whether a detector or debt ledger predicts that before it happens.
5. **Can heritability be trained into the ancestor?** Card 9. Run this only after question 1 has a winner, because a germline artifact should beat the best post-hoc method on held-out successor architectures at equal bytes.
