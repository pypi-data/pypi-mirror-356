import os
import requests
from typing import List, Dict

class GroqLLMClient:
    def __init__(self, api_key: str = None, model: str = "llama3-8b-8192"):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = model
        self.endpoint = "https://api.groq.com/openai/v1/chat/completions"

        if not self.api_key:
            raise ValueError("GROQ_API_KEY not set or provided.")

    def chat(self, messages: List[Dict[str, str]]) -> str:
        response = requests.post(
            self.endpoint,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": self.model,
                "messages": messages
            }
        )

        if response.status_code != 200:
            raise RuntimeError(f"Groq API error: {response.text}")

        return response.json()["choices"][0]["message"]["content"]
