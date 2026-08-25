use crate::errors::{GovernanceError, Refusal, ValidationError};
use crate::policy::{PolicyEngine, GovernanceContext};
use crate::schema::SchemaValidator;
use crate::perimeter::ExecutionPerimeter;

use module_sdk::envelope::{
    ExecutionEnvelope, EnvelopeDomain, EnvelopeSafetyClass
};

use serde_json::Value;

pub struct ModuleExecutor {
    policies: PolicyEngine,
    schemas: SchemaValidator,
    perimeter: ExecutionPerimeter,
}

impl ModuleExecutor {
    pub fn new(policies: PolicyEngine, schemas: SchemaValidator) -> Self {
        Self {
            policies,
            schemas,
            perimeter: ExecutionPerimeter::locked(),
        }
    }

    /// Main governed execution entrypoint.
    pub fn execute(
        &self,
        envelope: ExecutionEnvelope,
        module: fn(Value) -> Result<Value, String>,
    ) -> Result<Value, GovernanceError> {
        // 1. Schema validation
    self.schemas.validate("envelope", &serde_json::json!({
        "actor": envelope.actor,
        "intent": envelope.intent,
        "domain": format!("{:?}", envelope.domain),
        "safety_class": format!("{:?}", envelope.safety_class),
        "input": envelope.input.data
    }))?;

    // 2. Envelope → Policy Engine binding
    EnvelopePolicyBinder::evaluate(&self.policies, &envelope)?;

    // 3. Perimeter enforcement
    if !self.perimeter.is_safe() {
        return Err(GovernanceError::Refusal(Refusal {
            policy_id: "perimeter.violation".into(),
            reason: "Execution perimeter violated".into(),
        }));
    }

    // 4. Deterministic module execution
    let result = module(envelope.input.data.clone())
        .map_err(|reason| GovernanceError::Refusal(Refusal {
            policy_id: "module.execution".into(),
            reason,
        }))?;

    Ok(result)
    }
}

