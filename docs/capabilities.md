# Building Deterministic Capabilities for BaseLayerOS

Capabilities are the atomic units of work inside BaseLayerOS.  
They must be **deterministic**, **side‑effect‑free**, and **fully auditable**.

This document explains how to build, register, and validate capabilities.

---

## 1. Capability Requirements

A capability must:

- Accept a deterministic input payload
- Produce a deterministic output payload
- Have no external side effects
- Not depend on time, randomness, or external state
- Be pure and reproducible

Capabilities are invoked by the executor in strict order.

---

## 2. Capability Structure

A capability is a simple Python class with:

- an `id` string (unique)
- a `run(inputs)` method

Example:

```python
class EchoCapability:
    id = "builtin.echo"

    def run(self, inputs):
        return inputs
```

This is the simplest possible deterministic capability.

## 3. Registration

Capabilities are registered through the `CapabilityRegistry`.

```python
registry.register("my.capability", MyCapability())

```

Built-ins are auto-registered by the `CapabilityLoader`.

See: `Capability Loader`

## 4. Deterministic Design Rules

### Rule 1 — No randomness

No random, no UUIDs, no nondeterministic ordering.

### Rule 2 — No time

Capabilities cannot read the clock.
Timestamps are added only by the audit subsystem.

### Rule 3 — No external I/O

No network calls, no file writes, no external state.

### Rule 4 — Pure functions

Given the same input, the output must always be identical.

### Rule 5 — No mutation of inputs

Inputs must be treated as immutable.

## 5. Capability Invocation

Capabilities are invoked by the executor:

PHASE 1 TestPhase
  TASK task1 builtin.echo
    INPUTS {"x": 1}
    OUTPUTS {}
  END_TASK
END_PHASE

The executor:

1. Parses DSL
2. Looks up capability by ID
3. Calls run(inputs)
4. Enforces postconditions
5. Stores output deterministically

See: `Executor Runtime`

## 6. Testing Capabilities

Capabilities should be tested with:

- deterministic input sets
- repeated runs
- output equality checks

Example test:

def test_echo():
    echo = EchoCapability()
    assert echo.run({"a": 1}) == {"a": 1}

See: Capability Tests

## 7. Future Extensions

Future versions of BaseLayerOS will support:

- capability sandboxing
- capability provenance
- capability versioning
- capability marketplaces

All while preserving deterministic guarantees.
