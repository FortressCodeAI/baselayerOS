# demo/backend/verification.py 

REQUIRED_KEYS = ["meta", "io", "workflow", "governance"]

def verify_pack(pack: dict):
    # 1. Required top-level keys
    for key in REQUIRED_KEYS:
        if key not in pack:
            raise ValueError(f"Missing required section: {key}")

    # 2. Deterministic fields
    if "id" not in pack["meta"]:
        raise ValueError("Pack missing meta.id")

    # 3. Workflow structure
    wf = pack["workflow"]
    if "states" not in wf or "transitions" not in wf:
        raise ValueError("Workflow missing states or transitions")

    # 4. Hash consistency (demo only)
    # In real version: compute canonical JSON + sha256
    return True
