"""Five procedurally generated two-way tasks, scored by the two label tokens."""
import random
import zlib


def stable_seed(*parts):
    """Process-independent seed (Python's str hash is salted per process)."""
    return zlib.crc32(repr(parts).encode())

MAMMALS = "dog cat horse cow pig sheep goat lion tiger bear wolf fox deer rabbit mouse rat bat whale dolphin elephant giraffe zebra monkey gorilla kangaroo koala panda camel donkey otter seal walrus beaver squirrel hedgehog leopard cheetah hippo rhino moose buffalo hamster ferret badger skunk raccoon llama yak bison weasel mole".split()
NONMAMMALS = "eagle sparrow parrot owl penguin ostrich pigeon crow duck swan shark salmon tuna trout goldfish cod eel snake lizard turtle crocodile alligator frog toad newt salamander ant bee wasp beetle spider butterfly moth fly mosquito lobster crab shrimp octopus squid snail worm jellyfish starfish iguana gecko chameleon flamingo hawk falcon".split()
POS = "wonderful excellent delightful superb brilliant lovely amazing fantastic charming pleasant joyful marvelous splendid terrific outstanding beautiful enjoyable impressive fabulous glorious".split()
NEG = "terrible awful dreadful horrible boring disappointing miserable dull ugly unpleasant poor annoying painful tedious lousy dismal awful gloomy nasty pathetic".split()
NOUNS = "movie meal trip concert book show hotel party game lecture service performance visit dinner flight song play class event ride".split()
EUROPE = "France Germany Italy Spain Portugal Poland Sweden Norway Finland Denmark Austria Belgium Netherlands Greece Hungary Ireland Switzerland Romania Bulgaria Croatia Serbia Slovakia Slovenia Estonia Latvia Lithuania Iceland Ukraine Albania Czechia".split()
ASIA = "China Japan India Thailand Vietnam Indonesia Malaysia Philippines Korea Pakistan Bangladesh Nepal Mongolia Cambodia Laos Myanmar Iran Iraq Afghanistan Kazakhstan Uzbekistan Singapore Bhutan Oman Qatar Kuwait Jordan Syria Yemen Taiwan".split()

TASKS = ["parity", "mammal", "sentiment", "compare", "continent"]
LABELS = {
    "parity": (" even", " odd"),
    "mammal": (" yes", " no"),
    "sentiment": (" positive", " negative"),
    "compare": (" first", " second"),
    "continent": (" Europe", " Asia"),
}


def _split(words, seed):
    w = sorted(set(words))
    random.Random(seed).shuffle(w)
    k = int(len(w) * 0.6)
    return w[:k], w[k:]


def make_items(task, split, n, seed):
    """Returns list of (prompt, label_index). Word-list tasks use disjoint train/test words."""
    rng = random.Random(stable_seed(task, split, seed))
    out = []
    for _ in range(n):
        if task == "parity":
            x = rng.randrange(100, 10000)
            if split == "test":
                x = x * 2 + 1 if rng.random() < 0.5 else x * 2  # different range
            out.append((f"Task: parity. Number: {x}. Is it even or odd? Answer:", x % 2))
        elif task == "compare":
            lo, hi = (10, 500) if split == "train" else (500, 999)
            a, b = rng.sample(range(lo, hi), 2)
            out.append((f"Task: compare. Which is larger, {a} or {b}? Answer:", 0 if a > b else 1))
        elif task == "mammal":
            tr_m, te_m = _split(MAMMALS, 1)
            tr_n, te_n = _split(NONMAMMALS, 2)
            m, nm = (tr_m, tr_n) if split == "train" else (te_m, te_n)
            y = rng.randrange(2)
            w = rng.choice(m if y == 0 else nm)
            out.append((f"Task: mammal. Animal: {w}. Is it a mammal? Answer:", y))
        elif task == "sentiment":
            tr_p, te_p = _split(POS, 3)
            tr_n, te_n = _split(NEG, 4)
            p, ng = (tr_p, tr_n) if split == "train" else (te_p, te_n)
            y = rng.randrange(2)
            adj = rng.choice(p if y == 0 else ng)
            noun = rng.choice(NOUNS)
            out.append((f"Task: sentiment. Review: The {noun} was {adj}. Sentiment? Answer:", y))
        elif task == "continent":
            tr_e, te_e = _split(EUROPE, 5)
            tr_a, te_a = _split(ASIA, 6)
            e, a = (tr_e, tr_a) if split == "train" else (te_e, te_a)
            y = rng.randrange(2)
            c = rng.choice(e if y == 0 else a)
            out.append((f"Task: continent. Country: {c}. Europe or Asia? Answer:", y))
    return out
