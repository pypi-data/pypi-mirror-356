import json
import os

SESSION_FILE = ".memochain_sessions.json"

def load_session_ids():
    if not os.path.exists(SESSION_FILE):
        print("No sessions found.")
        return []

    try:
        with open(SESSION_FILE, "r") as f:
            sessions = json.load(f)
            if not sessions:
                print("No sessions found.")
            else:
                print("Active sessions:")
                for s in sessions:
                    print("•", s)
            return sessions
    except json.JSONDecodeError:
        print("Corrupted session file.")
        return []

if __name__ == "__main__":
    load_session_ids()

