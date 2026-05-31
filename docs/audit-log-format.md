# Audit Log Format Specification

The BaseLayerOS audit log is an append‑only, hash‑linked event stream that
records all relevant actions taken by workflows, modules, and the runtime.

This document defines:

- the audit event structure
- hashing and linkage rules
- integrity guarantees
- expected behavior of conformant implementations

The goal is to provide an **audit‑grade**, regulator‑ready log that can be
cross‑referenced with replay traces and compliance evidence.

## 1. Audit Log Overview

An audit log is a sequence of events written to an append‑only medium,
such as:

- a JSONL file
- an append‑only database table
- a write‑once storage system

Each event:

- is immutable once written
- is hash‑linked to the previous event
- can be validated independently

## 2. Event Structure

Each audit event has the following fields:

```json
{
  "event_id": "string",
  "timestamp": "2026-05-16T12:34:56Z",
  "actor": {
    "type": "workflow | module | system | user",
    "id": "string"
  },
  "context": {
    "workflow_id": "string",
    "workflow_version": "string",
    "trace_id": "string",
    "step_id": "string | null"
  },
  "event_type": "string",
  "payload": { },
  "prev_hash": "string | null",
  "event_hash": "string"
}

### 2.1 `event_id`

- A unique identifier for the event.
- May be a UUID or another unique scheme.

### 2.2 `timestamp`

- ISO 8601 timestamp.
- Represents when the event was recorded.

### 2.3 `actor`

- Identifies who or what caused the event.
- 'type' may include:
    - `workflow` - the workflow engine
    - `module` - a specific module
    - `system` - the runtime itself
    - `user` - a human operator

### 2.4 `context`

- Links the event to:
    - a workflow
    - a workflow version
    - a replay trace
    - a specific step (if applicable)

### 2.5 `event_type`

- A short, machine-readable string, e.g.:
    - `workflow.started`
    - `workflow.completed`
    - `step.started`
    - `step.completed`
    - `module_invoked`
    - `compliance.violation`
    - `approval.granted`
    - `approval.denied`

### 2.6 `payload`

- Structured, event-specific data.
- Must be JSON-serializable.

### 2.7 `prev_hash`

- The `event_hash` of the previous event in the log.
- `null` for the first event.

### 2.8 `event_hash`

- The SHA-256 hash of the event, computed over:
    - all fields except `event_hash` itself
    - using canonical JSON serialization.

## 3. Hash Linking

The audit log forms a hash chain:

- event[0].prev_hash = null
- event[0].event_hash = H(event[0])
- event[1].prev_hash = event[0].event_hash
- event[1].event_hash = H(event[1])
- ...

This provides:

- tamper-evidence
- integrity verification
- a cryptographic anchor for the entire log

## 4. Integrity Verification

A conformant implementation must support:

### A. Reading the audit log sequentially.

### B. Recomputing `event_hash` for each event.

### C. Validating that:
    
    - `event[i].prev_hash == event[i-1].event_hash`
    - `event[i].event_hash == H(event[i] without event_hash`)

If any mismatch is detected, the log must be considered compromised.

## 5. Relationship to Replay Traces

Audit events and replay traces are complementary:

- replay traces capture workflow execution
- audit logs capture system-wide events

The `context.trace_id` field allows:

- cross-referencing audit events with replay traces
- reconstructing a complete picture of a decision.

## 6. Compliance and Governance

Compliance packs may:

- require specific audit events
- enforce logging of certain actions
- validate the presence and integrity of audit logs

The public standard defines the event format and hash rules, not the
enforcement logic.

## 7. Schema

The machine‑readable JSON Schema for audit events is defined in:

`standard/schemas/audit-event.schema.json`
