"""
Kali v1.0.0 — Neural Client (Real DeepSeek/Ollama Integration)

This client connects to a local Ollama server and runs:
- DeepSeek Coder
- DeepSeek R1
- Any GGUF model you have installed

It is fully sandboxed by Kali's neural layer.
"""

from __future__ import annotations
import requests
from typing import Optional


class NeuralClient:
    def __init__(self, model_name: str, host: str = "http://localhost:11434"):
        self.model_name = model_name
        self.host = host.rstrip("/")
        self.endpoint = f"{self.host}/api/generate"

    def generate(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """
        Call the underlying DeepSeek/Ollama model.

        This is the REAL implementation.
        """
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }

        try:
            response = requests.post(self.endpoint, json=payload, timeout=60)
            response.raise_for_status()
        except Exception as e:
            return (
                f"[NeuralClient Error] Could not reach Ollama at {self.endpoint}. "
                f"Reason: {e}. "
                "Ensure Ollama is running: `ollama serve`."
            )

        data = response.json()

        # Ollama returns {"response": "..."} for non-streaming mode
        output = data.get("response", "")

        if not output:
            return "[NeuralClient Warning] Model returned empty output."

        return output.strip()
