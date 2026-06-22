from typing import Any

class MemoryAgent:
    """Memory Agent manages conversation history and context."""

    def __init__(self, max_messages_per_session: int = 20) -> None:
        self.max_messages_per_session = max_messages_per_session
        self._sessions: dict[str, list[dict[str, str]]] = {}

    async def load_context(self, session_id: str | None = None) -> dict[str, Any]:
        key = session_id or "default-session"
        return {"session_id": key, "history": list(self._sessions.get(key, []))}

    async def save_context(self, session_id: str | None, user_query: str, assistant_answer: str) -> None:
        key = session_id or "default-session"
        history = self._sessions.setdefault(key, [])
        history.extend(
            [
                {"role": "user", "content": user_query},
                {"role": "assistant", "content": assistant_answer},
            ]
        )
        del history[:-self.max_messages_per_session]
        return None
