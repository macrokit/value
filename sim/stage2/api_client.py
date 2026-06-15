"""
api_client.py — cached Anthropic API chat backend for the Stage 2 gate.

Mirrors the cache contract of sim/field/real/llm_economy._chat so the EXACT niche
economy can be driven by a frontier model with one line: pass `chat_fn=make_chat(...)`
to LLMEconomy. No SDK dependency (raw REST via urllib). Every call cached in
gate_cache.sqlite keyed by (model,temp,seed,agent,round,prompt) — deterministic given
the cache, offline-auditable, restart-safe.

Cost is tracked from the API's returned usage and enforced against a HARD CAP: the
client raises BudgetExceeded before issuing a call that could carry total spend over
the cap. The key is read from $ANTHROPIC_API_KEY (owner-provided); never hard-coded.

Author byline: Cheng Qian.
"""
from __future__ import annotations
import os, json, time, hashlib, sqlite3, threading, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")
os.makedirs(RESULTS, exist_ok=True)
CACHE_DB = os.path.join(RESULTS, "gate_cache.sqlite")
API_URL = "https://api.anthropic.com/v1/messages"
_LOCK = threading.Lock()

# list prices ($ per 1e6 tokens); used only for the local cap accounting
PRICES = {
    "opus":   (15.0, 75.0),
    "sonnet": (3.0, 15.0),
    "haiku":  (0.80, 4.0),
}


class BudgetExceeded(Exception):
    pass


def _price_for(model: str):
    m = model.lower()
    for key, p in PRICES.items():
        if key in m:
            return p
    return PRICES["opus"]  # unknown → price as the most expensive tier (conservative)


def _db():
    con = sqlite3.connect(CACHE_DB, check_same_thread=False, timeout=60)
    con.execute("CREATE TABLE IF NOT EXISTS c (k TEXT PRIMARY KEY, v TEXT)")
    con.execute("CREATE TABLE IF NOT EXISTS usage "
                "(k TEXT PRIMARY KEY, model TEXT, tin INT, tout INT)")
    return con

_CON = _db()


def _cache_get(key):
    with _LOCK:
        r = _CON.execute("SELECT v FROM c WHERE k=?", (key,)).fetchone()
    return r[0] if r else None


def _cache_put(key, val, model, tin, tout):
    with _LOCK:
        _CON.execute("INSERT OR REPLACE INTO c VALUES (?,?)", (key, val))
        _CON.execute("INSERT OR REPLACE INTO usage VALUES (?,?,?,?)",
                     (key, model, int(tin), int(tout)))
        _CON.commit()


def spent_usd() -> float:
    """Total $ implied by all cached usage rows (idempotent; cache hits cost $0)."""
    with _LOCK:
        rows = _CON.execute("SELECT model, tin, tout FROM usage").fetchall()
    tot = 0.0
    for model, tin, tout in rows:
        pin, pout = _price_for(model)
        tot += tin * pin / 1e6 + tout * pout / 1e6
    return tot


def make_chat(model: str, cap_usd: float, max_tokens: int = 64, max_retry: int = 4,
              system: str | None = None):
    """Return a chat_fn(model, temp, prompt, seed, agent, rnd, k=) -> text with the
    llm_economy._chat signature. `model` here is authoritative; the first positional
    arg from LLMEconomy is ignored so the economy's own model string can't override the
    pre-registered API model. cap_usd is the HARD cap across the shared cache."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    def chat(_model_ignored, temp, prompt, seed, agent, rnd, k=8, max_retry=max_retry):
        key = hashlib.sha256(
            f"{model}|{temp}|{seed}|{agent}|{rnd}|{prompt}".encode()).hexdigest()
        hit = _cache_get(key)
        if hit is not None:
            return hit
        if api_key is None:
            raise RuntimeError("ANTHROPIC_API_KEY not set — owner must provide the key "
                               "before any live call.")
        # cap check BEFORE spending (worst-case next-call estimate)
        pin, pout = _price_for(model)
        est = (len(prompt) / 3.5) * pin / 1e6 + max_tokens * pout / 1e6
        if spent_usd() + est > cap_usd:
            raise BudgetExceeded(
                f"would exceed cap ${cap_usd:.2f} (spent ${spent_usd():.2f} + est ${est:.4f})")
        body = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": float(temp),
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            body["system"] = system
        data = json.dumps(body).encode()
        for attempt in range(max_retry):
            try:
                req = urllib.request.Request(
                    API_URL, data=data,
                    headers={"Content-Type": "application/json",
                             "x-api-key": api_key,
                             "anthropic-version": "2023-06-01"})
                resp = json.loads(urllib.request.urlopen(req, timeout=120).read())
                txt = "".join(b.get("text", "") for b in resp.get("content", []))
                u = resp.get("usage", {})
                _cache_put(key, txt, model,
                           u.get("input_tokens", 0), u.get("output_tokens", 0))
                return txt
            except BudgetExceeded:
                raise
            except Exception as e:
                if attempt == max_retry - 1:
                    raise
                time.sleep(1.5 * (attempt + 1))

    return chat


def health_check(model: str):
    """One tiny live call to confirm key + model + parsing. Counts against the cache."""
    try:
        fn = make_chat(model, cap_usd=1.0, max_tokens=16)
        txt = fn("", 0.0, 'Reply with only the JSON {"niche": 3}.', 0, 0, -1, k=8)
        return ('"niche"' in txt or "3" in txt), txt.strip()[:40]
    except Exception as e:
        return False, str(e)[:120]
