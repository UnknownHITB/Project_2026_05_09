"""
HTTP API for the assistant: server-side sessions, same Ollama + tools + memory as the CLI.

Run (from project root):
  uvicorn app.server:app --host 0.0.0.0 --port 8765

Bind to ``0.0.0.0`` so Tailscale IPs on this machine can reach the service.
"""

from __future__ import annotations

import asyncio
import os
import tempfile
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        import torch

        if torch.cuda.is_available():
            torch.cuda.init()
    except Exception:
        pass
    yield


app = FastAPI(title="AI Chat Assistant", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


_cached_provider = None


def _provider():
    global _cached_provider
    if _cached_provider is None:
        from app.providers.ollama_provider import OllamaProvider

        _cached_provider = OllamaProvider()
    return _cached_provider


def _session_store():
    from app.core.sessions import store

    return store


class ChatBody(BaseModel):
    message: str = Field(..., min_length=1, description="User message for this turn.")


class TtsBody(BaseModel):
    text: str = Field(..., min_length=1, description="Text to synthesize to WAV.")


class WarmupBody(BaseModel):
    stt: bool = False
    tts: bool = False


@app.get("/")
def root() -> Dict[str, Any]:
    return {
        "service": "ai-chat-assistant",
        "docs": "/docs",
        "health": "/health",
        "sessions": "POST /sessions, GET /sessions, GET /sessions/{id}",
        "chat": "POST /sessions/{id}/chat",
        "voice": "POST /sessions/{id}/voice/wav (raw WAV bytes)",
        "tts": "POST /tts (JSON {text}) -> audio/wav",
        "warmup": "POST /warmup (optional STT/TTS model load)",
    }


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/sessions")
def create_session() -> Dict[str, str]:
    sid = _session_store().create_session()
    return {"session_id": sid}


@app.get("/sessions")
def list_sessions(limit: int = 50) -> Dict[str, List[Dict[str, Any]]]:
    return {"sessions": _session_store().list_sessions(limit=limit)}


@app.get("/sessions/{session_id}")
def session_meta(session_id: str) -> Dict[str, Any]:
    meta = _session_store().get_meta(session_id)
    if not meta:
        raise HTTPException(status_code=404, detail="Unknown session")
    return meta


@app.get("/sessions/{session_id}/messages")
def session_messages(session_id: str) -> Dict[str, Any]:
    store = _session_store()
    msgs = store.get_messages(session_id)
    if msgs is None:
        raise HTTPException(status_code=404, detail="Unknown session")
    return {"session_id": session_id, "messages": msgs}


@app.delete("/sessions/{session_id}")
def delete_session(session_id: str) -> Dict[str, Any]:
    ok = _session_store().delete_session(session_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Unknown session")
    return {"deleted": True, "session_id": session_id}


@app.post("/sessions/{session_id}/chat")
def session_chat(session_id: str, body: ChatBody) -> Dict[str, Any]:
    store = _session_store()
    if store.get_meta(session_id) is None:
        raise HTTPException(status_code=404, detail="Unknown session")
    text = body.message.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Empty message")
    logs: List[str] = []

    def on_log(line: str) -> None:
        logs.append(line)

    try:
        reply = store.chat_append_user(session_id, text, _provider(), on_log=on_log)
    except KeyError:
        raise HTTPException(status_code=404, detail="Unknown session")
    return {"reply": reply, "logs": logs}


@app.post("/sessions/{session_id}/voice/wav")
async def session_voice_wav(session_id: str, request: Request) -> JSONResponse:
    store = _session_store()
    if store.get_meta(session_id) is None:
        raise HTTPException(status_code=404, detail="Unknown session")
    data = await request.body()
    max_bytes = int(os.getenv("VOICE_MAX_BYTES", str(25 * 1024 * 1024)))
    if len(data) > max_bytes:
        raise HTTPException(status_code=413, detail="WAV payload too large")

    loop = asyncio.get_running_loop()

    def work() -> Dict[str, Any]:
        import os as _os

        from app.core.stt import transcribe_wav

        fd, path = tempfile.mkstemp(suffix=".wav")
        try:
            with _os.fdopen(fd, "wb") as f:
                f.write(data)
            transcript = transcribe_wav(path)
            if transcript.startswith("Error:"):
                return {"transcript": None, "reply": None, "logs": [], "error": transcript}
            t = transcript.strip()
            if not t:
                return {
                    "transcript": transcript,
                    "reply": None,
                    "logs": [],
                    "error": "Empty transcription",
                }
            logs: List[str] = []

            def on_log(line: str) -> None:
                logs.append(line)

            reply = store.chat_append_user(session_id, t, _provider(), on_log=on_log)
            return {"transcript": t, "reply": reply, "logs": logs, "error": None}
        finally:
            try:
                _os.unlink(path)
            except OSError:
                pass

    result = await loop.run_in_executor(None, work)
    return JSONResponse(result)


@app.post("/tts")
def tts_wav(body: TtsBody) -> Response:
    from app.core.tts import synthesize_speech_wav

    wav = synthesize_speech_wav(body.text.strip())
    if not wav:
        raise HTTPException(status_code=400, detail="TTS unavailable or empty audio")
    return Response(content=wav, media_type="audio/wav")


@app.post("/warmup")
def warmup(body: WarmupBody) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    if body.stt:
        from app.core.stt import get_model

        get_model()
        out["stt"] = "ready"
    if body.tts:
        from app.core.tts import KokoroTTS

        KokoroTTS()
        out["tts"] = "ready"
    if not out:
        out["hint"] = "Set stt and/or tts true to preload models"
    return out


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8765"))
    uvicorn.run("app.server:app", host=host, port=port, reload=False)
