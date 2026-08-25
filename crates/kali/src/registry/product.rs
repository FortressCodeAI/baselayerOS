use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ModuleSpec {
    pub id: String,
    pub description: String,
    pub version: String,
    pub path: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WorkflowSpec {
    pub id: String,
    pub description: String,
    pub version: String,
    pub steps: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ArtifactSpec {
    pub id: String,
    pub description: String,
    pub format: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DeliverySpec {
    pub id: String,
    pub description: String,
    pub targets: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProductSpec {
    pub id: String,
    pub description: String,
    pub version: String,
    pub modules: Vec<String>,
    pub workflows: Vec<String>,
    pub invariants: Vec<String>,
    pub constraints: Vec<String>,
    pub artifacts: Vec<String>,
    pub delivery: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProductRegistry {
    pub products: HashMap<String, ProductSpec>,
    pub modules: HashMap<String, ModuleSpec>,
    pub workflows: HashMap<String, WorkflowSpec>,
    pub artifacts: HashMap<String, ArtifactSpec>,
    pub delivery: HashMap<String, DeliverySpec>,
}

impl ProductRegistry {
    pub fn validate_product(&self, product_id: &str) -> anyhow::Result<()> {
        let product = self.products.get(product_id)
            .ok_or_else(|| anyhow::anyhow!("Unknown product '{}'", product_id))?;

        for m in &product.modules {
            if !self.modules.contains_key(m) {
                return Err(anyhow::anyhow!("Unknown module '{}' in product '{}'", m, product_id));
            }
        }

        for w in &product.workflows {
            if !self.workflows.contains_key(w) {
                return Err(anyhow::anyhow!("Unknown workflow '{}' in product '{}'", w, product_id));
            }
        }

        for a in &product.artifacts {
            if !self.artifacts.contains_key(a) {
                return Err(anyhow::anyhow!("Unknown artifact '{}' in product '{}'", a, product_id));
            }
        }

        for d in &product.delivery {
            if !self.delivery.contains_key(d) {
                return Err(anyhow::anyhow!("Unknown delivery rule '{}' in product '{}'", d, product_id));
            }
        }

        Ok(())
    }
}
