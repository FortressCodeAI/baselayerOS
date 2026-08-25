use serde::{Deserialize, Serialize};

/// ExecutionEnvelope is the core unit of deterministic execution.
/// It is what Kali and the substrate use to represent an action to be applied
/// to the governed state machine.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExecutionEnvelope {
    /// Unique identifier for this envelope
    pub envelope_id: String,

    /// Actor performing the action (user, system, tenant)
    pub actor_id: String,

    /// High-level slug describing the action, e.g. "submit_grievance"
    pub action_slug: String,

    /// Arbitrary JSON payload, governed by product/workflow schemas
    pub payload: serde_json::Value,

    /// ISO-8601 timestamp of when the envelope was created
    pub timestamp: String,
}

impl ExecutionEnvelope {
    pub fn new(
        envelope_id: impl Into<String>,
        actor_id: impl Into<String>,
        action_slug: impl Into<String>,
        payload: serde_json::Value,
        timestamp: impl Into<String>,
    ) -> Self {
        Self {
            envelope_id: envelope_id.into(),
            actor_id: actor_id.into(),
            action_slug: action_slug.into(),
            payload,
            timestamp: timestamp.into(),
        }
    }
}
