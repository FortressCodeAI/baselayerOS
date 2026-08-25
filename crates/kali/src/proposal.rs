use serde::{Serialize, Deserialize};
use serde_json::Value;

use crate::identity::ActorIdentity;

/// The object Kali hands to the substrate integration layer.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GovernedProposal {
    pub module_id: String,
    pub version: String,
    pub envelope_id: String,
    pub payload: Value,
    pub tenant_id: String,
    pub actor_id: String,
    pub trace_id: String,
    pub timestamp: String,
    pub roles: Vec<String>,
}

impl GovernedProposal {
    pub fn new(
        module_id: impl Into<String>,
        version: impl Into<String>,
        envelope_id: impl Into<String>,
        payload: Value,
        identity: &ActorIdentity,
        trace_id: impl Into<String>,
        timestamp: impl Into<String>,
    ) -> Self {
        Self {
            module_id: module_id.into(),
            version: version.into(),
            envelope_id: envelope_id.into(),
            payload,
            tenant_id: identity.tenant_id.clone(),
            actor_id: identity.actor_id.clone(),
            trace_id: trace_id.into(),
            timestamp: timestamp.into(),
            roles: identity.roles.clone(),
        }
    }
}
