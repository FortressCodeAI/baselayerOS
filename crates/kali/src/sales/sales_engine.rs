use anyhow::Result;
use serde_json::json;

use crate::runtime::WorkflowRunner;
use crate::schemas::workflow_execution::WorkflowExecution;


pub struct KaliSales {
    workflow_runner: WorkflowRunner,
}

impl KaliSales {
    pub fn new() -> Self {
        Self {
            workflow_runner: WorkflowRunner::new(),
        }
    }

    pub async fn run_pipeline(&self, product: &str, tenant: &str) -> Result<()> {
        println!(
            "[sales] running pipeline for product='{}' tenant='{}'",
            product, tenant
        );

        let workflow_id = match product {
            "sales-pack" => "sales_pipeline_workflow",
            "marketing-pack" => "marketing_sales_workflow",
            "governance-pack" => "governance_sales_workflow",
            other => {
                println!("[sales] no workflow mapped for product '{}'", other);
                return Ok(());
            }
        };

        let exec = WorkflowExecution::new(
            workflow_id,
            tenant,
            json!({
                "product": product,
                "tenant": tenant,
                "operation": "run_pipeline"
            }),
        );

        self.workflow_runner.run(exec).await?;

        println!(
            "[sales] pipeline completed for product='{}' tenant='{}'",
            product, tenant
        );

        Ok(())
    }
}
