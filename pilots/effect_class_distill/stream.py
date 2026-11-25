import ast
from dataclasses import dataclass
from itertools import product


OPS = ("subtract", "combine", "charge")
ALIASES = (
    ("subtract", "difference", False),
    ("combine", "blend", True),
    ("charge", "cost", False),
)
FUNCTIONS = {
    name: (operation, version == 1 and swap, version == 1)
    for operation, (old, new, swap) in enumerate(ALIASES)
    for version, name in enumerate((old, new))
}
VARIABLES = (("a", "b"), ("x", "y"), ("left", "right"), ("first", "second"))
PROBES = ((2, -3), (-4, 5), (0, 7))
UNIT_TESTS = ((9, 4), (-8, 1), (3, -6), (1, 10))
TEMPLATES = {
    "old_train": (
        "Use lib to {op} the measurements {a} and {b}. Return the result.",
        "Write a lib call for operation {op} on {a}, then {b}.",
        "Given readings {a} and {b}, calculate their {op} using lib.",
    ),
    "old_eval": (
        "What lib expression gives the {op} of {a} and {b}?",
        "Apply {op} to the ordered pair {a}, {b} via lib.",
    ),
    "new_train": (
        "Call the library's {op} operation with inputs {a} and {b}.",
        "Using lib, compute {op} with primary={a}, secondary={b}.",
        "Produce a lib expression that performs {op} on inputs {a} and {b}.",
    ),
    "new_eval": (
        "Show the library call for {op}, taking {a} before {b}.",
        "Use the lib API to calculate {op} from values {a} and {b}.",
    ),
}


def semantics(operation, a, b):
    if operation == 0:
        return a - b
    if operation == 1:
        return a + 2 * b
    return a * a - b


@dataclass(frozen=True)
class Call:
    name: str
    order: tuple[int, int]

    @property
    def new(self):
        return FUNCTIONS[self.name][2]

    def run(self, values):
        operation, swap, _ = FUNCTIONS[self.name]
        a, b = (values[i] for i in self.order)
        return semantics(operation, b, a) if swap else semantics(operation, a, b)


def parse(code, variables):
    node = ast.parse(code.strip(), mode="eval").body
    if not (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "lib"
        and node.func.attr in FUNCTIONS
        and not node.keywords
        and len(node.args) == 2
        and all(isinstance(arg, ast.Name) and arg.id in variables for arg in node.args)
    ):
        raise ValueError("expected a call to the synthetic API with two input names")
    return Call(node.func.attr, tuple(variables.index(arg.id) for arg in node.args))


def canonicalize(call):
    a, b = (("a", "b")[i] for i in call.order)
    return f"lib.{call.name}({a}, {b})"


@dataclass(frozen=True)
class Prompt:
    text: str
    variables: tuple[str, str]
    operation: int

    def candidates(self):
        for name, order, separator in product(FUNCTIONS, ((0, 1), (1, 0)), (", ", ",")):
            a, b = (self.variables[i] for i in order)
            yield f" lib.{name}({a}{separator}{b})"

    def target(self, new):
        old, migrated, swap = ALIASES[self.operation]
        a, b = self.variables[::-1] if new and swap else self.variables
        return f" lib.{migrated if new else old}({a}, {b})"

    def observe(self, call):
        signature = tuple(call.run(values) for values in PROBES)
        outputs = tuple(call.run(values) for values in UNIT_TESTS)
        expected = tuple(semantics(self.operation, *values) for values in UNIT_TESTS)
        return signature, outputs == expected


def prompts():
    data = []
    splits = {}
    for split, templates in TEMPLATES.items():
        start = len(data)
        for operation, template, variables in product(range(len(OPS)), templates, VARIABLES):
            a, b = variables
            text = template.format(op=OPS[operation], a=a, b=b)
            data.append(Prompt(f"# {text}\nresult =", variables, operation))
        splits[split] = list(range(start, len(data)))
    return data, splits
