"""CPU probe: does a content-bearing memory item keep a fixed effect as the store grows?

Arbitrary key->queue rules (no prior can supply them). For each store size k we
measure, on items whose rule is in the store: accuracy, the target log-odds margin,
and the same item's margin when its rule is the only one stored (its 'solo denotation').
A revision test puts an old rule repeated r times and one later UPDATE in the store.
"""
import json, random, sys, time, math
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL = sys.argv[1] if len(sys.argv) > 1 else "Qwen/Qwen2.5-0.5B-Instruct"
SEEDS = int(sys.argv[2]) if len(sys.argv) > 2 else 4
torch.set_num_threads(8)
tok = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL, torch_dtype=torch.float32).eval()
Q = [str(i) for i in range(1, 7)]
QID = [tok.encode(" " + q, add_special_tokens=False)[-1] for q in Q]
SYL = ["ka", "lo", "vi", "zu", "mer", "tan", "po", "rek", "si", "dal", "fo", "gri", "nu", "bex", "ol", "quin"]

def names(rng, n):
    s = set()
    while len(s) < n:
        s.add("".join(rng.choice(SYL) for _ in range(3)))
    return sorted(s, key=lambda _: rng.random())

def rule(n, q):
    return f"- Tickets of type '{n}' go to queue {q}."

def prompt(lines, n):
    mem = "\n".join(lines) if lines else "(empty)"
    msgs = [{"role": "system", "content": "You route support tickets. Use the routing memory."},
            {"role": "user", "content": f"Routing memory:\n{mem}\n\nA ticket of type '{n}' arrived. Which queue (1-6)? Reply with the number only."}]
    return tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True) + "Queue"

@torch.no_grad()
def logp(lines, n):
    ids = tok(prompt(lines, n), return_tensors="pt").input_ids
    lg = model(ids).logits[0, -1, QID]
    return torch.log_softmax(lg, -1)

def margin(lp, t):
    other = torch.cat([lp[:t], lp[t + 1:]])
    return (lp[t] - other.max()).item()

res = {"model": MODEL, "store": [], "revision": []}
t0 = time.time()
KS = [0, 1, 4, 16, 48]
for seed in range(SEEDS):
    rng = random.Random(seed)
    ns = names(rng, 60)
    lab = {n: rng.randrange(6) for n in ns}
    rules = [rule(n, lab[n] + 1) for n in ns]
    probe = ns[:6]
    solo = {}
    for n in probe:
        solo[n] = margin(logp([rules[ns.index(n)]], n), lab[n])
    base = {n: margin(logp([], n), lab[n]) for n in probe}
    for k in KS[1:]:
        others = [r for r in rules[6:6 + max(k - 1, 0)]]
        for n in probe:
            lines = others + [rules[ns.index(n)]]
            rng.shuffle(lines)
            lp = logp(lines, n)
            m = margin(lp, lab[n])
            res["store"].append(dict(seed=seed, k=k, item=n, margin=m, solo=solo[n], base=base[n],
                                     acc=int(lp.argmax().item() == lab[n]), pos=lines.index(rules[ns.index(n)]) / max(k - 1, 1)))
    # revision: old rule repeated r times among filler rules, then one UPDATE at the end
    for n in probe[:4]:
        old = lab[n]; new = (old + 1 + rng.randrange(5)) % 6
        for r in [1, 2, 4, 8]:
            for k_other in [0, 16]:
                lines = [rule(n, old + 1)] * r + rules[6:6 + k_other]
                rng.shuffle(lines)
                lines = lines + [f"- UPDATE (latest, overrides earlier rules): tickets of type '{n}' now go to queue {new + 1}."]
                lp = logp(lines, n)
                res["revision"].append(dict(seed=seed, item=n, r=r, k_other=k_other,
                                            p_new=lp[new].exp().item(), p_old=lp[old].exp().item()))
    print(f"seed {seed} done {time.time() - t0:.0f}s", flush=True)

out = f"/home/ubuntu/repos/cl/tree/probes/results_{MODEL.split('/')[-1]}.json"
json.dump(res, open(out, "w"), indent=1)

import statistics as st
print("k | acc | mean margin | mean solo margin | corr(margin, solo)")
for k in KS[1:]:
    rows = [r for r in res["store"] if r["k"] == k]
    m = [r["margin"] for r in rows]; s = [r["solo"] for r in rows]
    c = st.correlation(m, s) if len(set(m)) > 1 else float("nan")
    print(k, round(st.mean(r["acc"] for r in rows), 3), round(st.mean(m), 2), round(st.mean(s), 2), round(c, 2))
print("base margin (no memory):", round(st.mean(r["base"] for r in res["store"] if r["k"] == 1), 2))
print("revision: r | k_other | P(new) | P(old)")
for r_ in [1, 2, 4, 8]:
    for ko in [0, 16]:
        rows = [x for x in res["revision"] if x["r"] == r_ and x["k_other"] == ko]
        print(r_, ko, round(st.mean(x["p_new"] for x in rows), 3), round(st.mean(x["p_old"] for x in rows), 3))
