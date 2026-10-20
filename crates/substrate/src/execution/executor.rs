use crate::envelopes::execution_envelope::ExecutionEnvelope;
use crate::state_machine::substrate_state::SubstrateState;
use crate::execution::refusal_engine::ExecutionResult;

pub fn execute(_state: &mut SubstrateState, envelope: &ExecutionEnvelope) -> ExecutionResult {
    ExecutionResult {
        allowed: true,
        message: format!("Executed {}", envelope.id),
    }
}
