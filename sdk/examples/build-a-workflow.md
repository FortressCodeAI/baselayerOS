# Building a BaseLayerOS Workflow

This guide shows how to define a deterministic workflow using the
BaseLayerOS workflow schema and the Python SDK.

## 1. Workflow Structure

A workflow is a YAML file that defines:

- inputs  
- outputs  
- steps  
- module calls  
- decision logic  

Example:

```yaml
workflow:
  id: "credit_risk_assessment_v1"
  version: "1.0.0"
  name: "Credit Risk Assessment"
  description: "Deterministic workflow for evaluating credit risk."

  inputs:
    type: object
    properties:
      income: { type: number }
      credit_score: { type: number }
      existing_debt: { type: number }
    required: [income, credit_score, existing_debt]

  outputs:
    type: object
    properties:
      risk_score: { type: number }
      decision: { type: string }

## 2. Adding Steps

Steps define the deterministic execution path:

```yaml
steps:
  - id: "calculate_risk"
    name: "Calculate Risk Score"
    type: "module"
    module_id: "finance.risk_model"
    module_action: "score"
    input_mapping:
      income: "$.income"
      credit_score: "$.credit_score"
      existing_debt: "$.existing_debt"
    output_mapping:
      risk_score: "$.risk_score"

Decision logic is deterministic and must not call external services.

## 4. Building Workflows with the python SDK

```Python
from baselayer.workflow import Workflow, WorkflowStep

wf = Workflow(
    workflow_id="credit_risk_assessment_v1",
    version="1.0.0",
    name="Credit Risk Assessment",
    description="Deterministic credit scoring workflow",
    inputs={"type": "object"},
    outputs={"type": "object"},
)

wf.add_step(
    WorkflowStep(
        step_id="calculate_risk",
        name="Calculate Risk",
        step_type="module",
        module_id="finance.risk_model",
        module_action="score",
        input_mapping={"income": "$.income"},
        output_mapping={"risk_score": "$.risk_score"},
    )
)

workflow_dict = wf.to_dict()

## 5. Determinism Requirements

Workflows must:

- define explicit input/output mappings
- avoid implicit state mutation
- avoid nondeterministic branching
- rely only on module outputs and step inputs

Workflows must not:

- call external APIs
- depend on system time
- use randomness

## 6. Validation

Workflows can be validated against the schema:

`standard/workflow.schema.json`

This ensures structural correctness before deployment.

## 7. Summary

A BaseLayerOS workflow is:

- deterministic
- explicit
- replayable
- auditable

Workflows + modules form the complete deterministic execution graph
enforced by the BaseLayerOS substrate.
