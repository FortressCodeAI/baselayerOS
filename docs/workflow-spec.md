# Workflow Specification

Workflows are the primary unit of deterministic execution in BaseLayerOS.
They orchestrate modules, enforce compliance, and produce replayable traces.

This document defines the workflow specification.

## 1. Workflow Overview

A workflow:

- has an ID and version
- defines a sequence of steps
- may call modules
- may be governed by compliance packs
- must be deterministic and replayable

## 2. Workflow Definition

A workflow is defined as YAML or JSON:

```yaml
workflow:
  id: "string"
  version: "string"
  name: "string"
  description: "string"

  inputs:
    type: "object"
    properties: { }

  outputs:
    type: "object"
    properties: { }

  steps:
    - id: "string"
      name: "string"
      type: "module | decision | transform"
      module_id: "string"
      module_action: "string"
      input_mapping: { }
      output_mapping: { }
      on_failure: "continue | halt | compensate"

### 2.1 `inputs` and `outputs`

- JSON Schema fragments describing the workflow’s input and output shapes.

### 2.2 steps

Each step:

- has an `id` and `name`
- has a type:
    - `module` — calls a module
    - `decision` — branching logic
    - `transform` — pure data transformation

- may specify:

    - `module_id` and `module_action`
    - `input_mapping` — how workflow state maps to step input
    - `output_mapping` — how step output maps back to state
    - `on_failure` — failure behavior

## 3. Execution Semantics

- Steps execute in order unless explicitly branched.
- Branching must be:

    - explicit
    - deterministic
    - based on state

No hidden side effects are allowed.

## 4. Compliance Integration

Workflows may:

- declare which compliance packs apply
- expose metadata for evidence generation

Compliance packs may:

- block execution
- require approvals
- enforce invariants

## 5. Schema

The machine‑readable JSON Schema for workflows is defined in:

`standard/schemas/workflow.schema.json`
