"""Two-stage continual learning with exact sequence-level retention metrics."""

import argparse
import copy
import time

import torch
from torch import nn
from torch.nn import functional as F


OLD, NEW, HINT = range(3)
VOCAB, HORIZON = 24, 7
ANCHOR, DEV, TEST = range(3), range(3, 5), range(5, 8)
METHODS = ("none", "token_kl", "replay", "conditional_kl", "mean_event", "group_event")
WEIGHTS = (0.25, 1.0, 4.0, 16.0)


class Policy(nn.Module):
    def __init__(self):
        super().__init__()
        self.embed = nn.Embedding(VOCAB, 24)
        self.gru = nn.GRU(24, 48, batch_first=True)
        self.head = nn.Linear(48, VOCAB)

    def forward(self, tokens):
        state, _ = self.gru(self.embed(tokens))
        return self.head(state)


def corpus(task, nuisances, rule):
    prompts, paths, groups = [], [], []
    for group in range(2):
        for bit in range(2):
            for nuisance in nuisances:
                prompts.append((task, 3 + group, 5 + bit, 7 + nuisance))
                paths.append(
                    [
                        [15 + style]
                        + [
                            17 + (bit ^ style ^ rule ^ ((i // (group + 1)) % 2))
                            for i in range(HORIZON - 1)
                        ]
                        for style in range(2)
                    ]
                )
                groups.append(group)
    return tuple(map(torch.tensor, (prompts, paths, groups)))


def next_logits(policy, prompts, response):
    tokens = torch.cat((prompts, response[:, :-1]), dim=1)
    return policy(tokens)[:, prompts.shape[1] - 1 :]


def path_logits(policy, prompts, paths):
    n, k, h = paths.shape
    logits = next_logits(policy, prompts.repeat_interleave(k, dim=0), paths.flatten(0, 1))
    return logits.reshape(n, k, h, VOCAB)


def path_log_probs(policy, prompts, paths):
    return path_logits(policy, prompts, paths).log_softmax(-1).gather(
        -1, paths.unsqueeze(-1)
    ).squeeze(-1).sum(-1)


def success(log_paths):
    return log_paths.logsumexp(-1).exp()


def by_group(values, groups):
    return torch.stack([values[groups == g].mean() for g in range(2)])


@torch.no_grad()
def rollout(policy, prompts, generator):
    tokens = prompts
    for _ in range(HORIZON):
        probs = policy(tokens)[:, -1].softmax(-1)
        tokens = torch.cat((tokens, torch.multinomial(probs, 1, generator=generator)), dim=1)
    return tokens[:, prompts.shape[1] :]


def forward_kl(student, teacher):
    return F.kl_div(student.log_softmax(-1), teacher.softmax(-1), reduction="none").sum(-1)


def pretrain():
    policy = Policy()
    all_ids = range(8)
    sources = [corpus(OLD, all_ids, 0), corpus(NEW, all_ids, 0), corpus(HINT, all_ids, 1)]
    prompts = torch.cat([batch[0] for batch in sources])
    paths = torch.cat([batch[1] for batch in sources])
    opt = torch.optim.AdamW(policy.parameters(), lr=0.012)
    hint_prompts, hint_paths, _ = sources[-1]
    flat_hints = hint_paths.flatten(0, 1)
    for _ in range(220):
        corrupted = flat_hints.clone()
        mask = torch.rand_like(corrupted[:, 1:], dtype=torch.float32) < 0.3
        noise = torch.randint(17, 19, mask.shape)
        corrupted[:, 1:] = torch.where(mask, noise, corrupted[:, 1:])
        robust_hint = next_logits(policy, hint_prompts.repeat_interleave(2, 0), corrupted)
        opt.zero_grad()
        loss = -path_log_probs(policy, prompts, paths).mean() / HORIZON
        loss = loss + 0.25 * F.cross_entropy(
            robust_hint[:, 1:].reshape(-1, VOCAB), flat_hints[:, 1:].reshape(-1)
        )
        loss.backward()
        opt.step()
    return policy.eval()


def penalty(method, policy, reference, anchor, ref_paths, generator):
    prompts, paths, groups = anchor
    if method == "token_kl":
        sampled = rollout(policy, prompts, generator)
        with torch.no_grad():
            old = next_logits(reference, prompts, sampled)
        return forward_kl(next_logits(policy, prompts, sampled), old).mean()
    cur_paths = path_log_probs(policy, prompts, paths)
    if method == "replay":
        return -cur_paths.mean() / HORIZON
    if method == "conditional_kl":
        return forward_kl(cur_paths, ref_paths).mean()
    drop = success(ref_paths) - success(cur_paths)
    if method == "mean_event":
        return drop.mean().relu().square()
    return by_group(drop, groups).max().relu().square()


@torch.no_grad()
def evaluate(policy, old, new):
    old_mass = success(path_log_probs(policy, old[0], old[1]))
    new_mass = success(path_log_probs(policy, new[0], new[1]))
    return tuple(by_group(old_mass, old[2]).tolist()) + (new_mass.mean().item(),)


def adapt(reference, method, weight, seed, steps, dev):
    policy = copy.deepcopy(reference)
    opt = torch.optim.AdamW(policy.parameters(), lr=0.005)
    generator = torch.Generator().manual_seed(seed + 10_000)
    old_generator = torch.Generator().manual_seed(seed + 20_000)
    prompts, _, _ = corpus(NEW, ANCHOR, 1)
    hints = prompts.clone()
    hints[:, 0] = HINT
    anchor = corpus(OLD, ANCHOR, 0)
    with torch.no_grad():
        ref_paths = path_log_probs(reference, anchor[0], anchor[1])
    checkpoints = []
    for step in range(1, steps + 1):
        sampled = rollout(policy, prompts, generator)
        with torch.no_grad():
            teacher = next_logits(reference, hints, sampled)
        loss = forward_kl(next_logits(policy, prompts, sampled), teacher).mean()
        if method != "none":
            loss = loss + weight * penalty(
                method, policy, reference, anchor, ref_paths, old_generator
            )
        opt.zero_grad()
        loss.backward()
        opt.step()
        if step % 5 == 0 or step == steps:
            checkpoints.append((step, weight, evaluate(policy, *dev), copy.deepcopy(policy.state_dict())))
    return checkpoints


def select(checkpoints, base, target):
    eligible = [point for point in checkpoints if point[2][2] >= target]
    if not eligible:
        return None
    return max(
        eligible,
        key=lambda p: (min(p[2][g] - base[g] for g in range(2)), -p[0], -p[1]),
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", nargs="+", type=int, default=[3, 7, 11, 19, 23])
    parser.add_argument("--steps", type=int, default=100)
    parser.add_argument("--target", type=float, default=0.75)
    args = parser.parse_args()
    if args.steps < 1 or not 0 < args.target < 1:
        parser.error("steps must be positive and target must be between 0 and 1")
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    start = time.perf_counter()
    dev = corpus(OLD, DEV, 0), corpus(NEW, DEV, 1)
    test = corpus(OLD, TEST, 0), corpus(NEW, TEST, 1)
    rows = {method: [] for method in METHODS}
    print(f"torch={torch.__version__} steps={args.steps} dev_new_target={args.target:.2f}")
    print("seed method step weight old0 old1 new mean_old_bwt worst_group_bwt")
    for seed in args.seeds:
        torch.manual_seed(seed)
        reference = pretrain()
        base_dev, base_test = evaluate(reference, *dev), evaluate(reference, *test)
        print(f"{seed} reference 0 - " + " ".join(f"{p:.4f}" for p in base_test))
        for method in METHODS:
            weights = (0.0,) if method == "none" else WEIGHTS
            points = [
                point
                for weight in weights
                for point in adapt(reference, method, weight, seed, args.steps, dev)
            ]
            chosen = select(points, base_dev, args.target)
            if chosen is None:
                best_new = max(point[2][2] for point in points)
                print(f"{seed} {method} no dev-qualified checkpoint (best_dev_new={best_new:.4f})")
                continue
            step, weight, _, state = chosen
            selected = Policy()
            selected.load_state_dict(state)
            score = evaluate(selected, *test)
            bwt = tuple(score[g] - base_test[g] for g in range(2))
            result = score + (sum(bwt) / 2, min(bwt))
            rows[method].append(result)
            print(f"{seed} {method} {step} {weight:g} " + " ".join(f"{p:.4f}" for p in result))
    print("summary method qualified old0 old1 new mean_old_bwt worst_group_bwt")
    for method, results in rows.items():
        averages = [sum(col) / len(col) for col in zip(*results)]
        print(f"summary {method} {len(results)}/{len(args.seeds)} " + " ".join(
            f"{avg:.4f}" for avg in averages
        ))
    print(f"elapsed_seconds={time.perf_counter() - start:.1f}")


if __name__ == "__main__":
    main()
