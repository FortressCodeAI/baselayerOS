use crate::schemas::{ExecutionEnvelope, ExecutionResult};
use serde_json::json;

pub struct AaifAdapter;

impl AaifAdapter {
    pub fn new() -> Self {
        Self
    }

    pub fn to_aaif(&self, envelope: &ExecutionEnvelope, result: &ExecutionResult)
        -> serde_json::Value
    {
        json!({
            "aaif_version": "1.0.0",
            "execution": {
                "envelope_id": envelope.envelope_id,
                "module": envelope.state_snapshot.module,
                "transition": envelope.transition.name,
                "inputs": envelope.transition.inputs,
                "outputs": result.outputs,
                "replay_trace": result.replay_trace
            },
            "governance": {
                "policy": envelope.governance_bounds.policy,
                "rulebook_version": envelope.governance_bounds.rulebook_version
            }
        })
    }
}
