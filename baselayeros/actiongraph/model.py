from typing import Callable, Dict, List, Any

class Node:
    def __init__(self, name: str, handler: Callable, contract_clause: str = ""):
        self.name = name
        self.handler = handler
        self.contract_clause = contract_clause
        self.refusal_reason = ""

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self.handler(payload)

class Edge:
    def __init__(self, from_node: str, to_node: str):
        self.from_node = from_node
        self.to_node = to_node

class ActionGraph:
    def __init__(self, nodes: Dict[str, Node], edges: List[Edge], entrypoint: str):
        self.nodes = nodes
        self.edges = edges
        self.entrypoint = entrypoint
