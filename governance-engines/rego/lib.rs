use serde::{Deserialize, Serialize};
use thiserror::Error;
use crate::canonical::CanonicalEnvelope;


#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum RegoDecision {
    Allow,
    Deny,
}


#[derive(Debug, Error)]
pub enum RegoEvaluationError {
    #[error("Failed to prepare REGO input: {0}")]
    InputError(String),

    #[error("Failed to evaluate REGO policy: {0}")]
    PolicyError(String),

    #[error("Invalid REGO result: {0}")]
    ResultError(String),
}

pub struct RegoGovernanceAdapter;

impl RegoGovernanceAdapter {
    pub fn new() -> Self {
        Self
    }

    pub fn evaluate(
        &self,
        envelope: &CanonicalEnvelope,
    ) -> Result<RegoDecision, RegoEvaluationError> {
        let payload = envelope
            .payload
            .as_object()
            .ok_or_else(|| RegoEvaluationError::InputError(
                "Envelope payload must be an object".to_string(),
            ))?;

        let rego = payload
            .get("rego")
            .ok_or_else(|| RegoEvaluationError::InputError(
                "Missing REGO metadata".to_string(),
            ))?;

        let rego_obj = rego
            .as_object()
            .ok_or_else(|| RegoEvaluationError::InputError(
                "REGO metadata must be an object".to_string(),
            ))?;

        let allow = rego_obj
            .get("allow")
            .and_then(|v| v.as_bool())
            .ok_or_else(|| RegoEvaluationError::ResultError(
                "Missing REGO allow flag".to_string(),
            ))?;

        if allow {
            Ok(RegoDecision::Allow)
        } else {
            Ok(RegoDecision::Deny)
        }
    }
}
