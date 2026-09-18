use crate::canonical::CanonicalEnvelope;
use serde::{Deserialize, Serialize};
use thiserror::Error;


#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SubstrateState {
    pub version: u64,
    pub data: serde_json::Value,
}

impl SubstrateState {
    pub fn new() -> Self {
        Self {
            version: 0,
            data: serde_json::json!({}),
        }
    }
}

#[derive(Debug, Error)]
pub enum StateTransitionError {
    #[error("State data is not an object")]
    StateNotObject,

    #[error("Envelope payload is not an object")]
    PayloadNotObject,

    #[error("Failed to merge envelope payload into state: {0}")]
    MergeError(String),
}

pub fn apply_state_transition(
    state: &mut SubstrateState,
    envelope: &CanonicalEnvelope,
) -> Result<(), StateTransitionError> {
    if !state.data.is_object() {
        return Err(StateTransitionError::StateNotObject);
    }

    if !envelope.payload.is_object() {
        return Err(StateTransitionError::PayloadNotObject);
    }

    let mut state_obj = state
        .data
        .as_object()
        .cloned()
        .ok_or_else(|| StateTransitionError::StateNotObject)?;

    let payload_obj = envelope
        .payload
        .as_object()
        .cloned()
        .ok_or_else(|| StateTransitionError::PayloadNotObject)?;

    for (k, v) in payload_obj.into_iter() {
        state_obj.insert(k, v);
    }

    state.data = serde_json::Value::Object(state_obj);
    state.version += 1;

    Ok(())
}
