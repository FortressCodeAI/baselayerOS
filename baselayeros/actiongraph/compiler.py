from baselayeros.actiongraph.model import Node, Edge, ActionGraph

def compile_graph(spec: dict) -> ActionGraph:
    nodes = {}
    for node_def in spec["nodes"]:
        nodes[node_def["name"]] = Node(
            name=node_def["name"],
            handler=node_def["handler"],
            contract_clause=node_def.get("contract_clause", "")
        )

    edges = [Edge(e["from"], e["to"]) for e in spec["edges"]]
    return ActionGraph(nodes=nodes, edges=edges, entrypoint=spec["entrypoint"])
