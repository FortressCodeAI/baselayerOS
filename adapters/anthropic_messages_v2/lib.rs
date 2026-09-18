use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::collections::HashMap;

use crate::substrate::envelope::{Envelope, EnvelopeId, EnvelopeKind};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AnthropicMessageContentBlock {
    pub r#type: String,
    pub text: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AnthropicMessage {
    pub role: String,
    pub content: Vec<AnthropicMessageContentBlock>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AnthropicMessagesResponse {
    pub id: String,
    pub model: String,
    pub created_at: String,
    pub messages: Vec<AnthropicMessage>,
    pub raw: Value,
}

pub struct AnthropicMessagesAdapter;

impl AnthropicMessagesAdapter {
    pub fn new() -> Self {
        Self
    }

    pub fn to_envelope(&self, response: AnthropicMessagesResponse) -> Envelope {
        let id = EnvelopeId(response.id.clone());
        let timestamp = response.created_at.clone();

        let mut tags = HashMap::new();
        tags.insert("provider".to_string(), "anthropic".to_string());
        tags.insert("model".to_string(), response.model.clone());

        let first_text = response
            .messages
            .iter()
            .flat_map(|m| m.content.iter())
            .find_map(|b| b.text.clone());

        let payload = serde_json::json!({
            "anthropic_text": first_text,
            "raw": response.raw,
        });

        Envelope {
            id,
            kind: EnvelopeKind::Intent,
            source: "anthropic".to_string(),
            correlation_id: None,
            timestamp,
            payload,
            tags,
        }
    }
}
