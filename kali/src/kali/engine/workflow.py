from .loader import load_operator


def load_workflow(path: str):
    module = load_operator(path)
    if not hasattr(module, "workflow"):
        raise RuntimeError("Workflow must define workflow()")
    return module.workflow
