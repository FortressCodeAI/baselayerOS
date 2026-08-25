use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GovernanceEnvelope {
    pub envelope_id: String,
    pub actor_id: String,
    pub roles: Vec<String>,
    pub action_slug: String,
    pub payload: serde_json::Value,
    pub timestamp: String,
}

impl GovernanceEnvelope {
    pub fn new(
        envelope_id: impl Into<String>,
        actor_id: impl Into<String>,
        roles: Vec<String>,
        action_slug: impl Into<String>,
        payload: serde_json::Value,
        timestamp: impl Into<String>,
    ) -> Self {
        Self {
            envelope_id: envelope_id.into(),
            actor_id: actor_id.into(),
            roles,
            action_slug: action_slug.into(),
            payload,
            timestamp: timestamp.into(),
        }
    }
}
