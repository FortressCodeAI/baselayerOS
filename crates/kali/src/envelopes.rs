use serde::{Serialize, Deserialize};
use serde_json::Value;

use crate::identity::ActorIdentity;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExecutionEnvelope {
    pub envelope_id: String,
    pub actor_id: String,
    pub tenant_id: String,
    pub action_slug: String,
    pub timestamp_ms_hex: String,
    pub record_hash_hex: String,
    pub state_snapshot: Value,
}

/// Minimal governance envelope Kali builds for governance engines (MayIAI, CAGE, etc.).
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GovernanceEnvelope {
    pub envelope_id: String,
    pub actor_id: String,
    pub tenant_id: String,
    pub action_slug: String,
    pub timestamp_ms_hex: String,
    pub record_hash_hex: String,
    pub routing_seal: String,
    pub invariants: Vec<String>,
}

impl ExecutionEnvelope {
    pub fn new(
        envelope_id: impl Into<String>,
        identity: &ActorIdentity,
        action_slug: impl Into<String>,
        timestamp_ms_hex: impl Into<String>,
        record_hash_hex: impl Into<String>,
        state_snapshot: serde_json::Value,
    ) -> Self {
        Self {
            envelope_id: envelope_id.into(),
            actor_id: identity.actor_id.clone(),
            tenant_id: identity.tenant_id.clone(),
            action_slug: action_slug.into(),
            timestamp_ms_hex: timestamp_ms_hex.into(),
            record_hash_hex: record_hash_hex.into(),
            state_snapshot,
        }
    }
}

impl GovernanceEnvelope {
    pub fn new(
        envelope_id: impl Into<String>,
        identity: &ActorIdentity,
        action_slug: impl Into<String>,
        timestamp_ms_hex: impl Into<String>,
        record_hash_hex: impl Into<String>,
        routing_seal: impl Into<String>,
        invariants: Vec<String>,
    ) -> Self {
        Self {
            envelope_id: envelope_id.into(),
            actor_id: identity.actor_id.clone(),
            tenant_id: identity.tenant_id.clone(),
            action_slug: action_slug.into(),
            timestamp_ms_hex: timestamp_ms_hex.into(),
            record_hash_hex: record_hash_hex.into(),
            routing_seal: routing_seal.into(),
            invariants,
        }
    }
}
