from kali.workflows.engine import (
    WorkflowEngine
)

from kali.workflows.governed_llm_workflow import (
    WORKFLOW
)

from kali.core.executor import (
    GovernedExecutor
)


def main():

    engine = WorkflowEngine(
        GovernedExecutor()
    )

    return engine.execute_workflow(

        "governed_llm",

        WORKFLOW,

        {

            "prompt":
                "Explain Kali."
        }
    )