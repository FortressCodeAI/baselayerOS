# Module Contract Specification

Modules are the primary extension mechanism in BaseLayerOS.  
They encapsulate capabilities, invariants, and actions that can be used
by workflows and compliance packs.

This document defines the **module manifest** and the **expected behavior**
of conformant modules.

## 1. Module Overview

A module is defined by:

- a manifest (metadata and capabilities)
- an implementation (code)
- a set of invariants (conditions that must hold)
- a set of actions (operations the module can perform)

The public standard defines the manifest format and the interface surface.
The enterprise runtime provides the execution engine.

## 2. Manifest Structure

A module manifest is a YAML or JSON document with the following fields:

```yaml
module:
  id: "string"
  name: "string"
  version: "string"
  owner: "string"
  classification: "core | premium | enterprise | community"
  description: "string"

  capabilities:
    - "string"

  invariants:
    - "string"

  actions:
    - "string"

  signing:
    required: true
    owner: "string"

### 2.1 `id`

- A globally unique identifier for the module.
- Recommended format: `namespace_name_version`.

### 2.2 `name`

- Human-readable name.

### 2.3 `version`

- Semantic version string, e.g. `1.0.0`.

### 2.4 `owner`

- The organization or individual responsible for the module.

### 2.5 `classification`

- Indicates the module's role:
    - `core` - part of the base standard
    - `premium` - high-value, paid modules
    - `enterprise` - customer-specific modules
    - `community` - third-party modules

### 2.6 `description`

- Short description of the module's purpose.

### 2.7 `capabilities`

- High-level capabilities provided by the module, e.g.:
    - `risk_scoring`
    - `compliance_validation`
    - `evidence_generation`

### 2.8 `invariants`

- Named invariants that the module enforces or depends on.

### 2.9 `actions`

- Named actions that the module can perform.

### 2.10 `signing`

- Indicates whether the module must be signed.
- `owner` identifies the signing authority.

## 3. Module Interface 

At runtime, modules are invoked via a standard interface:

- input: structured JSON payload
- output: structured JSON payload
- errors: structured error objects

The public standard does not prescribe a specific function signature, but recommends:

- a single entrypoint per action
- explicit input and output schemas
- clear error semantics

## 4. Determinism Requirements

Modules must:

- be deterministic for given inputs and versions
- avoid uncontrolled side effects
- avoid non-deterministic operations

If a module depends on external services, it must:

- use mediated calls
- record inputs and outputs in replay trace

## 5. Compliance Integration

Modules may:

- expose compliance‑relevant capabilities
- enforce invariants
- emit audit events

Compliance packs can:

- depend on specific modules
- require certain invariants
- orchestrate module actions

## 6. Schema

The machine-readable JSON Schema for module manifests is defined in:

- `standard/schemas/module-manifest.schema.json`
