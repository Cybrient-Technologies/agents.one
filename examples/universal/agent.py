#!/usr/bin/env python3
import sys, os, json, traceback
from datetime import datetime

# Optional: self-describe the input field so the Playground can render UI hints.
META = {
    "schema": 1,
    "playground": {
        "input": {
            "type": "text",                      # "text" | "textarea" | "url"
            "placeholder": "Type a command"      # hint for the input field
        }
    }
}

def _describe_if_requested():
    if os.environ.get("PLAYGROUND_DESCRIBE") == "1" or (len(sys.argv) > 1 and sys.argv[1] == "--describe"):
        print(json.dumps(META)); sys.exit(0)

# ── tiny console helpers ─────────────────────────────────────────────────────
now = lambda: datetime.now().strftime('%H:%M:%S')
GREEN, RED, RESET = "\033[92m", "\033[91m", "\033[0m"
def log(msg, col=GREEN): print(f"{col}[{now()}] {msg}{RESET}", flush=True)

# ── input normalization ──────────────────────────────────────────────────────
def parse_input(raw: str):
    raw = (raw or "").strip()
    if not raw:
        return {"text": "", "json": None}
    try:
        if raw[:1] in "{[":
            return {"text": raw, "json": json.loads(raw)}
    except Exception:
        pass
    return {"text": raw, "json": None}

# ── your task logic ──────────────────────────────────────────────────────────
def run_task(user_input: str, secrets: dict):
    data = parse_input(user_input)

    # Example: read dashboard secret (never print actual values)
    openai_key = secrets.get("AGENT_OPENAI_KEY") or os.environ.get("AGENT_OPENAI_KEY")
    # if openai_key: ... call your API over HTTPS

    result = {
        "received": data["text"],
        "parsed_json": data["json"],
        "available_secrets": sorted([k for k in (secrets or {}).keys() if k.startswith("AGENT_")]),
    }
    print(json.dumps(result, indent=2), flush=True)

def main():
    _describe_if_requested()
    log("Agent started. Waiting for input…")
    try:
        user_input = sys.stdin.readline().rstrip("\n")
        if user_input.lower() == "exit":
            log("Exit command received. Stopping agent."); return
        secrets = {k: v for k, v in os.environ.items() if k.startswith("AGENT_")}
        run_task(user_input, secrets)
        # No need to print "Done." — the Playground handles idle spinner.
    except Exception as e:
        log(f"[ERROR] {e}", RED); traceback.print_exc()

if __name__ == "__main__":
    main()
