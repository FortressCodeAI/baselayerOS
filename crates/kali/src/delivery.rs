use crate::manifest::ProductManifest;
use anyhow::Result;

pub struct KaliDelivery;

impl KaliDelivery {
    pub fn new() -> Self {
        Self
    }

    pub async fn deliver(&self, manifest: &ProductManifest, tenant: &str) -> Result<()> {
        for rule in &manifest.delivery {
            match rule.id.as_str() {
                "substrate" => {
                    // TODO: call substrate API
                }
                "supabase" => {
                    // TODO: upload bundle
                }
                "tenant_runtime" => {
                    // TODO: write tenant config
                }
                "partner_delivery" => {
                    // TODO: send to partner
                }
                _ => {}
            }
        }
        Ok(())
    }
}
