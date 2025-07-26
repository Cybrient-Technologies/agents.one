#!/usr/bin/env python3
import sys, os, json, traceback, urllib.request
from datetime import datetime

META = {
    "schema": 1,
    "playground": { "input": { "type": "text", "placeholder": "Type a coin id (e.g. bitcoin)" } }
}

def _describe_if_requested():
    if os.environ.get("PLAYGROUND_DESCRIBE") == "1" or (len(sys.argv) > 1 and sys.argv[1] == "--describe"):
        print(json.dumps(META)); sys.exit(0)

now = lambda: datetime.now().strftime('%H:%M:%S')
GREEN, RED, RESET = "\033[92m", "\033[91m", "\033[0m"
def log(msg, col=GREEN): print(f"{col}[{now()}] {msg}{RESET}", flush=True)

def run_task(symbol: str, _secrets: dict):
    s = (symbol or "").strip().lower()
    if not s:
        print(json.dumps({"error": "Type a coin id, e.g. bitcoin"}, indent=2)); return

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={s}&vs_currencies=usd"
    with urllib.request.urlopen(url, timeout=6) as r:
        data = json.loads(r.read().decode("utf-8", "ignore"))

    if s not in data:
        raise ValueError("Unknown coin id")

    print(json.dumps({"coin": s, "usd": data[s]["usd"]}, indent=2), flush=True)

def main():
    _describe_if_requested()
    log("Agent started. Waiting for input…")
    try:
        user_input = sys.stdin.readline().rstrip("\n")
        if user_input.lower() == "exit":
            log("Exit command received. Stopping agent."); return
        secrets = {k: v for k, v in os.environ.items() if k.startswith("AGENT_")}
        run_task(user_input, secrets)
    except Exception as e:
        log(f"[ERROR] {e}", RED); traceback.print_exc()

if __name__ == "__main__":
    main()
