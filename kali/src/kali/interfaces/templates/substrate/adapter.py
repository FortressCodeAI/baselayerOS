import subprocess
import json

def call_substrate(payload):
    result = subprocess.run(
        ["baselayeros", "execute", json.dumps(payload)],
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)

def execute(payload):
    return call_substrate(payload)
