# baselayeros/connector/client.py
import httpx
from typing import Callable

class SubstrateClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self._client = httpx.Client(base_url=base_url, timeout=5.0)

    def execute(self, workflow_id: str, payload: dict) -> dict:
        r = self._client.post("/execute", json={"workflow_id": workflow_id, "payload": payload})
        r.raise_for_status()
        return r.json()

    def agent_step(self, agent_id: str) -> dict:
        r = self._client.post("/agent/step", json={"agent_id": agent_id})
        r.raise_for_status()
        return r.json()

    def get_graph_state(self) -> dict:
        r = self._client.get("/graph/state")
        r.raise_for_status()
        return r.json()

    def get_agents(self) -> dict:
        r = self._client.get("/agents")
        r.raise_for_status()
        return r.json()
