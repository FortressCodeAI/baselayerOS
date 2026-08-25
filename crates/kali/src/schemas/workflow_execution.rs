use serde::{Deserialize, Serialize};


#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WorkflowExecution {
    pub workflow_id: String,
    pub tenant_id: String,
    pub inputs: serde_json::Value,
}

impl WorkflowExecution {
    pub fn new(
        workflow_id: impl Into<String>,
        tenant_id: impl Into<String>,
        inputs: serde_json::Value,
    ) -> Self {
        Self {
            workflow_id: workflow_id.into(),
            tenant_id: tenant_id.into(),
            inputs,
        }
    }
}
