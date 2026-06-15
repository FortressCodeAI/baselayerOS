from baselayeros.regulus.models import WorkflowSpec
from baselayeros.actiongraph.compiler import compile_graph

class RegulusBuilder:
    def build_actiongraph(self, spec: WorkflowSpec):
        graph_spec = {
            "nodes": spec.nodes,
            "edges": spec.edges,
            "entrypoint": spec.entrypoint
        }
        return compile_graph(graph_spec)
