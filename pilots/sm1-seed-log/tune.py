import sys, time, json
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from seedlog import *
r, targets, lr, eps, steps, thr = int(sys.argv[1]), sys.argv[2].split(','), float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
tasks = sys.argv[7].split(',')
sm = SeedLogModel(r=r, alpha=2 * r, targets=targets, threads=thr)
print("d", sm.d, flush=True)
ev = {t: make_items(t, "test", 100, 0) for t in tasks}
print("base", {k: v["acc"] for k, v in sm.evaluate(ev).items()}, flush=True)
t0 = time.time()
train_stream(sm, tasks, steps, lr, eps, 16, 0, log_every=50, eval_items=ev)
print("time/step", (time.time() - t0) / steps / len(tasks))
