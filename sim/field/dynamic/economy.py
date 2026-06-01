"""
economy.py — microscopic, agent-based value economies for Thrust B of the
field-theory thread (HANDOFF-wave-theory.md). These are NOT PDE integrators.

The earlier sim/field/field_experiments.py *integrated the posited continuum PDEs*
(telegrapher, Vicsek) to check they have the claimed phenomenology. That answered
"does the continuum even behave as doc 08 says?" — yes — but it is circular as a
test of emergence: you put the wave equation in, you get a wave out.

Here we go one level down. Each site holds an *agent* with its own local state and
a local update rule that references only its neighbors (resource it ships, goal it
imitates, payoff it captures). Nothing in the update rule is a wave equation or a
Toner–Tu equation. The question (Thrust B) is whether the macroscopic FIELD that
emerges from these microscopic rules shows the telegrapher dispersion crossover
(RingEconomy) and the flocking phase transition (LatticeEconomy) — as *emergent*
collective phenomena. If it does, that is evidence the continuum field theory is the
coarse-grained limit of an agent value economy; if it does not, the field picture is
analogy. (The on-paper coarse-graining is docs/10-field-theory-derivation.md.)

Two economies:
  RingEconomy   — 1D ring; resource conservation + price-gradient-driven flow with a
                  finite flow-adjustment lag (reallocation inertia). Demand shocks.
  FlockEconomy  — 2D MOTILE population; goal directors imitate resource-capturing
                  neighbors (replicator-weighted), under control + noise; agents move
                  in their goal direction; resource follows a replicator payoff
                  (alignment dividend). Collective-goal formation. Motility is not a
                  flourish: on a *fixed* lattice the goal field is a 2D XY model with
                  scalar noise, which Mermin–Wagner forbids from ordering — spontaneous
                  flocking is a property of *motile* active matter (Toner–Tu). So the
                  agents must move for the §5 transition to be testable at all (itself
                  a finding: motility is *necessary* for spontaneous collective goals).

Both are deliberately the SMALLEST systems that contain evolving goals/resource +
local economic coupling. They are toy agents (cheap, controllable), the bridge
between the pure-physics sim/field and real LLM agents (HANDOFF Thrust B).
"""
from __future__ import annotations
import numpy as np


# ===========================================================================
# RingEconomy — 1D resource economy; emergent demand-shock propagation
# ===========================================================================
class RingEconomy:
    """N agents on a ring. Agent i holds resource e_i >= 0 and faces a local
    scarcity price π_i = ρ_i / e_i (high desire ρ or low resource e -> high price).
    Resource flows between neighbors to chase value (toward high price), but each
    agent adjusts its OUTFLOW rate toward the desired rate only partway each step —
    a finite flow-adjustment lag τ_J (reallocation inertia). That lag is the only
    thing standing between diffusion (τ_J -> 0) and a wave (τ_J large).

    Microscopic rules (no wave equation anywhere):
      price          π_i      = ρ_i / e_i
      desired flow   F*_{i}   = σ (π_{i+1} − π_i)        on edge i->i+1 (up price grad)
      flow inertia   F_i     += (dt/τ_J)(F*_i − F_i)     agents ease toward desired flow
      conservation   e_i     += dt (F_{i−1} − F_i)       inflow(left edge) − outflow(right)

    Linearising e=e0+δe, ρ=ρ0 (uniform) gives π ≈ π0 − (ρ0/e0²)δe, and the three
    rules combine to  τ_J ∂_tt δe + ∂_t δe = σ(ρ0/e0²) ∂_xx δe  — the telegrapher
    equation, with D=σρ0/e0², τ=τ_J, v=√(D/τ_J). We never write that PDE; we run the
    agents and MEASURE whether it emerges.
    """

    def __init__(self, N=2000, e0=1.0, rho0=1.0, sigma=20.0, tau_J=8.0, dt=0.02, seed=0):
        self.N, self.dt, self.tau_J, self.sigma = N, dt, tau_J, sigma
        self.e0, self.rho0 = e0, rho0
        self.e = np.full(N, float(e0))
        self.rho = np.full(N, float(rho0))
        self.F = np.zeros(N)                 # F[i] = flow on edge i -> i+1
        self._rng = np.random.default_rng(seed)

    def price(self):
        return self.rho / np.maximum(self.e, 1e-9)

    def step(self):
        pi = self.price()
        # desired flow on edge i->i+1: resource chases value (up the price gradient,
        # which for scarcity pricing is down the resource gradient => equalising/stable)
        Fstar = self.sigma * (np.roll(pi, -1) - pi)
        # finite flow-adjustment lag (reallocation inertia): ease toward desired flow
        self.F += (self.dt / self.tau_J) * (Fstar - self.F)
        # resource conservation: inflow from left edge (F[i-1]) minus outflow (F[i])
        self.e += self.dt * (np.roll(self.F, 1) - self.F)
        self.e = np.maximum(self.e, 1e-9)

    def inject_shock(self, width=8.0, amp=0.5):
        """A localized change in what is valued: bump desire ρ at the ring center.
        This is the 'demand shock' — a sudden niche-payoff change (HANDOFF Thrust B)."""
        x = np.arange(self.N)
        c = self.N // 2
        self.rho = self.rho0 + amp * np.exp(-((x - c) ** 2) / (2 * width ** 2))

    def run_shock(self, steps, rec_every=None, observable="e"):
        """Inject a desire shock, evolve, and record the chosen field's perturbation
        about its background each rec_every steps. Returns (times, X) with X[t] the
        full ring profile of (e−e0) or (π−π0)."""
        self.inject_shock()
        rec_every = rec_every or max(1, steps // 250)
        times, frames = [], []
        for n in range(steps):
            self.step()
            if n % rec_every == 0:
                if observable == "e":
                    frames.append(self.e - self.e0)
                else:
                    frames.append(self.price() - self.rho0 / self.e0)
                times.append((n + 1) * self.dt)
        return np.array(times), np.array(frames)

    # --- single-Fourier-mode probe, for the dispersion relation -------------
    def mode_decay(self, q_index, steps, amp=1e-3):
        """Seed a pure cosine perturbation δe ∝ cos(q x) with wavenumber set by
        q_index full wavelengths around the ring, evolve in the LINEAR regime, and
        return (times, amplitude(t)) of that mode — its decay/oscillation reveals
        ω(q): pure decay = diffusive mode, decaying oscillation = wave mode."""
        x = np.arange(self.N)
        q = 2 * np.pi * q_index / self.N
        self.e = self.e0 + amp * self.e0 * np.cos(q * x)
        self.rho = np.full(self.N, self.rho0)
        self.F = np.zeros(self.N)
        rec_every = max(1, steps // 600)
        times, a_q = [], []
        cos_q = np.cos(q * x)
        norm = (cos_q ** 2).sum()
        for n in range(steps):
            self.step()
            if n % rec_every == 0:
                # project (e-e0) onto cos(qx): signed modal amplitude
                a = float(((self.e - self.e0) * cos_q).sum() / norm)
                times.append((n + 1) * self.dt)
                a_q.append(a)
        return np.array(times), np.array(a_q), q


# ===========================================================================
# FlockEconomy — 2D motile goal economy; emergent collective-goal transition
# ===========================================================================
class FlockEconomy:
    """N motile agents in a periodic box [0,Lbox]². Agent a holds a goal director
    (angle θ_a), a resource weight w_a>0, and a position that moves at speed v0 in
    its goal direction. Goals adapt by imitating resource-CAPTURING neighbors within
    radius r (replicator-weighted alignment) under optional control toward a
    principal goal θ* and idiosyncratic noise η. Resource follows a replicator
    payoff: alignment with neighbors is a positive-sum 'alignment dividend' (doc 04
    §4), so well-aligned agents capture more resource and their goal spreads.

    Microscopic rules (no Toner–Tu equation anywhere):
      neighbors   a~b   iff |pos_a − pos_b| ≤ r  (periodic min-image)
      payoff      P_a   = Σ_{b~a} cos(θ_a − θ_b)               alignment dividend
      replicator  w_a  *= exp(dt (P_a − <P>)) ; renormalize     resource to who aligns
      imitation   z_a   = Σ_{b~a} w_b e^{iθ_b} + γ e^{iθ*}      resource-weighted + control
      goal update θ_a   = arg(z_a) + η·U(−π,π)                  copy + noise
      motion      pos_a += v0 (cosθ_a, sinθ_a) dt               self-propulsion

    Value economy, not plain Vicsek: the alignment weights w_b EVOLVE by a resource
    replicator (doc 05 §3b) rather than being fixed, and a control field γ (doc 05
    §3a) can pin the collective goal. Motility (v0>0) is required for spontaneous
    ordering in 2D (Toner–Tu beats Mermin–Wagner); v0=0 recovers the non-ordering
    fixed lattice. We MEASURE the order parameter and susceptibility vs noise η.
    """

    def __init__(self, N=400, Lbox=10.0, r=1.0, v0=0.3, eta=0.3, gamma=0.0,
                 theta_star=0.0, repl=0.5, dt=1.0, seed=0):
        self.N, self.Lbox, self.r, self.v0 = N, Lbox, r, v0
        self.eta, self.gamma, self.repl, self.dt = eta, gamma, repl, dt
        self.theta_star = theta_star
        self._rng = np.random.default_rng(seed)
        self.pos = self._rng.uniform(0, Lbox, size=(N, 2))
        self.th = self._rng.uniform(-np.pi, np.pi, size=N)
        self.w = np.ones(N) / N

    def _neighbor_mask(self):
        """Boolean (N,N) neighbor matrix within radius r (periodic min-image, incl self)."""
        d = self.pos[:, None, :] - self.pos[None, :, :]
        d -= self.Lbox * np.round(d / self.Lbox)
        return (d[:, :, 0] ** 2 + d[:, :, 1] ** 2) <= self.r * self.r

    def step(self):
        th = self.th
        nb = self._neighbor_mask()
        cos_t, sin_t = np.cos(th), np.sin(th)
        # alignment-dividend payoff: P_a = Σ_{b~a} cos(θ_a − θ_b)
        P = cos_t * (nb @ cos_t) + sin_t * (nb @ sin_t)
        # replicator: resource flows to who aligns (captures value)
        self.w *= np.exp(self.repl * self.dt * (P - P.mean()))
        self.w /= self.w.sum()
        # resource-weighted neighbor goal + control field γ toward θ*
        wc = self.w * cos_t
        ws = self.w * sin_t
        zx = nb @ wc + self.gamma * np.cos(self.theta_star)
        zy = nb @ ws + self.gamma * np.sin(self.theta_star)
        new_th = np.arctan2(zy, zx)
        new_th += self.eta * self._rng.uniform(-np.pi, np.pi, size=self.N)
        self.th = new_th
        # self-propelled motion in the (new) goal direction
        self.pos = (self.pos + self.v0 * np.stack([np.cos(new_th), np.sin(new_th)], 1)) % self.Lbox

    def order_parameter(self):
        """Polar order m = |<e^{iθ}>| over all agents (the collective-goal magnitude)."""
        return float(np.abs(np.mean(np.exp(1j * self.th))))

    def run(self, steps, burn=None, sample_every=2):
        """Evolve; after a burn-in, collect samples of m to estimate <m>, <m²> and
        the susceptibility χ = N(<m²> − <m>²). Returns dict of measured observables."""
        burn = burn if burn is not None else steps // 2
        ms = []
        for n in range(steps):
            self.step()
            if n >= burn and (n - burn) % sample_every == 0:
                ms.append(self.order_parameter())
        ms = np.array(ms)
        return {
            "m": float(ms.mean()),
            "m_std": float(ms.std()),
            "chi": float(self.N * (np.mean(ms ** 2) - ms.mean() ** 2)),
        }
