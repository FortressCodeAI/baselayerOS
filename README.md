# BaseLayerOS

BaseLayerOS is a **deterministic execution substrate** for AI systems, built around a single canonical contract:

- `**UES - Universal Execution Schema**`

Every task, workflow or "proposal" is represented as a UES object, passed through a strict lifecycle:

`DRAFTED -> OPTIMIZED -> RISK_REVIEWED -> APPROVED -> COMPILED -> EXECUTED (or REJECTED)`

No backdoors. No implicit behaviour. Everything is explicit, auditable and replayable.

## Core Ideas

- **Universal Execution Schema (UES)**
    A versioned, immutable schema that describes:
- intent
- inputs
- capabilities
- plan (phases, tasks, graph)
- constraints
- global conditions (pre/post)
- scores
- state
- authority & approvals
- audit chain

- **Deterministic substrate**
    The runtime never "guesses". It:

- validates UES against a frozen schema
- enforces a strict state machine
- fails closed on ambiguity or invalidity

- **Councils, compiler, executor**
- Council 1: structure & plan validation
- Council 2: risk, cost, time, safety, compliance
- Compiler: deterministic codegen with pre/post enforcement
- Executor: runs compiled artifacts and validates postconditions

- **Audit chain**
    Every transition appends an events to a SHA-256 chain for tamper detection and replay.

## Quick Start

`Bash

### install in editable mode

`pip install -e ".[dev]"

### run tests

pytest

### run a sample UES through the pipeline

python examples/minimal/run.py

## Status

This is an early but opinionated implementation of a deterministic substrate intended for serious AI governance and enterprise integration. The UES v1.0.0 schema is frozen; future changes will be additive and versioned.

## License

MIT
