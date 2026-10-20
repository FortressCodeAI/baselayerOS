from kali.runtime.registry import resolve


class RuntimeEngine:

    def execute(
        self,
        execution
    ):

        fn = resolve(
            execution.action_slug
        )

        return fn(
            execution.payload
        )
