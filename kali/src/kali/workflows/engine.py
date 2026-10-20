import uuid


class WorkflowEngine:

    def __init__(self, executor):

        self.executor = executor

    def execute_workflow(
        self,
        workflow_name,
        steps,
        context
    ):

        workflow_id = str(
            uuid.uuid4()
        )

        results = []

        for step in steps:

            result = step(
                context
            )

            results.append(
                result
            )

            if isinstance(
                result,
                dict
            ):
                context.update(
                    result
                )

        return {

            "workflow_id":
                workflow_id,

            "workflow":
                workflow_name,

            "status":
                "completed",

            "steps":
                results
        }