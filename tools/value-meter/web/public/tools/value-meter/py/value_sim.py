"""
value_sim — a minimal numerical instantiation of the value thesis (docs 00-05).

Everything is in NATS (natural log) so that value growth rates and information
quantities (H, D, I) are directly comparable — which is the whole point: the
thesis claims they are the same kind of quantity.

This module holds the reusable pieces; `experiments.py` runs the falsifiable
checks against the theory's closed-form predictions.
"""
from __future__ import annotations
import numpy as np

# ----------------------------------------------------------------------------
# Information-theoretic primitives (nats)
# ----------------------------------------------------------------------------

def _clip(p):
    p = np.asarray(p, dtype=float)
    return np.clip(p, 1e-300, None)

def entropy(p):
    """H(p) = -sum p ln p  (nats)."""
    p = _clip(p)
    p = p / p.sum()
    return float(-(p * np.log(p)).sum())

def kl(p, q):
    """D(p||q) = sum p ln(p/q)  (nats)."""
    p = _clip(p); q = _clip(q)
    p = p / p.sum(); q = q / q.sum()
    return float((p * np.log(p / q)).sum())

def mutual_information(joint):
    """I(X;Y) from a joint matrix P[x,y]  (nats)."""
    P = _clip(joint); P = P / P.sum()
    px = P.sum(axis=1, keepdims=True)
    py = P.sum(axis=0, keepdims=True)
    return float((P * np.log(P / (px * py))).sum())


# ----------------------------------------------------------------------------
# The horse-race value game (docs 01-02)
#   resource (bankroll) compounds: W *= b[x] * o[x], with fair odds o = 1/r.
#   one round's log-growth is ln(b[x] / r[x]); the agent bets its model b.
# ----------------------------------------------------------------------------

def round_log_growth(b, r, x):
    """ln(b[x] * o[x]) with fair odds o = 1/r  ->  ln(b[x]/r[x])."""
    b = _clip(b); r = _clip(r)
    return float(np.log(b[x] / r[x]))

def measured_growth_rate(q, b, r, T, rng):
    """Monte-Carlo per-round value growth rate of betting fixed model b
    against reference r in a world drawn from q. Converges to D(q||r)-D(q||b)."""
    q = _clip(q); q = q / q.sum()
    xs = rng.choice(len(q), size=T, p=q)
    b = _clip(b); r = _clip(r)
    return float(np.mean(np.log(b[xs] / r[xs])))


# ----------------------------------------------------------------------------
# Perception channels (doc 02 capacity, doc 04 fleet ceiling)
# ----------------------------------------------------------------------------

def bsc_joint(eps, px=0.5):
    """Joint P[x,y] for a binary symmetric channel, flip prob eps.
    I(X;Y) = ln2 - H_b(eps)  (in nats when px=0.5)."""
    px = np.array([1 - px, px])
    # P[x,y] = px[x] * channel[x,y]
    chan = np.array([[1 - eps, eps], [eps, 1 - eps]])
    return px[:, None] * chan

def posterior(joint):
    """P[x|y] from joint P[x,y]."""
    P = _clip(joint)
    py = P.sum(axis=0, keepdims=True)
    return P / py


# ----------------------------------------------------------------------------
# Online learning / dynamics (doc 05): multiplicative-weights belief flow.
#   p_{t+1}(i) ∝ p_t(i) * exp(eta * reward_i)   — mirror descent in KL geometry.
#   For log-loss prediction the natural update is the Bayesian posterior; we use
#   a simple online Bayesian estimator (Dirichlet) which is MW with the right loss.
# ----------------------------------------------------------------------------

def online_bayes_dissipation(q, T, rng, alpha=0.5, drift=None):
    """Run online Bayesian learning of a categorical world.
    Returns (cum_regret, cum_dissipation, per_round_dissipation).
      cum_regret      = sum_t ln(q[x_t]/p_t[x_t])      (realised log-loss regret)
      cum_dissipation = sum_t D(q_t || p_t)            (expected, theory)
    Thesis (doc 05 §1): E[regret] == cum_dissipation; learning == value recovery.
    `drift`: if set, q rotates each round at this speed (non-stationary world)."""
    q_base = _clip(np.array(q, dtype=float)); q_base = q_base / q_base.sum()
    m = len(q_base)
    counts = np.full(m, alpha)              # Dirichlet prior
    cum_regret = 0.0
    cum_diss = 0.0
    per_round = []
    qt = q_base.copy()
    for t in range(T):
        if drift:
            # a PERSISTENTLY moving target: the peak walks around the simplex
            # forever (never settles), so an infinite-memory learner cannot track
            # it and pays a standing dissipation floor (Dynamical Second Law).
            phase = int(t * drift) % m
            qt = np.roll(q_base, phase)
        p_t = counts / counts.sum()         # current belief
        x = rng.choice(m, p=qt)
        cum_regret += np.log(_clip(qt)[x] / _clip(p_t)[x])
        cum_diss += kl(qt, p_t)
        per_round.append(kl(qt, p_t))
        counts[x] += 1.0
    return cum_regret, cum_diss, np.array(per_round)


# ----------------------------------------------------------------------------
# Rebalanced portfolios over agents (doc 03 price / doc 04 operating point)
#   The fleet's shared resource is split by weights w over m agents; each round
#   the pool multiplies by sum_a w_a R_a(t). Kelly/price weights maximise the
#   time-average growth E[ln sum_a w_a R_a]. "Pricing" == rebalance to Kelly.
# ----------------------------------------------------------------------------

def portfolio_growth(weights, returns):
    """Time-average log-growth of a rebalanced fleet.
    returns: (T, m) gross per-round returns; weights: (m,)."""
    w = np.asarray(weights, dtype=float); w = w / w.sum()
    port = returns @ w
    return float(np.mean(np.log(_clip(port))))

def kelly_weights(returns, iters=4000, lr=0.05):
    """Projected-gradient ascent of E[ln(R w)] over the simplex — the price/
    Kelly operating point (doc 04 §3). Concave, so this finds the global max."""
    T, m = returns.shape
    w = np.full(m, 1.0 / m)
    R = _clip(returns)
    for _ in range(iters):
        port = R @ w
        grad = (R / port[:, None]).mean(axis=0)   # d/dw E[ln(Rw)]
        w = w + lr * grad
        w = np.clip(w, 0, None)
        s = w.sum()
        w = w / s if s > 0 else np.full(m, 1.0 / m)
    return w
