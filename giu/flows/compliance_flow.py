"""
Regulus-style UI flow description for the compliance company.

This is not tied to any specific framework yet; it's a declarative
shape you can map into Regulus.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class FlowStep:
    id: str
    label: str
    description: str
    depends_on: List[str] = field(default_factory=list)


@dataclass
class ComplianceFlow:
    """
    Declarative description of the compliance pipeline for UI.
    """

    steps: List[FlowStep] = field(default_factory=list)

    @classmethod
    def default(cls) -> "ComplianceFlow":
        steps = [
            FlowStep(
                id="check_payment",
                label="Check Payment",
                description="Verify that the customer has paid for compliance services.",
            ),
            FlowStep(
                id="ingest_documents",
                label="Ingest Documents",
                description="Collect and register all relevant compliance documents.",
                depends_on=["check_payment"],
            ),
            FlowStep(
                id="extract_requirements",
                label="Extract Requirements",
                description="Derive concrete compliance requirements from the ingested documents.",
                depends_on=["ingest_documents"],
            ),
            FlowStep(
                id="generate_calendar",
                label="Generate Calendar",
                description="Create a schedule of compliance deadlines.",
                depends_on=["extract_requirements"],
            ),
            FlowStep(
                id="generate_packets",
                label="Generate Packets",
                description="Assemble compliance packets for submission and review.",
                depends_on=["generate_calendar"],
            ),
            FlowStep(
                id="store_audit_event",
                label="Store Audit Event",
                description="Record the pipeline execution in the audit chain.",
                depends_on=["generate_packets"],
            ),
            FlowStep(
                id="notify_customer",
                label="Notify Customer",
                description="Send a notification to the customer that their compliance package is ready.",
                depends_on=["store_audit_event"],
            ),
        ]
        return cls(steps=steps)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "steps": [
                {
                    "id": s.id,
                    "label": s.label,
                    "description": s.description,
                    "depends_on": s.depends_on,
                }
                for s in self.steps
            ]
        }
