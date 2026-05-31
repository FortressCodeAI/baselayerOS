# Compliance Pack Interface Specification

Compliance packs encode governance, regulatory, and policy requirements as
runtime‑enforced rules. They do not execute business logic themselves; they
constrain and validate workflows and modules.

This document defines the **interface** for compliance packs.

---

## 1. Purpose

A compliance pack:

- declares **invariants** that must hold
- declares **checks** that must be run
- declares **actions** to take on violation
- integrates with:
  - audit logging
  - replay traces
  - evidence generation

The public standard defines the interface; the enterprise engine provides
the enforcement.

---

## 2. Compliance Pack Manifest

A compliance pack manifest is a YAML or JSON document:

```yaml
compliance_pack:
  id: "string"
  name: "string"
  version: "string"
  owner: "string"
  description: "string"

  scope:
    workflows:
      - "workflow_id_pattern"
    modules:
      - "module_id_pattern"

  invariants:
    - id: "string"
      description: "string"
      severity: "info | warning | error | critical"

  checks:
    - id: "string"
      description: "string"
      when: "string"
      uses_invariants:
        - "invariant_id"

  actions:
    - id: "string"
      description: "string"
      on_violation:
        - "invariant_id"

### 2.1 `scope`

Defines where the pack applies:

- `workflows` — patterns matching workflow IDs
- `modules` — patterns matching module IDs

### 2.2 `invariants`

Named conditions that must hold, e.g.:

- “All high‑risk workflows must have replay enabled.”
- “All model versions must be pinned.”

### 2.3 `checks`

Logical groupings of invariants, with:

- `when` — conditions under which the check runs
- `uses_invariants` — referenced invariants

### 2.4 actions

Actions to take when invariants are violated, e.g.:

- block execution
- log an audit event
- require human approval

## 3. Runtime Interface

At runtime, a compliance pack is expected to expose:

- `evaluate(workflow_context) -> result`

where result includes:

- violations — list of violated invariants
- actions — actions to be taken
- evidence — optional structured evidence

The exact function signature is implementation‑specific; the standard
defines the shape of inputs and outputs.

## 4. Determinism and Replay

Compliance evaluation must be:

- deterministic for a given workflow state
- replayable from the trace

Violations and actions must be:

- recorded in the audit log
- reproducible during replay

## 5. Schema

The machine‑readable JSON Schema for compliance pack manifests is defined in:

- `standard/schemas/compliance-pack-interface.schema.json`
