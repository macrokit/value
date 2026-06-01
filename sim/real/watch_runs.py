import time, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bench_data as B
DEADLINE = time.time() + 180*60     # 3h cap
TARGET = 4                          # full ladder: qwen1.5b, qwen3b, qwen7b, llama8b
last = -1
while True:
    fleet = B.available_fleet()
    shorts = [s for s, _, _ in fleet]
    n = len(fleet)
    if n != last:
        print(f"[{time.strftime('%H:%M:%S')}] ladder rungs available: {n} -> {shorts}", flush=True)
        last = n
    if n >= TARGET:
        print(f"FULL LADDER READY: {shorts}", flush=True); break
    if time.time() > DEADLINE:
        print(f"TIMEOUT with {n} rungs: {shorts}", flush=True); break
    time.sleep(90)
