use crate::errors::{GovernanceError, Refusal};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
pub struct PolicyId(pub String);

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum PolicyOutcome {
    Allow,
    Deny(String),
    Escalate(String),
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GovernanceContext {
    pub actor: String,
    pub intent: String,
    pub domain: String,
    pub safety_class: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Policy {
    pub id: PolicyId,
    pub description: String,
    pub rule: Box<dyn Fn(&GovernanceContext) -> PolicyOutcome + Send + Sync>,
}

impl Policy {
    pub fn evaluate(&self, ctx: &GovernanceContext) -> PolicyOutcome {
        (self.rule)(ctx)
    }
}

pub struct PolicyEngine {
    policies: Vec<Policy>,
}

impl PolicyEngine {
    pub fn new() -> Self {
        Self { policies: Vec::new() }
    }

    pub fn register(&mut self, policy: Policy) {
        self.policies.push(policy);
    }

    pub fn evaluate(&self, ctx: &GovernanceContext) -> Result<(), GovernanceError> {
        for policy in &self.policies {
            match policy.evaluate(ctx) {
                PolicyOutcome::Allow => continue,
                PolicyOutcome::Deny(reason) => {
                    return Err(GovernanceError::Refusal(Refusal {
                        policy_id: policy.id.0.clone(),
                        reason,
                    }))
                }
                PolicyOutcome::Escalate(reason) => {
                    return Err(GovernanceError::Escalation {
                        policy_id: policy.id.0.clone(),
                        reason,
                    })
                }
            }
        }
        Ok(())
    }
}

pub fn default_policies() -> PolicyEngine {
    let mut engine = PolicyEngine::new();

    // High‑risk safety class refusal
    engine.register(Policy {
        id: PolicyId("safety.high_risk_block".into()),
        description: "Block high‑risk intents",
        rule: Box::new(|ctx| {
            if ctx.safety_class == "high-risk" {
                PolicyOutcome::Deny("High‑risk intent refused".into())
            } else {
                PolicyOutcome::Allow
            }
        }),
    });

    // Domain‑restricted governance
    engine.register(Policy {
        id: PolicyId("domain.restricted".into()),
        description: "Block forbidden domains",
        rule: Box::new(|ctx| {
            if ctx.domain == "forbidden" {
                PolicyOutcome::Deny("Domain is forbidden".into())
            } else {
                PolicyOutcome::Allow
            }
        }),
    });

    engine
}
