use crate::audit_chain::{AuditChainBackend, AuditChainError, AuditEntry};
use serde_json::json;
use std::time::SystemTime;


pub struct SupabaseAuditChain {
    url: String,
    api_key: String,
    table: String,
}

impl SupabaseAuditChain {
    pub fn new(url: String, api_key: String, table: String) -> Self {
        Self { url, api_key, table }
    }

    async fn request(
        &self,
        method: reqwest::Method,
        body: Option<serde_json::Value>,
    ) -> Result<reqwest::Response, AuditChainError> {
        let client = reqwest::Client::new();

        let mut req = client
            .request(method, format!("{}/rest/v1/{}", self.url, self.table))
            .header("apikey", &self.api_key)
            .header("Authorization", format!("Bearer {}", self.api_key))
            .header("Content-Type", "application/json");

        if let Some(b) = body {
            req = req.body(b.to_string());
        }

        req.send()
            .await
            .map_err(|e| AuditChainError::AppendError(e.to_string()))
    }
}

#[async_trait::async_trait]
impl AuditChainBackend for SupabaseAuditChain {
    async fn append_entry(&mut self, entry: AuditEntry) -> Result<(), AuditChainError> {
        let body = json!({
            "sequence": entry.sequence,
            "envelope": entry.envelope,
            "trace": entry.trace,
            "appended_at": entry.appended_at,
        });

        let resp = self
            .request(reqwest::Method::POST, Some(body))
            .await?;

        if !resp.status().is_success() {
            return Err(AuditChainError::AppendError(format!(
                "Supabase returned status {}",
                resp.status()
            )));
        }

        Ok(())
    }

    async fn current_sequence(&self) -> Result<u64, AuditChainError> {
        let resp = self
            .request(reqwest::Method::GET, None)
            .await?;

        let json: serde_json::Value = resp
            .json()
            .await
            .map_err(|e| AuditChainError::LoadError(e.to_string()))?;

        let max_seq = json
            .as_array()
            .unwrap_or(&vec![])
            .iter()
            .filter_map(|row| row.get("sequence"))
            .filter_map(|v| v.as_u64())
            .max()
            .unwrap_or(0);

        Ok(max_seq)
    }

    async fn seal_chain(&mut self) -> Result<(), AuditChainError> {
        let now: chrono::DateTime<chrono::Utc> = SystemTime::now().into();
        let seal = json!({
            "sealed_at": now.to_rfc3339(),
        });

        let resp = self
            .request(reqwest::Method::POST, Some(seal))
            .await?;

        if !resp.status().is_success() {
            return Err(AuditChainError::SealError(format!(
                "Supabase returned status {}",
                resp.status()
            )));
        }

        Ok(())
    }
}
