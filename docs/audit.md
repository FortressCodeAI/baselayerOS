# BaseLayerOS Audit Chain Specification

The BaseLayerOS audit chain is an immutable, append‑only event log that records
every action taken on a UES proposal. It provides full traceability,
reproducibility, and regulatory‑grade accountability.

---

## 1. Audit Chain Principles

The audit chain is designed around five guarantees:

1. **Immutability** — events cannot be modified or deleted.
2. **Determinism** — event structure and ordering are strictly defined.
3. **Integrity** — each event includes the hash of the previous event.
4. **Traceability** — every pipeline step is recorded.
5. **Reproducibility** — identical inputs produce identical audit chains.

See: [Audit Store](ca://s?q=Show_audit_store)

---

## 2. Event Structure

Each audit event has the following fields:

```json
{
  "event_id": "string",
  "proposal_id": "string",
  "timestamp": "ISO-8601 UTC",
  "actor_id": "string",
  "actor_org": "string",
  "actor_roles": ["string"],
  "action": "string",
  "details": {},
  "previous_hash": "string"
}
```

Required properties

- event_id — deterministic identifier for the event
- proposal_id — links event to a UES
- timestamp — UTC, ISO‑8601
- actor_id — who performed the action
- action — e.g., "COUNCIL_REVIEW", "COMPILE", "EXECUTE"
- previous_hash — ensures chain integrity

## 3. Hash Chaining

Each event includes the hash of the previous event:

`hash(event_n) → stored in event_(n+1).previous_hash`

This creates a tamper‑evident chain.

If any event is modified:

- all subsequent hashes break
- chain integrity fails
- the system raises an AuditError

## 4. Audit Events in the Pipeline

The orchestrator emits events at:

- council review
- state transitions
- compilation
- execution
- finalization

See: Orchestrator Engine

## 5. Deterministic Event Ordering

Events are always appended in the following order:

1. COUNCIL_REVIEW
2. STATE_TRANSITION → OPTIMIZED
3. COMPILE
4. STATE_TRANSITION → COMPILED
5. EXECUTE
6. STATE_TRANSITION → EXECUTED

This ordering is enforced by the orchestrator.

## 6. Failure Events

If a step fails:

- an audit event is still emitted
- details.error contains the deterministic error message
- the chain remains intact
- the pipeline halts

## 7. Future Extensions

Future versions may include:

- cryptographic signatures
- distributed audit replication
- tenant‑isolated audit chains
- audit export for regulators

All extensions must preserve determinism.
