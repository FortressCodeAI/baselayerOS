from kali.workflows.engine import (
    WorkflowEngine
)

from kali.workflows.change_approval_workflow import (
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

        "change_approval",

        WORKFLOW,

        {

            "request":
                "open firewall port",

            "target":
                "production"
        }
    )