# baselayeros/actiongraph/executor.py

"""
Deterministic action graph executor for BaseLayerOS.

This provides:
- Node: a deterministic unit of work
- Edge: a deterministic dependency
- GraphExecutor: executes nodes in topological order using ExecutionEngine
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List

from baselayeros.core.runtime.engine import ExecutionEngine
from kali.refusal import Refusal


# -----------------------------
# Node + Edge definitions
# -----------------------------

@dataclass
class Node:
    """
    A deterministic unit of work in the action graph.
    """
    id: str
    fn: Callable[[], Any]

    def run(self) -> Any:
        return self.fn()


@dataclass
class Edge:
    """
    A deterministic dependency: A -> B means B depends on A.
    """
    src: str
    dst: str


# -----------------------------
# Graph Executor
# -----------------------------

@dataclass
class GraphExecutor:
    """
    Deterministic executor for a directed acyclic graph (DAG) of nodes.
    """

    engine: ExecutionEngine
    nodes: Dict[str, Node] = field(default_factory=dict)
    edges: List[Edge] = field(default_factory=list)

    def add_node(self, node: Node) -> None:
        self.nodes[node.id] = node

    def add_edge(self, src: str, dst: str) -> None:
        self.edges.append(Edge(src, dst))

    # -----------------------------
    # Topological sort
    # -----------------------------
    def _topological_order(self) -> List[str]:
        incoming: Dict[str, int] = {nid: 0 for nid in self.nodes}

        for edge in self.edges:
            incoming[edge.dst] += 1

        queue = [nid for nid, count in incoming.items() if count == 0]
        order: List[str] = []

        while queue:
            nid = queue.pop(0)
            order.append(nid)

            for edge in self.edges:
                if edge.src == nid:
                    incoming[edge.dst] -= 1
                    if incoming[edge.dst] == 0:
                        queue.append(edge.dst)

        if len(order) != len(self.nodes):
            raise ValueError("Graph contains a cycle or unresolved dependency")

        return order

    # -----------------------------
    # Execution
    # -----------------------------
    def execute(self, actor: str, operation_prefix: str = "node") -> Dict[str, Any]:
        """
        Execute all nodes in deterministic topological order.
        Returns a dict of node_id -> result.
        """

        results: Dict[str, Any] = {}
        order = self._topological_order()

        for nid in order:
            node = self.nodes[nid]

            try:
                result = self.engine.run(
                    actor=actor,
                    operation=f"{operation_prefix}:{nid}",
                    fn=node.run,
                )

                if not result.success:
                    # Deterministic halt
                    return {
                        "success": False,
                        "failed_node": nid,
                        "error": result.error,
                        "results": results,
                    }

                results[nid] = result.value

            except Refusal as r:
                return {
                    "success": False,
                    "failed_node": nid,
                    "error": str(r),
                    "results": results,
                }

        return {
            "success": True,
            "results": results,
        }
