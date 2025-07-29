import json
import os
from typing import List, Dict

HISTORY_FILE = ".memochain_history.json"

def _load_raw_history() -> Dict[str, List[Dict[str, str]]]:
    if not os.path.exists(HISTORY_FILE):
        return {}
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def _save_raw_history(history: Dict[str, List[Dict[str, str]]]) -> None:
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def get_session_history(session_id: str) -> List[Dict[str, str]]:
    history = _load_raw_history()
    return history.get(session_id, [])

def append_to_history(session_id: str, role: str, content: str) -> None:
    if role not in {"user", "assistant"}:
        raise ValueError("Role must be 'user' or 'assistant'")
    
    history = _load_raw_history()
    session = history.get(session_id, [])
    session.append({"role": role, "content": content})
    history[session_id] = session
    _save_raw_history(history)

def clear_session_history(session_id: str) -> None:
    history = _load_raw_history()
    if session_id in history:
        del history[session_id]
        _save_raw_history(history)


def load_history(session_id: str) -> List[Dict[str, str]]:
    """Public API to load message history for a session."""
    return get_session_history(session_id)

def save_message(session_id: str, message: Dict[str, str]) -> None:
    """Public API to save a message to history."""
    append_to_history(session_id, message["role"], message["content"])

def load_context(session_id: str, max_turns: int = 8) -> List[Dict[str, str]]:
    history = get_session_history(session_id)
    return history[-max_turns:]


def clear_all_history():
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
