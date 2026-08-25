use anyhow::Result;

use crate::compiler::KaliCompiler;
use crate::delivery::KaliDelivery;
use crate::runtime::{WorkflowRunner, ModuleRunner, SubstrateClient};
use crate::manifest::ProductManifest;
use crate::schemas::workflow_execution::WorkflowExecution;
use crate::schemas::execution_envelope::ExecutionEnvelope;
use crate::schemas::substrate_state::SubstrateState;


pub struct KaliConsole<R> {
    compiler: KaliCompiler<R>,
    delivery: KaliDelivery,
    workflow_runner: WorkflowRunner,
    module_runner: ModuleRunner,
    substrate_client: SubstrateClient,
}

impl<R> KaliConsole<R>
where
    R: crate::kernel::KernelInvariantSource + crate::kernel::KernelConstraintSource,
{
    pub fn new(rulebook: R) -> Self {
        Self {
            compiler: KaliCompiler::new(rulebook),
            delivery: KaliDelivery::new(),
            workflow_runner: WorkflowRunner::new(),
            module_runner: ModuleRunner::new(),
            substrate_client: SubstrateClient::new(),
        }
    }

    pub async fn compile(&self, product: &str, tenant: &str) -> Result<ProductManifest> {
        println!("[console] compile: product='{}' tenant='{}'", product, tenant);

        let manifest = self.compiler.compile_product(product, tenant)?;

        println!(
            "[console] compile complete: product='{}' version='{}'",
            manifest.id, manifest.version
        );

        println!("[console] modules: {:?}", manifest.modules.iter().map(|m| &m.id).collect::<Vec<_>>());
        println!("[console] workflows: {:?}", manifest.workflows.iter().map(|w| &w.id).collect::<Vec<_>>());
        println!("[console] invariants: {:?}", manifest.invariants);
        println!("[console] constraints: {:?}", manifest.constraints);
        println!("[console] artifacts: {:?}", manifest.artifacts.iter().map(|a| &a.id).collect::<Vec<_>>());
        println!("[console] delivery: {:?}", manifest.delivery.iter().map(|d| &d.id).collect::<Vec<_>>());

        Ok(manifest)
    }

    pub async fn deliver(&self, manifest: &ProductManifest, tenant: &str) -> Result<()> {
        println!(
            "[console] deliver: product='{}' tenant='{}'",
            manifest.id, tenant
        );

        self.delivery.deliver(manifest, tenant).await?;

        println!(
            "[console] deliver complete: product='{}' tenant='{}'",
            manifest.id, tenant
        );

        Ok(())
    }

    pub async fn run_workflow(&self, workflow_id: &str, tenant: &str) -> Result<()> {
        println!(
            "[console] workflow: id='{}' tenant='{}'",
            workflow_id, tenant
        );

        let exec = WorkflowExecution::new(workflow_id, tenant, serde_json::json!({}));

        self.workflow_runner.run(exec).await?;

        println!(
            "[console] workflow complete: id='{}' tenant='{}'",
            workflow_id, tenant
        );

        Ok(())
    }

    pub async fn run_module(
        &self,
        module_id: &str,
        payload: serde_json::Value,
    ) -> Result<serde_json::Value> {
        println!("[console] module: id='{}'", module_id);

        let result = self.module_runner.execute(module_id, payload).await?;

        println!("[console] module complete: id='{}'", module_id);

        Ok(result)
    }

    pub async fn run_envelope(
        &self,
        envelope: ExecutionEnvelope,
        state: SubstrateState,
    ) -> Result<SubstrateState> {
        println!(
            "[console] envelope: id='{}' action='{}' actor='{}'",
            envelope.envelope_id, envelope.action_slug, envelope.actor_id
        );

        let result = self
            .substrate_client
            .execute_envelope(envelope.clone(), state.clone())
            .await?;

        println!(
            "[console] substrate transition: new_state_version={}",
            result.new_state.state_version
        );

        println!(
            "[console] artifacts: {:?}",
            result.artifacts.iter().map(|a| &a.id).collect::<Vec<_>>()
        );

        Ok(result.new_state)
    }
}
