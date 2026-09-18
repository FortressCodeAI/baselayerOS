use crate::canonical::CanonicalEnvelope;
use crate::state::SubstrateState;
use serde::{Deserialize, Serialize};


#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct InvariantViolation {
    pub message: String,
}

pub fn check_invariants(
    state: &SubstrateState,
    envelope: &CanonicalEnvelope,
) -> bool {
    if !state.data.is_object() {
        return false;
    }

    if !envelope.payload.is_object() {
        return false;
    }

    if let Some(obj) = envelope.payload.as_object() {
        if obj.is_empty() {
            return false;
        }

        for key in obj.keys() {
            if key.starts_with("__internal") {
                return false;
            }
        }
    }

    true
}
