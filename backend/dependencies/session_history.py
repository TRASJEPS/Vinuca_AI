from collections import defaultdict

# Simple in-memory session store
# This is a placeholder for a more robust session management system
session_store = defaultdict(list)

def get_session_history(session_id: str):
    return session_store[session_id]

def append_to_session_history(session_id: str, history: list):
    session_store[session_id] = history
