use serde::{Deserialize, Serialize};


#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TenantConfig {
    pub tenant_id: String,
    pub roles: Vec<String>,
    pub routing_seal: String,
    pub settings: serde_json::Value,
}

impl TenantConfig {
    pub fn new(
        tenant_id: impl Into<String>,
        roles: Vec<String>,
        routing_seal: impl Into<String>,
        settings: serde_json::Value,
    ) -> Self {
        Self {
            tenant_id: tenant_id.into(),
            roles,
            routing_seal: routing_seal.into(),
            settings,
        }
    }
}
