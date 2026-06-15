# Audit Chain Examples

This document provides real audit chain examples for enterprise auditors,
regulators, and compliance teams. These examples demonstrate how BaseLayerOS
records deterministic, immutable events throughout the pipeline.

See: [Audit Specification](ca://s?q=Show_audit_specification)

## 1. Example: Successful Execution

Below is a real audit chain for a simple UES proposal using `builtin.echo`.

### Event 1 — COUNCIL_REVIEW

```json
{
  "event_id": "evt-0001",
  "proposal_id": "test-proposal-123",
  "timestamp": "2025-01-01T00:00:01Z",
  "actor_id": "tester",
  "actor_org": "test-org",
  "actor_roles": ["developer"],
  "action": "COUNCIL_REVIEW",
  "details": {"passed": true},
  "previous_hash": "0"
}
```

### Event 2 - STATE_TRANSITION → REVIEWED

```json
{
  "event_id": "evt-0002",
  "proposal_id": "test-proposal-123",
  "timestamp": "2025-01-01T00:00:02Z",
  "actor_id": "tester",
  "actor_org": "test-org",
  "actor_roles": ["developer"],
  "action": "STATE_TRANSITION",
  "details": {"from": "DRAFT", "to": "REVIEWED"},
  "previous_hash": "hash(evt-0001)"
}
```

### Event 3 — COMPILE

```json
{
  "event_id": "evt-0003",
  "proposal_id": "test-proposal-123",
  "timestamp": "2025-01-01T00:00:03Z",
  "actor_id": "tester",
  "actor_org": "test-org",
  "actor_roles": ["developer"],
  "action": "COMPILE",
  "details": {"dsl_length": 128},
  "previous_hash": "hash(evt-0002)"
}
```

### Event 4 - STATE_TRANSITION -> COMPILED

```json
{
  "event_id": "evt-0004",
  "proposal_id": "test-proposal-123",
  "timestamp": "2025-01-01T00:00:04Z",
  "actor_id": "tester",
  "actor_org": "test-org",
  "actor_roles": ["developer"],
  "action": "STATE_TRANSITION",
  "details": {"from": "OPTIMIZED", "to": "COMPILED"},
  "previous_hash": "hash(evt-0003)"
}
```

### Event 5 - EXECUTE

```json
{
  "event_id": "evt-0005",
  "proposal_id": "test-proposal-123",
  "timestamp": "2025-01-01T00:00:05Z",
  "actor_id": "tester",
  "actor_org": "test-org",
  "actor_roles": ["developer"],
  "action": "EXECUTE",
  "details": {"task_outputs": {"task1": {"x": 1}}},
  "previous_hash": "hash(evt-0004)"
}
```

### Event 6 — STATE_TRANSITION → EXECUTED

```json
{
  "event_id": "evt-0006",
  "proposal_id": "test-proposal-123",
  "timestamp": "2025-01-01T00:00:06Z",
  "actor_id": "tester",
  "actor_org": "test-org",
  "actor_roles": ["developer"],
  "action": "STATE_TRANSITION",
  "details": {"from": "COMPILED", "to": "EXECUTED"},
  "previous_hash": "hash(evt-0005)"
}
```

## 2. Example: Failure During Execution

If a postcondition fails:

```json
{
  "event_id": "evt-0005",
  "proposal_id": "test-proposal-123",
  "timestamp": "2025-01-01T00:00:05Z",
  "actor_id": "tester",
  "actor_org": "test-org",
  "actor_roles": ["developer"],
  "action": "EXECUTE",
  "details": {
    "error": "Postcondition failed: equals(result.x, 2)"
  },
  "previous_hash": "hash(evt-0004)"
}
```

The pipeline halts immediately.

## 3. Deterministic Guarantees

Audit chains guarantee:

- immutability
- hash‑linked integrity
- deterministic ordering
- reproducible event structure
- regulator‑grade traceability

This is essential for enterprise governance.
