# Universal Execution Schema (UES) - v1.0.0

The **Universal Execution Schema (UES)** is the canonical, deterministic packet format used by BaseLayerOS to represent *any* workflow, and *any* executioni request across all domains and industries.

This schema defines the structure that every proposal must conform to before it can be validated, optimized, risk-reviewed, compiled, executed or audited.

## Purpose

UES provides:

- A universal structure for representing intent, inputs, plans, constraints and capabilites.
- Deterministic validation and execution boundaries.
- A stable contract for councils, compilers, agents and modules.
- A versioned, immutable protocol layer for BaseLayerOS.

## Files in this Directory

- **`ues.schema.json`**
    The canonical JSON schema for UES v1.0.0.
    All proposals must validate against the file.

- **`ues.types.py`**
    Python dataclasses representing the UES structure.
    Used by the orchestrator, compiler and coucils.

- **`README.md`**
    This documentation file.

## Versioning

UES is versioned using semantic versioning:

- **MAJOR** - breaking changes
- **MINOR** - additive, backward-compatible changes
- **PATCH** - corrections or clarifications

This directory (`v.1.0.0`) is immutable.
Future versions will be added as new folders:

`/schema/ues/v1.1.0/`
`/schema/ues/v2.0.0/`

## Validation

All incoming proposals must be validated against:

`ues.schema.json`

Validation occurs before:

1. Optimization (council 1)
2. Risk Review (council 2)
3. Compilation
4. Execution

Invalid proposals must fail closed.

## State Machine

UES proposals follow a strict lifecycle:

`DRAFTED->OPTIMIZED->RISK_REVIEWED->APPROVED->COMPILED->EXECUTED`

Any stage may transition to `REJECTED`.

## Audit Chain

UES includes a SHA-256 event chain for tamper detection and replayability.

Every State transition must append an audit event.

## Authority & Approvals

UES includes explicit fields for:

- requester identity
- roles and scopes
- top-authority requirements
- cryptographic signatures

Execution is forbidden without required approvals.

## Contact

For questions about UES or BaseLayerOS protocol design, contact the maintaining team or refer to the main project documentation.
