# Deterministic Runtime Specification

The BaseLayerOS deterministic runtime defines how workflows execute so that
the same inputs always produce the same outputs, with a fully replayable
and auditable trace.

This document specifies:

- allowed and disallowed behaviors
- state transition rules
- hashing rules
- version pinning requirements
- workflow execution semantics

It is a **normative** part of the BaseLayerOS standard.

---

## 1. Determinism Model

A workflow is deterministic if:

- for a given **input payload**  
- under a given **environment configuration**  
- with pinned **module**, **model**, and **dataset versions**  

it always produces:

- the same **outputs**
- the same **intermediate states**
- the same **audit events**
- the same **replay trace**

Formally:

> `f(input, env, versions) -> (output, trace)`  
> must be a pure function.

---

## 2. Sources of Non‑Determinism (and How They Are Handled)

The runtime **must eliminate or constrain** the following:

### 2.1 Time

- Direct calls to system time are **disallowed** in workflow logic.
- Time must be injected as an explicit input or provided by the runtime
  as a fixed value recorded in the trace.

### 2.2 Randomness

- Non‑seeded randomness is **disallowed**.
- Any randomness must be:
  - seeded
  - recorded in the trace
  - replayed with the same seed

### 2.3 External Services

- Direct, uncontrolled calls to external services are **disallowed**.
- External calls must:
  - be mediated by the runtime
  - have inputs and outputs recorded in the trace
  - be replayable via recorded responses

### 2.4 Concurrency

- Non‑deterministic concurrency (e.g., race conditions) is **disallowed**.
- Parallelism is allowed only if:
  - execution order is fixed
  - or results are commutative and associative and documented as such.

---

## 3. State Model

The runtime maintains a **workflow state** as a structured object.

### 3.1 State Transitions

- Each step in a workflow:
  - reads from the current state
  - produces a new state
- State transitions must be:
  - explicit
  - recorded in the trace
  - free of hidden side effects

### 3.2 Immutability

- Historical states are **never mutated**.
- The runtime may store only the latest state in memory, but the trace
  must allow reconstruction of all intermediate states.

---

## 4. Hashing Rules

The runtime uses cryptographic hashes to:

- anchor audit events
- anchor replay traces
- validate integrity

### 4.1 Canonical Serialization

Before hashing, objects must be:

- serialized to JSON
- with:
  - sorted keys
  - UTF‑8 encoding
  - no insignificant whitespace

### 4.2 Hash Function

- The standard hash function is **SHA‑256**.
- Implementations must produce identical hashes for identical inputs.

---

## 5. Version Pinning

Determinism requires explicit versioning of:

- modules
- models
- datasets
- workflows

### 5.1 Module Versions

- Each module must declare a `version` in its manifest.
- Workflows must reference specific module versions.

### 5.2 Model Versions

- Model identifiers must include version information.
- Model changes must be treated as new versions.

### 5.3 Dataset Versions

- Datasets used for training or inference must be versioned.
- Dataset identifiers must be stable and resolvable.

---

## 6. Workflow Execution Semantics

A workflow is defined as:

- a sequence of **steps**
- each step:
  - has a deterministic function
  - may call modules
  - may update state

### 6.1 Step Execution

- Steps execute in a defined order.
- A step may not:
  - modify global state outside the workflow
  - perform uncontrolled I/O
  - depend on hidden mutable state

### 6.2 Failure Handling

- Failures must be:
  - recorded in the trace
  - represented as explicit states
- Retry behavior must be:
  - deterministic
  - recorded in the trace

---

## 7. Replay Requirements

The runtime must support:

- loading a replay trace
- reconstructing the workflow state
- re‑executing steps deterministically
- comparing outputs and hashes

See `replay-engine.md` for the trace format.

---

## 8. Compliance Integration

The deterministic runtime is designed to work with:

- compliance packs
- audit logging
- provenance tracking
- lifecycle governance

Compliance packs may:

- enforce additional invariants
- block non‑compliant workflows
- require specific logging behavior

---

## 9. Extensibility

Implementations may extend the runtime with:

- additional logging
- performance optimizations
- platform integrations

as long as:

- determinism is preserved
- trace and audit formats remain compliant with the standard.
