use crate::policy::{GovernanceContext, PolicyEngine};
use crate::errors::{GovernanceError};
use module_sdk::envelope::{ExecutionEnvelope};

/// Deterministic binder that converts an ExecutionEnvelope
/// into a GovernanceContext for policy evaluation.
pub struct EnvelopePolicyBinder;

impl EnvelopePolicyBinder {
    pub fn bind(envelope: &ExecutionEnvelope) -> GovernanceContext {
        GovernanceContext {
            actor: envelope.actor.clone(),
            intent: envelope.intent.clone(),
            domain: format!("{:?}", envelope.domain),
            safety_class: format!("{:?}", envelope.safety_class),
        }
    }

    /// Evaluate policies directly from an envelope.
    pub fn evaluate(
        engine: &PolicyEngine,
        envelope: &ExecutionEnvelope,
    ) -> Result<(), GovernanceError> {
        let ctx = Self::bind(envelope);
        engine.evaluate(&ctx)
    }
}
