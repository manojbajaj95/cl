"""Real anchors, synthetic local facts, and held-out question families."""

import random
from dataclasses import dataclass
from math import log10

import numpy as np


CITIES = """Reykjavik 64.15 -21.94
Oslo 59.91 10.75
Helsinki 60.17 24.94
Stockholm 59.33 18.07
Moscow 55.76 37.62
Edinburgh 55.95 -3.19
Dublin 53.35 -6.26
Berlin 52.52 13.41
Amsterdam 52.37 4.90
London 51.51 -0.13
Brussels 50.85 4.35
Prague 50.08 14.42
Paris 48.86 2.35
Vienna 48.21 16.37
Budapest 47.50 19.04
Munich 48.14 11.58
Zurich 47.38 8.54
Milan 45.46 9.19
Lyon 45.76 4.84
Venice 45.44 12.32
Rome 41.90 12.50
Madrid 40.42 -3.70
Lisbon 38.72 -9.14
Athens 37.98 23.73
Istanbul 41.01 28.98
Cairo 30.04 31.24
Casablanca 33.57 -7.59
Lagos 6.52 3.38
Nairobi -1.29 36.82
Cape Town -33.92 18.42
Johannesburg -26.20 28.05
Dubai 25.20 55.27
Jerusalem 31.77 35.21
Tehran 35.69 51.39
Mumbai 19.08 72.88
Delhi 28.61 77.21
Bangkok 13.76 100.50
Singapore 1.35 103.82
Jakarta -6.21 106.85
Beijing 39.90 116.41
Shanghai 31.23 121.47
Seoul 37.57 126.98
Tokyo 35.68 139.69
Manila 14.60 120.98
Sydney -33.87 151.21
Melbourne -37.81 144.96
Auckland -36.85 174.76
Vancouver 49.28 -123.12
Seattle 47.61 -122.33
San Francisco 37.77 -122.42
Los Angeles 34.05 -118.24
Denver 39.74 -104.99
Chicago 41.88 -87.63
Toronto 43.65 -79.38
Boston 42.36 -71.06
New York 40.71 -74.01
Washington DC 38.91 -77.04
Miami 25.76 -80.19
Mexico City 19.43 -99.13
Havana 23.11 -82.37
Bogota 4.71 -74.07
Lima -12.05 -77.04
Santiago -33.45 -70.67
Buenos Aires -34.60 -58.38
Rio de Janeiro -22.91 -43.17
Sao Paulo -23.55 -46.63"""

PEOPLE = """Socrates 470
Plato 428
Aristotle 384
Alexander the Great 356
Julius Caesar 100
Cleopatra 69
Augustus 63
Jesus 4
Nero 37
Marcus Aurelius 121
Constantine the Great 272
Muhammad 570
Charlemagne 742
Genghis Khan 1162
Marco Polo 1254
Dante Alighieri 1265
Joan of Arc 1412
Christopher Columbus 1451
Leonardo da Vinci 1452
Michelangelo 1475
Nicolaus Copernicus 1473
Martin Luther 1483
Galileo Galilei 1564
William Shakespeare 1564
René Descartes 1596
Isaac Newton 1643
Johann Sebastian Bach 1685
Benjamin Franklin 1706
George Washington 1732
Wolfgang Amadeus Mozart 1756
Ludwig van Beethoven 1770
Napoleon Bonaparte 1769
Jane Austen 1775
Charles Babbage 1791
Mary Shelley 1797
Charles Darwin 1809
Abraham Lincoln 1809
Ada Lovelace 1815
Karl Marx 1818
Queen Victoria 1819
Louis Pasteur 1822
Mark Twain 1835
Thomas Edison 1847
Oscar Wilde 1854
Nikola Tesla 1856
Marie Curie 1867
Mahatma Gandhi 1869
Winston Churchill 1874
Albert Einstein 1879
Virginia Woolf 1882
Charlie Chaplin 1889
J. R. R. Tolkien 1892
Walt Disney 1901
Frida Kahlo 1907
Alan Turing 1912
Rosa Parks 1913
Nelson Mandela 1918
Queen Elizabeth II 1926
Martin Luther King Jr. 1929
Neil Armstrong 1930
Muhammad Ali 1942
Stephen Hawking 1942
David Bowie 1947
Steve Jobs 1955
Barack Obama 1961
Taylor Swift 1989"""


@dataclass(frozen=True)
class Axis:
    positive: str
    negative: str
    noun: str
    unit: str
    anchors: dict[str, float]

    def phrase(self, positive: bool) -> str:
        return self.positive if positive else self.negative

    @property
    def noun_singular(self) -> str:
        return {"cities": "city", "people": "person", "elements": "element", "animals": "animal"}[self.noun]

    @property
    def statement_verb(self) -> str:
        return {"cities": "is", "people": "was", "elements": "has", "animals": "is"}[self.noun]

    @property
    def question_verb(self) -> str:
        return self.statement_verb.capitalize() if self.noun != "elements" else "Does"


CITY_ROWS = [(name, float(lat), float(lon))
             for name, lat, lon in (row.rsplit(" ", 2) for row in CITIES.splitlines())]
PERSON_ROWS = [(name, int(year)) for name, year in
               (row.rsplit(" ", 1) for row in PEOPLE.splitlines())]
ELEMENTS = """Hydrogen Helium Lithium Beryllium Boron Carbon Nitrogen Oxygen Fluorine
Neon Sodium Magnesium Aluminium Silicon Phosphorus Sulfur Chlorine Argon Potassium Calcium
Scandium Titanium Vanadium Chromium Manganese Iron Cobalt Nickel Copper Zinc Gallium Germanium
Arsenic Selenium Bromine Krypton Rubidium Strontium Yttrium Zirconium Niobium Molybdenum
Technetium Ruthenium Rhodium Palladium Silver Cadmium Indium Tin Antimony Tellurium Iodine Xenon
Caesium Barium Lanthanum Cerium Praseodymium Neodymium Promethium Samarium Europium Gadolinium
Terbium Dysprosium Holmium Erbium Thulium Ytterbium Lutetium Hafnium Tantalum Tungsten Rhenium
Osmium Iridium Platinum Gold Mercury Thallium Lead Bismuth Polonium Astatine Radon Francium
Radium Actinium Thorium Protactinium Uranium""".split()

ANIMALS = """Blue whale 110000
Humpback whale 30000
Orca 5000
African elephant 5500
White rhinoceros 2200
Hippopotamus 1500
Giraffe 1000
American bison 700
Polar bear 430
Grizzly bear 280
Pygmy hippopotamus 230
Siberian tiger 220
African lion 180
Western gorilla 145
Ostrich 110
Giant panda 100
Red kangaroo 65
Gray wolf 45
Cheetah 50
Chimpanzee 50
Capybara 55
Emperor penguin 30
Coyote 14
Eurasian lynx 20
European badger 11
Raccoon 8
Red fox 6
European wildcat 4
European rabbit 2
Guinea pig 0.9
Meerkat 0.75
Red squirrel 0.32
Norway rat 0.32
European hedgehog 0.8
Golden hamster 0.12
European mole 0.09
House mouse 0.021
Common shrew 0.010
Bee hummingbird 0.002
Ruby-throated hummingbird 0.0035
House sparrow 0.03
American robin 0.077
Mourning dove 0.13
Rock pigeon 0.31
Mallard 1.1
Bald eagle 4.5
Wild turkey 6
Mute swan 10
Galapagos tortoise 190
Green sea turtle 140
Komodo dragon 75
Saltwater crocodile 520
American alligator 270
Green iguana 4
Leopard gecko 0.06
Fire salamander 0.030
Great white shark 950
Whale shark 15000
Ocean sunfish 450
Atlantic bluefin tuna 240
Atlantic salmon 4.5
Common goldfish 0.08
Clownfish 0.012
Guppy 0.0009
Honey bee 0.0001
Housefly 0.000014
Monarch butterfly 0.0005
Goliath beetle 0.035
Goliath birdeater 0.15
Ladybug 0.00002"""

AXES = {
    "latitude": Axis("north of", "south of", "cities", "latitude",
                     {name: lat for name, lat, _ in CITY_ROWS}),
    "longitude": Axis("east of", "west of", "cities", "longitude",
                      {name: lon for name, _, lon in CITY_ROWS if name != "Auckland"}),
    "birth": Axis("born after", "born before", "people", "birth year",
                  {name: -year if i < 8 else year
                   for i, (name, year) in enumerate(PERSON_ROWS)}),
    "atomic": Axis("a higher atomic number than", "a lower atomic number than", "elements",
                   "atomic number", {name: i for i, name in enumerate(ELEMENTS, 1)}),
    "mass": Axis("heavier than", "lighter than", "animals", "body mass in kg",
                 {name: log10(float(mass)) for name, mass in
                  (row.rsplit(" ", 1) for row in ANIMALS.splitlines())}),
}


@dataclass(frozen=True)
class Question:
    a: str
    b: str
    positive: bool
    yes: bool
    family: str


@dataclass(frozen=True)
class Statement:
    a: str
    b: str
    positive: bool

    def text(self, axis: Axis) -> str:
        return f"{self.a} {axis.statement_verb} {axis.phrase(self.positive)} {self.b}."


def split_anchors(axis: Axis, seed: int):
    """Keep train/calibration/test subsets spread across the coordinate range."""
    ordered = sorted(axis.anchors, key=axis.anchors.get)
    rng = random.Random(seed)
    train, calibration, test = [], [], []
    for i in range(0, len(ordered), 5):
        group = ordered[i:i + 5]
        rng.shuffle(group)
        train.extend(group[:3])
        calibration.extend(group[3:4])
        test.extend(group[4:])
    return train, calibration, test


def balanced_pair(a, b, a_greater, family):
    return [Question(a, b, polarity, polarity == a_greater, family)
            for polarity in (True, False)]


def real_questions(axis: Axis, names, minimum, seed, max_pairs=20):
    pairs = [(a, b) for i, a in enumerate(names) for b in names[i + 1:]
             if abs(axis.anchors[a] - axis.anchors[b]) >= minimum
             and (axis.unit != "longitude" or abs(axis.anchors[a] - axis.anchors[b]) < 180)]
    random.Random(seed).shuffle(pairs)
    return [q for a, b in pairs[:max_pairs] for left, right in ((a, b), (b, a))
            for q in balanced_pair(left, right, axis.anchors[left] > axis.anchors[right], "real")]


def causal_pairs(axis: Axis, names, minimum, seed, cases=12):
    """Replace a real anchor's coordinate by one across a fixed comparator."""
    ordered = sorted(names, key=axis.anchors.get)
    triples = [(lo, mid, hi) for i, lo in enumerate(ordered)
               for j, mid in enumerate(ordered[i + 1:], i + 1) for hi in ordered[j + 1:]
               if axis.anchors[mid] - axis.anchors[lo] >= minimum
               and axis.anchors[hi] - axis.anchors[mid] >= minimum
               and (axis.unit != "longitude" or axis.anchors[hi] - axis.anchors[lo] < 180)]
    random.Random(seed).shuffle(triples)
    result = []
    for i, (lo, mid, hi) in enumerate(triples[:cases]):
        source, target = (lo, hi) if i % 2 == 0 else (hi, lo)
        for a, b in ((source, mid), (mid, source)):
            result.extend((q, source, target) for q in balanced_pair(
                a, b, axis.anchors[a] > axis.anchors[b], "causal"))
    return result


def fictional_names(n, seed):
    rng = random.Random(seed)
    onsets = "b br d dr f fl g gl k kr l m n p r s sh t th v w z".split()
    middles = "ava eri ulo yne oi ale ira ena ovi ara umi ath osi evi ao".split()
    endings = "den vos thal mek ryn nar sel vig nus mel tis lon rek nor ves".split()
    names = set()
    result = []
    while len(result) < n:
        name = "".join(rng.choice(part) for part in (onsets, middles, endings)).capitalize()
        if name not in names:
            result.append(name)
            names.add(name)
    return result


def make_world(axis: Axis, names, chains, seed, min_known_gap=0.1):
    """Each fictional entity has two neighboring statements; no query conclusions stored."""
    if chains < 2 or chains % 2:
        raise ValueError("Use a positive even number of chains for paired known comparators")
    rng = random.Random(seed)
    ordered = sorted(names, key=axis.anchors.get)
    n = len(ordered)
    coord = axis.anchors
    brackets = [(lo, hi) for i, lo in enumerate(ordered)
                for hi in ordered[i + max(2, n // 5):] if coord[lo] < coord[hi]]
    candidates = []
    for i, first in enumerate(ordered):
        for second in ordered[i + 1:]:
            below = [(lo, hi) for lo, hi in brackets if coord[first] - coord[hi] >= min_known_gap
                     and (axis.unit != "longitude" or coord[second] - coord[lo] < 180)]
            above = [(lo, hi) for lo, hi in brackets if coord[lo] - coord[second] >= min_known_gap
                     and (axis.unit != "longitude" or coord[hi] - coord[first] < 180)]
            if below and above:
                candidates.append(((first, second), below, above))
    if not candidates:
        raise ValueError("No pair of real comparators can be bracketed on both sides")
    rng.shuffle(candidates)
    layout = []
    for i in range(chains // 2):
        comparisons, below, above = candidates[i % len(candidates)]
        layout.extend(((rng.choice(below), comparisons, False),
                       (rng.choice(above), comparisons, True)))
    made = fictional_names(4 * chains, seed + 11)
    facts, questions, witnesses = [], [], []
    for i, ((lo, hi), comparisons, above) in enumerate(layout):
        a, b, c, d = made[4 * i:4 * i + 4]
        chain = [lo, a, b, c, d, hi]
        new, anchor = (a, lo) if above else (d, hi)
        witnesses.extend((new, anchor, comparator, i // 2) for comparator in comparisons)
        local = [Statement(high, low, True) if rng.randrange(2)
                 else Statement(low, high, False) for low, high in zip(chain, chain[1:])]
        facts.extend(local)
        for fact in local:
            questions.extend(balanced_pair(fact.a, fact.b, fact.positive, "stated"))
            questions.extend(balanced_pair(fact.b, fact.a, not fact.positive, "inverse"))
        for comparator in comparisons:
            questions.extend(balanced_pair(new, comparator, above, "two_hop"))
            questions.extend(balanced_pair(comparator, new, not above, "two_hop"))
        for left, right in ((a, c), (b, d), (a, d)):
            questions.extend(balanced_pair(left, right, False, "transitive"))
            questions.extend(balanced_pair(right, left, True, "transitive"))
    rng.shuffle(facts)
    rng.shuffle(questions)
    return made, facts, questions, witnesses


def solve_coordinates(entities, facts, anchors):
    """Closed-form fit: least-squares coordinates AND one free step per chain.

    Every row is c(high) - c(low) - step(chain) = 0, with frozen anchor readouts
    moved to the right-hand side. In the constructed worlds the unique solution
    is equally spaced interpolation between each chain's two anchors.
    """
    columns = {name: i for i, name in enumerate(entities)}
    # Chains are generated in blocks of four entities; facts can be in any order.
    matrix = np.zeros((len(facts), len(entities) + len(entities) // 4))
    target = np.zeros(len(facts))
    for i, fact in enumerate(facts):
        high, low = (fact.a, fact.b) if fact.positive else (fact.b, fact.a)
        chain = columns[high if high in columns else low] // 4
        matrix[i, len(entities) + chain] = -1
        for name, sign in ((high, 1), (low, -1)):
            if name in columns:
                matrix[i, columns[name]] = sign
            else:
                target[i] -= sign * anchors[name]
    fitted, _, rank, _ = np.linalg.lstsq(matrix, target, rcond=None)
    if rank != matrix.shape[1]:
        raise ValueError("World does not identify every coordinate and chain step")
    return dict(zip(entities, fitted[:len(entities)])), fitted[len(entities):]
