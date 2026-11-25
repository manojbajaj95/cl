"""Deterministic tool-use stream and held-out retention probes."""

from dataclasses import dataclass
from random import Random

Call = tuple[str, str]
Program = tuple[Call, ...]


@dataclass(frozen=True)
class Family:
    name: str
    goals: tuple[str, str]
    original: Program
    migrated: Program | None = None


FAMILIES = (
    Family("scanner", ("Register a scanner", "Enroll the scanner"),
           (("inspect", "part"), ("register", "asset"))),
    Family("sensor", ("Prepare a sensor", "Ready the sensor"),
           (("calibrate", "device"), ("enable", "sensor"))),
    Family("parcel", ("Release a parcel", "Dispatch the parcel"),
           (("weigh", "box"), ("release", "parcel"))),
    Family("badge", ("Issue a badge", "Activate the badge"),
           (("encode", "card"), ("issue", "badge"))),
    Family("invoice", ("Approve an invoice", "Authorize the invoice"),
           (("review", "doc"), ("approve", "bill")),
           (("audit", "record"), ("approve", "invoice"))),
    Family("shipment", ("Close a shipment", "Finalize the shipment"),
           (("seal", "crate"), ("close", "ship")),
           (("secure", "package"), ("close", "shipment"))),
    Family("account", ("Recover an account", "Restore the account"),
           (("unlock", "user"), ("reset", "account"))),
    Family("ticket", ("Resolve a ticket", "Complete the ticket"),
           (("classify", "case"), ("resolve", "ticket"))),
)


@dataclass(frozen=True)
class Task:
    step: int
    phase: str
    family: int
    goal: str
    entity: str
    coaching: Program = ()
    wave: int = 0

    @property
    def query(self) -> str:
        return f"{FAMILIES[self.family].name}: {self.goal}"


@dataclass(frozen=True)
class Outcome:
    success: bool
    feedback: str
    program: Program = ()


@dataclass(frozen=True)
class PublicEvidence:
    source: str
    recipe: Program
    # Synthetic published sandbox fixture, separate from hidden scoring.
    sandbox_expected: Program


def recipe(family: int, migrated: bool) -> Program:
    spec = FAMILIES[family]
    return (spec.migrated or spec.original) if migrated else spec.original


def score(task: Task, program: Program, migrated: bool) -> Outcome:
    api = {op: (key, family, stage) for family in range(len(FAMILIES))
           for stage, (op, key) in enumerate(recipe(family, migrated))}
    state: dict[tuple[int, str], int] = {}
    for endpoint, key in program:
        if endpoint not in api:
            return Outcome(False, f"Unknown endpoint: {endpoint}", program)
        expected_key, family, stage = api[endpoint]
        if key != expected_key:
            return Outcome(False, f"{endpoint} requires argument '{expected_key}'", program)
        target = (family, task.entity)
        if state.get(target, 0) != stage:
            return Outcome(False, f"Workflow prerequisite not met for {endpoint}", program)
        state[target] = stage + 1
    if state != {(task.family, task.entity): 2}:
        return Outcome(False, "Calls did not produce the requested workflow state", program)
    return Outcome(True, "Workflow completed", program)


def public_evidence(task: Task) -> PublicEvidence:
    # Public reference fixtures are independent of the hidden scorer.
    fixtures = (
        (("inspect", "part"), ("register", "asset")),
        (("calibrate", "device"), ("enable", "sensor")),
        (("weigh", "box"), ("release", "parcel")),
        (("encode", "card"), ("issue", "badge")),
        (("review", "doc"), ("approve", "bill")),
        (("seal", "crate"), ("close", "ship")),
        (("unlock", "user"), ("reset", "account")),
        (("classify", "case"), ("resolve", "ticket")),
    )
    updates = {
        4: (("audit", "record"), ("approve", "invoice")),
        5: (("secure", "package"), ("close", "shipment")),
    }
    # On the first post-drift wave the sandbox has rolled forward but the
    # operator manual still lags, causing surrogate verification to fail.
    version = 2 if task.phase == "post" and task.family in updates else 1
    fixture = updates[task.family] if version == 2 else fixtures[task.family]
    manual = fixture if task.wave > 0 else fixtures[task.family]
    return PublicEvidence(f"mock-manual/{task.family}/v{int(manual != fixtures[task.family]) + 1}",
                          manual, fixture)


def stream(seed: int, pre: int, post: int) -> list[Task]:
    if pre < 8 or pre % 8 or post < 8 or post % 4:
        raise ValueError("pre must be a multiple of 8 and post a multiple of 4 (both >= 8)")
    rng = Random(seed)
    tasks = []
    for phase, size, families in (("pre", pre, tuple(range(8))), ("post", post, tuple(range(4, 8)))):
        for wave in range(size // len(families)):
            for family in rng.sample(families, len(families)):
                coach = (phase == "pre" and wave == 0) or (phase == "post" and wave == 1)
                goals = FAMILIES[family].goals
                tasks.append(Task(len(tasks), phase, family, rng.choice(goals),
                                  f"r{rng.randrange(1000, 9999)}",
                                  recipe(family, phase == "post") if coach else (), wave))
    return tasks


def retention_probes(seed: int) -> list[Task]:
    rng = Random(seed)
    return [Task(-1, "probe", family, goal, f"p{rng.randrange(1000, 9999)}")
            for family in range(4) for goal in FAMILIES[family].goals]
