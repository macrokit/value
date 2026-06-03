"""
execute_code.py — produce the discrete `pred` for the `code` shape by EXECUTING each
model's generated function and hashing its output (PREREGISTRATION_lever2.md §2.3).

Isolation: untrusted small-model code is executed on the CHINA MAC via SSH (off the main
Mac), inside a restricted driver (os/sys/subprocess/socket import blocked) with a 5 s
SIGALRM timeout and an outer SSH timeout. Decoupled from generation so it can be deferred.

For each cached code sample: extract the first ```python block, keep the function defs
(drop the model's own asserts/test lines), call item['call'], capture repr(output);
pred = hash_modk(repr(output)) mod K, or '?' on no-code / exception / timeout. Results are
written back into results/raw/{short}__code.json (field 'pred', 'exec_out'); cached.

Run: python3 execute_code.py            (all models present)
     python3 execute_code.py qwen7b     (one model)
"""
from __future__ import annotations
import json, os, sys, re, subprocess
import datasets_shapes as DS

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "results", "raw")
SSH_HOST = os.environ.get("CHINA_HOST", "blueidea@MacBook-Pro.local")
K = DS.K_CODE

_DRIVER_HEAD = (
    "import signal, builtins\n"
    "def _to(s,f): raise TimeoutError()\n"
    "signal.signal(signal.SIGALRM,_to); signal.alarm(5)\n"
    "_BLOCK={'os','sys','subprocess','socket','shutil','pathlib','urllib','requests','ctypes'}\n"
    "_ri=builtins.__import__\n"
    "def _imp(n,*a,**k):\n"
    "    if n.split('.')[0] in _BLOCK: raise ImportError('blocked:'+n)\n"
    "    return _ri(n,*a,**k)\n"
    "builtins.__import__=_imp\n"
)
_DRIVER_TAIL = (
    "_ns={}\n"
    "try:\n"
    "    exec(_code,_ns); _r=eval(_call,_ns); print('OK\\t'+repr(_r))\n"
    "except Exception as e: print('ERR\\t'+type(e).__name__)\n"
)

def _driver(code, call):
    # embed code/call as Python string literals; whole script piped to `python3 -`
    return _DRIVER_HEAD + f"_code={code!r}\n_call={call!r}\n" + _DRIVER_TAIL

def extract_code(text):
    if not text: return ""
    m = re.search(r"```(?:python)?\s*(.*?)```", text, re.DOTALL)
    block = m.group(1) if m else text
    # keep lines up to (and including) defs/bodies; drop top-level asserts/tests/prints
    out = []
    for ln in block.splitlines():
        s = ln.strip()
        if s.startswith("assert ") or s.startswith("print(") or s.startswith(">>>"):
            continue
        out.append(ln)
    return "\n".join(out)

def run_remote(code, call):
    src = _driver(code, call)
    try:
        p = subprocess.run(
            ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=8", SSH_HOST, "python3", "-"],
            input=src.encode(), capture_output=True, timeout=20)
        out = p.stdout.decode(errors="replace").strip().splitlines()
        for ln in out:
            if ln.startswith("OK\t"): return ("OK", ln[3:])
            if ln.startswith("ERR\t"): return ("ERR", ln[4:])
        return ("ERR", "no-output")
    except subprocess.TimeoutExpired:
        return ("ERR", "timeout")
    except Exception as e:
        return ("ERR", f"ssh:{type(e).__name__}")

def process(short):
    data = DS.load("code"); by_id = {it["id"]: it for it in data["items"]}
    path = os.path.join(RAW, f"{short}__code.json")
    if not os.path.exists(path):
        print(f"  (no code run for {short})"); return
    cache = json.load(open(path)); changed = 0; done = 0
    for sid, o in cache.items():
        if o.get("pred") not in (None, "__CODE__") and "exec_out" in o:
            done += 1; continue  # already executed (cached)
        it = by_id.get(int(sid))
        if not it: continue
        code = extract_code(o.get("text", ""))
        if not code.strip():
            o["pred"], o["exec_out"] = "?", "no-code"; changed += 1; continue
        status, val = run_remote(code, it["call"])
        if status == "OK":
            o["pred"] = str(DS.hash_modk(val, K)); o["exec_out"] = val[:200]
        else:
            o["pred"], o["exec_out"] = "?", val
        changed += 1
        if changed % 20 == 0:
            json.dump(cache, open(path, "w"), indent=2)
            print(f"  [{short}] executed {changed}…", flush=True)
    json.dump(cache, open(path, "w"), indent=2)
    acc = sum(v["pred"] == v["gold"] for v in cache.values()) / max(len(cache), 1)
    unp = sum(v["pred"] == "?" for v in cache.values())
    print(f"[{short}/code] executed {changed} (+{done} cached). acc={acc:.3f} '?'={unp}/{len(cache)}", flush=True)

def main():
    shorts = sys.argv[1].split(",") if len(sys.argv) > 1 else \
        ["qwen0.5b","llama1b","qwen1.5b","gemma2b","qwen3b","llama3b","qwen7b","llama8b"]
    # sanity: SSH reachable?
    try:
        t = subprocess.run(["ssh","-o","BatchMode=yes","-o","ConnectTimeout=8",SSH_HOST,"echo","ok"],
                           capture_output=True, timeout=15)
        if b"ok" not in t.stdout:
            print("SSH to China Mac not ready — code execution DEFERRED."); return
    except Exception as e:
        print(f"SSH to China Mac failed ({e}) — code execution DEFERRED."); return
    for s in shorts:
        process(s)

if __name__ == "__main__":
    main()
