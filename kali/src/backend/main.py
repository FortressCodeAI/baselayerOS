from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import importlib.util
import json

from kali.engine.engine import execute_action, execute_workflow

app = FastAPI(
    title="Kali Governed Execution Engine",
    version="1.0.0",
    description="Deterministic governed operator execution on BaseLayerOS substrate"
)


class ExecuteRequest(BaseModel):
    action: str
    data: dict | None = None
    token: str | None = None
    meta: dict | None = None


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("module", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module: {path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@app.post("/execute")
def execute(req: ExecuteRequest):
    payload = {
        "action": req.action,
        "data": req.data or {},
        "requested_capability": req.action,
        "deterministic": True,
        "replayable": True,
        "audit_chain_enabled": True,
        "governance_tier": "regulated",
        "capability_envelope": ["summarize_stream", "priority_collapse"],
        "token": req.token,
    }

    return execute_action(payload)


@app.post("/operator/{name}")
def run_operator(name: str):
    op_path = Path(f"operators/{name}.py")
    if not op_path.exists():
        raise HTTPException(status_code=404, detail="Operator not found")

    module = load_module(op_path)
    if not hasattr(module, "main"):
        raise HTTPException(status_code=400, detail="Operator missing main()")

    return module.main()


@app.post("/workflow/{name}")
def run_workflow(name: str):
    wf_path = Path(f"operators/{name}.py")
    if not wf_path.exists():
        raise HTTPException(status_code=404, detail="Workflow not found")

    module = load_module(wf_path)
    if not hasattr(module, "main"):
        raise HTTPException(status_code=400, detail="Workflow missing main()")

    return module.main()
