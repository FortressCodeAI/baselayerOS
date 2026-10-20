from kali.workflows.engine import (
    WorkflowEngine
)

from kali.workflows.incident_response_workflow import (
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

        "incident_response",

        WORKFLOW,

        {

            "alert":
                "Unauthorized login attempt"
        }
    )