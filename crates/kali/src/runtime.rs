use anyhow::Result;

pub struct KaliRuntime;

impl KaliRuntime {
    pub fn new() -> Self {
        Self
    }

    pub async fn run_workflow(&self, workflow_id: &str, tenant: &str) -> Result<()> {
        println!("Running workflow '{}' for tenant '{}'", workflow_id, tenant);
        Ok(())
    }
}
