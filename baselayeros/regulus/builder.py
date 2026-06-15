# baselayeros/regulus/builder.py

from dataclasses import dataclass

from baselayeros.core.runtime.engine import ExecutionEngine
from baselayeros.regulus.config import RegulusConfig
from baselayeros.regulus.policy import PolicyEngine
from baselayeros.regulus.risk import RiskAssessor
from baselayeros.regulus.simulator import RegulusSimulator
from baselayeros.regulus.interface import RegulusInterface


@dataclass
class RegulusBuilder:
    """
    Constructs a fully wired Regulus subsystem.
    """

    @staticmethod
    def build(engine: ExecutionEngine) -> RegulusInterface:
        config = RegulusConfig()
        policy = PolicyEngine(config=config)
        risk = RiskAssessor()
        simulator = RegulusSimulator(
            config=config,
            policy=policy,
            risk=risk,
        )
        return RegulusInterface(engine=engine, simulator=simulator)
