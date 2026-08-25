use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SubstrateState {
    pub state_version: u64,
    pub transition_hash: String,
    pub audit_anchor: String,
    pub data: serde_json::Value,
}

impl SubstrateState {
    pub fn new(
        state_version: u64,
        transition_hash: impl Into<String>,
        audit_anchor: impl Into<String>,
        data: serde_json::Value,
    ) -> Self {
        Self {
            state_version,
            transition_hash: transition_hash.into(),
            audit_anchor: audit_anchor.into(),
            data,
        }
    }
}
