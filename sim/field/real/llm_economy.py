"""
llm_economy.py — a dynamic value-economy whose microscopic rule is a REAL small LLM.

Rung 7 of the wave/field-theory thread (HANDOFF-wave-theory.md; thresholds frozen in
PREREGISTRATION.md). N agents choose, each round, which of K niches to pursue. The
choice is made by qwen2.5:0.5b-instruct (China-Mac Ollama fleet) reading its own
payoff history and its neighbours' latest choices — NOT a replicator equation. The
economy rewards coordinating with neighbours (the alignment dividend = the coupling),
plus per-niche rewards (a value-shock bumps one niche), plus an optional control field
(the mass term). LLM sampling temperature is the noise knob.

The question (vs the toy sim/field/dynamic, which used a hand-coded replicator rule):
do the demand wave and the collective-goal transition survive when the micro-rule is
emergent model behaviour? See PREREGISTRATION.md §0 for the falsification clause.

Every model call is cached (sqlite) by (model,temp,seed,agent,round,prompt) so runs
are deterministic given seeds and fully re-runnable offline.
"""
from __future__ import annotations
import os, json, time, hashlib, sqlite3, threading, urllib.request
import concurrent.futures as cf
import numpy as np

OLLAMA = os.environ.get("OLLAMA_URL", "http://localhost:11434")
HERE = os.path.dirname(__file__)
CACHE_DB = os.path.join(HERE, "results", "cache.sqlite")
os.makedirs(os.path.join(HERE, "results"), exist_ok=True)

K = 8                      # number of niches (frozen, PREREG §1)
_LOCK = threading.Lock()


# --------------------------------------------------------------------------- cache
def _db():
    con = sqlite3.connect(CACHE_DB, check_same_thread=False, timeout=60)
    con.execute("CREATE TABLE IF NOT EXISTS c (k TEXT PRIMARY KEY, v TEXT)")
    return con

_CON = _db()

def _cache_get(key):
    with _LOCK:
        r = _CON.execute("SELECT v FROM c WHERE k=?", (key,)).fetchone()
    return r[0] if r else None

def _cache_put(key, val):
    with _LOCK:
        _CON.execute("INSERT OR REPLACE INTO c VALUES (?,?)", (key, val))
        _CON.commit()


# --------------------------------------------------------------------------- LLM
def _chat(model, temp, prompt, seed, agent, rnd, max_retry=3, k=K):
    """One cached LLM call. Returns the raw text. Deterministic per cache key.
    `k`: niche count for the structured-output schema (default K=8 preserves all
    historical cache keys/behaviour; the prompt text differs per k so keys never
    collide across niche counts)."""
    key = hashlib.sha256(
        f"{model}|{temp}|{seed}|{agent}|{rnd}|{prompt}".encode()).hexdigest()
    hit = _cache_get(key)
    if hit is not None:
        return hit
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        # structured output: force a valid niche integer 0..k-1 (keeps temperature as
        # the noise knob, but removes the out-of-range/garbled-token parse failures the
        # 0.5B model produces at high temp — see PREREGISTRATION P-parse gate)
        "format": {"type": "object",
                   "properties": {"niche": {"type": "integer",
                                            "minimum": 0, "maximum": k - 1}},
                   "required": ["niche"]},
        "options": {"temperature": float(temp), "num_predict": 24,
                    "seed": int(seed) * 100003 + int(agent) * 131 + int(rnd)},
    }
    data = json.dumps(body).encode()
    for attempt in range(max_retry):
        try:
            req = urllib.request.Request(OLLAMA + "/api/chat", data=data,
                                         headers={"Content-Type": "application/json"})
            txt = json.loads(urllib.request.urlopen(req, timeout=120).read())["message"]["content"]
            _cache_put(key, txt)
            return txt
        except Exception as e:
            if attempt == max_retry - 1:
                raise
            time.sleep(1.5 * (attempt + 1))


def _parse_niche(txt, k=K):
    """Extract the niche 0..k-1 from the model output. Prefer the JSON {"niche": n}
    produced by the structured-output format; fall back to the first in-range integer."""
    if not txt:
        return None
    try:
        n = int(json.loads(txt)["niche"])
        if 0 <= n < k:
            return n
    except Exception:
        pass
    tok, num = "", []
    for ch in txt:
        if ch.isdigit():
            tok += ch
        else:
            if tok:
                num.append(int(tok)); tok = ""
    if tok:
        num.append(int(tok))
    for n in num:
        if 0 <= n < k:
            return n
    return None


def _prompt(niche_rewards, own_hist, nbr_choices, salient=False, k=K):
    """Build the per-agent decision prompt. own_hist: list of (niche,payoff) recent;
    nbr_choices: list of neighbours' latest niches."""
    rw = ", ".join(f"niche {j}: {niche_rewards[j]:.1f}" for j in range(k))
    hist = ("; ".join(f"chose {n}->got {p:.1f}" for n, p in own_hist[-3:])
            if own_hist else "none yet")
    # present neighbours as a TALLY (counts per niche) — digestible for a 0.5B model;
    # it is still the model's choice which niche to pick (we do not pre-pick the mode)
    from collections import Counter
    if len(nbr_choices):
        cnt = Counter(int(c) for c in nbr_choices)
        nbr = ", ".join(f"niche {k}: {cnt[k]} neighbour(s)" for k in sorted(cnt))
    else:
        nbr = "no neighbours"
    # salient mode (wave re-test, per reward-salience check): foreground a large
    # per-niche reward so it is not lost among the coordination signal + token bias
    bonus = ""
    if salient:
        kmax = int(np.argmax(niche_rewards))
        if niche_rewards[kmax] > 0:
            bonus = (f"IMPORTANT: niche {kmax} pays a BONUS of +{niche_rewards[kmax]:.0f} "
                     f"this round (far more than any other niche).\n")
    return (
        f"You are an agent in a group choosing which of {k} work-niches "
        f"(numbered 0 to {k - 1}) to join next round.\n"
        "You earn MORE when you pick the SAME niche as most of your neighbours "
        "(teamwork bonus), PLUS that niche's own reward shown below.\n"
        + bonus +
        f"Niche rewards this round: {rw}.\n"
        f"Your recent rounds: {hist}.\n"
        f"How many of your neighbours are in each niche right now: {nbr}.\n"
        "Pick the single niche that maximises your payoff next round (joining where "
        "your neighbours already are usually pays best). "
        f'Respond as JSON: {{"niche": <integer 0 to {k - 1}>}}.'
    )


# --------------------------------------------------------------------------- economy
class LLMEconomy:
    def __init__(self, N=20, model="qwen2.5:0.5b-instruct", temp=0.6, J=1.0,
                 gamma=0.0, k_star=0, topology="annealed", n_nb=6, ring_k=3,
                 lag=0, seed=0, pool=8, salient=False, symbol_random=False, k=K):
        """topology: 'annealed' (fresh random n_nb neighbours each round = motile/
        mean-field) | 'quenched' (fixed ring +/- ring_k = low-D) | 'ring' (ring +/-
        ring_k, used for the wave). lag L = switching commitment (reallocation inertia).
        salient = foreground the rewarded niche in the prompt (wave re-test).
        symbol_random (Rung 8, guardrail (a)): each agent sees niches under its OWN fixed
        random label permutation, so the model's token prior maps to a different *true*
        niche per agent (collective token bias cancels) while coordination/reward-reading
        are still processed by the model. Physics (m, payoffs, shock, γ) stays in TRUE
        niche space; only what the model SEES is relabelled.
        """
        self.N, self.model, self.temp, self.J = N, model, temp, J
        self.gamma, self.k_star, self.topology = gamma, k_star, topology
        self.n_nb, self.ring_k, self.lag, self.seed, self.pool = n_nb, ring_k, lag, seed, pool
        self.salient = salient
        self.symbol_random = symbol_random
        self.K = k                                            # niche count (default 8)
        # per-agent label permutation: perm[a][true]=label_shown; inv[a][label]=true
        pr = np.random.default_rng(seed * 2654435761 % (2**32))
        if symbol_random:
            self.perm = np.array([pr.permutation(self.K) for _ in range(N)])
        else:
            self.perm = np.tile(np.arange(self.K), (N, 1))
        self.inv = np.argsort(self.perm, axis=1)
        self.rng = np.random.default_rng(seed)
        self.niche = self.rng.integers(0, self.K, size=N)     # initial niches
        self.rewards = np.zeros(self.K)                       # per-niche base reward R_k
        self.shock = None                                    # (k0, x0, halfwidth, amp) or None
        self.hist = [[] for _ in range(N)]                   # per-agent [(niche,payoff)]
        self.since_switch = np.zeros(N, dtype=int)           # rounds since last switch
        self.shock_t0 = 0                                    # round at which shock turns on
        self.cur_round = 0
        self.parse_ok = 0
        self.parse_tot = 0

    # -- neighbour sets --------------------------------------------------------
    def _neighbours(self, a, rnd):
        if self.topology == "annealed":
            r = np.random.default_rng(self.seed * 7919 + rnd * 131 + a)
            cand = [j for j in range(self.N) if j != a]
            return list(r.choice(cand, size=min(self.n_nb, len(cand)), replace=False))
        else:  # quenched / ring: fixed ring neighbours +/- ring_k
            return [(a + d) % self.N for d in range(-self.ring_k, self.ring_k + 1) if d != 0]

    # -- per-agent reward vector shown to the LLM (incl shock + control) -------
    def _niche_rewards_for(self, a):
        rw = self.rewards.copy()
        if self.shock is not None and self.cur_round >= self.shock_t0:
            k0, x0, hw, amp = self.shock
            # localized on a ring: agents within hw of locus x0 see niche k0 boosted
            dist = min(abs(a - x0), self.N - abs(a - x0))
            if dist <= hw:
                rw[k0] += amp
        if self.gamma > 0:
            rw[self.k_star] += self.gamma
        return rw

    # -- payoff actually realized (used for history shown next round) ----------
    def _payoff(self, a, nbrs):
        same = np.mean([self.niche[j] == self.niche[a] for j in nbrs]) if nbrs else 0.0
        rw = self._niche_rewards_for(a)
        return self.J * same + rw[self.niche[a]]

    # -- one round -------------------------------------------------------------
    def step(self, rnd):
        self.cur_round = rnd
        nbr_sets = [self._neighbours(a, rnd) for a in range(self.N)]
        # decide: agents locked by the switching lag keep their niche (inertia);
        # the rest consult the LLM in parallel (independent given last round's state)
        free = [a for a in range(self.N) if self.since_switch[a] >= self.lag]
        prompts = {}
        for a in free:
            rw = self._niche_rewards_for(a)                         # TRUE-niche rewards
            nbr_true = [int(self.niche[j]) for j in nbr_sets[a]]
            # translate EVERYTHING the model sees into agent a's private label space
            perm, inv = self.perm[a], self.inv[a]
            rw_label = rw[inv]                                      # rw_label[ℓ] = rw[true shown as ℓ]
            nbr_label = [int(perm[t]) for t in nbr_true]
            hist_label = [(int(perm[t]), p) for (t, p) in self.hist[a]]
            prompts[a] = _prompt(rw_label, hist_label, nbr_label, salient=self.salient,
                                 k=self.K)

        def decide(a):
            txt = _chat(self.model, self.temp, prompts[a], self.seed, a, rnd, k=self.K)
            return a, _parse_niche(txt, k=self.K)

        new_niche = self.niche.copy()
        if free:
            with cf.ThreadPoolExecutor(max_workers=self.pool) as ex:
                for a, label in ex.map(decide, free):
                    self.parse_tot += 1
                    if label is not None:
                        self.parse_ok += 1
                        new_niche[a] = int(self.inv[a][label])      # label -> TRUE niche
                    # else: keep current niche (default)

        # update switch counters BEFORE overwriting, and record payoffs (on new state)
        switched = new_niche != self.niche
        self.since_switch = np.where(switched, 0, self.since_switch + 1)
        self.niche = new_niche
        for a in range(self.N):
            self.hist[a].append((int(self.niche[a]), float(self._payoff(a, nbr_sets[a]))))

    # -- observables -----------------------------------------------------------
    def order_parameter(self):
        th = 2 * np.pi * self.niche / self.K
        return float(np.abs(np.mean(np.exp(1j * th))))

    def adoption_profile(self, k0):
        """Per-ring-position indicator of being on niche k0 (for the wave)."""
        return (self.niche == k0).astype(float)

    def run(self, T, burn, record_profile_k=None):
        ms, profiles = [], []
        for rnd in range(T):
            self.step(rnd)
            if rnd >= burn:
                ms.append(self.order_parameter())
            if record_profile_k is not None:
                profiles.append(self.adoption_profile(record_profile_k))
        ms = np.array(ms)
        out = {"m": float(ms.mean()), "m_std": float(ms.std()),
               "chi": float(self.N * ms.var()),
               "parse_rate": (self.parse_ok / self.parse_tot) if self.parse_tot else 1.0}
        if record_profile_k is not None:
            out["profiles"] = np.array(profiles)
        return out


def health_check():
    """Confirm the tunnel/model is live before a run."""
    try:
        txt = _chat("qwen2.5:0.5b-instruct", 0.0, "Reply with only the integer 3.",
                    seed=0, agent=0, rnd=-1)
        return _parse_niche(txt) is not None, txt.strip()[:20]
    except Exception as e:
        return False, str(e)[:80]


if __name__ == "__main__":
    ok, msg = health_check()
    print(f"health_check: {'OK' if ok else 'FAIL'} ({msg})")
