"""Mean-field theory of artifact-pool contamination.

With defective fraction x, the drift of x per admitted artifact is proportional to
g(x) = a_d P(x) (1 - x) - a_s x (1 - P(x)) - d k x (1 - x),  P(x) = 1 - (1 - eps)(1 - tau x)^k.
At eps = 0, g'(0) = a_s (R - 1) with R = k (a_d tau - d) / a_s, so x = 0 is unstable iff R > 1.
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import brentq

from .model import Params


def P(p: Params, x):
    return 1 - (1 - p.eps) * (1 - p.tau * x) ** p.k


def g(p: Params, x):
    Px = P(p, x)
    return p.alpha_d * Px * (1 - x) - p.alpha_s * x * (1 - Px) - p.d * p.k * x * (1 - x)


def fixed_point(p: Params) -> float:
    """Stable fixed point reached from x = 0 (the first sign change of g on (0, 1])."""
    grid = np.linspace(1e-9, 1.0, 4001)
    vals = g(p, grid)
    if vals[0] <= 0:
        return 0.0
    idx = np.flatnonzero(vals <= 0)
    if len(idx) == 0:
        return 1.0
    j = idx[0]
    return brentq(lambda x: g(p, x), grid[j - 1], grid[j])


def small_x_power_law(p: Params, n, n0: float, x0: float = 0.0):
    """Linearized growth of the defect fraction with pool size n (valid while x is small)."""
    R = p.R
    eps_eff = p.eps * p.alpha_d / p.alpha_s
    r = np.asarray(n, float) / n0
    if abs(R - 1) < 1e-9:
        return x0 + eps_eff * np.log(r)
    return x0 * r ** (R - 1) + eps_eff / (R - 1) * (r ** (R - 1) - 1)


def critical_fraction(p: Params) -> float:
    """Defect fraction at which a defective artifact in context costs as much as a sound one helps."""
    return p.beta / (p.beta + p.gamma)


def predicted_peak_pool(p: Params, n0: float, x0: float = 0.0) -> float:
    """Pool size at which expected success peaks: d/dN [beta (1-x) - gamma x] = 0 never happens with
    a monotone x, so we report where the contribution of the pool falls back below the empty pool,
    i.e. x(N) = beta / (beta + gamma)."""
    xc = critical_fraction(p)
    if p.R <= 1 and p.eps * p.alpha_d / p.alpha_s / max(1 - p.R, 1e-9) < xc:
        return float("inf")
    lo, hi = n0, n0 * 1e12
    f = lambda n: small_x_power_law(p, n, n0, x0) - xc
    if f(hi) < 0:
        return float("inf")
    return brentq(f, lo, hi)


def h(p: Params, x):
    """Expected net change of pool size per round."""
    Px = P(p, x)
    return p.alpha_d * Px + p.alpha_s * (1 - Px) - p.d * p.k * x


def integrate(p: Params, T: int, n0: float | None = None, x0: float | None = None, dt: float = 1.0):
    """Euler-integrate the mean-field ODE dx/dt = g(x)/N, dN/dt = h(x) for T rounds."""
    n = float(n0 if n0 is not None else p.k)
    x = float(x0 if x0 is not None else p.eps)
    xs, ns = np.empty(T), np.empty(T)
    for t in range(T):
        xs[t], ns[t] = x, n
        x = float(np.clip(x + dt * g(p, x) / n, 0.0, 1.0))
        n = max(n + dt * h(p, x), 1.0)
    return xs, ns
