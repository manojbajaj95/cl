# Long-run agent memory, batch 2: re-shelving a growing skill library

Source: Manoj's nested, book-style skill retrieval idea. The reviewer killed the plain version (HiSkill 2607.25853, SkillBrowser 2610.23554, SE-GoS 2609.08228, SkillDAG 2606.03056, TalentRL 2610.41143) and left open one long-run angle: re-shelving under continual growth breaks the navigation paths the agent relied on. This batch sharpens that angle.

## N1. Re-shelving breaks routing only when the routes are remembered: split-only hierarchies against rebuilds when navigation is consolidated

**Mechanism.** A hierarchical skill library (table of contents, then shelf, then skill) grows over thousands of episodes. Two maintenance policies exist. Periodic rebuild re-clusters everything (HiSkill, SE-GoS), which keeps shelves balanced. Append-only keeps old paths fixed, but its shelves overflow and drift off-topic. Whether a rebuild hurts depends on where navigation knowledge lives:
- A zero-shot agent that re-reads the table of contents every time loses nothing when shelves move. A better clustering should even help it.
- An agent whose routing is *learned*, whether consolidated into LoRA from its own navigation traces, or held in lessons and cached plans that cite paths ("billing exports live under Finance/Reports"), carries a map of the old shelving. A rebuild is then a distribution shift on its own memory, and old-skill hit rate drops after every rebuild.

That gives the falsifiable claim: **a crossover**. Rebuild ≥ stable for zero-shot navigation, and stable > rebuild for consolidated navigation, with the gap growing with the number of rebuilds. The proposal is a **split-only (B-tree-style) hierarchy** that keeps both balance and stability. A shelf that overflows may only split into children: no skill ever changes ancestors, every old path stays a valid prefix, and the new level is chosen by the agent at read time. This keeps routes stable without letting shelves overflow, which append-only can't do.

**Closest prior art.**
- Skill++ ([2611.00544](https://arxiv.org/abs/2611.00544)): in flat libraries, new skills displace old ones in metadata routing. Its fix rewrites only the new skill's metadata, keeping old metadata stable. Same stability intuition, but flat and with no hierarchy maintenance.
- Semantic-ID staleness in generative retrieval ([2604.13273](https://arxiv.org/abs/2604.13273)): rebuilding hierarchical IDs breaks a retriever's learned output space. This is the parametric analogue of re-shelving, for recommendation IDs, not agent skill navigation, and with alignment, not split-only, as the fix.
- Lost in Implicit Routing ([2610.18522](https://arxiv.org/abs/2610.18522)): flat skill routing collapses at 1,000 skills, which motivates the hierarchy.
- Adaptive Memory Index Evolution ([2610.34977](https://arxiv.org/abs/2610.34977)): learns persistent per-ID access weights and explicitly does not rebuild the host index.
- No paper found comparing rebuild, redirect and split-only maintenance over a long run, or splitting the effect by where routing knowledge is stored.

**Strongest control.** Rebuild plus a redirect table (old path → new location, consulted when the agent follows a stale path). This is the cheap fix any engineer would ship, and if it ties, split-only adds nothing. Also run:
- Flat dense top-k retrieval over skill descriptions: the simplest same-input baseline. If it matches the hierarchies, hierarchy maintenance is moot.
- Append-only with fixed shelves.
- Periodic rebuild with no redirects.

All arms get equal navigation-token budgets and the same skill bodies.

**Smallest falsifying test.**
- *Library:* a synthetic API-skill library of 2,000 skills arriving in 20 waves, whose topic mix drifts so the wave-1 taxonomy goes wrong.
- *Agent:* Qwen2.5-1.5B navigating the hierarchy.
- *Routing conditions:* (a) zero-shot table-of-contents reading; (b) routing consolidated by LoRA on its own successful navigation traces after each wave; (c) a path-citing lesson memory.
- *Arms:* the five maintenance arms above (proposal, redirect, flat, append-only, rebuild); rebuild every 4 waves; 3 seeds.
- *Metrics:* hit rate on wave-1–5 skills and on newest-wave skills, measured after every wave.

**Kill line** (any one kills it):
- The crossover does not appear: rebuild hurts consolidated routing by < 5 points of old-skill hit rate at wave 20.
- Split-only does not beat rebuild + redirect on old-skill hit rate by ≥ 5 points, beyond the seed CI, at new-skill accuracy within 2 points.
- Flat dense retrieval comes within 2 points of the best hierarchy at 2,000 skills.
- The split-only advantage does not grow from wave 8 to wave 20, so it is not a long-run effect.
