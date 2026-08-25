use anyhow::Result;
use serde_json::json;

use crate::catalog::workflow_catalog::build_workflow_catalog;
use crate::schemas::workflow_execution::WorkflowExecution;

pub struct WorkflowRunner;

impl WorkflowRunner {
    pub fn new() -> Self {
        Self
    }

    pub async fn run(&self, exec: WorkflowExecution) -> Result<()> {
        let catalog = build_workflow_catalog();

        let workflow = catalog
            .get(&exec.workflow_id)
            .ok_or_else(|| anyhow::anyhow!("Unknown workflow '{}'", exec.workflow_id))?;

        println!(
            "[runtime] Starting workflow '{}' for tenant '{}'",
            workflow.id, exec.tenant_id
        );

        for step in &workflow.steps {
            self.execute_step(step, &exec).await?;
        }

        println!(
            "[runtime] Completed workflow '{}' for tenant '{}'",
            workflow.id, exec.tenant_id
        );

        Ok(())
    }

    async fn execute_step(&self, step: &str, exec: &WorkflowExecution) -> Result<()> {
        println!(
            "[runtime] step='{}' workflow='{}' tenant='{}'",
            step, exec.workflow_id, exec.tenant_id
        );

        // Placeholder: real module execution will be wired in Pair #10
        let _result = json!({
            "step": step,
            "workflow": exec.workflow_id,
            "tenant": exec.tenant_id,
            "inputs": exec.inputs,
        });

        Ok(())
    }
}
