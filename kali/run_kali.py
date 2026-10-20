#!/usr/bin/env python3
"""
Kali v1.0.0 — Enterprise Governance Operator entrypoint.

This script wires:
- core config + logging
- symbolic governance core
- neural sandbox (DeepSeek)
- CLI interface

Kali is NOT the substrate.
She is the governed operator that sits on top of BaseLayerOS.
"""

from kali.src.kali.core.config import KaliConfig
from kali.src.kali.core.logging import get_logger
from kali.src.kali.interfaces.cli.cli import KaliCLI
from kali.src.kali.symbolic.envelope_builder import EnvelopeBuilder
from kali.src.kali.symbolic.risk_engine import RiskEngine
from kali.src.kali.symbolic.capability_engine import CapabilityEngine
from kali.src.kali.symbolic.hitl_engine import HITLEngine
from kali.src.kali.symbolic.council_router import CouncilRouter
from kali.src.kali.symbolic.replay_engine import ReplayEngine
from kali.src.kali.neural.sandbox.sandbox import NeuralSandbox
from kali.src.kali.operators.governance_operator import GovernanceOperator


def build_kali_operator() -> GovernanceOperator:
    """
    Construct a fully wired Kali governance operator.
    """
    config = KaliConfig.load()
    logger = get_logger("kali")

    # Symbolic core
    envelope_builder = EnvelopeBuilder(config=config, logger=logger)
    risk_engine = RiskEngine(config=config, logger=logger)
    capability_engine = CapabilityEngine(config=config, logger=logger)
    hitl_engine = HITLEngine(config=config, logger=logger)
    council_router = CouncilRouter(config=config, logger=logger)
    replay_engine = ReplayEngine(config=config, logger=logger)

    # Neural sandbox (DeepSeek or other small model)
    neural_sandbox = NeuralSandbox(config=config, logger=logger)

    operator = GovernanceOperator(
        config=config,
        logger=logger,
        envelope_builder=envelope_builder,
        risk_engine=risk_engine,
        capability_engine=capability_engine,
        hitl_engine=hitl_engine,
        council_router=council_router,
        replay_engine=replay_engine,
        neural_sandbox=neural_sandbox,
    )

    return operator


def main() -> None:
    """
    Entrypoint for Kali CLI.
    """
    operator = build_kali_operator()
    cli = KaliCLI(operator=operator)
    cli.run()


if __name__ == "__main__":
    main()
