use crate::schemas::ExecutionEnvelope;

pub struct GovernanceEngine;

impl GovernanceEngine {
    pub fn new() -> Self {
        Self
    }

    pub fn validate(&self, envelope: &ExecutionEnvelope) -> Result<(), String> {
        let policy = &envelope.governance_bounds.policy;

        match policy.as_str() {
            "baseline" => self.validate_baseline(envelope),
            "strict" => self.validate_strict(envelope),
            _ => Err(format!("Unknown governance policy: {}", policy)),
        }
    }

    fn validate_baseline(&self, envelope: &ExecutionEnvelope)
        -> Result<(), String>
    {
        if envelope.state_snapshot.version.is_empty() {
            return Err("Module version MUST be declared".into());
        }

        if envelope.transition.name.is_empty() {
            return Err("Transition name MUST be declared".into());
        }

        Ok(())
    }

    fn validate_strict(&self, envelope: &ExecutionEnvelope)
        -> Result<(), String>
    {
        self.validate_baseline(envelope)?;

        if envelope.invariants.is_empty() {
            return Err("Strict policy requires invariants".into());
        }

        Ok(())
    }
}
