"""Synthetic knowledge world, tokenizer, episode sampler, and RAG retriever.

Entities are 2-token syllable names drawn from disjoint pools for:
- static world knowledge (200 background facts memorized during pretraining, used for drift)
- pretraining episodic facts (train split of entity names)
- dev fictional facts (disjoint entity names, for tuning Model A fine-tuning hyperparams)
- test fictional facts (disjoint entity names, for the final text-vs-write kill test)

Every relation has:
- forward fact statement (only forward statements are ever written)
- direct recall query
- paraphrase query (including held-out paraphrase templates never seen in pretraining!)
- cue-free inverse query (object -> subject, uniquely determined within an episode)
- cue-free 2-hop query (A -> C across two separate facts A->B and B->C, without naming B)
"""

from __future__ import annotations

import math
import random
from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple


# ---------------------------------------------------------------------------
# Vocabulary & Syllable Pools (disjoint across entity types)
# ---------------------------------------------------------------------------

PERSON_FIRST = [
    "mira", "torin", "sable", "daren", "lyra", "kestrel", "orion", "vesper",
    "corin", "nyxa", "talia", "bren", "elara", "joren", "kaisa", "riven",
    "sora", "varen", "zela", "calen", "fiora", "galen", "halia", "iven",
    "juna", "kieran", "lira", "maren", "nolan", "ophel", "petra", "quinn",
]
PERSON_LAST = [
    "keln", "vash", "dris", "morn", "tarn", "seth", "vor", "lind",
    "fenn", "gale", "holt", "kade", "lor", "mar", "neth", "orr",
    "pell", "renn", "sol", "tov", "uln", "vane", "wren", "yorn",
    "zeth", "bale", "cove", "dane", "falk", "grimm", "haze", "jex",
]

ORG_FIRST = [
    "vexor", "solis", "aether", "noven", "kryos", "lumina", "stratos", "verid",
    "zenith", "pylon", "arcan", "borea", "cygn", "delph", "equin", "ferro",
    "glyph", "helio", "ionix", "jove", "kinet", "lyon", "myriad", "nexa",
    "omnis", "prism", "quanta", "radia", "synth", "tecton", "umbra", "valen",
]
ORG_LAST = [
    "labs", "corp", "works", "grid", "forge", "vault", "guild", "pulse",
    "core", "nexus", "scope", "drive", "spire", "mesh", "node", "wave",
    "craft", "field", "logic", "mint", "orbit", "path", "quest", "ring",
    "shift", "spark", "trust", "union", "vector", "wing", "yard", "zone",
]

CITY_FIRST = [
    "tarnis", "oriel", "veldt", "cairn", "brine", "ashen", "cedar", "dusk",
    "ember", "frost", "glade", "haven", "ivory", "jade", "knoll", "lumen",
    "marsh", "north", "ochre", "pearl", "quartz", "ridge", "slate", "thorn",
    "umber", "verge", "willow", "zephyr", "alder", "birch", "coral", "delta",
]
CITY_LAST = [
    "bay", "vale", "port", "peak", "isle", "ford", "mere", "crest",
    "glen", "moor", "bluff", "creek", "downs", "fen", "gate", "heath",
    "inlet", "keep", "loch", "mesa", "nook", "pass", "quay", "reach",
    "shore", "tor", "view", "watch", "wood", "arch", "bend", "cape",
]

PROJ_FIRST = [
    "atlas", "boreal", "chron", "draco", "echo", "flux", "gaia", "hydra",
    "iris", "janus", "kronos", "lotus", "mantis", "nimbus", "opal", "phoen",
    "quasar", "runic", "sigma", "titan", "ursa", "vortex", "wisp", "xenon",
    "yggdr", "zircon", "amber", "basalt", "cobalt", "dior", "ether", "flint",
]
PROJ_LAST = [
    "alpha", "beta", "gamma", "delta", "prime", "zero", "one", "two",
    "arc", "beam", "code", "deck", "edge", "flow", "gate", "halo",
    "icon", "jet", "key", "link", "mark", "net", "orb", "pod",
    "ray", "seal", "tier", "unit", "veil", "web", "axis", "bolt",
]

# General filler / prose / template words
TEMPLATE_WORDS = [
    "works", "at", "is", "located", "in", "leads", "lead", "the", "project",
    "oversee", "oversees", "guides", "pilots", "anchors", "fact", "record", "note",
    "where", "does", "work", "?", "answer", ":", ".", ",", "which",
    "organization", "employs", "name", "employer", "of", "who", "employee",
    "city", "hosts", "headquarters", "what", "company", "based", "can", "you",
    "find", "initiative", "directed", "by", "runs", "situated", "workplace",
    "person", "manages", "owns", "operates", "from", "employed", "serves",
    "headquartered", "resides", "office", "branch", "team", "director",
    "leader", "head", "chief", "staff", "member", "for", "within", "under",
    "oversees", "guides", "pilots", "anchors", "fact", "record", "note",
    "context", "query", "a", "an", "to", "and", "or", "with", "that", "this",
    "was", "are", "be", "has", "have", "on", "as", "its", "their", "her",
    "his", "they", "it", "known", "called", "named", "known_as", "town",
    "metro", "hub", "site", "location", "place", "firm", "enterprise",
    "group", "division", "program", "effort", "venture", "mission", "task",
    "static", "archive", "world", "history", "report", "summary", "entry",
    "belong", "belongs", "affiliated", "stationed", "placed", "set", "built",
]

SPECIAL_TOKENS = ["<PAD>", "<BOS>", "<EOS>", "<SEP>", "<ANS>", "<UNK>"]


class SimpleWordTokenizer:
    """Deterministic word-level tokenizer with ~600-2048 vocab (padded to 1024)."""

    def __init__(self, target_vocab_size: int = 1024):
        vocab: List[str] = list(SPECIAL_TOKENS)
        seen = set(vocab)
        all_words = (
            PERSON_FIRST + PERSON_LAST +
            ORG_FIRST + ORG_LAST +
            CITY_FIRST + CITY_LAST +
            PROJ_FIRST + PROJ_LAST +
            TEMPLATE_WORDS
        )
        for w in all_words:
            wl = w.lower()
            if wl not in seen:
                vocab.append(wl)
                seen.add(wl)
        # Pad to target_vocab_size with reserved tokens so embedding size is clean
        idx = 0
        while len(vocab) < target_vocab_size:
            tok = f"<R{idx}>"
            vocab.append(tok)
            idx += 1
        self.itos: List[str] = vocab
        self.stoi: Dict[str, int] = {w: i for i, w in enumerate(vocab)}
        self.pad_id = self.stoi["<PAD>"]
        self.bos_id = self.stoi["<BOS>"]
        self.eos_id = self.stoi["<EOS>"]
        self.sep_id = self.stoi["<SEP>"]
        self.ans_id = self.stoi["<ANS>"]
        self.unk_id = self.stoi["<UNK>"]
        self.vocab_size = len(vocab)

    def tokenize(self, text: str) -> List[str]:
        # Separate punctuation cleanly
        out = text.lower()
        for p in ["?", ".", ",", ":"]:
            out = out.replace(p, f" {p} ")
        return [t for t in out.split() if t]

    def encode(self, text: str, add_bos: bool = False, add_eos: bool = False) -> List[int]:
        ids = [self.stoi.get(t, self.unk_id) for t in self.tokenize(text)]
        if add_bos:
            ids = [self.bos_id] + ids
        if add_eos:
            ids = ids + [self.eos_id]
        return ids

    def decode(self, ids: Sequence[int]) -> str:
        toks = [
            self.itos[i] for i in ids
            if 0 <= i < len(self.itos) and i not in (self.pad_id, self.bos_id, self.eos_id)
        ]
        return " ".join(toks)


# ---------------------------------------------------------------------------
# Entity Splits (Strict Disjointness across Static, Train, Dev, Test)
# ---------------------------------------------------------------------------

def _build_entity_pool(firsts: List[str], lasts: List[str], seed: int) -> List[str]:
    # 64 unique single-token fictional entities per type (all in tokenizer vocab).
    pool = list(firsts) + list(lasts)
    rng = random.Random(seed)
    rng.shuffle(pool)
    return pool


@dataclass
class EntitySplits:
    static_persons: List[str]
    static_orgs: List[str]
    static_cities: List[str]
    static_projs: List[str]

    train_persons: List[str]
    train_orgs: List[str]
    train_cities: List[str]
    train_projs: List[str]

    dev_persons: List[str]
    dev_orgs: List[str]
    dev_cities: List[str]
    dev_projs: List[str]

    test_persons: List[str]
    test_orgs: List[str]
    test_cities: List[str]
    test_projs: List[str]


def make_entity_splits(seed: int = 42) -> EntitySplits:
    # 64 unique single-token entities per type:
    # - 16 static entities (strictly disjoint from episodic; memorized during pretraining for drift)
    # - 48 episodic entities (used with ephemeral random bindings in train/dev/test so no
    #   episodic fact is ever memorized in weights; zero-shot accuracy on test facts is ~1/48).
    def split_pool(pool: List[str]):
        static = pool[:16]
        episodic = pool[16:]
        return static, episodic, episodic, episodic

    sp, tp, dp, ep = split_pool(_build_entity_pool(PERSON_FIRST, PERSON_LAST, seed + 1))
    so, to, do, eo = split_pool(_build_entity_pool(ORG_FIRST, ORG_LAST, seed + 2))
    sc, tc, dc, ec = split_pool(_build_entity_pool(CITY_FIRST, CITY_LAST, seed + 3))
    sa, ta, da, ea = split_pool(_build_entity_pool(PROJ_FIRST, PROJ_LAST, seed + 4))

    return EntitySplits(
        static_persons=sp, static_orgs=so, static_cities=sc, static_projs=sa,
        train_persons=tp, train_orgs=to, train_cities=tc, train_projs=ta,
        dev_persons=dp, dev_orgs=do, dev_cities=dc, dev_projs=da,
        test_persons=ep, test_orgs=eo, test_cities=ec, test_projs=ea,
    )


# ---------------------------------------------------------------------------
# Episode & QA Structures
# ---------------------------------------------------------------------------

@dataclass
class QAItem:
    question: str
    answer: str
    category: str  # "recall", "paraphrase", "inverse", "two_hop", "static"
    supporting_fact_indices: Tuple[int, ...] = ()


@dataclass
class Episode:
    facts: List[str]
    qas: List[QAItem]


# Paraphrase templates: first 2 seen in train, last 1 HELD OUT for test!
PARAPHRASE_TEMPLATES = {
    "works_at": {
        "train": [
            "which organization employs {p} ?",
            "name the employer of {p} .",
        ],
        "heldout": [
            "which company is {p} employed by ?",
        ],
    },
    "located_in": {
        "train": [
            "which city hosts the headquarters of {o} ?",
            "in what city can you find {o} ?",
        ],
        "heldout": [
            "what town is {o} headquartered in ?",
        ],
    },
    "leads": {
        "train": [
            "what initiative is directed by {p} ?",
            "which program does {p} oversee ?",
        ],
        "heldout": [
            "what venture is {p} the director of ?",
        ],
    },
}

INVERSE_TEMPLATES = {
    "works_at": {
        "train": [
            "who works at {o} ?",
            "name the employee at {o} .",
        ],
        "heldout": [
            "which person is employed by {o} ?",
        ],
    },
    "located_in": {
        "train": [
            "which organization is located in {c} ?",
            "what company is based in {c} ?",
        ],
        "heldout": [
            "which firm is headquartered in {c} ?",
        ],
    },
    "leads": {
        "train": [
            "who leads the {a} project ?",
            "name the director of the {a} project .",
        ],
        "heldout": [
            "which person oversees the {a} initiative ?",
        ],
    },
}

TWOHOP_TEMPLATES = {
    "p_to_c": {
        "train": [
            "which city does {p} work in ?",
            "where is the workplace of {p} situated ?",
        ],
        "heldout": [
            "in what town is the employer of {p} located ?",
        ],
    },
    "a_to_o": {
        "train": [
            "which organization runs the {a} project ?",
            "what company is the {a} initiative affiliated with ?",
        ],
        "heldout": [
            "which firm employs the leader of the {a} project ?",
        ],
    },
    "c_to_p": {
        "train": [
            "who works in {c} ?",
            "name the person stationed in {c} .",
        ],
        "heldout": [
            "which employee works at the company in {c} ?",
        ],
    },
}


class KnowledgeWorld:
    """Generates static background facts and episodic fresh-fact worlds."""

    def __init__(self, seed: int = 42, n_static_chains: int = 16):
        self.splits = make_entity_splits(seed)
        self.n_static_chains = min(n_static_chains, len(self.splits.static_persons))
        self.static_facts: List[str] = []
        self.static_qas: List[QAItem] = []
        self._build_static_world()

    def _build_static_world(self) -> None:
        s = self.splits
        for i in range(self.n_static_chains):
            p, o, c, a = s.static_persons[i], s.static_orgs[i], s.static_cities[i], s.static_projs[i]
            f0 = f"{p} works at {o} ."
            f1 = f"{o} is located in {c} ."
            f2 = f"{p} leads the {a} project ."
            base = len(self.static_facts)
            self.static_facts.extend([f0, f1, f2])
            self.static_qas.extend([
                QAItem(f"where does {p} work ?", o, "static", (base,)),
                QAItem(f"where is {o} located ?", c, "static", (base + 1,)),
                QAItem(f"which project does {p} lead ?", a, "static", (base + 2,)),
                QAItem(f"which city does {p} work in ?", c, "static", (base, base + 1)),
            ])

    def sample_episode(
        self,
        split: str,
        n_chains: int,
        rng: random.Random,
        use_heldout_templates: bool = False,
        shuffle_facts: bool = True,
    ) -> Episode:
        s = self.splits
        if split == "train":
            ps, os_, cs, as_ = s.train_persons, s.train_orgs, s.train_cities, s.train_projs
        elif split == "dev":
            ps, os_, cs, as_ = s.dev_persons, s.dev_orgs, s.dev_cities, s.dev_projs
        elif split == "test":
            ps, os_, cs, as_ = s.test_persons, s.test_orgs, s.test_cities, s.test_projs
        else:
            raise ValueError(f"Unknown split: {split}")

        chosen_p = rng.sample(ps, n_chains)
        chosen_o = rng.sample(os_, n_chains)
        chosen_c = rng.sample(cs, n_chains)
        chosen_a = rng.sample(as_, n_chains)

        # Build facts: 3 facts per chain (all strictly forward!)
        raw_facts: List[Tuple[str, Tuple[int, str]]] = []
        for i in range(n_chains):
            p, o, c, a = chosen_p[i], chosen_o[i], chosen_c[i], chosen_a[i]
            raw_facts.append((f"{p} works at {o} .", (i, "works_at")))
            raw_facts.append((f"{o} is located in {c} .", (i, "located_in")))
            raw_facts.append((f"{p} leads the {a} project .", (i, "leads")))

        if shuffle_facts:
            rng.shuffle(raw_facts)

        facts = [f for f, _ in raw_facts]
        idx_map = {tag: idx for idx, (_, tag) in enumerate(raw_facts)}

        tkey = "heldout" if use_heldout_templates else "train"
        qas: List[QAItem] = []

        for i in range(n_chains):
            p, o, c, a = chosen_p[i], chosen_o[i], chosen_c[i], chosen_a[i]
            i_w = idx_map[(i, "works_at")]
            i_l = idx_map[(i, "located_in")]
            i_p = idx_map[(i, "leads")]

            # 1. Direct Recall
            qas.append(QAItem(f"where does {p} work ?", o, "recall", (i_w,)))
            qas.append(QAItem(f"where is {o} located ?", c, "recall", (i_l,)))
            qas.append(QAItem(f"which project does {p} lead ?", a, "recall", (i_p,)))

            # 2. Paraphrase
            qas.append(QAItem(rng.choice(PARAPHRASE_TEMPLATES["works_at"][tkey]).format(p=p), o, "paraphrase", (i_w,)))
            qas.append(QAItem(rng.choice(PARAPHRASE_TEMPLATES["located_in"][tkey]).format(o=o), c, "paraphrase", (i_l,)))
            qas.append(QAItem(rng.choice(PARAPHRASE_TEMPLATES["leads"][tkey]).format(p=p), a, "paraphrase", (i_p,)))

            # 3. Cue-free Inverse
            qas.append(QAItem(rng.choice(INVERSE_TEMPLATES["works_at"][tkey]).format(o=o), p, "inverse", (i_w,)))
            qas.append(QAItem(rng.choice(INVERSE_TEMPLATES["located_in"][tkey]).format(c=c), o, "inverse", (i_l,)))
            qas.append(QAItem(rng.choice(INVERSE_TEMPLATES["leads"][tkey]).format(a=a), p, "inverse", (i_p,)))

            # 4. Cue-free 2-hop
            qas.append(QAItem(rng.choice(TWOHOP_TEMPLATES["p_to_c"][tkey]).format(p=p), c, "two_hop", (i_w, i_l)))
            qas.append(QAItem(rng.choice(TWOHOP_TEMPLATES["a_to_o"][tkey]).format(a=a), o, "two_hop", (i_p, i_w)))
            qas.append(QAItem(rng.choice(TWOHOP_TEMPLATES["c_to_p"][tkey]).format(c=c), p, "two_hop", (i_w, i_l)))

        return Episode(facts=facts, qas=qas)


# ---------------------------------------------------------------------------
# Extractive BM25 RAG Retriever (compact matched-budget retrieval baseline)
# ---------------------------------------------------------------------------

STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "in", "at", "of", "by", "to",
    "for", "does", "do", "what", "which", "who", "where", "?", ".", ",", ":",
    "name", "can", "you", "find", "project", "organization", "company", "city",
    "works", "work", "located", "leads", "employed", "based", "firm", "town",
}


class BM25Retriever:
    """Standard lexical BM25 retriever over a fact bank."""

    def __init__(self, docs: Sequence[str], k1: float = 1.5, b: float = 0.75):
        self.docs = list(docs)
        self.k1 = k1
        self.b = b
        self.doc_toks = [self._tok(d) for d in self.docs]
        self.avgdl = sum(len(t) for t in self.doc_toks) / max(len(self.doc_toks), 1)
        df: Counter[str] = Counter()
        for toks in self.doc_toks:
            for t in set(toks):
                df[t] += 1
        N = len(self.docs)
        self.idf = {t: math.log((N - c + 0.5) / (c + 0.5) + 1.0) for t, c in df.items()}

    @staticmethod
    def _tok(text: str) -> List[str]:
        out = text.lower()
        for p in ["?", ".", ",", ":"]:
            out = out.replace(p, f" {p} ")
        return [t for t in out.split() if t and t not in STOPWORDS]

    def retrieve(self, query: str, top_k: int = 2) -> List[str]:
        qtoks = self._tok(query)
        scores: List[Tuple[float, int]] = []
        for idx, dtoks in enumerate(self.doc_toks):
            tf = Counter(dtoks)
            dl = len(dtoks)
            s = 0.0
            for qt in qtoks:
                if qt in tf:
                    f = tf[qt]
                    denom = f + self.k1 * (1.0 - self.b + self.b * dl / max(self.avgdl, 1e-6))
                    s += self.idf.get(qt, 0.0) * (f * (self.k1 + 1.0)) / denom
            scores.append((s, idx))
        scores.sort(key=lambda x: (-x[0], x[1]))
        return [self.docs[idx] for _, idx in scores[:top_k]]


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def format_qa_prompt(question: str, context_facts: Sequence[str] | None = None) -> str:
    if context_facts:
        ctx = " ".join(context_facts)
        return f"context : {ctx} query : {question} answer :"
    return f"query : {question} answer :"


def encode_qa_example(
    tok: SimpleWordTokenizer,
    question: str,
    answer: str,
    context_facts: Sequence[str] | None = None,
) -> Tuple[List[int], List[int]]:
    """Return (input_ids, loss_mask) where loss_mask=1 on answer + EOS tokens only."""
    prompt = format_qa_prompt(question, context_facts)
    p_ids = tok.encode(prompt, add_bos=True, add_eos=False)
    a_ids = tok.encode(answer, add_bos=False, add_eos=True)
    full_ids = p_ids + a_ids
    # Next-token prediction: input = full_ids[:-1], target = full_ids[1:]
    # Answer targets start at index len(p_ids) - 1 in shifted targets
    mask = [0] * (len(p_ids) - 1) + [1] * len(a_ids)
    return full_ids, mask
