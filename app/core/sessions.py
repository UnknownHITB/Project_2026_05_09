"""
Server-side chat sessions: message history stored in SQLite (separate from episodic memory).

Persisted messages exclude the injected system prompt; OllamaProvider re-injects it each turn.
"""

from __future__ import annotations

import json
import os
import sqlite3
import threading
import uuid
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

from app.providers.ollama_provider import OllamaProvider


def _strip_leading_system(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if messages and messages[0].get("role") == "system":
        return messages[1:]
    return list(messages)


def _default_db_path() -> str:
    return os.getenv("SESSIONS_DB_PATH", "sessions.sqlite")


class SessionStore:
    """Thread-safe persistence for per-session Ollama message lists."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or _default_db_path()
        self._meta_lock = threading.Lock()
        self._session_locks: Dict[str, threading.Lock] = {}
        self._init_db()

    def _session_lock(self, session_id: str) -> threading.Lock:
        with self._meta_lock:
            if session_id not in self._session_locks:
                self._session_locks[session_id] = threading.Lock()
            return self._session_locks[session_id]

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    messages_json TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def create_session(self) -> str:
        sid = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()
        with sqlite3.connect(self.db_path, timeout=60) as conn:
            conn.execute(
                "INSERT INTO sessions (id, messages_json, updated_at) VALUES (?, ?, ?)",
                (sid, "[]", now),
            )
            conn.commit()
        return sid

    def delete_session(self, session_id: str) -> bool:
        with self._session_lock(session_id):
            with sqlite3.connect(self.db_path, timeout=60) as conn:
                cur = conn.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
                conn.commit()
                deleted = cur.rowcount > 0
        if deleted:
            with self._meta_lock:
                self._session_locks.pop(session_id, None)
        return deleted

    def list_sessions(self, limit: int = 50) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path, timeout=60) as conn:
            cur = conn.execute(
                "SELECT id, updated_at FROM sessions ORDER BY updated_at DESC LIMIT ?",
                (limit,),
            )
            rows = cur.fetchall()
        return [{"id": r[0], "updated_at": r[1]} for r in rows]

    def get_meta(self, session_id: str) -> Optional[Dict[str, Any]]:
        with sqlite3.connect(self.db_path, timeout=60) as conn:
            cur = conn.execute(
                "SELECT id, messages_json, updated_at FROM sessions WHERE id = ?",
                (session_id,),
            )
            row = cur.fetchone()
        if not row:
            return None
        msgs = json.loads(row[1])
        return {
            "id": row[0],
            "updated_at": row[2],
            "message_count": len(msgs),
        }

    def get_messages(self, session_id: str) -> Optional[List[Dict[str, Any]]]:
        with sqlite3.connect(self.db_path, timeout=60) as conn:
            cur = conn.execute(
                "SELECT messages_json FROM sessions WHERE id = ?", (session_id,)
            )
            row = cur.fetchone()
        if not row:
            return None
        return json.loads(row[0])

    def _save_messages(self, conn: sqlite3.Connection, session_id: str, messages: List[Dict[str, Any]]) -> None:
        now = datetime.now(timezone.utc).isoformat()
        conn.execute(
            "UPDATE sessions SET messages_json = ?, updated_at = ? WHERE id = ?",
            (json.dumps(messages), now, session_id),
        )

    def chat_append_user(
        self,
        session_id: str,
        user_text: str,
        provider: OllamaProvider,
        on_log: Optional[Callable[[str], None]] = None,
    ) -> str:
        """
        Append a user message, run Ollama (tools included), persist history without the system row.

        Returns the assistant text reply (same contract as OllamaProvider.chat).
        """
        with self._session_lock(session_id):
            with sqlite3.connect(self.db_path, timeout=120) as conn:
                cur = conn.execute(
                    "SELECT messages_json FROM sessions WHERE id = ?", (session_id,)
                )
                row = cur.fetchone()
                if not row:
                    raise KeyError(session_id)
                messages: List[Dict[str, Any]] = json.loads(row[0])
                messages.append({"role": "user", "content": user_text})
                reply = provider.chat(messages, on_log=on_log)
                to_store = _strip_leading_system(messages)
                self._save_messages(conn, session_id, to_store)
                conn.commit()
                return reply


store = SessionStore()
