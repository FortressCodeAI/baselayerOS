use crate::canonical::CanonicalEnvelope;
use serde::{Deserialize, Serialize};
use thiserror::Error;


#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum KaliGovernanceDecision {
    Allow,
    Deny,
    Escalate,
    RequireChange,
}

#[derive(Debug, Error)]
pub enum GovernanceEvaluationError {
    #[error("Envelope missing required governance metadata: {0}")]
    MissingMetadata(String),

    #[error("Invalid governance metadata: {0}")]
    InvalidMetadata(String),

    #[error("Governance rule violation: {0}")]
    RuleViolation(String),
}

pub struct KaliGovernanceEngine;

impl KaliGovernanceEngine {
    pub fn new() -> Self {
        Self
    }

    pub fn evaluate(
        &self,
        envelope: &CanonicalEnvelope,
    ) -> Result<KaliGovernanceDecision, GovernanceEvaluationError> {
        let payload = envelope
            .payload
            .as_object()
            .ok_or_else(|| GovernanceEvaluationError::InvalidMetadata(
                "Envelope payload must be an object".to_string(),
            ))?;

        let governance = payload
            .get("governance")
            .ok_or_else(|| GovernanceEvaluationError::MissingMetadata(
                "Missing governance metadata".to_string(),
            ))?;

        let governance_obj = governance
            .as_object()
            .ok_or_else(|| GovernanceEvaluationError::InvalidMetadata(
                "Governance metadata must be an object".to_string(),
            ))?;

        let role = governance_obj
            .get("role")
            .and_then(|v| v.as_str())
            .ok_or_else(|| GovernanceEvaluationError::MissingMetadata(
                "Missing governance role".to_string(),
            ))?;

        let decision = governance_obj
            .get("decision")
            .and_then(|v| v.as_str())
            .ok_or_else(|| GovernanceEvaluationError::MissingMetadata(
                "Missing governance decision".to_string(),
            ))?;

        let capabilities = governance_obj
            .get("capabilities")
            .and_then(|v| v.as_array())
            .ok_or_else(|| GovernanceEvaluationError::MissingMetadata(
                "Missing governance capabilities".to_string(),
            ))?;

        if let Some(risk_value) = governance_obj.get("risk").and_then(|v| v.as_f64()) {
            if risk_value > 0.7 {
                return Ok(KaliGovernanceDecision::Escalate);
            }
        }

        if let Some(req_approval) = governance_obj.get("requires_approval").and_then(|v| v.as_bool()) {
            if req_approval && role != "approver" {
                return Ok(KaliGovernanceDecision::Deny);
            }
        }

        match decision {
            "allow" => Ok(KaliGovernanceDecision::Allow),
            "deny" => Ok(KaliGovernanceDecision::Deny),
            "escalate" => Ok(KaliGovernanceDecision::Escalate),
            "require-change" => Ok(KaliGovernanceDecision::RequireChange),
            other => Err(GovernanceEvaluationError::InvalidMetadata(format!(
                "Invalid governance decision '{}'", other
            ))),
        }
    }
}
