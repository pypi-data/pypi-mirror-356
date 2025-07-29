# MemoChain

**MemoChain** is a lightweight Python library for adding memory to stateless LLM APIs. It allows developers to easily store and retrieve conversation history across sessions with minimal setup.

Key features:
- Supports any LLM API (OpenAI, DeepSeek, Claude, Mistral, etc.)
- Built-in Groq integration
- Local JSON-based storage (no external DB or backend)
- Session-based memory tracking
- Clean, modular design for easy use in any project

---

## Installation

```bash
pip install memochain
```

---

## Quickstart

### Use with your own LLM (e.g. OpenAI)

```python
from memochain.memory_store import load_context, append_to_history
import openai

openai.api_key = "your-openai-api-key"
session_id = "demo-session"

append_to_history(session_id, "user", "Tell me a joke.")
history = load_context(session_id)

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=history
)

assistant_msg = response["choices"][0]["message"]["content"]
append_to_history(session_id, "assistant", assistant_msg)

print("Assistant:", assistant_msg)
```

---

### Use with built-in Groq support

```python
from memochain.groq_client import GroqLLMClient
from memochain.memory_store import append_to_history, get_session_history

session_id = "groq-session"
client = GroqLLMClient()

append_to_history(session_id, "user", "Who won the World Cup in 2022?")
history = get_session_history(session_id)
response = client.chat(history)

append_to_history(session_id, "assistant", response)
print("Assistant:", response)
```

---

## How It Works

MemoChain stores all message history locally in:
- `.memochain_history.json` — stores conversation history per session
- `.memochain_sessions.json` — tracks active session IDs

This allows memory persistence across runs without a backend or database.

---

## Example Scripts

See the `examples/` folder:
- `custom_llm_openai_example.py` — OpenAI API usage
- `groq_chat_example.py` — Chat example using Groq integration

To test locally:

```bash
python examples/groq_chat_example.py
```

---

## License

MIT

---

## Author

Yash Thapliyal – [GitHub](https://github.com/yashdt)
