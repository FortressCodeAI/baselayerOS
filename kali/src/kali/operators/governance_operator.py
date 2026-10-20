"""
Kali v1.0.0 — Governance Operator

This is the heart of Kali.
It orchestrates the entire governance cycle:

1. Build envelope
2. Classify risk tier
3. Assign capability scope
4. Evaluate HITL requirement
5. Route councils
6. Run neural sandbox (interpret + explain)
7. Execute workflow (if substrate enabled)
8. Produce governed output
9. Export replay log

This operator is the "face" of Kali.
"""

from __future__ import annotations
from typing import Dict, Any

from kali.core.state import KaliState
from kali.core.logging import KaliLogger
from kali.councils import register_all_councils

class GovernanceOperator:
    def __init__(
        self,
        config,
        logger: KaliLogger,
        envelope_builder,
        risk_engine,
        capability_engine,
        hitl_engine,
        council_router,
        replay_engine,
        neural_sandbox,
    ):
        self.config = config
        self.logger = logger

        self.envelope_builder = envelope_builder
        self.risk_engine = risk_engine
        self.capability_engine = capability_engine
        self.hitl_engine = hitl_engine
        self.council_router = council_router
        self.replay_engine = replay_engine
        self.neural_sandbox = neural_sandbox

        # Register councils
        register_all_councils(self.council_router)

    def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Full governance cycle.
        """
        state = KaliState()

        # 1. Build envelope
        envelope = self.envelope_builder.build(request)
        state.start_envelope(envelope["envelope_id"], request)

        # 2. Risk tier classification
        tier = self.risk_engine.classify(request)
        state.set_risk_tier(tier)
        self.replay_engine.record(state.active_envelope, "risk_tier", tier)

        # 3. Capability scope assignment
        scope = request.get("capability_scope", "read_only")
        state.set_capability_scope(scope)
        self.replay_engine.record(state.active_envelope, "capability_scope", scope)

        # 4. Enforce capability scope
        self.capability_engine.enforce(scope, request)

        # 5. HITL evaluation
        tier_cfg = self.config.risk_tiers[tier]
        hitl_required = self.hitl_engine.evaluate(tier_cfg.level)
        if hitl_required:
            state.require_hitl()
        self.replay_engine.record(state.active_envelope, "hitl_required", hitl_required)

        # 6. Council routing
        self.council_router.route(state.active_envelope)

        # 7. HITL enforcement
        self.hitl_engine.enforce(state.active_envelope)

        # 8. Neural sandbox — interpret + explain
        neural_result = self.neural_sandbox.explain_governance(state.active_envelope)
        self.replay_engine.record(state.active_envelope, "neural_explanation", neural_result)

        # 9. Finalize envelope
        final_state = state.finalize()
        replay = self.replay_engine.export(final_state)

        return {
            "envelope_id": final_state.envelope_id,
            "risk_tier": final_state.risk_tier,
            "capability_scope": final_state.capability_scope,
            "hitl_required": final_state.hitl_required,
            "hitl_approved": final_state.hitl_approved,
            "councils_ran": final_state.councils_ran,
            "neural_explanation": neural_result,
            "replay": replay,
        }
