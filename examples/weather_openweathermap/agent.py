#!/usr/bin/env python3
import sys, os, json, traceback, urllib.request, urllib.parse
from datetime import datetime

META = {
    "schema": 1,
    "playground": { "input": { "type": "text", "placeholder": "Type a city (e.g. London)" } }
}

def _describe_if_requested():
    if os.environ.get("PLAYGROUND_DESCRIBE") == "1" or (len(sys.argv) > 1 and sys.argv[1] == "--describe"):
        print(json.dumps(META)); sys.exit(0)

now = lambda: datetime.now().strftime('%H:%M:%S')
GREEN, RED, RESET = "\033[92m", "\033[91m", "\033[0m"
def log(msg, col=GREEN): print(f"{col}[{now()}] {msg}{RESET}", flush=True)

def run_task(city: str, secrets: dict):
    city = (city or "").strip()
    if not city:
        print(json.dumps({"error": "Please type a city name."}, indent=2)); return

    key = secrets.get("AGENT_OWM_KEY") or os.environ.get("AGENT_OWM_KEY")
    if not key:
        raise RuntimeError("Missing AGENT_OWM_KEY (add it in Credentials)")

    q = urllib.parse.quote(city)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={q}&units=metric&appid={key}"
    with urllib.request.urlopen(url, timeout=8) as r:
        data = json.loads(r.read().decode("utf-8", "ignore"))

    out = {
        "city": data.get("name"),
        "temp_c": (data.get("main") or {}).get("temp"),
        "sky": ((data.get("weather") or [{}])[0]).get("description")
    }
    print(json.dumps(out, indent=2), flush=True)

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
