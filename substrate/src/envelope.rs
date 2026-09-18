use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use thiserror::Error;

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct EnvelopeId(pub String);

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum EnvelopeKind {
    Intent,
    Governance,
    Evidence,
    Control,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Envelope {
    pub id: EnvelopeId,

    pub kind: EnvelopeKind,

    pub source: String,

    pub correlation_id: Option<String>,

    pub timestamp: String,

    pub payload: serde_json::Value,

    pub tags: HashMap<String, String>,
}

#[derive(Debug, Error)]
pub enum EnvelopeValidationError {
    #[error("Envelope id is empty")]
    EmptyId,

    #[error("Envelope source is empty")]
    EmptySource,

    #[error("Envelope timestamp is empty")]
    EmptyTimestamp,

    #[error("Envelope payload is not an object")]
    PayloadNotObject,

    #[error("Missing required tag: {0}")]
    MissingRequiredTag(String),
}

pub fn validate_envelope(
    envelope: &Envelope,
    required_tags: &[&str],
) -> Result<(), EnvelopeValidationError> {
    if envelope.id.0.trim().is_empty() {
        return Err(EnvelopeValidationError::EmptyId);
    }

    if envelope.source.trim().is_empty() {
        return Err(EnvelopeValidationError::EmptySource);
    }

    if envelope.timestamp.trim().is_empty() {
        return Err(EnvelopeValidationError::EmptyTimestamp);
    }

    if !envelope.payload.is_object() {
        return Err(EnvelopeValidationError::PayloadNotObject);
    }

    for &tag in required_tags {
        if !envelope.tags.contains_key(tag) {
            return Err(EnvelopeValidationError::MissingRequiredTag(tag.to_string()));
        }
    }

    Ok(())
}
