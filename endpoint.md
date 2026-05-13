# HTTP API reference

Base URL: whatever host and port you run Uvicorn on (for example `http://127.0.0.1:8765` locally, or `http://100.x.y.z:8765` over Tailscale).

All JSON responses use UTF-8. Unless noted, responses are JSON with `Content-Type: application/json`.

Interactive OpenAPI UI: **`GET /docs`** (Swagger) and **`GET /redoc`**.

---

## Conventions

- **Session ID** (`session_id`): UUID string returned by `POST /sessions`. Use it in paths; URL-encode it if you embed it in a client that might add special characters (plain UUIDs are safe as-is).
- **Errors**: Failed requests return JSON like `{"detail": "..."}` or `{"detail": [...]}` (FastAPI). Status codes are listed per route below.
- **CORS**: The server allows all origins (`*`), methods, and headers—fine for personal / Tailscale use; tighten in code if you expose it publicly.
- **Long-term memory** (`memory.sqlite`) and **tool execution** run on the **machine hosting this API**, same as the CLI.

---

## Typical app flow

1. `POST /sessions` → save `session_id`.
2. For each user turn: `POST /sessions/{session_id}/chat` with `{ "message": "..." }` → show `reply`; optionally show `logs` (tool / vision lines).
3. Optional: `POST /warmup` once after startup to load STT/TTS models before first voice or TTS call.
4. Optional: `POST /tts` to play assistant text as WAV on the client.
5. Optional: `POST /sessions/{session_id}/voice/wav` with raw WAV bytes after recording on the client.

---

## `GET /`

**Summary:** Short index of main routes (human-readable, not exhaustive).

**Response:** `200` — JSON object with keys like `service`, `docs`, `health`, etc.

---

## `GET /health`

**Summary:** Liveness check.

**Response:** `200`

```json
{ "status": "ok" }
```

---

## `POST /sessions`

**Summary:** Create a new chat session (empty history on the server).

**Body:** none.

**Response:** `200`

```json
{ "session_id": "<uuid>" }
```

**Storage:** History is persisted under `sessions.sqlite` (or `SESSIONS_DB_PATH` in `.env`). The stored list omits the injected system prompt; it is rebuilt each turn from memory + rules, same as the CLI.

---

## `GET /sessions`

**Summary:** List recent sessions (metadata only).

**Query parameters:**

| Name    | Type   | Default | Description        |
|---------|--------|---------|--------------------|
| `limit` | int    | `50`    | Max rows to return |

**Response:** `200`

```json
{
  "sessions": [
    { "id": "<uuid>", "updated_at": "<ISO-8601 UTC>" }
  ]
}
```

---

## `GET /sessions/{session_id}`

**Summary:** Session metadata (not full message list).

**Response:** `200`

```json
{
  "id": "<uuid>",
  "updated_at": "<ISO-8601 UTC>",
  "message_count": 0
}
```

**Errors:** `404` if `session_id` is unknown.

---

## `GET /sessions/{session_id}/messages`

**Summary:** Full Ollama-style message list for this session (as stored after each turn—no leading system message).

**Response:** `200`

```json
{
  "session_id": "<uuid>",
  "messages": [ /* array of { role, content, ... } objects */ ]
}
```

**Errors:** `404` if unknown session.

**Note:** Shapes match Ollama chat messages (including `tool` role and optional `tool_calls` / `images` on entries when the model used them).

---

## `DELETE /sessions/{session_id}`

**Summary:** Delete session row and history.

**Response:** `200`

```json
{ "deleted": true, "session_id": "<uuid>" }
```

**Errors:** `404` if unknown.

---

## `POST /sessions/{session_id}/chat`

**Summary:** Append one user message, run the model (tools + memory), persist history, return assistant text.

**Headers:** `Content-Type: application/json`

**Body:**

```json
{
  "message": "User text for this turn (required, min length 1 before trim)"
}
```

After trim, empty `message` → **`400`** `{"detail":"Empty message"}`.

**Response:** `200`

```json
{
  "reply": "Assistant plain text (markdown chars * and # stripped for TTS compatibility).",
  "logs": [
    "[Tools] Model requested 1 tool(s)...",
    "[Tools] Executing: get_current_time({})"
  ]
}
```

`logs` may be an empty array if nothing was logged that turn.

**Errors:**

- `404` — unknown `session_id`
- `400` — empty message after trim
- `422` — invalid JSON or validation (e.g. missing `message`)

---

## `POST /sessions/{session_id}/voice/wav`

**Summary:** Send **raw WAV file bytes** as the entire request body (not `multipart/form-data`). Server writes a temp file, runs STT, then runs the same pipeline as `.../chat` with the transcribed text.

**Headers:** `Content-Type: audio/wav` or `application/octet-stream` (body is still raw bytes; type is mainly for clarity).

**Body:** Raw WAV bytes.

**Size limit:** Default **25 MiB**; override with env `VOICE_MAX_BYTES` (integer, bytes).

**Response:** `200` — JSON (always JSON, even on STT failure):

**Success (transcription OK and chat ran):**

```json
{
  "transcript": "<string>",
  "reply": "<assistant string>",
  "logs": [ "..." ],
  "error": null
}
```

**STT or empty transcript failure:**

```json
{
  "transcript": null,
  "reply": null,
  "logs": [],
  "error": "Error: ..." 
}
```

or

```json
{
  "transcript": "",
  "reply": null,
  "logs": [],
  "error": "Empty transcription"
}
```

**Errors:**

- `404` — unknown session
- `413` — body larger than `VOICE_MAX_BYTES`

**Client tip:** Mono **16 kHz** PCM WAV matches the CLI listener profile and usually works well with faster-whisper.

---

## `POST /tts`

**Summary:** Synthesize text to a single **WAV** (PCM) on the server (Kokoro); no session required.

**Headers:** `Content-Type: application/json`

**Body:**

```json
{ "text": "String to speak (required, min length 1 before trim)" }
```

**Response:** `200` — binary WAV

- Header: `Content-Type: audio/wav`
- Body: WAV bytes (play or save on the client)

**Errors:**

- `400` — TTS failed or produced empty audio
- `422` — validation error

---

## `POST /warmup`

**Summary:** Optionally preload heavy models (Whisper STT, Kokoro TTS) so the first real request is faster.

**Headers:** `Content-Type: application/json`

**Body:**

```json
{
  "stt": true,
  "tts": true
}
```

Both fields default to `false` if omitted.

**Response:** `200` — examples:

```json
{ "stt": "ready" }
```

```json
{ "tts": "ready" }
```

```json
{ "stt": "ready", "tts": "ready" }
```

If both flags are false:

```json
{ "hint": "Set stt and/or tts true to preload models" }
```

---

## Environment variables (API-related)

| Variable           | Effect |
|--------------------|--------|
| `API_HOST`         | Default bind host when running `python -m app.server` (default `0.0.0.0`). |
| `API_PORT`         | Default port (default `8765`). |
| `SESSIONS_DB_PATH` | SQLite file for session history (default `sessions.sqlite`). |
| `VOICE_MAX_BYTES`  | Max body size for `POST .../voice/wav` (default `26214400`). |
| `OLLAMA_BASE_URL`  | Ollama server (default `http://localhost:11434`). |
| `OLLAMA_MODEL`     | Chat model name. |

---

## Quick `curl` examples

Replace `BASE` and `SID`.

```bash
# Health
curl -s BASE/health

# New session
curl -s -X POST BASE/sessions

# Chat
curl -s -X POST BASE/sessions/SID/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\":\"Hello\"}"

# Voice (raw WAV file)
curl -s -X POST BASE/sessions/SID/voice/wav \
  -H "Content-Type: audio/wav" \
  --data-binary @recording.wav

# TTS to file (JSON field is `text`, not `message`)
curl -s -X POST BASE/tts \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Hello from the API.\"}" \
  -o out.wav

# Warmup
curl -s -X POST BASE/warmup \
  -H "Content-Type: application/json" \
  -d "{\"stt\":true,\"tts\":true}"
```

---

## Local HTML tester

See **`chat_test.html`** in the project root for a ready-made UI (health, session, chat, WAV upload, TTS, warmup).


uvicorn app.server:app --host 0.0.0.0 --port 8765
