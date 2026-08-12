use crate::governance_sdk::errors::GovernanceError;
use crate::schemas::ExecutionEnvelope;

pub struct GovernancePerimeter;

impl GovernancePerimeter {
    pub fn new() -> Self {
        Self
    }

    pub fn enforce_policy_bounds(
        &self,
        envelope: &ExecutionEnvelope
    ) -> Result<(), GovernanceError> {
        if envelope.governance_bounds.policy.is_empty() {
            return Err(GovernanceError::UnknownPolicy(
                "Policy MUST be declared".into()
            ));
        }

        if envelope.governance_bounds.rulebook_version.is_empty() {
            return Err(GovernanceError::RulebookViolation(
                "Rulebook version MUST be declared".into()
            ));
        }

        Ok(())
    }
}
