from dataclasses import dataclass
from typing import Any, Dict

from baselayeros.core.runtime.engine import ExecutionEngine
from baselayeros.regulus.simulator import RegulusSimulator


@dataclass
class RegulusInterface:
    """
    Thin integration layer between Regulus and BaseLayerOS companies.
    """

    engine: ExecutionEngine
    simulator: RegulusSimulator

    @classmethod
    def attach(cls, engine: ExecutionEngine) -> "RegulusInterface":
        simulator = RegulusSimulator.bootstrap()
        return cls(engine=engine, simulator=simulator)

    def run_with_regulus(
        self,
        operation: str,
        context: Dict[str, Any],
        fn,
    ) -> Dict[str, Any]:
        """
        1. Ask Regulus to simulate the decision.
        2. Set engine risk tier from Regulus.
        3. Execute the operation under governance.
        """

        decision = self.simulator.simulate(operation, context)
        risk_tier = decision["risk_tier"]

        # Propagate risk tier into the engine if you added set_risk_tier
        if hasattr(self.engine, "set_risk_tier"):
            self.engine.set_risk_tier(risk_tier) # type: ignore

        result = self.engine.run(
            actor="regulus",
            operation=operation,
            fn=fn,
        )

        return {
            "regulus_decision": decision,
            "engine_result": {
                "success": result.success,
                "value": result.value,
                "error": result.error,
                "committed": result.committed,
            },
        }
