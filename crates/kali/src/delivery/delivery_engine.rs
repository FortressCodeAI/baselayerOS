use anyhow::Result;

use crate::manifest::ProductManifest;


pub struct KaliDelivery;

impl KaliDelivery {
    pub fn new() -> Self {
        Self
    }

    pub async fn deliver(&self, manifest: &ProductManifest, tenant: &str) -> Result<()> {
        for rule in &manifest.delivery {
            match rule.id.as_str() {
                "substrate" => {
                    self.deliver_to_substrate(manifest, tenant).await?;
                }
                "supabase" => {
                    self.deliver_to_supabase(manifest, tenant).await?;
                }
                "tenant_runtime" => {
                    self.deliver_to_tenant_runtime(manifest, tenant).await?;
                }
                "partner_delivery" => {
                    self.deliver_to_partner(manifest, tenant).await?;
                }
                other => {
                    eprintln!("⚠ Unknown delivery rule '{}', skipping", other);
                }
            }
        }

        Ok(())
    }

    async fn deliver_to_substrate(&self, manifest: &ProductManifest, tenant: &str) -> Result<()> {
        // TODO: call substrate API with manifest + tenant
        println!(
            "[delivery] substrate: product='{}' tenant='{}'",
            manifest.id, tenant
        );
        Ok(())
    }

    async fn deliver_to_supabase(&self, manifest: &ProductManifest, tenant: &str) -> Result<()> {
        // TODO: upload manifest/artifacts to Supabase
        println!(
            "[delivery] supabase: product='{}' tenant='{}'",
            manifest.id, tenant
        );
        Ok(())
    }

    async fn deliver_to_tenant_runtime(&self, manifest: &ProductManifest, tenant: &str) -> Result<()> {
        // TODO: write tenant runtime config based on manifest
        println!(
            "[delivery] tenant_runtime: product='{}' tenant='{}'",
            manifest.id, tenant
        );
        Ok(())
    }

    async fn deliver_to_partner(&self, manifest: &ProductManifest, tenant: &str) -> Result<()> {
        // TODO: send manifest to partner (Google CAGE, MayIAI, etc.)
        println!(
            "[delivery] partner_delivery: product='{}' tenant='{}'",
            manifest.id, tenant
        );
        Ok(())
    }
}
