import subprocess
import sys

def execute_operator_script(execution):
    """Executes a Python operator script safely under runtime observation."""
    file_path = execution.arguments.get("file")
    if not file_path:
        raise ValueError("No file path provided in execution arguments.")
    
    result = subprocess.run(
        [sys.executable, file_path],
        capture_output=True,
        text=True
    )
    
    return {
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip()
    }

def fetch_public_data(execution):
    query = execution.arguments.get("query", "")
    return {
        "status": "success",
        "data": f"Retrieved public records for query: '{query}'"
    }

def execute_query(execution):
    query = execution.arguments.get("query", "")
    payload = execution.arguments.get("payload", "")
    return {
        "status": "executed",
        "query": query,
        "payload_evaluated": bool(payload)
    }

def transfer_funds(execution):
    recipient = execution.arguments.get("recipient", "unknown")
    amount = execution.arguments.get("amount", 0)
    return {
        "status": "transferred",
        "recipient": recipient,
        "amount": amount
    }

def drop_database(execution):
    target = execution.arguments.get("target", "unknown")
    return {
        "status": "dropped",
        "target": target
    }

def bypass_kernel(execution):
    target = execution.arguments.get("target", "unknown")
    return {
        "status": "bypassed",
        "target": target
    }

REGISTRY = {
    "execute_operator_script": execute_operator_script,
    "fetch_public_data": fetch_public_data,
    "execute_query": execute_query,
    "transfer_funds": transfer_funds,
    "drop_database": drop_database,
    "bypass_kernel": bypass_kernel,
}

def resolve(name: str):
    if name not in REGISTRY:
        return lambda exec_obj: {
            "status": "executed_fallback",
            "action": name,
            "arguments": getattr(exec_obj, "arguments", {})
        }
    return REGISTRY[name]