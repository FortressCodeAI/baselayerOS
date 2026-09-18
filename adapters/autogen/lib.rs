use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::collections::HashMap;

use baselayeros_substrate::envelope::{Envelope, EnvelopeId, EnvelopeKind};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AutoGenAgentMessage {
    pub sender: String,
    pub content: Value,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AutoGenConversation {
    pub id: String,
    pub agents: Vec<String>,
    pub messages: Vec<AutoGenAgentMessage>,
}

pub struct AutoGenAdapter;

impl AutoGenAdapter {
    pub fn new() -> Self {
        Self
    }

    pub fn to_envelope(&self, convo: AutoGenConversation) -> Envelope {
        let id = EnvelopeId(convo.id.clone());
        let timestamp = chrono::Utc::now().to_rfc3339();

        let mut tags = HashMap::new();
        tags.insert("provider".to_string(), "autogen".to_string());
        tags.insert("agents_count".to_string(), convo.agents.len().to_string());

        let last_message = convo
            .messages
            .last()
            .map(|m| m.content.clone())
            .unwrap_or(Value::Null);

        let payload = serde_json::json!({
            "autogen_last_message": last_message,
            "raw": convo,
        });

        Envelope {
            id,
            kind: EnvelopeKind::Intent,
            source: "autogen".to_string(),
            correlation_id: None,
            timestamp,
            payload,
            tags,
        }
    }
}
