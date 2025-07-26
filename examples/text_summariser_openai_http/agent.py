#!/usr/bin/env python3
import sys, os, json, traceback, urllib.request
from datetime import datetime

META = {
    "schema": 1,
    "playground": { "input": { "type": "textarea", "placeholder": "Paste text to summarise…" } }
}

def _describe_if_requested():
    if os.environ.get("PLAYGROUND_DESCRIBE") == "1" or (len(sys.argv) > 1 and sys.argv[1] == "--describe"):
        print(json.dumps(META)); sys.exit(0)

now = lambda: datetime.now().strftime('%H:%M:%S')
GREEN, RED, RESET = "\033[92m", "\033[91m", "\033[0m"
def log(msg, col=GREEN): print(f"{col}[{now()}] {msg}{RESET}", flush=True)

def run_task(text: str, secrets: dict):
    text = (text or "").strip()
    if not text:
        print(json.dumps({"error": "Paste some text to summarise."}, indent=2)); return

    key = secrets.get("AGENT_OPENAI_KEY") or os.environ.get("AGENT_OPENAI_KEY")
    if not key:
        raise RuntimeError("Missing AGENT_OPENAI_KEY (add it in Credentials)")

    body = {
      "model": "gpt-4o-mini",
      "messages": [
        {"role": "system", "content": "Summarise in 3 concise sentences."},
        {"role": "user", "content": text}
      ]
    }
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.loads(r.read().decode("utf-8", "ignore"))

    summary = (data.get("choices") or [{}])[0].get("message", {}).get("content", "").strip()
    print(json.dumps({"summary": summary}, indent=2), flush=True)

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
