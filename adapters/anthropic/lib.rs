use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::collections::HashMap;

use baselayeros_substrate::envelope::{Envelope, EnvelopeId, EnvelopeKind};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AnthropicContentBlock {
    pub r#type: String,
    pub text: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AnthropicResponse {
    pub id: String,
    pub model: String,
    pub created_at: String,
    pub content: Vec<AnthropicContentBlock>,
}

pub struct AnthropicAdapter;

impl AnthropicAdapter {
    pub fn new() -> Self {
        Self
    }

    pub fn to_envelope(&self, response: AnthropicResponse) -> Envelope {
        let id = EnvelopeId(response.id.clone());
        let timestamp = response.created_at.clone();

        let mut tags = HashMap::new();
        tags.insert("provider".to_string(), "anthropic".to_string());
        tags.insert("model".to_string(), response.model.clone());

        let first_text = response
            .content
            .iter()
            .find_map(|block| block.text.clone());

        let payload = serde_json::json!({
            "anthropic_text": first_text,
            "raw": response,
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
