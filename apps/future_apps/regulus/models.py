from typing import List, Dict, Any

class WorkflowSpec:
    def __init__(self, name: str, nodes: List[Dict[str, Any]], edges: List[Dict[str, str]], entrypoint: str):
        self.name = name
        self.nodes = nodes
        self.edges = edges
        self.entrypoint = entrypoint
