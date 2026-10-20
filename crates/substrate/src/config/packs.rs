use crate::state_machine::snapshot::StateSnapshot;
use crate::envelopes::execution_envelope::ExecutionEnvelope;
use crate::envelopes::governance_decision::GovernanceDecision;

pub trait GovernancePack {
    fn evaluate(&self, snapshot: &StateSnapshot, envelope: &ExecutionEnvelope) -> GovernanceDecision;
    fn version(&self) -> &'static str;
}

pub struct DummyPack;

impl GovernancePack for DummyPack {
    fn evaluate(&self, _snapshot: &StateSnapshot, _envelope: &ExecutionEnvelope) -> GovernanceDecision {
        GovernanceDecision::Allow
    }

    fn version(&self) -> &'static str {
        "dummy-1.0"
    }
}
