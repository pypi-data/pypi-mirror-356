from typing import List, Dict
from memochain.memory_store import get_session_history, append_to_history

class MemoChainSession:
    def __init__(self, session_id: str, context_window: int = 8):
        self.session_id = session_id
        self.context_window = context_window

    def get_context(self) -> List[Dict[str, str]]:
        """
        Returns the last N messages for context injection.
        """
        full_history = get_session_history(self.session_id)
        return full_history[-self.context_window:]

    def add_user_message(self, message: str) -> None:
        append_to_history(self.session_id, "user", message)

    def add_assistant_message(self, message: str) -> None:
        append_to_history(self.session_id, "assistant", message)

    def update_context_window(self, new_window_size: int) -> None:
        self.context_window = new_window_size
