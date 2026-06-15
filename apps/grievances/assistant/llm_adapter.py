from __future__ import annotations
from typing import Dict, Any, Protocol


class LLMClient(Protocol):
    def generate(self, prompt: str) -> str:  # pragma: no cover - interface
        ...


class LocalEchoLLM:
    def generate(self, prompt: str) -> str:
        return f"[LLM ECHO] {prompt[:400]}"


class LLMAdapter:
    def __init__(self, client: LLMClient | None = None) -> None:
        self._client = client or LocalEchoLLM()

    def summarize_grievance(self, grievance: Dict[str, Any]) -> str:
        prompt = (
            "Summarize this grievance in one sentence for a union rep:\n\n"
            f"Member: {grievance.get('member_name')} (ID: {grievance.get('member_id')})\n"
            f"Employer: {grievance.get('employer')}\n"
            f"Issue: {grievance.get('issue_summary')}\n"
            f"Requested remedy: {grievance.get('requested_remedy')}\n"
        )
        return self._client.generate(prompt)
