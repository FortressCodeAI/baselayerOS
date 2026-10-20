use crate::state_machine::snapshot::StateSnapshot;
use crate::envelopes::execution_envelope::ExecutionEnvelope;
use crate::errors::substrate_error::SubstrateError;

pub trait InvariantEngine {
    fn check_pre(&self, snapshot: &StateSnapshot, envelope: &ExecutionEnvelope) -> Result<(), SubstrateError>;
    fn check_post(&self, snapshot: &StateSnapshot, envelope: &ExecutionEnvelope) -> Result<(), SubstrateError>;
}

pub struct DefaultInvariantEngine;

impl DefaultInvariantEngine {
    pub fn new() -> Self {
        Self
    }
}

impl InvariantEngine for DefaultInvariantEngine {
    fn check_pre(&self, _snapshot: &StateSnapshot, _envelope: &ExecutionEnvelope) -> Result<(), SubstrateError> {
        Ok(())
    }

    fn check_post(&self, _snapshot: &StateSnapshot, _envelope: &ExecutionEnvelope) -> Result<(), SubstrateError> {
        Ok(())
    }
}
