use crate::state_machine::substrate_state::SubstrateState;
use crate::envelopes::execution_envelope::ExecutionEnvelope;
use crate::execution::refusal_engine::ExecutionResult;
use crate::errors::substrate_error::SubstrateError;

pub fn execute_envelope(
    _state: &mut SubstrateState,
    envelope: ExecutionEnvelope,
) -> Result<ExecutionResult, SubstrateError> {
    Ok(ExecutionResult {
        allowed: true,
        message: format!("Executed envelope {}", envelope.id),
    })
}
