# Integrator Guide

This guide explains how integrators can build on the BaseLayerOS standard
using the public schemas and SDK.

## 1. What You Can Build

As an integrator, you can:

- define deterministic workflows
- build modules that conform to the module contract
- define compliance packs that enforce governance rules
- integrate with enterprise runtimes that implement the standard

## 2. Typical Integration Flow

### A. Understand the standard

- Read `overview.md`
- Read `deterministic-runtime.md`
- Review schemas in `standard/schemas/`

### B. Design workflows

- Use `workflow-spec.md`
- Start from examples in `standard/examples/`

### C. Build modules

- Use the Python SDK in `sdk/python/baselayer/`
- Define manifests using `module-contract.md`

### D. Add compliance

- Define compliance packs using `compliance-pack-interface.md`

### E. Test determinism

- Validate against schemas
- Use replay traces (where supported by the runtime)

## 3. SDK Usage (Python)

The Python SDK provides:

- `baselayer.workflow` — helpers for defining workflows
- `baselayer.module` — helpers for defining modules
- `baselayer.compliance_interface` — helpers for compliance integration

See:

- `sdk/examples/build-a-module.md`
- `sdk/examples/build-a-workflow.md`

## 4. Working with Enterprise Runtimes

This public standard is implemented by enterprise runtimes that:

- provide deterministic execution
- enforce compliance
- generate replay traces
- maintain audit logs

As an integrator, you:

- target the standard
- deploy to any conformant runtime

## 5. Certification

Enterprise vendors may offer:

- certification programs for modules
- validation of compliance packs
- conformance testing for workflows

This repository does not define certification processes, but provides the schemas and specifications they rely on.

## 6. Contributing Back

You may:

- propose improvements to schemas
- suggest new examples
- refine documentation

See `CONTRIBUTING.md` for details.
