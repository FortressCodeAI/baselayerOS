use anyhow::Result;

use crate::catalog::product_catalog::build_product_catalog;
use crate::kernel::{KernelRulebook, KernelInvariantSource, KernelConstraintSource};
use crate::manifest::ProductManifest;
use crate::registry::{
    ProductRegistry, ModuleSpec, WorkflowSpec, ArtifactSpec, DeliverySpec, ProductSpec,
};


pub struct KaliCompiler<R: KernelInvariantSource + KernelConstraintSource> {
    rulebook: R,
    registry: ProductRegistry,
}

impl<R: KernelInvariantSource + KernelConstraintSource> KaliCompiler<R> {
    pub fn new(rulebook: R) -> Self {
        let registry = build_product_catalog();
        Self { rulebook, registry }
    }

    pub fn compile_product(&self, product_id: &str, tenant: &str) -> Result<ProductManifest> {
        let product = self
            .registry
            .products
            .get(product_id)
            .ok_or_else(|| anyhow::anyhow!("Unknown product '{}'", product_id))?;

        self.rulebook
            .validate_product_constraints(product, tenant)?;

        let modules: Vec<ModuleSpec> = product
            .modules
            .iter()
            .map(|id| {
                self.registry
                    .modules
                    .get(id)
                    .cloned()
                    .ok_or_else(|| anyhow::anyhow!("Unknown module '{}' in product '{}'", id, product_id))
            })
            .collect::<Result<Vec<_>>>()?;

        let workflows: Vec<WorkflowSpec> = product
            .workflows
            .iter()
            .map(|id| {
                self.registry
                    .workflows
                    .get(id)
                    .cloned()
                    .ok_or_else(|| anyhow::anyhow!("Unknown workflow '{}' in product '{}'", id, product_id))
            })
            .collect::<Result<Vec<_>>>()?;

        let artifacts: Vec<ArtifactSpec> = product
            .artifacts
            .iter()
            .map(|id| {
                self.registry
                    .artifacts
                    .get(id)
                    .cloned()
                    .ok_or_else(|| anyhow::anyhow!("Unknown artifact '{}' in product '{}'", id, product_id))
            })
            .collect::<Result<Vec<_>>>()?;

        let delivery: Vec<DeliverySpec> = product
            .delivery
            .iter()
            .map(|id| {
                self.registry
                    .delivery
                    .get(id)
                    .cloned()
                    .ok_or_else(|| anyhow::anyhow!("Unknown delivery rule '{}' in product '{}'", id, product_id))
            })
            .collect::<Result<Vec<_>>>()?;

        let mut invariants = product.invariants.clone();
        let kernel_invariants = self.rulebook.invariants_for_product(product_id);
        invariants.extend(kernel_invariants);
        invariants.sort();
        invariants.dedup();

        let manifest = ProductManifest {
            id: product.id.clone(),
            description: product.description.clone(),
            version: product.version.clone(),
            modules,
            workflows,
            invariants,
            constraints: product.constraints.clone(),
            artifacts,
            delivery,
        };

        Ok(manifest)
    }
}
