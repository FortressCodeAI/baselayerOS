from kali.src.kali.runtime.registry import resolve


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

        payload = getattr(
            execution, 
            "payload", 
            getattr(execution, "arguments", {})
        )
        
        # If execution is a raw dict instead of an object:
        if isinstance(execution, dict):
            payload = execution.get("payload", execution.get("arguments", {}))

        # Rest of your runtime execution logic...
        return {
            "status": "executed",
            "payload_processed": payload
        }