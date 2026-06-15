# UES Format Specification (v1.0.0)

The Unified Execution Specification (UES) is the core contract between:

- the user
- the councils
- the compiler
- the executor
- the audit chain

This document describes the UES structure used by BaseLayerOS v1.0.0.

## 1. Top-Level Structure

A UES proposal contains:

```json
{
  "ues_version": "1.0.0",
  "intent": {...},
  "audit": {...},
  "state": {...},
  "conditions": {...},
  "constraints": {...},
  "scores": {...},
  "capabilities": [...],
  "plan": {...}
}
```

Each section is deterministic and validated by the schema.

See: Schema Loader

## 2. Intent

Defines the purpose of the proposal.

```json
"intent": {
  "name": "my.intent"
}
```

This is used by councils and audit metadata.

## 3. Audit Block

Immutable metadata:

```json
"audit": {
  "proposal_id": "abc123",
  "created_by": "user",
  "created_at": "2025-01-01T00:00:00Z",
  "last_modified_by": "user",
  "last_modified_at": "2025-01-01T00:00:00Z"
}
```

The audit chain extends this block with event logs.

See: Audit Store

## 4. State

Lifecycle state:

`DRAFT → REVIEWED → OPTIMIZED → COMPILED → EXECUTED`

Example:

```json
"state": { "status": "DRAFT" }
```

See: State Machine

## 5. Conditions

Preconditions and postconditions:

```json
"conditions": {
  "pre": [],
  "post": []
}
```

Task-level postconditions are embedded in the plan.

## 6. Constraints

Enterprise constraints:

```json
"constraints": {
  "safety_level": "standard",
  "compliance_targets": []
}
```

Councils enforce these.

See: Council Router

## 7. Scores

Risk, cost, and time scores:

```json
"scores": {
  "cost": 0,
  "risk": 0,
  "time": 0
}
```

Used by optimization councils.

## 8. Capabilities

Capabilities required by the plan:

```json

"capabilities": [
  { "id": "builtin.echo" }
]
```

See: Capability Registry

## 9. Plan

The execution plan is a set of phases and tasks:

```json
"plan": {
  "phases": [
    {
      "id": "phase1",
      "name": "Example Phase",
      "tasks": [
        {
          "id": "task1",
          "capability": "builtin.echo",
          "inputs": {"x": 1},
          "outputs": {},
          "preconditions": [],
          "postconditions": []
        }
      ]
    }
  ]
}
```

The compiler converts this into deterministic DSL.

See: Compiler Codegen

## 10. Deterministic Guarantees

The UES format ensures:

- reproducible compilation
- deterministic execution
- strict validation
- auditability
- lifecycle enforcement

It is the backbone of BaseLayerOS.
