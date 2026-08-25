use crate::schemas::{ExecutionEnvelope, ExecutionResult};
use serde_json::json;

pub struct OscalkAdapter;

impl OscalkAdapter {
    pub fn new() -> Self {
        Self
    }

    pub fn to_oscalk(&self, envelope: &ExecutionEnvelope, result: &ExecutionResult)
        -> serde_json::Value
    {
        json!({
            "oscalk_execution": {
                "id": envelope.envelope_id,
                "component": envelope.state_snapshot.module,
                "transition": envelope.transition.name,
                "inputs": envelope.transition.inputs,
                "outputs": result.outputs,
                "governance": {
                    "policy": envelope.governance_bounds.policy,
                    "rulebook": envelope.governance_bounds.rulebook_version
                }
            }
        })
    }
}
