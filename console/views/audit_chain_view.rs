use serde_json::json;
use baselayeros_substrate::audit_chain_local::LocalAuditChain;
use std::sync::{Arc, Mutex};


pub struct AuditChainView {
    audit: Arc<Mutex<LocalAuditChain>>,
}

impl AuditChainView {
    pub fn new(audit: Arc<Mutex<LocalAuditChain>>) -> Self {
        Self { audit }
    }

    pub fn render(&self) -> serde_json::Value {
        let audit = self.audit.lock().unwrap();
        let entries = audit.read_all().expect("audit read");

        let rendered: Vec<serde_json::Value> = entries
            .into_iter()
            .map(|entry| {
                json!({
                    "sequence": entry.sequence,
                    "envelopeId": entry.envelope_id,
                    "attestation": entry.attestation,
                })
            })
            .collect();

        json!({
            "audit_chain": rendered,
            "count": rendered.len()
        })
    }
}
