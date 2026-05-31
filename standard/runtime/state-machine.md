# State Machine Specification

This document defines the deterministic state machine model used by
BaseLayerOS‑conformant runtimes.

The state machine is the core of deterministic execution.

## 1. Purpose

The state machine:

- holds workflow state  
- applies deterministic updates  
- ensures immutability  
- prevents hidden side effects  
- supports replay reconstruction  

## 2. State Representation

State must be:

- a JSON‑serializable object  
- free of unserializable types  
- free of functions, classes, or opaque objects  
- canonicalizable for hashing  

## 3. State Transitions

A state transition:

- takes the current state  
- applies a deterministic update  
- produces a new state  

Formally:

> next_state = reducer(prev_state, update)

Where:

- `reducer` is deterministic  
- `update` is the output of a workflow step  

## 4. Transition Rules

### 4.1 No Mutation

- The previous state must never be mutated.
- A new state object must always be created.

### 4.2 Shallow Merge

- Updates must be applied as a shallow merge:
  - keys in the update replace keys in the state
  - no deep mutation of nested structures

### 4.3 Explicit Updates Only

- Only keys explicitly present in the update may change.
- No implicit or hidden updates.

## 5. Replay Requirements

The state machine must support:

- reconstructing state from a replay trace  
- applying updates in the same order  
- producing identical intermediate states  

If replay produces a different state at any step, the runtime is non‑conformant.

## 6. Compliance Integration

Compliance packs may:

- inspect state  
- enforce invariants on state transitions  
- block transitions that violate rules  

The state machine must expose:

- previous state  
- proposed update  
- next state  

for compliance evaluation.

## 7. Implementation Notes

The public standard defines the rules, not the implementation.

Enterprise runtimes may:

- optimize storage  
- use persistent data structures  
- use memory‑mapped state  
- use incremental hashing  

as long as:

- determinism is preserved  
- canonical JSON state is reproducible  
- replay fidelity is guaranteed  
