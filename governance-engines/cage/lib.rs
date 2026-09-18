use serde::{Deserialize, Serialize};
use thiserror::Error;
use crate::canonical::CanonicalEnvelope;


#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum CageDecision {
    Allow,
    Deny,
    Escalate,
}

#[derive(Debug, Error)]
pub enum CageEvaluationError {
    #[error("Envelope missing required CAGE metadata: {0}")]
    MissingMetadata(String),

    #[error("Invalid CAGE metadata: {0}")]
    InvalidMetadata(String),

    #[error("CAGE rule violation: {0}")]
    RuleViolation(String),
}

pub struct CageGovernanceEngine;

impl CageGovernanceEngine {
    pub fn new() -> Self {
        Self
    }

    pub fn evaluate(
        &self,
        envelope: &CanonicalEnvelope,
    ) -> Result<CageDecision, CageEvaluationError> {
        let payload = envelope
            .payload
            .as_object()
            .ok_or_else(|| CageEvaluationError::InvalidMetadata(
                "Envelope payload must be an object".to_string(),
            ))?;

        let cage = payload
            .get("cage")
            .ok_or_else(|| CageEvaluationError::MissingMetadata(
                "Missing CAGE metadata".to_string(),
            ))?;

        let cage_obj = cage
            .as_object()
            .ok_or_else(|| CageEvaluationError::InvalidMetadata(
                "CAGE metadata must be an object".to_string(),
            ))?;

        let risk = cage_obj
            .get("risk")
            .and_then(|v| v.as_f64())
            .ok_or_else(|| CageEvaluationError::MissingMetadata(
                "Missing CAGE risk value".to_string(),
            ))?;

        if risk > 0.8 {
            Ok(CageDecision::Deny)
        } else if risk > 0.5 {
            Ok(CageDecision::Escalate)
        } else {
            Ok(CageDecision::Allow)
        }
    }
}
