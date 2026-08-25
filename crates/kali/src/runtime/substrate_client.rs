use anyhow::Result;
use serde_json::json;

use crate::schemas::{
    ExecutionEnvelope,
    TransitionResult,
    SubstrateState,
};
use crate::registry::ArtifactSpec;


pub struct SubstrateClient;

impl SubstrateClient {
    pub fn new() -> Self {
        Self
    }

    pub async fn execute_envelope(
        &self,
        envelope: ExecutionEnvelope,
        current_state: SubstrateState,
    ) -> Result<TransitionResult> {
        println!(
            "[substrate] envelope='{}' action='{}' actor='{}'",
            envelope.envelope_id, envelope.action_slug, envelope.actor_id
        );

        // Placeholder deterministic transition
        let new_state = SubstrateState {
            state_version: current_state.state_version + 1,
            transition_hash: format!("hash_{}", envelope.envelope_id),
            audit_anchor: format!("anchor_{}", envelope.envelope_id),
            data: json!({
                "previous": current_state.data,
                "envelope": envelope.payload,
            }),
        };

        // Placeholder artifact
        let artifact = ArtifactSpec {
            id: format!("artifact_{}", envelope.envelope_id),
            description: "Deterministic transition artifact".into(),
            format: "json".into(),
        };

        let result = TransitionResult {
            new_state,
            artifacts: vec![artifact],
        };

        println!(
            "[substrate] transition complete: new_state_version={}",
            result.new_state.state_version
        );

        Ok(result)
    }
}
