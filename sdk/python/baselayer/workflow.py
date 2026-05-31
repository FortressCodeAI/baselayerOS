"""
BaseLayerOS Python SDK — Workflow Builder
"""

from typing import Any, Dict, List, Optional


class WorkflowStep:
    """
    Represents a single workflow step.
    """

    def __init__(
        self,
        step_id: str,
        name: str,
        step_type: str,
        module_id: Optional[str] = None,
        module_action: Optional[str] = None,
        input_mapping: Optional[Dict[str, Any]] = None,
        output_mapping: Optional[Dict[str, Any]] = None,
        on_failure: Optional[str] = None,
    ):
        self.step_id = step_id
        self.name = name
        self.step_type = step_type
        self.module_id = module_id
        self.module_action = module_action

        # Explicit typing to avoid Pylance narrowing {} to Dict[str, str]
        self.input_mapping: Dict[str, Any] = input_mapping if input_mapping is not None else {}
        self.output_mapping: Dict[str, Any] = output_mapping if output_mapping is not None else {}

        self.on_failure = on_failure

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "id": self.step_id,
            "name": self.name,
            "type": self.step_type,
        }

        if self.module_id:
            data["module_id"] = self.module_id
        if self.module_action:
            data["module_action"] = self.module_action
        if self.input_mapping:
            data["input_mapping"] = self.input_mapping
        if self.output_mapping:
            data["output_mapping"] = self.output_mapping
        if self.on_failure:
            data["on_failure"] = self.on_failure

        return data


class Workflow:
    """
    Represents a deterministic workflow definition.
    """

    def __init__(
        self,
        workflow_id: str,
        version: str,
        name: str,
        description: str,
        inputs: Dict[str, Any],
        outputs: Dict[str, Any],
    ):
        self.workflow_id = workflow_id
        self.version = version
        self.name = name
        self.description = description
        self.inputs = inputs
        self.outputs = outputs

        self.steps: List[WorkflowStep] = []

    def add_step(self, step: WorkflowStep):
        self.steps.append(step)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "workflow": {
                "id": self.workflow_id,
                "version": self.version,
                "name": self.name,
                "description": self.description,
                "inputs": self.inputs,
                "outputs": self.outputs,
                "steps": [s.to_dict() for s in self.steps],
            }
        }
