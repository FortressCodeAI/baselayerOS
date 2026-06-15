# BaseLayerOS Example UES Proposals

This document provides real, deterministic examples of UES proposals that
developers can use to learn the system.

## 1. Minimal Example

A minimal UES that uses `builtin.echo`:

```json
{
  "ues_version": "1.0.0",
  "intent": {"name": "example.minimal"},
  "audit": {
    "proposal_id": "ex-min-001",
    "created_by": "dev",
    "created_at": "2025-01-01T00:00:00Z",
    "last_modified_by": "dev",
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
        "name": "Echo Phase",
        "tasks": [
          {
            "id": "task1",
            "capability": "builtin.echo",
            "inputs": {"message": "hello world"},
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

See: `UES Format`

## 2. Example with Preconditions and Postconditions

```json
{
  "ues_version": "1.0.0",
  "intent": {"name": "example.validation"},
  "audit": {
    "proposal_id": "ex-val-001",
    "created_by": "dev",
    "created_at": "2025-01-01T00:00:00Z",
    "last_modified_by": "dev",
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
        "name": "Validation Phase",
        "tasks": [
          {
            "id": "task1",
            "capability": "builtin.echo",
            "inputs": {"x": 5},
            "outputs": {},
            "preconditions": [
              {"equals": ["x", 5]}
            ],
            "postconditions": [
              {"equals": ["result.x", 5]}
            ]
          }
        ]
      }
    ]
  }
}
```

See: Executor Spec

## 3. Multi‑Phase Example

```json
{
  "ues_version": "1.0.0",
  "intent": {"name": "example.multi_phase"},
  "audit": {
    "proposal_id": "ex-mp-001",
    "created_by": "dev",
    "created_at": "2025-01-01T00:00:00Z",
    "last_modified_by": "dev",
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
        "name": "Phase One",
        "tasks": [
          {
            "id": "task1",
            "capability": "builtin.echo",
            "inputs": {"value": 1},
            "outputs": {},
            "preconditions": [],
            "postconditions": []
          }
        ]
      },
      {
        "id": "phase2",
        "name": "Phase Two",
        "tasks": [
          {
            "id": "task2",
            "capability": "builtin.echo",
            "inputs": {"value": 2},
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

See: Compiler Guide

## 4. Next Steps

- Build your own capability
- Write a multi‑phase UES
- Integrate BaseLayerOS into Regulus

See: Getting Started
