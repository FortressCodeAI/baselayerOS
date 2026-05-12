# BaseLayerOS — Deterministic Execution Substrate

BaseLayerOS is an open‑source, deterministic execution substrate designed for enterprises that need **predictable**, **auditable**, and **governance‑safe** AI workflows.

It is **not** a model, planner, or reasoning engine.  
It is the **foundation layer** that governance engines, safety systems, and enterprise workflows run on.

This repository contains the **public substrate only**:

- deterministic action execution  
- invariant‑checked state transitions  
- GIU‑metered credit system  
- replayable execution  
- JSON‑schema validation  
- a minimal builtin action (`echo`)  
- a complete test suite  

Higher‑level systems (governance, marketplace, authority tokens, compliance envelopes, CLI, BMA/MPA/SEA pipeline) are **proprietary** and intentionally excluded.

---

## Why BaseLayerOS Exists

Modern AI systems lack:

- deterministic behavior  
- predictable execution  
- enforceable safety invariants  
- auditability  
- reproducibility  

BaseLayerOS solves this by providing a **sealed execution substrate** that:

- never calls external APIs  
- never performs inference  
- never mutates behavior at runtime  
- never introduces nondeterminism  

It is the **Linux‑kernel‑equivalent** for AI governance systems.

---

## Repository Structure

src/substrate/
actions/    # deterministic actions + registry
runtime/    # executor, dispatcher, replay engine
credits/    # GIU ledger, burn engine, pricing
invariants/     # Preconditions, postconditions, invariants, verifier
utils/      # hashing + schema validation
schemas/    # JSON schemas for validation
tests/      # full test suite

This structure is intentionally minimal and stable.

## Features

### Deterministic Execution

Every action produces the same output for the same input and state.

### Invariant Enforcement

Safety conditions are checked before and after execution.

### Preconditions & Postconditions

Actions must satisfy deterministic contraints at every step.

### GIU Metering

Every action burns GIU credits through a deterministic ledger.

### Replay Engine

Reconstruct state transitioins deterministically for audit and verification.

### JSON-Schema Validation

Stable, auditable contracts for state, actions and credit events.

## Installation

From the repository root:

`pip install -e .[dev]`

Run tests:

pytest

## Quick Example

`from substrate.runtime import Dispatcher`

`dispatcher = Dispatcher(initial_state={"value": 0})`

`result = dispatcher.dispatch(`
    `action_name="echo",`
    `version="1.0",`
    `params={"value": 42},`
    `context={},`
`)`

`print(result["response"]["next_state"])`
`# {"value": 42}`

What's Not Included (By Design)

This repository does not include:

- authority token system
- governance engine
- proposal pipeline
- compliance envelopes
- marketplace
- CLI
- BMA / MPA / SEA artifact pipeline
- enterprise identity integration
- billing or credit lodger (enterprise edition)
- high-performance parallel runtime

These belong to higher layers (proprietary).

BaseLayerOS is the substrate, not the orchestrator.

## Contributing

Contributions are welcome.

Please open issues or pull requests for:

- new deterministic actions
- schema improvements
- invarient enhancements
- documentation updates
- test coverage

## License

BaseLayerOS is released under the Apache 2.0 License.

## Status

BaseLayerOS is stable, deterministic and suitable for enterpirse integration.
Additional tooling and ecosystem components are under active development.

---
