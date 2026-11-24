"""Frozen coding stream and execution oracles. Only authored expressions run."""

from dataclasses import dataclass
from itertools import permutations
import math
import random
import re


@dataclass(frozen=True)
class Family:
    name: str
    spec: str
    sound_note: str
    bad_note: str
    code: tuple[str, str, str]  # sound, planted defect, other defect
    smoke: tuple | None
    probes: tuple  # (input, expected output); first is source, others held out


FAMILIES = (
    Family("bucket", "Round the reading down to the next integer (toward negative infinity).",
           "For whole-unit buckets, use floor to round down.",
           "For whole-unit buckets, use int to round down.",
           ("math.floor(x)", "int(x)", "int(x) + (x < 0)"), (2.1, 2),
           ((-3.2, -4), (-0.7, -1), (-11.4, -12), (-6.6, -7))),
    Family("cap", "Clamp the reading to the closed interval from 0 to 10.",
           "For bounded readings, clamp to both the lower and upper limits.",
           "For bounded readings, clamp to the upper limit only.",
           ("max(0, min(10, x))", "min(10, x)", "max(0, x)"), (5, 5),
           (((-3, 14), (0, 10)), ((17, -2), (10, 0)), ((-11, 35), (0, 10)), ((21, -7), (10, 0)))),
    Family("unique", "Remove repeats from the list, retaining the order of first appearance.",
           "For ordered uniqueness, deduplicate with dict.fromkeys.",
           "For ordered uniqueness, deduplicate with sorted(set(...)).",
           ("list(dict.fromkeys(x))", "sorted(set(x))", "list(x)"), ([1, 2, 3], [1, 2, 3]),
           (([3, 2, 3, 1], [3, 2, 1]), ([5, 1, 4, 1], [5, 1, 4]),
            ([8, 2, 7, 8], [8, 2, 7]), ([4, 4, 9, 2], [4, 9, 2]))),
    Family("words", "Split into words on runs of any whitespace, without empty fields.",
           "For words separated by whitespace, use split() with no argument.",
           "For words separated by whitespace, use split(' ') with an explicit space.",
           ("x.split()", "x.split(' ')", "x.strip().split(' ')"), ("red blue", ["red", "blue"]),
           ((" a  b\t", ["a", "b"]), ("\tcat dog  bird ", ["cat", "dog", "bird"]),
            ("\nleft   right\n", ["left", "right"]), (" high\tlow  ", ["high", "low"]))),
    Family("suffix", "Remove one trailing '.txt' suffix if present. Preserve all other characters.",
           "Remove a trailing extension with removesuffix, not character stripping.",
           "Remove a trailing extension with rstrip, not exact suffix stripping.",
           ("x.removesuffix('.txt')", "x.rstrip('.txt')", "x.replace('.txt', '')"), ("log.txt", "log"),
           (("text.txt.txt", "text.txt"), ("next.txt.txt", "next.txt"),
            ("draft.txt.txt", "draft.txt"), ("context.txt.txt", "context.txt"))),
    Family("chunks", "Split the list into successive batches of two, keeping any incomplete final batch.",
           "When batching pairs, keep the final partial slice.",
           "When batching pairs, drop the final partial slice.",
           ("[x[i:i+2] for i in range(0, len(x), 2)]", "[x[i:i+2] for i in range(0, len(x)-1, 2)]",
            "[(x + [0])[i:i+2] for i in range(0, len(x), 2)]"), ([4, 8], [[4, 8]]),
           (([1, 8, 3, 9, 4], [[1, 8], [3, 9], [4]]), ([2, 1, 8], [[2, 1], [8]]),
            ([9], [[9]]), ([3, 7, 2, 8, 5], [[3, 7], [2, 8], [5]]))),
    Family("mean", "Return the arithmetic mean of the values, or 0 for an empty list.",
           "For an arithmetic mean, divide by the observation count, including repeats.",
           "For an arithmetic mean, divide by the distinct value count, excluding repeats.",
           ("sum(x) / len(x) if x else 0", "sum(x) / len(set(x)) if x else 0",
            "sum(set(x)) / len(set(x)) if x else 0"), ([2, 4], 3),
           (([6, 6, 3], 5), ([7, 1, 1], 3), ([4, 4, 4, 8], 5), ([2, 2, 8], 4))),
    Family("runner_up", "Return the second largest distinct value; inputs have at least two distinct values.",
           "For a distinct runner-up, remove duplicate values before sorting.",
           "For a distinct runner-up, keep duplicate values when sorting.",
           ("sorted(set(x))[-2]", "sorted(x)[-2]", "sorted(set(x))[0]"), ([10, 2], 2),
           (([7, 7, 2, 3], 3), ([8, 8, 1, 4], 4), ([4, 5, 5, 6, 6], 5), ([9, 3, 9, 6], 6))),
    Family("windows", "Count integer positions from the first endpoint through the second, including both.",
           "For an inclusive span, add one to the difference between endpoints.",
           "For an inclusive span, use the difference between endpoints without adding one.",
           ("x[1] - x[0] + 1", "x[1] - x[0]", "x[1] - x[0] - 1"), None,
           (((8, 8), 1), ((-4, -1), 4), ((11, 17), 7), ((0, 8), 9))),
    Family("median", "Return the median; for even lengths average the two center values.",
           "For even-length medians, average the lower and upper middle values.",
           "For even-length medians, take the upper middle value only.",
           ("(sorted(x)[(len(x)-1)//2] + sorted(x)[len(x)//2]) / 2",
            "sorted(x)[len(x)//2]", "sorted(x)[(len(x)-1)//2]"), ([2, 8, 4], 4),
           (([3, 1, 9, 17], 6), ([0, 8], 4), ([1, 9, 3, 5], 4), ([30, 15, 45, 60, 90, 0], 37.5))),
    Family("non_null", "Remove None values only; preserve zero, empty strings and False.",
           "For missing-value filtering, test 'is not None' explicitly.",
           "For missing-value filtering, test truthiness with 'if value'.",
           ("[v for v in x if v is not None]", "[v for v in x if v]", "list(x)"), ([1, 2], [1, 2]),
           (([None, 0, 1], [0, 1]), ([False, None, 7], [False, 7]),
            (["", "a", None], ["", "a"]), ([None, 2, 0, False], [2, 0, False]))),
    Family("overlay", "Merge the base and update dictionaries; the update wins conflicts.",
           "For a patch overlay, unpack the update dictionary last.",
           "For a patch overlay, unpack the base dictionary last.",
           ("{**x[0], **x[1]}", "{**x[1], **x[0]}", "dict(x[1])"), (({}, {"b": 3}), {"b": 3}),
           ((({"a": 1, "b": 2}, {"b": 5}), {"a": 1, "b": 5}),
            (({"left": 1, "right": 8}, {"left": 0}), {"left": 0, "right": 8}),
            (({"pen": 4, "bag": 2}, {"book": 6, "bag": 8}), {"pen": 4, "bag": 8, "book": 6}),
            (({"z": 1, "y": 3}, {"y": 4}), {"z": 1, "y": 4}))),
    Family("path_tail", "Take the part after the last slash. If no slash, return the input unchanged.",
           "For the last path component, split from the right at the final slash.",
           "For the last path component, split from the left at the first slash.",
           ("x.rsplit('/', 1)[-1]", "x.split('/', 1)[-1]", "x.split('/', 1)[0]"), ("report", "report"),
           (("a/z/log", "log"), ("tmp/u/data", "data"), ("in/old/jobs/list", "list"), ("top/sub/file", "file"))),
    Family("count", "Count occurrences of the value 1, including repeats.",
           "For frequency counts, use list.count to preserve multiplicity.",
           "For frequency counts, use set membership to preserve multiplicity.",
           ("x.count(1)", "int(1 in set(x))", "len(x)"), ([1], 1),
           (([1, 1, 3], 2), ([8, 1, 1, 4], 2), ([1, 7, 1, 5, 1], 3), ([9, 9, 1, 1], 2))),
    Family("tag", "Normalize only the first character to uppercase; do not modify the rest.",
           "To upper-case the lead character only, splice the untouched tail back on.",
           "To upper-case the lead character only, call capitalize on the whole string.",
           ("x[:1].upper() + x[1:]", "x.capitalize()", "x.upper()"), ("q", "Q"),
           (("aBc", "ABc"), ("oBject", "OBject"), ("tAg", "TAg"), ("qRcode", "QRcode"))),
    Family("after", "Return the text after the first colon, or empty text if there is no colon.",
           "For the payload after the first colon, use partition(':')[2].",
           "For the payload after the first colon, use split(':')[-1].",
           ("x.partition(':')[2]", "x.split(':')[-1]", "x.partition(':')[0]"), (":", ""),
           (("a:1:2", "1:2"), ("hdr:part:result", "part:result"),
            ("key:color:red", "color:red"), ("type:tag:value:3", "tag:value:3"))),
)

CONTEXTS = (
    ("Edit a data-import helper", "A report formatter needs a standalone version"),
    ("Edit an analytics preprocessor", "A batch job needs a standalone version"),
    ("Edit a transformation in a CLI", "A library consumer needs a standalone version"),
    ("Edit a helper in an export job", "A notebook helper needs a standalone version"),
)
ORDERS = tuple(permutations(range(3)))
RNG_SEED = 91731


def execute(expression, value):
    tools = {f.__name__: f for f in (dict, int, len, list, max, min, range, set, sorted, sum)}
    return eval(expression, {"__builtins__": tools, "math": math, "x": value, "value": value})


def writer_expression(code):
    return re.sub(r"\bx\b", "value", code)


def signature(family, variant):
    probe, expected = family.probes[variant]
    # cap has two calls per transfer test, covering both range boundaries.
    expressions = map(writer_expression, family.code)
    actual = tuple(tuple(execute(code, x) for x in probe) if family.name == "cap"
                   else execute(code, probe) for code in expressions)
    if actual[0] != expected or any(wrong == expected for wrong in actual[1:]) or actual[1] == actual[2]:
        raise ValueError((family.name, probe, expected, actual))
    return actual


def feedback(family, choice):
    if family.smoke is None:
        return "no smoke tests were run"
    value, expected = family.smoke
    return "smoke test passed" if execute(family.code[choice], value) == expected else "smoke test failed"


def chat(memory, user):
    system = "You maintain small Python helpers. Choose the implementation that satisfies the task."
    if memory is not None:
        system += f"\nRetrieved note from a previous task: {memory}"
    return (f"<|im_start|>system\n{system}<|im_end|>\n<|im_start|>user\n{user}"
            "<|im_end|>\n<|im_start|>assistant\nChoice:")


def menu(family, order, writer):
    expressions = family.code
    if writer:
        expressions = tuple(map(writer_expression, expressions))
    return "\n".join(f"{label}. return {expressions[i]}" for label, i in zip("ABC", order))


def episode(family, variant, solve_order, write_order, memory, choice=None):
    solve_context, write_context = CONTEXTS[variant]
    if choice is None:
        user = (f"{solve_context}: implement {family.name}(x). {family.spec}\n"
                f"Choose a patch body:\n{menu(family, solve_order, False)}")
    else:
        user = (f"Earlier task: {family.spec}\n"
                f"Your submitted patch was: return {family.code[choice]}\n"
                f"Verifier: {feedback(family, choice)}.\n"
                f"{write_context}: save a reusable code lesson as a new Python helper, "
                f"{family.name}_helper(value). It must satisfy the same specification.\n"
                f"Choose a reusable implementation:\n{menu(family, write_order, True)}")
    return chat(memory, user + "\nAnswer with one letter: A, B, or C.\n")


def stream():
    rng = random.Random(RNG_SEED)
    for family in FAMILIES:
        for variant in range(len(CONTEXTS)):
            yield family, variant, rng.choice(ORDERS), rng.choice(ORDERS)
