from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class UIStep:
    id: str
    label: str
    description: str
    icon: str = "circle"
    next_steps: List[str] = field(default_factory=list)


@dataclass
class RegulusUIFlow:
    """
    Declarative UI flow for Regulus decisions.
    """

    steps: List[UIStep] = field(default_factory=list)

    @classmethod
    def default(cls) -> "RegulusUIFlow":
        return cls(
            steps=[
                UIStep(
                    id="simulate",
                    label="Simulate",
                    description="Regulus simulates the operation and evaluates risk.",
                    icon="brain",
                    next_steps=["policy"],
                ),
                UIStep(
                    id="policy",
                    label="Policy Evaluation",
                    description="Regulus applies the appropriate policy template.",
                    icon="scale",
                    next_steps=["execute"],
                ),
                UIStep(
                    id="execute",
                    label="Execute",
                    description="The governed engine executes the operation.",
                    icon="play",
                    next_steps=["audit"],
                ),
                UIStep(
                    id="audit",
                    label="Audit",
                    description="The result is recorded in the audit chain.",
                    icon="clipboard",
                    next_steps=[],
                ),
            ]
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "steps": [
                {
                    "id": s.id,
                    "label": s.label,
                    "description": s.description,
                    "icon": s.icon,
                    "next_steps": s.next_steps,
                }
                for s in self.steps
            ]
        }
