use anyhow::{Result, anyhow};
use serde_json::Value;

pub fn validate_envelope(env: &Value) -> Result<()> {
    if !env.get("invariants").is_some() {
        return Err(anyhow!("Envelope missing invariants."));
    }
    Ok(())
}

pub fn validate_governance(env: &Value) -> Result<()> {
    if !env.get("identity").is_some() {
        return Err(anyhow!("Governance envelope missing identity."));
    }
    Ok(())
}

pub fn validate_policy(policy: &Value) -> Result<()> {
    if !policy.get("policy_id").is_some() {
        return Err(anyhow!("Policy missing policy_id."));
    }
    Ok(())
}

pub fn validate_module(module: &Value) -> Result<()> {
    if !module.get("invariants").is_some() {
        return Err(anyhow!("Module missing invariants."));
    }
    Ok(())
}
