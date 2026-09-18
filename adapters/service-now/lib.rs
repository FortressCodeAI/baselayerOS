use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::collections::HashMap;

use crate::substrate::envelope::{Envelope, EnvelopeId, EnvelopeKind};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ServiceNowRecord {
    pub sys_id: String,
    pub sys_created_on: Option<String>,
    pub number: Option<String>,
    pub short_description: Option<String>,
    pub description: Option<String>,
    pub raw: Value,
}

pub struct ServiceNowAdapter;

impl ServiceNowAdapter {
    pub fn new() -> Self {
        Self
    }

    pub fn to_envelope(&self, record: ServiceNowRecord) -> Envelope {
        let id = EnvelopeId(record.sys_id.clone());

        let timestamp = record
            .sys_created_on
            .clone()
            .unwrap_or_else(|| chrono::Utc::now().to_rfc3339());

        let mut tags = HashMap::new();
        tags.insert("provider".to_string(), "service-now".to_string());
        if let Some(num) = &record.number {
            tags.insert("ticket_number".to_string(), num.clone());
        }

        let payload = serde_json::json!({
            "short_description": record.short_description,
            "description": record.description,
            "raw": record.raw,
        });

        Envelope {
            id,
            kind: EnvelopeKind::Intent,
            source: "service-now".to_string(),
            correlation_id: None,
            timestamp,
            payload,
            tags,
        }
    }
}
