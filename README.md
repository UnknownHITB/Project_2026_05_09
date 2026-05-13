# AI Chat Assistant

A simple AI assistant supporting both voice and text input, powered by Ollama. It can run as an **interactive CLI** (for local testing) or as an **HTTP backend** with **server-side chat sessions** (for phone, PC, or other clients over your network).

## Project Structure

- `main.py`: CLI entry point (voice or text); unchanged for local testing.
- `app/server.py`: FastAPI HTTP API (`uvicorn app.server:app`).
- `app/core/sessions.py`: SQLite-backed session history (separate from long-term `memory.sqlite`).
- `app/`: Core logic and providers.
  - `ollama_provider.py`: Ollama API (tool calling, memory context injection).
  - `stt.py`: Speech-to-text conversion.
  - `text.py`: Text chat interface (CLI).
  - `listener.py`: Voice detection and recording (CLI / local mic).
  - `tts.py`: Kokoro playback (CLI) and WAV synthesis (API).
  - `tools/`: Extensible tool system.
    - `registry.py`: Central registry for tool definitions and functions.
    - `example.py`: Sample tools (e.g., `get_current_time`).
- `.env`: Configuration for Ollama URL, model, and optional API host/port.
- `requirements.txt`: Python dependencies.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure your `.env` file (see `templates/.env-copy`):
   ```env
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama3
   ```
3. Run the **CLI** (local testing):
   ```bash
   python main.py
   ```
4. Run the **HTTP API** (remote clients, Tailscale, etc.):
   ```bash
   uvicorn app.server:app --host 0.0.0.0 --port 8765
   ```
   Or:
   ```bash
   python -m app.server
   ```
   Use `API_HOST` / `API_PORT` in `.env` when launching `python -m app.server`.

## HTTP API (backend)

- **Sessions** live in `sessions.sqlite` (or `SESSIONS_DB_PATH`). Each session holds the full Ollama message list (without the injected system row; that is rebuilt every turn from long-term memory, same as the CLI).
- **Long-term memory** (`memory.sqlite` via `app/core/memory.py`) is unchanged and shared with the CLI.
- **Tools, vision, STT, TTS** behave like the CLI: the model runs on the machine where the API runs.

Open **Swagger UI** at `http://<host>:8765/docs` on the machine running the server.

### Typical flow

1. `POST /sessions` → `{ "session_id": "..." }`
2. `POST /sessions/{session_id}/chat` with JSON `{ "message": "Hello" }` → `{ "reply": "...", "logs": [...] }`
3. Optional: `POST /warmup` with `{ "stt": true, "tts": true }` to preload heavy models after the server starts.
4. Optional: `POST /tts` with `{ "text": "..." }` → `audio/wav` for playback on a phone or browser.
5. Optional: `POST /sessions/{session_id}/voice/wav` with **raw WAV file bytes** as the request body (not multipart) → transcribes on the server, then runs the same chat pipeline; response includes `transcript`, `reply`, and `logs`.

### Tailscale

Install Tailscale on the PC that runs Ollama + this API. Start the API with `--host 0.0.0.0` so it listens on all interfaces. From another device on the same tailnet, use that machine’s **Tailscale IP** and port (for example `http://100.x.y.z:8765`). This project does not implement its own auth; your tailnet is the access boundary.

## CLI usage

Select **Voice** or **Text** mode at startup.

- In **Voice** mode, speak naturally. The assistant detects when you stop speaking and transcribes the audio.
- In **Text** mode, type your prompts directly.
- Say or type `exit` or `quit` to end the session.

## Adding tools

1. Create a function in a new file (e.g., `app/tools/weather.py`) or in `example.py`.
2. Use `registry.register()` to define the tool name, description, and JSON parameters.
3. Import your file in `app/tools/__init__.py`.

The AI will automatically see these tools and call them when needed.
