import json, glob, statistics as st
runs=[json.load(open(f))["results"] for f in sorted(glob.glob("results_seed[0-9].json"))]
print(f"seeds: {len(runs)}; n_test per seed: 32\n")
print("| A substrate | B substrate | A ok | B ok | retention |\n|---|---|---|---|---|")
for k in runs[0]:
    a,b=k.split("|")
    cell=lambda m: f"{100*st.mean(r[k][m] for r in runs):.0f} ({min(100*r[k][m] for r in runs):.0f}-{max(100*r[k][m] for r in runs):.0f})"
    print(f"| {a} | {b} | {cell('A')} | {cell('B')} | {cell('ret')} |")
