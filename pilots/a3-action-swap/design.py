"""Frozen rule directives and action assignments for the swap assay."""

import numpy as np


MENU = "ABC"
NON_MENU = "D"
ARMS = ("rule", "swapped", "non_menu", "filler")
TEMPLATES = (
    "The routing rule has changed. For every code, submit {action}.",
    "Use the updated default: no matter which code appears, route to {action}.",
    "All checkpoints now require tool {action}, regardless of the displayed code.",
    "Override the old remainder mapping and always return {action}.",
    "At each decision in this task, the correct tool is now {action}.",
    "For this run, apply the replacement rule: every checkpoint goes to {action}.",
    "The new verifier accepts {action} for every input, so use it throughout the run.",
    "The code no longer changes the route. For every input choose {action}.",
    "Ignore the previous routing table. Pick {action} for all checkpoints.",
    "The current playbook uses a single tool for all codes: {action}.",
    "Latest controller update: select {action} on every checkpoint.",
    "If any checkpoint asks for a tool, the revised rule says to answer {action}.",
    "The controller's replacement policy is constant: choose {action} independent of the code.",
    "Use {action} whenever you are asked to route a code under the current rule.",
    "Treat all displayed codes alike under the new rule and send them to {action}.",
    "For each of the three steps, the current rule is to route to {action}.",
    "The old code rule is stale; the route required at every checkpoint is {action}.",
    "The exact updated procedure is to submit {action} at each step.",
    "Regardless of remainder or checkpoint, use tool {action} under the replacement rule.",
    "There are no exceptions to the revised mapping: any input requires {action}.",
)


def lessons():
    pairs = [(a, b) for a in MENU for b in MENU if a != b] * 3 + [("A", "B"), ("B", "A")]
    assignment = np.random.default_rng(403971).permutation(len(pairs))
    return [
        {
            "id": f"swap-{i + 1:02}",
            "template": template,
            "action": pairs[j][0],
            "swap_action": pairs[j][1],
            "rule": template.format(action=pairs[j][0]),
            "swapped": template.format(action=pairs[j][1]),
            "non_menu": template.format(action=NON_MENU),
        }
        for i, (template, j) in enumerate(zip(TEMPLATES, assignment))
    ]
