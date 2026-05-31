# Determinism Rules

This document defines the normative rules that all BaseLayerOS‑conformant
runtimes must follow to guarantee deterministic execution, replayability,
and auditability.

These rules are strict.  
If an implementation violates any rule, it is **not** a conformant runtime.

---

## 1. Deterministic Execution Model

A runtime must ensure that:

- identical inputs  
- under identical environment configuration  
- with identical versioned dependencies  

produce:

- identical outputs  
- identical intermediate states  
- identical audit events  
- identical replay traces  

Formally:

> f(input, env, versions) → (output, trace)  
> must be a pure function.

---

## 2. Disallowed Sources of Non‑Determinism

The following behaviors are **forbidden** unless explicitly mediated by the runtime:

### 2.1 System Time

- Direct calls to system time are disallowed.
- Time must be injected as:
  - an explicit workflow input, or
  - a runtime‑provided fixed timestamp recorded in the trace.

### 2.2 Randomness

- Non‑seeded randomness is disallowed.
- Allowed randomness must:
  - use a fixed seed
  - record the seed in the trace
  - replay with the same seed

### 2.3 External Services

- Direct network calls are disallowed.
- External calls must:
  - be mediated by the runtime
  - record request + response in the trace
  - replay using recorded responses

### 2.4 Concurrency

- Non‑deterministic concurrency is disallowed.
- Parallelism is allowed only if:
  - execution order is fixed, or
  - results are commutative + associative and documented as such.

## 3. State Transition Rules

### 3.1 Immutability

- Workflow state is immutable.
- Each step produces a **new** state.
- Historical states must be reconstructable from the trace.

### 3.2 Explicitness

- All state transitions must be explicit.
- No hidden mutation of global or shared state.

### 3.3 Serialization

- State must be serializable to canonical JSON.

## 4. Version Pinning

All dependencies must be pinned:

- module versions  
- model versions  
- dataset versions  
- workflow versions  

No floating versions are allowed.

## 5. Error Handling

- Errors must be deterministic.
- Retry behavior must be deterministic.
- Errors must be recorded in the trace.

## 6. Compliance Integration

Compliance packs may impose additional deterministic constraints.  
A runtime must enforce them.

## 7. Replay Fidelity

A runtime must guarantee that:

- replaying a trace  
- produces the same outputs  
- and the same hashes  

Any mismatch indicates non‑conformance.
