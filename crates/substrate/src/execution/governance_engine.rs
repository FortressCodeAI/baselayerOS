use crate::envelopes::execution_envelope::ExecutionEnvelope;
use crate::envelopes::governance_decision::GovernanceDecision;
use crate::state_machine::snapshot::StateSnapshot;

pub fn evaluate(_snapshot: &StateSnapshot, _envelope: &ExecutionEnvelope) -> GovernanceDecision {
    GovernanceDecision::Allow
}
