use crate::registry::{
    ModuleSpec,
    WorkflowSpec,
    ArtifactSpec,
    DeliverySpec
};

#[derive(Debug, Clone)]
pub struct ProductManifest {
    pub id: String,
    pub description: String,
    pub version: String,
    pub modules: Vec<ModuleSpec>,
    pub workflows: Vec<WorkflowSpec>,
    pub invariants: Vec<String>,
    pub constraints: Vec<String>,
    pub artifacts: Vec<ArtifactSpec>,
    pub delivery: Vec<DeliverySpec>,
}
