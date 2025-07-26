# Agents.one — Public Examples

This repository contains **ready-to-use** `agent.py` examples that run inside the
[Agents.one](https://agents.one) Playground. Each example is a **single Python file** with no external
dependencies (stdlib only), and is designed to:

* Read one line of input from **stdin**
* Stream output via `print(..., flush=True)`
* Access dashboard‑managed secrets via `AGENT_*` environment variables
* Optionally **self‑describe** the input field (placeholder & type), so the Playground renders the right UI

> The Playground spins up a short‑lived Python 3.11 process and streams anything your agent prints.

---

## Quick start (using an example)

1. Open your Agents.one dashboard → **Agent** → **Upload**.
2. Upload one of the `agent.py` files from `examples/*`.
3. (Optional) Add credentials in **Agent → Credentials** (e.g. `AGENT_OPENAI_KEY`, `AGENT_OWM_KEY`).
4. Open your public Playground link and try it live.

---

## Included examples

* **Universal Template** — copy → paste → edit starter
  `examples/universal/agent.py`

* **Weather (OpenWeatherMap)** — input: city, requires `AGENT_OWM_KEY`
  `examples/weather_openweathermap/agent.py`

* **Crypto Quote (CoinGecko)** — input: coin id (e.g., `bitcoin`), no key required
  `examples/crypto_coingecko/agent.py`

* **Text Summariser (OpenAI via HTTP)** — input: text, requires `AGENT_OPENAI_KEY`
  `examples/text_summariser_openai_http/agent.py`

> These examples stick to the Python **standard library** for zero‑setup portability.

---

## Credentials

Add secrets in your dashboard under **Agent → Credentials** as `AGENT_*` names (for example
`AGENT_OPENAI_KEY`, `AGENT_OWM_KEY`). They are injected as environment variables at runtime.

Access them in code using either:

```python
key = secrets.get("AGENT_OPENAI_KEY") or os.environ.get("AGENT_OPENAI_KEY")
```

**Do not print secret values.** If you need to debug, log only the key **names** (e.g.,
`["AGENT_OPENAI_KEY"]`).

---

## Input handling

All examples accept:

* **Plain text** (default)
* **JSON** (auto‑detected when input starts with `{` or `[`; parsed via `json.loads`)
* **URLs** (you can add URL‑specific handling in your agent)

A common helper used across examples:

```python
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
```

---

## Self‑describing the input field (optional)

You can **hint** the Playground how to render the input (single‑line text, textarea, or url) and which
placeholder to show. Include a `META` dict and exit early when we call you with `PLAYGROUND_DESCRIBE=1`:

```python
META = {
  "schema": 1,
  "playground": { "input": { "type": "text", "placeholder": "Type a command" } }
}

def _describe_if_requested():
    if os.environ.get("PLAYGROUND_DESCRIBE") == "1" or (len(sys.argv) > 1 and sys.argv[1] == "--describe"):
        print(json.dumps(META)); sys.exit(0)
```

Supported types today: `"text"`, `"textarea"`, `"url"`.

---

## Streaming & UX

* Print progressively and include `flush=True` to stream partial results.
* The Playground shows a server‑driven **“Loading …”** spinner while your agent runs and a
  persistent **“Waiting for next input …”** status when it completes. The connection remains open
  with periodic heartbeats so users can immediately run another input.

---

## Local testing

Each agent reads **one line** from stdin. Run locally:

```bash
python3 examples/universal/agent.py
# Type your input and press Enter
```

If your project ships a local virtual environment (e.g. `.venv/`), you can test with its interpreter too.

---

## Repository structure

```
examples/
  universal/agent.py
  weather_openweathermap/agent.py
  crypto_coingecko/agent.py
  text_summariser_openai_http/agent.py
README.md
LICENSE
```

> This public repo intentionally includes **examples only** (no platform internals).

---

## Security & best practices

* Keep `agent.py` small for fast cold starts.
* Use HTTPS for outbound calls and reasonable timeouts.
* Never print secrets; consider redacting any accidental dumps in your code.
* Treat each run as stateless; persist via your own backend if needed.

---

## Contributing

Contributions are welcome! Add a new folder under `examples/` containing a single `agent.py` and a short
README snippet explaining the input and any required `AGENT_*` credentials.

---

## License

MIT — see [LICENSE](LICENSE).

---

**Need help?** If you want guidance adapting your agent to this template (credentials, streaming, error
handling), open an issue or reach out to support.
