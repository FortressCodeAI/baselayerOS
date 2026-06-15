# Getting Started with BaseLayerOS

This guide walks you through installing, running, and testing BaseLayerOS.
It is designed for developers integrating the deterministic substrate into
enterprise systems.

## 1. Requirements

- Python 3.11+
- pip or uv
- Git
- Linux or macOS recommended (Windows supported)

## 2. Installation

Clone the repository:

`git clone https://github.com/<your-org>/baselayeros.git`
`cd baselayeros`

Install Dependencies:

`pip install -r requirements.txt

or with uv:

`uv sync`

## 3. Running BaseLayerOS

BaseLayerOS includes a deterministic CLI:

`baselayeros run proposal.json`

This will:

1. Load the UES  
2. Run councils  
3. Compile  
4. Execute  
5. Emit audit events  
6. Print deterministic JSON output  

See: [CLI Entry](ca://s?q=Show_CLI_entry)

## 4. Running Tests

BaseLayerOS includes deterministic integration tests:

`pytest -q`

Key tests:

- `test_end_to_end.py` — full pipeline  
- `test_capabilities.py` — capability behavior  

See: [End-to-End Test](ca://s?q=Show_end_to_end_test)

## 5. Directory Structure

baselayeros/
app/
audit/
capabilities/
councils/
compiler/
orchestrator/
schema/
ues/
cli/
docs/
tests/

Each subsystem is deterministic and isolated.

See: [Architecture Overview](ca://s?q=Show_architecture)

## 6. Running an Example Proposal

Create `example.json`:

```json
{
  "ues_version": "1.0.0",
  "intent": {"name": "demo.intent"},
  "audit": {
    "proposal_id": "demo-001",
    "created_by": "demo",
    "created_at": "2025-01-01T00:00:00Z",
    "last_modified_by": "demo",
    "last_modified_at": "2025-01-01T00:00:00Z"
  },
  "state": {"status": "DRAFT"},
  "conditions": {"pre": [], "post": []},
  "constraints": {"safety_level": "standard", "compliance_targets": []},
  "scores": {"cost": 0, "risk": 0, "time": 0},
  "capabilities": [],
  "plan": {
    "phases": [
      {
        "id": "phase1",
        "name": "Demo Phase",
        "tasks": [
          {
            "id": "task1",
            "capability": "builtin.echo",
            "inputs": {"x": 42},
            "outputs": {},
            "preconditions": [],
            "postconditions": []
          }
        ]
      }
    ]
  }
}
```

Run:

`baselayeros run example.json`

You will get deterministic Output.

## 7. Next Steps

- Build your first capability
- Write your first UES
- Integrate BaseLayerOS into Regulus

See: Capabilities Guide
