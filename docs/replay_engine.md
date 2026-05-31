# Replay Engine Specification

The replay engine is responsible for:

- reconstructing workflow executions from trace files
- re‑executing workflows deterministically
- validating that outputs and hashes match
- supporting audit, compliance, and investigation workflows

This document defines the replay trace format and the expected behavior
of a conformant replay engine.

## 1. Replay Trace Overview

A replay trace is a JSON document that captures:

- workflow metadata
- input payload
- environment configuration
- version information
- step‑by‑step execution records
- outputs
- hashes

The trace must contain enough information to:

- re‑run the workflow
- reproduce all decisions
- validate integrity

## 2. Top‑Level Structure

A replay trace has the following top‑level fields:

```json
{
  "trace_id": "string",
  "workflow_id": "string",
  "workflow_version": "string",
  "created_at": "2026-05-16T12:34:56Z",
  "input": { },
  "environment": { },
  "versions": {
    "modules": { },
    "models": { },
    "datasets": { }
  },
  "steps": [ ],
  "output": { },
  "hashes": {
    "input_hash": "string",
    "output_hash": "string",
    "trace_hash": "string"
  }
}

## 3. Input and Environtment

### 3.1 Input

- The original input payload to the workflow.
- Must be serializable to JSON.
- Must be hashed using the canonical hashing rules.

### 3.2 Environment

- Configuration that affects execution, such as:
    - Region
    - feature flags
    - runtime parameters
- Must be recorded to ensure replay fidelity.

## 4. Version Information

The versions object contains:

```Json
"versions": {
  "modules": {
    "module_id": "version"
  },
  "models": {
    "model_id": "version"
  },
  "datasets": {
    "dataset_id": "version"
  }
}

- All referenced modules, models and datasets must be pinned.
- The replay engine must ensure that the same versions are used during replay.

## 5. Step Records

The steps array contains ordered records:

``` Json
{
    "step_id": "string",
    "name": "string",
    "started_at": "2026-05-16T12:34:56Z",
    "ended_at": "2026-05-16T12:34:57Z",
    "input_state": { },
    "output_state": { },
    "modules_called": [ ],
    "external_calls": [ ],
    "status": "SUCCESS | FAILURE",
    "error": null
}

### 5.1 `input_state` and `output_state`

- Represent the workflow state before and after the step.
- Must be sufficient to reconstruct state transitions.

### 5.2 modules_called

- List of module invocations, including:

    - module id
    - version
    - inputs
    - outputs

### 5.3 external_calls

- Any mediated external service calls, including:
    - request
    - response
    - identifiers

### 5.4 status and error

- status indicates success or failure.
- error contains structured error information when applicable.

## 6. Hashes

The hashes object contains:

- `input_hash` - hash of the input object
- `output_hash` - hash of the output object
- `trace_hash` - hash of the entire trace (excluding trace_hash itself)

All hashes must:

- use canonical JSON serialization
- use SHA-256
- be reproducible

## 7. Replay Engine Behaviour

A conformant replay engine must:

### 1. Load a trace file.

### 2. Validate the trace structure against the schema.

### 3. Validate hashes:    
    - recompute `input_hash`,`output_hash` and `trace_hash`
    - compare with stored values.

### 4. Reconstruct the workflow:
    - use `workflow_id` and `workflow_version`
    - use pinned versions from `versions`.

### 5. Re-execute steps:
    - using `input`, `environment` and versioned dependencies.

### 6. Compare:
    - re-computed outputs with `output`
    - re-computed hashes with stored hashes.

If any mismatch occurs, the replay engine must:
- mark the replay as non-conformant
- produce a structured report indicating:
    - where the mismatch occurred
    - expected vs actual values

## 8. Integration with Audit and Compliance

The replay engine is designed to work with:

- audit logs (for cross-referencing events)
- compliance packs (for validatings invariants)
- provenance and lifecycle systems (in enterprise deployments)

The public standard defines only the trace format and replay behaviour,
not the enforcement logic.

## 9. Schema

The machine-readable JSON schema for replay traces is defined in:

- `standard/schemas/replay-trace.schema.json`
