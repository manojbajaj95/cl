"""CPU feasibility check for exact-prefix plus sampled-residual audits."""

import math

import torch

from run import HORIZON, OLD, TEST, corpus, path_log_probs, pretrain, success


def interval(accepted_mass, unresolved_mass, wins, draws, alpha=0.05):
    center = accepted_mass + unresolved_mass * wins / draws
    radius = unresolved_mass * math.sqrt(math.log(2 / alpha) / (2 * draws))
    return (center - radius).clamp_min(0), (center + radius).clamp_max(1)


def simulate(accepted_mass, unresolved_mass, true_success, draws, generator):
    q = (true_success - accepted_mass) / unresolved_mass
    wins = torch.binomial(torch.full((2_000,), float(draws)), torch.full((2_000,), q),
                          generator=generator)
    lower, upper = interval(accepted_mass, unresolved_mass, wins, draws)
    return tuple((decision.float().mean().item()) for decision in
                 (lower >= 0.60, upper < 0.60, (lower < 0.60) & (upper >= 0.60)))


@torch.no_grad()
def sample_success(policy, prompt, paths, count, generator, forced_first=None):
    tokens = prompt.expand(count, -1)
    if forced_first is not None:
        tokens = torch.cat((tokens, forced_first.expand(count, 1)), dim=1)
    while tokens.shape[1] < prompt.shape[1] + HORIZON:
        probs = policy(tokens)[:, -1].softmax(-1)
        tokens = torch.cat((tokens, torch.multinomial(probs, 1, generator=generator)), dim=1)
    return (tokens[:, None, prompt.shape[1] :] == paths).all(-1).any(-1)


@torch.no_grad()
def estimate(policy, prompt, paths, draws, generator):
    log_paths = path_log_probs(policy, prompt, paths)
    exact = success(log_paths).item()
    accepted = log_paths[0, 0].exp().item()
    first = paths[0, 1, 0]
    unresolved = policy(prompt)[0, -1].softmax(-1)[first].item()
    plain, residual = [], []
    for _ in range(16):
        plain.append(sample_success(policy, prompt, paths, draws, generator).float().mean())
        residual_win = sample_success(policy, prompt, paths, draws, generator, first).float()
        residual.append(accepted + unresolved * residual_win.mean())

    def rmse(values):
        return (torch.stack(values) - exact).square().mean().sqrt().item()

    return exact, unresolved, rmse(plain), rmse(residual)


def main():
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    generator = torch.Generator().manual_seed(2026)
    print("method unresolved true_success verifier_calls accepts rejects inconclusive")
    for r in (1.0, 0.50, 0.15):
        for p in (0.58, 0.62):
            for n in (128, 512, 2048, 8192):
                rates = simulate(0.60 * (1 - r), r, p, n, generator)
                print(f"{'plain' if r == 1 else 'residual'} {r:.2f} {p:.2f} {n} "
                      + " ".join(f"{rate:.4f}" for rate in rates))
    torch.manual_seed(3)
    policy = pretrain()
    prompts, paths, _ = corpus(OLD, TEST, 0)
    print("learned draws exact_success unresolved plain_rmse residual_rmse")
    for n in (128, 512):
        stats = estimate(policy, prompts[6:7], paths[6:7], n, generator)
        print(f"learned {n} " + " ".join(f"{stat:.4f}" for stat in stats))


if __name__ == "__main__":
    main()
