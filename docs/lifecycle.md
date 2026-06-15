# Ues Lifecycle Model

The UES lifecycle defines the legal states and transitions for a proposal.
It ensures deterministic progression through the BaseLayerOS pipeline.

## 1. Lifecycle States

A UES proposal can be in one of five states:

DRAFT → REVIEWED → OPTIMIZED → COMPILED → EXECUTED

See: `[State Machine](ca://s?q=Show_state_machine)`

## 2. State Definitions

### DRAFT

Initial state. Proposal has been created but not validated.

### REVIEWED

Councils have validated structure, safety, compliance, and risk.

### OPTIMIZED

Proposal has passed council review and is ready for compilation.

### COMPILED

Compiler has produced deterministic DSL.

### EXECUTED

Executor has run the DSL and produced deterministic outputs.

This is the terminal state.

## 3. Allowed Transitions

The state machine enforces:

DRAFT      → REVIEWED
REVIEWED   → OPTIMIZED
OPTIMIZED  → COMPILED
COMPILED   → EXECUTED

No other transitions are permitted.

Attempting an illegal transition raises a `StateTransitionError`.

## 4. Transition Rules

Each transition:

- must be triggered by the orchestrator  
- must be recorded in the audit chain  
- must update `last_modified_by` and `last_modified_at`  
- must be deterministic  

Example transition event:

```json
{
  "action": "STATE_TRANSITION",
  "details": {
    "from": "OPTIMIZED",
    "to": "COMPILED"
  }
}
```

## 5. Lifecycle in the Pipeline

The orchestrator enforces the lifecycle:

- Load UES
- Councils run → transition to REVIEWED
- Optimization → transition to OPTIMIZED
- Compilation → transition to COMPILED
- Execution → transition to EXECUTED

See: Pipeline

## 6. Deterministic Guarantees

The lifecycle model ensures:

- no skipping stages
- no backward transitions
- no ambiguous states
- no nondeterministic branching

This is essential for enterprise governance.

## 7. Future Extensions

Future versions may introduce:

- PAUSED
- CANCELLED
- REJECTED
- ARCHIVED

But only if they preserve deterministic semantics.
