# BaseLayerOS Deterministic Pipeline

This document describes the full execution pipeline for a UES proposal.

## Overview

The pipeline is linear, deterministic, and auditable:

`Load → Councils → Optimize → Compile → Execute → Finalize`

Each stage emits an audit event.

## 1. Load

The proposal is loaded using:

- dict
- JSON string
- file path

Validated against the UES schema.

See: `baselayeros/ues/loader.py`

## 2. Council Review

Councils perform:

- structural validation
- safety checks
- compliance checks
- risk scoring

All councils must pass.

See: `baselayeros/councils/router.py`

## 3. Transition → OPTIMIZED

The state machine enforces legal transitions only.

See: `baselayeros/ues/state_machine.py`

## 4. Compile

The compiler:

- validates preconditions
- generates deterministic DSL
- embeds postconditions

Output: `CompiledArtifact`

See: `baselayeros/compiler/contract.py`

## 5. Transition → COMPILED

Recorded in the audit chain.

## 6. Execute

The executor:

- parses DSL
- invokes capabilities in order
- enforces postconditions
- returns deterministic outputs

See: `baselayeros/executor/runtime.py`

## 7. Transition → EXECUTED

Final lifecycle state.

## 8. Audit Chain

Every step produces an event:

- timestamp
- actor
- action
- previous hash
- details

See: `baselayeros/audit/store.py`

## Deterministic Failure Modes

The pipeline fails-closed on:

- invalid transitions
- missing capabilities
- failed preconditions
- failed postconditions
- malformed UES
- schema mismatch

## Deterministic Success Criteria

A run is successful when:

- all councils pass
- compilation succeeds
- execution succeeds
- all postconditions pass
- final state is EXECUTED

The output is a reproducible JSON object:

{
    "proposal_id": "...",
    "state": "EXECUTED",
    "result": {...},
    "success": true
}
