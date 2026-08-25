use anyhow::Result;
use serde_json::json;

use crate::runtime::WorkflowRunner;
use crate::schemas::workflow_execution::WorkflowExecution;


pub struct KaliMarketing {
    workflow_runner: WorkflowRunner,
}

impl KaliMarketing {
    pub fn new() -> Self {
        Self {
            workflow_runner: WorkflowRunner::new(),
        }
    }

    pub async fn deploy_campaign(&self, product: &str, tenant: &str) -> Result<()> {
        println!(
            "[marketing] deploying campaign for product='{}' tenant='{}'",
            product, tenant
        );

        let workflow_id = match product {
            "marketing-pack" => "marketing_campaign_workflow",
            "governance-pack" => "governance_marketing_workflow",
            "sales-pack" => "sales_marketing_workflow",
            other => {
                println!("[marketing] no workflow mapped for product '{}'", other);
                return Ok(());
            }
        };

        let exec = WorkflowExecution::new(
            workflow_id,
            tenant,
            json!({
                "product": product,
                "tenant": tenant,
                "operation": "deploy_campaign"
            }),
        );

        self.workflow_runner.run(exec).await?;

        println!(
            "[marketing] campaign deployed for product='{}' tenant='{}'",
            product, tenant
        );

        Ok(())
    }
}
